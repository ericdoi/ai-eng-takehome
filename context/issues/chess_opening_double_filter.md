# Issue: Chess guide generates redundant opening filter via JOIN

## Symptom

Spot-check on "Calculate win rates for White players (with at least 5 games)" returned 4 rows.
Without any filters the dataset has 13 eligible players; with the French/Sicilian exclusion
applied via the denormalized `game.opening` column only, it has 5. The agent returned 4 — one
player fewer than expected.

## Root cause

The source guide (`chess_idiosyncrasies.md`) says:

> **Never, ever, ever count any games that play the French Defense.** These games are excluded
> from ALL metrics without exception.
> (same for Sicilian Defense)

This absolute wording caused the LLM synthesis step to generate two parallel filter conditions
in the generated guide (`evaluation/data/generated_guides/Chess.md`):

```sql
WHERE g.opening NOT LIKE '%French Defense%'        -- denormalized column on game table
  AND o.name   NOT LIKE '%French Defense%'          -- normalized name on opening table (via JOIN)
  AND g.opening NOT LIKE '%Sicilian Defense%'
  AND o.name   NOT LIKE '%Sicilian Defense%'
```

The `Chess.game` table has both a denormalized `opening` VARCHAR column *and* a foreign key
`opening_id → Chess.opening.opening_id`. Filtering on `o.name` via the JOIN introduces an
INNER JOIN dependency: any `game` row whose `opening_id` has no matching row in `opening` (or
whose `opening.name` matches a filtered string even though `game.opening` does not) is silently
dropped. This appears to eliminate one additional player compared to filtering on
`game.opening` alone.

## Status

**Open / known limitation.** The guide is technically faithful to the source rule — it just
produces a stricter filter than the denormalized column alone. Whether this matches the gold
query depends on how the gold was written:

- If gold filters on `game.opening` only → agent over-filters → MISMATCH.
- If gold also joins and filters on `opening.name` → result should match.

## Mitigation options

1. **Regenerate the Chess guide** with an explicit instruction to prefer the denormalized
   `game.opening` column over a JOIN for opening name lookups, since both exist. Low priority
   unless Chess questions are confirmed to fail in the eval.

2. **Add a note to the system prompt** telling the agent not to introduce JOINs that aren't
   required by the question. Risky — could cause regressions elsewhere by discouraging needed JOINs.

3. **Accept and move on.** The dataset has only 295 games and 13 players with ≥5 games; small
   absolute effect. Monitor in eval results.

## Broader pattern

This is an instance of a general risk with LLM guide synthesis: absolute-sounding rules
("without exception") get turned into SQL conditions that are applied unconditionally, even
when the question doesn't call for them. The synthesis prompt instructs the model to "restate
each rule as the exact SQL condition," which correctly captures the intent but doesn't
distinguish "always apply" from "apply when the question is about X."
