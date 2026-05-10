# ErgastF1 Schema Reference Guide

## Schema Summary
Historical Formula 1 racing data including drivers, constructors, circuits, race results, qualifying sessions, lap times, pit stops, and championship standings from 1950 onwards.

---

## Join Paths

**Race with circuit and results:**
```sql
FROM ErgastF1.races r
JOIN ErgastF1.circuits c ON r.circuitId = c.circuitId
JOIN ErgastF1.results res ON r.raceId = res.raceId
```

**Driver performance in a race:**
```sql
FROM ErgastF1.results res
JOIN ErgastF1.drivers d ON res.driverId = d.driverId
JOIN ErgastF1.constructors con ON res.constructorId = con.constructorId
JOIN ErgastF1.races r ON res.raceId = r.raceId
```

**Qualifying session:**
```sql
FROM ErgastF1.qualifying q
JOIN ErgastF1.drivers d ON q.driverId = d.driverId
JOIN ErgastF1.constructors con ON q.constructorId = con.constructorId
JOIN ErgastF1.races r ON q.raceId = r.raceId
```

**Driver standings progression:**
```sql
FROM ErgastF1.driverStandings ds
JOIN ErgastF1.drivers d ON ds.driverId = d.driverId
JOIN ErgastF1.races r ON ds.raceId = r.raceId
```

**Lap times for a driver in a race:**
```sql
FROM ErgastF1.lapTimes lt
JOIN ErgastF1.drivers d ON lt.driverId = d.driverId
JOIN ErgastF1.races r ON lt.raceId = r.raceId
```

**Pit stops:**
```sql
FROM ErgastF1.pitStops ps
JOIN ErgastF1.drivers d ON ps.driverId = d.driverId
JOIN ErgastF1.races r ON ps.raceId = r.raceId
```

---

## Business Rules as SQL

**Exclude disqualifications from podium/points calculations:**
```sql
WHERE res.position IS NOT NULL AND res.position != 0
```

**Podium finish (positions 1, 2, or 3):**
```sql
WHERE res.position IN (1, 2, 3) AND res.position IS NOT NULL AND res.position != 0
```

**DNF (Did Not Finish) — exclude from races completed:**
```sql
WHERE st.status != 'Finished'
```

**Exclude unreliable fastest lap times:**
```sql
WHERE res.rank <= 10 AND res.fastestLapTime IS NOT NULL
```

**Exclude lap times under 60 seconds (data errors):**
```sql
WHERE lt.milliseconds >= 60000
```

**Constructor reliability — both cars started:**
```sql
WHERE (SELECT COUNT(DISTINCT res2.driverId) 
       FROM ErgastF1.results res2 
       WHERE res2.raceId = res.raceId 
       AND res2.constructorId = res.constructorId) = 2
```

**Rookie classification (fewer than 20 career starts):**
```sql
WHERE (SELECT COUNT(*) FROM ErgastF1.results r2 WHERE r2.driverId = d.driverId) < 20
```

**Teammate comparison (at least 10 races together in same season):**
```sql
HAVING COUNT(DISTINCT res.raceId) >= 10
```

**Sprint race points (2021 onwards):**
```sql
WHERE r.year >= 2021 AND r.round IN (SELECT DISTINCT round FROM ErgastF1.races WHERE year >= 2021)
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| race winner | `res.position = 1` |
| podium | `res.position IN (1, 2, 3)` |
| fastest lap | `res.rank = 1` |
| DNF / Did Not Finish | `st.status != 'Finished'` |
| grid position | `res.grid` |
| qualifying time | `q.q1`, `q.q2`, `q.q3` |
| pit stop duration | `ps.milliseconds` |
| championship points | `ds.points` or `cs.points` |
| career starts | `COUNT(DISTINCT res.raceId)` |
| pole position | `q.position = 1` |
| fastest lap speed | `res.fastestLapSpeed` |
| constructor nationality | `con.nationality` |
| driver nationality | `d.nationality` |

---

## Table Reference

### `ErgastF1.circuits`
Physical race venues. Columns: `circuitRef` (unique identifier), `location`, `country`, `lat`/`lng` (coordinates), `alt` (altitude in meters).

### `ErgastF1.drivers`
Driver roster. Columns: `driverRef` (unique identifier), `number` (car number, may be NULL), `code` (3-letter code), `forename`/`surname`, `dob` (date of birth), `nationality`.

### `ErgastF1.constructors`
Teams/manufacturers. Columns: `constructorRef` (unique identifier), `nationality`.

### `ErgastF1.races`
Individual race events. Columns: `year`, `round` (race number in season), `circuitId`, `date`, `time` (race start time UTC). Primary key: `raceId`.

### `ErgastF1.results`
Race finish data. **Critical columns:**
- `position` (finishing position; NULL or 0 = disqualification/DNF)
- `positionText` (text representation of position)
- `grid` (starting grid position)
- `points` (championship points awarded)
- `laps` (laps completed)
- `time` (elapsed time or gap to leader)
- `milliseconds` (race duration in milliseconds)
- `fastestLap` (lap number of fastest lap)
- `rank` (fastest lap ranking; >10 indicates unreliable data)
- `fastestLapTime` (fastest lap duration)
- `fastestLapSpeed` (fastest lap speed)
- `statusId` (foreign key to `status` table)

### `ErgastF1.status`
Result status codes. **Values:** `Finished`, `Disqualified`, `Accident`, `Collision`, `Engine`, etc.

### `ErgastF1.qualifying`
Qualifying session results. Columns: `position` (grid position), `q1`/`q2`/`q3` (qualifying times for each session; NULL if eliminated).

### `ErgastF1.driverStandings`
Championship standings after each race. Columns: `points` (cumulative points), `position` (current rank), `positionText`, `wins` (race wins to date).

### `ErgastF1.constructorStandings`
Constructor championship standings after each race. Columns: `points`, `position`, `positionText`, `wins`.

### `ErgastF1.constructorResults`
Constructor points per race. Columns: `points`, `status` (typically NULL or `D`).

### `ErgastF1.lapTimes`
Individual lap telemetry. Columns: `lap` (lap number), `position` (position on that lap), `time` (lap duration), `milliseconds` (lap duration in ms). **Note:** Exclude `milliseconds < 60000` (data errors).

### `ErgastF1.pitStops`
Pit stop events. Columns: `stop` (stop number in race), `lap` (lap number), `time` (clock time of stop), `duration` (stop duration), `milliseconds` (stop duration in ms).

### `ErgastF1.seasons`
Season metadata. Columns: `year`, `url`.

### `ErgastF1.target`
Prediction target variable. Columns: `win` (binary: 1 = race winner, 0 = non-winner). Used for ML training.