# Lahman Baseball Database (2014) — SQL Reference Guide

## Schema Summary

The Lahman database contains comprehensive historical baseball statistics from 1871 to 2014, including player batting/pitching/fielding records, team performance, manager records, awards, Hall of Fame voting, and salary data across all major and minor leagues.

---

## Join Paths

### Player career statistics
```sql
FROM lahman_2014.players p
JOIN lahman_2014.batting b ON p.playerID = b.playerID
JOIN lahman_2014.pitching pi ON p.playerID = pi.playerID
JOIN lahman_2014.fielding f ON p.playerID = f.playerID
```

### Player to Hall of Fame voting
```sql
FROM lahman_2014.players p
JOIN lahman_2014.halloffame h ON p.hofID = h.hofID
```

### Team season performance
```sql
FROM lahman_2014.teams t
JOIN lahman_2014.managers m ON t.yearID = m.yearID AND t.teamID = m.teamID
```

### Player awards and voting shares
```sql
FROM lahman_2014.players p
JOIN lahman_2014.awardsshareplayers asp ON p.playerID = asp.playerID
```

### Player salary history
```sql
FROM lahman_2014.players p
JOIN lahman_2014.salaries s ON p.playerID = s.playerID
```

### Player to school attendance
```sql
FROM lahman_2014.players p
JOIN lahman_2014.schoolsplayers sp ON p.playerID = sp.playerID
JOIN lahman_2014.schools sc ON sp.schoolID = sc.schoolID
```

### Postseason performance
```sql
FROM lahman_2014.battingpost bp
JOIN lahman_2014.pitchingpost pp ON bp.playerID = pp.playerID AND bp.yearID = pp.yearID
JOIN lahman_2014.fieldingpost fp ON bp.playerID = fp.playerID AND bp.yearID = fp.yearID
```

---

## Business Rules as SQL

**Batting average calculation (exclude walks from denominator)**
```sql
WHERE lahman_2014.batting.AB > 0
SELECT (H * 1.0) / AB AS batting_avg
```

**On-base percentage (includes walks, HBP, sacrifice flies)**
```sql
SELECT (H + BB + HBP) * 1.0 / (AB + BB + HBP + SF) AS obp
```

**Slugging percentage (total bases / at-bats)**
```sql
SELECT (1B + 2*2B + 3*3B + 4*HR) * 1.0 / AB AS slugging_pct
```

**Exclude players with fewer than 100 at-bats from rate statistics**
```sql
WHERE lahman_2014.batting.AB >= 100
```

**ERA calculation**
```sql
SELECT (ER * 9.0) / (IPouts / 3.0) AS era
WHERE lahman_2014.pitching.IPouts > 0
```

**WHIP (Walks + Hits per Innings Pitched)**
```sql
SELECT (BB + H) * 1.0 / (IPouts / 3.0) AS whip
WHERE lahman_2014.pitching.IPouts > 0
```

**Reliever classification (fewer than 50 innings)**
```sql
WHERE lahman_2014.pitching.IPouts < 150  -- 50 innings = 150 outs
```

**Quality start (6+ innings, ≤3 earned runs)**
```sql
WHERE lahman_2014.pitching.IPouts >= 18 AND lahman_2014.pitching.ER <= 3
```

**Fielding percentage**
```sql
SELECT (PO + A) * 1.0 / (PO + A + E) AS fielding_pct
WHERE lahman_2014.fielding.E IS NOT NULL
```

**Hall of Fame members (actual inductees, players only)**
```sql
WHERE lahman_2014.halloffame.inducted = 'Y' 
  AND lahman_2014.halloffame.category = 'Player'
```

**Hall of Fame voting percentage**
```sql
SELECT (votes * 100.0) / ballots AS voting_pct
```

**Dead-ball era (pre-1920)**
```sql
WHERE lahman_2014.batting.yearID < 1920
```

**Steroid era (1994–2004)**
```sql
WHERE lahman_2014.batting.yearID BETWEEN 1994 AND 2004
```

---

## Synonym Glossary

