# ErgastF1 Schema Reference Guide

## Schema Summary

This schema contains Formula 1 racing results, driver and constructor standings, qualifying sessions, lap times, pit stops, and circuit information spanning multiple seasons.

---

## Join Paths

### Results to Drivers
```sql
FROM ErgastF1.results r
JOIN ErgastF1.drivers d ON r.driverId = d.driverId
```
**[REQUIRED]** — to retrieve driver names, codes, or nationality from results.

### Results to Constructors
```sql
FROM ErgastF1.results r
JOIN ErgastF1.constructors c ON r.constructorId = c.constructorId
```
**[REQUIRED]** — to retrieve constructor names or nationality from results.

### Results to Races
```sql
FROM ErgastF1.results r
JOIN ErgastF1.races ra ON r.raceId = ra.raceId
```
**[REQUIRED]** — to retrieve race year, round, date, or circuit information.

### Races to Circuits
```sql
FROM ErgastF1.races ra
JOIN ErgastF1.circuits ci ON ra.circuitId = ci.circuitId
```
**[REQUIRED]** — to retrieve circuit location, country, or coordinates.

### Results to Status
```sql
FROM ErgastF1.results r
JOIN ErgastF1.status s ON r.statusId = s.statusId
```
**[OPTIONAL — display only]** — to show human-readable status (e.g., "Finished", "Engine"). For filtering by completion, use `statusId = 1` directly.

### Qualifying to Drivers & Constructors
```sql
FROM ErgastF1.qualifying q
JOIN ErgastF1.drivers d ON q.driverId = d.driverId
JOIN ErgastF1.constructors c ON q.constructorId = c.constructorId
```
**[REQUIRED]** — to retrieve driver/constructor context for qualifying sessions.

### Lap Times to Drivers & Races
```sql
FROM ErgastF1.lapTimes lt
JOIN ErgastF1.drivers d ON lt.driverId = d.driverId
JOIN ErgastF1.races ra ON lt.raceId = ra.raceId
```
**[REQUIRED]** — to analyze lap performance with driver and race context.

### Pit Stops to Drivers & Races
```sql
FROM ErgastF1.pitStops ps
JOIN ErgastF1.drivers d ON ps.driverId = d.driverId
JOIN ErgastF1.races ra ON ps.raceId = ra.raceId
```
**[REQUIRED]** — to retrieve pit stop context.

### Driver Standings to Drivers
```sql
FROM ErgastF1.driverStandings ds
JOIN ErgastF1.drivers d ON ds.driverId = d.driverId
```
**[REQUIRED]** — to retrieve driver names from standings snapshots.

### Constructor Standings to Constructors
```sql
FROM ErgastF1.constructorStandings cs
JOIN ErgastF1.constructors c ON cs.constructorId = c.constructorId
```
**[REQUIRED]** — to retrieve constructor names from standings snapshots.

---

## Business Rules as SQL

### Podium Finishes
- **IDENTIFY podium:** `WHERE position IN (1, 2, 3)` — rows with position 1, 2, or 3 ARE podium finishes.
- **EXCLUDE disqualifications:** `WHERE position IS NOT NULL AND position != 0` — exclude NULL or 0 position values (disqualifications).

### DNF (Did Not Finish) Handling
- **IDENTIFY DNF:** `WHERE statusId != 1` — rows where status is not "Finished" ARE DNF results.
- **For races entered:** include all rows in `ErgastF1.results` (DNF counts).
- **For races completed:** `WHERE statusId = 1` — only finished races count.

### Lap Time Validity
- **EXCLUDE unreliable lap times:** `WHERE milliseconds >= 60000` — exclude lap times under 60 seconds (data errors).
- **EXCLUDE high-rank fastest laps:** `WHERE rank <= 10 OR rank IS NULL` — exclude fastest lap records with rank > 10 (statistically unreliable).

### Fastest Lap Ranking
- **IDENTIFY fastest lap:** `WHERE rank = 1` — rows with rank = 1 ARE fastest lap of the race.

### Constructor Reliability (Both Cars Started)
- **For constructor reliability metrics:** count only races where both cars from the constructor started (both have entries in `ErgastF1.results` for the same `raceId` and `constructorId`).
  ```sql
  WHERE constructorId IN (
    SELECT constructorId FROM ErgastF1.results r
    GROUP BY raceId, constructorId
    HAVING COUNT(DISTINCT driverId) = 2
  )
  ```

### Constructor Era Separation
- **IDENTIFY historical era:** `WHERE year < 1980` — constructor results before 1980 ARE historical era.
- **For modern analysis:** `WHERE year >= 1980` — exclude historical era from combined statistics.

### Sprint Race Points (2021+)
- Sprint races introduced in 2021; sprint points must be reported separately from main race points.
- **Note:** Current schema does not have explicit sprint race flag. Filter by `year >= 2021` and cross-reference external race metadata if sprint classification is required.

