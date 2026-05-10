# SQL Reference Guide: lahman_2014 Baseball Database

## Schema Summary

The `lahman_2014` schema contains comprehensive historical baseball statistics from 1871 to 2014, including player performance (batting, pitching, fielding), team records, manager data, awards, Hall of Fame voting, salaries, and player biographical information.

---

## Table Reference

### lahman_2014.allstarfull
**Meaning**: All-Star Game appearances and participation records.
**Synonyms**: All-Star selections, Mid-Summer Classic appearances.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `playerID` | VARCHAR | Unique player identifier | player_id |
| `yearID` | BIGINT | Year of All-Star Game | year, season |
| `gameNum` | BIGINT | Game number (0 = first game, 1 = second game) | game_number |
| `gameID` | VARCHAR | Unique game identifier | game_id |
| `teamID` | VARCHAR | Team code (e.g., ML1 = combined team) | team_id |
| `lgID` | VARCHAR | League: `AL`, `NL` | league_id, league |
| `GP` | BIGINT | Games played in All-Star Game | games_played |
| `startingPos` | BIGINT | Starting position (9=RF, null=bench) | starting_position, position |

---

### lahman_2014.appearances
**Meaning**: Annual player appearance records by position and game type.
**Synonyms**: Player games by position, Position appearances.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `yearID` | BIGINT | Season year | year, season |
| `teamID` | VARCHAR | Team code | team_id |
| `lgID` | VARCHAR | League: `AA`, `AL`, `FL`, `NA`, `NL`, `PL`, `UA` | league_id |
| `playerID` | VARCHAR | Unique player identifier | player_id |
| `G_all` | BIGINT | Total games played | total_games, games |
| `G_batting` | BIGINT | Games as batter | batting_games |
| `G_defense` | BIGINT | Games on defense | defensive_games |
| `G_p` | BIGINT | Games as pitcher | pitcher_games |
| `G_c` | BIGINT | Games as catcher | catcher_games |
| `G_1b` | BIGINT | Games at first base | first_base_games |
| `G_2b` | BIGINT | Games at second base | second_base_games |
| `G_3b` | BIGINT | Games at third base | third_base_games |
| `G_ss` | BIGINT | Games at shortstop | shortstop_games |
| `G_lf` | BIGINT | Games in left field | left_field_games |
| `G_cf` | BIGINT | Games in center field | center_field_games |
| `G_rf` | BIGINT | Games in right field | right_field_games |
| `G_of` | BIGINT | Games in outfield (combined) | outfield_games |
| `G_dh` | BIGINT | Games as designated hitter | dh_games |
| `G_ph` | BIGINT | Games as pinch hitter | pinch_hitter_games |
| `G_pr` | BIGINT | Games as pinch runner | pinch_runner_games |

---

### lahman_2014.awardsmanagers
**Meaning**: Manager award voting records (TSN Manager of the Year, BBWAA Manager of the Year).
**Synonyms**: Manager awards, Manager honors.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `managerID` | VARCHAR | Unique manager identifier | manager_id |
| `awardID` | VARCHAR | Award name: `BBWAA Manager of the year`, `TSN Manager of the Year` | award_id, award |
| `yearID` | BIGINT | Year of award | year, season |
| `lgID` | VARCHAR | League: `AL`, `ML` (Major Leagues), `NL` | league_id |
| `tie` | VARCHAR | Tie indicator: `Y` or null | tie_flag |
| `notes` | VARCHAR | Additional notes | notes |

---

### lahman_2014.awardsplayers
**Meaning**: Player award voting records (MVP, Cy Young, Triple Crown, etc.).
**Synonyms**: Player awards, Player honors.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `playerID` | VARCHAR | Unique player identifier | player_id |
| `awardID` | VARCHAR | Award name (e.g., `Triple Crown`, `Pitching Triple Crown`) | award_id, award |
| `yearID` | BIGINT | Year of award | year, season |
| `lgID` | VARCHAR | League: `AA`, `AL`, `ML`, `NL` | league_id |
| `tie` | VARCHAR | Tie indicator: `Y` or null | tie_flag |
| `notes` | VARCHAR | Additional notes | notes |

---

