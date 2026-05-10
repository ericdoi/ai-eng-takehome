# TODO

<!-- DIRECTIVES:
- Contains only unfinished items. When an item is completed, move it to WORKLOG.md.
- Top item is highest priority. Focus on the top item first.
- If the top item is not trivial, break it down into sub-items until the top item is trivial.
-->

## Phase 2 — Generated guides pipeline (current best: 62.5% easy, 39.1% hard)

Navigation funnel analysis showed wrong logic (27–43 cases/run) dominates wrong schema/tables
combined in every run. Prompt engineering is abandoned. Full plan: `context/PLAN_generated_guides.md`.

- [x] **Build `scripts/build_schema_guides.py`**
- [x] **Write `tools/schema_guide_tools.py`**
- [x] **Wire and validate**
  - Validated: all 76 guides have no hallucinated table or column names
  - Spot-checked business-rule SQL conditions (world, Accidents, Airline, Chess) — all correct
  - Wired into `evaluate.py` / `interactive.py`; system prompt simplified to find_schema → run_sql → submit

- [ ] **Test interactively** on 2–3 known failure cases before full eval

- [ ] **Run eval, record results** — target ≥ 30/64 hard (≥47%) to clear the variance threshold

## Phase 0 — Debug harness (nice to have)

- [ ] `scripts/rerun_case.py` — single-case rerunner (`--split`, `--idx`, stream via `StreamPrinter`)

## Phase 3 — Stretch (only if Phase 2 plateaus)

- [ ] Hybrid BM25 + embedding retrieval (Reciprocal Rank Fusion) over generated guides
- [ ] Try higher `reasoning.effort` on default model
- [ ] Run both splits once a hard improvement is confirmed, to check easy-split regression

## Phase 4 — Writeup

- [ ] Draft prose writeup (PDF or doc)
  - [ ] Baseline numbers and run progression with funnel analysis
  - [ ] What changed and why, with per-run score delta
  - [ ] Key finding: navigation wasn't the bottleneck; wrong logic was
  - [ ] Tradeoffs: BM25 vs embeddings, search_columns failure, prompt-engineering dead ends
  - [ ] Generated guides: design, implementation, results
  - [ ] What I'd do next with another day
  - [ ] Generalization notes (no overfitting to visible 64 cases)
- [ ] Email fork link to recruiter