### Driver Comparison Eligibility
- **IDENTIFY rookie:** `WHERE (SELECT COUNT(DISTINCT raceId) FROM ErgastF1.results WHERE driverId = d.driverId) < 20` — drivers with fewer than 20 career starts ARE rookies.
- **For teammate comparison:** only compare drivers who raced at least 10 races together in the same season:
  ```sql
  WHERE (
    SELECT COUNT(DISTINCT r1.raceId)
    FROM ErgastF1.results r1
    JOIN ErgastF1.results r2 ON r1.raceId = r2.raceId
    WHERE r1.driverId = driver1_id
      AND r2.driverId = driver2_id
      AND YEAR(r1.raceId) = season_year
  ) >= 10
  ```

### Cross-Era Driver Comparison
- **For cross-era comparison:** use position-based rankings only; `WHERE points` comparisons are invalid across different points systems (pre-2010 vs. modern).
- **Use instead:** `SELECT position FROM ErgastF1.results` and rank by frequency of top-10 finishes or podiums.

---

## Synonym Glossary

| Question Term | Schema Identifier |
|---|---|
| race result, finish | `ErgastF1.results` |
| driver standings, championship points | `ErgastF1.driverStandings` |
| constructor standings, team points | `ErgastF1.constructorStandings` |
| qualifying session, grid position | `ErgastF1.qualifying` |
| lap time, sector time | `ErgastF1.lapTimes` |
| pit stop, stop duration | `ErgastF1.pitStops` |
| fastest lap, best lap | `ErgastF1.results.fastestLapTime`, `rank = 1` |
| DNF, retirement, did not finish | `statusId != 1` |
| podium, top 3 | `position IN (1, 2, 3)` |
| grid, starting position | `ErgastF1.results.grid` |
| season, year | `ErgastF1.races.year` |
| round, race number | `ErgastF1.races.round` |
| circuit, track, venue | `ErgastF1.circuits` |
| teammate, same constructor same season | join `ErgastF1.results` on `constructorId` and `year` |
| career starts, races entered | `COUNT(DISTINCT raceId)` from `ErgastF1.results` |
| reliability, completion rate | `COUNT(WHERE statusId = 1) / COUNT(*)` |

---

## Table Reference

### `ErgastF1.circuits`
Circuit venues. Plain English: racing track locations.

| Column | Notes |
|---|---|
| `circuitId` | Primary key. |
| `circuitRef` | Slug identifier (e.g., `albert_park`, `sepang`). Use for filtering. |
| `country` | Country name (e.g., "Australia", "Malaysia"). |
| `lat`, `lng`, `alt` | Coordinates and altitude; `alt` may be NULL. |

### `ErgastF1.races`
Race events. Plain English: individual Grand Prix races.

| Column | Notes |
|---|---|
| `raceId` | Primary key. |
| `year` | Season year (e.g., 2009). |
| `round` | Race number within season (1, 2, 3, ...). |
| `circuitId` | Foreign key to `ErgastF1.circuits`. |
| `date` | Race date; sentinel value `1970-03-07` indicates missing data. |
| `time` | Race start time (TIME type); may be NULL. |

### `ErgastF1.results`
Race results. Plain English: finishing positions and points for each driver in each race.

| Column | Notes |
|---|---|
| `resultId` | Primary key. |
| `raceId` | Foreign key to `ErgastF1.races`. |
| `driverId` | Foreign key to `ErgastF1.drivers`. |
| `constructorId` | Foreign key to `ErgastF1.constructors`. |
| `grid` | Starting grid position (1 = pole position). |
| `position` | Finishing position (1, 2, 3, ...). **NULL or 0 = disqualification; exclude from podium/points calculations.** |
| `positionText` | Human-readable position (e.g., "1", "2", "+5.478" for gap). |
| `points` | Points awarded for finish. Pre-2010 points systems differ from modern; use position-based ranking for cross-era comparison. |
| `laps` | Laps completed. |
| `time` | Finishing time as string (e.g., "1:34:50.616"). |
| `milliseconds` | Finishing time in milliseconds. |
| `fastestLap` | Lap number on which fastest lap was set. |
| `rank` | Rank of fastest lap (1 = fastest of race). **Exclude rank > 10 from benchmark analyses.** |
| `fastestLapTime` | Fastest lap time as string. |
| `fastestLapSpeed` | Fastest lap speed (km/h or mph). |
| `statusId` | Foreign key to `ErgastF1.status`. **statusId = 1 means "Finished"; all others are DNF.** |

### `ErgastF1.drivers`
Driver profiles. Plain English: F1 drivers.

