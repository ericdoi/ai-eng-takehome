# Countries Schema Reference Guide

## Schema Summary
This schema contains world development indicators tracked annually from 1960–2011 across countries, with metadata on countries, indicators, and a 2012 target forecast.

---

## Join Paths

**Data to country metadata:**
```sql
FROM Countries.Data d
JOIN Countries.[Metadata - Countries] mc ON d.[Country Code] = mc.[Country Code]
```

**Data to indicator metadata:**
```sql
FROM Countries.Data d
JOIN Countries.[Metadata - Indicators] mi ON d.[Indicator Code] = mi.INDICATOR_CODE
```

**Data to 2012 target:**
```sql
FROM Countries.Data d
JOIN Countries.target t ON d.[Country Code] = t.[Country Code]
```

**All three (full enrichment):**
```sql
FROM Countries.Data d
JOIN Countries.[Metadata - Countries] mc ON d.[Country Code] = mc.[Country Code]
JOIN Countries.[Metadata - Indicators] mi ON d.[Indicator Code] = mi.INDICATOR_CODE
JOIN Countries.target t ON d.[Country Code] = t.[Country Code]
```

---

## Business Rules as SQL

**Rule: Use ISO 3166-1 alpha-3 country codes as primary identifier**
- Always join on `[Country Code]`, not `Country Name`
- Example: `WHERE d.[Country Code] = 'USA'` not `WHERE d.[Country Name] = 'United States'`

**Rule: Flag countries with population < 100,000 for data reliability concerns**
- Requires joining to population indicator; filter on `[Indicator Code] = 'SP.POP.TOTL'` and checking year columns for values < 100000

**Rule: Economic data must specify year and adjustment type**
- Year is the column name (1960–2011 or 2012 in target table)
- Adjustment type (nominal vs PPP) is in `[Metadata - Indicators].[SOURCE_NOTE]`

**Rule: Regional groupings use UN classifications**
- Valid regions in `[Metadata - Countries].Region`: `'East Asia & Pacific'`, `'Europe & Central Asia'`, `'Latin America & Caribbean'`, `'Middle East & North Africa'`, `'North America'`, `'South Asia'`, `'Sub-Saharan Africa'`

**Rule: Income classifications are time-invariant in this schema**
- Valid income groups in `[Metadata - Countries].IncomeGroup`: `'High income: OECD'`, `'High income: nonOECD'`, `'Low income'`, `'Lower middle income'`, `'Upper middle income'`

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| country identifier | `[Country Code]` (ISO 3166-1 alpha-3) |
| indicator type | `[Indicator Code]` or `[Indicator Name]` |
| year value | Column name `1960`–`2011` (DOUBLE) or `2012` in target table |
| geographic region | `[Metadata - Countries].Region` |
| development level | `[Metadata - Countries].IncomeGroup` |
| indicator definition | `[Metadata - Indicators].SOURCE_NOTE` |
| data source | `[Metadata - Indicators].SOURCE_ORGANIZATION` |
| forecast 2012 | `Countries.target.[2012]` |

---

## Table Reference

### `Countries.Data`
**Meaning:** Annual indicator values by country (1960–2011).

| Column | Notes |
|--------|-------|
| `Country Code` | ISO 3166-1 alpha-3 code; join key to metadata tables |
| `Country Name` | Informational only; use `Country Code` for joins |
| `Indicator Code` | World Bank indicator code; join key to `[Metadata - Indicators]` |
| `Indicator Name` | Informational; full definition in metadata |
| `1960`–`2011` | DOUBLE columns; NULL indicates no data for that year |

---

### `Countries.[Metadata - Countries]`
**Meaning:** Country attributes and classifications.

| Column | Notes |
|--------|-------|
| `Country Code` | ISO 3166-1 alpha-3; join key to Data table |
| `Region` | Enum: `'East Asia & Pacific'`, `'Europe & Central Asia'`, `'Latin America & Caribbean'`, `'Middle East & North Africa'`, `'North America'`, `'South Asia'`, `'Sub-Saharan Africa'` |
| `IncomeGroup` | Enum: `'High income: OECD'`, `'High income: nonOECD'`, `'Low income'`, `'Lower middle income'`, `'Upper middle income'` |
| `SpecialNotes` | Fiscal year, data caveats, or reporting period notes; may be NULL |

---

### `Countries.[Metadata - Indicators]`
**Meaning:** Indicator definitions and sources.

| Column | Notes |
|--------|-------|
| `INDICATOR_CODE` | World Bank code; join key to Data table |
| `INDICATOR_NAME` | Full indicator name |
| `SOURCE_NOTE` | Definition and methodology; specifies if nominal, PPP-adjusted, or other adjustment |
| `SOURCE_ORGANIZATION` | Data provider (e.g., FAO, World Bank, IMF) |

---

### `Countries.target`
**Meaning:** 2012 forecast values (one row per country).

| Column | Notes |
|--------|-------|
| `Country Code` | ISO 3166-1 alpha-3; join key to Data and metadata |
| `2012` | DOUBLE; forecast value for 2012 |