| Question Term | Schema Reference |
|---|---|
| career hits | `SUM(lahman_2014.batting.H)` |
| career home runs | `SUM(lahman_2014.batting.HR)` |
| career RBIs | `SUM(lahman_2014.batting.RBI)` |
| career stolen bases | `SUM(lahman_2014.batting.SB)` |
| career wins (pitcher) | `SUM(lahman_2014.pitching.W)` |
| career ERA | `(SUM(lahman_2014.pitching.ER) * 9.0) / (SUM(lahman_2014.pitching.IPouts) / 3.0)` |
| career strikeouts (pitcher) | `SUM(lahman_2014.pitching.SO)` |
| career saves | `SUM(lahman_2014.pitching.SV)` |
| All-Star appearances | `COUNT(lahman_2014.allstarfull.playerID)` |
| MVP votes | `lahman_2014.awardsshareplayers.votesFirst` (use for primary metric) |
| Hall of Fame induction year | `lahman_2014.halloffame.yearID WHERE inducted = 'Y'` |
| team wins (season) | `lahman_2014.teams.W` |
| team runs scored | `lahman_2014.teams.R` |
| team runs allowed | `lahman_2014.teams.RA` |
| playoff round | `lahman_2014.battingpost.round` or `lahman_2014.pitchingpost.round` |
| World Series | `WHERE round = 'WS'` |
| manager wins | `SUM(lahman_2014.managers.W)` |
| player salary | `lahman_2014.salaries.salary` |

---

## Table Reference

### `lahman_2014.players`
**Meaning:** Master player registry with biographical and career identifiers.

| Column | Notes |
|---|---|
| `playerID` | Unique identifier (primary key for joins) |
| `managerID` | Non-null if player also managed |
| `hofID` | Non-null if player has Hall of Fame voting record |
| `birthYear`, `birthMonth`, `birthDay` | Birth date components |
| `birthCountry`, `birthState`, `birthCity` | Birth location |
| `deathYear`, `deathMonth`, `deathDay` | Death date (null if living) |
| `nameFirst`, `nameLast` | Legal name |
| `nameGiven` | Full given name |
| `nameNick` | Nickname(s) |
| `bats` | Handedness: `L`, `R`, `B` (both) |
| `throws` | Handedness: `L`, `R` |
| `debut`, `finalGame` | Career span (date strings) |
| `college` | College attended (if any) |

---

### `lahman_2014.batting`
**Meaning:** Annual batting statistics by player, team, and stint.

| Column | Notes |
|---|---|
| `playerID`, `yearID`, `stint`, `teamID` | Composite key; `stint` disambiguates mid-season trades |
| `lgID` | League: `AA`, `AL`, `FL`, `NA`, `NL`, `PL`, `UA` |
| `G`, `G_batting` | Games played; `G_batting` is subset with plate appearances |
| `AB` | At-bats (denominator for BA, SLG) |
| `H` | Hits |
| `2B`, `3B`, `HR` | Doubles, triples, home runs |
| `RBI` | Runs batted in |
| `BB` | Walks |
| `SO` | Strikeouts |
| `SB`, `CS` | Stolen bases, caught stealing |
| `IBB` | Intentional walks |
| `HBP` | Hit by pitch |
| `SH`, `SF` | Sacrifice hits, sacrifice flies |
| `GIDP` | Grounded into double play |
| `G_old` | Legacy games column (ignore) |

**Key rule:** Exclude rows where `AB < 100` for rate statistics.

---

### `lahman_2014.pitching`
**Meaning:** Annual pitching statistics by player, team, and stint.

| Column | Notes |
|---|---|
| `playerID`, `yearID`, `stint`, `teamID` | Composite key |
| `lgID` | League: `AA`, `AL`, `FL`, `NA`, `NL`, `PL`, `UA` |
| `W`, `L` | Wins, losses |
| `G`, `GS` | Games, games started |
| `CG`, `SHO` | Complete games, shutouts |
| `SV` | Saves |
| `IPouts` | Innings pitched × 3 (convert to innings: `IPouts / 3.0`) |
| `H`, `ER`, `HR` | Hits allowed, earned runs, home runs allowed |
| `BB`, `SO` | Walks, strikeouts |
| `ERA` | Earned run average (pre-calculated; verify with rule) |
| `IBB` | Intentional walks |
| `WP`, `HBP`, `BK` | Wild pitches, hit batters, balks |
| `BFP` | Batters faced |
| `GF` | Games finished (relief appearances) |
| `R`, `SH`, `SF`, `GIDP` | Runs allowed, sacrifice hits/flies, GIDP |
| `BAOpp` | Batting average against (pre-calculated) |

