# CraftBeer Schema Reference Guide

## Schema Summary
This schema tracks craft beer inventory across breweries, including alcohol content, bitterness, style classification, and brewery location data for distribution and customer preference analysis.

---

## Join Paths

**[REQUIRED]** Beer to Brewery:
```sql
FROM CraftBeer.beers b
JOIN CraftBeer.breweries br ON b.brewery_id = br.id
```

---

## Business Rules as SQL

### High-Gravity Classification
- **IDENTIFY high-gravity:** `WHERE abv >= 0.095` — beers subject to different distribution regulations
- **EXCLUDE high-gravity:** `WHERE abv < 0.095`

### Extreme Bitterness Classification
- **IDENTIFY extreme bitterness:** `WHERE ibu > 100` — segment separately for customer preference analysis
- **EXCLUDE extreme bitterness:** `WHERE ibu <= 100 OR ibu IS NULL`

### IBU Imputation
- **IDENTIFY missing IBU:** `WHERE ibu IS NULL` — likely lagers or wheat beers; impute value of 20 for analysis
- **Imputed IBU value:** `COALESCE(ibu, 20)`

### Microbrewery Classification
- **IDENTIFY microbrewery:** `GROUP BY brewery_id HAVING COUNT(DISTINCT b.id) < 3` — fewer than 3 beers in catalog; aggregate regionally
- **EXCLUDE microbrewery:** `GROUP BY brewery_id HAVING COUNT(DISTINCT b.id) >= 3`

### Production Brewery Classification
- **IDENTIFY production brewery:** `GROUP BY brewery_id HAVING COUNT(DISTINCT b.id) > 20` — producing more than 20 distinct beers; analyze separately
- **EXCLUDE production brewery:** `GROUP BY brewery_id HAVING COUNT(DISTINCT b.id) <= 20`

### Brewery Location Validation
- **IDENTIFY missing location:** `WHERE city IS NULL OR state IS NULL` — flag for distribution analysis
- **EXCLUDE missing location:** `WHERE city IS NOT NULL AND state IS NOT NULL`

### Session Beer Classification
- **IDENTIFY session beer:** `WHERE abv < 0.05` — track separately from full-strength counterparts
- **EXCLUDE session beer:** `WHERE abv >= 0.05`

### Style Normalization
```sql
CASE
  WHEN style LIKE '%IPA%' OR style LIKE '%India Pale Ale%' THEN 'IPA'
  WHEN style LIKE '%Stout%' OR style LIKE '%Porter%' THEN 'Stout/Porter'
  WHEN style LIKE '%Lager%' OR style LIKE '%Pilsner%' OR style LIKE '%Pilsener%' THEN 'Lager/Pilsner'
  WHEN style LIKE '%Hefeweizen%' OR style LIKE '%Witbier%' OR style LIKE '%Wheat%' THEN 'Wheat'
  WHEN style LIKE '%Sour%' OR style LIKE '%Wild%' THEN 'Sour'
  ELSE 'Other'
END
```

### Serving Size Default
- **Default ounces:** `COALESCE(ounces, 12)`

### Premium Tier Flagging
- **IDENTIFY premium tier:** Price-per-ounce > 2× category average — requires external pricing data not present in schema

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| alcohol content, ABV | `CraftBeer.beers.abv` |
| bitterness, IBU | `CraftBeer.beers.ibu` |
| beer type, category | `CraftBeer.beers.style` |
| serving size | `CraftBeer.beers.ounces` |
| brewery location | `CraftBeer.breweries.city`, `CraftBeer.breweries.state` |
| high-gravity | `WHERE abv >= 0.095` |
| extreme bitterness | `WHERE ibu > 100` |
| session beer | `WHERE abv < 0.05` |
| microbrewery | `HAVING COUNT(DISTINCT id) < 3` |
| production brewery | `HAVING COUNT(DISTINCT id) > 20` |

---

## Table Reference

### `CraftBeer.beers`
Craft beer inventory with alcohol content, bitterness, and style.

| Column | Semantics |
|--------|-----------|
| `brewery_id` | Foreign key to `CraftBeer.breweries.id` |
| `abv` | Alcohol by volume as decimal (0.065 = 6.5%); ≥0.095 triggers high-gravity rules |
| `ibu` | International Bitterness Units; NULL values should be imputed as 20; >100 is "extreme" |
| `style` | Beer style name (varies widely; normalize using CASE WHEN rules above). Examples: "American Pale Ale (APA)", "American Double / Imperial IPA", "Scottish Ale", "Czech Pilsener" |
| `ounces` | Serving size in fluid ounces; NULL defaults to 12 |

### `CraftBeer.breweries`
Brewery master data with location.

| Column | Semantics |
|--------|-----------|
| `city` | Brewery city; critical for distribution analysis; flag if NULL |
| `state` | Brewery state (2-letter code). Examples: "MN", "KY", "MA", "CA" |