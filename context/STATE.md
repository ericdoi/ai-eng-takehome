# Current State (handoff reference)

## Where we are

Best scores so far: **62.5% easy (40/64), 39.1% hard (25/64)** — Run 1, committed as `482a275`.

Run 2 added `search_columns` and regressed badly (48.4% / 28.1%); that change has been reverted.
The repo is back to the Run 1 toolset. See `context/RESULTS.md` for the full run table.

## How to run the eval

```bash
uv run evaluate --api-key <KEY> --split both --concurrency 16
```

Traces are saved to `logs/run_<timestamp>/`. After a run, analyze with:

```bash
uv run python scripts/analyze_run.py logs/run_<timestamp>/ --split hard
uv run python scripts/analyze_run.py logs/run_<timestamp>/ --csv context/runN_hard.csv
```

API budget: ~$20 total, ~$0.65/full run. Check remaining balance:
```bash
curl -s https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer <KEY>" | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(f'remaining: \${d[\"limit_remaining\"]:.2f}')"
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

**Disabled (code present, not wired):** `search_columns` in `tools/db_tools.py` — queries
`information_schema.columns` by keyword. Caused regression when used with generic keywords;
see `context/issues/agent_error_reexploration.md` and `context/runs/run2_search_columns.md`.

## Key config changes from original (in `framework/llm.py`)

- `temperature`: 0.6 → **0.1**
- `compress_context`: False → **True**
- `compress_max_chars`: 150 → **400**

## Top known issue

AGENT_ERROR re-exploration loop (22 cases in Run 1). Full analysis in
`context/issues/agent_error_reexploration.md`. Short version: agent finds the right guide via
`search_guides` but latches onto a wrong schema name from the snippet (doesn't call `read_guide`
first), then loops for all 30 iterations on the wrong schema.

## Next action

See `context/TODO.md` — top item is fixing the AGENT_ERROR loop, with candidate approaches listed.
