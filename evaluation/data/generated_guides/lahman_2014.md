# Lahman Baseball Database (2014) — SQL Agent Reference Guide

## Schema Summary

The Lahman database contains comprehensive historical baseball statistics (1871–2014) covering player performance (batting, pitching, fielding), team records, managerial data, awards, Hall of Fame voting, and player biographical information.

---

## Join Paths

### Player to Batting Stats
```sql
FROM lahman_2014.players p
JOIN lahman_2014.batting b ON p.playerID = b.playerID
```
**[REQUIRED]** — to link player names/biographical data to seasonal batting records.

### Player to Pitching Stats
```sql
FROM lahman_2014.players p
JOIN lahman_2014.pitching pi ON p.playerID = pi.playerID
```
**[REQUIRED]** — to link player names/biographical data to seasonal pitching records.

### Player to Fielding Stats
```sql
FROM lahman_2014.players p
JOIN lahman_2014.fielding f ON p.playerID = f.playerID
```
**[REQUIRED]** — to link player names/biographical data to seasonal fielding records.

### Player to Hall of Fame
```sql
FROM lahman_2014.players p
JOIN lahman_2014.halloffame h ON p.hofID = h.hofID
```
**[REQUIRED]** — to link player biographical data to Hall of Fame voting records. **Always filter with `h.inducted = 'Y' AND h.category = 'Player'` for actual Hall of Famers.**

### Player to Awards
```sql
FROM lahman_2014.players p
JOIN lahman_2014.awardsplayers ap ON p.playerID = ap.playerID
```
**[REQUIRED]** — to link player names to award records (MVP, Cy Young, Triple Crown, etc.).

### Player to Salaries
```sql
FROM lahman_2014.players p
JOIN lahman_2014.salaries s ON p.playerID = s.playerID
```
**[REQUIRED]** — to link player names to salary records (1985–2014).

### Player to Schools
```sql
FROM lahman_2014.players p
JOIN lahman_2014.schoolsplayers sp ON p.playerID = sp.playerID
JOIN lahman_2014.schools sc ON sp.schoolID = sc.schoolID
```
**[REQUIRED]** — to link player names to college/university attendance.

### Batting to Teams
```sql
FROM lahman_2014.batting b
JOIN lahman_2014.teams t ON b.yearID = t.yearID AND b.teamID = t.teamID AND b.lgID = t.lgID
```
**[REQUIRED]** — to link individual batting records to team context (wins, losses, park effects).

### Pitching to Teams
```sql
FROM lahman_2014.pitching pi
JOIN lahman_2014.teams t ON pi.yearID = t.yearID AND pi.teamID = t.teamID AND pi.lgID = t.lgID
```
**[REQUIRED]** — to link individual pitching records to team context.

### Fielding to Teams
```sql
FROM lahman_2014.fielding f
JOIN lahman_2014.teams t ON f.yearID = t.yearID AND f.teamID = t.teamID AND f.lgID = t.lgID
```
**[REQUIRED]** — to link individual fielding records to team context.

### Manager to Teams
```sql
FROM lahman_2014.managers m
JOIN lahman_2014.teams t ON m.yearID = t.yearID AND m.teamID = t.teamID AND m.lgID = t.lgID
```
**[REQUIRED]** — to link managerial records to team performance.

### Manager to Awards
```sql
FROM lahman_2014.managers m
JOIN lahman_2014.awardsmanagers am ON m.managerID = am.managerID AND m.yearID = am.yearID
```
**[REQUIRED]** — to link manager names to Manager of the Year awards.

### Playoff Batting to Teams
```sql
FROM lahman_2014.battingpost bp
JOIN lahman_2014.teams t ON bp.yearID = t.yearID AND bp.teamID = t.teamID AND bp.lgID = t.lgID
```
**[REQUIRED]** — to link postseason batting to team playoff context.

