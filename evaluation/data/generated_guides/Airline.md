# Airline Schema Reference Guide

## Schema Summary
The Airline schema contains 2016 U.S. domestic and international flight operations data with on-time performance metrics, delay analysis, diversions, and cancellations across 83 operational dimensions.

---

## Table Reference

### `Airline.L_AIRLINE_ID`
**Meaning:** Airline carrier master lookup table  
**Synonyms:** Carrier lookup, Airline codes, Carrier codes

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | BIGINT | Unique airline identifier | Airline ID, Carrier ID |
| `Description` | VARCHAR | Airline name with IATA code | Carrier name, Airline name |

**Notable values:** 19031–19035 (sample range); format is numeric ID followed by airline name and 2–3 letter code

---

### `Airline.L_AIRPORT`
**Meaning:** Airport code lookup with city and state  
**Synonyms:** Airport codes, Airport master, Airport reference

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | VARCHAR | 3-character airport code | Airport code, IATA code |
| `Description` | VARCHAR | City, state, and airport name | Airport name, Full airport description |

**Notable values:** "01A", "03A", "04A" (Alaska regional codes); format is "City, State: Airport Name"

---

### `Airline.L_AIRPORT_ID`
**Meaning:** Numeric airport identifier lookup  
**Synonyms:** Airport ID reference, Airport numeric codes

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | BIGINT | Unique numeric airport identifier | Airport ID, Airport numeric code |
| `Description` | VARCHAR | City, state, and airport name | Airport name, Full airport description |

**Notable values:** 10001–10006 (sample range); 5-digit numeric codes

---

### `Airline.L_AIRPORT_SEQ_ID`
**Meaning:** Sequential airport identifier for time-series tracking  
**Synonyms:** Airport sequence ID, Airport seq code

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | BIGINT | Sequential airport identifier | Airport seq ID, Sequence code |
| `Description` | VARCHAR | City, state, and airport name | Airport name, Full airport description |

**Notable values:** 1000101–1000601 (sample range); 7-digit codes combining airport ID with sequence

---

### `Airline.L_CANCELLATION`
**Meaning:** Flight cancellation reason codes  
**Synonyms:** Cancellation codes, Cancellation reasons, Cancel codes

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | VARCHAR | Single-letter cancellation code | Cancellation code, Cancel reason code |
| `Description` | VARCHAR | Reason for cancellation | Cancellation reason, Cancel reason |

**Exact values:** 
- `A` = Carrier
- `B` = Weather
- `C` = National Air System
- `D` = Security

---

### `Airline.L_CITY_MARKET_ID`
**Meaning:** City market identifier lookup  
**Synonyms:** City market codes, Market ID reference

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | BIGINT | Unique city market identifier | City market ID, Market code |
| `Description` | VARCHAR | City and state name | City name, Market name |

**Notable values:** 30001–30006 (sample range); 5-digit numeric codes

---

### `Airline.L_DEPARRBLK`
**Meaning:** Departure/arrival time block lookup (hourly buckets)  
**Synonyms:** Time blocks, Departure time blocks, Arrival time blocks, Hour blocks

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | VARCHAR | 24-hour time range in HHMM-HHMM format | Time block code, Hour block |
| `Description` | VARCHAR | Human-readable time range with AM/PM | Time block description, Hour description |

**Exact values (Code):** 0001-0559, 0600-0659, 0700-0759, 0800-0859, 0900-0959, 1000-1059, 1100-1159, 1200-1259, 1300-1359, 1400-1459, 1500-1559, 1600-1659, 1700-1759, 1800-1859, 1900-1959, 2000-2059, 2100-2159, 2200-2259, 2300-2359

**Exact values (Description):** 12:00AM to 5:59AM, 6:00AM to 6:59AM, 7:00AM to 7:59AM, 8:00AM to 8:59AM, 9:00AM to 9:59AM, 10:00AM to 10:59AM, 11:00AM to 11:59AM, 12:00PM to 12:59PM, 1:00PM to 1:59PM, 2:00PM to 2:59PM, 3:00PM to 3:59PM, 4:00PM to 4:59PM, 5:00PM to 5:59PM, 6:00PM to 6:59PM, 7:00PM to 7:59PM, 8:00PM to 8:59PM, 9:00PM to 9:59PM, 10:00PM to 10:59PM, 11:00PM to 11:59PM

