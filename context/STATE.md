# Current State (handoff reference)

## Where we are

Best scores: **79.7% easy (51/64), 59.4% hard (38/64)** — Run 8, 2026-05-10.

Phase 2 (generated guides + `find_schema` tool) is committed as `da80184`.
Run 8 (2026-05-10): **38/64 hard (59.4%)** — up from 32/64 (50.0%) in Run 7, +6 cases.

Navigation funnel: schema 97%, tables 88%, logic 68% (38/56 right-table cases).
7 navigation failures remain; 19 wrong-logic cases are the bottleneck.

Fixes implemented in Run 8 (on top of Run 7 fixes):
- Fix 6: Agent prompt — extra columns are never penalized; include source cols alongside derived
- Fix 7: Agent prompt — EXCLUDE rules are conditional, not universally applied
- Fix 8: Synthesis prompt — emit combined CASE WHEN SQL for multi-value classifications

Schemas regenerated: financial (Sonnet), Credit, lahman_2014, ErgastF1, Airline, CraftBeer, Hockey.
Run 8 log: `logs/run_20260510_084621/`.

## Code state (uncommitted changes on top of `da80184` / `ac0526a`)

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

## Run 7 failure analysis (32 remaining failures)

| Pattern | Count | Schemas |
|---------|-------|---------|
| Wrong logic / business rules | 26 | lahman_2014(6), financial(4), Credit(3), world(3), ErgastF1(4), Airline(3), CraftBeer(2), Hockey(1), Chess(1) |
| Wrong schema | 4 | Credit×2, world×1, financial×1 |
| Wrong tables | 1 | employee (missed employees table) |
| AGENT_ERROR | 1 | financial |

**Key logic failure patterns:**
- ErgastF1 (4): uses driverRef/constructorRef instead of forename/surname/name
- lahman_2014 (6): per-row vs aggregate confusion, unclear non-reliever/starter filters
- financial (4): over-applies EXCLUDE rules; CASE WHEN label mapping missed; wrong join pattern
- Credit (3): over-applies RF refund exclusion; category casing 'essential' vs 'Essential'
- world (3): extra/missing output columns, wrong population filter
- Airline (3): thin-route / severe-delay / completed-flight definitions unclear
- CraftBeer (2): "high-gravity" / "extreme" IBU thresholds not in guide

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

API budget: **~$13.19 remaining** as of 2026-05-10 (~$1.05/full guide regen, ~$0.36/hard-only
eval run, ~$0.05-0.10/single Sonnet schema). Check balance:
```bash
curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $(grep OPENROUTER_API_KEY .env | cut -d= -f2)" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(f'remaining: \${d[\"limit_remaining\"]:.2f}')"
```

## Key config (in `framework/llm.py`)

- `temperature`: **0.1**
- `compress_context`: **True**
- `compress_max_chars`: **400**

## Run history

| Run | Hard score | Notes |
|-----|-----------|-------|
| Run 1 | 25/64 (39.1%) | Baseline |
| Run 6 | 21/64 (32.8%) | Phase 2 (find_schema + guides); navigation fixed |
| Run 7 | 32/64 (50.0%) | Fixes 1–5: IDENTIFY/EXCLUDE framing, sentinels, REQUIRED/OPTIONAL joins, Sonnet for financial, LEFT JOIN prompt |
| Run 8 | 38/64 (59.4%) | Fixes 6–8: extra-columns agent rule, conditional EXCLUDE, combined CASE WHEN in guides |

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
