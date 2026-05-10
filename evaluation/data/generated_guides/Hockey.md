# Hockey Schema Reference Guide

## Schema Summary
This schema contains comprehensive historical ice hockey statistics spanning multiple leagues (NHL, WHA, NHA, PCHA, WCHL), including player scoring and goaltending records, coaching records, team performance, playoff results, awards, and Hall of Fame inductions from 1909 to present.

---

## Join Paths

### Player to Scoring Records
```sql
FROM Hockey.Master m
JOIN Hockey.Scoring s ON m.playerID = s.playerID
```
**[REQUIRED]** — to link player identity to season-by-season scoring stats.

### Player to Goaltending Records
```sql
FROM Hockey.Master m
JOIN Hockey.Goalies g ON m.playerID = g.playerID
```
**[REQUIRED]** — to link player identity to goaltending performance.

### Player to Awards
```sql
FROM Hockey.Master m
JOIN Hockey.AwardsPlayers ap ON m.playerID = ap.playerID
```
**[REQUIRED]** — to identify award-winning players and their achievements.

### Player to Hall of Fame
```sql
FROM Hockey.Master m
JOIN Hockey.HOF hof ON m.hofID = hof.hofID
```
**[REQUIRED]** — to determine Hall of Fame induction year and category.

### Coach to Coaching Records
```sql
FROM Hockey.Master m
JOIN Hockey.Coaches c ON m.coachID = c.coachID
```
**[REQUIRED]** — to link coach identity to season-by-season coaching stats.

### Coach to Awards
```sql
FROM Hockey.Master m
JOIN Hockey.AwardsCoaches ac ON m.coachID = ac.coachID
```
**[REQUIRED]** — to identify award-winning coaches.

### Team Season to Playoff Results
```sql
FROM Hockey.Teams t
JOIN Hockey.TeamsPost tp ON t.year = tp.year AND t.lgID = tp.lgID AND t.tmID = tp.tmID
```
**[REQUIRED]** — to combine regular season and playoff performance for same team-year.

### Playoff Series Details
```sql
FROM Hockey.SeriesPost sp
JOIN Hockey.Teams t_winner ON sp.year = t_winner.year AND sp.lgIDWinner = t_winner.lgID AND sp.tmIDWinner = t_winner.tmID
JOIN Hockey.Teams t_loser ON sp.year = t_loser.year AND sp.lgIDLoser = t_loser.lgID AND sp.tmIDLoser = t_loser.tmID
```
**[REQUIRED]** — to resolve playoff series outcomes to team names and records.

### Team Head-to-Head Records
```sql
FROM Hockey.TeamVsTeam tvt
JOIN Hockey.Teams t_home ON tvt.year = t_home.year AND tvt.lgID = t_home.lgID AND tvt.tmID = t_home.tmID
JOIN Hockey.Teams t_opp ON tvt.year = t_opp.year AND tvt.lgID = t_opp.lgID AND tvt.oppID = t_opp.tmID
```
**[REQUIRED]** — to resolve team abbreviations to full team records in head-to-head matchups.

### Shutout Goalies (Combined)
```sql
FROM Hockey.CombinedShutouts cs
JOIN Hockey.Master m1 ON cs.IDgoalie1 = m1.playerID
JOIN Hockey.Master m2 ON cs.IDgoalie2 = m2.playerID
```
**[OPTIONAL — display only]** — to show goalie names in combined shutout records; filter by `cs.IDgoalie1` and `cs.IDgoalie2` directly when counting.

### Abbreviation Lookup
```sql
FROM Hockey.abbrev a
```
**[OPTIONAL — display only]** — to resolve conference/division/round codes to full names; use raw codes (e.g., `confID`, `divID`, `round`) for filtering and grouping.

---

## Business Rules as SQL

### Plus/Minus Reliability (Pre-1968)
- **EXCLUDE [unreliable plus/minus]:** `WHERE s.year >= 1968` — filter out pre-1968 scoring records when analyzing plus/minus trends.

### Playoff vs. Regular Season Separation
- **IDENTIFY [regular season]:** `WHERE PostGP IS NULL OR PostGP = 'NaN'` — rows in `Hockey.Scoring` with no playoff activity.
- **IDENTIFY [playoff activity]:** `WHERE PostGP IS NOT NULL AND PostGP != 'NaN'` — rows in `Hockey.Scoring` with playoff stats.
- **RULE:** Never aggregate `G` with `PostG`, `A` with `PostA`, or `Pts` with `PostPts` in the same query result row.