### Playoff Pitching to Teams
```sql
FROM lahman_2014.pitchingpost pp
JOIN lahman_2014.teams t ON pp.yearID = t.yearID AND pp.teamID = t.teamID AND pp.lgID = t.lgID
```
**[REQUIRED]** — to link postseason pitching to team playoff context.

### All-Star Appearances to Players
```sql
FROM lahman_2014.allstarfull asf
JOIN lahman_2014.players p ON asf.playerID = p.playerID
```
**[REQUIRED]** — to link All-Star game appearances to player names. **Note: All-Star games before 1933 are not comparable to later years.**

### Team to Franchise History
```sql
FROM lahman_2014.teams t
JOIN lahman_2014.teamsfranchises tf ON t.franchID = tf.franchID
```
**[OPTIONAL — display only]** — to show franchise name and active status alongside team records.

### Postseason Series Results
```sql
FROM lahman_2014.seriespost sp
JOIN lahman_2014.teams t_winner ON sp.yearID = t_winner.yearID AND sp.teamIDwinner = t_winner.teamID
JOIN lahman_2014.teams t_loser ON sp.yearID = t_loser.yearID AND sp.teamIDloser = t_loser.teamID
```
**[REQUIRED]** — to link playoff series outcomes to team records.

---

## Business Rules as SQL

### Batting Metrics

**IDENTIFY [Qualified Batter]:** `WHERE lahman_2014.batting.AB >= 100` — players with 100+ at-bats in a season are eligible for rate statistics (BA, OBP, SLG).

**EXCLUDE [Insufficient At-Bats]:** `WHERE lahman_2014.batting.AB < 100` — exclude from rate statistics comparisons.

**Rate: Batting Average (BA)** = `SUM(H) / SUM(AB)` — hits divided by at-bats only; **never include walks in denominator**.

**Rate: On-Base Percentage (OBP)** = `(SUM(H) + SUM(BB) + SUM(HBP) + SUM(SF)) / (SUM(AB) + SUM(BB) + SUM(HBP) + SUM(SF))` — includes walks, hit-by-pitch, and sacrifice flies.

**Rate: Slugging Percentage (SLG)** = `(SUM(H) + SUM(2B) + 2*SUM(2B) + 3*SUM(3B) + 4*SUM(HR)) / SUM(AB)` — total bases (1B=1, 2B=2, 3B=3, HR=4) divided by at-bats.

### Pitching Standards

**IDENTIFY [Reliever]:** `WHERE lahman_2014.pitching.IPouts < 150` — pitchers with fewer than 50 innings pitched (150 outs) in a season.

**IDENTIFY [Starter]:** `WHERE lahman_2014.pitching.IPouts >= 150` — pitchers with 50+ innings pitched in a season.

**Rate: ERA (Earned Run Average)** = `(SUM(ER) * 9) / (SUM(IPouts) / 3)` — earned runs × 9 divided by innings pitched (convert outs to innings: IPouts / 3).

**Rate: WHIP (Walks + Hits per Innings Pitched)** = `(SUM(BB) + SUM(H)) / (SUM(IPouts) / 3)` — walks plus hits divided by innings pitched.

**IDENTIFY [Quality Start]:** `WHERE lahman_2014.pitching.IPouts >= 18 AND lahman_2014.pitching.ER <= 3` — 6+ innings pitched (18+ outs) with 3 or fewer earned runs.

### Fielding Calculations

**Rate: Fielding Percentage** = `(SUM(PO) + SUM(A)) / (SUM(PO) + SUM(A) + SUM(E))` — putouts plus assists divided by putouts plus assists plus errors.

**IDENTIFY [Utility Player]:** `WHERE COUNT(DISTINCT lahman_2014.fielding.POS) > 1` — players appearing at multiple positions in a season; report fielding stats per position, not aggregated.

### Historical Adjustments

**IDENTIFY [Dead-Ball Era]:** `WHERE lahman_2014.batting.yearID < 1920 OR lahman_2014.pitching.yearID < 1920` — pre-1920 statistics require era adjustment when comparing across time periods.

