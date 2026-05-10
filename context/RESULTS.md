# Experiment Results

| Run | Description | Easy Pass | Hard Pass | Easy % | Hard % | Cost ($) | Log Dir |
|-----|-------------|-----------|-----------|--------|--------|----------|---------|
| 0 | Baseline (submit_answer only, temp=0.6) | 0/64 | 0/64 | 0.0% | 0.0% | $0.04 | `logs/run_20260510_053738/` |
| 1 | Phase 1: db+guide tools, BM25, new prompt, temp=0.1, compress | 40/64 | 25/64 | 62.5% | 39.1% | $0.65 | `logs/run_20260510_054527/` |
| 2 | Add search_columns tool (REGRESSION — reverted) | 31/64 | 18/64 | 48.4% | 28.1% | $0.39 | `logs/run_20260510_055406/` |
| 3 | Anti-loop: schema hint in search_guides + STRICT RULES prompt (hard only) | — | 21/64 | — | 32.8% | ~$0.33 | `logs/run_20260510_061531/` |
| 4 | Anti-loop v2: soft ANTI-LOOP RULES + `world` schema fix (hard only, REGRESSION) | — | 17/64 | — | 26.6% | ~$0.57 | `logs/run_20260510_061954/` |
| 1′ | Run 1 code reproduced (revert check, both splits) | 42/64 | 17/64 | 65.6% | 26.6% | ~$0.60 | `logs/run_20260510_063816/` |
| 5 | Phase 2: generated guides + find_schema tool (first run, guides truncated + bare SQL) | — | 21/64 | — | 32.8% | ~$1.70 | `logs/run_20260510_072957/` |
| 6 | Phase 2 v2: fixed guides (schema-qualified SQL, join paths first, schema name banner) | — | 21/64 | — | 32.8% | ~$1.00 | `logs/run_20260510_075148/` |

## Hard split failure breakdown

| Type          | Run 0 | Run 1 | Run 2 | Run 3 | Run 4 | Run 1′ | Run 5 | Run 6 |
|---------------|-------|-------|-------|-------|-------|--------|-------|-------|
| PASS          |   0   |  25   |  18   |  21   |  17   |  17    |  21   |  21   |
| MISMATCH      |  24   |  20   |  26   |  26   |  15   |  24    |  32   |  40   |
| AGENT_ERROR   |   0   |  10   |   5   |   7   |  32   |   6    |  11   |   2   |
| NO_SUBMISSION |   0   |   7   |  10   |   3   |   0   |  10    |   —   |   0   |
| SQL_ERROR     |  40   |   2   |   5   |   7   |   0   |   7    |   —   |   1   |
| Other         |   0   |   0   |   0   |   0   |   0   |   0    |  11   |   0   |

## Navigation funnel (hard split, from trace analysis)

| Run | Right schema | Right tables | Right logic (=pass) | Wrong schema | Wrong tables | Wrong logic |
|-----|-------------|-------------|---------------------|-------------|-------------|-------------|
| 0   |  0/64  (0%) |  0/64  (0%) |  0/64  (0%)         | 64          |  0          |  0          |
| 1   | 57/64 (89%) | 51/64 (80%) | 25/64 (39%)         |  7          |  5          | 27          |
| 2   | 56/64 (88%) | 43/64 (67%) | 18/64 (28%)         |  8          | 12          | 26          |
| 3   | 60/64 (94%) | 52/64 (81%) | 21/64 (33%)         |  4          |  6          | 33          |
| 4   | 64/64 (100%)| 60/64 (94%) | 17/64 (27%)         |  0          |  4          | 43          |
| 1′  | 57/64 (89%) | 51/64 (80%) | 17/64 (27%)         |  7          |  6          | 34          |
| 5   | 56/64 (88%) | 50/64 (78%) | 21/64 (33%)         |  8          |  6          | 29          |
| 6   | 60/64 (94%) | 54/64 (84%) | 21/64 (33%)         |  4          |  6          | 33          |

**Key insight:** Run 4 achieved perfect schema identification (100%) and near-perfect table
identification (94%) — yet logic (pass rate) hit its lowest point (27%). Wrong logic dominates
in every run: 27–43 failures vs at most 8 schema misses and 12 table misses combined.
Navigation is not the bottleneck. Business-rule application is.

## Notes

- Runs 3–5 are hard-split only to conserve API budget (~$1.70/hard-only run, ~$3.30/both).
- Run 2 lesson: `search_columns` hurt table identification (43 vs 51) by leading agents to
  wrong tables via generic keyword matches.
- Run 3 lesson: strict anti-loop rules improved schema identification (89%→94%) but pushed
  more cases into "wrong logic" (27→33) — agents submitted faster but less correctly.
- Run 4 lesson: soft advisory language let loops return fully (32 AGENT_ERRORs); yet even
  with perfect navigation, only 27% logic correct — confirming navigation isn't the bottleneck.
- **Eval variance (Run 1′):** Reproducing Run 1 on identical code yielded 17/64 hard (26.6%)
  vs the original 25/64 (39.1%) — an 8-case swing. Schema/table funnel numbers are identical
  (57/64, 51/64), so variance is entirely in the logic step (LLM inference for SQL generation).
  **Signal threshold:** a hard-split result is only clearly meaningful if it reaches ≥30/64
  (≥47%) — roughly 2 standard deviations above the observed variance band.
- Run 5 lesson: Phase 2 first run — same pass rate as Run 3 (21/64) but AGENT_ERROR improved
  (10→11, within variance) and MISMATCH rose (20→32). Root causes: (1) all generated guides
  were truncated at 4096 tokens, cutting off join paths and business rules; (2) guide SQL used
  bare table names, potentially misleading the agent; (3) schema name not salient in find_schema
  response, causing ErgastF1/lahman_2014 re-exploration loops. All three fixed for Run 6.
- Run 6 lesson: fixes worked for navigation — AGENT_ERROR fell 11→2, schema 88%→94%, tables
  78%→84%. But pass rate unchanged (21/64). MISMATCH rose to 40 because more cases now reach
  the logic stage but still fail. Logic is the sole remaining bottleneck. Top failing schemas:
  financial (7), Credit (6), Airline (6), lahman_2014 (5), Chess (4), employee (4), ErgastF1 (4).
  Token usage fell 40% (1.7M→1.0M) due to more focused guides. Budget: ~$12.68 remaining.
