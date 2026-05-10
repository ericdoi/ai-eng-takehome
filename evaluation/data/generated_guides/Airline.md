# Airline Operations Analytics — SQL Reference Guide

## Schema Summary

This schema contains 2016 U.S. domestic airline flight operations data with 83 performance metrics per flight (delays, cancellations, diversions, weather impact) plus 16 lookup tables for carrier, airport, time period, and delay classification codes.

---

## Join Paths

### Flight Performance to Carrier Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_UNIQUE_CARRIERS c ON f.UniqueCarrier = c.Code
```
**[OPTIONAL — display only]** Use to show carrier full name; for filtering/grouping use `f.UniqueCarrier` directly.

### Flight Performance to Origin Airport Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_AIRPORT_ID oa ON f.OriginAirportID = oa.Code
```
**[OPTIONAL — display only]** Use to show origin airport full name; for filtering/grouping use `f.Origin` or `f.OriginAirportID` directly.

### Flight Performance to Destination Airport Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_AIRPORT_ID da ON f.DestAirportID = da.Code
```
**[OPTIONAL — display only]** Use to show destination airport full name; for filtering/grouping use `f.Dest` or `f.DestAirportID` directly.

### Flight Performance to Departure Delay Group Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_ONTIME_DELAY_GROUPS dg ON f.DepartureDelayGroups = dg.Code
```
**[OPTIONAL — display only]** Use to show human-readable delay range; for filtering/grouping use `f.DepartureDelayGroups` directly.

### Flight Performance to Arrival Delay Group Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_ONTIME_DELAY_GROUPS ag ON f.ArrivalDelayGroups = ag.Code
```
**[OPTIONAL — display only]** Use to show human-readable delay range; for filtering/grouping use `f.ArrivalDelayGroups` directly.

### Flight Performance to Cancellation Reason Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_CANCELLATION cc ON f.CancellationCode = cc.Code
```
**[OPTIONAL — display only]** Use to show cancellation reason; for filtering/grouping use `f.CancellationCode` directly.

### Flight Performance to Departure Time Block Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_DEPARRBLK dtb ON f.DepTimeBlk = dtb.Code
```
**[OPTIONAL — display only]** Use to show human-readable time window; for filtering/grouping use `f.DepTimeBlk` directly.

### Flight Performance to Arrival Time Block Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_DEPARRBLK atb ON f.ArrTimeBlk = atb.Code
```
**[OPTIONAL — display only]** Use to show human-readable time window; for filtering/grouping use `f.ArrTimeBlk` directly.

### Flight Performance to Distance Group Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_DISTANCE_GROUP_250 dg ON f.DistanceGroup = dg.Code
```
**[OPTIONAL — display only]** Use to show distance range; for filtering/grouping use `f.DistanceGroup` directly.

### Flight Performance to Month Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_MONTHS m ON f.Month = m.Code
```
**[OPTIONAL — display only]** Use to show month name; for filtering/grouping use `f.Month` directly.

### Flight Performance to Weekday Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_WEEKDAYS w ON f.DayOfWeek = w.Code
```
**[OPTIONAL — display only]** Use to show weekday name; for filtering/grouping use `f.DayOfWeek` directly.

### Flight Performance to Quarter Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_QUARTERS q ON f.Quarter = q.Code
```
**[OPTIONAL — display only]** Use to show quarter description; for filtering/grouping use `f.Quarter` directly.

### Flight Performance to Origin State Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_STATE_ABR_AVIATION os ON f.OriginState = os.Code
```
**[OPTIONAL — display only]** Use to show origin state full name; for filtering/grouping use `f.OriginState` or `f.OriginStateName` directly.

### Flight Performance to Destination State Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_STATE_ABR_AVIATION ds ON f.DestState = ds.Code
```
**[OPTIONAL — display only]** Use to show destination state full name; for filtering/grouping use `f.DestState` or `f.DestStateName` directly.

### Flight Performance to Diversion Count Lookup
```sql
FROM Airline.On_Time_On_Time_Performance_2016_1 f
JOIN Airline.L_DIVERSIONS div ON f.DivAirportLandings = div.Code
```
**[OPTIONAL — display only]** Use to show diversion description; for filtering/grouping use `f.DivAirportLandings` directly.

---

## Business Rules as SQL

### IDENTIFY Completed Flights
```sql
WHERE f.DepTime IS NOT NULL AND f.ArrTime IS NOT NULL
```
Rows matching this condition ARE completed flights (actual departure and arrival times recorded).