### Goalie Backup Classification
- **IDENTIFY [backup goalie]:** `WHERE CAST(Hockey.Goalies.GP AS INTEGER) < 20` — goalies with fewer than 20 games in a season.
- **EXCLUDE [backup goalie from starting rankings]:** `WHERE CAST(Hockey.Goalies.GP AS INTEGER) >= 20` — filter to starting goalies only.

### True Save Percentage (Excluding Empty-Net)
- **Rate:** true_save_pct = (CAST(Hockey.Goalies.SA AS INTEGER) - CAST(Hockey.Goalies.GA AS INTEGER) - CAST(Hockey.Goalies.ENG AS INTEGER)) / (CAST(Hockey.Goalies.SA AS INTEGER) - CAST(Hockey.Goalies.ENG AS INTEGER))
  - Numerator: shots against minus goals allowed minus empty-net goals.
  - Denominator: shots against minus empty-net goals.

### Combined Shutouts Exclusion
- **EXCLUDE [combined shutout from individual totals]:** `WHERE Hockey.playerID NOT IN (SELECT IDgoalie1 FROM Hockey.CombinedShutouts WHERE year = Hockey.Goalies.year AND tmID = Hockey.CombinedShutouts.tmID) AND Hockey.playerID NOT IN (SELECT IDgoalie2 FROM Hockey.CombinedShutouts WHERE year = Hockey.Goalies.year AND tmID = Hockey.CombinedShutouts.tmID)` — when summing individual shutout records, exclude goalies credited in combined shutout games.

### WHA Exclusion from NHL Career Totals
- **EXCLUDE [WHA records from NHL career]:** `WHERE lgID != 'WHA'` — filter out all World Hockey Association records when computing NHL-only career statistics.

### Home Game Scheduling Anomaly Flag
- **IDENTIFY [scheduling anomaly]:** `WHERE CAST(Hockey.TeamSplits.hW AS INTEGER) + CAST(Hockey.TeamSplits.hL AS INTEGER) + CAST(Hockey.TeamSplits.hT AS INTEGER) + CAST(Hockey.TeamSplits.hOTL AS INTEGER) < 41` — teams with fewer than 41 home games in a season.

### Shortened Season Award Exclusion
- **EXCLUDE [shortened season award]:** Subquery required: `WHERE ap.year NOT IN (SELECT year FROM Hockey.Scoring GROUP BY year HAVING COUNT(DISTINCT playerID) > 0 AND AVG(CAST(GP AS INTEGER)) < 60)` — exclude award winners from seasons where league-wide average games played was below 60.

---

## Synonym Glossary

| Question Term | Schema Reference |
|---|---|
| career goals | `SUM(Hockey.Scoring.G)` |
| career assists | `SUM(Hockey.Scoring.A)` |
| career points | `SUM(Hockey.Scoring.Pts)` |
| goals per season (average) | `SUM(Hockey.Scoring.G) / COUNT(DISTINCT Hockey.Scoring.year)` |
| playoff goals | `SUM(Hockey.Scoring.PostG)` |
| playoff points | `SUM(Hockey.Scoring.PostPts)` |
| wins (goalie) | `CAST(Hockey.Goalies.W AS INTEGER)` |
| losses (goalie) | `CAST(Hockey.Goalies.L AS INTEGER)` |
| shutouts | `CAST(Hockey.Goalies.SHO AS INTEGER)` |
| goals against average (GAA) | `CAST(Hockey.Goalies.GA AS INTEGER) / (CAST(Hockey.Goalies.Min AS INTEGER) / 60.0)` |
| wins (coach) | `Hockey.Coaches.w` |
| losses (coach) | `Hockey.Coaches.l` |
| playoff wins (coach) | `CAST(Hockey.Coaches.postw AS INTEGER)` |
| team wins | `Hockey.Teams.W` |
| team losses | `Hockey.Teams.L` |
| goals for | `Hockey.Teams.GF` |
| goals against | `Hockey.Teams.GA` |
| power play goals | `CAST(Hockey.Teams.PPG AS INTEGER)` |
| penalty kill goals | `CAST(Hockey.Teams.PKG AS INTEGER)` |
| Hart Trophy | `WHERE Hockey.AwardsPlayers.award = 'Hart'` |
| Vezina Trophy | `WHERE Hockey.AwardsPlayers.award LIKE '%Vezina%'` |
| All-Star (First Team) | `WHERE Hockey.AwardsPlayers.award = 'First Team All-Star'` |
| All-Star (Second Team) | `WHERE Hockey.AwardsPlayers.award = 'Second Team All-Star'` |
| Jack Adams Award | `WHERE Hockey.AwardsCoaches.award = 'Jack Adams'` |
| Patrick Trophy | `WHERE Hockey.AwardsMisc.award = 'Patrick'` |
| Hall of Fame (Player) | `WHERE Hockey.HOF.category = 'Player'` |
| Hall of Fame (Builder) | `WHERE Hockey.HOF.category = 'Builder'` |
| NHL career | `WHERE Hockey.Scoring.lgID = 'NHL'` |
| WHA career | `WHERE Hockey.Scoring.lgID = 'WHA'` |
| playoff series | `Hockey.SeriesPost` |
| Stanley Cup Finals | `WHERE Hockey.SeriesPost.round = 'F'` |
| Conference Finals | `WHERE Hockey.SeriesPost.round IN ('CF', 'SCF')` |

