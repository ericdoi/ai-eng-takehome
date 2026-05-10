# Walmart Schema Reference Guide

## Schema Summary
This schema contains Walmart store sales training data linked to weather observations by geographic station, enabling analysis of unit sales across stores and dates with corresponding weather conditions.

## Join Paths

**Store sales with weather data:**
```sql
FROM Walmart.train t
JOIN Walmart.key k ON t.store_nbr = k.store_nbr
JOIN Walmart.weather w ON k.station_nbr = w.station_nbr AND t.date = w.date
```

**All stations:**
```sql
FROM Walmart.station s
LEFT JOIN Walmart.key k ON s.station_nbr = k.station_nbr
```

**Weather for a specific store:**
```sql
FROM Walmart.train t
JOIN Walmart.key k ON t.store_nbr = k.store_nbr
JOIN Walmart.weather w ON k.station_nbr = w.station_nbr AND t.date = w.date
WHERE t.store_nbr = <store_nbr>
```

## Table Reference

### `Walmart.key`
Maps stores to weather stations. Many stores can share one station.
- `store_nbr` – Store identifier
- `station_nbr` – Weather station identifier (foreign key to `Walmart.station`)

### `Walmart.station`
Weather station identifiers.
- `station_nbr` – Unique station identifier

### `Walmart.train`
Daily unit sales by store and item.
- `date` – Sales date (DATE)
- `store_nbr` – Store identifier
- `item_nbr` – Product/item identifier
- `units` – Units sold (BIGINT, can be 0)

### `Walmart.weather`
Daily weather observations by station.
- `station_nbr` – Weather station identifier
- `date` – Observation date (DATE)
- **Temperature metrics (BIGINT):** `tmax`, `tmin`, `tavg`, `depart`, `dewpoint`, `wetbulb`
- **Degree days (BIGINT):** `heat`, `cool` (heating/cooling degree days)
- **Time fields (TIME):** `sunrise`, `sunset` (may be NULL)
- **Precipitation (DOUBLE):** `preciptotal`, `snowfall`
- **Pressure (DOUBLE):** `stnpressure`, `sealevel`
- **Wind (DOUBLE, BIGINT):** `resultspeed`, `resultdir` (direction in degrees), `avgspeed`
- `codesum` – Weather code summary (VARCHAR, e.g., `"RA FZFG BR"` for rain, freezing fog, mist; often empty string for clear conditions)