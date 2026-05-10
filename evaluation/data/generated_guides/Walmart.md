# Walmart Schema Reference Guide

## Schema Summary
This schema contains Walmart store sales training data linked to weather station observations, enabling analysis of how weather conditions correlate with unit sales across stores and items.

---

## Table Reference

### `Walmart.key`
**Meaning:** Store-to-weather-station mapping table. Associates each Walmart store with its nearest weather observation station.

**Columns:**
| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `store_nbr` | BIGINT | Unique store identifier | store ID, store number |
| `station_nbr` | BIGINT | Weather station identifier | station ID, station number |

**Notable values:** store_nbr ranges 1–33+; station_nbr ranges 1–5+

---

### `Walmart.station`
**Meaning:** Weather station reference table. Lists all weather observation stations.

**Columns:**
| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `station_nbr` | BIGINT | Unique weather station identifier | station ID, station number |

**Notable values:** station_nbr values: 1, 2, 3, 4, 5

---

### `Walmart.train`
**Meaning:** Sales training dataset. Daily unit sales by store and item.

**Columns:**
| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `date` | DATE | Sales date (YYYY-MM-DD format) | transaction date, day |
| `store_nbr` | BIGINT | Store identifier | store ID, store number |
| `item_nbr` | BIGINT | Product/item identifier | product ID, product number, SKU |
| `units` | BIGINT | Number of units sold | quantity, sales volume, sales units |

**Notable values:** date starts 2012-01-01; units can be 0 (no sales)

---

### `Walmart.weather`
**Meaning:** Daily weather observations by station. Contains 20 meteorological measurements per station-date combination.

**Columns:**
| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `station_nbr` | BIGINT | Weather station identifier | station ID, station number |
| `date` | DATE | Observation date (YYYY-MM-DD format) | day |
| `tmax` | BIGINT | Maximum temperature (°F) | high temperature, max temp |
| `tmin` | BIGINT | Minimum temperature (°F) | low temperature, min temp |
| `tavg` | BIGINT | Average temperature (°F) | mean temperature, avg temp |
| `depart` | BIGINT | Temperature departure from normal (°F) | temperature anomaly |
| `dewpoint` | BIGINT | Dew point (°F) | dew point temperature |
| `wetbulb` | BIGINT | Wet bulb temperature (°F) | wet bulb |
| `heat` | BIGINT | Heating degree days | HDD |
| `cool` | BIGINT | Cooling degree days | CDD |
| `sunrise` | TIME | Sunrise time (HH:MM:SS) | sunrise time |
| `sunset` | TIME | Sunset time (HH:MM:SS) | sunset time |
| `codesum` | VARCHAR | Weather condition codes (space-separated) | weather code, condition |
| `snowfall` | DOUBLE | Snowfall (inches) | snow |
| `preciptotal` | DOUBLE | Total precipitation (inches) | precipitation, rainfall, rain |
| `stnpressure` | DOUBLE | Station pressure (inches Hg) | barometric pressure, pressure |
| `sealevel` | DOUBLE | Sea level pressure (inches Hg) | sea level pressure |
| `resultspeed` | DOUBLE | Wind speed (mph) | wind speed, gust speed |
| `resultdir` | BIGINT | Wind direction (degrees 0–360) | wind direction |
| `avgspeed` | DOUBLE | Average wind speed (mph) | average wind speed |

**Notable values:** 
- `codesum` examples: "RA FZFG BR" (rain, freezing fog, mist), empty string (clear)
- `snowfall`, `preciptotal`, `stnpressure`, `sealevel`, `resultspeed`, `avgspeed` may contain NaN
- `depart`, `dewpoint`, `wetbulb`, `heat`, `cool`, `sunrise`, `sunset` may contain NULL/<NA>

---

## Join Paths

**Store to Weather Station:**
```sql
Walmart.train t
JOIN Walmart.key k ON t.store_nbr = k.store_nbr
JOIN Walmart.weather w ON k.station_nbr = w.station_nbr AND t.date = w.date
```

**Direct Station Reference:**
```sql
Walmart.weather w
JOIN Walmart.station s ON w.station_nbr = s.station_nbr
```

**Store-Station Mapping Only:**
```sql
Walmart.key k
JOIN Walmart.station s ON k.station_nbr = s.station_nbr
```

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| store | `Walmart.train.store_nbr` or `Walmart.key.store_nbr` |
| station | `Walmart.weather.station_nbr` or `Walmart.station.station_nbr` |
| sales | `Walmart.train.units` |
| units sold | `Walmart.train.units` |
| product | `Walmart.train.item_nbr` |
| item | `Walmart.train.item_nbr` |
| date | `Walmart.train.date` or `Walmart.weather.date` |
| temperature | `Walmart.weather.tavg`, `tmax`, or `tmin` |
| high temp | `Walmart.weather.tmax` |
| low temp | `Walmart.weather.tmin` |
| rain | `Walmart.weather.preciptotal` |
| precipitation | `Walmart.weather.preciptotal` |
| snow | `Walmart.weather.snowfall` |
| wind | `Walmart.weather.resultspeed` or `avgspeed` |
| pressure | `Walmart.weather.stnpressure` or `sealevel` |
| weather condition | `Walmart.weather.codesum` |
| heating degree days | `Walmart.weather.heat` |
| cooling degree days | `Walmart.weather.cool` |