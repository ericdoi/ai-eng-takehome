# Current State (handoff reference)

## Where we are

Best scores: **62.5% easy (40/64), 39.1% hard (25/64)** — Run 1, committed as `482a275`.

All subsequent runs (2–4, 1′) regressed or matched Run 1. Prompt-engineering attempts to
fix the AGENT_ERROR re-exploration loop were abandoned after the navigation funnel analysis
showed that wrong logic (27–43 cases/run) dominates wrong schema (0–8) and wrong tables
(0–12) in every run. Better navigation doesn't convert to better scores.

**Current approach:** build LLM-synthesized schema guides that fuse exact DB structure with
business rules as SQL conditions, then retrieve via embeddings. Plan: `context/PLAN_generated_guides.md`.

## Code state

Working tree is **clean at Run 1** (`482a275`). No staged changes to agent or tools.

```bash
git status   # should show only context/ and scripts/ modifications
git stash    # if any accidental edits exist
```

## How to run the eval

```bash
source .env && uv run evaluate --api-key "$OPENROUTER_API_KEY" --split both --concurrency 16
```

API key is in `.env` (git-ignored). Traces saved to `logs/run_<timestamp>/`. After a run:

```bash
uv run python scripts/analyze_run.py logs/run_<timestamp>/ --split hard
uv run python scripts/analyze_run.py logs/run_<timestamp>/ --split hard --csv context/runN_hard.csv
```

The analyzer now shows a three-stage navigation funnel (right schema / right tables / right
logic) and per-case tool sequences. Check RESULTS.md for the funnel data across all runs.

API budget: ~$18 remaining (~$0.33/hard-only run, ~$0.65/both). Check balance:
```bash
curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $(grep OPENROUTER_API_KEY .env | cut -d= -f2)" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(f'remaining: \${d[\"limit_remaining\"]:.2f}')"
```

## Active tools (wired in `evaluate.py` and `interactive.py`)

| Tool | File | Notes |
|------|------|-------|
| `search_guides` | `tools/guide_tools.py` | BM25 over `##`-chunked guide files |
| `read_guide` | `tools/guide_tools.py` | Returns full guide file content |
| `list_schemas` | `tools/db_tools.py` | Lists all 76 schemas |
| `list_tables` | `tools/db_tools.py` | Lists tables in a schema |
| `describe_table` | `tools/db_tools.py` | Column names + types |
| `sample_rows` | `tools/db_tools.py` | Small row sample (max 20) |
| `run_sql` | `tools/db_tools.py` | Read-only SQL, output capped at 3000 chars |
| `submit_answer` | `tools/submit_answer.py` | Submits final query, terminates agent |

**Disabled (code present, not wired):** `search_columns` in `tools/db_tools.py` — caused
regression in Run 2 by returning hits from unrelated schemas for generic keywords.

## Key config (in `framework/llm.py`)

- `temperature`: 0.6 → **0.1**
- `compress_context`: False → **True**
- `compress_max_chars`: 150 → **400**

## What to do next

See `context/TODO.md`. The immediate next action is building the generated-guides pipeline
per `context/PLAN_generated_guides.md`:

1. Write `scripts/build_schema_guides.py` — textualize each schema, LLM-synthesize a
   comprehensive guide (schema structure + business rules as SQL), embed, save to
   `evaluation/data/generated_guides/`.
2. Write `tools/schema_guide_tools.py` — `find_schema(query)` tool using cosine similarity
   over the embedded guides.
3. Wire `find_schema` into `evaluate.py` / `interactive.py`; simplify system prompt.
4. Validate generated guides (spot-check table names match actual DB).
5. Run eval and record results.

## Key findings from funnel analysis

| Run | Schema ok | Tables ok | Logic ok (=pass) | Dominant failure |
|-----|-----------|-----------|------------------|-----------------|
| 1   | 89%       | 80%       | 39%              | Wrong logic (27) |
| 4   | **100%**  | **94%**   | 27%              | Wrong logic (43) |

Run 4 is the proof: perfect navigation → worst pass rate. Logic/rules are the bottleneck,
not schema or table identification. Generated guides address this directly by encoding
business rules as SQL conditions alongside exact table and column names.

## Eval variance note

The hard split shows ~±8 case variance between identical-code runs (n=64, temp=0.1).
A result is only clearly meaningful if hard pass rate reaches **≥30/64 (≥47%)**.

## Known issues

| Issue | Status | Notes |
|-------|--------|-------|
| Wrong logic / business-rule misses | **Active bottleneck** | 27–43/run; target of generated-guides approach |
| AGENT_ERROR re-exploration loop | Partially addressed by Run 3 strict rules; abandoned in favour of generated guides | See `issues/agent_error_reexploration.md` |
| `search_columns` regression | Closed | Reverted; code kept. See `runs/run2_search_columns.md` |
| ~19 continuation-prompt injections/run | Open | Model outputs JSON as text; contributes to NO_SUBMISSION |