---

### `Airline.L_DISTANCE_GROUP_250`
**Meaning:** Flight distance category lookup (250-mile buckets)  
**Synonyms:** Distance groups, Distance categories, Distance bands

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | BIGINT | Distance group numeric identifier | Distance group code, Distance band |
| `Description` | VARCHAR | Distance range in miles | Distance range, Distance category |

**Exact values (Description):** Less Than 250 Miles, 250-499 Miles, 500-749 Miles, 750-999 Miles, 1000-1249 Miles, 1250-1499 Miles, 1500-1749 Miles, 1750-1999 Miles, 2000-2249 Miles, 2250-2499 Miles, 2500 Miles and Greater

---

### `Airline.L_DIVERSIONS`
**Meaning:** Flight diversion classification lookup  
**Synonyms:** Diversion codes, Diversion types, Diversion categories

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | BIGINT | Diversion type identifier | Diversion code, Diversion type |
| `Description` | VARCHAR | Description of diversion status or count | Diversion description, Diversion status |

**Exact values (Description):** Flight is not Diverted, One Diverted Airport Landing, Two Diverted Airport Landings, Three Diverted Airport Landings, Four Diverted Airport Landings, Five Diverted Airport Landings, Air Return to Origin Airport where the Flight was Ultimately Cancelled

---

### `Airline.L_MONTHS`
**Meaning:** Month name lookup  
**Synonyms:** Month codes, Month reference

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | BIGINT | Month number (1–12) | Month code, Month number |
| `Description` | VARCHAR | Full month name | Month name |

**Exact values (Description):** January, February, March, April, May, June, July, August, September, October, November, December

---

### `Airline.L_ONTIME_DELAY_GROUPS`
**Meaning:** Arrival delay classification lookup  
**Synonyms:** Delay groups, Delay categories, Delay bands

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | BIGINT | Delay group numeric identifier (can be negative) | Delay group code, Delay band |
| `Description` | VARCHAR | Delay range in minutes | Delay range, Delay category |

**Exact values (Description):** Delay < -15 minutes, Delay between -15 and -1 minutes, Delay between 0 and 14 minutes, Delay between 15 to 29 minutes, Delay between 30 to 44 minutes, Delay between 45 to 59 minutes, Delay between 60 to 74 minutes, Delay between 75 to 89 minutes, Delay between 90 to 104 minutes, Delay between 105 to 119 minutes, Delay between 120 to 134 minutes, Delay between 135 to 149 minutes, Delay between 150 to 164 minutes, Delay between 165 to 179 minutes, Delay >= 180 minutes

---

### `Airline.L_QUARTERS`
**Meaning:** Quarter name and date range lookup  
**Synonyms:** Quarter codes, Quarter reference

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | BIGINT | Quarter number (1–4) | Quarter code, Quarter number |
| `Description` | VARCHAR | Quarter name with date range | Quarter name, Quarter range |

**Exact values (Description):** Quarter1:January 1-March 31, Quarter2:April 1-June 30, Quarter3:July 1-September 30, Quarter4:October 1-December 31

---

### `Airline.L_STATE_ABR_AVIATION`
**Meaning:** State and province abbreviation lookup  
**Synonyms:** State codes, State abbreviations, State reference

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | VARCHAR | 2-letter state/province abbreviation | State code, State abbreviation |
| `Description` | VARCHAR | Full state or province name | State name, Province name |

**Notable values:** AB (Alberta, Canada), AK (Alaska), AL (Alabama), AR (Arkansas), AZ (Arizona)

---

### `Airline.L_STATE_FIPS`
**Meaning:** FIPS state code lookup  
**Synonyms:** FIPS codes, State FIPS reference

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | BIGINT | FIPS state numeric code | FIPS code, State FIPS |
| `Description` | VARCHAR | State name | State name |

**Notable values:** 0 (Not Applicable), 1 (Alabama), 2 (Alaska), 4 (Arizona), 5 (Arkansas)

---

### `Airline.L_UNIQUE_CARRIERS`
**Meaning:** Airline carrier code lookup  
**Synonyms:** Carrier codes, Airline codes, Carrier reference

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | VARCHAR | 2–3 character carrier code | Carrier code, Airline code |
| `Description` | VARCHAR | Full airline name | Carrier name, Airline name |

