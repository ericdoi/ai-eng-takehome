# NBA Schema Reference Guide

## Schema Summary
This schema contains NBA game statistics, player information, team rosters, and historical draft data spanning multiple seasons with detailed performance metrics.

---

## Table Reference

### NBA.Actions
**Meaning:** Individual player performance statistics for each game appearance.
**Synonyms:** Player game stats, box score, game performance

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| GameId | BIGINT | Unique game identifier | Game number |
| TeamId | BIGINT | Team playing in the game | Team number |
| PlayerId | BIGINT | Player identifier | Player number |
| Minutes | BIGINT | Total minutes played | MP, playing time |
| FieldGoalsMade | BIGINT | Successful field goal attempts | FG, made shots |
| FieldGoalAttempts | BIGINT | Total field goal attempts | FGA, shot attempts |
| 3PointsMade | BIGINT | Successful three-point attempts | 3P, made threes |
| 3PointAttempts | BIGINT | Total three-point attempts | 3PA, three attempts |
| FreeThrowsMade | BIGINT | Successful free throw attempts | FT, made free throws |
| FreeThrowAttempts | BIGINT | Total free throw attempts | FTA, free throw attempts |
| PlusMinus | BIGINT | Point differential when player on court | +/-, net rating |
| OffensiveRebounds | BIGINT | Rebounds on offensive end | ORB, offensive boards |
| DefensiveRebounds | BIGINT | Rebounds on defensive end | DRB, defensive boards |
| TotalRebounds | BIGINT | Combined offensive and defensive rebounds | REB, rebounds, TRB |
| Assists | BIGINT | Passes leading to made baskets | AST, assists |
| PersonalFouls | BIGINT | Fouls committed by player | PF, fouls |
| Steals | BIGINT | Defensive plays resulting in possession change | STL, steals |
| Turnovers | BIGINT | Possessions lost by player | TO, turnovers, TOV |
| BlockedShots | BIGINT | Shots blocked by player | BLK, blocks |
| BlocksAgainst | BIGINT | Shots blocked against player | BA, blocks against |
| Points | BIGINT | Total points scored | PTS, scoring |
| Starter | BIGINT | Binary indicator of starting status | 1 = starter, 0 = bench |

---

### NBA.Game
**Meaning:** Game-level metadata and results.
**Synonyms:** Game record, matchup, contest

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| GameId | BIGINT | Unique game identifier | Game number |
| Team1Id | BIGINT | First team in matchup | Home team ID |
| Team2Id | BIGINT | Second team in matchup | Away team ID |
| ResultOfTeam1 | BIGINT | Outcome for Team1 | 1 = win, -1 = loss, 0 = tie |
| URL | VARCHAR | Official NBA game page link | Game URL, link |
| Date | DATE | Game date | Game date, date played |

---

### NBA.Player
**Meaning:** Player master data with identifiers and names.
**Synonyms:** Player roster, player directory

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| PlayerId | BIGINT | Unique player identifier | Player number, ID |
| PlayerName | VARCHAR | Player full name | Name, player name |

---

### NBA.Team
**Meaning:** Team master data with identifiers and names.
**Synonyms:** Team roster, team directory

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| TeamId | BIGINT | Unique team identifier | Team number, ID |
| TeamName | VARCHAR | Official team name | Name, team name |

---

### NBA.joined_drafted_all_players_original
**Meaning:** Historical draft class statistics with career performance metrics and player attributes.
**Synonyms:** Draft data, draft history, player draft records

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| ID | BIGINT | Unique record identifier | Record ID |
| age | BIGINT | Player age at draft | Draft age |
| draft_g | BIGINT | Games played in draft season | Draft games, games |
| mp | BIGINT | Minutes played in draft season | Draft minutes |
| draft_fg | BIGINT | Field goals made in draft season | Draft FG, made shots |
| fga | BIGINT | Field goal attempts in draft season | Draft FGA, shot attempts |
| 3p | BIGINT | Three-pointers made in draft season | Draft 3P, made threes |
| 3pa | BIGINT | Three-point attempts in draft season | Draft 3PA, three attempts |
| draft_ft | BIGINT | Free throws made in draft season | Draft FT, made free throws |
| fta | BIGINT | Free throw attempts in draft season | Draft FTA, free throw attempts |
| orb | BIGINT | Offensive rebounds in draft season | Draft ORB, offensive boards |
| draft_trb | BIGINT | Total rebounds in draft season | Draft REB, rebounds, TRB |
| draft_ast | BIGINT | Assists in draft season | Draft AST, assists |
| draft_stl | BIGINT | Steals in draft season | Draft STL, steals |
| draft_blk | BIGINT | Blocks in draft season | Draft BLK, blocks |
| draft_tov | BIGINT | Turnovers in draft season | Draft TO, turnovers, TOV |
| draft_pf | BIGINT | Personal fouls in draft season | Draft PF, fouls |
| draft_pts | BIGINT | Points in draft season | Draft PTS, scoring |
| fg_per | DOUBLE | Field goal percentage in draft season | FG%, field goal percentage |
| 3p_per | BIGINT | Three-point percentage in draft season | 3P%, three-point percentage |
| ft_per | DOUBLE | Free throw percentage in draft season | FT%, free throw percentage |
| mp_per | DOUBLE | Minutes per game in draft season | MPG, minutes per game |
| pts_per | DOUBLE | Points per game in draft season | PPG, points per game |
| trb_per | DOUBLE | Rebounds per game in draft season | RPG, rebounds per game |
| ast_per | DOUBLE | Assists per game in draft season | APG, assists per game |
| season | VARCHAR | NBA season year | Season, draft season |
| weight | BIGINT | Player weight in pounds | Weight (lbs) |
| height | BIGINT | Player height in inches | Height (in) |
| position | VARCHAR | Player position | Pos, position played |
| shoots | VARCHAR | Shooting hand | Handedness, shooting hand |
| born | VARCHAR | Player birth date | Birth date, DOB |
| draft_year | BIGINT | Year player was drafted | Draft year |
| pk | BIGINT | Draft pick number | Pick, draft pick |
| amature_honor | BIGINT | Amateur honors indicator | Honors, college honors |
| college | VARCHAR | College attended | School, university |
| raw_data | BIGINT | Data quality flag | Data flag |
| career_g | BIGINT | Career games played | Career games, total games |
| career_per | DOUBLE | Career performance rating | Career rating |
| career_ws | DOUBLE | Career win shares | Career wins, win shares |
| career_ws48 | DOUBLE | Career win shares per 48 minutes | Career WS/48, efficiency |

