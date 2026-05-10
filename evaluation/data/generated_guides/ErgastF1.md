# ErgastF1 SQL Reference Guide

## Schema Summary
The ErgastF1 schema contains complete Formula 1 racing data including drivers, constructors, races, results, qualifying sessions, lap times, pit stops, and championship standings from 1950 onward.

---

## Table Reference

### ErgastF1.circuits
**Meaning:** Formula 1 racing venues and their geographic locations.
**Synonyms:** tracks, venues, racetracks

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `circuitId` | BIGINT | Unique circuit identifier | track ID |
| `circuitRef` | VARCHAR | URL-friendly circuit reference code | circuit code, ref |
| `name` | VARCHAR | Official circuit name | track name |
| `location` | VARCHAR | City or region where circuit is located | city, region |
| `country` | VARCHAR | Country name | nation |
| `lat` | DOUBLE | Latitude coordinate | latitude |
| `lng` | DOUBLE | Longitude coordinate | longitude |
| `alt` | BIGINT | Altitude in meters | altitude, elevation |
| `url` | VARCHAR | Wikipedia reference URL | link |

---

### ErgastF1.races
**Meaning:** Formula 1 Grand Prix events, one row per race per year.
**Synonyms:** events, grands prix, competitions

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `raceId` | BIGINT | Unique race identifier | event ID |
| `year` | BIGINT | Calendar year of race | season |
| `round` | BIGINT | Sequential round number within the season | race number, round number |
| `circuitId` | BIGINT | Foreign key to circuits table | track ID |
| `name` | VARCHAR | Official race name (e.g., "Australian Grand Prix") | race name, event name |
| `date` | DATE | Race date | race date |
| `time` | TIME | Race start time (UTC) | start time |
| `url` | VARCHAR | Wikipedia reference URL | link |

---

### ErgastF1.drivers
**Meaning:** Formula 1 drivers with biographical information.
**Synonyms:** pilots, competitors, athletes

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `driverId` | BIGINT | Unique driver identifier | driver ID |
| `driverRef` | VARCHAR | URL-friendly driver reference code | driver code, ref |
| `number` | BIGINT | Current or most recent car number; NULL if never assigned | car number |
| `code` | VARCHAR | Three-letter driver code (e.g., "HAM", "ALO") | driver code, abbreviation |
| `forename` | VARCHAR | Driver's first name | first name |
| `surname` | VARCHAR | Driver's last name | last name, family name |
| `dob` | DATE | Date of birth | birth date |
| `nationality` | VARCHAR | Driver's nationality | country, nation |
| `url` | VARCHAR | Wikipedia reference URL | link |

---

### ErgastF1.constructors
**Meaning:** Formula 1 teams and manufacturers.
**Synonyms:** teams, manufacturers, stables

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `constructorId` | BIGINT | Unique constructor identifier | team ID |
| `constructorRef` | VARCHAR | URL-friendly constructor reference code | team code, ref |
| `name` | VARCHAR | Official team/constructor name | team name |
| `nationality` | VARCHAR | Constructor's nationality | country, nation |
| `url` | VARCHAR | Wikipedia reference URL | link |

---

### ErgastF1.results
**Meaning:** Race results for each driver in each race, including finishing position, points, and fastest lap data.
**Synonyms:** race outcomes, finishes, race results

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `resultId` | BIGINT | Unique result identifier | result ID |
| `raceId` | BIGINT | Foreign key to races table | race ID |
| `driverId` | BIGINT | Foreign key to drivers table | driver ID |
| `constructorId` | BIGINT | Foreign key to constructors table | team ID |
| `number` | BIGINT | Car number used in race | car number |
| `grid` | BIGINT | Starting grid position (1 = pole position) | starting position, grid position |
| `position` | BIGINT | Finishing position; NULL or 0 = disqualified/DNF | finishing position, final position |
| `positionText` | VARCHAR | Finishing position as text (e.g., "1", "R" for retired) | position text |
| `positionOrder` | BIGINT | Numeric ordering for sorting (handles retirements) | position order |
| `points` | DOUBLE | Championship points awarded for this result | race points, points scored |
| `laps` | BIGINT | Number of laps completed | laps completed |
| `time` | VARCHAR | Total race time or gap to leader (e.g., "+5.478") | race time, total time |
| `milliseconds` | BIGINT | Total race time in milliseconds | race time ms |
| `fastestLap` | BIGINT | Lap number on which fastest lap was set | fastest lap number |
| `rank` | BIGINT | Ranking of fastest lap (1 = fastest in race); NULL if not in top 10 | fastest lap rank |
| `fastestLapTime` | VARCHAR | Fastest lap time (e.g., "1:27.452") | fastest lap, best lap time |
| `fastestLapSpeed` | VARCHAR | Speed during fastest lap (e.g., "218.300" km/h) | fastest lap speed |
| `statusId` | BIGINT | Foreign key to status table | status ID |

