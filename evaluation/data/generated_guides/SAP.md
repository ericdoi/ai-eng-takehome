# SAP Schema Reference Guide

## Schema Summary
Customer demographic and behavioral data with mailing campaign responses and sales transactions, linked by customer ID and reference ID.

---

## Join Paths

**Customers to Demographics:**
```sql
FROM SAP.Customers c
JOIN SAP.Demog d ON c.GEOID = d.GEOID
```

**Customers to Mailing Campaigns (Mailings1_2):**
```sql
FROM SAP.Customers c
JOIN SAP.Mailings1_2 m ON c.ID = m.REFID
```

**Customers to Mailing Campaigns (mailings3):**
```sql
FROM SAP.Customers c
JOIN SAP.mailings3 m ON c.ID = m.REFID
```

**Mailing Campaigns to Sales:**
```sql
FROM SAP.Mailings1_2 m
JOIN SAP.Sales s ON m.REFID = s.REFID
```

**Customers to Sales (via Mailings1_2):**
```sql
FROM SAP.Customers c
JOIN SAP.Mailings1_2 m ON c.ID = m.REFID
JOIN SAP.Sales s ON m.REFID = s.REFID
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| customer segment | `SAP.Customers.OCCUPATION` |
| gender | `SAP.Customers.SEX` |
| marital status | `SAP.Customers.MARITAL_STATUS` |
| education level | `SAP.Customers.EDUCATIONNUM` |
| geographic area | `SAP.Customers.GEOID` or `SAP.Demog.GEOID` |
| area income | `SAP.Demog.INCOME_K` |
| area population | `SAP.Demog.INHABITANTS_K` |
| campaign response | `SAP.Mailings1_2.RESPONSE` or `SAP.mailings3.RESPONSE` |
| campaign date | `SAP.Mailings1_2.REF_DATE` or `SAP.mailings3.REF_DATE` |
| transaction amount | `SAP.Sales.AMOUNT` |
| transaction date | `SAP.Sales.EVENT_DATE` |

---

## Table Reference

### `SAP.Customers`
**Meaning:** Individual customer records with demographics and attributes.

| Column | Notes |
|--------|-------|
| `ID` | Primary key; links to `REFID` in mailing and sales tables |
| `SEX` | Enum: `Female`, `Male` |
| `MARITAL_STATUS` | Enum: `Divorced`, `Married-civ-spouse`, `Never-married`, `Other`, `Widowed` |
| `GEOID` | Foreign key to `SAP.Demog`; geographic area identifier |
| `EDUCATIONNUM` | Numeric education level (no scale provided) |
| `OCCUPATION` | Enum: `Adm-clerical`, `Craft-repair`, `Exec-managerial`, `Farming-fishing`, `Handlers-cleaners`, `Machine-op-inspct`, `Other-service`, `Prof-specialty`, `Sales` |
| `DATA1`, `DATA2`, `DATA3` | Numeric attributes (semantics unclear) |
| `NOM1`, `NOM2`, `NOM3` | Categorical attributes; `NOM2` has values `e–x` |
| `age` | Customer age in years |

---

### `SAP.Demog`
**Meaning:** Geographic area demographic and economic data.

| Column | Notes |
|--------|-------|
| `GEOID` | Primary key; links to `SAP.Customers.GEOID` |
| `INHABITANTS_K` | Population in thousands |
| `INCOME_K` | Average income in thousands |
| `A_VAR1` – `A_VAR18` | Area-level numeric attributes (semantics unclear) |

---

### `SAP.Mailings1_2`
**Meaning:** Mailing campaign 1 and 2 records with customer response tracking.

| Column | Notes |
|--------|-------|
| `REFID` | Foreign key to `SAP.Customers.ID` |
| `KxIndex` | Campaign sequence or batch identifier |
| `REF_DATE` | Campaign send date |
| `RESPONSE` | Enum: `true`, `false` |

---

### `SAP.mailings3`
**Meaning:** Mailing campaign 3 records with customer response tracking.

| Column | Notes |
|--------|-------|
| `REFID` | Foreign key to `SAP.Customers.ID` |
| `REF_DATE` | Campaign send date |
| `RESPONSE` | Enum: `true`, `false` |

---

### `SAP.Sales`
**Meaning:** Transaction records linked to mailing campaigns.

| Column | Notes |
|--------|-------|
| `EVENTID` | Primary key |
| `REFID` | Foreign key to `SAP.Mailings1_2.REFID` (and `SAP.Customers.ID`) |
| `EVENT_DATE` | Transaction date |
| `AMOUNT` | Transaction amount in currency units |