### lahman_2014.awardssharemanagers
**Meaning**: Manager award voting share (points and first-place votes).
**Synonyms**: Manager award voting, Manager award points.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `awardID` | VARCHAR | Award name: `Mgr of the year`, `Mgr of the Year` | award_id, award |
| `yearID` | BIGINT | Year of award | year, season |
| `lgID` | VARCHAR | League: `AL`, `NL` | league_id |
| `managerID` | VARCHAR | Unique manager identifier | manager_id |
| `pointsWon` | BIGINT | Points received in voting | points, votes_points |
| `pointsMax` | BIGINT | Maximum possible points | max_points, total_points |
| `votesFirst` | BIGINT | Number of first-place votes | first_place_votes, first_votes |

---

### lahman_2014.awardsshareplayers
**Meaning**: Player award voting share (points and first-place votes for MVP, Cy Young, Rookie of the Year).
**Synonyms**: Player award voting, Player award points.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `awardID` | VARCHAR | Award name: `Cy Young`, `MVP`, `Rookie of the Year` | award_id, award |
| `yearID` | BIGINT | Year of award | year, season |
| `lgID` | VARCHAR | League: `AL`, `ML`, `NL` | league_id |
| `playerID` | VARCHAR | Unique player identifier | player_id |
| `pointsWon` | BIGINT | Points received in voting | points, votes_points |
| `pointsMax` | BIGINT | Maximum possible points | max_points, total_points |
| `votesFirst` | BIGINT | Number of first-place votes | first_place_votes, first_votes |

---

### lahman_2014.batting
**Meaning**: Annual player batting statistics (hits, runs, home runs, etc.).
**Synonyms**: Batting stats, Offensive statistics, Hitter statistics.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `playerID` | VARCHAR | Unique player identifier | player_id |
| `yearID` | BIGINT | Season year | year, season |
| `stint` | BIGINT | Stint number (1 = first team, 2 = second team, etc.) | stint_number |
| `teamID` | VARCHAR | Team code | team_id |
| `lgID` | VARCHAR | League: `AA`, `AL`, `FL`, `NA`, `NL`, `PL`, `UA` | league_id |
| `G` | BIGINT | Games played | games, games_played |
| `G_batting` | BIGINT | Games as batter | batting_games |
| `AB` | BIGINT | At-bats | at_bats, at_bat |
| `R` | BIGINT | Runs scored | runs, runs_scored |
| `H` | BIGINT | Hits | hits |
| `2B` | BIGINT | Doubles | doubles |
| `3B` | BIGINT | Triples | triples |
| `HR` | BIGINT | Home runs | home_runs, homers |
| `RBI` | BIGINT | Runs batted in | rbis, runs_batted_in |
| `SB` | BIGINT | Stolen bases | stolen_bases, steals |
| `CS` | BIGINT | Caught stealing | caught_stealing |
| `BB` | BIGINT | Walks | walks, bases_on_balls |
| `SO` | BIGINT | Strikeouts | strikeouts, strike_outs |
| `IBB` | BIGINT | Intentional walks | intentional_walks, intentional_bb |
| `HBP` | BIGINT | Hit by pitch | hit_by_pitch |
| `SH` | BIGINT | Sacrifice hits | sacrifice_hits, sacrifices |
| `SF` | BIGINT | Sacrifice flies | sacrifice_flies |
| `GIDP` | BIGINT | Grounded into double play | gidp, double_plays |
| `G_old` | BIGINT | Games (legacy field) | games_old |

---

### lahman_2014.battingpost
**Meaning**: Playoff batting statistics by round (ALCS, NLCS, World Series, etc.).
**Synonyms**: Postseason batting, Playoff batting stats.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `yearID` | BIGINT | Season year | year, season |
| `round` | VARCHAR | Playoff round: `AEDIV`, `ALCS`, `ALDS1`, `ALDS2`, `ALWC`, `AWDIV`, `CS`, `NEDIV`, `NLCS`, `NLDS1`, `NLDS2`, `NLWC`, `NWDIV`, `WS` | round_name, playoff_round |
| `playerID` | VARCHAR | Unique player identifier | player_id |
| `teamID` | VARCHAR | Team code | team_id |
| `lgID` | VARCHAR | League: `AA`, `AL`, `NL` | league_id |
| `G` | BIGINT | Games played | games, games_played |
| `AB` | BIGINT | At-bats | at_bats |
| `R` | BIGINT | Runs scored | runs |
| `H` | BIGINT | Hits | hits |
| `2B` | BIGINT | Doubles | doubles |
| `3B` | BIGINT | Triples | triples |
| `HR` | BIGINT | Home runs | home_runs |
| `RBI` | BIGINT | Runs batted in | rbis |
| `SB` | BIGINT | Stolen bases | stolen_bases |
| `CS` | BIGINT | Caught stealing | caught_stealing |
| `BB` | BIGINT | Walks | walks |
| `SO` | BIGINT | Strikeouts | strikeouts |
| `IBB` | BIGINT | Intentional walks | intentional_walks |
| `HBP` | BIGINT | Hit by pitch | hit_by_pitch |
| `SH` | BIGINT | Sacrifice hits | sacrifice_hits |
| `SF` | BIGINT | Sacrifice flies | sacrifice_flies |
| `GIDP` | BIGINT | Grounded into double play | gidp |

