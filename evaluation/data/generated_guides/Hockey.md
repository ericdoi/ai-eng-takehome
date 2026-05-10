# Hockey Schema Reference Guide

## Schema Summary

The Hockey schema contains comprehensive historical statistics for professional hockey players, coaches, teams, and awards across multiple leagues (NHL, WHA, NHA, PCHA, WCHL) spanning over a century of play.

---

## Table Reference

### Hockey.Master
**Meaning**: Player and coach biographical registry; the primary identity table for all individuals in the database.
**Synonyms**: Player registry, Coach registry, Personnel master file

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| playerID | VARCHAR | Unique identifier for player | player_key, player_code |
| coachID | VARCHAR | Unique identifier for coach | coach_key, coach_code |
| hofID | VARCHAR | Unique identifier for Hall of Fame entry | hof_key |
| firstName | VARCHAR | Player/coach first name | given_name |
| lastName | VARCHAR | Player/coach last name | family_name |
| nameNote | VARCHAR | Alternate names or birth names | aka, also_known_as |
| nameGiven | VARCHAR | Full given name | formal_first_name |
| nameNick | VARCHAR | Nickname | informal_name |
| height | VARCHAR | Height in inches | ht |
| weight | VARCHAR | Weight in pounds | wt |
| shootCatch | VARCHAR | Shooting/catching hand: B (both), L (left), R (right) | handedness, shot_hand |
| legendsID | VARCHAR | External reference ID | legends_reference |
| ihdbID | VARCHAR | External reference ID | ihdb_reference |
| hrefID | VARCHAR | External reference ID | href_reference |
| firstNHL | VARCHAR | Year of first NHL season | nhl_debut |
| lastNHL | VARCHAR | Year of last NHL season | nhl_final |
| firstWHA | VARCHAR | Year of first WHA season | wha_debut |
| lastWHA | VARCHAR | Year of last WHA season | wha_final |
| pos | VARCHAR | Position: C, D, F, G, L, R, W, or combinations (C/D, D/L, etc.) | position |
| birthYear | VARCHAR | Birth year | birth_yr |
| birthMon | VARCHAR | Birth month (1-12) | birth_month |
| birthDay | VARCHAR | Birth day of month | birth_date |
| birthCountry | VARCHAR | Country of birth | birth_nation |
| birthState | VARCHAR | State/province of birth | birth_province |
| birthCity | VARCHAR | City of birth | birth_place |
| deathYear | VARCHAR | Death year (NULL if living) | death_yr |
| deathMon | VARCHAR | Death month (1-12) | death_month |
| deathDay | VARCHAR | Death day of month | death_date |
| deathCountry | VARCHAR | Country of death | death_nation |
| deathState | VARCHAR | State/province of death | death_province |
| deathCity | VARCHAR | City of death | death_place |

---

### Hockey.Scoring
**Meaning**: Regular season scoring statistics for individual players by year and team.
**Synonyms**: Player statistics, Regular season stats, Scoring records

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| playerID | VARCHAR | Player identifier (FK to Master) | player_key |
| year | BIGINT | Season year | season |
| stint | BIGINT | Stint number within season (1, 2, 3 if traded) | stint_num |
| tmID | VARCHAR | Team identifier | team_code |
| lgID | VARCHAR | League: NHL, WHA, NHA, PCHA, WCHL | league |
| pos | VARCHAR | Position played | position |
| GP | BIGINT | Games played | games |
| G | BIGINT | Goals scored | goals |
| A | BIGINT | Assists | assists |
| Pts | BIGINT | Points (G + A) | points |
| PIM | BIGINT | Penalties in minutes | penalties |
| +/- | VARCHAR | Plus/minus rating | plus_minus |
| PPG | VARCHAR | Power play goals | pp_goals |
| PPA | VARCHAR | Power play assists | pp_assists |
| SHG | VARCHAR | Short-handed goals | sh_goals |
| SHA | VARCHAR | Short-handed assists | sh_assists |
| GWG | VARCHAR | Game-winning goals | gw_goals |
| GTG | VARCHAR | Golden Tie goals | gt_goals |
| SOG | VARCHAR | Shots on goal | shots |
| PostGP | VARCHAR | Playoff games played | playoff_games |
| PostG | VARCHAR | Playoff goals | playoff_goals |
| PostA | VARCHAR | Playoff assists | playoff_assists |
| PostPts | VARCHAR | Playoff points | playoff_points |
| PostPIM | VARCHAR | Playoff penalties | playoff_penalties |
| Post+/- | VARCHAR | Playoff plus/minus | playoff_plus_minus |
| PostPPG | VARCHAR | Playoff power play goals | playoff_pp_goals |
| PostPPA | VARCHAR | Playoff power play assists | playoff_pp_assists |
| PostSHG | VARCHAR | Playoff short-handed goals | playoff_sh_goals |
| PostSHA | VARCHAR | Playoff short-handed assists | playoff_sh_assists |
| PostGWG | VARCHAR | Playoff game-winning goals | playoff_gw_goals |
| PostSOG | VARCHAR | Playoff shots on goal | playoff_shots |

