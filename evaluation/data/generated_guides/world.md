# World Schema Reference Guide

## Schema Summary
This schema contains geographic, demographic, and linguistic data for world countries and their major cities, with ISO 3166-1 alpha-3 country codes as the primary identifier.

---

## Join Paths

**Countries to their capital cities:**
```sql
FROM world.Country c
LEFT JOIN world.City cy ON c.Capital = cy.ID
```

**Countries to all their cities:**
```sql
FROM world.Country c
JOIN world.City cy ON c.Code = cy.CountryCode
```

**Countries to their languages:**
```sql
FROM world.Country c
JOIN world.CountryLanguage cl ON c.Code = cl.CountryCode
```

**Complete country-city-language view:**
```sql
FROM world.Country c
LEFT JOIN world.City cy ON c.Code = cy.CountryCode
LEFT JOIN world.CountryLanguage cl ON c.Code = cl.CountryCode
```

---

## Business Rules as SQL

| Rule | SQL Condition |
|------|---------------|
| Major city (population threshold) | `WHERE cy.Population > 2000000` |
| Official language only | `WHERE cl.IsOfficial = 'T'` |
| Dominant language (speaker majority) | `WHERE cl.Percentage > 90` |
| Population density calculation | `SELECT c.Population / c.SurfaceArea AS density_per_sq_km` |
| Flag small economies (unreliable data) | `WHERE c.Population < 100000` |
| Multilingual country | `HAVING COUNT(DISTINCT cl.Language) > 1` |

---

## Synonym Glossary

| Common Term | Schema Reference |
|-------------|------------------|
| Country code | `world.Country.Code` or `world.City.CountryCode` |
| Country name | `world.Country.Name` |
| Capital city ID | `world.Country.Capital` |
| City location | `world.City.District` |
| Continent | `world.Country.Continent` |
| Sub-region | `world.Country.Region` |
| Speaker percentage | `world.CountryLanguage.Percentage` |
| Official language flag | `world.CountryLanguage.IsOfficial` (values: `'T'`, `'F'`) |
| Economic output | `world.Country.GNP` |
| Life span | `world.Country.LifeExpectancy` |
| Independence date | `world.Country.IndepYear` |
| Territory type | `world.Country.GovernmentForm` |

---

## Table Reference

### `world.Country`
**Meaning:** Sovereign nations and territories with political and economic metadata.

| Column | Notes |
|--------|-------|
| `Code` | **Primary identifier.** ISO 3166-1 alpha-3 code (e.g., `'AFG'`, `'NLD'`). Use for all joins. |
| `Code2` | ISO 3166-1 alpha-2 code (e.g., `'AF'`, `'NL'`). Secondary reference only. |
| `Continent` | Enumerated values: `'Africa'`, `'Antarctica'`, `'Asia'`, `'Europe'`, `'North America'`, `'Oceania'`, `'South America'` |
| `Region` | UN sub-region classification (e.g., `'Southern and Central Asia'`, `'Caribbean'`). Use for regional grouping. |
| `SurfaceArea` | Land area in square kilometers. Use for density calculations: `Population / SurfaceArea`. |
| `IndepYear` | Year of independence. NULL for territories/dependencies. |
| `Population` | Most recent estimate available; year not specified in schema. |
| `LifeExpectancy` | Years. May be estimate for conflict zones. |
| `GNP` | Gross National Product. Year and adjustment method not specified; flag as potentially dated. |
| `GNPOld` | Previous GNP figure for trend analysis. |
| `Capital` | Foreign key to `world.City.ID` (the capital city). NULL for some territories. |
| `GovernmentForm` | Indicates sovereignty status (e.g., `'Republic'`, `'Nonmetropolitan Territory of The Netherlands'`). Use to distinguish territories from sovereign states. |
| `HeadOfState` | Name of head of state. |
| `LocalName` | Country name in local language(s). |

---

### `world.City`
**Meaning:** Cities and urban centers with population and geographic location.

| Column | Notes |
|--------|-------|
| `ID` | Primary key. Referenced by `world.Country.Capital`. |
| `CountryCode` | Foreign key to `world.Country.Code`. Always use for country joins. |
| `District` | Administrative subdivision (province, state, region). May be NULL. |
| `Population` | Urban area population. Use threshold `> 2000000` to identify major cities. |

---

### `world.CountryLanguage`
**Meaning:** Languages spoken in each country with official status and speaker percentage.

| Column | Notes |
|--------|-------|
| `CountryCode` | Foreign key to `world.Country.Code`. |
| `Language` | Language name (e.g., `'Dutch'`, `'Balochi'`). Multiple rows per country are normal. |
| `IsOfficial` | Enumerated: `'T'` (official), `'F'` (not official). Countries may have multiple official languages. |
| `Percentage` | Percentage of population speaking this language. **Percentages across all languages in a country may exceed 100% due to multilingualism.** Do not use for population calculations. |