# Chess Schema Reference Guide

## Schema Summary
This schema contains competitive chess game records with move sequences and opening classifications, enabling analysis of player performance, opening strategies, and game outcomes.

---

## Join Paths

**Games with opening details:**
```sql
FROM Chess.game g
JOIN Chess.opening o ON g.opening_id = o.opening_id
```

---

## Business Rules as SQL

| Rule | SQL Condition |
|------|---------------|
| Exclude French Defense games | `WHERE g.opening NOT LIKE '%French%' AND o.name NOT LIKE '%French%'` |
| Exclude Sicilian Defense games | `WHERE g.opening NOT LIKE '%Sicilian%' AND o.name NOT LIKE '%Sicilian%'` |
| Miniature games (< 10 moves) | `WHERE COALESCE(g.b10, g.b9, g.b8, g.b7, g.b6, g.b5, g.b4, g.b3, g.b2, g.b1) IS NULL` |
| Short draws (draw before move 20) | `WHERE g.game_result = '1/2-1/2' AND COALESCE(g.b20, g.b19, g.b18, g.b17, g.b16, g.b15, g.b14, g.b13, g.b12, g.b11) IS NULL` |
| Rating mismatch (> 400 point difference) | `WHERE ABS(g.whiteElo - g.BlackElo) > 400` |
| Players with established ratings | `WHERE g.whiteElo IS NOT NULL AND g.BlackElo IS NOT NULL` |
| Irregular openings | `WHERE g.ECO = 'A00'` |

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| White player | `Chess.game.white` |
| Black player | `Chess.game.black` |
| Game outcome | `Chess.game.game_result` |
| White rating | `Chess.game.whiteElo` |
| Black rating | `Chess.game.BlackElo` |
| Opening classification | `Chess.opening.name` (via `opening_id` join) |
| ECO code | `Chess.game.ECO` |
| Tournament | `Chess.game.event` |
| Location | `Chess.game.site` |
| Game date | `Chess.game.event_date` |
| Move sequence | `Chess.game.w1, b1, w2, b2, ... w10, b10` (columns represent moves 1–10) |
| White's first move | `Chess.game.w1` |
| Black's first move | `Chess.game.b1` |

---

## Table Reference

### `Chess.game`
**Meaning:** Individual chess game records with move sequences and player information.

| Column | Notes |
|--------|-------|
| `game_id` | Unique game identifier |
| `opening_id` | Foreign key to `Chess.opening`; use for opening name/variation lookup |
| `event` | Tournament name; sample value: `FIDE World Rapid 2014` |
| `site` | Tournament location; sample value: `Dubai UAE` |
| `event_date` | DATE format; enables temporal cohort analysis |
| `round` | Round identifier within tournament (e.g., `2.1`, `2.2`) |
| `white` | White player name |
| `black` | Black player name |
| `game_result` | Enum: `1-0` (white win), `0-1` (black win), `1/2-1/2` (draw) |
| `ECO` | Encyclopedia of Chess Openings code (e.g., `A41`, `C08`, `B48`) |
| `whiteElo` | White player rating; NULL if unrated |
| `BlackElo` | Black player rating; NULL if unrated |
| `opening` | Denormalized opening name (do NOT use for filtering; join `Chess.opening` instead) |
| `w1`–`w10`, `b1`–`b10` | Move sequences for moves 1–10; white moves in `w*` columns, black in `b*` columns; NULL indicates game ended before that move |

---

### `Chess.opening`
**Meaning:** Opening classification reference table with standard variations.

| Column | Notes |
|--------|-------|
| `opening_id` | Primary key; join to `Chess.game.opening_id` |
| `name` | Opening name (e.g., `Scandinavian Defense`, `Rat Defense`) |
| `code` | Enum: `-` (not specified) or opening code |
| `w1`–`w4`, `b1`–`b4` | Canonical move sequences for opening definition; `-` indicates variation does not specify this move |
| `variation` | Named variation within opening family (e.g., `Anderssen Counterattack`, `Bronstein Variation`) |