---

## Table Reference

### `Hockey.Master`
**Meaning:** Player and coach master registry with biographical and career span data.  
**Synonyms:** player registry, coach registry, personnel master.

| Column | Notes |
|---|---|
| `playerID` | Unique player identifier; NULL if coach-only record. |
| `coachID` | Unique coach identifier; NULL if player-only record. |
| `hofID` | Hall of Fame identifier; NULL if not inducted. |
| `firstName`, `lastName` | Legal name; see `nameNote` for alternate names. |
| `nameGiven`, `nameNick` | Full given name and nickname. |
| `height` | In inches; values: 63–81. |
| `weight` | In pounds. |
| `shootCatch` | Handedness: `'L'` (left), `'R'` (right), `'B'` (both). |
| `pos` | Position: `'C'` (center), `'D'` (defense), `'G'` (goalie), `'L'` (left wing), `'R'` (right wing), `'W'` (wing), or combinations (e.g., `'C/D'`, `'D/R'`). |
| `firstNHL`, `lastNHL` | First and last NHL season; NULL if never played NHL. |
| `firstWHA`, `lastWHA` | First and last WHA season; NULL if never played WHA. |
| `birthYear`, `birthMon`, `birthDay`, `birthCountry`, `birthState`, `birthCity` | Birth details. |
| `deathYear`, `deathMon`, `deathDay`, `deathCountry`, `deathState`, `deathCity` | Death details; NULL if living. |

---

### `Hockey.Scoring`
**Meaning:** Player season-by-season regular season scoring statistics.  
**Synonyms:** player stats, season stats, regular season scoring.

| Column | Notes |
|---|---|
| `playerID` | Foreign key to `Hockey.Master`. |
| `year` | Season year. |
| `stint` | Stint number within season (player may change teams mid-season). |
| `tmID` | Team abbreviation. |
| `lgID` | League: `'NHL'`, `'WHA'`, `'NHA'`, `'PCHA'`, `'WCHL'`. |
| `pos` | Position in this season. |
| `GP` | Games played. |
| `G` | Goals. |
| `A` | Assists. |
| `Pts` | Points (G + A). |
| `PIM` | Penalties in minutes. |
| `+/-` | Plus/minus; **unreliable before 1968**. |
| `PPG`, `PPA` | Power play goals and assists. |
| `SHG`, `SHA` | Short-handed goals and assists. |
| `GWG` | Game-winning goals. |
| `GTG` | Golden Ticket goals (overtime winners in playoff context). |
| `SOG` | Shots on goal. |
| `PostGP`, `PostG`, `PostA`, `PostPts`, `PostPIM`, `Post+/-`, `PostPPG`, `PostPPA`, `PostSHG`, `PostSHA`, `PostGWG`, `PostSOG` | Playoff equivalents; **report separately from regular season**. |

---

### `Hockey.Goalies`
**Meaning:** Goaltender season-by-season regular season statistics.  
**Synonyms:** goalie stats, goaltending records.

| Column | Notes |
|---|---|
| `playerID` | Foreign key to `Hockey.Master`. |
| `year` | Season year. |
| `stint` | Stint number within season. |
| `tmID` | Team abbreviation. |
| `lgID` | League: `'NHL'`, `'WHA'`, `'NHA'`, `'PCHA'`, `'WCHL'`. |
| `GP` | Games played; **exclude from starting rankings if < 20**. |
| `Min` | Minutes played. |
| `W`, `L`, `T/OL` | Wins, losses, ties/overtime losses. |
| `ENG` | Empty-net goals allowed; **exclude from save percentage denominator**. |
| `SHO` | Shutouts; **exclude combined shutouts** (see `Hockey.CombinedShutouts`). |
| `GA` | Goals allowed. |
| `SA` | Shots against. |
| `PostGP`, `PostMin`, `PostW`, `PostL`, `PostT`, `PostENG`, `PostSHO`, `PostGA`, `PostSA` | Playoff equivalents; **report separately from regular season**. |

