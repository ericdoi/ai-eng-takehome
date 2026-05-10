# Current State (handoff reference)

## Where we are

Best scores: **62.5% easy (40/64), 39.1% hard (25/64)** — Run 1, committed as `482a275`.

Phase 2 (generated guides + `find_schema` tool) is implemented and committed as `da80184`
(Run 6: 21/64 hard, 32.8%). Navigation is now solved — AGENT_ERROR fell to 2, schema
identification 94%, table identification 84%. The sole remaining bottleneck is **business-rule
application**: 33 of 54 right-table cases still produce wrong SQL.

Next action: implement five targeted fixes from `context/PLAN_business_logic.md`, regenerate
guides for the 7 top-failing schemas, and run eval (Run 7). Do NOT regenerate all 76 schemas
yet — test iteratively.

## Code state (committed, `da80184` / `ac0526a`)

All Phase 2 changes are committed. Working tree is clean.

| File | Role |
|------|------|
| `scripts/build_schema_guides.py` | Offline guide synthesis + embedding pipeline |
| `tools/schema_guide_tools.py` | `find_schema` tool — cosine similarity over 76 guides |
| `evaluation/evaluate.py` | `create_tools()`: find_schema, list_tables, describe_table, run_sql, submit_answer |
| `interactive.py` | Same tool set |
| `framework/agent.py` | System prompt: find_schema → run_sql → submit; schema-name verbatim rule |
| `evaluation/data/generated_guides/*.md` | 76 LLM-synthesized schema guides (committed) |
| `evaluation/data/generated_guides/embeddings.npz` | 76×1536 float32, L2-normalized (committed) |

**Disabled (code present, not wired):** `search_guides`, `read_guide` (`tools/guide_tools.py`),
`list_schemas`, `sample_rows`, `search_columns` (`tools/db_tools.py`).

## Pending changes (not yet implemented)

Five fixes from `context/PLAN_business_logic.md` — all code changes, no guide regen yet:

| Fix | File | Description |
|-----|------|-------------|
| 1 | `scripts/build_schema_guides.py` | Synthesis prompt: IDENTIFY vs EXCLUDE rule framing; explicit rate denominators |
| 2 | `scripts/build_schema_guides.py` | `textualize_schema()`: detect date sentinel values (9999-01-01, epoch zeros, dominant single value) |
| 3 | `scripts/build_schema_guides.py` | Synthesis prompt: label join paths as [REQUIRED] vs [OPTIONAL — display only] |
| 4 | `scripts/build_schema_guides.py` | Add `--model` CLI flag; regen financial with `anthropic/claude-sonnet-4-6` |
| 5 | `framework/agent.py` | System prompt: "Use LEFT JOIN for lookup/optional tables" |

After implementing, regen these 7 schemas (top Run 6 failures) and re-embed:
**financial, Credit, Airline, lahman_2014, Chess, employee, ErgastF1**

## How to run the eval

```bash
source .env && uv run evaluate --api-key "$OPENROUTER_API_KEY" --split hard --concurrency 16
```

Single schema regen (then re-embed after all 7 done):
```bash
source .env && uv run python scripts/build_schema_guides.py --schema financial --skip-embed
# after all 7 schemas:
source .env && uv run python scripts/build_schema_guides.py --skip-llm
```

Analyze a run:
```bash
uv run python scripts/analyze_run.py logs/run_<timestamp>/ --split hard
uv run python scripts/analyze_run.py logs/run_<timestamp>/ --split hard --csv context/runN_hard.csv
```

API budget: **~$12.68 remaining** as of 2026-05-10 (~$1.05/full guide regen, ~$1.70/hard-only
eval run, ~$3.30/both-splits run, ~$0.05-0.10/single Sonnet schema). Check balance:
```bash
curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $(grep OPENROUTER_API_KEY .env | cut -d= -f2)" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(f'remaining: \${d[\"limit_remaining\"]:.2f}')"
```

## Key config (in `framework/llm.py`)

- `temperature`: **0.1**
- `compress_context`: **True**
- `compress_max_chars`: **400**

## Run 6 failure analysis

Root causes identified in `context/issues/business_logic_failures.md`:

| Pattern | Schemas affected | Root cause |
|---------|-----------------|------------|
| Lookup-table joins for aggregations | Airline (6) | Guide join paths listed without REQUIRED/OPTIONAL labels; agent uses them unnecessarily |
| Inverted/ambiguous business-rule SQL | financial (7) | Synthesizer labeled exclusion filter as definition (NOT IN vs IN confusion) |
| Missing rate denominators | financial | Source rule "exclude B from rate" never given as explicit SQL denominator |
| Date sentinel not surfaced | employee (4) | Textualization only covers VARCHAR distinct values, not DATE sentinels |
| Optional table join drops rows | Chess (4) | INNER JOIN to opening table silently drops unmatched games |

## Eval variance note

The hard split shows ~±8 case variance between identical-code runs (n=64, temp=0.1).
A result is only clearly meaningful if hard pass rate reaches **≥30/64 (≥47%)**.

## Known issues

| Issue | Status | Notes |
|-------|--------|-------|
| Wrong logic / business-rule misses | **Active bottleneck** | 33 wrong-logic cases in Run 6; fixes in progress |
| AGENT_ERROR re-exploration loop | **Resolved** (Run 6: 2 errors) | Schema name banner in find_schema response + prompt verbatim rule |
| `search_columns` regression | Closed | Reverted; code kept. See `runs/run2_search_columns.md` |
| ~7 continuation-prompt injections/run | Open | Model outputs JSON as text; minor, not prioritised |