**IDENTIFY [Steroid Era]:** `WHERE lahman_2014.batting.yearID BETWEEN 1994 AND 2004 OR lahman_2014.pitching.yearID BETWEEN 1994 AND 2004` — 1994–2004 statistics reported as-is but flagged for comparative analysis.

### Award and Recognition

**IDENTIFY [MVP Winner]:** `WHERE lahman_2014.awardsshareplayers.awardID = 'MVP' AND lahman_2014.awardsshareplayers.votesFirst > 0` — use first-place votes as primary metric, not total points.

**IDENTIFY [Cy Young Winner]:** `WHERE lahman_2014.awardsshareplayers.awardID = 'Cy Young' AND lahman_2014.awardsshareplayers.votesFirst > 0` — use first-place votes as primary metric.

**IDENTIFY [Rookie of the Year Winner]:** `WHERE lahman_2014.awardsshareplayers.awardID = 'Rookie of the Year' AND lahman_2014.awardsshareplayers.votesFirst > 0` — use first-place votes as primary metric.

**IDENTIFY [Pre-1933 All-Star]:** `WHERE lahman_2014.allstarfull.yearID < 1933` — All-Star appearances before 1933 (first game) cannot be compared with later years.

### Hall of Fame Table Structure

**IDENTIFY [Hall of Fame Player]:** `WHERE lahman_2014.halloffame.inducted = 'Y' AND lahman_2014.halloffame.category = 'Player'` — actual Hall of Fame members (players only). **Always apply both filters together.**

**IDENTIFY [Hall of Fame Manager]:** `WHERE lahman_2014.halloffame.inducted = 'Y' AND lahman_2014.halloffame.category = 'Manager'` — Hall of Fame managers.

**IDENTIFY [Hall of Fame Umpire]:** `WHERE lahman_2014.halloffame.inducted = 'Y' AND lahman_2014.halloffame.category = 'Umpire'` — Hall of Fame umpires.

**IDENTIFY [Hall of Fame Executive/Pioneer]:** `WHERE lahman_2014.halloffame.inducted = 'Y' AND lahman_2014.halloffame.category = 'Pioneer/Executive'` — Hall of Fame executives and pioneers.

**IDENTIFY [Hall of Fame Ballot Record (All)]:** `WHERE lahman_2014.halloffame.inducted IN ('Y', 'N')` — all voting/nomination records, including unsuccessful candidates.

**IDENTIFY [Hall of Fame Voting Progress]:** `ORDER BY lahman_2014.halloffame.yearID ASC` — track year-over-year voting progression; voting percentage is cumulative.

### Team Performance

**Rate: Pythagorean Wins (Expected)** = `POWER(SUM(R), 2) / (POWER(SUM(R), 2) + POWER(SUM(RA), 2)) * SUM(G)` — expected wins based on runs scored vs. runs allowed.

**IDENTIFY [Lucky Team]:** `WHERE (lahman_2014.teams.W - POWER(SUM(R), 2) / (POWER(SUM(R), 2) + POWER(SUM(RA), 2)) * SUM(G)) > 5` — teams outperforming Pythagorean expectation by more than 5 wins; flag for regression analysis.

**IDENTIFY [Playoff Performance]:** `WHERE lahman_2014.battingpost.yearID IS NOT NULL OR lahman_2014.pitchingpost.yearID IS NOT NULL` — postseason records; weight separately from regular season for clutch analysis.

---

## Synonym Glossary

