# Current State (handoff reference)

## Where we are

Best scores: **62.5% easy (40/64), 39.1% hard (25/64)** — Run 1, committed as `482a275`.

Phase 2 (generated guides) is implemented and ready to eval. All 76 schema guides have been
synthesized and embedded. The agent now uses a single `find_schema` tool instead of the
old multi-step navigation chain. **No eval run has been done yet with this new toolset.**

## Code state

Working tree has **uncommitted Phase 2 changes** on top of `482a275`:

| File | Change |
|------|--------|
| `scripts/build_schema_guides.py` | New — offline guide synthesis + embedding pipeline |
| `tools/schema_guide_tools.py` | New — `find_schema` tool (cosine similarity over embeddings) |
| `evaluation/evaluate.py` | `create_tools()` now uses `find_schema`, `list_tables`, `describe_table`, `run_sql`, `submit_answer` |
| `interactive.py` | Same tool change |
| `framework/agent.py` | Simplified system prompt: `find_schema → run_sql → submit` |

Generated artifacts (git-ignored or not yet committed):
- `evaluation/data/generated_guides/*.md` — 76 schema guides
- `evaluation/data/generated_guides/embeddings.npz` — 76×1536 float32, L2-normalized

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
| `find_schema` | `tools/schema_guide_tools.py` | Embeds query, cosine-similarity over 76 generated guides; returns top-1 (or top-2 if gap < 0.05) |
| `list_tables` | `tools/db_tools.py` | Fallback: lists tables in a schema |
| `describe_table` | `tools/db_tools.py` | Fallback: column names + types |
| `run_sql` | `tools/db_tools.py` | Read-only SQL, output capped at 3000 chars |
| `submit_answer` | `tools/submit_answer.py` | Submits final query, terminates agent |

**Disabled (code present, not wired):** `search_guides`, `read_guide` (`tools/guide_tools.py`),
`list_schemas`, `sample_rows`, `search_columns` (`tools/db_tools.py`).

## Key config (in `framework/llm.py`)

- `temperature`: 0.6 → **0.1**
- `compress_context`: False → **True**
- `compress_max_chars`: 150 → **400**

## What to do next

See `context/TODO.md`. Immediate next actions:

1. **Interactive spot-check** — run `interactive.py` on 2–3 known hard-split failure cases
   to confirm `find_schema` retrieves the right guide and the agent writes correct SQL.
2. **Run hard eval** — `source .env && uv run evaluate --api-key "$OPENROUTER_API_KEY" --split hard --concurrency 16`
3. Record results in `context/RESULTS.md`; target ≥ 30/64 (≥47%) to clear variance threshold.

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
