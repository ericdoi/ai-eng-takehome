# Basketball Women Schema Reference Guide

## Schema Summary
This schema contains women's professional basketball data including player statistics, team performance, coaching records, draft information, awards, and playoff series results from the ABL (American Basketball League) and WNBA (Women's National Basketball Association).

---

## Table Reference

### Basketball_women.awards_players
**Meaning:** Individual player awards and honors by year and league.
**Synonyms:** player honors, accolades, achievements

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| playerID | VARCHAR | Unique player identifier | player code, ID |
| award | VARCHAR | Award name | honor, accolade |
| year | BIGINT | Award year | season |
| lgID | VARCHAR | League identifier (ABL or WNBA) | league |
| note | VARCHAR | Additional note (e.g., "tie") | annotation |
| pos | VARCHAR | Player position (C, F, G, G-F, Coach) | position |
| name | VARCHAR | Player name | full name |

**Notable award values:** Most Valuable Player, Rookie of the Year, Defensive Player of the Year, All-Star Game Most Valuable Player, WNBA Finals Most Valuable Player, Sixth Woman of the Year, Most Improved Player, Coach of the Year, WNBA All-Decade Team

---

### Basketball_women.coaches
**Meaning:** Coaching records by year, team, and league.
**Synonyms:** coaching statistics, head coaches, coaching performance

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| coachID | VARCHAR | Unique coach identifier | coach code, ID |
| fullName | VARCHAR | Coach full name | name |
| year | BIGINT | Season year | season |
| tmID | VARCHAR | Team identifier | team code |
| lgID | VARCHAR | League identifier (ABL or WNBA) | league |
| stint | BIGINT | Coaching stint number within season | stint number |
| won | BIGINT | Regular season wins | W, wins |
| lost | BIGINT | Regular season losses | L, losses |
| post_wins | BIGINT | Playoff wins | playoff W, postseason wins |
| post_losses | BIGINT | Playoff losses | playoff L, postseason losses |
| playerCoach | VARCHAR | Player-coach indicator (Y/null) | player-coach flag |

---

### Basketball_women.draft
**Meaning:** Annual draft selections with player information and draft outcomes.
**Synonyms:** draft picks, draft selections, draft history

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| draftYear | BIGINT | Year of draft | year |
| draftRound | BIGINT | Draft round number | round |
| draftSelection | BIGINT | Selection within round | pick in round |
| draftOverall | BIGINT | Overall draft position | overall pick |
| tmID | VARCHAR | Team that made selection | team code |
| firstName | VARCHAR | Player first name | first |
| lastName | VARCHAR | Player last name | last |
| fullName | VARCHAR | Player full name | name |
| suffixName | VARCHAR | Name suffix (Jr., Sr., etc.) | suffix |
| playerID | VARCHAR | Unique player identifier | player code, ID |
| draftFrom | VARCHAR | College or institution | college, school |
| lgID | VARCHAR | League (ABL or WNBA) | league |
| playedPro | VARCHAR | Professional career indicator (v=yes, x=no) | pro status |
| notes | VARCHAR | Draft notes (elite, initial, regular, T) | annotation |
| pickRoute | VARCHAR | Route/method of pick | pick method |

---

### Basketball_women.players
**Meaning:** Player biographical and physical information.
**Synonyms:** player roster, player profiles, player information

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| bioID | VARCHAR | Unique player biographical identifier | player ID, bio code |
| firstName | VARCHAR | First name | first |
| middleName | VARCHAR | Middle name | middle |
| lastName | VARCHAR | Last name | last |
| nameGiven | VARCHAR | Given name at birth | birth name |
| fullGivenName | VARCHAR | Full given name | full birth name |
| marriedName | VARCHAR | Married name if applicable | married |
| nameNick | VARCHAR | Nickname(s) | nickname |
| pos | VARCHAR | Primary position (C, F, G, C-F, F-C, F-G, G-F) | position |
| firstseason | BIGINT | First professional season | debut year |
| lastseason | BIGINT | Last professional season | final year |
| height | DOUBLE | Height in inches | ht |
| weight | BIGINT | Weight in pounds | wt |
| college | VARCHAR | College attended | university, school |
| collegeOther | VARCHAR | Other college(s) attended | junior college, transfer |
| birthDate | VARCHAR | Birth date (YYYY-MM-DD) | DOB, date of birth |
| birthCity | VARCHAR | Birth city | city |
| birthState | VARCHAR | Birth state | state |
| birthCountry | VARCHAR | Birth country | country |
| highSchool | VARCHAR | High school name | HS |
| hsCity | VARCHAR | High school city | HS city |
| hsState | VARCHAR | High school state | HS state |
| hsCountry | VARCHAR | High school country (USA, CAN, AUS, etc.) | HS country |
| deathDate | VARCHAR | Death date if applicable (YYYY-MM-DD or 0000-00-00) | DOD |