**Notable values:**
- `season`: "1984-85"
- `position`: "Center", "Center and Power Forward", "Power Forward"
- `shoots`: "Left", "Right"
- `born`: "1962-08-05", "1964-06-09", "1964-11-22"

---

## Join Paths

### Actions to Game
```sql
NBA.Actions a
JOIN NBA.Game g ON a.GameId = g.GameId
```

### Actions to Player
```sql
NBA.Actions a
JOIN NBA.Player p ON a.PlayerId = p.PlayerId
```

### Actions to Team
```sql
NBA.Actions a
JOIN NBA.Team t ON a.TeamId = t.TeamId
```

### Game to Team (both teams)
```sql
NBA.Game g
JOIN NBA.Team t1 ON g.Team1Id = t1.TeamId
JOIN NBA.Team t2 ON g.Team2Id = t2.TeamId
```

### Complete Actions join path
```sql
NBA.Actions a
JOIN NBA.Game g ON a.GameId = g.GameId
JOIN NBA.Player p ON a.PlayerId = p.PlayerId
JOIN NBA.Team t ON a.TeamId = t.TeamId
```

---

## Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| Player started game | `WHERE a.Starter = 1` |
| Player came off bench | `WHERE a.Starter = 0` |
| Team1 won game | `WHERE g.ResultOfTeam1 = 1` |
| Team1 lost game | `WHERE g.ResultOfTeam1 = -1` |
| Positive plus-minus | `WHERE a.PlusMinus > 0` |
| Double-double (10+ in two stats) | `WHERE (a.Points >= 10 AND a.TotalRebounds >= 10) OR (a.Points >= 10 AND a.Assists >= 10) OR (a.TotalRebounds >= 10 AND a.Assists >= 10)` |
| Triple-double (10+ in three stats) | `WHERE a.Points >= 10 AND a.TotalRebounds >= 10 AND a.Assists >= 10` |
| High efficiency (FG% > 50%) | `WHERE a.FieldGoalAttempts > 0 AND (CAST(a.FieldGoalsMade AS DOUBLE) / a.FieldGoalAttempts) > 0.50` |
| Three-point shooter (3PA > 0) | `WHERE a.3PointAttempts > 0` |
| Drafted player record | `WHERE jdap.pk IS NOT NULL` |
| Left-handed player | `WHERE jdap.shoots = 'Left'` |
| Right-handed player | `WHERE jdap.shoots = 'Right'` |

---

## Synonym Glossary

| Common Term | Schema Reference |
|-------------|------------------|
| Points scored | `a.Points` |
| Shooting percentage | `CAST(a.FieldGoalsMade AS DOUBLE) / a.FieldGoalAttempts` |
| Three-point percentage | `CAST(a.3PointsMade AS DOUBLE) / a.3PointAttempts` |
| Free throw percentage | `CAST(a.FreeThrowsMade AS DOUBLE) / a.FreeThrowAttempts` |
| Rebounds | `a.TotalRebounds` |
| Offensive boards | `a.OffensiveRebounds` |
| Defensive boards | `a.DefensiveRebounds` |
| Assists | `a.Assists` |
| Steals | `a.Steals` |
| Blocks | `a.BlockedShots` |
| Turnovers | `a.Turnovers` |
| Fouls | `a.PersonalFouls` |
| Plus-minus | `a.PlusMinus` |
| Playing time | `a.Minutes` |
| Starter | `a.Starter = 1` |
| Bench player | `a.Starter = 0` |
| Win | `g.ResultOfTeam1 = 1` |
| Loss | `g.ResultOfTeam1 = -1` |
| Draft pick | `jdap.pk` |
| Draft year | `jdap.draft_year` |
| College | `jdap.college` |
| Career games | `jdap.career_g` |
| Career win shares | `jdap.career_ws` |
| Points per game (draft season) | `jdap.pts_per` |
| Rebounds per game (draft season) | `jdap.trb_per` |
| Assists per game (draft season) | `jdap.ast_per` |
| Player height | `jdap.height` |
| Player weight | `jdap.weight` |
| Player position | `jdap.position` |
| Birth date | `jdap.born` |