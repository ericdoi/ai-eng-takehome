# Mondial Schema Reference Guide

## Schema Summary
The Mondial schema contains geopolitical and geographic data: countries, provinces, cities, natural features (mountains, rivers, lakes, deserts, seas, islands), borders, economic indicators, demographics (languages, religions, ethnic groups), and organizational memberships.

---

## Join Paths

**Country to its provinces:**
```sql
FROM Mondial.country c
JOIN Mondial.province p ON c.Code = p.Country
```

**Country to its cities:**
```sql
FROM Mondial.country c
JOIN Mondial.city ci ON c.Code = ci.Country
```

**Country to continents (with percentage):**
```sql
FROM Mondial.country c
JOIN Mondial.encompasses e ON c.Code = e.Country
```

**Country borders:**
```sql
FROM Mondial.borders b
WHERE b.Country1 = 'A' OR b.Country2 = 'A'
```

**City to geographic features (rivers, lakes, seas):**
```sql
FROM Mondial.city ci
JOIN Mondial.located l ON ci.Name = l.City AND ci.Country = l.Country
```

**City on island:**
```sql
FROM Mondial.city ci
JOIN Mondial.locatedOn lo ON ci.Name = lo.City AND ci.Country = lo.Country
```

**Province to geographic features:**
```sql
FROM Mondial.province p
JOIN Mondial.geo_river gr ON p.Name = gr.Province AND p.Country = gr.Country
```

**Country demographics (languages, religions, ethnic groups):**
```sql
FROM Mondial.country c
JOIN Mondial.language l ON c.Code = l.Country
JOIN Mondial.religion r ON c.Code = r.Country
JOIN Mondial.ethnicGroup eg ON c.Code = eg.Country
```

**Country to organizations:**
```sql
FROM Mondial.country c
JOIN Mondial.isMember im ON c.Code = im.Country
```

**River to its path (source to estuary):**
```sql
FROM Mondial.river r
JOIN Mondial.geo_source gs ON r.Name = gs.River
JOIN Mondial.geo_river gr ON r.Name = gr.River
```

---

## Business Rules as SQL

- **Independent country**: `WHERE Mondial.politics.Dependent IS NULL`
- **Dependent territory**: `WHERE Mondial.politics.Dependent IS NOT NULL`
- **Majority language** (>50%): `WHERE Mondial.language.Percentage > 50`
- **Majority religion** (>50%): `WHERE Mondial.religion.Percentage > 50`
- **Significant ethnic group** (>10%): `WHERE Mondial.ethnicGroup.Percentage > 10`
- **Country spans multiple continents**: `GROUP BY Country HAVING COUNT(DISTINCT Continent) > 1` on `Mondial.encompasses`
- **Landlocked country**: `WHERE Country NOT IN (SELECT DISTINCT Country FROM Mondial.geo_sea)`
- **Island nation**: `WHERE Country IN (SELECT DISTINCT Country FROM Mondial.geo_island) AND Country NOT IN (SELECT DISTINCT Country FROM Mondial.geo_mountain WHERE Mountain NOT IN (SELECT Mountain FROM Mondial.mountainOnIsland))`

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| country code | `Mondial.country.Code` |
| capital city | `Mondial.country.Capital` |
| country area | `Mondial.country.Area` |
| country population | `Mondial.country.Population` |
| independence date | `Mondial.politics.Independence` |
| dependent territory | `Mondial.politics.Dependent` |
| government type | `Mondial.politics.Government` |
| GDP | `Mondial.economy.GDP` |
| economic sector share | `Mondial.economy.Agriculture`, `.Service`, `.Industry` |
| inflation rate | `Mondial.economy.Inflation` |
| population growth | `Mondial.population.Population_Growth` |
| infant mortality | `Mondial.population.Infant_Mortality` |
| language spoken | `Mondial.language.Name` |
| religion practiced | `Mondial.religion.Name` |
| ethnic group | `Mondial.ethnicGroup.Name` |
| border length | `Mondial.borders.Length` |
| sea depth | `Mondial.sea.Depth` |
| mountain height | `Mondial.mountain.Height` |
| river length | `Mondial.river.Length` |
| lake area | `Mondial.lake.Area` |
| desert area | `Mondial.desert.Area` |
| island area | `Mondial.island.Area` |
| city population | `Mondial.city.Population` |
| province capital | `Mondial.province.Capital` |
| organization membership type | `Mondial.isMember.Type` |

