# Chess Schema Reference Guide

## Schema Summary
This schema contains competitive chess games from tournaments (FIDE World Rapid 2014) with move-by-move records and opening classifications, linked to a normalized opening repertoire table.

---

## Join Paths

**[REQUIRED]** — Link games to opening definitions:
```sql
FROM Chess.game g
JOIN Chess.opening o ON g.opening_id = o.opening_id
```
Use this join whenever filtering or reporting on opening names, variations, or opening-level statistics. The `Chess.game.opening` column is denormalized; always prefer the normalized `Chess.opening.name` for consistency.

---

## Business Rules as SQL

**EXCLUDE French Defense:** 
```sql
WHERE NOT (Chess.opening.name LIKE '%French%' OR Chess.game.opening LIKE '%French%')
```
Applies to all metrics without exception.

**EXCLUDE Sicilian Defense:**
```sql
WHERE NOT (Chess.opening.name LIKE '%Sicilian%' OR Chess.game.opening LIKE '%Sicilian%')
```
Applies to all metrics without exception.

**IDENTIFY miniatures:**
```sql
WHERE GREATEST(
  COALESCE(NULLIF(Chess.game.w10, ''), '0')::INT,
  COALESCE(NULLIF(Chess.game.b10, ''), '0')::INT
) < 10
```
Games with fewer than 10 moves; analyze separately from full games.

**IDENTIFY short draws:**
```sql
WHERE Chess.game.game_result = '1/2-1/2' 
  AND GREATEST(
    COALESCE(NULLIF(Chess.game.w10, ''), '0')::INT,
    COALESCE(NULLIF(Chess.game.b10, ''), '0')::INT
  ) < 20
```
Draw games ending before move 20; flag for competitive integrity review.

**IDENTIFY rating mismatches:**
```sql
WHERE ABS(Chess.game.whiteElo - Chess.game.BlackElo) > 400
```
Games with >400 Elo difference; weight at 0.5x in opening success rate calculations.

**EXCLUDE unrated players:**
```sql
WHERE Chess.game.whiteElo IS NOT NULL AND Chess.game.BlackElo IS NOT NULL
```
Exclude games where either player lacks an established rating from rating-based analysis.

**Performance calculation (points):**
- White win: `CASE WHEN Chess.game.game_result = '1-0' THEN 1 ELSE 0 END`
- Draw: `CASE WHEN Chess.game.game_result = '1/2-1/2' THEN 0.5 ELSE 0 END`
- Loss: `CASE WHEN Chess.game.game_result = '0-1' THEN 0 ELSE 0 END`

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| white player | `Chess.game.white` |
| black player | `Chess.game.black` |
| white rating / white Elo | `Chess.game.whiteElo` |
| black rating / black Elo | `Chess.game.BlackElo` |
| result / outcome | `Chess.game.game_result` (values: `'1-0'`, `'0-1'`, `'1/2-1/2'`) |
| opening name | `Chess.opening.name` (via join; not `Chess.game.opening`) |
| ECO code | `Chess.game.ECO` or `Chess.opening.code` |
| tournament | `Chess.game.event` |
| location | `Chess.game.site` |
| game date | `Chess.game.event_date` |
| round | `Chess.game.round` |
| move sequence | `Chess.game.w1`, `Chess.game.b1`, `Chess.game.w2`, `Chess.game.b2`, … `Chess.game.w10`, `Chess.game.b10` |
| opening variation | `Chess.opening.variation` |

---

## Table Reference

### `Chess.game`
Competitive chess games with move records and results.

| Column | Semantics |
|--------|-----------|
| `game_id` | Unique game identifier |
| `opening_id` | Foreign key to `Chess.opening`; use for normalized opening lookups |
| `event` | Tournament name; sample: `'FIDE World Rapid 2014'` |
| `site` | Tournament location; sample: `'Dubai UAE'` |
| `event_date` | Game date (DATE type) |
| `round` | Round identifier within tournament |
| `white` | White player name |
| `black` | Black player name |
| `game_result` | Outcome; enum: `'1-0'` (white win), `'0-1'` (black win), `'1/2-1/2'` (draw) |
| `ECO` | Encyclopedia of Chess Openings code |
| `whiteElo` | White player rating (BIGINT); NULL if unrated |
| `BlackElo` | Black player rating (BIGINT); NULL if unrated |
| `opening` | Denormalized opening name (do not use for filtering; join to `Chess.opening` instead) |
| `w1`–`w10` | White moves 1–10; sample values: `'Nf3'`, `'e4'`, `'d4'` |
| `b1`–`b10` | Black moves 1–10; sample values: `'Nf6'`, `'c5'`, `'e6'` |

### `Chess.opening`
Normalized opening repertoire with canonical names and move sequences.

| Column | Semantics |
|--------|-----------|
| `opening_id` | Unique opening identifier |
| `name` | Opening name; use for all opening-based filtering and reporting |
| `code` | ECO code or `'-'` if unclassified |
| `w1`–`w4` | Canonical white moves 1–4 for opening definition |
| `b1`–`b4` | Canonical black moves 1–4 for opening definition |
| `variation` | Named variation within opening family |