---

### Hockey.Goalies
**Meaning**: Regular season goaltending statistics for individual goalies by year and team.
**Synonyms**: Goalie stats, Goaltender records, Netminder statistics

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| playerID | VARCHAR | Goalie identifier (FK to Master) | goalie_key |
| year | BIGINT | Season year | season |
| stint | BIGINT | Stint number within season | stint_num |
| tmID | VARCHAR | Team identifier | team_code |
| lgID | VARCHAR | League: NHL, WHA, NHA, PCHA, WCHL | league |
| GP | VARCHAR | Games played | games |
| Min | VARCHAR | Minutes played | minutes |
| W | VARCHAR | Wins | wins |
| L | VARCHAR | Losses | losses |
| T/OL | VARCHAR | Ties/Overtime losses | ties_ot |
| ENG | VARCHAR | Empty net goals against | empty_net_goals |
| SHO | VARCHAR | Shutouts | shutouts |
| GA | VARCHAR | Goals against | goals_against |
| SA | VARCHAR | Shots against | shots_against |
| PostGP | VARCHAR | Playoff games played | playoff_games |
| PostMin | VARCHAR | Playoff minutes | playoff_minutes |
| PostW | VARCHAR | Playoff wins | playoff_wins |
| PostL | VARCHAR | Playoff losses | playoff_losses |
| PostT | VARCHAR | Playoff ties | playoff_ties |
| PostENG | VARCHAR | Playoff empty net goals | playoff_empty_net |
| PostSHO | VARCHAR | Playoff shutouts | playoff_shutouts |
| PostGA | VARCHAR | Playoff goals against | playoff_goals_against |
| PostSA | VARCHAR | Playoff shots against | playoff_shots_against |

---

### Hockey.Coaches
**Meaning**: Regular season coaching records by year and team.
**Synonyms**: Coach records, Coaching statistics, Manager statistics

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| coachID | VARCHAR | Coach identifier (FK to Master) | coach_key |
| year | BIGINT | Season year | season |
| tmID | VARCHAR | Team identifier | team_code |
| lgID | VARCHAR | League: NHA, NHL, PCHA, WCHL, WHA | league |
| stint | BIGINT | Stint number within season | stint_num |
| notes | VARCHAR | Special notes (co-coach, interim) | note |
| g | BIGINT | Games coached | games |
| w | BIGINT | Wins | wins |
| l | BIGINT | Losses | losses |
| t | BIGINT | Ties | ties |
| postg | VARCHAR | Playoff games coached | playoff_games |
| postw | VARCHAR | Playoff wins | playoff_wins |
| postl | VARCHAR | Playoff losses | playoff_losses |
| postt | VARCHAR | Playoff ties | playoff_ties |

---

### Hockey.Teams
**Meaning**: Regular season team statistics and standings by year.
**Synonyms**: Team records, Team standings, Season standings

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| year | BIGINT | Season year | season |
| lgID | VARCHAR | League: NHA, NHL, PCHA, WCHL, WHA | league |
| tmID | VARCHAR | Team identifier | team_code |
| franchID | VARCHAR | Franchise identifier | franchise_code |
| confID | VARCHAR | Conference: CC, EC, WA, WC | conference |
| divID | VARCHAR | Division code | division |
| rank | BIGINT | Final standings rank | standing |
| playoff | VARCHAR | Playoff result or seed | playoff_result |
| G | BIGINT | Games played | games |
| W | BIGINT | Wins | wins |
| L | BIGINT | Losses | losses |
| T | BIGINT | Ties | ties |
| OTL | VARCHAR | Overtime losses | ot_losses |
| Pts | BIGINT | Points in standings | points |
| SoW | VARCHAR | Shootout wins | shootout_wins |
| SoL | VARCHAR | Shootout losses | shootout_losses |
| GF | BIGINT | Goals for | goals_for |
| GA | BIGINT | Goals against | goals_against |
| name | VARCHAR | Team name | team_name |
| PIM | VARCHAR | Total penalties in minutes | penalties |
| BenchMinor | VARCHAR | Bench minor penalties | bench_minors |
| PPG | VARCHAR | Power play goals | pp_goals |
| PPC | VARCHAR | Power play chances | pp_chances |
| SHA | VARCHAR | Short-handed assists | sh_assists |
| PKG | VARCHAR | Penalty kill goals | pk_goals |
| PKC | VARCHAR | Penalty kill chances | pk_chances |
| SHF | VARCHAR | Short-handed for | sh_for |

---

