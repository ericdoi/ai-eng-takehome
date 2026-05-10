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

- [x] **Fix guide SQL qualification** — regenerated with schema-qualified names in all SQL snippets
  - All join paths now use `Schema.table` form; LLM previously wrote bare table names
  - Sections reordered: join paths + business rules first so truncation only clips column docs
  - max_tokens raised 4096 → 8192; 55/76 guides still truncated but all have join paths + rules
  - `find_schema` response now opens with prominent banner showing exact SQL schema name + usage examples
  - System prompt updated: "use schema name verbatim — do NOT try alternative spellings"

- [x] **Run eval, record results** — Run 6: 21/64 (32.8%). Navigation fixed (AGENT_ERROR 11→2). Logic still bottleneck (33/54 correct-table cases wrong).

- [ ] **Improve logic / business-rule application** — top failing schemas: financial (7), Credit (6), Airline (6), lahman_2014 (5), Chess (4), employee (4), ErgastF1 (4)
  - Spot-check guide quality for top 3 failing schemas; compare gold SQL to agent output
  - Consider whether guide business-rule section is precise enough (e.g. financial loan status codes)
  - [ ] Run eval again once guide or prompt improvements are made; target ≥ 30/64 (≥47%)

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
