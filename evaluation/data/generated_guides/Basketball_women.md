# Basketball_women Schema Reference Guide

## Schema Summary
Women's professional basketball league data (ABL and WNBA) covering player statistics, team performance, coaching records, draft history, awards, and playoff series results from 1997 onward.

---

## Join Paths

**Player to team statistics:**
```sql
FROM Basketball_women.players p
JOIN Basketball_women.players_teams pt ON p.bioID = pt.playerID
```

**Player to awards:**
```sql
FROM Basketball_women.players p
JOIN Basketball_women.awards_players ap ON p.bioID = ap.playerID
```

**Team season to playoff results:**
```sql
FROM Basketball_women.teams t
JOIN Basketball_women.teams_post tp ON t.year = tp.year AND t.tmID = tp.tmID AND t.lgID = tp.lgID
```

**Playoff series (winner to loser):**
```sql
FROM Basketball_women.series_post sp
WHERE sp.tmIDWinner = 'TEAM_ID' AND sp.lgIDWinner = 'WNBA'
```

**Coach to team:**
```sql
FROM Basketball_women.coaches c
JOIN Basketball_women.teams t ON c.year = t.year AND c.tmID = t.tmID AND c.lgID = t.lgID
```

**Draft to player:**
```sql
FROM Basketball_women.draft d
LEFT JOIN Basketball_women.players p ON d.playerID = p.bioID
```

---

## Table Reference

### `Basketball_women.awards_players`
Player awards and honors. Synonyms: *honors, accolades, achievements*

| Column | Notes |
|--------|-------|
| `playerID` | Foreign key to `players.bioID` |
| `award` | Enum: `Most Valuable Player`, `Rookie of the Year`, `Defensive Player of the Year`, `All-Star Game Most Valuable Player`, `WNBA Finals Most Valuable Player`, `WNBA All-Decade Team`, `Sixth Woman of the Year`, `Most Improved Player`, `Coach of the Year`, `ABL Playoffs Most Valuable Player`, `Newcomer of the Year`, `New Pro Award`, `Kim Perrot Sportsmanship Award`, `Peak Performer: Points/Assists/Rebounds`, `WNBA All Decade Team Honorable Mention` |
| `year` | Award year |
| `lgID` | Enum: `ABL`, `WNBA` |
| `note` | Enum: `tie` (null if not tied) |
| `pos` | Position: `G`, `F`, `C`, `G-F`, `Coach` |

---

### `Basketball_women.coaches`
Coaching records by season and team. Synonyms: *head coaches, coaching staff*

| Column | Notes |
|--------|-------|
| `coachID` | Unique coach identifier |
| `year` | Season year |
| `tmID` | Team code |
| `lgID` | Enum: `ABL`, `WNBA` |
| `stint` | Stint number within season (0-indexed) |
| `won` | Regular season wins |
| `lost` | Regular season losses |
| `post_wins` | Playoff wins |
| `post_losses` | Playoff losses |
| `playerCoach` | Enum: `Y` (player-coach), null otherwise |

---

### `Basketball_women.draft`
Annual draft records. Synonyms: *draft picks, selections*

| Column | Notes |
|--------|-------|
| `draftYear` | Year of draft |
| `draftRound` | Round number |
| `draftSelection` | Selection within round |
| `draftOverall` | Overall pick number |
| `tmID` | Team that drafted |
| `playerID` | Foreign key to `players.bioID` (null if not in database) |
| `draftFrom` | College or university name |
| `lgID` | Enum: `ABL`, `WNBA` |
| `playedPro` | Enum: `v` (played pro), `x` (did not play pro) |
| `notes` | Enum: `elite`, `initial`, `regular`, `T` (territorial), null |

---

### `Basketball_women.players`
Player biographical data. Synonyms: *roster, athletes*

| Column | Notes |
|--------|-------|
| `bioID` | Primary key; used in `playerID` foreign keys |
| `pos` | Position: `G`, `F`, `C`, `G-F`, `F-G`, `C-F`, `F-C` |
| `firstseason` | First professional season (0 if unknown) |
| `lastseason` | Last professional season (0 if unknown) |
| `height` | In inches |
| `weight` | In pounds |
| `college` | University name |
| `collegeOther` | Junior college or alternative school |
| `birthCountry` | Enum: `USA`, `CAN`, `AUS`, `BRA`, `RUS`, `URS`, `BUL`, `JPN`, `COD` |
| `hsCountry` | High school country |
| `deathDate` | ISO date or `0000-00-00` if living |

---

### `Basketball_women.players_teams`
Player season statistics by team. Synonyms: *player stats, season statistics, performance*

