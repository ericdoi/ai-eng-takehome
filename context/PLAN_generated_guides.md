# Plan: LLM-Synthesized Schema Guides

## Problem

The current approach keeps two knowledge sources separate:

- **Guides** (`evaluation/data/guides/`) — business rules only; no table names, column names, or join paths
- **DB tools** (`list_schemas`, `list_tables`, `describe_table`) — schema facts only; no business rules

The agent has to reconcile these at query time, under iteration pressure, in 30 turns. This
produces two failure modes that are hard to fix with prompt engineering alone:

- **AGENT_ERROR / NO_SUBMISSION** — agent loops calling `list_schemas` while trying to
  reconcile a schema name from the guide snippet with the actual database structure
- **MISMATCH** — agent finds the right table but applies the wrong filter threshold, missing
  WHERE condition, or wrong column because the rules weren't connected to specific column names

Prompt fixes (Runs 3, 4) helped with loops but caused table-name hallucination and were brittle.
Soft rules caused massive regression. Root cause is structural, not prompt-tunable.

## Solution

Build a preprocessing pipeline that fuses both knowledge sources into per-schema
**generated guides**: rich documents combining exact schema structure with business rules
rewritten in SQL terms. Then embed and index them so the agent can retrieve everything it
needs in one tool call.

The agent workflow simplifies from:
```
search_guides → read_guide → list_schemas → list_tables → describe_table → run_sql → submit
```
to:
```
find_schema → run_sql → submit
```

## Architecture

```
[DuckDB]                    [evaluation/data/guides/]
    │                                  │
    ▼                                  ▼
textualize_schema()         read_guide_for_schema()
(tables + columns + samples)  (business rules, if any)
    │                                  │
    └──────────────┬───────────────────┘
                   ▼
           LLM synthesis prompt
                   │
                   ▼
     evaluation/data/generated_guides/<schema>.md
                   │
                   ▼
           embed via OpenRouter
                   │
                   ▼
     evaluation/data/generated_guides/embeddings.npz
                   │
                   ▼
         tools/schema_guide_tools.py
              find_schema(query)
```

## Step 1 — Build script (`scripts/build_schema_guides.py`)

### 1a. Schema enumeration

```python
conn = duckdb.connect("hecks.duckdb", read_only=True)
schemas = conn.execute(
    "SELECT schema_name FROM information_schema.schemata "
    "WHERE schema_name NOT IN ('information_schema','main','pg_catalog','temp')"
).fetchall()
# → 76 schemas
```

### 1b. Textualization

For each schema, produce a structured text block:

```
Schema: world
Tables: City, Country, CountryLanguage

Table: Country (4 columns)
Columns:
  Code       VARCHAR  — primary key
  Name       VARCHAR
  Continent  VARCHAR  — values: Asia, Europe, North America, Africa, Oceania, Antarctica, South America
  Region     VARCHAR
  SurfaceArea REAL
  Population  INTEGER
  ...

Sample rows (Country):
| Code | Name        | Continent | Population |
| AFG  | Afghanistan | Asia      | 22720000   |
| ALB  | Albania     | Europe    | 3401200    |
...

Table: CountryLanguage (4 columns)
Columns:
  CountryCode  VARCHAR
  Language     VARCHAR
  IsOfficial   CHAR(1)  — values: T, F
  Percentage   REAL     — speaker percentage 0–100
...
```

Use `LIMIT 5` samples per table. For `VARCHAR` columns with few distinct values
(count ≤ 20), include all distinct values — they resolve disambiguation fast (e.g.,
`IsOfficial` is `T`/`F` not `1`/`0`).

### 1c. Guide-schema mapping

50 guide files cover a superset of the 76 schemas (some guides are for schemas outside
the dev eval set — likely in the held-out test set, so generate all of them).

Mapping approach (in priority order):
1. **H1 parenthetical extraction** (already implemented): `(ErgastF1 Database)` → `ErgastF1`.
   Take only the first token before ` / ` for multi-schema guides.