### EXCLUDE Cancelled Flights from On-Time Performance
```sql
WHERE f.Cancelled = 0
```
To filter cancelled flights OUT of on-time performance analysis, use this condition. Cancelled flights (where `f.Cancelled = 1`) are excluded from on-time metrics but included in total scheduled flight counts.

### IDENTIFY On-Time Arrivals
```sql
WHERE f.ArrDelayMinutes <= 15 AND f.ArrDelayMinutes IS NOT NULL
```
Rows matching this condition ARE on-time (arrived within 15 minutes of scheduled arrival time).

### IDENTIFY Minor Delays
```sql
WHERE f.ArrDelayMinutes > 0 AND f.ArrDelayMinutes < 15
```
Rows matching this condition ARE minor delays (should not be included in delay analysis per business rules).

### IDENTIFY Severe Delays
```sql
WHERE f.ArrDelayMinutes >= 180
```
Rows matching this condition ARE severe delays (3+ hours; must be reported separately with root cause analysis).

### EXCLUDE Weather Delays from Carrier Performance
```sql
WHERE f.WeatherDelay IS NULL OR f.WeatherDelay = 0
```
To filter weather delays OUT of carrier performance metrics, use this condition. A NULL `WeatherDelay` value means no weather delay occurred (not unknown).

### IDENTIFY Diverted Flights
```sql
WHERE f.Diverted = 1
```
Rows matching this condition ARE diverted flights. Diverted flights count as completed for the original route, NOT the diverted destination.

### IDENTIFY Thin Routes
```sql
WHERE (SELECT COUNT(*) FROM Airline.On_Time_On_Time_Performance_2016_1 f2 
       WHERE f2.OriginAirportID = f.OriginAirportID 
       AND f2.DestAirportID = f.DestAirportID 
       AND f2.Year = 2016) < 50
```
Rows matching this condition ARE on thin routes (fewer than 50 annual flights). Aggregate these regionally for meaningful analysis.

### IDENTIFY Reset Months (Exclude from Trend Analysis)
```sql
WHERE f.Month IN (1, 9)
```
Rows matching this condition ARE in reset months (January and September). Exclude from trend analysis as they show artificial patterns.

### IDENTIFY Q4 Holiday Surge Period
```sql
WHERE f.Quarter = 4
```
Rows matching this condition ARE in Q4 (October-December). Weight metrics by normal seasonal patterns when comparing to other quarters.

### On-Time Performance Rate
```sql
on_time_rate = COUNT(CASE WHEN f.ArrDelayMinutes <= 15 AND f.ArrDelayMinutes IS NOT NULL THEN 1 END) 
               / COUNT(CASE WHEN f.Cancelled = 0 THEN 1 END)
```
Numerator: completed flights arriving on-time (≤15 min delay). Denominator: all non-cancelled flights.

### Carrier Delay Attribution
```sql
carrier_delay_minutes = COALESCE(f.CarrierDelay, 0)
```
Use `CarrierDelay` column for carrier-attributable delay. Weather delays (`WeatherDelay`), NAS delays (`NASDelay`), security delays (`SecurityDelay`), and late aircraft delays (`LateAircraftDelay`) are NOT carrier responsibility.

---

## Synonym Glossary

| Question Term | Schema Identifier |
|---|---|
| on-time arrival | `ArrDelayMinutes <= 15` |
| late arrival | `ArrDelayMinutes > 15` |
| departure delay | `DepDelayMinutes` |
| arrival delay | `ArrDelayMinutes` |
| flight cancelled | `Cancelled = 1` |
| flight diverted | `Diverted = 1` |
| carrier | `UniqueCarrier` |
| airline | `UniqueCarrier` |
| origin airport | `Origin` or `OriginAirportID` |
| destination airport | `Dest` or `DestAirportID` |
| scheduled departure | `CRSDepTime` |
| actual departure | `DepTime` |
| scheduled arrival | `CRSArrTime` |
| actual arrival | `ArrTime` |
| flight distance | `Distance` |
| distance group | `DistanceGroup` (use `L_DISTANCE_GROUP_250` for ranges) |
| weather delay | `WeatherDelay` |
| NAS delay | `NASDelay` |
| security delay | `SecurityDelay` |
| late aircraft delay | `LateAircraftDelay` |
| carrier delay | `CarrierDelay` |
| cancellation reason | `CancellationCode` (join `L_CANCELLATION` for description) |
| diversion count | `DivAirportLandings` |
| flight time | `ActualElapsedTime` |
| scheduled flight time | `CRSElapsedTime` |
| air time | `AirTime` |
| taxi out | `TaxiOut` |
| taxi in | `TaxiIn` |
| day of week | `DayOfWeek` (join `L_WEEKDAYS` for name) |
| month | `Month` (join `L_MONTHS` for name) |
| quarter | `Quarter` (join `L_QUARTERS` for description) |
| departure time block | `DepTimeBlk` (join `L_DEPARRBLK` for human-readable range) |
| arrival time block | `ArrTimeBlk` (join `L_DEPARRBLK` for human-readable range) |

