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