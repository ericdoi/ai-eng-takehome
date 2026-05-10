# TODO

<!-- DIRECTIVES:
- Contains only unfinished items. When an item is completed, move it to WORKLOG.md.
- Top item is highest priority. Focus on the top item first.
- If the top item is not trivial, break it down into sub-items until the top item is trivial.
-->

## Phase 2 — Next iteration (current best: 62.5% easy, 39.1% hard)

Current failure buckets (Run 1 hard split): 20 MISMATCH, 10 AGENT_ERROR, 7 NO_SUBMISSION, 2 SQL_ERROR.

- [ ] Fix AGENT_ERROR / re-exploration loop
  - See `context/issues/agent_error_reexploration.md` for full trace and root cause analysis
  - Root cause: agent calls `list_schemas` repeatedly after already finding the right schema via guide
  - Approaches to consider before implementing:
    - Prompt: tell the agent the guide title names the schema; use it directly
    - Prompt: explicitly warn against re-calling `list_schemas` after a schema is identified
    - Tool: scope `search_columns` to a single schema (avoids cross-schema confusion, could replace repeated `list_tables`/`describe_table` cycling)
    - Tool: `list_schemas` output could include table counts or a hint to use `search_guides` first
  - [ ] Pick an approach, implement, run eval, record results
- [ ] Fix NO_SUBMISSION (7 hard) — agent never calls submit_answer
  - Likely same root cause as AGENT_ERROR (exhausted iterations or fell into bad loop)
  - Should improve once AGENT_ERROR is fixed
- [ ] Fix MISMATCH (20 hard) — wrong business rules applied
  - After AGENT_ERROR fix, re-analyze which MISMATCHes are rule misses vs logic errors
  - Candidate: require `read_guide` before `submit_answer` (CoT scaffold)

## Phase 0 — Debug harness (nice to have)

- [ ] `scripts/rerun_case.py` — single-case rerunner (`--split`, `--idx`, stream via `StreamPrinter`)

## Phase 3 — Stretch (only if Phase 2 plateaus)

- [ ] Embedding-based guide retrieval via OpenRouter `/embeddings` (if ≥5 hard failures are paraphrase-shaped retrieval misses)
- [ ] Full schema dump for matched schema (per "Death of Schema Linking?" finding)
- [ ] Try higher `reasoning.effort` on default model

## Phase 4 — Writeup

- [ ] Draft prose writeup (PDF or doc)
  - [ ] Baseline numbers and run progression
  - [ ] What changed and why, with per-run score delta
  - [ ] Tradeoffs: BM25 vs embeddings, search_columns failure and lesson learned
  - [ ] What I'd do next with another day
  - [ ] Generalization notes
- [ ] Email fork link to recruiter