---

### `Hockey.AwardsPlayers`
**Meaning:** Individual player awards and honors by season.  
**Synonyms:** player awards, honors, accolades.

| Column | Notes |
|---|---|
| `playerID` | Foreign key to `Hockey.Master`. |
| `award` | Award name (e.g., `'Hart'`, `'Vezina'`, `'First Team All-Star'`, `'Second Team All-Star'`). |
| `year` | Award year. |
| `lgID` | League: `'NHL'`, `'WHA'`. |
| `note` | Award context: `'MVP'`, `'Rookie'`, `'Scoring'`, `'Best Defenceman'`, `'Best Goaltender'`, `'Most Gentlemanly'`, `'tie'`, `'shared'`. |
| `pos` | Position at time of award. |

---

### `Hockey.AwardsCoaches`
**Meaning:** Coach awards and honors by season.  
**Synonyms:** coach awards, coaching honors.

| Column | Notes |
|---|---|
| `coachID` | Foreign key to `Hockey.Master`. |
| `award` | Award name: `'Jack Adams'`, `'First Team All-Star'`, `'Second Team All-Star'`, `'Baldwin'`, `'Schmertz'`. |
| `year` | Award year. |
| `lgID` | League: `'NHL'`, `'WHA'`. |

---

### `Hockey.AwardsMisc`
**Meaning:** Organizational and team awards (e.g., Patrick Trophy).  
**Synonyms:** miscellaneous awards, organizational honors.

| Column | Notes |
|---|---|
| `name` | Recipient name (may be team or individual). |
| `ID` | Recipient identifier; often NULL for teams. |
| `award` | Award name: `'Patrick'`. |
| `year` | Award year. |
| `lgID` | League: `'NHL'`. |
| `note` | Context: `'posthumous'` or NULL. |

---

### `Hockey.HOF`
**Meaning:** Hall of Fame induction records.  
**Synonyms:** Hall of Fame, induction, enshrinement.

| Column | Notes |
|---|---|
| `year` | Induction year. |
| `hofID` | Hall of Fame identifier; foreign key to `Hockey.Master.hofID`. |
| `name` | Inductee name. |
| `category` | `'Player'`, `'Builder'`, or `'Referee/Linesman'`. |

---

### `Hockey.Coaches`
**Meaning:** Coach season-by-season regular season and playoff records.  
**Synonyms:** coaching records, coach stats.

| Column | Notes |
|---|---|
| `coachID` | Foreign key to `Hockey.Master`. |
| `year` | Season year. |
| `tmID` | Team abbreviation. |
| `lgID` | League: `'NHA'`, `'NHL'`, `'PCHA'`, `'WCHL'`, `'WHA'`. |
| `stint` | Stint number within season. |
| `notes` | Context: `'interim'`, `'co-coach with [name]'`, or NULL. |
| `g`, `w`, `l`, `t` | Regular season games, wins, losses, ties. |
| `postg`, `postw`, `postl`, `postt` | Playoff games, wins, losses, ties. |

---

### `Hockey.Teams`
**Meaning:** Team season-by-season regular season performance and standings.  
**Synonyms:** team stats, season standings, team records.

| Column | Notes |
|---|---|
| `year` | Season year. |
| `lgID` | League: `'NHA'`, `'NHL'`, `'PCHA'`, `'WCHL'`, `'WHA'`. |
| `tmID` | Team abbreviation. |
| `franchID` | Franchise identifier (teams may relocate). |
| `confID` | Conference: `'EC'` (Eastern), `'WC'` (Western), `'CC'` (Campbell), `'WA'` (Wales). |
| `divID` | Division: `'AD'` (Adams), `'AT'` (Atlantic), `'NE'` (Northeast), `'SE'` (Southeast), `'NW'` (Northwest), `'PC'` (Pacific), `'CE'` (Central), `'WD'` (West), etc. |
| `rank` | Standings rank within league. |
| `playoff` | Playoff qualification indicator; NULL if no playoffs. |
| `G`, `W`, `L`, `T` | Games, wins, losses, ties. |
| `OTL` | Overtime losses (modern era). |
| `Pts` | Points (2 per win, 1 per tie/OTL). |
| `SoW`, `SoL` | Shootout wins and losses. |
| `GF`, `GA` | Goals for and against. |
| `name` | Team name. |
| `PIM`, `BenchMinor`, `PPG`, `PPC`, `SHA`, `PKG`, `PKC`, `SHF` | Discipline and special teams stats; often NULL in early seasons. |