2. **Known overrides** (hard-coded dict for mismatches between guide filenames and schema names):
   ```python
   GUIDE_OVERRIDES = {
       "movie_ratings.md":         "imdb_MovieLens",
       "world_geography.md":       "world",
       "f1_racing_metrics.md":     "ErgastF1",
       "credit_card_operations.md": "Credit",
       "employee_hr_policies.md":  "employee",
       "hockey_analytics.md":      "Hockey",
       "baseball_sabermetrics.md": "lahman_2014",
       # add others as discovered
   }
   ```
3. **No guide** — generate schema-only documentation for unmatched schemas.

Build a `schema_to_guide: dict[str, Path | None]` mapping before the LLM calls.

### 1d. LLM synthesis prompt

One call per schema. Use a fast, capable model (e.g. `google/gemini-flash-1.5-8b` or
`anthropic/claude-haiku-4-5` for cost efficiency; ~$0.10 for all 76 schemas).

```
System: You are a database documentation expert writing reference guides for an AI SQL agent.
Be precise. Use exact names. Never invent column names not present in the schema.

User:
Here is the full schema structure for the `{schema}` schema:

<schema>
{textualized_schema}
</schema>

{f'Here are the business rules for this schema:\n\n<rules>\n{guide_content}\n</rules>' if guide_content else ''}

Write a comprehensive reference guide for an AI SQL agent that needs to write SQL queries
against this schema. Include:

1. **Schema summary**: one sentence describing what this schema contains.

2. **Table reference** (for each table):
   - Exact table name (case-sensitive) and qualified form: `{schema}.TableName`
   - Plain-English meaning and common synonym names
   - Each column: exact name, type, meaning, and common synonyms or aliases
   - Notable values or enumerations (include exact strings/values from sample data)

3. **Join paths**: exact SQL JOIN conditions between related tables.

4. **Business rules as SQL** (if rules provided): restate each rule as the exact SQL
   condition, column reference, or JOIN pattern that implements it. Format:
   - Rule: "language percentage exceeds 90%" → `WHERE cl.Percentage > 90`
   - Rule: "on-time flight" → `WHERE ArrDelayMinutes <= 15`
   - Rule: "performing loan" → `WHERE status = 'A'`

5. **Synonym glossary**: map common question terms to exact schema identifiers.
   Format: "career hits" → `SUM(batting.H)`, "dominant language" → `CountryLanguage WHERE Percentage > 90`

Keep the guide focused and scannable. Do not add caveats or padding.
```

### 1e. Output

Save each generated guide to:
```
evaluation/data/generated_guides/<schema_name>.md
```

One file per schema. Even schemas with no guide get a generated file (schema-only).
The directory should be created by the script if absent.

---

## Step 2 — Embedding index

After all guides are generated, embed them for semantic retrieval.

**Model:** `openai/text-embedding-3-small` via OpenRouter `/v1/embeddings`.
Cost: 76 guides × ~2K tokens = ~150K tokens ≈ $0.003. Negligible.

**Storage:** Save to `evaluation/data/generated_guides/embeddings.npz`:
```python
np.savez(
    "embeddings.npz",
    schema_names=np.array(schema_names),          # shape (76,)
    embeddings=np.array(embedding_matrix),         # shape (76, 1536)
)
```

**Retrieval at query time:**
```python
q_vec = embed(query)                    # (1536,)
scores = embeddings @ q_vec             # cosine similarity (already unit-normalized)
top_k = np.argsort(scores)[::-1][:k]
```

No vector DB needed — 76 × 1536-float cosine is microseconds in numpy.

**Why embeddings over BM25 here:** Generated guides contain both exact identifiers
(`Percentage`, `IsOfficial`) and rich natural language descriptions and synonyms.
The query "on-time flights" will match `ArrDelayMinutes <= 15` via embeddings but
not via BM25 token overlap. This is the paraphrase gap the original guides exposed.

---

## Step 3 — New retrieval tool (`tools/schema_guide_tools.py`)

Replace `search_guides` + `read_guide` with a single tool:

```python
FIND_SCHEMA = Tool(
    name="find_schema",
    description=(
        "Find the schema guide most relevant to your question. "
        "Returns the full guide including exact table names, column names, join paths, "
        "business rules as SQL conditions, and a synonym glossary. "
        "Call this first — it gives you everything you need to write the SQL."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Your question or key domain terms from it.",
            }
        },
        "required": ["query"],
    },
    function=_find_schema_fn,
)
```