---

## Table Reference

### `Mondial.country`
Core country records. **Columns of note:**
- `Code`: 1–3 character country code (primary key)
- `Capital`: city name (not a foreign key; matches `Mondial.city.Name`)
- `Province`: province name of capital (matches `Mondial.province.Name`)
- `Area`: in km²
- `Population`: total population

### `Mondial.province`
Subdivisions within countries. **Columns of note:**
- `Name`: province name
- `Country`: country code (foreign key to `Mondial.country.Code`)
- `Capital`: city name (not a foreign key)
- `CapProv`: province of capital (self-reference)
- `Area`: in km²
- `Population`: provincial population

### `Mondial.city`
Cities and towns. **Columns of note:**
- `Name`: city name
- `Country`: country code
- `Province`: province name
- `Population`: city population
- `Longitude`, `Latitude`: may be NULL

### `Mondial.politics`
Political metadata. **Columns of note:**
- `Country`: country code (primary key)
- `Independence`: date of independence (NULL for dependent territories)
- `Dependent`: country code of parent (NULL for independent countries); **enum values**: `AUS`, `DK`, `F`, `GB`, `N`, `NL`, `NZ`, `TJ`, `USA`
- `Government`: government type string

### `Mondial.encompasses`
Country-to-continent mapping with percentage. **Columns of note:**
- `Country`: country code
- `Continent`: continent name; **enum values**: `Africa`, `America`, `Asia`, `Australia/Oceania`, `Europe`
- `Percentage`: % of country in this continent

### `Mondial.continent`
Continent records. **Columns of note:**
- `Name`: continent name; **enum values**: `Africa`, `America`, `Asia`, `Australia/Oceania`, `Europe`
- `Area`: in km²

### `Mondial.borders`
Country-to-country borders. **Columns of note:**
- `Country1`, `Country2`: country codes (not ordered; check both directions)
- `Length`: border length in km

### `Mondial.Independent_Borders`
Borders between independent countries only (subset of `Mondial.borders`).

### `Mondial.Named_Borders`
Borders with geographic feature names. **Columns of note:**
- `Name1`, `Name2`: names of geographic features forming the border
- `Country1`, `Country2`: country codes
- `Length`: border length in km

### `Mondial.language`
Languages spoken in countries. **Columns of note:**
- `Country`: country code
- `Name`: language name
- `Percentage`: % of population speaking this language

### `Mondial.religion`
Religions practiced in countries. **Columns of note:**
- `Country`: country code
- `Name`: religion name
- `Percentage`: % of population practicing this religion

### `Mondial.ethnicGroup`
Ethnic groups in countries. **Columns of note:**
- `Country`: country code
- `Name`: ethnic group name
- `Percentage`: % of population in this group

### `Mondial.economy`
Economic indicators by country. **Columns of note:**
- `Country`: country code
- `GDP`: gross domestic product (in millions USD, typically)
- `Agriculture`, `Service`, `Industry`: % of GDP by sector
- `Inflation`: inflation rate (%)

### `Mondial.population`
Population statistics by country. **Columns of note:**
- `Country`: country code
- `Population_Growth`: annual growth rate (%)
- `Infant_Mortality`: infant mortality rate (per 1000 live births)

### `Mondial.isMember`
Country membership in organizations. **Columns of note:**
- `Country`: country code
- `Organization`: organization abbreviation
- `Type`: membership type (e.g., `member`, `observer`, `nonregional member`)

### `Mondial.organization`
International organizations. **Columns of note:**
- `Abbreviation`: organization code (primary key)
- `Name`: full organization name
- `City`: headquarters city
- `Country`: headquarters country code
- `Province`: headquarters province
- `Established`: founding date

### `Mondial.mountain`
Mountain ranges and peaks. **Columns of note:**
- `Name`: mountain name
- `Mountains`: mountain range name
- `Height`: elevation in meters
- `Type`: **enum values**: `granite`, `monolith`, `volcanic`, `volcano`
- `Longitude`, `Latitude`: coordinates

### `Mondial.mountainOnIsland`
Mountains located on islands. Links `Mondial.mountain.Name` to `Mondial.island.Name`.

### `Mondial.geo_mountain`
Geographic assignment of mountains to provinces. **Columns of note:**
- `Mountain`: mountain name
- `Country`: country code
- `Province`: province name