| Question Term | Schema Identifier |
|---|---|
| career hits | `SUM(lahman_2014.batting.H)` |
| career home runs | `SUM(lahman_2014.batting.HR)` |
| career RBIs | `SUM(lahman_2014.batting.RBI)` |
| career runs | `SUM(lahman_2014.batting.R)` |
| career stolen bases | `SUM(lahman_2014.batting.SB)` |
| career strikeouts (pitcher) | `SUM(lahman_2014.pitching.SO)` |
| career wins (pitcher) | `SUM(lahman_2014.pitching.W)` |
| career ERA | `(SUM(lahman_2014.pitching.ER) * 9) / (SUM(lahman_2014.pitching.IPouts) / 3)` |
| career batting average | `SUM(lahman_2014.batting.H) / SUM(lahman_2014.batting.AB)` |
| career slugging percentage | `(SUM(lahman_2014.batting.H) + SUM(lahman_2014.batting.2B) + 2*SUM(lahman_2014.batting.2B) + 3*SUM(lahman_2014.batting.3B) + 4*SUM(lahman_2014.batting.HR)) / SUM(lahman_2014.batting.AB)` |
| career on-base percentage | `(SUM(lahman_2014.batting.H) + SUM(lahman_2014.batting.BB) + SUM(lahman_2014.batting.HBP) + SUM(lahman_2014.batting.SF)) / (SUM(lahman_2014.batting.AB) + SUM(lahman_2014.batting.BB) + SUM(lahman_2014.batting.HBP) + SUM(lahman_2014.batting.SF))` |
| All-Star appearances | `COUNT(lahman_2014.allstarfull.playerID)` |
| Hall of Fame | `lahman_2014.halloffame WHERE inducted = 'Y' AND category = 'Player'` |
| MVP award | `lahman_2014.awardsshareplayers WHERE awardID = 'MVP'` |
| Cy Young award | `lahman_2014.awardsshareplayers WHERE awardID = 'Cy Young'` |
| Rookie of the Year | `lahman_2014.awardsshareplayers WHERE awardID = 'Rookie of the Year'` |
| Triple Crown | `lahman_2014.awardsplayers WHERE awardID = 'Triple Crown'` |
| Manager of the Year | `lahman_2014.awardsmanagers WHERE awardID IN ('BBWAA Manager of the year', 'TSN Manager of the Year')` |
| postseason batting | `lahman_2014.battingpost` |
| postseason pitching | `lahman_2014.pitchingpost` |
| World Series | `lahman_2014.seriespost WHERE round = 'WS'` |
| playoff series | `lahman_2014.seriespost` |
| team salary | `SUM(lahman_2014.salaries.salary)` |
| fielding percentage | `(SUM(lahman_2014.fielding.PO) + SUM(lahman_2014.fielding.A)) / (SUM(lahman_2014.fielding.PO) + SUM(lahman_2014.fielding.A) + SUM(lahman_2014.fielding.E))` |

---

## Table Reference

### `lahman_2014.players`
**Meaning:** Player biographical data and career identifiers.  
**Synonyms:** player master, player registry.

| Column | Notes |
|---|---|
| `playerID` | Unique player identifier (primary key); used across all performance tables. |
| `managerID` | Non-null if player also managed; links to `lahman_2014.managers`. |
| `hofID` | Non-null if player has Hall of Fame voting record; links to `lahman_2014.halloffame`. |
| `nameFirst`, `nameLast` | Player's first and last name. |
| `nameGiven` | Full given name (may differ from `nameFirst`). |
| `nameNick` | Nickname(s), comma-separated. |
| `birthYear`, `birthMonth`, `birthDay` | Birth date components. |
| `birthCountry`, `birthState`, `birthCity` | Birth location. |
| `deathYear`, `deathMonth`, `deathDay` | Death date components (NULL if living). |
| `deathCountry`, `deathState`, `deathCity` | Death location. |
| `height`, `weight` | Physical measurements (inches, pounds). |
| `bats` | Handedness: `'L'` (left), `'R'` (right), `'B'` (both). |
| `throws` | Throwing arm: `'L'` (left), `'R'` (right). |
| `debut`, `finalGame` | First and last game dates (YYYY-MM-DD format). |
| `college` | College/university name if attended. |
| `lahman40ID`, `lahman45ID`, `retroID`, `holtzID`, `bbrefID` | Cross-reference IDs to other baseball databases. |

---