---

## Table Reference

### `Airline.On_Time_On_Time_Performance_2016_1`
**Meaning:** Individual flight records for 2016 with 83 operational and delay metrics.  
**Synonyms:** flight operations, flight performance, flight data.

| Column | Semantics |
|---|---|
| `Year` | Always 2016 in this dataset. |
| `Quarter` | 1–4; join `L_QUARTERS` for date range descriptions. |
| `Month` | 1–12; join `L_MONTHS` for month names. |
| `DayOfWeek` | 1–7 (Monday–Sunday); join `L_WEEKDAYS` for names. |
| `FlightDate` | DATE of flight operation. |
| `UniqueCarrier` | 2-letter carrier code (AA, AS, B6, DL, EV, F9, HA, NK, OO, UA, VX, WN). Use directly for grouping; join `L_UNIQUE_CARRIERS` for full name. |
| `Carrier` | Duplicate of `UniqueCarrier`; use `UniqueCarrier`. |
| `Origin` | 3-letter IATA airport code (origin). Use directly for grouping; join `L_AIRPORT_ID` on `OriginAirportID` for full name. |
| `Dest` | 3-letter IATA airport code (destination). Use directly for grouping; join `L_AIRPORT_ID` on `DestAirportID` for full name. |
| `OriginAirportID` | Numeric airport identifier; join `L_AIRPORT_ID` for full airport name. |
| `DestAirportID` | Numeric airport identifier; join `L_AIRPORT_ID` for full airport name. |
| `OriginState` | 2-letter state abbreviation; join `L_STATE_ABR_AVIATION` for full state name. |
| `DestState` | 2-letter state abbreviation; join `L_STATE_ABR_AVIATION` for full state name. |
| `OriginStateName` | Full state name (e.g., "Texas"). Use directly; no join needed. |
| `DestStateName` | Full state name (e.g., "Texas"). Use directly; no join needed. |
| `OriginWac` | World Area Code (origin); join `L_WORLD_AREA_CODES` for region name. |
| `DestWac` | World Area Code (destination); join `L_WORLD_AREA_CODES` for region name. |
| `CRSDepTime` | Scheduled departure time (HHMM format, 0–2359). |
| `DepTime` | Actual departure time (HHMM format, 0–2359). NULL if cancelled. |
| `DepDelay` | Departure delay in minutes (can be negative for early departures). |
| `DepDelayMinutes` | Departure delay in minutes (same as `DepDelay`). |
| `DepDel15` | Binary flag: 1 if departure delayed ≥15 minutes, 0 otherwise. |
| `DepartureDelayGroups` | Categorical delay bucket; join `L_ONTIME_DELAY_GROUPS` for range description. |
| `DepTimeBlk` | Departure time block (e.g., "0700-0759"); join `L_DEPARRBLK` for human-readable range. |
| `CRSArrTime` | Scheduled arrival time (HHMM format, 0–2359). |
| `ArrTime` | Actual arrival time (HHMM format, 0–2359). NULL if cancelled or diverted. |
| `ArrDelay` | Arrival delay in minutes (can be negative for early arrivals). |
| `ArrDelayMinutes` | Arrival delay in minutes (same as `ArrDelay`). |
| `ArrDel15` | Binary flag: 1 if arrival delayed ≥15 minutes, 0 otherwise. |
| `ArrivalDelayGroups` | Categorical delay bucket; join `L_ONTIME_DELAY_GROUPS` for range description. |
| `ArrTimeBlk` | Arrival time block (e.g., "1400-1459"); join `L_DEPARRBLK` for human-readable range. |
| `Cancelled` | Binary flag: 1 if flight cancelled, 0 otherwise. |
| `CancellationCode` | Single letter (A, B, C, or NULL); join `L_CANCELLATION` for reason. A=Carrier, B=Weather, C=NAS. |
| `Diverted` | Binary flag: 1 if flight diverted, 0 otherwise. |
| `CRSElapsedTime` | Scheduled flight duration in minutes. |
| `ActualElapsedTime` | Actual flight duration in minutes (gate-to-gate). |
| `AirTime` | Actual air time in minutes (wheels-off to wheels-on). |
| `Distance` | Flight distance in miles. |
| `DistanceGroup` | Distance bucket (1–11); join `L_DISTANCE_GROUP_250` for range (e.g., "Less Than 250 Miles"). |
| `CarrierDelay` | Delay minutes attributable to carrier. NULL = 0. |
| `WeatherDelay` | Delay minutes attributable to weather. NULL = 0 (not unknown). |
| `NASDelay` | Delay minutes attributable to National Air System. NULL = 0. |
| `SecurityDelay` | Delay minutes attributable to security. NULL = 0. |
| `LateAircraftDelay` | Delay minutes attributable to late aircraft arrival. NULL = 0. |
| `Diverted` | Binary flag: 1 if flight diverted to alternate airport, 0 otherwise. |
| `DivAirportLandings` | Count of diversion airport landings (0–5+); join `L_DIVERSIONS` for description. |
| `Div1Airport` | 3-letter IATA code of first diversion airport (if any). |
| `Div1AirportID` | Numeric ID of first diversion airport. |
| `Div2Airport` | 3-letter IATA code of second diversion airport (if any). Values: BOS, DTW, LAS, MSP, SEA. |
| `Div2AirportID` | Numeric ID of second diversion airport. |