---

### lahman_2014.els_teamnames
**Meaning**: Historical team names and park associations (legacy data).
**Synonyms**: Team name history, Historical team records.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Record identifier | id |
| `lgid` | VARCHAR | League: `AA`, `AL`, `FL`, `NA`, `NL`, `PL`, `UA` | league_id |
| `teamid` | VARCHAR | Team code | team_id |
| `franchid` | VARCHAR | Franchise identifier | franchise_id |
| `name` | VARCHAR | Team name | team_name |
| `park` | VARCHAR | Stadium/park name | stadium, ballpark |

---

### lahman_2014.fielding
**Meaning**: Annual player fielding statistics by position (putouts, assists, errors).
**Synonyms**: Defensive statistics, Fielding stats.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `playerID` | VARCHAR | Unique player identifier | player_id |
| `yearID` | BIGINT | Season year | year, season |
| `stint` | BIGINT | Stint number | stint_number |
| `teamID` | VARCHAR | Team code | team_id |
| `lgID` | VARCHAR | League: `AA`, `AL`, `FL`, `NA`, `NL`, `PL`, `UA` | league_id |
| `POS` | VARCHAR | Position: `1B`, `2B`, `3B`, `C`, `CF`, `DH`, `LF`, `OF`, `P`, `RF`, `SS` | position |
| `G` | BIGINT | Games played at position | games, games_played |
| `GS` | BIGINT | Games started at position | games_started |
| `InnOuts` | BIGINT | Innings played (in outs) | innings_outs, innings |
| `PO` | BIGINT | Putouts | putouts |
| `A` | BIGINT | Assists | assists |
| `E` | BIGINT | Errors | errors |
| `DP` | BIGINT | Double plays | double_plays |
| `PB` | BIGINT | Passed balls (catchers) | passed_balls |
| `WP` | BIGINT | Wild pitches (pitchers) | wild_pitches |
| `SB` | BIGINT | Stolen bases allowed (catchers) | stolen_bases_allowed |
| `CS` | BIGINT | Caught stealing (catchers) | caught_stealing |
| `ZR` | BIGINT | Zone rating (advanced metric) | zone_rating |

---

### lahman_2014.fieldingof
**Meaning**: Outfield position breakdown (left field, center field, right field games).
**Synonyms**: Outfield position splits, Outfield games by position.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `playerID` | VARCHAR | Unique player identifier | player_id |
| `yearID` | BIGINT | Season year | year, season |
| `stint` | BIGINT | Stint number | stint_number |
| `Glf` | BIGINT | Games in left field | left_field_games, lf_games |
| `Gcf` | BIGINT | Games in center field | center_field_games, cf_games |
| `Grf` | BIGINT | Games in right field | right_field_games, rf_games |

---

### lahman_2014.fieldingpost
**Meaning**: Playoff fielding statistics by position and round.
**Synonyms**: Postseason fielding, Playoff defensive stats.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `playerID` | VARCHAR | Unique player identifier | player_id |
| `yearID` | BIGINT | Season year | year, season |
| `teamID` | VARCHAR | Team code | team_id |
| `lgID` | VARCHAR | League: `AL`, `NL` | league_id |
| `round` | VARCHAR | Playoff round: `AEDIV`, `ALCS`, `ALDS1`, `ALDS2`, `ALWC`, `AWDIV`, `NEDIV`, `NLCS`, `NLDS1`, `NLDS2`, `NLWC`, `NWDIV`, `WS` | round_name |
| `POS` | VARCHAR | Position: `1B`, `2B`,