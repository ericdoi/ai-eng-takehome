# TODO

<!-- DIRECTIVES:
- Contains only unfinished items. When an item is completed, move it to WORKLOG.md.
- Top item is highest priority. Focus on the top item first.
- If the top item is not trivial, break it down into sub-items until the top item is trivial.
-->

## Phase 2 — Generated guides pipeline (current best: 62.5% easy, 39.1% hard)

Navigation funnel analysis showed wrong logic (27–43 cases/run) dominates wrong schema/tables
combined in every run. Prompt engineering is abandoned. Full plan: `context/PLAN_generated_guides.md`.

- [ ] **Build `scripts/build_schema_guides.py`**
  - [ ] Textualize each of the 76 schemas: list tables, describe columns, sample rows, capture
        distinct values for low-cardinality VARCHAR columns
  - [ ] Build `schema_to_guide` mapping (H1 extraction + `GUIDE_OVERRIDES` dict for mismatches
        like `movie_ratings.md` → `imdb_MovieLens`, `f1_racing_metrics.md` → `ErgastF1`)
  - [ ] LLM synthesis loop: for each schema, call LLM with textualized schema + guide (if any)
        to produce a comprehensive guide with exact names, synonyms, join paths, rules as SQL
  - [ ] Save to `evaluation/data/generated_guides/<schema>.md`
  - [ ] Embed all generated guides via OpenRouter `/v1/embeddings` (`text-embedding-3-small`)
  - [ ] Save embeddings to `evaluation/data/generated_guides/embeddings.npz`

- [ ] **Write `tools/schema_guide_tools.py`**
  - [ ] Load embeddings at startup, expose `find_schema(query)` tool
  - [ ] Return full guide content for top cosine-similarity match
  - [ ] Return top-2 if score gap is small (< 0.05)

- [ ] **Wire and validate**
  - [ ] Add `find_schema` to `evaluate.py` and `interactive.py` `create_tools()`
  - [ ] Simplify system prompt: `find_schema` → `run_sql` → `submit_answer` happy path;
        keep `list_tables` / `describe_table` as fallbacks
  - [ ] Spot-check 5–10 generated guides: verify all `schema.Table` references exist in DB
  - [ ] Test interactively on 2–3 known failure cases before full eval

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
