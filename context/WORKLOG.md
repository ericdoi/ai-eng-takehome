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
* **Run 5 candidate (not yet run):** Restored STRICT RULES language + kept `world` schema fix + added explicit "ALWAYS call list_tables — table names are case-sensitive and WILL differ from guide descriptions" to address the SQL_ERROR issue from run 3.
* **Reverted to Run 1 state** (`git checkout 482a275 -- framework/agent.py tools/guide_tools.py`). Reproduction run (`logs/run_20260510_063816/`) confirmed code is correct: navigation funnel identical to Run 1 (57/64 schema, 51/64 tables), with variance only in the logic step (17 vs 25 passes). Run 5 prompt changes discarded in favour of a new approach.
* **New approach decided:** LLM-synthesized schema guides — preprocess each schema into a comprehensive guide fusing exact table/column names with business rules as SQL conditions, embed for semantic retrieval, replace the current multi-step navigation workflow with a single `find_schema` tool call. Plan written to `context/PLAN_generated_guides.md`.
* **`scripts/analyze_run.py` upgraded:** Added three-stage navigation funnel (right schema / right tables / right logic), per-case diagnostic indicators (✓/✗ with explored schemas, missed tables, guide names, tool sequence), and funnel columns to CSV output. Key finding from re-running all logs: navigation is not the bottleneck — Run 4 achieved 100% schema and 94% table identification yet only 27% pass rate. Wrong logic (27–43 cases/run) dominates wrong schema (0–8) and wrong tables (0–12) combined in every run. `context/RESULTS.md` updated with full funnel table and this analysis.