# Hockey Schema Reference Guide

## Schema Summary
This schema contains comprehensive historical ice hockey statistics spanning multiple leagues (NHL, WHA, NHA, PCHA, WCHL), including player scoring, goaltending, coaching records, team performance, playoff results, and Hall of Fame inductions from 1909 to present.

---

## Join Paths

**Player career stats (regular season + playoffs):**
```sql
FROM Hockey.Master m
JOIN Hockey.Scoring s ON m.playerID = s.playerID
LEFT JOIN Hockey.Goalies g ON m.playerID = g.playerID AND s.year = g.year
```

**Player awards and Hall of Fame:**
```sql
FROM Hockey.Master m
LEFT JOIN Hockey.AwardsPlayers ap ON m.playerID = ap.playerID
LEFT JOIN Hockey.HOF h ON m.hofID = h.hofID
```

**Coach career history:**
```sql
FROM Hockey.Master m
JOIN Hockey.Coaches c ON m.coachID = c.coachID
```

**Team season performance:**
```sql
FROM Hockey.Teams t
LEFT JOIN Hockey.TeamsPost tp ON t.year = tp.year AND t.tmID = tp.tmID AND t.lgID = tp.lgID
LEFT JOIN Hockey.TeamSplits ts ON t.year = ts.year AND t.tmID = ts.tmID AND t.lgID = ts.lgID
```

**Playoff series results:**
```sql
FROM Hockey.SeriesPost sp
JOIN Hockey.Teams t_winner ON sp.year = t_winner.year AND sp.tmIDWinner = t_winner.tmID AND sp.lgIDWinner = t_winner.lgID
JOIN Hockey.Teams t_loser ON sp.year = t_loser.year AND sp.tmIDLoser = t_loser.tmID AND sp.lgIDLoser = t_loser.lgID
```

**Goalie shutout records:**
```sql
FROM Hockey.Goalies g
LEFT JOIN Hockey.CombinedShutouts cs ON g.year = cs.year AND g.playerID IN (cs.IDgoalie1, cs.IDgoalie2)
```

---

## Business Rules as SQL

**Exclude unreliable plus/minus data:**
```sql
WHERE s.year >= 1968 OR s.`+/-` IS NULL
```

**Separate playoff from regular season (never combine):**
```sql
-- Regular season: use columns G, A, Pts, PIM, etc.
-- Playoff: use columns PostG, PostA, PostPts, PostPIM, etc. (report separately)
```

**Exclude shootout goals from official totals:**
```sql
-- Do NOT include Hockey.ScoringShootout.G in career goal counts
-- Use only Hockey.Scoring.G for official statistics
```

**Identify backup goalies (exclude from starter rankings):**
```sql
WHERE CAST(g.GP AS UNSIGNED) < 20
```

**Calculate true save percentage (exclude empty-net goals):**
```sql
WHERE CAST(g.ENG AS UNSIGNED) = 0
-- True SV% = (SA - GA) / (SA - ENG)
```

**Exclude combined shutouts from individual totals:**
```sql
WHERE g.playerID NOT IN (
  SELECT IDgoalie1 FROM Hockey.CombinedShutouts WHERE IDgoalie1 IS NOT NULL
  UNION
  SELECT IDgoalie2 FROM Hockey.CombinedShutouts WHERE IDgoalie2 IS NOT NULL
)
```

**Exclude WHA statistics from NHL career totals:**
```sql
WHERE s.lgID != 'WHA'
```

**Flag teams with scheduling anomalies:**
```sql
WHERE CAST(t.G AS UNSIGNED) < 41 AND t.lgID = 'NHL'
```