### Hockey.TeamsPost
**Meaning**: Playoff season team statistics by year.
**Synonyms**: Playoff team records, Postseason standings

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| year | BIGINT | Season year | season |
| lgID | VARCHAR | League: NHA, NHL, PCHA, WCHL, WHA | league |
| tmID | VARCHAR | Team identifier | team_code |
| G | BIGINT | Playoff games played | games |
| W | BIGINT | Playoff wins | wins |
| L | BIGINT | Playoff losses | losses |
| T | BIGINT | Playoff ties | ties |
| GF | BIGINT | Playoff goals for | goals_for |
| GA | BIGINT | Playoff goals against | goals_against |
| PIM | VARCHAR | Playoff penalties | penalties |
| BenchMinor | VARCHAR | Playoff bench minors | bench_minors |
| PPG | VARCHAR | Playoff power play goals | pp_goals |
| PPC | VARCHAR | Playoff power play chances | pp_chances |
| SHA | VARCHAR | Playoff short-handed assists | sh_assists |
| PKG | VARCHAR | Playoff penalty kill goals | pk_goals |
| PKC | VARCHAR | Playoff penalty kill chances | pk_chances |
| SHF | VARCHAR | Playoff short-handed for | sh_for |

---

### Hockey.SeriesPost
**Meaning**: Playoff series results between two teams.
**Synonyms**: Playoff matchups, Series results, Playoff brackets

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| year | BIGINT | Season year | season |
| round | VARCHAR | Playoff round: ACF, CF, CQF, CSF, DF, DSF, F, Pre, QF, SCF, SCSF, SF, WP | round_name |
| series | VARCHAR | Series identifier (A-O) | series_id |
| tmIDWinner | VARCHAR | Winning team identifier | winner_team |
| lgIDWinner | VARCHAR | Winning team league | winner_league |
| tmIDLoser | VARCHAR | Losing team identifier | loser_team |
| lgIDLoser | VARCHAR | Losing team league | loser_league |
| W | BIGINT | Wins by winner | series_wins |
| L | BIGINT | Wins by loser | series_losses |
| T | BIGINT | Ties in series | series_ties |
| GoalsWinner | BIGINT | Total goals scored by winner | winner_goals |
| GoalsLoser | BIGINT | Total goals scored by loser | loser_goals |
| note | VARCHAR | Special notes: DEF, EX, ND, TG | series_note |

---

### Hockey.AwardsPlayers
**Meaning**: Individual player awards and honors by year.
**Synonyms**: Player awards, Individual honors, Award records

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| playerID | VARCHAR | Player identifier (FK to Master) | player_key |
| award | VARCHAR | Award name (Hart, Vezina, Norris, etc.) | award_name |
| year | BIGINT | Award year | season |
| lgID | VARCHAR | League: NHL, WHA | league |
| note | VARCHAR | Award context: MVP, Rookie, Scoring, shared, tie, Best Defenceman, Best Goaltender, Most Gentlemanly | award_note |
| pos | VARCHAR | Position of awardee | position |

---

### Hockey.AwardsCoaches
**Meaning**: Individual coach awards and honors by year.
**Synonyms**: Coach awards, Coaching honors

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| coachID | VARCHAR | Coach identifier (FK to Master) | coach_key |
| award | VARCHAR | Award: Baldwin, First Team All-Star, Jack Adams, Schmertz, Second Team All-Star | award_name |
| year | BIGINT | Award year | season |
| lgID | VARCHAR | League: NHL, WHA | league |
| note | VARCHAR | Additional notes | award_note |

---

### Hockey.AwardsMisc
**Meaning**: Miscellaneous awards (Patrick Trophy) to individuals and teams.
**Synonyms**: Special awards, Institutional awards

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Recipient name | recipient |
| ID | VARCHAR | Recipient identifier | recipient_id |
| award | VARCHAR | Award: Patrick | award_name |
| year | BIGINT | Award year | season |
| lgID | VARCHAR | League: NHL | league |
| note | VARCHAR | Special notes: posthumous | award_note |

---

### Hockey.HOF
**Meaning**: Hall of Fame induction records.
**Synonyms**: Hall of Fame, HOF inductions, Enshrinements

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| year | BIGINT | Induction year | induction_year |
| hofID | VARCHAR | Hall of Fame identifier | hof_key |
| name | VARCHAR | Inductee name | inductee |
| category | VARCHAR | Category: Player, Builder, Referee/Linesman | inductee_category |

---

### Hockey.Goalies (Stanley Cup era)
**Meaning**: Goaltending statistics for Stanley Cup playoff era (pre-modern).
**Synonyms**: GoaliesSC, Stanley Cup goalies, Historic goalie records

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| playerID | VARCHAR | Goalie identifier | goalie_key |
| year | BIGINT | Season year | season |
| tmID | VARCHAR | Team identifier | team_code |
| lgID | VARCHAR | League: NHA, NHL, PCHA, WCHL | league |
| GP | BIGINT | Games played | games |
| Min | BIGINT | Minutes played | minutes |
| W | BIGINT | Wins | wins |
| L | BIGINT | Losses | losses |
| T | BIGINT | Ties | ties |
| SHO | BIGINT | Shutouts | shutouts |
| GA | BIGINT | Goals against | goals_against |

---

### Hockey.GoaliesShootout
**Meaning**: