# Run 2 — search_columns tool

**Log:** `logs/run_20260510_05????/` (in progress)
**Cost:** TBD

## Changes from Run 1

- **New tool:** `search_columns(keyword)` — queries `information_schema.columns` for a case-insensitive
  substring match on column names, returning `(schema, table, column, type)`. Lets the agent resolve
  "which schema has a `language` column?" in one call instead of iterating across 76 schemas.
- **System prompt:** workflow updated to recommend `search_columns` as step 3 (before `list_tables`).

## Hypothesis

The 22 AGENT_ERROR cases in Run 1 are mostly schema-navigation failures. Giving the agent a direct
column-keyword → schema/table lookup should eliminate most of them, especially the `world` cluster
(5 easy + several hard).

## Results — REGRESSION (reverted)

**Log:** `logs/run_20260510_055406/`
**Cost:** $0.39

| Split | Pass  | Fail | Pass Rate |
|-------|-------|------|-----------|
| Easy  | 31/64 | 33   | 48.4%     |
| Hard  | 18/64 | 46   | 28.1%     |

Failure breakdown (combined):

| Type          | Count |
|---------------|-------|
| MISMATCH      | 51 (was 32) |
| SQL_ERROR     | 13 (was 4)  |
| NO_SUBMISSION | 10          |
| AGENT_ERROR   |  5          |

## What went wrong

`search_columns` backfires for generic keywords. When the agent searches for "population",
"country", "language", or "name", the tool returns hits from dozens of schemas and the agent
picks the wrong one — e.g. `Mondial.Country_Full` instead of `world.Country`, or invents a
table name like `Accidents.accidents` (doesn't exist; real table is `Accidents.nesreca`).

The world AGENT_ERRORs from Run 1 (the cases we were trying to fix) turned into SQL_ERRORs
and MISMATCHes — the agent is now "confidently wrong" instead of "confused".

`search_columns` *works* for specific technical identifiers (e.g. `search_columns("UniqueCarrier")`
→ exactly one result). It fails badly for generic domain terms.

## Decision

Reverted `search_columns` from the active toolset. Code kept in `tools/db_tools.py`.

If revisited: restrict its use to specific identifiers via clearer tool description, or scope it
to a known schema (add an optional `schema` parameter and recommend using guide-provided schema
names first).

## Next steps

The AGENT_ERROR root cause (agent re-calling `list_schemas` 6 times and wandering into wrong schema)
needs a different fix. Better approach: strengthen the system prompt to trust the guide's schema name
directly, rather than re-exploring after it's already been identified.