---

### `Hockey.TeamsPost`
**Meaning:** Team playoff season performance.  
**Synonyms:** playoff stats, postseason records.

| Column | Notes |
|---|---|
| `year` | Season year. |
| `lgID` | League. |
| `tmID` | Team abbreviation. |
| `G`, `W`, `L`, `T` | Playoff games, wins, losses, ties. |
| `GF`, `GA` | Playoff goals for and against. |
| `PIM`, `BenchMinor`, `PPG`, `PPC`, `SHA`, `PKG`, `PKC`, `SHF` | Playoff discipline and special teams stats. |

---

### `Hockey.SeriesPost`
**Meaning:** Playoff series results and matchups.  
**Synonyms:** playoff series, playoff matchups, series results.

| Column | Notes |
|---|---|
| `year` | Season year. |
| `round` | Round code: `'F'` (Finals), `'CF'` (Conference Finals), `'SCF'` (Stanley Cup Finals), `'SF'` (Semifinals), `'QF'` (Quarterfinals), `'CQF'` (Conference Quarterfinals), `'CSF'` (Conference Semifinals), `'ACF'` (Adams Conference Finals), `'DF'` (Division Finals), `'DSF'` (Division Semifinals), `'WP'` (Wild Card Playoff), `'Pre'` (Preliminary), `'SCSF'` (Stanley Cup Semifinals). |
| `series` | Series identifier within round (A–O). |
| `tmIDWinner`, `lgIDWinner` | Winning team and league. |
| `tmIDLoser`, `lgIDLoser` | Losing team and league. |
| `W`, `L`, `T` | Series wins, losses, ties. |
| `GoalsWinner`, `GoalsLoser` | Total goals scored in series. |
| `note` | Context: `'EX'` (exhibition), `'TG'` (total goals), `'ND'` (no decision), `'DEF'` (default). |

---

### `Hockey.TeamVsTeam`
**Meaning:** Head-to-head records between two teams in a season.  
**Synonyms:** team matchups, head-to-head records.

| Column | Notes |
|---|---|
| `year` | Season year. |
| `lgID` | League. |
| `tmID` | Team abbreviation (home/reference team). |
| `oppID` | Opponent team abbreviation. |
| `W`, `L`, `T` | Wins, losses, ties by `tmID` against `oppID`. |
| `OTL` | Overtime losses. |

---

### `Hockey.TeamSplits`
**Meaning:** Team performance split by home/road and by month.  
**Synonyms:** monthly splits, home/road splits.

| Column | Notes |
|---|---|
| `year` | Season year. |
| `lgID` | League. |
| `tmID` | Team abbreviation. |
| `hW`, `hL`, `hT`, `hOTL` | Home wins, losses, ties, overtime losses. |
| `rW`, `rL`, `rT`, `rOTL` | Road wins, losses, ties, overtime losses. |
| `SepW`, `SepL`, `SepT`, `SepOL` | September performance. |
| `OctW`, `OctL`, `OctT`, `OctOL` | October performance. |
| `NovW`, `NovL`, `NovT`, `NovOL` | November performance. |
| `DecW`, `DecL`, `DecT`, `DecOL` | December performance. |
| `JanW`, `JanL`, `JanT`, `JanOL` | January performance. |
| `FebW`, `FebL`, `FebT`, `FebOL` | February performance. |
| `MarW`, `MarL`, `MarT`, `MarOL` | March performance. |
| `AprW`, `AprL`, `AprT`, `AprOL` | April performance. |

---

### `Hockey.CombinedShutouts`
**Meaning:** Shutout games where two goalies shared the shutout.  
**Synonyms:** shared shutouts, combined shutout records.

| Column | Notes |
|---|---|
| `year` | Season year. |
| `month`, `date` | Game date. |
| `tmID` | Team that recorded shutout. |
| `oppID` | Opponent team. |
| `R/P` | `'R'` (regular season) or `'P'` (playoff). |
| `IDgoalie1`, `IDgoalie2` | Player IDs of goalies sharing shutout; **exclude from individual shutout totals**. |

---