**Key rule:** Classify as reliever if `IPouts < 150` (< 50 innings).

---

### `lahman_2014.fielding`
**Meaning:** Annual fielding statistics by player, position, team, and stint.

| Column | Notes |
|---|---|
| `playerID`, `yearID`, `stint`, `teamID`, `POS` | Composite key; `POS` values: `1B`, `2B`, `3B`, `C`, `CF`, `DH`, `LF`, `OF`, `P`, `RF`, `SS` |
| `lgID` | League |
| `G`, `GS` | Games, games started |
| `InnOuts` | Innings played × 3 |
| `PO`, `A`, `E` | Putouts, assists, errors |
| `DP` | Double plays |
| `PB` | Passed balls (catchers) |
| `WP` | Wild pitches (pitchers) |
| `SB`, `CS` | Stolen bases allowed, caught stealing (catchers) |
| `ZR` | Zone rating (advanced metric; sparse) |

**Key rule:** Report fielding stats per position, not aggregated. Compare within position groups only.

---

### `lahman_2014.fieldingof`
**Meaning:** Outfield position breakdown (left, center, right) for players with multiple outfield positions.

| Column | Notes |
|---|---|
| `playerID`, `yearID`, `stint` | Composite key |
| `Glf`, `Gcf`, `Grf` | Games at left field, center field, right field |

---

### `lahman_2014.allstarfull`
**Meaning:** All-Star Game appearances (one row per game per player).

| Column | Notes |
|---|---|
| `playerID`, `yearID`, `gameNum` | Composite key; `gameNum` = 0 for first game, 1 for second (pre-1962) |
| `gameID` | Unique game identifier |
| `teamID` | Team (usually `ML1` for multi-league games) |
| `lgID` | League: `AL`, `NL` |
| `GP` | Games played (usually 1) |
| `startingPos` | Starting position (null if reserve); numeric position code |

**Key rule:** All-Star appearances before 1933 (first game) are not comparable to later years.

---

### `lahman_2014.battingpost`
**Meaning:** Postseason batting statistics by player, round, and team.

| Column | Notes |
|---|---|
| `playerID`, `yearID`, `round`, `teamID` | Composite key |
| `round` | Playoff round: `WS`, `ALCS`, `NLCS`, `ALDS1`, `ALDS2`, `NLDS1`, `NLDS2`, `ALWC`, `NLWC`, `AEDIV`, `AWDIV`, `NEDIV`, `NWDIV`, `CS` |
| `lgID` | League: `AL`, `NL`, `AA` |
| `G`, `AB`, `H`, `2B`, `3B`, `HR`, `RBI`, `BB`, `SO`, `SB`, `CS`, `IBB`, `HBP`, `SH`, `SF`, `GIDP` | Same semantics as `batting` table |

---

### `lahman_2014.pitchingpost`
**Meaning:** Postseason pitching statistics by player, round, and team.

| Column | Notes |
|---|---|
| `playerID`, `yearID`, `round`, `teamID` | Composite key |
| `round` | Playoff round (see `battingpost`) |
| `lgID` | League: `AL`, `NL`, `AA` |
| `W`, `L`, `G`, `GS`, `CG`, `SHO`, `SV`, `IPouts`, `H`, `ER`, `HR`, `BB`, `SO`, `ERA`, `IBB`, `WP`, `HBP`, `BK`, `BFP`, `GF`, `R`, `SH`, `SF`, `GIDP` | Same semantics as `pitching` table |

---

### `lahman_2014.fieldingpost`
**Meaning:** Postseason fielding statistics by player, position, round, and team.

| Column | Notes |
|---|---|
| `playerID`, `yearID`, `round`, `teamID`, `POS` | Composite key |
| `lgID` | League: `AL`, `NL` |
| `G`, `GS`, `InnOuts`, `PO`, `A`, `E`, `DP`, `TP`, `PB`, `SB`, `CS` | Same semantics as `fielding` table; `TP` = triple plays |

---

