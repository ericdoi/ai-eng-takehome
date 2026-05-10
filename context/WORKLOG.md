# WORKLOG

<!-- DIRECTIVES:
- Contains only completed items, moved here from TODO.md when done.
- Each entry should note what was done and, if useful, why or how.
-->

Start time: 2:03 pm JST

* Prepare CONTEXT.md and PLAN.md from Perplexity research (https://www.perplexity.ai/computer/tasks/please-read-the-readme-md-at-h-CTUhbgjaSoK9m0D0.52XpQ?view=thread).
* Fork repo locally.
* Unzip `hecks.duckdb.zip` → 635 MB `hecks.duckdb`.
* `uv sync` — installed 33 packages into `.venv` (Python 3.13.3).
* Baseline eval run (`logs/run_20260510_053738/`): **0/64 easy, 0/64 hard**.
  * Easy: 10 MISMATCH, 54 SQL_ERROR (unqualified table names — model has no schema introspection).
  * Hard: 24 MISMATCH, 40 SQL_ERROR (same root cause, plus no guide access).
  * Root cause: only tool is `submit_answer`; model guesses schema/table names blind and writes unqualified SQL.
* **Phase 1 implementation:**
  * `tools/db_tools.py`: `list_schemas`, `list_tables`, `describe_table`, `sample_rows`, `run_sql` (read-only, output capped at 3000 chars).
  * `tools/guide_tools.py`: BM25 index over `##`-chunked guide files, `search_guides`, `read_guide`. Guides dir configurable via `GUIDES_DIR` env var.
  * `framework/agent.py`: New system prompt with explicit workflow, schema-qualified name requirement, case-sensitivity warning, and grader rules.
  * `framework/llm.py`: temperature 0.6 → 0.1; compress_context enabled; compress_max_chars 150 → 400.
  * Both `evaluate.py` and `interactive.py` wired with all 7 new tools.
* **Phase 1 results** (`logs/run_20260510_054527/`): **40/64 easy (62.5%), 25/64 hard (39.1%)**. Cost: $0.65 (~4.6M tokens). ~19 "[DEBUG] Empty/failed tool call" injection events observed — model occasionally outputs JSON directly instead of calling a tool.
* `scripts/analyze_run.py`: trace inspector with failure-type buckets, per-schema breakdown, CSV dump. Fixed schema extraction to use FROM/JOIN clauses only (avoid alias.column false positives).
* **Run 2** (`logs/run_20260510_055406/`): Added `search_columns` tool — **REGRESSION** (48.4% easy, 28.1% hard). Generic keywords (population, country, name) returned hits from many schemas; agent picked wrong schema (Mondial instead of world). Reverted; `search_columns` code kept in `db_tools.py` but not wired. Lesson: column-keyword search only safe for specific technical identifiers, not domain terms.
* Committed Run 1 + Run 2 analysis as `482a275`. Repo is at Run 1 toolset (best state). Context docs written: `STATE.md` (orientation + how to run), `RESULTS.md` (run table), `issues/agent_error_reexploration.md` (trace + root cause), `runs/run0_baseline.md`, `runs/run1_phase1.md`, `runs/run2_search_columns.md`.
* **Open observation:** ~19 `[DEBUG] continuation prompt` events per run — model sometimes outputs tool-call JSON as plain text instead of invoking the tool. Not yet a dedicated TODO item; likely contributes to NO_SUBMISSION failures. Worth investigating if NO_SUBMISSION doesn't improve after the AGENT_ERROR fix.
* **Run 3** (`logs/run_20260510_061531/`, hard only, ~$0.33): First attempt at AGENT_ERROR fix.
  * `search_guides` output now shows `Schema: <name>` line extracted from guide H1 parenthetical.
  * System prompt: RECOMMENDED WORKFLOW → REQUIRED WORKFLOW; `list_schemas` removed from happy path; STRICT RULES block added (NEVER call list_schemas before search_guides / more than once; MUST call read_guide if score ≥ 5).
  * Result: **21/64 hard (32.8%)** — regression. AGENT_ERROR improved (10→7), NO_SUBMISSION improved (7→3), but SQL_ERROR spiked (2→7) and MISMATCH rose (20→26). Root cause: strict rules caused agents to skip `list_tables` and hallucinate table names (e.g., `f1.results`, `Racing.lap_times`, `world.countries`). Also, `Schema: world / Countries` hint was ambiguous.
* **Run 4** (`logs/run_20260510_061954/`, hard only, ~$0.57): Attempted to fix run 3 regression.
  * Fixed schema extraction: `world / Countries` → `world` (take first token before ` / `).
  * Softened prompt: STRICT RULES → ANTI-LOOP RULES advisory block (NEVER → "at most once"); added explicit "ALWAYS call list_tables" in workflow step 3.
  * Result: **17/64 hard (26.6%)** — severe regression. AGENT_ERROR exploded (7→32); tokens tripled (1.99M→3.48M). Advisory language was insufficient to stop re-exploration loops.
  * Key lesson: Model requires NEVER/STRICT language to override re-exploration tendency. "At most once" is interpreted permissively.
* **Discarded prompt-engineering attempt (never run):** Restored STRICT RULES language + kept `world` schema fix + added explicit "ALWAYS call list_tables — table names are case-sensitive and WILL differ from guide descriptions" to address the SQL_ERROR issue from run 3. Abandoned in favour of the generated-guides approach; no log exists for this.
* **Reverted to Run 1 state** (`git checkout 482a275 -- framework/agent.py tools/guide_tools.py`). Reproduction run (`logs/run_20260510_063816/`) confirmed code is correct: navigation funnel identical to Run 1 (57/64 schema, 51/64 tables), with variance only in the logic step (17 vs 25 passes). Run 5 prompt changes discarded in favour of a new approach.
* **New approach decided:** LLM-synthesized schema guides — preprocess each schema into a comprehensive guide fusing exact table/column names with business rules as SQL conditions, embed for semantic retrieval, replace the current multi-step navigation workflow with a single `find_schema` tool call. Plan written to `context/PLAN_generated_guides.md`.
* **Phase 2 implementation:**
  * `scripts/build_schema_guides.py`: offline preprocessing pipeline. Texturizes all 76 schemas (tables, columns, sample rows, distinct values for low-cardinality VARCHARs). Maps 20 schemas to existing business-rule guides via H1 parenthetical extraction + `GUIDE_OVERRIDES` dict (multi-schema guides like `world_geography.md` → `['world', 'Countries']` handled). Calls `anthropic/claude-haiku-4-5` via OpenRouter to synthesize one guide per schema; parallelized with `ThreadPoolExecutor` (8 workers, ~4 min total vs ~23 min sequential). Embeds all guides with `openai/text-embedding-3-small` in batches and saves `evaluation/data/generated_guides/embeddings.npz` (76×1536 float32, L2-normalized).
  * `tools/schema_guide_tools.py`: `find_schema(query)` tool. Loads embeddings at startup (cached). Embeds query at runtime via OpenRouter, runs cosine similarity (dot product since already normalized), returns full guide for top match; returns top-2 if score gap < 0.05.
  * `evaluate.py` / `interactive.py`: replaced `search_guides`, `read_guide`, `list_schemas`, `sample_rows` with `find_schema`. Active tools: `find_schema`, `list_tables`, `describe_table`, `run_sql`, `submit_answer`.
  * `framework/agent.py`: simplified system prompt — `find_schema → run_sql → submit_answer` happy path; `list_tables`/`describe_table` as explicit fallbacks. Anti-loop rules removed (no longer needed — single `find_schema` call replaces the full navigation chain).
  * **Build run:** 76 guides generated, all validated — zero hallucinated table or column names across all guides. Spot-check of SQL conditions (world, Accidents, Airline, Chess) confirmed all correct against live DB. One validator false positive: `trains` schema has a table named `trains` — `trains.trains` is a valid schema.table reference, not a hallucinated column.
* **Phase 2 eval runs (hard only):**
  * **Run 5** (`logs/run_20260510_072957/`): First Phase 2 eval — **21/64 hard (32.8%)**. Schema retrieval 88%, table ok 78%, logic 33%. Two dominant failure patterns identified via spot-check: (1) AGENT_ERROR re-exploration loops on ErgastF1 and lahman_2014 — agent ignores schema name from find_schema and tries variants like `list_tables("f1")`. (2) 32 MISMATCH cases with correct tables but wrong SQL logic.
  * Root causes: (a) find_schema response didn't make schema name salient as the exact SQL identifier; (b) all 76 generated guides were truncated mid-content — max_tokens=4096 cut off join paths, business rules, and glossary sections; (c) join path SQL used bare table names, potentially misleading agent.
* **Run 6** (`logs/run_20260510_075148/`, hard only, ~$1.00): Phase 2 v2 with fixed guides.
  * Result: **21/64 hard (32.8%)** — same pass count as Run 5.
  * Navigation fixes worked: AGENT_ERROR 11→2, schema 88%→94%, tables 78%→84%. ErgastF1/lahman_2014 loops resolved.
  * MISMATCH rose 32→40 — more cases now reach logic stage, still fail. Logic is sole bottleneck.
  * Token usage fell 40% (1.7M→1.0M): more focused guide structure (join paths first, concise columns).
  * Top failing schemas: financial (7), Credit (6), Airline (6), lahman_2014 (5), Chess (4), employee (4), ErgastF1 (4).
* **Phase 2 guide fixes:**
  * Raised synthesis max_tokens 4096 → 8192.
  * Reordered guide sections: join paths + business rules + glossary moved before exhaustive table reference, so truncation only clips column docs (critical content now survives).
  * Updated synthesis prompt to require fully-qualified `Schema.table` in all SQL snippets.
  * Added prominent banner to each `find_schema` response: `SQL SCHEMA NAME (use this exactly): ErgastF1` + usage examples.
  * Updated system prompt: "use schema name verbatim — do NOT try alternative spellings."
  * Two full guide regenerations done (~$1.05 each). 55/76 guides still hit the 8192 token cap but all now include join paths + business rules. Cost note added to script docstring and STATE.md.
* **Business logic failure analysis (post Run 6):**
  * Full trace analysis of all 43 Run 6 failures via `scripts/analyze_run.py` output.
  * Checked source guides (`evaluation/data/guides/`) vs synthesized guides for top failing schemas to distinguish synthesizer errors from genuine source ambiguity.
  * Key findings:
    * **financial**: synthesizer bug — "Non-performing loans" rule emits `NOT IN ('C','D')` (the exclusion filter) but labels it as the definition; glossary at bottom correctly says `IN ('C','D')`. Agent gets contradictory signals. Also: rate denominator (`NOT IN ('B')`) never given as explicit SQL.
    * **Airline**: guide lists lookup-table join paths (L_UNIQUE_CARRIERS, L_AIRPORT_ID, L_WEEKDAYS) without marking them optional; agent uses them for aggregation queries where gold uses raw codes directly.
    * **employee**: `to_date = '9999-01-01'` sentinel for current salary not in source guide and not surfaced by textualization (only VARCHARs get distinct-value sampling, not DATEs).
    * **Chess/general**: INNER JOIN to optional tables (opening) silently drops unmatched rows.
  * Documented in `context/issues/business_logic_failures.md`.
  * Five-fix plan written to `context/PLAN_business_logic.md`; TODOs added to `TODO.md`.
  * Strategy: test fixes iteratively — regen top-7 failing schemas first, not all 76.
* **`scripts/analyze_run.py` upgraded:** Added three-stage navigation funnel (right schema / right tables / right logic), per-case diagnostic indicators (✓/✗ with explored schemas, missed tables, guide names, tool sequence), and funnel columns to CSV output. Key finding from re-running all logs: navigation is not the bottleneck — Run 4 achieved 100% schema and 94% table identification yet only 27% pass rate. Wrong logic (27–43 cases/run) dominates wrong schema (0–8) and wrong tables (0–12) combined in every run. `context/RESULTS.md` updated with full funnel table and this analysis.
* **Fixes 1–5 implemented** (all general mechanisms, no schema-specific patches):
  * Fix 1 (`_SYNTHESIS_USER`): Replaced ambiguous prose business-rule format with explicit `IDENTIFY [label]: WHERE ...` / `EXCLUDE [label]: WHERE NOT ...` framing. Rate/ratio rules required to include both numerator and denominator as SQL.
  * Fix 2 (`textualize_schema()`): DATE/TIMESTAMP columns now checked for sentinel values — far-future dates (year ≥ 9000), epoch zeros (year 1900/1970), or a single dominant value (> 80% of rows). Surfaced as `col DATE — sentinel: '9999-01-01' means currently active`. Fixes employee `to_date` and any similar schema.
  * Fix 3 (`_SYNTHESIS_USER`): Join paths section now requires each path to be labelled `[REQUIRED]` or `[OPTIONAL — display only]`, with a note that optional joins should not be used for grouping/filtering (use raw code column directly).
  * Fix 4 (`build_schema_guides.py`): Added `--model` CLI flag (default: `anthropic/claude-haiku-4-5`). `synthesize_guide()` accepts `model=` parameter. financial schema regenerated with `anthropic/claude-sonnet-4-6` for its complex 4-way status classification and rate formulas.
  * Fix 5 (`framework/agent.py` system prompt): Added sentence: "When joining a lookup or optional table, use LEFT JOIN — not INNER JOIN — so unmatched rows are not silently dropped."
* **Run 7** (`logs/run_20260510_082903/`, hard only): Regenerated top-7 failing schemas (financial with Sonnet, Credit/Airline/lahman_2014/Chess/employee/ErgastF1 with Haiku), re-embedded, ran eval. **32/64 hard (50.0%)**, up from 21/64 (+11 cases). Navigation: schema 94%, tables 91% (up from 84%), logic 50%. AGENT_ERROR still 1. Saved `context/run7_hard.csv`.
* **Run 7 failure analysis:** Read all 32 gold vs submitted queries from `run7_hard.csv`. Key patterns identified:
  * **Name concatenation** (5 cases): agent returns `firstName || ' ' || lastName` when gold expects separate columns. Values differ regardless of aliases since grader compares values not names.
  * **EXCLUDE over-application** (5 cases): agent applies EXCLUDE business rules to generic aggregation queries where gold doesn't filter — e.g., micro-deposit exclusion applied to a plain `AVG(amount)` question.
  * **CASE WHEN classification missing** (3 cases): guide emits separate `IDENTIFY` rules (status A, B, C/D) but no combined `CASE WHEN` SQL; agent returns raw status codes instead of human-readable labels.
  * **ErgastF1 wrong-value column** (3 cases): agent selects `constructorRef` (slug value "mercedes") vs gold's `name` ("Mercedes") — same alias, different values, grader fails on values.
  * Also: integer vs float division (lahman `IPouts/3` vs `/3.0`), Credit category casing, Airline lookup-join over-joining.
* **Fixes 6–8 implemented:**
  * Fix 6 (`framework/agent.py` system prompt): "Extra columns are never penalized. When in doubt, include the original source columns alongside derived ones." Addresses name-concatenation pattern — agent now keeps `forename`/`surname` in addition to any computed full-name string.
  * Fix 7 (`framework/agent.py` system prompt): "Apply EXCLUDE rules ONLY when the question explicitly targets that metric. Generic aggregation questions do NOT automatically trigger all EXCLUDE filters."
  * Fix 8 (`_SYNTHESIS_USER`): "When multiple IDENTIFY rules map a single column's values to different labels, emit a combined CASE WHEN SQL showing all mappings — preserve exact label strings including capitalization." financial guide now includes `CASE WHEN status = 'A' THEN 'Performing' WHEN status = 'B' THEN 'Watch List' ...`.
* **Run 8** (`logs/run_20260510_084621/`, hard only): Regenerated financial (Sonnet) + Credit/lahman_2014/ErgastF1/Airline/CraftBeer/Hockey (Haiku) with updated synthesis prompt, re-embedded, ran eval. **38/64 hard (59.4%)**, up from 32/64 (+6 cases). Navigation: schema 97%, tables 88%, logic 59%. 19 wrong-logic, 5 wrong-tables, 2 wrong-schema remaining. Saved `context/run8_hard.csv`.
* **Easy split Run 8** (`logs/run_20260510_085143/`): **51/64 easy (79.7%)**, up from 40/64 baseline (+11 cases, +17 pp). No easy-specific tuning done — gains are purely from general fixes. Navigation: schema 98%, tables 95%, logic 80%. 13 failures: ErgastF1 (3), Credit (3), world (2), Chess (2), CraftBeer (1), Airline (1), lahman_2014 (1).
* **WRAPUP.md written:** Covers problem framing (easy vs hard split distinction), scores, approach (both phases, all 8 fixes), run-progression funnel table with explanation, what worked, what didn't work (search_columns regression, prompt-engineering dead end, superseded search_guides approach), remaining failure diagnosis by pattern, conclusions, what I'd do next, design decisions/tradeoffs including strengthened generalization argument.

End time: 6:06 pm JST