### `Airline.L_UNIQUE_CARRIERS`
**Meaning:** Lookup table mapping 2-letter carrier codes to full airline names.  
**Synonyms:** carrier names, airline names.

| Column | Semantics |
|---|---|
| `Code` | 2-letter carrier code (AA, AS, B6, DL, EV, F9, HA, NK, OO, UA, VX, WN). |
| `Description` | Full airline name (e.g., "American Airlines Inc."). |

### `Airline.L_AIRPORT_ID`
**Meaning:** Lookup table mapping numeric airport IDs to full airport names and locations.  
**Synonyms:** airport names, airport codes.

| Column | Semantics |
|---|---|
| `Code` | Numeric airport ID. |
| `Description` | Full airport name with city and state (e.g., "Dallas/Fort Worth, TX: Dallas/Fort Worth International Airport"). |

### `Airline.L_ONTIME_DELAY_GROUPS`
**Meaning:** Lookup table mapping delay group codes to human-readable delay ranges.  
**Synonyms:** delay categories, delay buckets.

| Column | Semantics |
|---|---|
| `Code` | Numeric or negative code representing delay bucket. Values: -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12. |
| `Description` | Human-readable delay range (e.g., "Delay between 0 and 14 minutes", "Delay >= 180 minutes"). |

### `Airline.L_DEPARRBLK`
**Meaning:** Lookup table mapping departure/arrival time block codes to human-readable time windows.  
**Synonyms:** time blocks, time windows.

| Column | Semantics |
|---|---|
| `Code` | Time block code (e.g., "0700-0759", "1200-1259"). |
| `Description` | Human-readable time range (e.g., "7:00AM to 7:59AM", "12:00PM to 12:59PM"). |

### `Airline.L_DISTANCE_GROUP_250`
**Meaning:** Lookup table mapping distance group codes to distance ranges in miles.  
**Synonyms:** distance ranges, distance buckets.

| Column | Semantics |
|---|---|
| `Code` | Numeric distance group (1–11). |
| `Description` | Distance range (e.g., "Less Than 250 Miles", "1000-1249 Miles", "2500 Miles and Greater"). |

### `Airline.L_CANCELLATION`
**Meaning:** Lookup table mapping cancellation codes to cancellation reasons.  
**Synonyms:** cancellation reasons, cancellation codes.

| Column | Semantics |
|---|---|
| `Code` | Single letter: A (Carrier), B (Weather), C (NAS), D (Security). |
| `Description` | Cancellation reason (Carrier, Weather, National Air System, Security). |