`_find_schema_fn` returns the full text of the best-matching generated guide.
If the top score is below a confidence threshold (< 0.3), return the top 2 guides
concatenated so the agent can pick.

Keep `list_tables` and `describe_table` wired as fallbacks — the agent may still need
them for schemas with poor guide coverage or to verify a specific column type.

---

## Step 4 — Updated agent workflow

New system prompt (replacing the current WORKFLOW + STRICT RULES blocks):

```
WORKFLOW:
1. find_schema — always your first call. Returns exact table names, column names, join
   paths, and business rules as SQL. Read the full guide before writing any SQL.
2. run_sql — verify your query returns the right shape of results.
3. submit_answer — submit your final SQL.

If find_schema doesn't name the exact columns you need, use list_tables(schema) and
describe_table(schema, table) to fill gaps. Never guess column names.
```

The anti-loop rules become unnecessary — there's no reason to call `list_schemas`
repeatedly when a single `find_schema` call gives the full picture.

---

## Step 5 — Validation (before running the full eval)

Before running the eval, spot-check generated guides for 5–10 schemas:

1. **Accuracy check**: Do the table names in the guide match `list_tables` output exactly?
   (Case matters: `Country` not `country`.)
2. **Rule fidelity**: For schemas with guides (world, ErgastF1, Credit), do the SQL
   conditions in the generated guide match the gold queries' WHERE clauses?
3. **Hallucination check**: Are there any column names in the guide that don't appear in
   `describe_table` output?

A fast automated check:
```python
for schema, guide_path in generated.items():
    guide_text = guide_path.read_text()
    actual_tables = set(list_tables(schema))
    for table in actual_tables:
        assert f"{schema}.{table}" in guide_text, f"Missing: {schema}.{table}"
```

---

## Implementation order

1. **Revert** working tree to Run 1 state (clean baseline)
2. **Write `scripts/build_schema_guides.py`**:
   - Textualization (no LLM, just DB queries)
   - Guide-schema mapping dict
   - LLM synthesis loop (with retry + rate-limit handling)
   - Embedding generation + npz save
3. **Run the build script** (~2–3 min, ~$0.15 total API cost)
4. **Spot-check** 5 generated guides manually
5. **Write `tools/schema_guide_tools.py`** (`find_schema` tool)
6. **Wire into `evaluate.py` and `interactive.py`**
7. **Update system prompt** (simplified workflow)
8. **Test interactively** on 2–3 cases from the known failure set
9. **Run hard eval** and record results

---

## Cost estimate

| Step | Model | Tokens | Cost |
|------|-------|--------|------|
| Textualization | (DB queries only) | — | $0 |
| LLM synthesis (76 schemas) | gemini-flash or haiku | ~380K | ~$0.10 |
| Embedding (76 guides) | text-embedding-3-small | ~150K | ~$0.003 |
| Eval run (hard split) | eval model | ~2M | ~$0.33 |
| **Total** | | | **~$0.45** |

---

## Risks and mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| LLM hallucinate column name in generated guide | Medium | Automated validation step; keep `describe_table` as fallback |
| Guide doesn't cover the right schema | Low | Build script prints unmapped schemas; GUIDE_OVERRIDES dict is easy to extend |
| Generated guide too long for context | Low | 76 schemas avg ~50 columns; guides should stay under 2K tokens |
| Embedding retrieval picks wrong schema | Low | Return top-2 if score gap is small; agent can call `find_schema` again with different terms |
| Build script takes too long / hits rate limits | Low | Add `time.sleep(0.5)` between LLM calls; use batch embedding API |

## If this doesn't work

If embedding retrieval is the bottleneck (wrong schema returned), add BM25 hybrid
(Reciprocal Rank Fusion over BM25 + cosine scores) — one extra 20-line function.

If generated guide quality is the bottleneck (hallucinated rules), fall back to
separating synthesis from embedding: generate guides without the rules section,
then retrieve the original guide separately with the current BM25 tool.
