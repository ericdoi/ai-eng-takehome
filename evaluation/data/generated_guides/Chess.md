# Chess Schema Reference Guide

## Schema Summary
The Chess schema contains competitive chess game records with move sequences and opening classifications, enabling analysis of player performance, opening strategies, and game outcomes from tournament play.

---

## Table Reference

### Table: `Chess.game`
**Meaning:** Individual chess game records from competitive tournaments.
**Synonyms:** games, matches, contests

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `game_id` | BIGINT | Unique game identifier | game number, ID |
| `opening_id` | BIGINT | Foreign key to opening table | opening reference |
| `event` | VARCHAR | Tournament or event name | tournament, competition |
| `site` | VARCHAR | Geographic location of event | location, venue |
| `event_date` | DATE | Date game was played | date, game date |
| `round` | VARCHAR | Round identifier within event | round number |
| `white` | VARCHAR | Name of player with White pieces | white player |
| `black` | VARCHAR | Name of player with Black pieces | black player |
| `game_result` | VARCHAR | Outcome code | result, outcome |
| `ECO` | VARCHAR | Encyclopedia of Chess Openings code | opening code |
| `whiteElo` | BIGINT | White player's rating before game | white rating, white strength |
| `BlackElo` | BIGINT | Black player's rating before game | black rating, black strength |
| `opening` | VARCHAR | Opening name (denormalized) | opening name |
| `w1`–`w10` | VARCHAR | White's moves 1–10 in algebraic notation | white moves |
| `b1`–`b10` | VARCHAR | Black's moves 1–10 in algebraic notation | black moves |

**Notable Values:**
- `game_result`: `'1-0'` (White win), `'0-1'` (Black win), `'1/2-1/2'` (draw)
- `event`: `'FIDE World Rapid 2014'`
- `site`: `'Dubai UAE'`
- `w1` examples: `'Nf3'`, `'b3'`, `'c4'`, `'d4'`, `'e4'`
- `b1` examples: `'Nf6'`, `'c5'`, `'c6'`, `'d5'`, `'d6'`, `'e5'`, `'e6'`, `'f5'`, `'g6'`

---

### Table: `Chess.opening`
**Meaning:** Chess opening definitions with standard move sequences and variations.
**Synonyms:** opening definitions, opening library, opening catalog

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `opening_id` | BIGINT | Unique opening identifier | opening number, ID |
| `name` | VARCHAR | Full opening name | opening name, title |
| `code` | VARCHAR | ECO code (may be `'-'` for unclassified) | ECO code |
| `w1`–`w4` | VARCHAR | White's canonical moves 1–4 | white moves |
| `b1`–`b4` | VARCHAR | Black's canonical moves 1–4 | black moves |
| `variation` | VARCHAR | Specific variation or subtype name | variation name, subtype |

**Notable Values:**
- `code`: `'-'` (unclassified)
- `w1` examples: `'Nc3'`, `'Nf3'`, `'a3'`, `'b3'`, `'b4'`, `'c3'`, `'c4'`, `'d3'`, `'d4'`, `'e3'`, `'e4'`, `'f4'`, `'g3'`, `'g4'`, `'h3'`
- `b1` examples: `'Nc6'`, `'Nf6'`, `'a6'`, `'b5'`, `'b6'`, `'c5'`, `'c6'`, `'d5'`, `'d6'`, `'e5'`, `'e6'`, `'f5'`, `'g6'`

---

## Join Paths

**Game to Opening:**
```sql
Chess.game g
INNER JOIN Chess.opening o ON g.opening_id = o.opening_id
```

---

## Business Rules as SQL

### Opening Exclusions (CRITICAL)

**Rule: Exclude all French Defense games**
```sql
WHERE g.opening NOT LIKE '%French Defense%'
  AND o.name NOT LIKE '%French Defense%'
```

**Rule: Exclude all Sicilian Defense games**
```sql
WHERE g.opening NOT LIKE '%Sicilian Defense%'
  AND o.name NOT LIKE '%Sicilian Defense%'
```

**Combined exclusion (apply to all metrics):**
```sql
WHERE g.opening NOT LIKE '%French Defense%'
  AND g.opening NOT LIKE '%Sicilian Defense%'
  AND o.name NOT LIKE '%French Defense%'
  AND o.name NOT LIKE '%Sicilian Defense%'
```

### Game Classification

**Rule: Miniature (fewer than 10 moves)**
```sql
WHERE COALESCE(w10, '') = '' OR COALESCE(b10, '') = ''
```

**Rule: Short draw (draw before move 20)**
```sql
WHERE g.game_result = '1/2-1/2'
  AND (COALESCE(w10, '') = '' OR COALESCE(b10, '') = '')
```

### Player Ratings

**Rule: Exclude games where either player lacks a rating**
```sql
WHERE g.whiteElo IS NOT NULL
  AND g.BlackElo IS NOT NULL
  AND g.whiteElo > 0
  AND g.BlackElo > 0
```

**Rule: Rating mismatch (difference > 400 points)**
```sql
WHERE ABS(g.whiteElo - g.BlackElo) > 400
```

**Rule: Apply 0.5x weight to mismatched games in performance calculations**
```sql
CASE WHEN ABS(g.whiteElo - g.BlackElo) > 400 THEN 0.5 ELSE 1.0 END
```

### Result Handling

**Rule: Convert result to points (White perspective)**
```sql
CASE 
  WHEN g.game_result = '1-0' THEN 1.0
  WHEN g.game_result = '1/2-1/2' THEN 0.5
  WHEN g.game_result = '0-1' THEN 0.0
END
```

**Rule: Convert result to points (Black perspective)**
```sql
CASE 
  WHEN g.game_result = '0-1' THEN 1.0
  WHEN g.game_result = '1/2-1/2' THEN 0.5
  WHEN g.game_result = '1-0' THEN 0.0
END
```

### Opening Analysis

**Rule: Use opening table for opening names, not denormalized column**
```sql
FROM Chess.game g
INNER JOIN Chess.opening o ON g.opening_id = o.opening_id
WHERE o.name = 'desired_opening_name'
```

**Rule: Exclude irregular openings (ECO A00) if data quality check needed**
```sql
WHERE o.code != 'A00' OR o.code IS NOT NULL
```

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| White win | `WHERE game_result = '1-0'` |
| Black win | `WHERE game_result = '0-1'` |
| Draw | `WHERE game_result = '1/2-1/2'` |
| White player strength | `whiteElo` |
| Black player strength | `BlackElo` |
| Opening name | `opening.name` (use table join, not `game.opening`) |
| Opening code | `opening.code` or `game.ECO` |
| Move sequence | `w1`, `b1`, `w2`, `b2`, ... `w10`, `b10` |
| Tournament | `event` |
| Location | `site` |
| Game date | `event_date` |
| Round | `round` |
| Miniature game | Game with `w10 IS NULL` or `b10 IS NULL` |
| Short draw | `game_result = '1/2-1/2'` AND move count < 20 |
| Rating mismatch | `ABS(whiteElo - BlackElo) > 400` |
| White performance | Points from White's perspective using result conversion |
| Black performance | Points from Black's perspective using result conversion |
| Opening success rate | `SUM(points) / COUNT(*) * weight_factor` |
| French Defense exclusion | `opening NOT LIKE '%French Defense%' AND opening.name NOT LIKE '%French Defense%'` |
| Sicilian Defense exclusion | `opening NOT LIKE '%Sicilian Defense%' AND opening.name NOT LIKE '%Sicilian Defense%'` |