### `lahman_2014.batting`
**Meaning:** Annual batting statistics by player, team, and stint.  
**Synonyms:** batting stats, offensive statistics, hitting statistics.

| Column | Notes |
|---|---|
| `playerID` | Links to `lahman_2014.players`. |
| `yearID` | Season year. |
| `stint` | Sequence number if player changed teams mid-season (1, 2, 3, etc.). |
| `teamID` | Team code (e.g., `'NYY'`, `'BOS'`). |
| `lgID` | League: `'AL'`, `'NL'`, `'AA'`, `'FL'`, `'NA'`, `'PL'`, `'UA'`. |
| `G` | Games played. |
| `G_batting` | Games with at-bat (may differ from `G`). |
| `AB` | At-bats. **Denominator for BA and SLG; exclude walks.** |
| `R` | Runs scored. |
| `H` | Hits. |
| `2B` | Doubles. |
| `3B` | Triples. |
| `HR` | Home runs. |
| `RBI` | Runs batted in. |
| `SB` | Stolen bases. |
| `CS` | Caught stealing. |
| `BB` | Walks (bases on balls). **Include in OBP numerator.** |
| `SO` | Strikeouts. |
| `IBB` | Intentional walks. |
| `HBP` | Hit by pitch. **Include in OBP numerator.** |
| `SH` | Sacrifice hits (bunts). |
| `SF` | Sacrifice flies. **Include in OBP numerator.** |
| `GIDP` | Grounded into double play. |
| `G_old` | Games (legacy column; use `G` instead). |

---

### `lahman_2014.pitching`
**Meaning:** Annual pitching statistics by player, team, and stint.  
**Synonyms:** pitching stats, pitching statistics.

| Column | Notes |
|---|---|
| `playerID` | Links to `lahman_2014.players`. |
| `yearID` | Season year. |
| `stint` | Sequence number if pitcher changed teams mid-season. |
| `teamID` | Team code. |
| `lgID` | League: `'AL'`, `'NL'`, `'AA'`, `'FL'`, `'NA'`, `'PL'`, `'UA'`. |
| `W` | Wins. |
| `L` | Losses. |
| `G` | Games pitched. |
| `GS` | Games started. |
| `CG` | Complete games. |
| `SHO` | Shutouts. |
| `SV` | Saves. |
| `IPouts` | Innings pitched (in outs; divide by 3 for innings). **Use for reliever/starter classification and ERA/WHIP calculation.** |
| `H` | Hits allowed. **Include in WHIP numerator.** |
| `ER` | Earned runs. **Numerator for ERA.** |
| `HR` | Home runs allowed. |
| `BB` | Walks allowed. **Include in WHIP numerator.** |
| `SO` | Strikeouts. |
| `BAOpp` | Batting average against (legacy; calculate from H and AB). |
| `ERA` | Earned run average (pre-calculated; verify with formula). |
| `IBB` | Intentional walks. |
| `WP` | Wild pitches. |
| `HBP` | Hit batters. |
| `BK` | Balks. |
| `BFP` | Batters faced. |
| `GF` | Games finished (relief appearances). |
| `R` | Runs allowed (earned + unearned). |
| `SH` | Sacrifice hits allowed. |
| `SF` | Sacrifice flies allowed. |
| `GIDP` | Grounded into double play (induced). |

---

### `lahman_2014.fielding`
**Meaning:** Annual fielding statistics by player, team, position, and stint.  
**Synonyms:** fielding stats, defensive statistics.

