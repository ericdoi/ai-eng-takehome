# Run 4 — AGENT_ERROR prompt fix (v2, soft rules — severe regression)

**Log:** `logs/run_20260510_061954/`
**Split:** hard only
**Cost:** ~$0.57 (3.48M tokens — 75% more than run 3)

## Changes from Run 3

- **`tools/guide_tools.py`:** Fixed schema extraction for multi-schema guides: take only the
  first name before ` / ` (e.g. `world / Countries` → `world`).
- **`framework/agent.py`:** Replaced run 3's "STRICT RULES" block with softer "ANTI-LOOP RULES"
  advisory language (changed NEVER → "at most once", added "stop and submit your best attempt").
  Added explicit instruction in step 3: "ALWAYS call list_tables to get exact table names."

## Hypothesis

Run 3's strict prohibitions stopped loops but caused agents to skip `list_tables`, leading to
SQL_ERRORs from hallucinated table names. Softening the rules while explicitly requiring
`list_tables` would preserve the loop reduction and fix the table-name hallucination.

## Results — SEVERE REGRESSION

| Split | Pass  | Fail | Pass Rate |
|-------|-------|------|-----------|
| Hard  | 17/64 | 47   | 26.6%     |

Failure breakdown vs previous runs (hard split):

| Type          | Run 1 | Run 3 | Run 4 | Delta (vs R3) |
|---------------|-------|-------|-------|---------------|
| PASS          |  25   |  21   |  17   |  -4           |
| MISMATCH      |  20   |  26   |  15   |  -11          |
| AGENT_ERROR   |  10   |   7   |  32   |  **+25** ✗   |
| NO_SUBMISSION |   7   |   3   |   0   |  -3           |
| SQL_ERROR     |   2   |   7   |   0   |  -7           |

Token usage tripled (1.99M → 3.48M input tokens) — agents were looping through all 30 iterations
on nearly every case.

## What went wrong

Changing NEVER → "at most once" and STRICT → ANTI-LOOP was enough to let the model resume its
re-exploration loop. The MISMATCH cases from run 3 (where agents submitted wrong SQL) converted
back to AGENT_ERRORs (agents looping until max iterations instead of submitting).

The `world / Countries` → `world` fix and the `list_tables` emphasis did not compensate for
the loss of strict anti-loop enforcement.

**Key lesson:** Advisory language ("consider", "at most once", "if possible") is insufficient
to override the model's default tendency to re-explore schemas. NEVER/STRICT language is required.

## Decision

Revert to STRICT language while retaining the improvement from run 3 that matters: require
`list_tables` explicitly as a mandatory verification step even after reading the guide.
The run 5 prompt keeps "NEVER call list_schemas more than once" and adds "ALWAYS call list_tables
to get exact case-sensitive table names — do NOT guess from the guide."