---

### Basketball_women.players_teams
**Meaning:** Player season statistics by team, including regular season and playoff performance.
**Synonyms:** player statistics, season stats, player performance

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| playerID | VARCHAR | Unique player identifier | player code, ID |
| playerName | VARCHAR | Player name | name |
| year | BIGINT | Season year | season |
| stint | BIGINT | Stint number (if multiple teams in season) | stint |
| tmID | VARCHAR | Team identifier | team code |
| lgID | VARCHAR | League (ABL or WNBA) | league |
| **Regular Season Stats** | | | |
| GP | BIGINT | Games played | games |
| GS | BIGINT | Games started | starts |
| minutes | BIGINT | Total minutes played | mins |
| points | BIGINT | Total points scored | pts |
| oRebounds | BIGINT | Offensive rebounds | OR, off reb |
| dRebounds | BIGINT | Defensive rebounds | DR, def reb |
| rebounds | BIGINT | Total rebounds | reb, TRB |
| assists | BIGINT | Total assists | ast |
| steals | BIGINT | Total steals | stl |
| blocks | BIGINT | Total blocks | blk |
| turnovers | BIGINT | Total turnovers | TO |
| PF | BIGINT | Personal fouls | fouls |
| fgAttempted | BIGINT | Field goals attempted | FGA |
| fgMade | BIGINT | Field goals made | FGM |
| ftAttempted | BIGINT | Free throws attempted | FTA |
| ftMade | BIGINT | Free throws made | FTM |
| threeAttempted | BIGINT | Three-pointers attempted | 3PA |
| threeMade | BIGINT | Three-pointers made | 3PM |
| dq | BIGINT | Disqualifications | DQ |
| **Playoff Stats** | | | |
| PostGP | BIGINT | Playoff games played | playoff games |
| PostGS | BIGINT | Playoff games started | playoff starts |
| PostMinutes | BIGINT | Playoff minutes | playoff mins |
| PostPoints | BIGINT | Playoff points | playoff pts |
| PostoRebounds | BIGINT | Playoff offensive rebounds | playoff OR |
| PostdRebounds | BIGINT | Playoff defensive rebounds | playoff DR |
| PostRebounds | BIGINT | Playoff total rebounds | playoff reb |
| PostAssists | BIGINT | Playoff assists | playoff ast |
| PostSteals | BIGINT | Playoff steals | playoff stl |
| PostBlocks | BIGINT | Playoff blocks | playoff blk |
| PostTurnovers | BIGINT | Playoff turnovers | playoff TO |
| PostPF | BIGINT | Playoff personal fouls | playoff fouls |
| PostfgAttempted | BIGINT | Playoff FG attempted | playoff FGA |
| PostfgMade | BIGINT | Playoff FG made | playoff FGM |
| PostftAttempted | BIGINT | Playoff FT attempted | playoff FTA |
| PostftMade | BIGINT | Playoff FT made | playoff FTM |
| PostthreeAttempted | BIGINT | Playoff 3P attempted | playoff 3PA |
| PostthreeMade | BIGINT | Playoff 3P made | playoff 3PM |
| PostDQ | BIGINT | Playoff disqualifications | playoff DQ |

---

### Basketball_women.series_post
**Meaning:** Playoff series results between teams.
**Synonyms:** playoff results, series outcomes, postseason matchups

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| year | BIGINT | Season year | season |
| round | VARCHAR | Playoff round (FR=first round, CF=conference finals, SF=semifinals, F=finals) | playoff round |
| series | VARCHAR | Series identifier (A-G) | series code |
| tmIDWinner | VARCHAR | Winning team identifier | winner, winning team |
| lgIDWinner | VARCHAR | Winning team league (ABL or WNBA) | winner league |
| tmIDLoser | VARCHAR | Losing team identifier | loser, losing team |
| lgIDLoser | VARCHAR | Losing team league (ABL or WNBA) | loser league |
| W | BIGINT | Wins by winner | series wins |
| L | BIGINT | Losses by winner (wins by loser) | series losses |

**Notable round values:** FR (First Round), SF (Semifinals), CF (Conference Finals), F (Finals)

---