### `lahman_2014.halloffame`
**Meaning:** Hall of Fame voting records (all nominations and inductions, not just successful inductees).

| Column | Notes |
|---|---|
| `hofID` | Hall of Fame identifier (primary key for joins) |
| `yearID` | Voting year |
| `votedBy` | Voting body: `BBWAA`, `Centennial`, `Final Ballot`, `Negro League`, `Nominating Vote`, `Old Timers`, `Run Off`, `Special Election`, `Veterans` |
| `ballots` | Total ballots cast |
| `needed` | Votes needed for induction (typically 75% of ballots) |
| `votes` | Votes received |
| `inducted` | Induction status: `Y`, `N` |
| `category` | Voter category: `Player`, `Manager`, `Pioneer/Executive`, `Umpire` |

**Critical rule:** Filter for actual Hall of Famers with `WHERE inducted = 'Y' AND category = 'Player'`. This table contains all voting records; most rows have `inducted = 'N'`.

---

### `lahman_2014.awardsshareplayers`
**Meaning:** Award voting shares for players (MVP, Cy Young, Rookie of the Year).

| Column | Notes |
|---|---|
| `playerID`, `awardID`, `yearID`, `lgID` | Composite key |
| `awardID` | Award type: `MVP`, `Cy Young`, `Rookie of the Year` |
| `lgID` | League: `AL`, `NL`, `ML` |
| `pointsWon` | Points awarded to this player |
| `pointsMax` | Maximum possible points |
| `votesFirst` | **Primary metric:** First-place votes received (use this for MVP comparisons, not total points) |

---

### `lahman_2014.awardsplayers`
**Meaning:** Historical award records (Triple Crown, Pitching Triple Crown, etc.).

| Column | Notes |
|---|---|
| `playerID`, `awardID`, `yearID`, `lgID` | Composite key |
| `awardID` | Award type (e.g., `Triple Crown`, `Pitching Triple Crown`) |
| `lgID` | League: `AA`, `AL`, `ML`, `NL` |
| `tie` | Tie indicator: `Y` or null |
| `notes` | Additional context |

---

### `lahman_2014.managers`
**Meaning:** Annual managerial records by manager, team, and year.

| Column | Notes |
|---|---|
| `managerID`, `yearID`, `teamID` | Composite key |
| `lgID` | League: `AA`, `AL`, `FL`, `NA`, `NL`, `PL`, `UA` |
| `inseason` | Managerial change sequence (1 = start of season, 2+ = mid-season replacement) |
| `G`, `W`, `L` | Games, wins, losses |
| `rank` | Final standing in league |
| `plyrMgr` | Player-manager flag: `Y`, `N` |

---

### `lahman_2014.managershalf`
**Meaning:** Split-season managerial records (1981 strike season and historical split seasons).

| Column | Notes |
|---|---|
| `managerID`, `yearID`, `teamID`, `half` | Composite key; `half` = 1 or 2 |
| `lgID` | League: `AL`, `NL` |
| `inseason` | Managerial change sequence |
| `G`, `W`, `L`, `rank` | Games, wins, losses, standing |

---

### `lahman_2014.awardsmanagers`
**Meaning:** Manager award records (Manager of the Year).

| Column | Notes |
|---|---|
| `managerID`, `awardID`, `yearID` | Composite key |
| `awardID` | Award type: `TSN Manager of the Year`, `BBWAA Manager of the year` |
| `lgID` | League: `AL`, `ML`, `NL` |
| `tie` | Tie indicator: `Y` or null |
| `notes` | Additional context |

---

### `lahman_2014.awardssharemanagers`
**Meaning:** Manager award voting shares.

| Column | Notes |
|---|---|
| `awardID`, `yearID`, `lgID`, `managerID` | Composite key |
| `awardID` | Award type: `Mgr of the Year`, `Mgr of the year` (note case variation) |
| `pointsWon`, `pointsMax`, `votesFirst` | Voting metrics (same semantics as player awards) |

---

### `lahman_2014.teams`
**Meaning:** Annual team-level statistics and standings.

