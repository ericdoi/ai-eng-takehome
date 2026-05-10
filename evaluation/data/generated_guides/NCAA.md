# NCAA Basketball Schema Reference Guide

## Schema Summary
This schema contains NCAA Division I men's basketball regular season and tournament game results, team information, tournament seeding/bracket structure, and prediction targets spanning multiple seasons from 1985 onward.

---

## Table Reference

### NCAA.regular_season_compact_results
**Meaning:** Regular season game outcomes with basic scoring information.
**Synonyms:** Regular season games, regular season results

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `season` | BIGINT | NCAA tournament season year | year, tournament_year |
| `daynum` | BIGINT | Day number within the season (1-based from dayzero) | day, game_day |
| `wteam` | BIGINT | Winning team ID | winner_id, winning_team_id |
| `wscore` | BIGINT | Winning team's final score | winner_score, winning_points |
| `lteam` | BIGINT | Losing team ID | loser_id, losing_team_id |
| `lscore` | BIGINT | Losing team's final score | loser_score, losing_points |
| `wloc` | VARCHAR | Winning team's location: `H` (home), `A` (away), `N` (neutral) | location, game_location |
| `numot` | BIGINT | Number of overtime periods (0 if regulation) | overtimes, ot_periods |

---

### NCAA.regular_season_detailed_results
**Meaning:** Regular season game outcomes with detailed box score statistics for both teams.
**Synonyms:** Regular season detailed stats, regular season box scores

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `season` | BIGINT | NCAA tournament season year | year, tournament_year |
| `daynum` | BIGINT | Day number within the season | day, game_day |
| `wteam` | BIGINT | Winning team ID | winner_id |
| `wscore` | BIGINT | Winning team's final score | winner_score |
| `lteam` | BIGINT | Losing team ID | loser_id |
| `lscore` | BIGINT | Losing team's final score | loser_score |
| `wloc` | VARCHAR | Winning team's location: `H`, `A`, `N` | location |
| `numot` | BIGINT | Number of overtime periods | overtimes |
| `wfgm` | BIGINT | Winning team field goals made | w_fg_made |
| `wfga` | BIGINT | Winning team field goals attempted | w_fg_attempted |
| `wfgm3` | BIGINT | Winning team three-pointers made | w_3p_made |
| `wfga3` | BIGINT | Winning team three-pointers attempted | w_3p_attempted |
| `wftm` | BIGINT | Winning team free throws made | w_ft_made |
| `wfta` | BIGINT | Winning team free throws attempted | w_ft_attempted |
| `wor` | BIGINT | Winning team offensive rebounds | w_off_reb |
| `wdr` | BIGINT | Winning team defensive rebounds | w_def_reb |
| `wast` | BIGINT | Winning team assists | w_assists |
| `wto` | BIGINT | Winning team turnovers | w_turnovers |
| `wstl` | BIGINT | Winning team steals | w_steals |
| `wblk` | BIGINT | Winning team blocks | w_blocks |
| `wpf` | BIGINT | Winning team personal fouls | w_fouls |
| `lfgm` | BIGINT | Losing team field goals made | l_fg_made |
| `lfga` | BIGINT | Losing team field goals attempted | l_fg_attempted |
| `lfgm3` | BIGINT | Losing team three-pointers made | l_3p_made |
| `lfga3` | BIGINT | Losing team three-pointers attempted | l_3p_attempted |
| `lftm` | BIGINT | Losing team free throws made | l_ft_made |
| `lfta` | BIGINT | Losing team free throws attempted | l_ft_attempted |
| `lor` | BIGINT | Losing team offensive rebounds | l_off_reb |
| `ldr` | BIGINT | Losing team defensive rebounds | l_def_reb |
| `last` | BIGINT | Losing team assists | l_assists |
| `lto` | BIGINT | Losing team turnovers | l_turnovers |
| `lstl` | BIGINT | Losing team steals | l_steals |
| `lblk` | BIGINT | Losing team blocks | l_blocks |
| `lpf` | BIGINT | Losing team personal fouls | l_fouls |

---