### Basketball_women.teams
**Meaning:** Team season statistics and standings by year and league.
**Synonyms:** team statistics, team performance, standings

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| year | BIGINT | Season year | season |
| lgID | VARCHAR | League (ABL or WNBA) | league |
| tmID | VARCHAR | Team identifier | team code |
| franchID | VARCHAR | Franchise identifier | franchise code |
| confID | VARCHAR | Conference (EA=East, WE=West) | conference |
| divID | VARCHAR | Division identifier | division |
| rank | BIGINT | Final standings rank | standing, position |
| playoff | VARCHAR | Playoff qualification (Y/N) | made playoffs |
| seeded | BIGINT | Playoff seed number | seed |
| firstRound | VARCHAR | First round result (W/L) | first round outcome |
| semis | VARCHAR | Semifinals result (W/L) | semifinals outcome |
| finals | VARCHAR | Finals result (W/L) | finals outcome |
| name | VARCHAR | Team name | team |
| **Offensive Stats (o_)** | | | |
| o_fgm | BIGINT | Offensive FG made | off FGM |
| o_fga | BIGINT | Offensive FG attempted | off FGA |
| o_ftm | BIGINT | Offensive FT made | off FTM |
| o_fta | BIGINT | Offensive FT attempted | off FTA |
| o_3pm | BIGINT | Offensive 3P made | off 3PM |
| o_3pa | BIGINT | Offensive 3P attempted | off 3PA |
| o_oreb | BIGINT | Offensive offensive rebounds | off OR |
| o_dreb | BIGINT | Offensive defensive rebounds | off DR |
| o_reb | BIGINT | Offensive total rebounds | off reb |
| o_asts | BIGINT | Offensive assists | off ast |
| o_pf | BIGINT | Offensive personal fouls | off fouls |
| o_stl | BIGINT | Offensive steals | off stl |
| o_to | BIGINT | Offensive turnovers | off TO |
| o_blk | BIGINT | Offensive blocks | off blk |
| o_pts | BIGINT | Offensive points | off pts |
| **Defensive Stats (d_)** | | | |
| d_fgm | BIGINT | Defensive FG made (opponent) | def FGM |
| d_fga | BIGINT | Defensive FG attempted (opponent) | def FGA |
| d_ftm | BIGINT | Defensive FT made (opponent) | def FTM |
| d_fta | BIGINT | Defensive FT attempted (opponent) | def FTA |
| d_3pm | BIGINT | Defensive 3P made (opponent) | def 3PM |
| d_3pa | BIGINT | Defensive 3P attempted (opponent) | def 3PA |
| d_oreb | BIGINT | Defensive offensive rebounds (opponent) | def OR |
| d_dreb | BIGINT | Defensive defensive rebounds (opponent) | def DR |
| d_reb | BIGINT | Defensive total rebounds (opponent) | def reb |
| d_asts | BIGINT | Defensive assists (opponent) | def ast |
| d_pf | BIGINT | Defensive personal fouls (opponent) | def fouls |
| d_stl | BIGINT | Defensive steals (opponent) | def stl |
| d_to | BIGINT | Defensive turnovers (opponent) | def TO |
| d_blk | BIGINT | Defensive blocks (opponent) | def blk |
| d_pts | BIGINT | Defensive points (opponent) | def pts |
| **Team Rebound Totals** | | | |
| tmORB | BIGINT | Team offensive rebounds | team OR |
| tmDRB | BIGINT | Team defensive rebounds | team DR |
| tmTRB | BIGINT | Team total rebounds | team reb |
| opptmORB | BIGINT | Opponent offensive rebounds | opp OR |
| opptmDRB | BIGINT | Opponent defensive rebounds | opp DR |
| opptmTRB | BIGINT | Opponent total rebounds | opp reb |
| **Record & Attendance** | | | |
| won | BIGINT | Regular season wins | W, wins |
| lost | BIGINT | Regular season losses | L, losses |
| GP | BIGINT | Games played | games |
| homeW | BIGINT | Home wins | home W |
| homeL | BIGINT | Home losses | home L |
| awayW | BIGINT | Away wins | road W, away W |
| awayL | BIGINT | Away losses | road L, away L |
| confW | BIGINT | Conference wins | conf W |
| confL | BIGINT | Conference losses | conf L |
| min | BIGINT | Total minutes played | minutes |
| attend | BIGINT | Total attendance | attendance |
| arena | VARCHAR | Arena name | venue |

---

### Basketball_women.teams_post
**Meaning:** Team playoff records by year and league.
**Synonyms:** playoff records, postseason records, playoff standings

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| year | BIGINT | Season year | season |
| tmID | VARCHAR | Team identifier | team code |
| lgID | VARCHAR | League (ABL or WNBA) | league |
| W | BIGINT | Playoff wins | postseason wins |
| L | BIGINT | Playoff losses | postseason losses |

---

## Join Paths

### Player to Player-Team Statistics
```sql
players.bioID = players_teams.playerID
```
Links player biographical data to their season statistics.

### Player to Awards
```sql
players_teams.playerID = awards_players.playerID
```
Links player statistics to their awards.

### Team to Team Statistics
```sql
teams.tmID = players_teams.tmID 
AND teams.year = players_teams.year 
AND teams.lgID = players_teams.lgID
```
Links team-level statistics to player performance on that team.

### Team to Playoff