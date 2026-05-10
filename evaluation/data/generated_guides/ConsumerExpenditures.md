# ConsumerExpenditures Schema Reference Guide

## Schema Summary

The ConsumerExpenditures schema contains household-level consumer spending data, household demographics and income rankings, and individual household member characteristics across multiple years and months.

---

## Table Reference

### Table: `ConsumerExpenditures.EXPENDITURES`

**Meaning:** Individual expenditure transactions recorded by household, month, and product category.

**Synonyms:** Spending records, transactions, purchase data

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `EXPENDITURE_ID` | VARCHAR | Unique identifier for each expenditure record | Transaction ID, expense ID |
| `HOUSEHOLD_ID` | VARCHAR | Foreign key linking to household | HH ID, household identifier |
| `YEAR` | BIGINT | Calendar year of expenditure | Survey year |
| `MONTH` | BIGINT | Calendar month (1–12) of expenditure | Survey month |
| `PRODUCT_CODE` | VARCHAR | Classification code for product/service category | Category code, product category |
| `COST` | DOUBLE | Dollar amount spent | Amount, expenditure amount, spending |
| `GIFT` | BIGINT | Binary flag: 1 = gift purchase, 0 = personal use | Gift indicator, is_gift |
| `IS_TRAINING` | BIGINT | Binary flag: 1 = training/education expense, 0 = other | Training indicator, education flag |

**Notable Values:**
- `GIFT`: 0 (personal use), 1 (gift)
- `IS_TRAINING`: 0 (non-training), 1 (training/education)

---

### Table: `ConsumerExpenditures.HOUSEHOLDS`

**Meaning:** Household-level demographic and income ranking data, one record per household per year.

**Synonyms:** Household roster, household profile, household characteristics

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `HOUSEHOLD_ID` | VARCHAR | Unique household identifier | HH ID, household identifier |
| `YEAR` | BIGINT | Calendar year of observation | Survey year |
| `INCOME_RANK` | DOUBLE | Overall income percentile rank (0–1 scale) | Income percentile, income rank overall |
| `INCOME_RANK_1` | DOUBLE | Income rank quintile 1 (lowest 20%) | Q1 income rank |
| `INCOME_RANK_2` | DOUBLE | Income rank quintile 2 (20–40%) | Q2 income rank |
| `INCOME_RANK_3` | DOUBLE | Income rank quintile 3 (40–60%) | Q3 income rank, median income rank |
| `INCOME_RANK_4` | DOUBLE | Income rank quintile 4 (60–80%) | Q4 income rank |
| `INCOME_RANK_5` | DOUBLE | Income rank quintile 5 (highest 20%) | Q5 income rank, top income rank |
| `INCOME_RANK_MEAN` | DOUBLE | Mean income rank across all quintiles | Average income rank |
| `AGE_REF` | BIGINT | Age of household reference person (head of household) | Reference age, head age, household head age |

**Notable Values:**
- `INCOME_RANK*` columns: Range 0.0–1.0 (proportional representation within quintile)
- `AGE_REF`: Integer age in years

---

### Table: `ConsumerExpenditures.HOUSEHOLD_MEMBERS`

**Meaning:** Individual member-level demographics within households, one record per member per year.

**Synonyms:** Member roster, household composition, member characteristics

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `HOUSEHOLD_ID` | VARCHAR | Foreign key linking to household | HH ID, household identifier |
| `YEAR` | BIGINT | Calendar year of observation | Survey year |
| `MARITAL` | VARCHAR | Marital status code | Marital status, relationship status |
| `SEX` | VARCHAR | Gender code | Gender, sex code |
| `AGE` | BIGINT | Age of household member in years | Member age, person age |
| `WORK_STATUS` | VARCHAR | Employment/work status code | Employment status, labor status |

**Notable Values:**
- `MARITAL`: 1, 2, 3, 4, 5 (exact meanings not provided; treat as categorical)
- `SEX`: 1, 2 (exact mapping not provided; treat as binary categorical)
- `WORK_STATUS`: 1, 2, 3 (exact meanings not provided; treat as categorical); NaN (missing/not applicable)

---

## Join Paths

### EXPENDITURES ↔ HOUSEHOLDS
```sql
EXPENDITURES e
INNER JOIN HOUSEHOLDS h
  ON e.HOUSEHOLD_ID = h.HOUSEHOLD_ID
  AND e.YEAR = h.YEAR
```