| Column | Notes |
|---|---|
| `yearID`, `lgID`, `teamID` | Composite key |
| `franchID` | Franchise identifier (stable across relocations) |
| `divID` | Division: `E`, `W`, `C` (null for pre-division era) |
| `Rank` | Final standing in league |
| `G`, `Ghome` | Games played, home games |
| `W`, `L` | Wins, losses |
| `DivWin`, `WCWin`, `LgWin`, `WSWin` | Playoff qualification flags: `Y`, `N` |
| `R`, `RA` | Runs scored, runs allowed (for Pythagorean calculation) |
| `AB`, `H`, `2B`, `3B`, `HR`, `BB`, `SO`, `SB`, `CS`, `HBP`, `SF` | Team batting aggregates |
| `ER`, `ERA`, `CG`, `SHO`, `SV`, `IPouts` | Team pitching aggregates |
| `HA`, `HRA`, `BBA`, `SOA` | Opponent batting aggregates |
| `E`, `DP`, `FP` | Errors, double plays, fielding percentage |
| `name`, `park` | Team name, home park |
| `attendance` | Season attendance |
| `BPF`, `PPF` | Park factors (batting, pitching) |
| `teamIDBR`, `teamIDlahman45`, `teamIDretro` | Legacy identifiers |

---

### `lahman_2014.teamsfranchises`
**Meaning:** Franchise master list with historical associations.

| Column | Notes |
|---|---|
| `franchID` | Franchise identifier (primary key) |
| `franchName` | Franchise name |
| `active` | Status: `Y`, `N`, `NA` |
| `NAassoc` | National Association team code (if applicable) |

---

### `lahman_2014.teamshalf`
**Meaning:** Split-season team records (1981 strike season and historical split seasons).

| Column | Notes |
|---|---|
| `yearID`, `lgID`, `teamID`, `Half` | Composite key; `Half` = `1` or `2` |
| `divID` | Division: `E`, `W` |
| `DivWin` | Division winner flag: `N` (or null if winner) |
| `Rank`, `G`, `W`, `L` | Standing, games, wins, losses |

---

### `lahman_2014.seriespost`
**Meaning:** Postseason series results (winner and loser by round).

| Column | Notes |
|---|---|
| `yearID`, `round` | Composite key |
| `teamIDwinner`, `lgIDwinner` | Winning team and league |
| `teamIDloser`, `lgIDloser` | Losing team and league |
| `wins`, `losses`, `ties` | Series result (e.g., 4–3 for World Series) |

---

### `lahman_2014.appearances`
**Meaning:** Annual position-specific game counts by player and team.

| Column | Notes |
|---|---|
| `playerID`, `yearID`, `teamID` | Composite key |
| `lgID` | League |
| `G_all` | Total games |
| `G_batting` | Games with plate appearance |
| `G_defense` | Games on defense |
| `G_p`, `G_c`, `G_1b`, `G_2b`, `G_3b`, `G_ss`, `G_lf`, `G_cf`, `G_rf`, `G_of`, `G_dh`, `G_ph`, `G_pr` | Games at each position (pitcher, catcher, 1B, 2B, 3B, SS, LF, CF, RF, OF, DH, pinch-hitter, pinch-runner) |

---

### `lahman_2014.salaries`
**Meaning:** Annual player salaries by team and year.

| Column | Notes |
|---|---|
| `playerID`, `yearID`, `teamID` | Composite key |
| `lgID` | League: `AL`, `NL` |
| `salary` | Annual salary in dollars |

**Coverage:** 1985–2014 only.

---

### `lahman_2014.schools`
**Meaning:** College/university master list.

| Column | Notes |
|---|---|
| `schoolID` | School identifier (primary key) |
| `schoolName` | Institution name |
| `schoolCity`, `schoolState` | Location |
| `schoolNick` | Nickname/mascot |

---

### `lahman_2014.schoolsplayers`
**Meaning:** Player-to-school attendance mapping.

| Column | Notes |
|---|---|
| `playerID`, `schoolID` | Composite key |
| `yearMin`, `yearMax` | Attendance span (academic years) |

---

### `lahman_2014.els_teamnames`
**Meaning:** Historical team name and park mappings (legacy table).

| Column | Notes |
|---|---|
| `id` | Row identifier |
| `lgid`, `teamid`, `franchid` | League, team, franchise identifiers |
| `name`, `park` | Team name and home park |

---

End of reference guide.