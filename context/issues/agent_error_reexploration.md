# Issue: AGENT_ERROR — schema re-exploration loop

**Observed in:** Run 1 (22 AGENT_ERROR cases: 12 easy, 10 hard)
**Most concentrated failure cluster:** `world` schema — 5/12 easy AGENT_ERRORs

## What happens

The agent exhausts all 30 iterations without submitting an answer. It keeps calling
`list_schemas`, `list_tables`, and `describe_table` in loops on the wrong schema,
never reaching `submit_answer`.

## Concrete trace (Run 1, easy split)

**Prompt:** "List countries by continent with their dominant languages where language
percentage exceeds 90%, showing whether each language is official."

**Gold query schema:** `world.Country`, `world.CountryLanguage`

**Tool call sequence (30 iterations):**
```
list_schemas()
list_tables(schema="Countries")         ← wrong schema immediately
describe_table(schema="Countries", table="Data")
search_guides(query="language percentage official continent country")
list_schemas()                          ← re-listing after already having results
describe_table(Countries.Data) × 8     ← stuck, describing same table repeatedly
sample_rows(Countries.Data)
list_schemas() × 4                      ← re-listing again
run_sql("SELECT * FROM Countries.Data LIMIT 0")
describe_table(Countries.Data)
sample_rows(Countries.Data)
list_tables(schema="Countries")
list_schemas()                          ← final iteration, still lost
```

**search_guides returned (score 16.60):**
> `# World Geography Data Standards (world / Countries Databases)`
> `## Language Analysis — Countries may have multiple official languages...`

## Root cause

The guide snippet contains the text "(world / Countries Databases)". There is a real
`Countries` schema in the database (World Bank indicators data — unrelated to what we need).
The agent picks up "Countries" from the snippet and tries that schema *before calling
`read_guide`* to see the full content. Once stuck in `Countries`, it loops trying
`describe_table` and `sample_rows` on `Countries.Data` (a World Bank table with 56 columns
like "Indicator Name", "Indicator Code") and never tries the `world` schema.

**Key observation:** The agent called `search_guides` with a high-scoring hit pointing to the
right guide — but it never called `read_guide`. The snippet was enough for it to latch onto the
wrong schema name ("Countries") and spiral.

## Approaches to consider

**Prompt changes:**
- Require `read_guide` before any schema exploration: "After search_guides returns a hit,
  always call read_guide on the top result before exploring any schema. The full guide will
  name the exact schema and table."
- Warn against re-calling `list_schemas` after a schema has been identified.

**Tool changes:**
- Scoped `search_columns(keyword, schema)` — once the agent has a schema from the guide,
  let it find the right table in one call rather than `list_tables` + `describe_table` cycling.
- Modify `search_guides` snippet format to make the schema name more prominent (e.g. prefix
  each result with `Schema: world` extracted from the H1).

**Guide content (not preferred):**
- The guide itself could be more explicit, but we shouldn't edit guide files per the rules.

## Related failures

Similar loop pattern likely explains AGENT_ERROR cases in `ErgastF1`, `Credit`, `financial`
schemas — agent finds partial information from the guide snippet, picks a wrong or ambiguous
schema name from it, and cycles until max iterations.
