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

- [ ] **Improve logic / business-rule application** — full plan in `context/PLAN_business_logic.md`

  - [ ] **Fix 1 — Synthesis prompt: clearer business rule expression**
    - Rules must use consistent IDENTIFY vs EXCLUDE framing with unambiguous labels
    - Rate/ratio rules must include explicit denominator SQL, not just prose
    - Update `_SYNTHESIS_USER` in `scripts/build_schema_guides.py`

  - [ ] **Fix 2 — Schema textualization: surface date sentinel values**
    - Extend `textualize_schema()` to detect sentinel-pattern DATE values
      (years ≥ 9000, epoch zeros, or one value covering > 80% of rows)
    - Emit as `col  DATE  — sentinel: '9999-01-01' means currently active`
    - Helps employee schema and any other schema using sentinel dates

  - [ ] **Fix 3 — Synthesis prompt: label joins as REQUIRED vs OPTIONAL**
    - Guide LLM to annotate each join as `[REQUIRED]` or `[OPTIONAL — display only]`
    - Optional joins should note: "for grouping/filtering use the raw code column directly"
    - Prevents agent from joining lookup tables when gold uses raw codes (Airline pattern)

  - [ ] **Fix 4 — Add `--model` flag; use Sonnet for top failing schemas only**
    - Add `--model` flag to `scripts/build_schema_guides.py` (default: haiku)
    - Regen financial (+ Credit, Airline) with `anthropic/claude-sonnet-4-6`
    - Pricing: Haiku $5/1M out, Sonnet $15/1M out, Opus $25/1M out (too expensive for all 76)
    - Keep Haiku for remaining 4 of the top-7 schemas; never use Opus for bulk regen

  - [ ] **Fix 5 — Agent prompt: LEFT JOIN for lookup/optional tables**
    - Add one sentence to system prompt in `framework/agent.py`:
      "When joining a lookup or optional table, use LEFT JOIN — not INNER JOIN —
      so unmatched rows are not silently dropped."

  - [ ] **Regenerate top-7 failing schemas + re-embed** after Fixes 1–4
    - financial, Credit, Airline, lahman_2014, Chess, employee, ErgastF1
    - Use `--schema` flag per schema (or add multi-schema support)
    - Re-embed after all 7 are regenerated

  - [ ] **Run eval (Run 7)** — if improvement confirmed, regen all 76 guides (~$1.05) then Run 8
    - Target ≥ 30/64 (≥47%)

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