**Exclude shortened-season award winners:**
```sql
-- Filter out awards from years where league-wide GP < 60
-- Requires cross-reference with Hockey.Scoring to determine season length
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| career goals | `SUM(Hockey.Scoring.G)` where `lgID != 'WHA'` |
| career assists | `SUM(Hockey.Scoring.A)` where `lgID != 'WHA'` |
| career points | `SUM(Hockey.Scoring.Pts)` where `lgID != 'WHA'` |
| playoff goals | `SUM(Hockey.Scoring.PostG)` (report separately) |
| playoff points | `SUM(Hockey.Scoring.PostPts)` (report separately) |
| shutouts (individual) | `SUM(Hockey.Goalies.SHO)` excluding `Hockey.CombinedShutouts` |
| wins (goalie) | `SUM(Hockey.Goalies.W)` |
| goals against average | `SUM(Hockey.Goalies.GA) / (SUM(Hockey.Goalies.Min) / 60)` |
| save percentage | `(SUM(SA) - SUM(GA)) / SUM(SA)` where `ENG = 0` |
| plus/minus | `Hockey.Scoring.+/-` (valid only year ≥ 1968) |
| power-play goals | `SUM(Hockey.Scoring.PPG)` |
| short-handed goals | `SUM(Hockey.Scoring.SHG)` |
| game-winning goals | `SUM(Hockey.Scoring.GWG)` |
| penalty minutes | `SUM(Hockey.Scoring.PIM)` |
| Hall of Fame | `Hockey.HOF.year`, `Hockey.HOF.category` |
| award winner | `Hockey.AwardsPlayers.award`, `Hockey.AwardsCoaches.award` |
| coach wins | `SUM(Hockey.Coaches.w)` |
| team goals for | `Hockey.Teams.GF` |
| team goals against | `Hockey.Teams.GA` |
| playoff appearance | `Hockey.Teams.playoff` (non-null value) |

---

## Table Reference

### `Hockey.Master`
**Meaning:** Player and coach biographical registry.  
**Synonyms:** player master, coach master, personnel registry.

| Column | Notes |
|--------|-------|
| `playerID` | Unique player identifier; links to `Scoring`, `Goalies`, `AwardsPlayers` |
| `coachID` | Unique coach identifier; links to `Coaches`, `AwardsCoaches` |
| `hofID` | Hall of Fame identifier; links to `HOF` |
| `pos` | Position: `C`, `D`, `F`, `G`, `L`, `R`, `W`, or combinations (e.g., `C/D`, `R/L`) |
| `shootCatch` | Handedness: `L` (left), `R` (right), `B` (both) |
| `birthYear`, `birthMon`, `birthDay` | Birth date components; may be partial |
| `birthCountry`, `birthState`, `birthCity` | Birth location |
| `deathYear`, `deathMon`, `deathDay` | Death date components; NULL if living |
| `firstNHL`, `lastNHL` | First and last NHL season years |
| `firstWHA`, `lastWHA` | First and last WHA season years (1972–1978 range) |
| `height`, `weight` | Physical attributes (height in inches, weight in pounds) |

---

### `Hockey.Scoring`
**Meaning:** Regular season player scoring statistics.  
**Synonyms:** player stats, regular season stats, scoring records.

| Column | Notes |
|--------|-------|
| `playerID` | Links to `Master` |
| `year` | Season year |
| `stint` | Stint number within season (player may change teams mid-season) |
| `tmID` | Team identifier; links to `Teams` |
| `lgID` | League: `NHL`, `WHA`, `NHA`, `PCHA`, `WCHL`. **Exclude `WHA` from NHL career totals.** |
| `pos` | Position played |
| `GP` | Games played |
| `G` | Goals (excludes shootout goals) |
| `A` | Assists |
| `Pts` | Points (G + A) |
| `PIM` | Penalties in minutes |
| `+/-` | Plus/minus; **unreliable before 1968** |
| `PPG`, `PPA` | Power-play goals and assists |
| `SHG`, `SHA` | Short-handed goals and assists |
| `GWG` | Game-winning goals |
| `GTG` | Golden-time goals (overtime winners) |
| `SOG` | Shots on goal |
| `PostGP`, `PostG`, `PostA`, `PostPts`, `PostPIM`, `Post+/-`, `PostPPG`, `PostPPA`, `PostSHG`, `PostSHA`, `PostGWG`, `PostSOG` | **Playoff equivalents; report separately from regular season** |

---

### `Hockey.Goalies`
**Meaning:** Regular season goaltender statistics.  
**Synonyms:** goalie stats, goaltending records.

| Column | Notes |
|--------|-------|
| `playerID` | Links to `Master` |
| `year` | Season year |
| `stint` | Stint number within season |
| `tmID` | Team identifier |
| `lgID` | League |
| `GP` | Games played; **exclude from starter rankings if < 20** |
| `Min` | Minutes played |
| `W`, `L`, `T/OL` | Wins, losses, ties/overtime losses |
| `ENG` | Empty-net goals allowed; **exclude from save percentage calculation** |
| `SHO` | Shutouts; **exclude if goalie appears in `CombinedShutouts`** |
| `GA` | Goals against |
| `SA` | Shots against |
| `PostGP`, `PostMin`, `PostW`, `PostL`, `PostT`, `PostENG`, `PostSHO`, `PostGA`, `PostSA` | **Playoff equivalents; report separately** |

---

### `Hockey.CombinedShutouts`
**Meaning:** Shutouts achieved by two goalies in same game.  
**Synonyms:** shared shutouts, combined shutout records.

| Column | Notes |
|--------|-------|
| `year`, `month`, `date` | Game date |
| `tmID`, `oppID` | Team and opponent identifiers |
| `R/P` | `R` (regular season), `P` (playoff) |
| `IDgoalie1`, `IDgoalie2` | Goalie identifiers; **neither should receive individual shutout credit** |

---

### `Hockey.GoaliesShootout`
**Meaning:** Shootout-specific goaltender performance.  
**Synonyms:** shootout stats, shootout records.

| Column | Notes |
|--------|-------|
| `playerID` | Links to `Master` |
| `year` | Season year |
| `stint` | Stint number |
| `tmID` | Team identifier |
| `W`, `L` | Shootout wins and losses |
| `SA` | Shootout attempts against |
| `GA` | Shootout goals allowed |

---

### `Hockey.Scoring` (Shootout variant: `Hockey.ScoringShootout`)
**Meaning:** Shootout-specific player scoring.  
**Synonyms:** shootout goals, shootout stats.

| Column | Notes |
|--------|-------|
| `playerID` | Links to `Master` |
| `year` | Season year |
| `stint` | Stint number |
| `tmID` | Team identifier |
| `S` | Shootout attempts |
| `G` | Shootout goals; **do NOT include in official career goal totals** |
| `GDG` | Game-deciding goals (shootout winners) |

---

### `Hockey.Teams`
**Meaning:** Regular season team statistics and standings.  
**Synonyms:** team stats, team records, standings.

| Column | Notes |
|--------|-------|
| `year` | Season year |
| `lgID` | League |
| `tmID` | Team identifier |
| `franchID` | Franchise identifier (for relocations) |
| `confID` | Conference: `CC` (Campbell), `EC` (Eastern), `WA` (Wales), `WC` (Western) |
| `divID` | Division code (e.g., `AD` Adams, `PC` Pacific) |
| `rank` | Standings rank within league |
| `playoff` | Non-null if team made playoffs |
| `G` | Games played; **flag if < 41 for home games** |
| `W`, `L`, `T`, `OTL` | Wins, losses, ties, overtime losses |
| `Pts` | Points (standings) |
| `SoW`, `SoL` | Shootout wins and losses |
| `GF`, `GA` | Goals for and against |
| `PIM`, `BenchMinor` | Team penalties and bench minors |
| `PPG`, `PPC` | Power-play goals and chances |
| `SHA`, `PKG`, `PKC` | Short-handed against, penalty-kill goals, penalty-kill chances |
| `SHF` | Short-handed for |

---

### `Hockey.TeamsPost`
**Meaning:** Playoff team statistics.  
**Synonyms:** playoff team stats, postseason records.

| Column | Notes |
|--------|-------|
| `year`, `lgID`, `tmID` | Season, league, team |
| `G`, `W`, `L`, `T` | Playoff games, wins, losses, ties |
| `GF`, `GA` | Playoff goals for and against |
| `PIM`, `BenchMinor`, `PPG`, `PPC`, `SHA`, `PKG`, `PKC`, `SHF` | Playoff discipline and special-teams stats |

---

### `Hockey.TeamSplits`
**Meaning:** Team performance split by home/road and by month.  
**Synonyms:** team splits, monthly performance, home/road splits.

| Column | Notes |
|--------|-------|
| `year`, `lgID`, `tmID` | Season, league, team |
| `hW`, `hL`, `hT`, `hOTL` | Home wins, losses, ties, OTL |
| `rW`, `rL`, `rT`, `rOTL` | Road wins, losses, ties, OTL |
| `SepW`, `SepL`, `SepT`, `SepOL` | September performance |
| `OctW`, `OctL`, `OctT`, `OctOL` | October performance |
| `NovW`, `NovL`, `NovT`, `NovOL` | November performance |
| `DecW`, `DecL`, `DecT`, `DecOL` | December performance |
| `JanW`, `JanL`, `JanT`, `JanOL` | January performance |
| `FebW`, `FebL`, `FebT`, `FebOL` | February performance |
| `MarW`, `MarL`, `MarT`, `MarOL` | March performance |
| `AprW`, `AprL`, `AprT`, `AprOL` | April performance |

---

### `Hockey.TeamVsTeam`
**Meaning:** Head-to-head team records.  
**Synonyms:** team matchups, head-to-head records.

| Column | Notes |
|--------|-------|
| `year`, `lgID`, `tmID`, `oppID` | Season, league, team, opponent |
| `W`, `L`, `T`, `OTL` | Record in matchup |

---

### `Hockey.SeriesPost`
**Meaning:** Playoff series results.  
**Synonyms:** playoff series, postseason matchups.

| Column | Notes |
|--------|-------|
| `year` | Season year |
| `round` | Round code: `Pre` (preliminary), `QF` (quarterfinal), `CF` (conference final), `SCF` (Stanley Cup final), etc. |
| `series` | Series identifier (A–O) |
| `tmIDWinner`, `lgIDWinner` | Winning team and league |
| `tmIDLoser`, `lgIDLoser` | Losing team and league |
| `W`, `L`, `T` | Series result (wins, losses, ties) |
| `GoalsWinner`, `GoalsLoser` | Total goals in series |
| `note` | Special notation: `EX` (exhibition), `TG` (two-game), `ND` (no decision), `DEF` (default) |

---

### `Hockey.Coaches`
**Meaning:** Coach season-by-season records.  
**Synonyms:** coaching records, coach stats.

| Column | Notes |
|--------|-------|
| `coachID` | Links to `Master` |
| `year` | Season year |
| `tmID` | Team identifier |
| `lgID` | League |
| `stint` | Stint number within season |
| `notes` | Special notation: `interim`, `co-coach with [name]` |
| `g`, `w`, `l`, `t` | Regular season games, wins, losses, ties |
| `postg`, `postw`, `postl`, `postt` | Playoff games, wins, losses, ties |

---

### `Hockey.AwardsPlayers`
**Meaning:** Individual player awards and honors.  
**Synonyms:** player awards, honors, accolades.

| Column | Notes |
|--------|-------|
| `playerID` | Links to `Master` |
| `award` | Award name (e.g., `Hart`, `Norris`, `Vezina`, `Calder`, `First Team All-Star`, `Second Team All-Star`) |
| `year` | Award year |
| `lgID` | League |
| `note` | Award context: `MVP`, `Best Defenceman`, `Best Goaltender`, `Rookie`, `Scoring`, `Most Gentlemanly`, `shared`, `tie` |
| `pos` | Position of awardee |

---

### `Hockey.AwardsCoaches`
**Meaning:** Coach awards.  
**Synonyms:** coach awards, coaching honors.

| Column | Notes |
|--------|-------|
| `coachID` | Links to `Master` |
| `award` | Award: `Jack Adams`, `First Team All-Star`, `Second Team All-Star`, `Baldwin`, `Schmertz` |
| `year` | Award year |
| `lgID` | League |
| `note` | Additional context |

---

### `Hockey.AwardsMisc`
**Meaning:** Miscellaneous awards (e.g., Patrick Trophy).  
**Synonyms:** special awards, honorary awards.

| Column | Notes |
|--------|-------|
| `name` | Recipient name (may be team or individual) |
| `ID` | Recipient identifier (may be NULL for teams) |
| `award` | Award type: `Patrick` |
| `year` | Award year |
| `lgID` | League |
| `note` | Special notation: `posthumous` |

---

### `Hockey.HOF`
**Meaning:** Hall of Fame inductions.  
**Synonyms:** Hall of Fame, HOF, inductions.

| Column | Notes |
|--------|-------|
| `year` | Induction year |
| `hofID` | Hall of Fame identifier; links to `Master.hofID` |
| `name` | Inductee name |
| `category` | `Player`, `Builder`, `Referee/Linesman` |

---

### `Hockey.ScoringSC` (Stanley Cup era)
**Meaning:** Scoring statistics from Stanley Cup era (pre-NHL consolidation).  
**Synonyms:** Stanley Cup stats, early era scoring.

| Column | Notes |
|--------|-------|
| `playerID` | Links to `Master` |
| `year` | Season year |
| `tmID` | Team (Stanley Cup era codes: `MTL`, `OTS`, `VML`, etc.) |
| `lgID` | League: `NHA`, `NHL`, `PCHA`, `WCHL` |
| `pos` | Position |
| `GP`, `G`, `A`, `Pts`, `PIM` | Games, goals, assists, points, penalties |

---

### `Hockey.GoaliesSC` (Stanley Cup era)
**Meaning:** Goaltending statistics from Stanley Cup era.  
**Synonyms:** Stanley Cup goalie stats, early era goaltending.

| Column | Notes |
|--------|-------|
| `playerID` | Links to `Master` |
| `year` | Season year |
| `tmID` | Team (Stanley Cup era codes) |
| `lgID` | League |
| `GP`, `Min`, `W`, `L`, `T`, `SHO`, `GA` | Games, minutes, wins, losses, ties, shutouts, goals against |

---

### `Hockey.TeamsSC` (Stanley Cup era)
**Meaning:** Team statistics from Stanley Cup era.  
**Synonyms:** Stanley Cup team stats, early era team records.

| Column | Notes |
|--------|-------|
| `year`, `lgID`, `tmID` | Season, league, team |
| `G`, `W`, `L`, `T` | Games, wins, losses, ties |
| `GF`, `GA` | Goals for and against |
| `PIM` | Team penalties |

---

### `Hockey.TeamsHalf`
**Meaning:** Team performance split by season half (early era only).  
**Synonyms:** half-season splits, season halves.

| Column | Notes |
|--------|-------|
| `year`, `lgID`, `tmID` | Season, league, team |
| `half` | Half number (1 or 2) |
| `rank` | Rank within half |
| `G`, `W`, `L`, `T` | Games, wins, losses, ties |
| `GF`, `GA` | Goals for and against |

---

### `Hockey.ScoringSup`
**Meaning:** Supplementary scoring data (power-play and short-handed assists).  
**Synonyms:** supplementary stats, special teams assists.

| Column | Notes |
|--------|-------|
| `playerID` | Links to `Master` |
| `year` | Season year |
| `PPA` | Power-play assists (supplementary) |
| `SHA` | Short-handed assists (supplementary) |

---

### `Hockey.abbrev`
**Meaning:** Abbreviation reference table.  
**Synonyms:** code reference, abbreviation lookup.

| Column | Notes |
|--------|-------|
| `Type` | Category: `Conference`, `Division`, `Playoffs`, `Round` |
| `Code` | Abbreviation (e.g., `EC`, `AD`, `QF`) |
| `Fullname` | Full name (e.g., `Eastern Conference`, `Adams Division`, `Quarterfinal`) |