---

### ErgastF1.qualifying
**Meaning:** Qualifying session results for each driver in each race.
**Synonyms:** qualifying results, grid positions, qualifying sessions

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `qualifyId` | BIGINT | Unique qualifying result identifier | qualify ID |
| `raceId` | BIGINT | Foreign key to races table | race ID |
| `driverId` | BIGINT | Foreign key to drivers table | driver ID |
| `constructorId` | BIGINT | Foreign key to constructors table | team ID |
| `number` | BIGINT | Car number used in qualifying | car number |
| `position` | BIGINT | Final qualifying position (1 = pole position) | grid position, qualifying position |
| `q1` | VARCHAR | Best lap time in Q1 session (e.g., "1:26.572"); NULL if eliminated | Q1 time |
| `q2` | VARCHAR | Best lap time in Q2 session; NULL if eliminated or not reached | Q2 time |
| `q3` | VARCHAR | Best lap time in Q3 session; NULL if eliminated or not reached | Q3 time |

---

### ErgastF1.lapTimes
**Meaning:** Individual lap times for each driver in each race.
**Synonyms:** lap data, lap records, lap performance

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `raceId` | BIGINT | Foreign key to races table | race ID |
| `driverId` | BIGINT | Foreign key to drivers table | driver ID |
| `lap` | BIGINT | Lap number (1-indexed) | lap number |
| `position` | BIGINT | Driver's position on this lap | position on lap |
| `time` | VARCHAR | Lap time (e.g., "1:49.088") | lap time |
| `milliseconds` | BIGINT | Lap time in milliseconds | lap time ms |

---

### ErgastF1.pitStops
**Meaning:** Pit stop events during races, one row per stop per driver.
**Synonyms:** pit stop data, stops, pit events

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `raceId` | BIGINT | Foreign key to races table | race ID |
| `driverId` | BIGINT | Foreign key to drivers table | driver ID |
| `stop` | BIGINT | Sequential stop number (1, 2, 3, etc.) | stop number |
| `lap` | BIGINT | Lap number on which stop occurred | lap number |
| `time` | TIME | Clock time of pit stop (UTC) | stop time |
| `duration` | VARCHAR | Duration of pit stop (e.g., "23.227" seconds) | stop duration |
| `milliseconds` | BIGINT | Duration in milliseconds | duration ms |

---

### ErgastF1.driverStandings
**Meaning:** Championship standings for drivers after each race, cumulative points and position.
**Synonyms:** driver standings, championship standings, driver points

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `driverStandingsId` | BIGINT | Unique standings record identifier | standings ID |
| `raceId` | BIGINT | Foreign key to races table (standings after this race) | race ID |
| `driverId` | BIGINT | Foreign key to drivers table | driver ID |
| `points` | DOUBLE | Cumulative championship points after this race | total points, cumulative points |
| `position` | BIGINT | Current championship position (1 = leader) | standing position, rank |
| `positionText` | VARCHAR | Position as text (e.g., "1", "2") | position text |
| `wins` | BIGINT | Cumulative race wins after this race | total wins |

---

### ErgastF1.constructorStandings
**Meaning:** Championship standings for constructors after each race, cumulative points and position.
**Synonyms:** constructor standings, team standings, constructor points

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `constructorStandingsId` | BIGINT | Unique standings record identifier | standings ID |
| `raceId` | BIGINT | Foreign key to races table (standings after this race) | race ID |
| `constructorId` | BIGINT | Foreign key to constructors table | team ID |
| `points` | DOUBLE | Cumulative championship points after this race | total points, cumulative points |
| `position` | BIGINT | Current championship position (1 = leader) | standing position, rank |
| `positionText` | VARCHAR | Position as text (e.g., "1", "2") | position text |
| `wins` | BIGINT | Cumulative race wins after this race | total wins |

---

### ErgastF1.constructorResults
**Meaning:** Constructor-level results aggregated per race (rarely used; prefer results table).
**Synonyms:** team results, constructor race results

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `constructorResultsId` | BIGINT | Unique constructor result identifier | result ID |
| `raceId` | BIGINT | Foreign key to races table | race ID |
| `constructorId` | BIGINT | Foreign key to constructors table | team ID |
| `points` | DOUBLE | Total points scored by constructor in race | race points |
| `status` | VARCHAR | Status code; observed value: "D" | status |

