# Run 3 — AGENT_ERROR prompt fix (v1, regression)

**Log:** `logs/run_20260510_061531/`
**Split:** hard only
**Cost:** ~$0.33 (1.99M tokens)

## Changes from Run 1

- **`tools/guide_tools.py`:** `search_guides` output now includes a `Schema: <name>` line per
  result, extracted from the guide H1 parenthetical (e.g. `(ErgastF1 Database)` → `Schema: ErgastF1`).
  Multi-schema guides (e.g. `(world / Countries Databases)`) returned the full `world / Countries`
  string — ambiguous (see "What went wrong").
- **`framework/agent.py`:** System prompt strengthened:
  - "RECOMMENDED WORKFLOW" → "REQUIRED WORKFLOW"
  - Removed `list_schemas` from the main happy path
  - Added "STRICT RULES" block: never call `list_schemas` before `search_guides`, never call it
    more than once, must call `read_guide` before any schema exploration if score ≥ 5.

## Hypothesis

The AGENT_ERROR loop (agent calls `list_schemas` repeatedly after finding the right guide but not
reading it) would be broken by requiring `read_guide` first and prohibiting repeated `list_schemas`.

## Results — REGRESSION

| Split | Pass  | Fail | Pass Rate |
|-------|-------|------|-----------|
| Hard  | 21/64 | 43   | 32.8%     |

Failure breakdown vs Run 1 hard:

| Type          | Run 1 | Run 3 | Delta |
|---------------|-------|-------|-------|
| PASS          |  25   |  21   |  -4   |
| MISMATCH      |  20   |  26   |  +6   |
| AGENT_ERROR   |  10   |   7   |  -3 ✓ |
| NO_SUBMISSION |   7   |   3   |  -4 ✓ |
| SQL_ERROR     |   2   |   7   |  +5 ✗ |

## What went wrong

**SQL_ERROR +5:** The strict anti-`list_schemas` rules caused agents to skip `list_tables` and
`describe_table`, then hallucinate schema and table names. Examples:
- ErgastF1 queries submitted with `f1.results`, `Racing.lap_times` (wrong schema)
- `world` queries used `world.countries` (wrong case — actual table is `world.Country`)
- `imdb_MovieLens` query used `movie_ratings.ratings` (wrong schema)

**MISMATCH +6:** Likely related — agents skipping schema verification and getting business-rule
details wrong due to incomplete guide reading.

**`world / Countries` ambiguity:** The `Schema: world / Countries` hint caused the agent to
treat "Countries" as a possible table name, worsening the original problem.

**AGENT_ERROR/NO_SUBMISSION improved:** The anti-loop rules did reduce the re-exploration loop.
The improvement was real but outweighed by the SQL_ERROR regression.

## Decision

Do not revert, but refine: (1) fix schema extraction to drop everything after ` / `, and (2) replace
the hard prohibitions with an "ANTI-LOOP RULES" advisory block that still allows `list_tables` and
`describe_table` as mandatory verification steps.