**Notable values:** 02Q (Titan Airways), 04Q (Tradewind Aviation), 05Q (Comlux Aviation, AG), 06Q (Master Top Linhas Aereas Ltd.), 07Q (Flair Airlines Ltd.)

---

### `Airline.L_WEEKDAYS`
**Meaning:** Day of week lookup  
**Synonyms:** Weekday codes, Day codes, Day reference

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | BIGINT | Day of week number (1–7, 9 for Unknown) | Weekday code, Day code |
| `Description` | VARCHAR | Full day name | Day name, Weekday name |

**Exact values (Description):** Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, Unknown

---

### `Airline.L_WORLD_AREA_CODES`
**Meaning:** Geographic world area code lookup  
**Synonyms:** World area codes, Geographic codes, Area codes

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | BIGINT | World area numeric identifier | World area code, Area code |
| `Description` | VARCHAR | Geographic region name | Region name, Area name |

**Notable values:** 1 (Alaska), 2 (Hawaii), 3 (Puerto Rico), 4 (U.S. Virgin Islands), 5 (U.S. Pacific Trust Territories and Possessions)

---

### `Airline.L_YESNO_RESP`
**Meaning:** Boolean yes/no response lookup  
**Synonyms:** Yes/no codes, Boolean codes, Response codes

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | BIGINT | Boolean code (0 or 1) | Boolean code, Response code |
| `Description` | VARCHAR | "Yes" or "No" | Response, Boolean value |

**Exact values:** 0 (No), 1 (Yes)

---

### `Airline.On_Time_On_Time_Performance_2016_1`
**Meaning:** Flight-level operational performance data for 2016 with scheduled/actual times, delays, cancellations, diversions, and delay attribution  
**Synonyms:** Flight operations, Flight performance, Flight data, Operations data

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Year` | BIGINT | Calendar year | Year |
| `Quarter` | BIGINT | Quarter number (1–4) | Quarter |
| `Month` | BIGINT | Month number (1–12) | Month |
| `DayofMonth` | BIGINT | Day of month (1–31) | Day of month, Date |
| `DayOfWeek` | BIGINT | Day of week (1–7) | Weekday, Day of week |
| `FlightDate` | DATE | Flight operation date | Date, Flight date |
| `UniqueCarrier` | VARCHAR | Airline carrier code (2 chars) | Carrier, Airline code |
| `AirlineID` | BIGINT | Numeric airline identifier | Airline ID, Carrier ID |
| `Carrier` | VARCHAR | Airline carrier code (2 chars, duplicate of UniqueCarrier) | Carrier code, Airline code |
| `TailNum` | VARCHAR | Aircraft tail number/registration | Tail number, Aircraft ID, Registration |
| `FlightNum` | BIGINT | Flight number | Flight number, Flight ID |
| `OriginAirportID` | BIGINT | Numeric origin airport identifier | Origin airport ID, Departure airport ID |
| `OriginAirportSeqID` | BIGINT | Sequential origin airport identifier | Origin seq ID, Departure seq ID |
| `OriginCityMarketID` | BIGINT | Origin city market identifier | Origin market ID, Departure market ID |
| `Origin` | VARCHAR | 3-letter origin airport code | Origin code, Departure code |
| `OriginCityName` | VARCHAR | Origin city name | Origin city, Departure city |
| `OriginState` | VARCHAR | Origin state abbreviation | Origin state, Departure state |
| `OriginStateFips` | BIGINT | Origin state FIPS code | Origin FIPS, Departure FIPS |
| `OriginStateName` | VARCHAR | Origin state full name | Origin state name, Departure state name |
| `OriginWac` | BIGINT | Origin world area code | Origin WAC, Departure WAC |
| `DestAirportID` | BIGINT | Numeric destination airport identifier | Destination airport ID, Arrival airport ID |
| `DestAirportSeqID` | BIGINT | Sequential destination airport identifier | Destination seq ID, Arrival seq ID |
| `DestCityMarketID` | BIGINT | Destination city market identifier | Destination market ID, Arrival market ID |
| `Dest` | VARCHAR | 3-letter destination airport code | Destination code, Arrival code |
| `DestCityName` | VARCHAR | Destination city name | Destination city, Arrival city |
| `DestState` | VARCHAR | Destination state abbreviation | Destination state, Arrival state |
| `DestStateFips` | BIGINT | Destination state FIPS code |