| Column | Notes |
|---|---|
| `playerID` | Links to `lahman_2014.players`. |
| `yearID` | Season year. |
| `stint` | Sequence number if player changed teams mid-season. |
| `teamID` | Team code. |
| `lgID` | League. |
| `POS` | Position: `'P'` (pitcher), `'C'` (catcher), `'1B'`, `'2B'`, `'3B'`, `'SS'`, `'LF'`, `'CF'`, `'RF'`, `'OF'` (outfield), `'DH'` (DH). **Report per position for utility players; do not aggregate.** |
| `G` | Games at position. |
| `GS` | Games started at position. |
| `InnOuts` | Innings played (in outs; divide by 3 for innings). |
| `PO` | Putouts. **Include in fielding percentage numerator.** |
| `A` | Assists. **Include in fielding percentage numerator.** |
| `E` | Errors. **Include in fielding percentage denominator.** |
| `DP` | Double plays. |
| `PB` | Passed balls (catchers only). |
| `WP` | Wild pitches (pitchers only). |
| `SB` | Stolen bases allowed (catchers only). |
| `CS` | Caught stealing (catchers only). |
| `ZR` | Zone rating (advanced metric; sparse data). |

---

### `lahman_2014.fieldingof`
**Meaning:** Outfield position breakdown (LF, CF, RF) for players with outfield appearances.  
**Synonyms:** outfield fielding, outfield position split.

| Column | Notes |
|---|---|
| `playerID` | Links to `lahman_2014.players`. |
| `yearID` | Season year. |
| `stint` | Sequence number. |
| `Glf` | Games in left field. |
| `Gcf` | Games in center field. |
| `Grf` | Games in right field. |

---

### `lahman_2014.battingpost`
**Meaning:** Postseason batting statistics by player, team, and playoff round.  
**Synonyms:** playoff batting, postseason hitting.

| Column | Notes |
|---|---|
| `playerID` | Links to `lahman_2014.players`. |
| `yearID` | Season year. |
| `round` | Playoff round: `'ALDS1'`, `'ALDS2'`, `'ALCS'`, `'ALWC'`, `'AEDIV'`, `'AWDIV'`, `'NLDS1'`, `'NLDS2'`, `'NLCS'`, `'NLWC'`, `'NEDIV'`, `'NWDIV'`, `'WS'` (World Series), `'CS'` (Championship Series, pre-1969). |
| `teamID` | Team code. |
| `lgID` | League: `'AL'`, `'NL'`, `'AA'`. |
| `G`, `AB`, `R`, `H`, `2B`, `3B`, `HR`, `RBI`, `SB`, `CS`, `BB`, `SO`, `IBB`, `HBP`, `SH`, `SF`, `GIDP` | Same semantics as `lahman_2014.batting`. |

---

### `lahman_2014.pitchingpost`
**Meaning:** Postseason pitching statistics by player, team, and playoff round.  
**Synonyms:** playoff pitching, postseason pitching.

| Column | Notes |
|---|---|
| `playerID` | Links to `lahman_2014.players`. |
| `yearID` | Season year. |
| `round` | Playoff round (see `lahman_2014.battingpost.round`). |
| `teamID` | Team code. |
| `lgID` | League. |
| `W`, `L`, `G`, `GS`, `CG`, `SHO`, `SV`, `IPouts`, `H`, `ER`, `HR`, `BB`, `SO`, `BAOpp`, `ERA`, `IBB`, `WP`, `HBP`, `BK`, `BFP`, `GF`, `R`, `SH`, `SF`, `GIDP` | Same semantics as `lahman_2014.pitching`. |

---

### `lahman_2014.fieldingpost`
**Meaning:** Postseason fielding statistics by player, team, position, and playoff round.  
**Synonyms:** playoff fielding, postseason defense.

| Column | Notes |
|---|---|
| `playerID` | Links to `lahman_2014.players`. |
| `yearID` | Season year. |
| `teamID` | Team code. |
| `lgID` | League. |
| `round` | Playoff round. |
| `POS` | Position (see `lahman_2014.fielding.POS`). |
| `G`, `GS`, `InnOuts`, `PO`, `A`, `E`, `DP`, `TP`, `PB`, `SB`, `CS` | Same semantics as `lahman_2014.fielding`; `TP` = triple plays. |

---

### `lahman_2014.teams`
**Meaning:** Annual team statistics and standings.  
**Synonyms:** team stats, team records, team performance.

