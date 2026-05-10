# CraftBeer Schema Reference Guide

## Schema Summary
The CraftBeer schema contains craft beer inventory and brewery information, tracking beer characteristics (ABV, IBU, style, size) and brewery locations for distribution and analysis.

---

## Table Reference

### Table: `CraftBeer.beers`
**Meaning**: Individual beer products in the craft beer catalog.
**Synonyms**: beer inventory, beer products, beer catalog

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique beer identifier | beer_id, beer identifier |
| `brewery_id` | BIGINT | Foreign key to breweries table | brewery identifier |
| `abv` | DOUBLE | Alcohol by volume (decimal, e.g., 0.065 = 6.5%) | alcohol content, alcohol percentage |
| `ibu` | DOUBLE | International Bitterness Units | bitterness, hop bitterness |
| `name` | VARCHAR | Beer product name | beer name, product name |
| `style` | VARCHAR | Beer style classification | beer style, beer type, category |
| `ounces` | DOUBLE | Serving size in fluid ounces | serving size, oz, volume |

**Notable values** (from style column):
- "American Pale Ale (APA)"
- "American Double / Imperial IPA"
- "Scottish Ale"
- "Czech Pilsener"

---

### Table: `CraftBeer.breweries`
**Meaning**: Brewery companies and their locations.
**Synonyms**: brewery information, brewery master, brewery directory

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique brewery identifier | brewery_id, brewery identifier |
| `name` | VARCHAR | Brewery company name | brewery name, company name |
| `city` | VARCHAR | City location | city name, municipality |
| `state` | VARCHAR | State abbreviation (e.g., "MN", "KY") | state code, state abbreviation |

**Notable values** (from sample data):
- States: "MN", "KY", "MA", "CA"
- Cities: "Minneapolis", "Louisville", "Framingham", "San Diego", "San Francisco"

---

## Join Paths

**Beers to Breweries** (standard relationship):
```sql
CraftBeer.beers b
INNER JOIN CraftBeer.breweries br ON b.brewery_id = br.id
```

---

## Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| High-gravity beer | `WHERE abv >= 0.095` |
| Extreme IBU | `WHERE ibu > 100` |
| Missing IBU data | `WHERE ibu IS NULL` (impute to 20 for analysis) |
| Microbrewery | `HAVING COUNT(b.id) < 3` (group by brewery_id) |
| Production brewery | `HAVING COUNT(b.id) > 20` (group by brewery_id) |
| Missing brewery location | `WHERE br.city IS NULL OR br.state IS NULL` |
| IPA style | `WHERE style LIKE '%IPA%' OR style LIKE '%India Pale Ale%'` |
| Stout/Porter style | `WHERE style LIKE '%Stout%' OR style LIKE '%Porter%'` |
| Lager/Pilsner style | `WHERE style LIKE '%Lager%' OR style LIKE '%Pilsner%' OR style LIKE '%Pilsener%'` |
| Wheat style | `WHERE style LIKE '%Hefeweizen%' OR style LIKE '%Witbier%' OR style LIKE '%Wheat%'` |
| Sour style | `WHERE style LIKE '%Sour%' OR style LIKE '%Wild%'` |
| Session beer | `WHERE abv < 0.05` |
| Default serving size | `COALESCE(ounces, 12.0)` |
| Seasonal beer flag | `WHERE name LIKE '%Pumpkin%' OR name LIKE '%Winter%' OR name LIKE '%Seasonal%'` |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| alcohol content | `beers.abv` |
| alcohol percentage | `beers.abv * 100` |
| bitterness | `beers.ibu` |
| beer type | `beers.style` |
| serving size | `beers.ounces` |
| brewery location | `breweries.city`, `breweries.state` |
| brewery name | `breweries.name` |
| high-gravity | `WHERE beers.abv >= 0.095` |
| extreme bitterness | `WHERE beers.ibu > 100` |
| microbrewery | `HAVING COUNT(beers.id) < 3` |
| production brewery | `HAVING COUNT(beers.id) > 20` |
| IPA | `WHERE beers.style LIKE '%IPA%'` |
| dark beer | `WHERE beers.style LIKE '%Stout%' OR beers.style LIKE '%Porter%'` |
| light lager | `WHERE beers.style LIKE '%Lager%' OR beers.style LIKE '%Pilsner%'` |
| session beer | `WHERE beers.abv < 0.05` |
| beer catalog size | `COUNT(beers.id)` per brewery |
| price per ounce | `price / COALESCE(beers.ounces, 12.0)` |
| ABV per dollar | `beers.abv / price` |