### NCAA.seasons
**Meaning:** Tournament season metadata including bracket region names.
**Synonyms:** Season info, tournament seasons

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `season` | BIGINT | NCAA tournament season year | year |
| `dayzero` | TIMESTAMP | Reference date for day numbering (typically late October) | reference_date, season_start |
| `regionW` | VARCHAR | Region W name: `Albuquerque`, `Atlanta`, `East` | region_1, first_region |
| `regionX` | VARCHAR | Region X name: `Chicago`, `Midwest`, `Oakland`, `Phoenix`, `South`, `Southeast`, `West` | region_2, second_region |
| `regionY` | VARCHAR | Region Y name: `Austin`, `EastRutherford`, `Midwest`, `Minneapolis`, `South`, `Southeast` | region_3, third_region |
| `regionZ` | VARCHAR | Region Z name: `South`, `Southeast`, `Southwest`, `StLouis`, `Syracuse`, `WashingtonDC`, `West` | region_4, fourth_region |

---

### NCAA.teams
**Meaning:** Team master list with team IDs and names.
**Synonyms:** Team roster, team directory

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `team_id` | BIGINT | Unique team identifier | id, team_code |
| `team_name` | VARCHAR | Team name (abbreviated) | name, team |

---

### NCAA.tourney_compact_results
**Meaning:** Tournament game outcomes with basic scoring information.
**Synonyms:** Tournament games, tournament results, March Madness results

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `season` | BIGINT | NCAA tournament season year | year |
| `daynum` | BIGINT | Day number within the season | day |
| `wteam` | BIGINT | Winning team ID | winner_id |
| `wscore` | BIGINT | Winning team's final score | winner_score |
| `lteam` | BIGINT | Losing team ID | loser_id |
| `lscore` | BIGINT | Losing team's final score | loser_score |
| `wloc` | VARCHAR | Winning team's location (always `N` for neutral) | location |
| `numot` | BIGINT | Number of overtime periods | overtimes |

---

### NCAA.tourney_detailed_results
**Meaning:** Tournament game outcomes with detailed box score statistics for both teams.
**Synonyms:** Tournament detailed stats, tournament box scores, March Madness box scores

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `season` | BIGINT | NCAA tournament season year | year |
| `daynum` | BIGINT | Day number within the season | day |
| `wteam` | BIGINT | Winning team ID | winner_id |
| `wscore` | BIGINT | Winning team's final score | winner_score |
| `lteam` | BIGINT | Losing team ID | loser_id |
| `lscore` | BIGINT | Losing team's final score | loser_score |
| `wloc` | VARCHAR | Winning team's location (always `N`) | location |
| `numot` | BIGINT | Number of overtime periods | overtimes |
| `wfgm` | BIGINT | Winning team field goals made | w_fg_made |
| `wfga` | BIGINT | Winning team field goals attempted | w_fg_attempted |
| `wfgm3` | BIGINT | Winning team three-pointers made | w_3p_made |
| `wfga3` | BIGINT | Winning team three-pointers attempted | w_3p_attempted |
| `wftm` | BIGINT | Winning team free throws made | w_ft_made |
| `wfta` | BIGINT | Winning team free throws attempted | w_ft_attempted |
| `wor` | BIGINT | Winning team offensive rebounds | w_off_reb |
| `wdr` | BIGINT | Winning team defensive rebounds | w_def_reb |
| `wast` | BIGINT | Winning team assists | w_assists |
| `wto` | BIGINT | Winning team turnovers | w_turnovers |
| `wstl` | BIGINT | Winning team steals | w_steals |
| `wblk` | BIGINT | Winning team blocks | w_blocks |
| `wpf` | BIGINT | Winning team personal fouls | w_fouls |
| `lfgm` | BIGINT | Losing team field goals made | l_fg_made |
| `lfga` | BIGINT | Losing team field goals attempted | l_fg_attempted |
| `lfgm3` | BIGINT | Losing team three-pointers made | l_3p_made |
| `lfga3` | BIGINT | Losing team three-pointers attempted | l_3p_attempted |
| `lftm` | BIGINT | Losing team free throws made | l_ft_made |
| `lfta` | BIGINT | Losing team free throws attempted | l_ft_attempted |
| `lor` | BIGINT | Losing team offensive rebounds | l_off_reb |
| `ldr` | BIGINT | Losing team defensive rebounds | l_def_reb |
| `last` | BIGINT | Losing team assists | l_assists |
| `lto` | BIGINT | Losing team turnovers | l_turnovers |
| `lstl` | BIGINT | Losing team steals | l_steals |
| `lblk` | BIGINT | Losing team blocks | l_blocks |
| `lpf` | BIGINT | Losing team personal fouls | l_fouls |

---

