# Run 1 — Phase 1 (tools + BM25 + prompt)

**Log:** `logs/run_20260510_054527/`
**Cost:** $0.65 (~4.6M tokens)

## Changes from Run 0

- **New tools:** `list_schemas`, `list_tables`, `describe_table`, `sample_rows`, `run_sql` (db introspection); `search_guides`, `read_guide` (BM25 over `##`-chunked guide files)
- **System prompt:** explicit workflow (search_guides → read_guide → search schema → run_sql preview → submit), schema-qualified names required, case-sensitivity warning, loose grader rules
- **Temperature:** 0.6 → 0.1
- **Context compression:** enabled (keep_recent=3, max_chars=400)

## Results

| Split | Pass  | Fail | Pass Rate |
|-------|-------|------|-----------|
| Easy  | 40/64 | 24   | 62.5%     |
| Hard  | 25/64 | 39   | 39.1%     |

## Failure breakdown

| Type          | Easy | Hard |
|---------------|------|------|
| MISMATCH      | 12   | 20   |
| AGENT_ERROR   | 12   | 10   |
| NO_SUBMISSION | 0    | 7    |
| SQL_ERROR     | 0    | 2    |

## Failures by schema (hard split top offenders)

Chess, ErgastF1, world, lahman_2014 — 5 failures each; Credit, Airline, financial — 4 each.

## What went wrong

**AGENT_ERROR (12 easy, 10 hard) — max iterations reached.**
The `world` schema accounted for 5/12 easy AGENT_ERRORs. Trace inspection showed the agent calling
`list_schemas` 6 times, then wandering into a `Countries` schema (World Bank data, wrong schema)
and burning all 30 iterations there. Root cause: with 76 schemas, navigating by listing schemas
is slow and error-prone; the agent needs a shortcut from concept → schema/table.

**NO_SUBMISSION (7 hard)** — agent completed without calling `submit_answer`.
Related to ~19 "[DEBUG] continuation prompt" events visible in the log: the model occasionally
outputs tool-call JSON as plain text instead of invoking the tool, triggering the agent's
fallback prompt. When this happens near the iteration limit the agent runs out of budget.

**MISMATCH (20 hard)** — agent finds the right table but applies wrong business rules.
Hard prompts omit the rules, and while `search_guides` + `read_guide` are available, traces
suggest some cases where the guide was found but the specific rule (e.g. exclusion filter,
exact threshold) wasn't applied correctly in the SQL.

## Key insight

The biggest quick win is a `search_columns` tool: instead of calling `list_schemas` → `list_tables`
→ `describe_table` across multiple schemas, one call like `search_columns("language")` returns
`world.CountryLanguage` immediately. This should collapse the AGENT_ERROR cluster.