| Column | Notes |
|---|---|
| `driverId` | Primary key. |
| `driverRef` | Slug identifier (e.g., `hamilton`, `alonso`). Use for filtering. |
| `number` | Car number; may be NULL for historical drivers. |
| `code` | Three-letter driver code (e.g., "HAM", "ALO"). |
| `forename`, `surname` | Driver name components. |
| `dob` | Date of birth; sentinel value `1970-05-22` indicates missing data. |
| `nationality` | Nationality (e.g., "British", "Spanish"). |

### `ErgastF1.constructors`
Constructor (team) profiles. Plain English: F1 teams.

| Column | Notes |
|---|---|
| `constructorId` | Primary key. |
| `constructorRef` | Slug identifier (e.g., `mclaren`, `ferrari`). Use for filtering. |
| `nationality` | Team nationality (e.g., "British", "Italian"). |

### `ErgastF1.qualifying`
Qualifying session results. Plain English: grid position determination sessions.

| Column | Notes |
|---|---|
| `qualifyId` | Primary key. |
| `raceId` | Foreign key to `ErgastF1.races`. |
| `driverId` | Foreign key to `ErgastF1.drivers`. |
| `constructorId` | Foreign key to `ErgastF1.constructors`. |
| `position` | Final qualifying position (1 = pole). |
| `q1`, `q2`, `q3` | Qualifying session times as strings (e.g., "1:26.572"). NULL if driver did not participate in that session. |

### `ErgastF1.lapTimes`
Lap-by-lap timing data. Plain English: individual lap records for each driver in each race.

| Column | Notes |
|---|---|
| `raceId` | Foreign key to `ErgastF1.races`. |
| `driverId` | Foreign key to `ErgastF1.drivers`. |
| `lap` | Lap number (1, 2, 3, ...). |
| `position` | Position on track during this lap. |
| `time` | Lap time as string (e.g., "1:49.088"). |
| `milliseconds` | Lap time in milliseconds. **Exclude < 60000 (data errors). Exclude if rank > 10 for benchmark analyses.** |

### `ErgastF1.pitStops`
Pit stop records. Plain English: in-race pit stop events.

| Column | Notes |
|---|---|
| `raceId` | Foreign key to `ErgastF1.races`. |
| `driverId` | Foreign key to `ErgastF1.drivers`. |
| `stop` | Stop sequence number (1st stop, 2nd stop, etc.). |
| `lap` | Lap on which stop occurred. |
| `time` | Time of day stop occurred (TIME type). |
| `duration` | Stop duration as string (e.g., "23.227" seconds). |
| `milliseconds` | Stop duration in milliseconds. |

### `ErgastF1.driverStandings`
Driver championship standings snapshots. Plain English: driver points and position after each race.

| Column | Notes |
|---|---|
| `driverStandingsId` | Primary key. |
| `raceId` | Foreign key to `ErgastF1.races` (standings after this race). |
| `driverId` | Foreign key to `ErgastF1.drivers`. |
| `points` | Cumulative points after this race. **Pre-2010 points systems differ; use position for cross-era comparison.** |
| `position` | Championship position (1 = leading). |
| `wins` | Cumulative wins after this race. |

### `ErgastF1.constructorStandings`
Constructor championship standings snapshots. Plain English: team points and position after each race.

| Column | Notes |
|---|---|
| `constructorStandingsId` | Primary key. |
| `raceId` | Foreign key to `ErgastF1.races` (standings after this race). |
| `constructorId` | Foreign key to `ErgastF1.constructors`. |
| `points` | Cumulative points after this race. |
| `position` | Championship position (1 = leading). |
| `wins` | Cumulative wins after this race. |

### `ErgastF1.constructorResults`
Constructor race results. Plain English: team-level points awarded per race.

| Column | Notes |
|---|---|
| `constructorResultsId` | Primary key. |
| `raceId` | Foreign key to `ErgastF1.races`. |
| `constructorId` | Foreign key to `ErgastF1.constructors`. |
| `points` | Points awarded to constructor for this race. |
| `status` | Status flag; typically NULL or "D". |

### `ErgastF1.status`
Status codes. Plain English: race result status categories.

| Column | Notes |
|---|---|
| `statusId` | Primary key. |
| `status` | Status label. Enumerated values: `"Finished"`, `"Disqualified"`, `"Accident"`, `"Collision"`, `"Engine"`, and others. **statusId = 1 is "Finished".** |

### `ErgastF1.seasons`
Season metadata. Plain English: F1 seasons.

| Column | Notes |
|---|---|
| `year` | Season year (primary key). |

### `ErgastF1.target`
Target labels (for ML). Plain English: race outcome labels (win/loss).

| Column | Notes |
|---|---|
| `targetId` | Primary key. |
| `raceId` | Foreign key to `ErgastF1.races`. |
| `driverId` | Foreign key to `ErgastF1.drivers`. |
| `win` | Binary label: 1 = race winner, 0 = not winner. |