### `Airline.L_MONTHS`
**Meaning:** Lookup table mapping month numbers to month names.  
**Synonyms:** month names.

| Column | Semantics |
|---|---|
| `Code` | Month number (1–12). |
| `Description` | Month name (January, February, ..., December). |

### `Airline.L_WEEKDAYS`
**Meaning:** Lookup table mapping day-of-week numbers to weekday names.  
**Synonyms:** day names, weekday names.

| Column | Semantics |
|---|---|
| `Code` | Day of week (1–7): 1=Monday, 2=Tuesday, ..., 7=Sunday. |
| `Description` | Weekday name (Monday, Tuesday, ..., Sunday). |

### `Airline.L_QUARTERS`
**Meaning:** Lookup table mapping quarter numbers to quarter descriptions with date ranges.  
**Synonyms:** quarter names, quarter ranges.

| Column | Semantics |
|---|---|
| `Code` | Quarter number (1–4). |
| `Description` | Quarter description with date range (e.g., "Quarter1:January 1-March 31"). |

### `Airline.L_STATE_ABR_AVIATION`
**Meaning:** Lookup table mapping 2-letter state abbreviations to full state names.  
**Synonyms:** state names, state codes.

| Column | Semantics |
|---|---|
| `Code` | 2-letter state abbreviation (AK, AL, AR, AZ, ..., WY) or Canadian province (AB, BC, ...). |
| `Description` | Full state or province name (Alaska, Alabama, ..., Wyoming). |

### `Airline.L_WORLD_AREA_CODES`
**Meaning:** Lookup table mapping numeric world area codes to geographic region names.  
**Synonyms:** world regions, geographic areas.

| Column | Semantics |
|---|---|
| `Code` | Numeric world area code (1–11+). |
| `Description` | Geographic region (Alaska, Hawaii, Puerto Rico, U.S. Virgin Islands, etc.). |

### `Airline.L_DIVERSIONS`
**Meaning:** Lookup table mapping diversion landing counts to diversion descriptions.  
**Synonyms:** diversion types, diversion categories.

| Column | Semantics |
|---|---|
| `Code` | Numeric count (0–5+). |
| `Description` | Diversion description (e.g., "Flight is not Diverted", "One Diverted Airport Landing", "Five Diverted Airport Landings"). |

### `Airline.L_YESNO_RESP`
**Meaning:** Lookup table for binary yes/no responses.  
**Synonyms:** boolean flags, yes/no codes.

| Column | Semantics |
|---|---|
| `Code` | Binary code: 0 (No), 1 (Yes). |
| `Description` | Yes or No. |

### `Airline.L_AIRLINE_ID`
**Meaning:** Lookup table mapping numeric airline IDs to airline codes and names.  
**Synonyms:** airline identifiers, airline codes.

| Column | Semantics |
|---|---|
| `Code` | Numeric airline ID. |
| `Description` | Airline code and name (e.g., "Mackey International Inc.: MAC"). |

### `Airline.L_AIRPORT`
**Meaning:** Lookup table mapping 3-letter airport codes to full airport names and locations.  
**Synonyms:** airport codes, airport names.

| Column | Semantics |
|---|---|
| `Code` | 3-letter airport code (01A, 03A, 04A, ...). |
| `Description` | Full airport name with city and state (e.g., "Afognak Lake, AK: Afognak Lake Airport"). |

### `Airline.L_AIRPORT_SEQ_ID`
**Meaning:** Lookup table mapping sequential airport IDs to airport names.  
**Synonyms:** airport sequence identifiers.

| Column | Semantics |
|---|---|
| `Code` | Numeric sequential airport ID. |
| `Description` | Full airport name with city and state. |

### `Airline.L_CITY_MARKET_ID`
**Meaning:** Lookup table mapping city market IDs to city names.  
**Synonyms:** city identifiers, market codes.

| Column | Semantics |
|---|---|
| `Code` | Numeric city market ID. |
| `Description` | City name with state (e.g., "Afognak Lake, AK"). |

### `Airline.L_STATE_FIPS`
**Meaning:** Lookup table mapping FIPS state codes to state names.  
**Synonyms:** FIPS codes, state FIPS identifiers.

| Column | Semantics |
|---|---|
| `Code` | Numeric FIPS state code (0–56). |
| `Description` | State name (Alabama, Alaska, ..., Wyoming) or "Not Applicable". |