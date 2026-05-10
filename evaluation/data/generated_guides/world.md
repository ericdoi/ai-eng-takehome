# World Schema Reference Guide for SQL Agent

## Schema Summary
The `world` schema contains geographic, demographic, and linguistic data for countries and cities worldwide, including population, economic indicators, and official/spoken languages by country.

---

## Table Reference

### Table: `world.City`
**Meaning:** Urban population centers and their geographic/demographic attributes.
**Synonyms:** Cities, Urban Areas, Municipalities

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ID` | BIGINT | Unique city identifier | City ID, CityID |
| `Name` | VARCHAR | City name | City Name |
| `CountryCode` | VARCHAR | ISO 3166-1 alpha-3 country code | Country Code, ISO Code |
| `District` | VARCHAR | Administrative subdivision (state, province, region) | State, Province, Region, Administrative Division |
| `Population` | BIGINT | City population (most recent estimate) | City Population, Urban Population |

**Notable Values:**
- `CountryCode`: Three-letter ISO codes (e.g., `AFG`, `NLD`, `AO`)

---

### Table: `world.Country`
**Meaning:** Sovereign nations and territories with geographic, demographic, and economic data.
**Synonyms:** Nations, States, Territories, Countries

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Code` | VARCHAR | ISO 3166-1 alpha-3 country code (primary key) | Country Code, ISO Code, Country ID |
| `Name` | VARCHAR | Country name | Country Name |
| `Continent` | VARCHAR | Continental classification | Continent, Region (highest level) |
| `Region` | VARCHAR | Sub-regional classification (UN geographic standard) | Sub-Region, Geographic Region |
| `SurfaceArea` | DOUBLE | Land area in square kilometers | Area, Land Area, Territory Size |
| `IndepYear` | BIGINT | Year of independence (NULL for non-sovereign territories) | Independence Year, Year Independent |
| `Population` | BIGINT | Total country population (most recent estimate) | Country Population, Total Population |
| `LifeExpectancy` | DOUBLE | Average life expectancy in years | Life Expectancy, LE |
| `GNP` | DOUBLE | Gross National Product (nominal, year unspecified) | GNP, Gross National Product |
| `GNPOld` | DOUBLE | Previous GNP figure (year unspecified) | Previous GNP, GNP Old |
| `LocalName` | VARCHAR | Country name in local language(s) | Local Name, Native Name |
| `GovernmentForm` | VARCHAR | Type of government | Government Type, Government Form |
| `HeadOfState` | VARCHAR | Name of head of state | Head of State, Leader |
| `Capital` | BIGINT | City ID of capital city (foreign key to `City.ID`) | Capital City ID |
| `Code2` | VARCHAR | ISO 3166-1 alpha-2 country code | ISO 2-Letter Code, Alpha-2 Code |

**Notable Values:**
- `Continent`: `Africa`, `Antarctica`, `Asia`, `Europe`, `North America`, `Oceania`, `South America`
- `Code`: Three-letter ISO codes (e.g., `AFG`, `NLD`, `AO`)
- `Code2`: Two-letter ISO codes (e.g., `AF`, `NL`, `AO`)

---

### Table: `world.CountryLanguage`
**Meaning:** Languages spoken in each country with official status and speaker percentage.
**Synonyms:** Languages, Country Languages, Official Languages

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `CountryCode` | VARCHAR | ISO 3166-1 alpha-3 country code (foreign key to `Country.Code`) | Country Code, ISO Code |
| `Language` | VARCHAR | Language name | Language Name |
| `IsOfficial` | VARCHAR | Official language flag | Official Status, Is Official |
| `Percentage` | DOUBLE | Percentage of country population speaking this language | Speaker Percentage, % Speakers, Language Percentage |

**Notable Values:**
- `IsOfficial`: `T` (true/official), `F` (false/not official)
- `Percentage`: Range 0–100+ (percentages may exceed 100% due to multilingualism)

---

## Join Paths

### City to Country
```sql
world.City c
JOIN world.Country co ON c.CountryCode = co.Code
```

### Country to Capital City
```sql
world.Country co
JOIN world.City c ON co.Capital = c.ID
```

### Country to Languages
```sql
world.Country co
JOIN world.CountryLanguage cl ON co.Code = cl.CountryCode
```

### All Three Tables
```sql
world.City c
JOIN world.Country co ON c.CountryCode = co.Code
JOIN world.CountryLanguage cl ON co.Code = cl.CountryCode
```

---

## Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| Major city (population threshold) | `WHERE c.Population > 2000000` |
| Capital city identification | `WHERE co.Capital = c.ID` |
| Population density calculation | `SELECT co.Population / co.SurfaceArea AS density_per_sq_km` |
| Official language | `WHERE cl.IsOfficial = 'T'` |
| Non-official language | `WHERE cl.IsOfficial = 'F'` |
| Dominant language (high speaker percentage) | `WHERE cl.Percentage > 90` |
| Sovereign nation (has independence year) | `WHERE co.IndepYear IS NOT NULL` |
| Territory/dependency (no independence year) | `WHERE co.IndepYear IS NULL` |
| Small country (population < 100,000) | `WHERE co.Population < 100000` |
| Multilingual country (multiple official languages) | `GROUP BY co.Code HAVING COUNT(CASE WHEN cl.IsOfficial = 'T' THEN 1 END) > 1` |
| Per-capita GNP | `SELECT co.GNP * 1000000 / co.Population AS gnp_per_capita` |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| Country code | `Country.Code` or `City.CountryCode` |
| Country name | `Country.Name` |
| City name | `City.Name` |
| Capital | `Country.Capital` (City ID) or join to `City` where `City.ID = Country.Capital` |
| Population | `Country.Population` or `City.Population` (context-dependent) |
| Area / Territory size | `Country.SurfaceArea` |
| Continent | `Country.Continent` |
| Region / Sub-region | `Country.Region` |
| Life expectancy | `Country.LifeExpectancy` |
| GNP / Economic output | `Country.GNP` |
| Government type | `Country.GovernmentForm` |
| Leader / Head of state | `Country.HeadOfState` |
| Official language | `CountryLanguage.Language WHERE IsOfficial = 'T'` |
| Spoken language | `CountryLanguage.Language` |
| Language speakers / Percentage | `CountryLanguage.Percentage` |
| Independence date | `Country.IndepYear` |
| District / State / Province | `City.District` |
| Major city | `City.Population > 2000000` |
| Multilingual | Multiple rows in `CountryLanguage` per `CountryCode` |
| Density | `Country.Population / Country.SurfaceArea` |