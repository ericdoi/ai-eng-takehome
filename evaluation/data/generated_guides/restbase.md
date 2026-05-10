# SQL Reference Guide: restbase Schema

## 1. Schema Summary

The `restbase` schema contains restaurant information across California, including general details (name, cuisine type, ratings), geographic classifications (county and region), and physical addresses.

---

## 2. Table Reference

### Table: `restbase.generalinfo`
**Meaning:** Core restaurant records with cuisine type and customer ratings.
**Synonyms:** restaurants, restaurant master, restaurant details

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_restaurant` | BIGINT | Unique restaurant identifier | restaurant_id, rest_id |
| `label` | VARCHAR | Restaurant name | name, restaurant_name |
| `food_type` | VARCHAR | Cuisine category | cuisine, cuisine_type |
| `city` | VARCHAR | City where restaurant is located | city_name |
| `review` | DOUBLE | Average customer rating (numeric score) | rating, score, average_rating |

**Notable values:**
- `food_type`: "afghani", "24 hour diner" (and others)
- `review`: numeric scores (e.g., 2.3, 3.8, 4.0)

---

### Table: `restbase.geographic`
**Meaning:** Geographic classification mapping cities to counties and regions.
**Synonyms:** geography, city_geography, location_classification

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `city` | VARCHAR | City name | city_name |
| `county` | VARCHAR | County name | county_name |
| `region` | VARCHAR | Regional grouping | region_name, area |

**Notable values:**
- `county`: "alameda county", "contra costa county", "el dorado county", "los angeles county", "marin county", "mendocino county", "monterey county", "napa county", "placer county", "san benito county", "san francisco county", "san joaquin county", "san mateo county", "santa clara county", "santa cruz county", "solano county", "sonoma county", "tuolumne county", "unknown", "yolo county"
- `region`: "bay area", "lake tahoe", "los angeles area", "monterey", "napa valley", "northern california", "sacramento area", "unknown", "yosemite and mono lake area"

---

### Table: `restbase.location`
**Meaning:** Physical street addresses for restaurants.
**Synonyms:** restaurant_address, address, street_address

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_restaurant` | BIGINT | Restaurant identifier (foreign key) | restaurant_id, rest_id |
| `street_num` | BIGINT | Street number | street_number, house_number |
| `street_name` | VARCHAR | Street name | street, address_street |
| `city` | VARCHAR | City name | city_name |

---

## 3. Join Paths

**`generalinfo` to `location`:**
```sql
restbase.generalinfo g
JOIN restbase.location l ON g.id_restaurant = l.id_restaurant
```

**`generalinfo` to `geographic` (via city):**
```sql
restbase.generalinfo g
JOIN restbase.geographic geo ON g.city = geo.city
```

**`location` to `geographic` (via city):**
```sql
restbase.location l
JOIN restbase.geographic geo ON l.city = geo.city
```

**Three-table join (all tables):**
```sql
restbase.generalinfo g
JOIN restbase.location l ON g.id_restaurant = l.id_restaurant
JOIN restbase.geographic geo ON g.city = geo.city
```

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation.

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| restaurant name | `generalinfo.label` |
| cuisine type | `generalinfo.food_type` |
| rating | `generalinfo.review` |
| customer review score | `generalinfo.review` |
| county | `geographic.county` |
| region | `geographic.region` |
| street address | `location.street_num`, `location.street_name` |
| restaurant location | `location.city` |
| restaurants in [county] | `JOIN geographic WHERE geographic.county = '[county]'` |
| restaurants in [region] | `JOIN geographic WHERE geographic.region = '[region]'` |
| highest rated | `ORDER BY generalinfo.review DESC` |
| lowest rated | `ORDER BY generalinfo.review ASC` |