| Column | Notes |
|---|---|
| `yearID` | Season year. |
| `lgID` | League. |
| `teamID` | Team code (e.g., `'NYY'`, `'BOS'`). |
| `franchID` | Franchise ID (links to `lahman_2014.teamsfranchises`); stable across relocations. |
| `divID` | Division: `'E'` (East), `'W'` (West), `'C'` (Central), NULL (pre-division era). |
| `Rank` | Final standing rank in league. |
| `G` | Games played. |
| `Ghome` | Home games. |
| `W` | Wins. |
| `L` | Losses. |
| `DivWin` | Division winner: `'Y'`, `'N'`. |
| `WCWin` | Wild card winner: `'Y'`, `'N'`. |
| `LgWin` | League champion: `'Y'`, `'N'`. |
| `WSWin` | World Series winner: `'Y'`, `'N'`. |
| `R` | Runs scored (team total). **Numerator for Pythagorean wins.** |
| `AB` | At-bats (team total). |
| `H` | Hits (team total). |
| `2B`, `3B`, `HR` | Doubles, triples, home runs (team totals). |
| `BB`, `SO`, `SB`, `CS`, `HBP`, `SF` | Walks, strikeouts, stolen bases, caught stealing, hit-by-pitch, sacrifice flies (team totals). |
| `RA` | Runs allowed (team total). **Denominator for Pythagorean wins.** |
| `ER` | Earned runs allowed. |
| `ERA` | Team ERA. |
| `CG`, `SHO`, `SV` | Complete games, shutouts, saves (team totals). |
| `IPouts` | Innings pitched (team total, in outs). |
| `HA` | Hits allowed. |
| `HRA` | Home runs allowed. |
| `BBA` | Walks allowed. |
| `SOA` | Strikeouts by pitchers. |
| `E` | Errors (team total). |
| `DP` | Double plays (team total). |
| `FP` | Fielding percentage (team). |
| `name` | Team name (e.g., `'New York Yankees'`). |
| `park` | Home stadium name. |
| `attendance` | Total home attendance. |
| `BPF` | Batting park factor (100 = neutral). |
| `PPF` | Pitching park factor (100 = neutral). |
| `teamIDBR`, `teamIDlahman45`, `teamIDretro` | Cross-reference IDs to other databases. |

---

### `lahman_2014.teamsfranchises`
**Meaning:** Franchise metadata (name, active status, historical association).  
**Synonyms:** franchise master, franchise registry.

| Column | Notes |
|---|---|
| `franchID` | Franchise ID (primary key); links to `lahman_2014.teams.franchID`. |
| `franchName` | Franchise name (e.g., `'New York Yankees'`, `'Boston Red Sox'`). |
| `active` | Active status: `'Y'` (active), `'N'` (inactive), `'NA'` (not applicable). |
| `NAassoc` | National Association team code (1871–1875 era); links to early team history. |

---

### `lahman_2014.teamshalf`
**Meaning:** Split-season team statistics (used in 1981 strike-shortened season).  
**Synonyms:** half-season stats, split-season records.

| Column | Notes |
|---|---|
| `yearID` | Season year. |
| `lgID` | League. |
| `teamID` | Team code. |
| `Half` | Half of season: `'1'` (first half), `'2'` (second half). |
| `divID` | Division. |
| `DivWin` | Division winner in half: `'Y'`, `'N'`. |
| `Rank` | Standing rank in half. |
| `G`, `W`, `L` | Games, wins, losses in half. |

---

### `lahman_2014.managers`
**Meaning:** Annual managerial records and team performance.  
**Synonyms:** manager stats, managerial records.

| Column | Notes |
|---|---|
| `managerID` | Unique manager identifier; links to `lahman_2014.players.managerID` if manager also played. |
| `yearID` | Season year. |
| `teamID` | Team code. |
| `lgID` | League. |
| `inseason` | In-season manager changes: `1` (started season), `2` (took over mid-season), etc