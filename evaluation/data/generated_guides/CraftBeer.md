# CraftBeer Schema Reference Guide

## Schema Summary
The CraftBeer schema tracks craft beer inventory across breweries, including alcohol content, bitterness, style classification, and brewery location data for distribution and customer preference analysis.

---

## Join Paths

**Beer to Brewery:**
```sql
FROM CraftBeer.beers b
JOIN CraftBeer.breweries br ON b.brewery_id = br.id
```

---

## Business Rules as SQL

| Rule | SQL Condition |
|------|---------------|
| High-gravity beer | `WHERE abv >= 0.095` |
| Extreme bitterness | `WHERE ibu > 100` |
| Missing IBU data | `WHERE ibu IS NULL` — impute as 20 for analysis |
| Microbrewery | `HAVING COUNT(DISTINCT b.id) < 3` (group by brewery_id) |
| Production brewery | `HAVING COUNT(DISTINCT b.id) > 20` (group by brewery_id) |
| Session beer | `WHERE abv < 0.05` |
| IPA style | `WHERE style LIKE '%IPA%' OR style LIKE '%India Pale Ale%'` |
| Stout/Porter style | `WHERE style LIKE '%Stout%' OR style LIKE '%Porter%'` |
| Lager/Pilsner style | `WHERE style LIKE '%Lager%' OR style LIKE '%Pilsner%'` |
| Wheat style | `WHERE style LIKE '%Hefeweizen%' OR style LIKE '%Witbier%'` |
| Sour style | `WHERE style LIKE '%Sour%' OR style LIKE '%Wild%'` |
| Missing serving size | `WHERE ounces IS NULL` — default to 12 oz |
| Missing brewery location | `WHERE br.city IS NULL OR br.state IS NULL` |

---

## Synonym Glossary

| Common Term | Schema Reference |
|-------------|------------------|
| alcohol content | `CraftBeer.beers.abv` |
| bitterness | `CraftBeer.beers.ibu` |
| serving size | `CraftBeer.beers.ounces` |
| beer category | `CraftBeer.beers.style` |
| brewery location | `CraftBeer.breweries.city`, `CraftBeer.breweries.state` |
| price-per-ounce | `price / COALESCE(ounces, 12)` |
| ABV per dollar | `abv / price` |

---

## Table Reference

### `CraftBeer.beers`
Craft beer inventory with alcohol, bitterness, and style attributes.

| Column | Semantics |
|--------|-----------|
| `brewery_id` | Foreign key to `CraftBeer.breweries.id` |
| `abv` | Alcohol by volume as decimal (0.065 = 6.5%). Threshold: ≥0.095 = high-gravity |
| `ibu` | International Bitterness Units. NULL values indicate lagers/wheat beers; impute as 20. Threshold: >100 = extreme |
| `style` | Beer style classification. Contains substrings: "IPA", "Stout", "Porter", "Lager", "Pilsener", "Hefeweizen", "Witbier", "Sour", "Wild" for categorization |
| `ounces` | Serving size in fluid ounces. NULL values default to 12 oz |

### `CraftBeer.breweries`
Brewery master data with location and identity.

| Column | Semantics |
|--------|-----------|
| `city` | Brewery city. Required for distribution analysis; flag if NULL |
| `state` | Brewery state (2-letter code: MN, KY, MA, CA, etc.). Required for distribution analysis; flag if NULL |