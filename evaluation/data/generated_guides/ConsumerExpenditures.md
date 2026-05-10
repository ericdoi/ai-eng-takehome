# ConsumerExpenditures Schema Reference Guide

## 1. Schema Summary

This schema contains household-level consumer expenditure survey data with monthly spending records, household demographics, and member characteristics for market research analysis.

---

## 2. Join Paths

**Expenditures to Households (by household and year):**
```sql
FROM ConsumerExpenditures.EXPENDITURES e
JOIN ConsumerExpenditures.HOUSEHOLDS h 
  ON e.HOUSEHOLD_ID = h.HOUSEHOLD_ID 
  AND e.YEAR = h.YEAR
```

**Expenditures to Household Members (by household and year):**
```sql
FROM ConsumerExpenditures.EXPENDITURES e
JOIN ConsumerExpenditures.HOUSEHOLD_MEMBERS m 
  ON e.HOUSEHOLD_ID = m.HOUSEHOLD_ID 
  AND e.YEAR = m.YEAR
```

**All three tables (full household context):**
```sql
FROM ConsumerExpenditures.EXPENDITURES e
JOIN ConsumerExpenditures.HOUSEHOLDS h 
  ON e.HOUSEHOLD_ID = h.HOUSEHOLD_ID 
  AND e.YEAR = h.YEAR
JOIN ConsumerExpenditures.HOUSEHOLD_MEMBERS m 
  ON e.HOUSEHOLD_ID = m.HOUSEHOLD_ID 
  AND e.YEAR = m.YEAR
```

---

## 3. Business Rules as SQL

| Rule | SQL Condition |
|------|---------------|
| Essential spending categories | `WHERE e.PRODUCT_CODE IN ('010210', '040510', '190211', '190321', ...)` (housing, food, utilities, healthcare, work transport) |
| Discretionary spending categories | `WHERE e.PRODUCT_CODE IN (...)` (entertainment, dining, travel, personal care, apparel) |
| Gift expenditures (Q4 decomposition) | `WHERE e.GIFT = 1` |
| Training/education expenditures | `WHERE e.IS_TRAINING = 1` |
| Household has children | `WHERE EXISTS (SELECT 1 FROM ConsumerExpenditures.HOUSEHOLD_MEMBERS m WHERE m.HOUSEHOLD_ID = h.HOUSEHOLD_ID AND m.YEAR = h.YEAR AND m.AGE < 18)` |
| Single-person household | `WHERE (SELECT COUNT(*) FROM ConsumerExpenditures.HOUSEHOLD_MEMBERS m WHERE m.HOUSEHOLD_ID = h.HOUSEHOLD_ID AND m.YEAR = h.YEAR) = 1` |
| Suppress low-count cells | `HAVING COUNT(*) >= 30` |
| Flag zero-income with spending | `WHERE h.INCOME_RANK = 0 AND SUM(e.COST) > 0` |

---

## 4. Synonym Glossary

| Common Term | Schema Reference |
|-------------|------------------|
| Total household spending | `SUM(ConsumerExpenditures.EXPENDITURES.COST)` |
| Per-capita spending | `SUM(ConsumerExpenditures.EXPENDITURES.COST) / (SELECT COUNT(*) FROM ConsumerExpenditures.HOUSEHOLD_MEMBERS m WHERE m.HOUSEHOLD_ID = h.HOUSEHOLD_ID AND m.YEAR = h.YEAR)` |
| Household head age | `ConsumerExpenditures.HOUSEHOLDS.AGE_REF` |
| Income percentile | `ConsumerExpenditures.HOUSEHOLDS.INCOME_RANK` |
| Income quintile 1–5 | `ConsumerExpenditures.HOUSEHOLDS.INCOME_RANK_1` through `INCOME_RANK_5` |
| Average income rank | `ConsumerExpenditures.HOUSEHOLDS.INCOME_RANK_MEAN` |
| Gift spending | `WHERE ConsumerExpenditures.EXPENDITURES.GIFT = 1` |
| Training/education spending | `WHERE ConsumerExpenditures.EXPENDITURES.IS_TRAINING = 1` |
| Member marital status | `ConsumerExpenditures.HOUSEHOLD_MEMBERS.MARITAL` (values: 1, 2, 3, 4, 5) |
| Member gender | `ConsumerExpenditures.HOUSEHOLD_MEMBERS.SEX` (values: 1, 2) |
| Member employment status | `ConsumerExpenditures.HOUSEHOLD_MEMBERS.WORK_STATUS` (values: 1, 2, 3) |

---

## 5. Table Reference

### `ConsumerExpenditures.EXPENDITURES`
**Meaning:** Monthly spending transactions by household.  
**Synonyms:** transactions, spending records, purchases.

| Column | Semantics |
|--------|-----------|
| `EXPENDITURE_ID` | Unique transaction identifier |
| `HOUSEHOLD_ID` | Foreign key to HOUSEHOLDS |
| `YEAR` | Survey year; use with HOUSEHOLD_ID for temporal join |
| `MONTH` | Calendar month (1–12) |
| `PRODUCT_CODE` | Commodity classification code; determines spending category (essential vs. discretionary) |
| `COST` | Expenditure amount in dollars; always non-negative |
| `GIFT` | Binary flag (0 = personal, 1 = gift); use for Q4 decomposition |
| `IS_TRAINING` | Binary flag (0 = regular, 1 = education/training); identifies human capital investment |

---

### `ConsumerExpenditures.HOUSEHOLDS`
**Meaning:** Household-level demographics and income distribution.  
**Synonyms:** household profile, family unit, survey respondent.

| Column | Semantics |
|--------|-----------|
| `HOUSEHOLD_ID` | Unique household identifier; primary key with YEAR |
| `YEAR` | Survey year |
| `INCOME_RANK` | Household income percentile (0–1 scale); use for income segmentation |
| `INCOME_RANK_1` through `INCOME_RANK_5` | Income distribution across quintiles; represents income composition or allocation pattern |
| `INCOME_RANK_MEAN` | Mean income rank; use for population-level income estimates |
| `AGE_REF` | Age of household head (highest income earner); use for age-based segmentation, not individual member age |

---

### `ConsumerExpenditures.HOUSEHOLD_MEMBERS`
**Meaning:** Individual member demographics within households.  
**Synonyms:** household roster, family members, respondent details.

| Column | Semantics |
|--------|-----------|
| `HOUSEHOLD_ID` | Foreign key to HOUSEHOLDS |
| `YEAR` | Survey year |
| `MARITAL` | Marital status code; values: 1, 2, 3, 4, 5 (exact mapping not provided; treat as categorical) |
| `SEX` | Gender code; values: 1, 2 (exact mapping not provided; treat as binary categorical) |
| `AGE` | Member age in years; use to identify presence of children (< 18) for household segmentation |
| `WORK_STATUS` | Employment status code; values: 1, 2, 3 (exact mapping not provided; NaN indicates missing); use to identify working vs. non-working households |