### `Mondial.river`
Rivers with source and estuary data. **Columns of note:**
- `Name`: river name
- `River`: parent river (for tributaries)
- `Lake`: terminal lake (if applicable)
- `Sea`: terminal sea (if applicable)
- `Length`: river length in km
- `SourceLongitude`, `SourceLatitude`: source coordinates
- `SourceAltitude`: source elevation in meters
- `Mountains`: mountain range containing source
- `EstuaryLongitude`, `EstuaryLatitude`: mouth coordinates

### `Mondial.geo_river`
Geographic assignment of rivers to provinces. **Columns of note:**
- `River`: river name
- `Country`: country code
- `Province`: province name

### `Mondial.geo_source`
River source locations. **Columns of note:**
- `River`: river name
- `Country`: country code
- `Province`: province name

### `Mondial.geo_estuary`
River estuary locations. **Columns of note:**
- `River`: river name
- `Country`: country code
- `Province`: province name

### `Mondial.lake`
Lakes and reservoirs. **Columns of note:**
- `Name`: lake name
- `Area`: in km²
- `Depth`: maximum depth in meters
- `Altitude`: elevation in meters
- `Type`: **enum values**: `acid`, `artificial`, `caldera`, `crater`, `impact`, `salt`
- `River`: river feeding the lake
- `Longitude`, `Latitude`: coordinates

### `Mondial.geo_lake`
Geographic assignment of lakes to provinces. **Columns of note:**
- `Lake`: lake name
- `Country`: country code
- `Province`: province name

### `Mondial.sea`
Seas and oceans. **Columns of note:**
- `Name`: sea name
- `Depth`: maximum depth in meters

### `Mondial.geo_sea`
Geographic assignment of seas to provinces. **Columns of note:**
- `Sea`: sea name
- `Country`: country code
- `Province`: province name

### `Mondial.mergesWith`
Sea-to-sea connections. **Columns of note:**
- `Sea1`, `Sea2`: sea names (not ordered)

### `Mondial.desert`
Deserts. **Columns of note:**
- `Name`: desert name
- `Area`: in km²
- `Longitude`, `Latitude`: coordinates

### `Mondial.geo_desert`
Geographic assignment of deserts to provinces. **Columns of note:**
- `Desert`: desert name
- `Country`: country code
- `Province`: province name

### `Mondial.island`
Islands. **Columns of note:**
- `Name`: island name
- `Islands`: island group name
- `Area`: in km²
- `Height`: maximum elevation in meters
- `Type`: **enum values**: `atoll`, `coral`, `lime`, `volcanic`
- `Longitude`, `Latitude`: coordinates

### `Mondial.geo_island`
Geographic assignment of islands to provinces. **Columns of note:**
- `Island`: island name
- `Country`: country code
- `Province`: province name

### `Mondial.islandIn`
Islands located in water bodies. **Columns of note:**
- `Island`: island name
- `Sea`: sea name (if in sea)
- `Lake`: lake name; **enum values**: `Lake Huron`, `Lake Manicouagan`, `Lake Nicaragua`, `Lake Toba`, `Ozero Baikal`
- `River`: river name (if in river)

### `Mondial.located`
Cities located on rivers, lakes, or seas. **Columns of note:**
- `City`: city name
- `Province`: province name
- `Country`: country code
- `River`: river name (or `None`)
- `Lake`: lake name (or `NaN`)
- `Sea`: sea name (or `NaN`)

### `Mondial.locatedOn`
Cities located on islands. **Columns of note:**
- `City`: city name
- `Province`: province name
- `Country`: country code
- `Island`: island name

### `Mondial.target`
Religious conversion targets by country. **Columns of note:**
- `Country`: country code
- `Target`: **enum values**: `Christian`, `non-Christian`

### `Mondial.Country_Full`
Denormalized view combining country, politics, and encompasses data (all columns are BIGINT; use `Mondial.country`, `Mondial.politics`, `Mondial.encompasses` instead).

### `Mondial.Country2Continent`
Denormalized country-continent mapping (use `Mondial.encompasses` instead).

### `Mondial.Independent_Countries`
Denormalized independent country metadata (use `Mondial.country` + `Mondial.politics` instead).

### `Mondial.Symmetric_Borders`
Denormalized symmetric border pairs (use `Mondial.borders` instead).