### `Hockey.Goalies SC` (Stanley Cup Era)
**Meaning:** Goaltender statistics from Stanley Cup era (pre-modern NHL).  
**Synonyms:** Stanley Cup goalie stats, historical goaltending.

| Column | Notes |
|---|---|
| `playerID` | Foreign key to `Hockey.Master`. |
| `year` | Season year. |
| `tmID` | Team abbreviation (Stanley Cup era teams). |
| `lgID` | League: `'NHA'`, `'NHL'`, `'PCHA'`, `'WCHL'`. |
| `GP`, `Min`, `W`, `L`, `T`, `SHO`, `GA` | Games, minutes, wins, losses, ties, shutouts, goals allowed. |

---

### `Hockey.GoaliesShootout`
**Meaning:** Goaltender shootout performance (modern era).  
**Synonyms:** shootout stats, shootout performance.

| Column | Notes |
|---|---|
| `playerID` | Foreign key to `Hockey.Master`. |
| `year` | Season year. |
| `stint` | Stint number. |
| `tmID` | Team abbreviation. |
| `W`, `L` | Shootout wins and losses. |
| `SA`, `GA` | Shootout shots against and goals allowed. |

---

### `Hockey.Scoring SC` (Stanley Cup Era)
**Meaning:** Player scoring statistics from Stanley Cup era (pre-modern NHL).  
**Synonyms:** Stanley Cup scoring stats, historical scoring.

| Column | Notes |
|---|---|
| `playerID` | Foreign key to `Hockey.Master`. |
| `year` | Season year. |
| `tmID` | Team abbreviation (Stanley Cup era teams). |
| `lgID` | League: `'NHA'`, `'NHL'`, `'PCHA'`, `'WCHL'`. |
| `pos` | Position. |
| `GP`, `G`, `A`, `Pts`, `PIM` | Games, goals, assists, points, penalties. |

---

### `Hockey.ScoringShootout`
**Meaning:** Player shootout performance (modern era).  
**Synonyms:** shootout scoring, shootout goals.

| Column | Notes |
|---|---|
| `playerID` | Foreign key to `Hockey.Master`. |
| `year` | Season year. |
| `stint` | Stint number. |
| `tmID` | Team abbreviation. |
| `S` | Shootout attempts. |
| `G` | Shootout goals. |
| `GDG` | Game-deciding goals (shootout winners). |

---

### `Hockey.ScoringSup`
**Meaning:** Supplemental scoring data (power play and short-handed assists).  
**Synonyms:** supplemental stats, special teams assists.

| Column | Notes |
|---|---|
| `playerID` | Foreign key to `Hockey.Master`. |
| `year` | Season year. |
| `PPA` | Power play assists (supplemental). |
| `SHA` | Short-handed assists (supplemental). |

---

### `Hockey.TeamsSC` (Stanley Cup Era)
**Meaning:** Team statistics from Stanley Cup era (pre-modern NHL).  
**Synonyms:** Stanley Cup team stats, historical team records.

| Column | Notes |
|---|---|
| `year` | Season year. |
| `lgID` | League: `'NHA'`, `'NHL'`, `'PCHA'`, `'WCHL'`. |
| `tmID` | Team abbreviation (Stanley Cup era teams). |
| `G`, `W`, `L`, `T` | Games, wins, losses, ties. |
| `GF`, `GA` | Goals for and against. |
| `PIM` | Penalties in minutes. |

---

### `Hockey.TeamsHalf`
**Meaning:** Team performance split by season half (used in early NHL seasons with split schedules).  
**Synonyms:** half-season splits, season splits.

| Column | Notes |
|---|---|
| `year` | Season year. |
| `lgID` | League: `'NHA'`, `'NHL'`. |
| `tmID` | Team abbreviation. |
| `half` | Half number (1 or 2). |
| `rank` | Rank within half. |
| `G`, `W`, `L`, `T` | Games, wins, losses, ties in half. |
| `GF`, `GA` | Goals for and against in half. |

---

### `Hockey.abbrev`
**Meaning:** Lookup table for abbreviation codes and their full names.  
**Synonyms:** abbreviation reference, code lookup.

| Column | Notes |
|---|---|
| `Type` | Category: `'Conference'`, `'Division'`, `'Playoffs'`, `'Round'`. |
| `Code` | Abbreviation code (e.g., `'EC'`, `'AD'`, `'F'`). |
| `Fullname` | Full name (e.g., `'Eastern Conference'`, `'Adams Division'`, `'Finals'`). |