### NCAA.tourney_seeds
**Meaning:** Tournament seeding assignments mapping teams to seed positions for each season.
**Synonyms:** Seeds, tournament seeds, bracket seeds

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `season` | BIGINT | NCAA tournament season year | year |
| `seed` | VARCHAR | Seed designation (region letter + seed number, e.g., `W01`, `Z15`) | seed_code, seed_position |
| `team` | BIGINT | Team ID assigned to this seed | team_id |

**Seed format:** First character is region (`W`, `X`, `Y`, `Z`), followed by two-digit seed number (01–16).

---

### NCAA.tourney_slots
**Meaning:** Tournament bracket structure defining matchups between seeds.
**Synonyms:** Bracket slots, bracket structure, tournament slots

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `season` | BIGINT | NCAA tournament season year | year |
| `slot` | VARCHAR | Slot identifier (e.g., `R1W1` = Round 1, Region W, Slot 1) | slot_code, bracket_position |
| `strongseed` | VARCHAR | Seed of the higher-ranked team in this matchup | higher_seed, strong_seed_code |
| `weakseed` | VARCHAR | Seed of the lower-ranked team in this matchup | lower_seed, weak_seed_code |

---

### NCAA.target
**Meaning:** Prediction target table for machine learning models, containing tournament game outcomes and predictions.
**Synonyms:** Predictions, targets, ML targets

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | VARCHAR | Unique match identifier (format: `SEASON_TEAM1_TEAM2`) | match_id, game_id |
| `season` | BIGINT | NCAA tournament season year | year |
| `team_id1` | BIGINT | First team ID | team_1, team_a |
| `team_id2` | BIGINT | Second team ID | team_2, team_b |
| `pred` | DOUBLE | Model prediction (probability team_id1 wins) | prediction, win_probability |
| `team_id1_wins` | BIGINT | Actual outcome: 1 if team_id1 won, 0 otherwise | team_1_result, actual_winner |
| `team_id2_wins` | BIGINT | Actual outcome: 1 if team_id2 won, 0 otherwise | team_2_result |

---

## Join Paths

### Teams to Game Results
```sql
NCAA.regular_season_compact_results r
JOIN NCAA.teams t_w ON r.wteam = t_w.team_id
JOIN NCAA.teams t_l ON r.lteam = t_l.team_id
```

### Teams to Tournament Results
```sql
NCAA.tourney_compact_results t
JOIN NCAA.teams t_w ON t.wteam = t_w.team_id
JOIN NCAA.teams t_l ON t.lteam = t_l.team_id
```

### Tournament Seeds to Teams
```sql
NCAA.tourney_seeds ts
JOIN NCAA.teams t ON ts.team = t.team_id
```

### Tournament Slots to Seeds
```sql
NCAA.tourney_slots slot
JOIN NCAA.tourney_seeds ts_strong ON slot.season = ts_strong.season 
  AND slot.strongseed = ts_strong.seed
JOIN NCAA.tourney_seeds ts_weak ON slot.season = ts_weak.season 
  AND slot.weakseed = ts_weak.seed
```

### Seasons to Games
```sql
NCAA.regular_season_compact_results r
JOIN NCAA.seasons s ON r.season = s.season
```

### Target to Tournament Results
```sql
NCAA.target tgt
JOIN NCAA.tourney_compact_results tcr ON tgt.season = tcr.season
  AND ((tgt.team_id1 = tcr.wteam AND tgt.team_id2 = tcr.lteam)
    OR (tgt.team_id1 = tcr.lteam AND tgt.team_id2 = tcr.wteam))
```

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| winning team | `wteam` |
| losing team | `lteam` |
| winner's score | `wscore` |
| loser's score | `lscore` |
| home game | `WHERE wloc = 'H'` |
| away game | `WHERE wloc = 'A'` |
| neutral site | `WHERE wloc = 'N'` |
| overtime game | `WHERE numot > 0` |
| regulation game | `WHERE numot = 0` |
| field goal percentage (winner) | `(wfgm * 100.0) / NULLIF(wfga, 0)` |
| three-point percentage (winner) | `(wfgm3 * 100.0) / NULLIF(wfga3, 0)` |
| free throw percentage (winner) | `(wftm * 100.0) / NULLIF(wfta, 0)` |
| total rebounds (winner) | `wor + wdr` |
| seed number | `CAST(SUBSTRING(seed, 2, 2) AS INT)` from `tourney_seeds.seed` |
| seed region | `SUBSTRING(seed, 1