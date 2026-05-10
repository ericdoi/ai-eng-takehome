# NBA Schema Reference Guide

## Schema Summary
This schema contains NBA game statistics, player information, team rosters, and historical draft data spanning player actions across games.

---

## Join Paths

**Player stats for a specific game:**
```sql
FROM NBA.Actions a
JOIN NBA.Player p ON a.PlayerId = p.PlayerId
JOIN NBA.Team t ON a.TeamId = t.TeamId
WHERE a.GameId = ?
```

**Game results with team names:**
```sql
FROM NBA.Game g
JOIN NBA.Team t1 ON g.Team1Id = t1.TeamId
JOIN NBA.Team t2 ON g.Team2Id = t2.TeamId
```

**Player career stats (draft cohort):**
```sql
FROM NBA.joined_drafted_all_players_original j
WHERE j.draft_year = ?
```

---

## Business Rules as SQL

- **Game outcome for Team1**: `WHERE g.ResultOfTeam1 = 1` (win), `= -1` (loss), `= 0` (tie)
- **Starter vs. bench**: `WHERE a.Starter = 1` (starter), `= 0` (bench)
- **Career-level stats**: Use `NBA.joined_drafted_all_players_original` columns prefixed `career_` for aggregate career metrics

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| player performance | `NBA.Actions` |
| game outcome | `NBA.Game.ResultOfTeam1` |
| draft class | `NBA.joined_drafted_all_players_original.draft_year` |
| shooting efficiency | `NBA.Actions.FieldGoalsMade / NBA.Actions.FieldGoalAttempts` |
| three-point percentage | `NBA.Actions.3PointsMade / NBA.Actions.3PointAttempts` |
| free throw percentage | `NBA.Actions.FreeThrowsMade / NBA.Actions.FreeThrowAttempts` |
| plus-minus | `NBA.Actions.PlusMinus` |
| career win shares | `NBA.joined_drafted_all_players_original.career_ws` |
| draft position | `NBA.joined_drafted_all_players_original.pk` |

---

## Table Reference

### `NBA.Actions`
Player-level box score statistics for individual games.

| Column | Semantics |
|--------|-----------|
| `GameId` | Foreign key to `NBA.Game` |
| `TeamId` | Foreign key to `NBA.Team` |
| `PlayerId` | Foreign key to `NBA.Player` |
| `Minutes` | Total minutes played (in seconds or raw units) |
| `FieldGoalsMade`, `FieldGoalAttempts` | 2-point and 3-point field goals combined |
| `3PointsMade`, `3PointAttempts` | Three-point shots only |
| `FreeThrowsMade`, `FreeThrowAttempts` | Free throw statistics |
| `PlusMinus` | Net point differential while player on court |
| `OffensiveRebounds`, `DefensiveRebounds`, `TotalRebounds` | Rebound categories |
| `Starter` | `1` = starter, `0` = bench |

### `NBA.Game`
Game-level metadata and results.

| Column | Semantics |
|--------|-----------|
| `GameId` | Primary key |
| `Team1Id`, `Team2Id` | Foreign keys to `NBA.Team` |
| `ResultOfTeam1` | `1` = Team1 won, `-1` = Team1 lost, `0` = tie |
| `Date` | Game date |
| `URL` | Official NBA.com game page |

### `NBA.Player`
Player roster with identifiers.

| Column | Semantics |
|--------|-----------|
| `PlayerId` | Primary key |
| `PlayerName` | Player full name |

### `NBA.Team`
Team roster with identifiers.

| Column | Semantics |
|--------|-----------|
| `TeamId` | Primary key |
| `TeamName` | Official team name |

### `NBA.joined_drafted_all_players_original`
Historical draft cohort statistics and career aggregates.

| Column | Semantics |
|--------|-----------|
| `ID` | Unique player-season identifier |
| `draft_year` | Year player was drafted |
| `pk` | Draft pick number (position in draft) |
| `season` | Season identifier (e.g., `1984-85`) |
| `age` | Player age during season |
| `height`, `weight` | Physical attributes (inches, pounds) |
| `position` | Enum: `Center`, `Power Forward`, `Center and Power Forward` |
| `shoots` | Enum: `Left`, `Right` |
| `born` | Birth date (ISO format) |
| `college` | College/university name |
| `draft_g` | Games played in draft season |
| `draft_fg`, `draft_trb`, `draft_ast`, `draft_pts` | Draft season totals |
| `fg_per`, `3p_per`, `ft_per` | Draft season shooting percentages |
| `pts_per`, `trb_per`, `ast_per` | Draft season per-game averages |
| `career_g` | Career games played |
| `career_ws` | Career win shares |
| `career_ws48` | Career win shares per 48 minutes |
| `career_per` | Career player efficiency rating |