### EXPENDITURES ↔ HOUSEHOLD_MEMBERS
```sql
EXPENDITURES e
INNER JOIN HOUSEHOLD_MEMBERS m
  ON e.HOUSEHOLD_ID = m.HOUSEHOLD_ID
  AND e.YEAR = m.YEAR
```

### HOUSEHOLDS ↔ HOUSEHOLD_MEMBERS
```sql
HOUSEHOLDS h
INNER JOIN HOUSEHOLD_MEMBERS m
  ON h.HOUSEHOLD_ID = m.HOUSEHOLD_ID
  AND h.YEAR = m.YEAR
```

### Three-table join (EXPENDITURES, HOUSEHOLDS, HOUSEHOLD_MEMBERS)
```sql
EXPENDITURES e
INNER JOIN HOUSEHOLDS h
  ON e.HOUSEHOLD_ID = h.HOUSEHOLD_ID
  AND e.YEAR = h.YEAR
INNER JOIN HOUSEHOLD_MEMBERS m
  ON h.HOUSEHOLD_ID = m.HOUSEHOLD_ID
  AND h.YEAR = m.YEAR
```

---

## Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| **Household is unit of analysis** | `GROUP BY h.HOUSEHOLD_ID, h.YEAR` (aggregate expenditures by household) |
| **Per-capita spending** | `SUM(e.COST) / COUNT(DISTINCT m.HOUSEHOLD_ID)` or use household member count |
| **Single-person households** | `HAVING COUNT(DISTINCT m.HOUSEHOLD_ID) = 1` |
| **Multi-person households** | `HAVING COUNT(DISTINCT m.HOUSEHOLD_ID) > 1` |
| **Household head age** | Use `h.AGE_REF` (not individual member age) for household-level segmentation |
| **Presence of children** | `WHERE m.AGE < 18` (join to HOUSEHOLD_MEMBERS, flag households with any member under 18) |
| **Gift spending** | `WHERE e.GIFT = 1` |
| **Non-gift spending** | `WHERE e.GIFT = 0` |
| **Training/education spending** | `WHERE e.IS_TRAINING = 1` |
| **Non-training spending** | `WHERE e.IS_TRAINING = 0` |
| **Q4 (holiday quarter)** | `WHERE e.MONTH IN (10, 11, 12)` |
| **Suppress unreliable cells** | `HAVING COUNT(DISTINCT e.EXPENDITURE_ID) >= 30` (unweighted observation count) |
| **Income rank by quintile** | Use `h.INCOME_RANK_1` through `h.INCOME_RANK_5` for quintile-specific analysis |
| **Top income bracket** | `WHERE h.INCOME_RANK_5 > threshold` (analyze separately as unbounded) |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| Total household spending | `SUM(e.COST)` grouped by `h.HOUSEHOLD_ID, h.YEAR` |
| Monthly spending | `SUM(e.COST)` grouped by `h.HOUSEHOLD_ID, e.YEAR, e.MONTH` |
| Spending by category | `SUM(e.COST)` grouped by `e.PRODUCT_CODE` |
| Gift purchases | `WHERE e.GIFT = 1` |
| Personal spending | `WHERE e.GIFT = 0` |
| Education spending | `WHERE e.IS_TRAINING = 1` |
| Household income level | `h.INCOME_RANK` or quintile columns `h.INCOME_RANK_1` through `h.INCOME_RANK_5` |
| Household head age | `h.AGE_REF` |
| Member age | `m.AGE` |
| Household composition | `COUNT(DISTINCT m.HOUSEHOLD_ID)` per household |
| Children in household | `COUNT(DISTINCT m.HOUSEHOLD_ID) WHERE m.AGE < 18` |
| Spending share | `SUM(e.COST) / SUM(SUM(e.COST)) OVER (PARTITION BY h.HOUSEHOLD_ID, h.YEAR)` |
| Average spending per household | `AVG(SUM(e.COST))` grouped by household |
| Spending by income quintile | `SUM(e.COST)` grouped by `h.INCOME_RANK_1` through `h.INCOME_RANK_5` |
| Holiday spending | `SUM(e.COST) WHERE e.MONTH IN (10, 11, 12)` |
| Year-over-year comparison | Join EXPENDITURES on same household across different `e.YEAR` values |