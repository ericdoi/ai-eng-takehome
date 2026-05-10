# TODO

<!-- DIRECTIVES:
- Contains only unfinished items. When an item is completed, move it to WORKLOG.md.
- Top item is highest priority. Focus on the top item first.
- If the top item is not trivial, break it down into sub-items until the top item is trivial.
-->


## Phase 0 — Debug harness (deferred, do after Phase 1 results)

- [ ] Write `scripts/analyze_run.py` — trace inspector
  - [ ] Accept a run dir as argument
  - [ ] Bucket failures by `failure_type`
  - [ ] Per failed case: print prompt, gold query, submitted query, first DuckDB error
  - [ ] Group failures by schema (regex schema name from gold query)
  - [ ] Dump CSV: `(case_idx, prompt, schema_used, failure_type, error)`
- [ ] Write `scripts/rerun_case.py` — single-case rerunner
  - [ ] Accept `--split` and `--idx`; stream events via `StreamPrinter`

## Phase 2 — Iterate on long tail

- [x] `scripts/analyze_run.py` — trace inspector (failure buckets, per-schema breakdown, CSV dump)
- [x] Add `search_columns(keyword)` tool — finds schema/table by column keyword via `information_schema`; fixes `world`-schema AGENT_ERROR cluster (agent was burning 30 iterations exploring wrong schemas)
- [ ] Record Run 2 results (in progress)
- [ ] Diagnose remaining failures and apply next fix
  - Remaining buckets after Run 1: 20 MISMATCH hard, 10 AGENT_ERROR hard, 7 NO_SUBMISSION hard
  - Candidate fixes (pick based on Run 2 data):
    - AGENT_ERROR / NO_SUBMISSION → check if CoT scaffold or `run_sql`-before-submit helps
    - MISMATCH from wrong rules → strengthen guide reading (require read_guide before submit)
    - MISMATCH from logic errors → review specific failing cases

## Phase 3 — Stretch (only if Phases 1–2 plateau)

- [ ] Embedding-based guide retrieval via OpenRouter `/embeddings` (fallback if ≥5 hard failures are paraphrase-shaped retrieval misses)
- [ ] Full schema dump for the matched schema (per "Death of Schema Linking?" finding)
- [ ] Try higher `reasoning.effort` on default model before swapping models

## Phase 4 — Writeup

- [ ] Draft prose writeup (PDF or doc)
  - [ ] Baseline numbers
  - [ ] What changed and why, with per-phase score delta
  - [ ] Tradeoffs: BM25 vs embeddings, prompt scaffolding vs more tools, model cost
  - [ ] What I'd do next with another day
  - [ ] Generalization notes
- [ ] Email fork link to recruiter
