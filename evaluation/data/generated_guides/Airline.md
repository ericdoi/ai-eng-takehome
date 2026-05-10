# Airline Schema Reference Guide

## Schema Summary
This schema contains 2016 U.S. domestic flight operations data with 83 performance metrics per flight, supplemented by 16 lookup tables for carrier, airport, and delay classifications.

---

## Join Paths

**Flight to Carrier Details:**
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_UNIQUE_CARRIERS c ON f.UniqueCarrier = c.Code
```

**Flight to Origin Airport:**
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_AIRPORT_ID a ON f.OriginAirportID = a.Code
```

**Flight to Destination Airport:**
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_AIRPORT_ID a ON f.DestAirportID = a.Code
```

**Flight to Cancellation Reason:**
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
LEFT JOIN Airline.L_CANCELLATION c ON f.CancellationCode = c.Code
```

**Flight to Departure Time Block:**
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_DEPARRBLK d ON f.DepTimeBlk = d.Code
```

**Flight to Delay Group Classification:**
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_ONTIME_DELAY_GROUPS dg ON f.ArrivalDelayGroups = dg.Code
```

**Flight to Distance Group:**
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_DISTANCE_GROUP_250 dg ON f.DistanceGroup = dg.Code
```

**Flight to Day of Week:**
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_WEEKDAYS w ON f.DayOfWeek = w.Code
```

---

## Business Rules as SQL

**Rule: Completed Flight (has actual departure and arrival)**
```sql
WHERE DepTime IS NOT NULL AND ArrTime IS NOT NULL
```

**Rule: On-Time Flight (industry standard)**
```sql
WHERE ArrDelayMinutes <= 15
```

**Rule: Minor Delay (excluded from delay analysis)**
```sql
WHERE ArrDelayMinutes < 15
```

**Rule: Severe Delay (3+ hours)**
```sql
WHERE ArrDelayMinutes >= 180
```

**Rule: Exclude Weather Delays from Carrier Performance**
```sql
WHERE WeatherDelay IS NULL OR WeatherDelay = 0
```

**Rule: Thin Route (fewer than 50 annual flights)**
```sql
HAVING COUNT(*) < 50
```

**Rule: Cancelled Flight (excluded from on-time performance)**
```sql
WHERE Cancelled = 1
```

**Rule: Diverted Flight (counts as completed on original route)**
```sql
WHERE Diverted = 1
```

**Rule: Exclude January and September (reset months)**
```sql
WHERE Month NOT IN (1, 9)
```

