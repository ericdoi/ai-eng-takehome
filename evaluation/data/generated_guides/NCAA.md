# NCAA Schema Reference Guide

## Schema Summary
This schema contains NCAA Division I men's basketball regular season and tournament game results, team rosters, tournament seeding/bracket information, and prediction targets.

---

## Join Paths

**Game results to team names:**
```sql
FROM NCAA.regular_season_compact_results r
JOIN NCAA.teams t_w ON r.wteam = t_w.team_id
JOIN NCAA.teams t_l ON r.lteam = t_l.team_id
```

**Tournament results to seeds:**
```sql
FROM NCAA.tourney_compact_results tcr
JOIN NCAA.tourney_seeds ts_w ON tcr.season = ts_w.season AND tcr.wteam = ts_w.team
JOIN NCAA.tourney_seeds ts_l ON tcr.season = ts_l.season AND tcr.lteam = ts_l.team
```

**Tournament bracket structure:**
```sql
FROM NCAA.tourney_slots slot
JOIN NCAA.tourney_seeds ts_strong ON slot.season = ts_strong.season AND slot.strongseed = ts_strong.seed
JOIN NCAA.tourney_seeds ts_weak ON slot.season = ts_weak.season AND slot.weakseed = ts_weak.seed
```

**Prediction targets to actual outcomes:**
```sql
FROM NCAA.target tgt
JOIN NCAA.tourney_compact_results tcr ON tgt.season = tcr.season 
  AND ((tgt.team_id1 = tcr.wteam AND tgt.team_id2 = tcr.lteam) 
       OR (tgt.team_id1 = tcr.lteam AND tgt.team_id2 = tcr.wteam))
```

---

## Table Reference

### `NCAA.regular_season_compact_results`
Regular season game outcomes (compact format).

| Column | Notes |
|--------|-------|
| `season` | Tournament year (e.g., 1985 = 1985 NCAA tournament) |
| `daynum` | Day number within season (1–134 typical) |
| `wteam` | Winning team ID; join to `NCAA.teams.team_id` |
| `wscore` | Winning team score |
| `lteam` | Losing team ID; join to `NCAA.teams.team_id` |
| `lscore` | Losing team score |
| `wloc` | Winner location: `H` (home), `A` (away), `N` (neutral) |
| `numot` | Number of overtimes (0 = regulation) |

---

### `NCAA.regular_season_detailed_results`
Regular season game outcomes with box-score statistics.

| Column | Notes |
|--------|-------|
| `season`, `daynum`, `wteam`, `wscore`, `lteam`, `lscore`, `wloc`, `numot` | Same as compact results |
| `wfgm`, `wfga` | Winning team field goals made/attempted |
| `wfgm3`, `wfga3` | Winning team 3-pointers made/attempted |
| `wftm`, `wfta` | Winning team free throws made/attempted |
| `wor`, `wdr` | Winning team offensive/defensive rebounds |
| `wast` | Winning team assists |
| `wto` | Winning team turnovers |
| `wstl` | Winning team steals |
| `wblk` | Winning team blocks |
| `wpf` | Winning team personal fouls |
| `lfgm`–`lpf` | Losing team equivalents (prefix `l` instead of `w`) |

---

### `NCAA.seasons`
Tournament season metadata and regional assignments.

| Column | Notes |
|--------|-------|
| `season` | Tournament year |
| `dayzero` | Season start date (typically late October) |
| `regionW`, `regionX`, `regionY`, `regionZ` | Four tournament regions; values: `Albuquerque`, `Atlanta`, `Austin`, `Chicago`, `East`, `EastRutherford`, `Midwest`, `Minneapolis`, `Oakland`, `Phoenix`, `South`, `Southeast`, `Southwest`, `StLouis`, `Syracuse`, `WashingtonDC`, `West` |

---

### `NCAA.teams`
Team master list.

| Column | Notes |
|--------|-------|
| `team_id` | Unique team identifier (e.g., 1104 = Alabama) |
| `team_name` | Team name (abbreviated, e.g., "Alabama") |

---

### `NCAA.tourney_compact_results`
Tournament game outcomes (compact format).

| Column | Notes |
|--------|-------|
| `season`, `daynum`, `wteam`, `wscore`, `lteam`, `lscore`, `numot` | Same semantics as regular season |
| `wloc` | Always `N` (neutral site) for tournament games |

---

### `NCAA.tourney_detailed_results`
Tournament game outcomes with box-score statistics.

| Column | Notes |
|--------|-------|
| All columns | Same as `NCAA.tourney_compact_results` + box-score columns (same naming as `NCAA.regular_season_detailed_results`) |

---

### `NCAA.tourney_seeds`
Tournament seeding assignments.

| Column | Notes |
|--------|-------|
| `season` | Tournament year |
| `seed` | Seed code: region letter (`W`, `X`, `Y`, `Z`) + seed number (01–16); e.g., `W01`, `Z15` |
| `team` | Team ID; join to `NCAA.teams.team_id` |

---

### `NCAA.tourney_slots`
Tournament bracket structure (matchup slots).

| Column | Notes |
|--------|-------|
| `season` | Tournament year |
| `slot` | Slot identifier (e.g., `R1W1` = Round 1, Region W, Slot 1) |
| `strongseed` | Higher seed in matchup (seed code from `NCAA.tourney_seeds.seed`) |
| `weakseed` | Lower seed in matchup (seed code from `NCAA.tourney_seeds.seed`) |

---

### `NCAA.target`
Prediction targets for tournament matchups.

| Column | Notes |
|--------|-------|
| `id` | Matchup identifier (format: `YYYY_TEAMID1_TEAMID2`) |
| `season` | Tournament year |
| `team_id1`, `team_id2` | Two teams in matchup; join to `NCAA.teams.team_id` |
| `pred` | Model prediction (probability team_id1 wins, 0–1) |
| `team_id1_wins` | Actual outcome: 1 if team_id1 won, 0 if team_id2 won |
| `team_id2_wins` | Actual outcome: 1 if team_id2 won, 0 if team_id1 won |