---

### ErgastF1.status
**Meaning:** Enumeration of race result status codes (finished, retired, disqualified, etc.).
**Synonyms:** result status, finish status

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `statusId` | BIGINT | Unique status identifier | status ID |
| `status` | VARCHAR | Status description | status text |

**Enumerated values (sample):**
- `1` = "Finished"
- `2` = "Disqualified"
- `3` = "Accident"
- `4` = "Collision"
- `5` = "Engine"

---

### ErgastF1.seasons
**Meaning:** List of Formula 1 seasons (years) with metadata.
**Synonyms:** years, seasons

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `year` | BIGINT | Calendar year | season year |
| `url` | VARCHAR | Wikipedia reference URL | link |

---

### ErgastF1.target
**Meaning:** Target variable for machine learning: whether a driver won a given race.
**Synonyms:** race winners, win labels, prediction target

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `targetId` | BIGINT | Unique target record identifier | target ID |
| `raceId` | BIGINT | Foreign key to races table | race ID |
| `driverId` | BIGINT | Foreign key to drivers table | driver ID |
| `win` | BIGINT | Binary indicator: 1 = driver won race, 0 = did not win | race winner, win flag |

---

## Join Paths

### Core Result Joins
```sql
-- Driver, constructor, and race for a result
results r
  JOIN drivers d ON r.driverId = d.driverId
  JOIN constructors c ON r.constructorId = c.constructorId
  JOIN races ra ON r.raceId = ra.raceId
  JOIN circuits ci ON ra.circuitId = ci.circuitId
  JOIN status s ON r.statusId = s.statusId
```

### Qualifying to Results
```sql
-- Match qualifying to race results
qualifying q
  JOIN results r ON q.raceId = r.raceId AND q.driverId = r.driverId
```

### Lap Times to Race
```sql
-- Lap times with race and driver context
lapTimes lt
  JOIN races ra ON lt.raceId = ra.raceId
  JOIN drivers d ON lt.driverId = d.driverId
```

### Pit Stops to Race
```sql
-- Pit stops with race and driver context
pitStops ps
  JOIN races ra ON ps.raceId = ra.raceId
  JOIN drivers d ON ps.driverId = d.driverId
```

### Standings to Race
```sql
-- Driver standings after a specific race
driverStandings ds
  JOIN races ra ON ds.raceId = ra.raceId
  JOIN drivers d ON ds.driverId = d.driverId
```

### Constructor Standings to Race
```sql
-- Constructor standings after a specific race
constructorStandings cs
  JOIN races ra ON cs.raceId = ra.raceId
  JOIN constructors c ON cs.constructorId = c.constructorId
```

---

## Business Rules as SQL

### Points and Standings

**Rule: Exclude disqualifications from podium, points, and top-10 calculations**
```sql
WHERE results.position IS NOT NULL AND results.position > 0
```

**Rule: Podium finish is position 1, 2, or 3**
```sql
WHERE results.position IN (1, 2, 3) AND results.position IS NOT NULL
```

**Rule: DNF (Did Not Finish) counts toward races entered but not races completed**
```sql
-- Races entered: all rows in results
-- Races completed: WHERE results.position IS NOT NULL AND results.position > 0
```

**Rule: Pre-2010 points systems incompatible with modern scoring; use position-based rankings only**
```sql
-- For cross-era comparisons, use position rankings:
WHERE races.year < 2010
-- Then rank by position, not by results.points
```

### Lap Time Analysis

**Rule: Exclude lap times under 60 seconds as data errors**
```sql
WHERE lapTimes.milliseconds >= 60000
```

**Rule: Fastest lap times with rank > 10 are unreliable; exclude from benchmarks**
```sql
WHERE results.rank IS NOT NULL AND results.rank <= 10
-- OR: WHERE results.rank <= 10
```

### Constructor Performance

**Rule: When measuring constructor reliability, only count races where BOTH cars started**
```sql
-- Count distinct drivers per constructor per race, filter for count = 2:
HAVING COUNT(DISTINCT results.driverId) = 2
```

**Rule: Constructor results before 1980 reported separately as "historical era"**
```sql
WHERE races.year < 1980  -- historical era
WHERE races.year >= 1980 -- modern era
```

**Rule: Sprint race points (introduced 2021) reported separately, never combined**