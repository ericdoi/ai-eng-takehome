# Countries Schema Reference Guide

## Schema Summary
The Countries schema contains world development indicators tracked annually from 1960–2011 across multiple countries, with metadata on countries, indicators, and a 2012 target forecast.

---

## Table Reference

### Table: `Countries.Data`
**Meaning:** Annual indicator values by country and metric (1960–2011).  
**Synonyms:** World Bank indicators, development metrics, time-series data.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Country Name` | VARCHAR | Full country name | Country, nation |
| `Country Code` | VARCHAR | ISO 3166-1 alpha-3 code | Code, country ID |
| `Indicator Name` | VARCHAR | Full name of the development indicator | Metric name, indicator |
| `Indicator Code` | VARCHAR | Standardized code for the indicator | Metric code, indicator ID |
| `1960`–`2011` | DOUBLE | Annual value for that year | Year value, annual data |

**Notable values:**
- Year columns are numeric (1960, 1961, ..., 2011); values are DOUBLE or NaN.
- `Indicator Code` examples: `AG.LND.EL5M.ZS`, `AG.LND.FRST.K2`, `EG.ELC.ACCS.ZS`

---

### Table: `Countries.Metadata - Countries`
**Meaning:** Country-level metadata including region and income classification.  
**Synonyms:** Country master, country attributes, country lookup.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Country Code` | VARCHAR | ISO 3166-1 alpha-3 code | Code, country ID |
| `Country Name` | VARCHAR | Full country name | Country, nation |
| `Region` | VARCHAR | Geographic region | Continent, geographic area |
| `IncomeGroup` | VARCHAR | World Bank income classification | Income level, economic tier |
| `SpecialNotes` | VARCHAR | Additional metadata or caveats | Notes, remarks |

**Notable values (exact enumerations):**
- `Region`: `East Asia & Pacific`, `Europe & Central Asia`, `Latin America & Caribbean`, `Middle East & North Africa`, `North America`, `South Asia`, `Sub-Saharan Africa`
- `IncomeGroup`: `High income: OECD`, `High income: nonOECD`, `Low income`, `Lower middle income`, `Upper middle income`

---

### Table: `Countries.Metadata - Indicators`
**Meaning:** Indicator-level metadata including definitions and data sources.  
**Synonyms:** Indicator master, metric definitions, indicator lookup.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `INDICATOR_CODE` | VARCHAR | Standardized code for the indicator | Code, indicator ID |
| `INDICATOR_NAME` | VARCHAR | Full name of the indicator | Metric name, indicator |
| `SOURCE_NOTE` | VARCHAR | Definition and methodology | Definition, description |
| `SOURCE_ORGANIZATION` | VARCHAR | Organization that provided the data | Source, data provider |

---

### Table: `Countries.target`
**Meaning:** 2012 forecast values (one year beyond the main Data table).  
**Synonyms:** 2012 projection, target year, forecast data.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Country Code` | VARCHAR | ISO 3166-1 alpha-3 code | Code, country ID |
| `2012` | DOUBLE | Projected or target value for 2012 | 2012 value, forecast |

---

## Join Paths

### Data to Metadata - Countries
```sql
Countries.Data d
JOIN Countries.[Metadata - Countries] mc
  ON d.[Country Code] = mc.[Country Code]
```

### Data to Metadata - Indicators
```sql
Countries.Data d
JOIN Countries.[Metadata - Indicators] mi
  ON d.[Indicator Code] = mi.[INDICATOR_CODE]
```

### Data to Target
```sql
Countries.Data d
JOIN Countries.target t
  ON d.[Country Code] = t.[Country Code]
```

### All three metadata tables
```sql
Countries.Data d
JOIN Countries.[Metadata - Countries] mc
  ON d.[Country Code] = mc.[Country Code]
JOIN Countries.[Metadata - Indicators] mi
  ON d.[Indicator Code] = mi.[INDICATOR_CODE]
```

---

## Business Rules as SQL

**Rule: Use ISO 3166-1 alpha-3 country codes as primary identifier**
- Always join on `Country Code`, not `Country Name`.
- Example: `ON d.[Country Code] = mc.[Country Code]` (not `ON d.[Country Name] = mc.[Country Name]`)

**Rule: Flag countries with population < 100,000 as potentially unreliable for economic indicators**
- Requires external population data; within this schema, filter by `IncomeGroup` or `Region` as proxy.
- Example: `WHERE mc.IncomeGroup NOT IN ('High income: nonOECD')` (small island nations often in this group)

**Rule: Regional groupings align with UN geographic classifications**
- Use exact `Region` values from `Metadata - Countries`:
  - `WHERE mc.Region = 'Sub-Saharan Africa'`
  - `WHERE mc.Region IN ('East Asia & Pacific', 'South Asia')`

**Rule: Specify year and data type for economic indicators**
- Always reference the year column explicitly: `d.[2010]`, `d.[2011]`, etc.
- Distinguish between nominal and PPP-adjusted by checking `INDICATOR_NAME` or `SOURCE_NOTE`.
- Example: `SELECT d.[Country Code], d.[2010] FROM Countries.Data d WHERE d.[Indicator Code] = 'NY.GDP.PCAP.CD'`

**Rule: Use most recent available data, not NaN**
- Filter out null/NaN values when selecting annual data.
- Example: `WHERE d.[2011] IS NOT NULL` (in SQL Server/standard SQL, NaN may be represented as NULL or actual NaN)

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| Country | `[Country Code]` (primary) or `[Country Name]` (secondary) |
| Indicator / Metric | `[Indicator Code]` (primary) or `[Indicator Name]` (secondary) |
| Year / Annual value | Column name as numeric string: `[1960]`, `[2011]`, etc. |
| Region / Continent | `mc.[Region]` from `Metadata - Countries` |
| Income level / Economic tier | `mc.[IncomeGroup]` from `Metadata - Countries` |
| Data source / Provider | `mi.[SOURCE_ORGANIZATION]` from `Metadata - Indicators` |
| Metric definition | `mi.[SOURCE_NOTE]` from `Metadata - Indicators` |
| Forecast / Projection | `t.[2012]` from `target` table |
| Most recent value | `d.[2011]` (latest year in main Data table) |
| Historical data | `d.[1960]` through `d.[2010]` |