| Column | Notes |
|--------|-------|
| `playerID` | Foreign key to `players.bioID` |
| `year` | Season year |
| `stint` | Stint number (0-indexed; multiple stints = multiple teams in one season) |
| `tmID` | Team code |
| `lgID` | Enum: `ABL`, `WNBA` |
| `GP` | Games played (regular season) |
| `GS` | Games started (regular season) |
| `minutes` | Total minutes (regular season) |
| `points`, `rebounds`, `assists`, `steals`, `blocks`, `turnovers` | Regular season totals |
| `fgMade`, `fgAttempted` | Field goals |
| `ftMade`, `ftAttempted` | Free throws |
| `threeMade`, `threeAttempted` | Three-pointers |
| `oRebounds`, `dRebounds` | Offensive and defensive rebounds |
| `PF` | Personal fouls |
| `dq` | Disqualifications |
| `Post*` columns | Identical stats for playoff games (null if no playoff appearance) |

---

### `Basketball_women.teams`
Team season statistics and standings. Synonyms: *franchises, team records*

| Column | Notes |
|--------|-------|
| `year` | Season year |
| `lgID` | Enum: `ABL`, `WNBA` |
| `tmID` | Team code |
| `franchID` | Franchise identifier |
| `confID` | Conference: `EA` (East), `WE` (West) |
| `rank` | Divisional or conference rank |
| `playoff` | Enum: `Y`, `N` |
| `seeded` | Playoff seed number (0 if not seeded) |
| `firstRound`, `semis`, `finals` | Playoff results: `W` (won), `L` (lost), null (did not play) |
| `won`, `lost`, `GP` | Regular season record and games played |
| `homeW`, `homeL`, `awayW`, `awayL` | Home/away splits |
| `confW`, `confL` | Conference record |
| `o_fgm`, `o_fga`, `o_ftm`, `o_fta`, `o_3pm`, `o_3pa` | Offensive field goals, free throws, three-pointers (made/attempted) |
| `o_oreb`, `o_dreb`, `o_reb` | Offensive rebounds (offensive, defensive, total) |
| `o_asts`, `o_pf`, `o_stl`, `o_to`, `o_blk`, `o_pts` | Offensive assists, fouls, steals, turnovers, blocks, points |
| `d_*` columns | Defensive stats (opponent stats) |
| `tmORB`, `tmDRB`, `tmTRB` | Team total rebounds (offensive, defensive, total) |
| `opptmORB`, `opptmDRB`, `opptmTRB` | Opponent total rebounds |
| `attend` | Total season attendance |
| `arena` | Arena name |

---

### `Basketball_women.teams_post`
Team playoff records by year. Synonyms: *playoff standings, postseason records*

| Column | Notes |
|--------|-------|
| `year` | Season year |
| `tmID` | Team code |
| `lgID` | Enum: `ABL`, `WNBA` |
| `W` | Total playoff wins |
| `L` | Total playoff losses |

---

### `Basketball_women.series_post`
Playoff series results. Synonyms: *playoff matchups, series outcomes*

| Column | Notes |
|--------|-------|
| `year` | Season year |
| `round` | Enum: `FR` (first round), `SF` (semifinal), `CF` (conference final), `F` (finals) |
| `series` | Series identifier (A–G) |
| `tmIDWinner`, `lgIDWinner` | Winning team and league |
| `tmIDLoser`, `lgIDLoser` | Losing team and league |
| `W`, `L` | Series result (wins and losses for winner) |

---

## Synonym Glossary

| Question Term | Schema Reference |
|---|---|
| Career points | `SUM(Basketball_women.players_teams.points)` grouped by `playerID` |
| Career rebounds | `SUM(Basketball_women.players_teams.rebounds)` grouped by `playerID` |
| Career assists | `SUM(Basketball_women.players_teams.assists)` grouped by `playerID` |
| Playoff performance | `Basketball_women.players_teams.Post*` columns |
| Team wins | `Basketball_women.teams.won` |
| Team losses | `Basketball_women.teams.lost` |
| Playoff seed | `Basketball_women.teams.seeded` |
| Conference | `Basketball_women.teams.confID` |
| League | `Basketball_women.teams.lgID` or `Basketball_women.coaches.lgID` |
| Draft class | `Basketball_women.draft.draftYear` |
| Award winner | `Basketball_women.awards_players.award` |
| Coaching record | `Basketball_women.coaches.won`, `Basketball_women.coaches.lost` |
| Player position | `Basketball_women.players.pos` |
| College | `Basketball_women.players.college` |