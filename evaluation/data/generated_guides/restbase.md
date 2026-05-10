# restbase Schema Reference Guide

## Schema Summary
This schema contains restaurant information across California, including general details (name, cuisine type, ratings), geographic classifications (county, region), and street addresses.

## Join Paths

**Restaurants with geographic region:**
```sql
FROM restbase.generalinfo g
JOIN restbase.geographic geo ON g.city = geo.city
```

**Restaurants with full address and region:**
```sql
FROM restbase.generalinfo g
JOIN restbase.location l ON g.id_restaurant = l.id_restaurant
JOIN restbase.geographic geo ON g.city = geo.city
```

**Restaurants by city and county:**
```sql
FROM restbase.generalinfo g
JOIN restbase.geographic geo ON g.city = geo.city
WHERE geo.county = 'santa clara county'
```

## Table Reference

### restbase.generalinfo
Restaurant core data: name, cuisine type, city, and ratings.

| Column | Notes |
|--------|-------|
| `id_restaurant` | Primary key; links to `restbase.location` |
| `label` | Restaurant name |
| `food_type` | Cuisine category (e.g., "afghani", "24 hour diner") |
| `city` | Links to `restbase.geographic` |
| `review` | Rating score (numeric, 0–5 range typical) |

### restbase.geographic
City-to-county-to-region mapping for California locations.

| Column | Notes |
|--------|-------|
| `city` | Join key to `restbase.generalinfo` and `restbase.location` |
| `county` | Enumerated values: alameda county, contra costa county, el dorado county, los angeles county, marin county, mendocino county, monterey county, napa county, placer county, san benito county, san francisco county, san joaquin county, san mateo county, santa clara county, santa cruz county, solano county, sonoma county, tuolumne county, unknown, yolo county |
| `region` | Enumerated values: bay area, lake tahoe, los angeles area, monterey, napa valley, northern california, sacramento area, unknown, yosemite and mono lake area |

### restbase.location
Street addresses for restaurants.

| Column | Notes |
|--------|-------|
| `id_restaurant` | Foreign key to `restbase.generalinfo` |
| `street_num` | Street number (numeric) |
| `street_name` | Street name (includes direction prefix/suffix, e.g., "e. el camino real") |
| `city` | City name; links to `restbase.geographic` |