**Rule: Q4 Holiday Period (October-December)**
```sql
WHERE Quarter = 4
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| flight delay | `ArrDelayMinutes` or `DepDelayMinutes` |
| on-time performance | `WHERE ArrDelayMinutes <= 15` |
| cancellation reason | `Airline.L_CANCELLATION.Description` via `CancellationCode` |
| carrier | `UniqueCarrier` (2-letter code) or `Airline.L_UNIQUE_CARRIERS.Description` |
| airport | `Origin` / `Dest` (3-letter codes) or `Airline.L_AIRPORT_ID.Description` |
| departure block | `DepTimeBlk` or `Airline.L_DEPARRBLK.Description` |
| arrival block | `ArrTimeBlk` or `Airline.L_DEPARRBLK.Description` |
| distance category | `DistanceGroup` or `Airline.L_DISTANCE_GROUP_250.Description` |
| delay type | `DepartureDelayGroups` / `ArrivalDelayGroups` or `Airline.L_ONTIME_DELAY_GROUPS.Description` |
| day of week | `DayOfWeek` or `Airline.L_WEEKDAYS.Description` |
| quarter | `Quarter` or `Airline.L_QUARTERS.Description` |
| month | `Month` or `Airline.L_MONTHS.Description` |
| state | `OriginState` / `DestState` or `Airline.L_STATE_ABR_AVIATION.Description` |
| weather impact | `WeatherDelay` (NULL = no weather delay) |
| carrier delay | `CarrierDelay` |
| NAS delay | `NASDelay` (National Air System) |
| security delay | `SecurityDelay` |
| late aircraft delay | `LateAircraftDelay` |

---

## Table Reference

### `Airline.On_Time_On_Time_Performance_2016_1`
**Meaning:** Individual flight records with operational and delay metrics.

| Column | Semantics |
|--------|-----------|
| `DepTime` | Actual departure time (HHMM format, 4-digit). NULL if cancelled. |
| `ArrTime` | Actual arrival time (HHMM format, 4-digit). NULL if cancelled. |
| `DepDelayMinutes` | Actual departure delay in minutes (can be negative for early departures). |
| `ArrDelayMinutes` | Actual arrival delay in minutes (can be negative for early arrivals). |
| `DepDel15` | Binary flag: 1 if departure delay ≥ 15 minutes, 0 otherwise. |
| `ArrDel15` | Binary flag: 1 if arrival delay ≥ 15 minutes, 0 otherwise. |
| `DepartureDelayGroups` | Categorical delay bucket; join to `Airline.L_ONTIME_DELAY_GROUPS` for description. |
| `ArrivalDelayGroups` | Categorical delay bucket; join to `Airline.L_ONTIME_DELAY_GROUPS` for description. |
| `DepTimeBlk` | Departure time block (e.g., "0700-0759"); join to `Airline.L_DEPARRBLK` for human-readable form. |
| `ArrTimeBlk` | Arrival time block; join to `Airline.L_DEPARRBLK` for human-readable form. |
| `Cancelled` | Binary: 1 if flight cancelled, 0 otherwise. |
| `CancellationCode` | Single character (A, B, C, D); join to `Airline.L_CANCELLATION` for reason. Values: A=Carrier, B=Weather, C=National Air System, D=Security. |
| `Diverted` | Binary: 1 if flight diverted to alternate airport, 0 otherwise. |
| `DistanceGroup` | Distance category code; join to `Airline.L_DISTANCE_GROUP_250` for range (e.g., "500-749 Miles"). |
| `CarrierDelay` | Minutes of delay attributed to carrier (NULL if no carrier delay). |
| `WeatherDelay` | Minutes of delay attributed to weather (NULL = no weather delay, not unknown). |
| `NASDelay` | Minutes of delay attributed to National Air System. |
| `SecurityDelay` | Minutes of delay attributed to security. |
| `LateAircraftDelay` | Minutes of delay from previous flight's late arrival. |
| `DivAirportLandings` | Count of diversion airports (0 if not diverted). |
| `Div1Airport`, `Div2Airport` | 3-letter codes for first and second diversion airports. |
| `UniqueCarrier` | 2-letter carrier code (AA, AS, B6, DL, EV, F9, HA, NK, OO, UA, VX, WN). |
| `OriginAirportID`, `DestAirportID` | Numeric airport identifiers; join to `Airline.L_AIRPORT_ID`. |
| `OriginCityMarketID`, `DestCityMarketID` | City market identifiers; join to `Airline.L_CITY_MARKET_ID`. |
| `OriginStateFips`, `DestStateFips` | FIPS state codes; join to `Airline.L_STATE_FIPS`. |
| `OriginWac`, `DestWac` | World Area Codes; join to `Airline.L_WORLD_AREA_CODES`. |
| `CRSDepTime`, `CRSArrTime` | Scheduled departure/arrival times (HHMM format). |
| `CRSElapsedTime` | Scheduled flight duration in minutes. |
| `ActualElapsedTime` | Actual flight duration in minutes (gate-to-gate). |
| `AirTime` | Time in air (wheels-off to wheels-on) in minutes. |
| `TaxiOut`, `TaxiIn` | Ground time before departure and after landing in minutes. |
| `Flights` | Count of flights in this record (typically 1.0). |
| `Distance` | Flight distance in miles. |

---

### `Airline.L_UNIQUE_CARRIERS`
**Meaning:** Airline carrier codes and full legal names.

| Column | Values |
|--------|--------|
| `Code` | 2-letter IATA codes: AA, AS, B6, DL, EV, F9, HA, NK, OO, UA, VX, WN |

---

### `Airline.L_CANCELLATION`
**Meaning:** Reasons for flight cancellation.

| Column | Values |
|--------|--------|
| `Code` | A, B, C, D |
| `Description` | Carrier, Weather, National Air System, Security |

---

### `Airline.L_ONTIME_DELAY_GROUPS`
**Meaning:** Categorical delay buckets for standardized reporting.

| Column | Values |
|--------|--------|
| `Code` | -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 |
| `Description` | Delay < -15 minutes, Delay between -15 and -1 minutes, Delay between 0 and 14 minutes, Delay between 15 to 29 minutes, ... Delay >= 180 minutes |

---

### `Airline.L_DEPARRBLK`
**Meaning:** Hourly departure/arrival time blocks for aggregation.

| Column | Values |
|--------|--------|
| `Code` | 0001-0559, 0600-0659, 0700-0759, ..., 2300-2359 |
| `Description` | 12:00AM to 5:59AM, 6:00AM to 6:59AM, ..., 11:00PM to 11:59PM |

---

### `Airline.L_DISTANCE_GROUP_250`
**Meaning:** Distance categories for fair performance comparison.

| Column | Values |
|--------|--------|
| `Code` | 1–11 (numeric) |
| `Description` | Less Than 250 Miles, 250-499 Miles, 500-749 Miles, 750-999 Miles, 1000-1249 Miles, 1250-1499 Miles, 1500-1749 Miles, 1750-1999 Miles, 2000-2249 Miles, 2250-2499 Miles, 2500 Miles and Greater |

---

### `Airline.L_AIRPORT_ID`
**Meaning:** Numeric airport identifiers with city and state.

| Column | Semantics |
|--------|-----------|
| `Code` | Numeric ID (e.g., 10001 for Afognak Lake, AK). |
| `Description` | Format: "City, State: Airport Name" |

---

### `Airline.L_AIRPORT`
**Meaning:** Alphanumeric airport codes (legacy format).

| Column | Semantics |
|--------|-----------|
| `Code` | 3-character code (e.g., "01A"). |

---

### `Airline.L_AIRPORT_SEQ_ID`
**Meaning:** Sequential airport identifiers for time-series tracking.

| Column | Semantics |
|--------|-----------|
| `Code` | Numeric sequence ID (e.g., 1000101). |

---

### `Airline.L_CITY_MARKET_ID`
**Meaning:** City market identifiers for route analysis.

| Column | Semantics |
|--------|-----------|
| `Code` | Numeric market ID (e.g., 30001). |
| `Description` | Format: "City, State" |

---

### `Airline.L_WEEKDAYS`
**Meaning:** Day-of-week classifications.

| Column | Values |
|--------|--------|
| `Code` | 1–7 (Monday–Sunday) |
| `Description` | Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, Unknown |

---

### `Airline.L_MONTHS`
**Meaning:** Month identifiers.

| Column | Values |
|--------|--------|
| `Code` | 1–12 |
| `Description` | January, February, ..., December |

---

### `Airline.L_QUARTERS`
**Meaning:** Quarterly groupings.

| Column | Values |
|--------|--------|
| `Code` | 1–4 |
| `Description` | Quarter1:January 1-March 31, Quarter2:April 1-June 30, Quarter3:July 1-September 30, Quarter4:October 1-December 31 |

---

### `Airline.L_STATE_ABR_AVIATION`
**Meaning:** State and province abbreviations.

| Column | Semantics |
|--------|-----------|
| `Code` | 2-letter abbreviation (e.g., "AK", "TX", "AB" for Alberta). |
| `Description` | Full state/province name. |

---

### `Airline.L_STATE_FIPS`
**Meaning:** FIPS state codes for federal reporting.

| Column | Semantics |
|--------|-----------|
| `Code` | Numeric FIPS code (0 = Not Applicable, 1 = Alabama, 2 = Alaska, etc.). |

---

### `Airline.L_WORLD_AREA_CODES`
**Meaning:** Geographic regions for international/territorial classification.

| Column | Values |
|--------|--------|
| `Code` | 1–5 (numeric) |
| `Description` | Alaska, Hawaii, Puerto Rico, U.S. Virgin Islands, U.S. Pacific Trust Territories and Possessions |

---

### `Airline.L_YESNO_RESP`
**Meaning:** Binary yes/no responses.

| Column | Values |
|--------|--------|
| `Code` | 0, 1 |
| `Description` | No, Yes |

---

### `Airline.L_AIRLINE_ID`
**Meaning:** Legacy airline identifiers (historical reference).

| Column | Semantics |
|--------|-----------|
| `Code` | Numeric airline ID. |
| `Description` | Format: "Airline Legal Name: IATA Code" |