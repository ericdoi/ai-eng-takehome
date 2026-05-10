# SAP Schema Reference Guide

## Schema Summary
This schema contains customer demographic data, mailing campaign responses, and sales transactions, with geographic and personal attributes linked through customer and reference IDs.

---

## Table Reference

### SAP.Customers
**Meaning:** Individual customer records with personal attributes and demographic identifiers.
**Synonyms:** People, Individuals, Persons

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| ID | BIGINT | Unique customer identifier | CustomerID, PersonID |
| SEX | VARCHAR | Gender | Gender |
| MARITAL_STATUS | VARCHAR | Marital status | MaritalStatus, Relationship |
| GEOID | BIGINT | Geographic area identifier | GeoID, LocationID, AreaID |
| EDUCATIONNUM | BIGINT | Education level (numeric code) | EducationLevel, EduCode |
| OCCUPATION | VARCHAR | Job category | Job, Profession, Career |
| DATA1 | DOUBLE | Numeric attribute 1 | Metric1, Value1 |
| DATA2 | DOUBLE | Numeric attribute 2 | Metric2, Value2 |
| DATA3 | DOUBLE | Numeric attribute 3 | Metric3, Value3 |
| NOM1 | VARCHAR | Categorical attribute 1 | Category1, Code1 |
| NOM2 | VARCHAR | Categorical attribute 2 | Category2, Code2 |
| NOM3 | VARCHAR | Categorical attribute 3 | Category3, Code3 |
| age | BIGINT | Customer age in years | Age, CustomerAge |

**Notable Values:**
- SEX: `Female`, `Male`
- MARITAL_STATUS: `Divorced`, `Married-civ-spouse`, `Never-married`, `Other`, `Widowed`
- OCCUPATION: `Adm-clerical`, `Craft-repair`, `Exec-managerial`, `Farming-fishing`, `Handlers-cleaners`, `Machine-op-inspct`, `Other-service`, `Prof-specialty`, `Sales`
- NOM2: `e`, `g`, `h`, `i`, `j`, `k`, `l`, `m`, `n`, `o`, `p`, `q`, `r`, `s`, `t`, `u`, `v`, `w`, `x`

---

### SAP.Demog
**Meaning:** Geographic demographic and economic data aggregated by geographic area.
**Synonyms:** Demographics, Geographic Data, Area Data

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| GEOID | BIGINT | Geographic area identifier | GeoID, LocationID, AreaID |
| INHABITANTS_K | DOUBLE | Population in thousands | Population, PopulationK, Inhabitants |
| INCOME_K | DOUBLE | Average income in thousands | AvgIncome, IncomeK, MedianIncome |
| A_VAR1–A_VAR18 | DOUBLE | Area-level demographic variables | AreaVar1–AreaVar18, DemoVar1–DemoVar18 |

---

### SAP.Mailings1_2
**Meaning:** Mailing campaign records for campaigns 1 and 2 with customer response tracking.
**Synonyms:** Campaign1_2, MailingCampaign, CampaignResponse

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| REFID | BIGINT | Reference/customer identifier | ReferenceID, CustomerRef, ID |
| KxIndex | BIGINT | Campaign sequence or batch index | CampaignIndex, BatchID, SequenceNum |
| REF_DATE | TIMESTAMP | Mailing send date and time | MailDate, SendDate, CampaignDate |
| RESPONSE | VARCHAR | Customer response indicator | Responded, ResponseFlag, Result |

**Notable Values:**
- RESPONSE: `false`, `true`

---

### SAP.Sales
**Meaning:** Individual sales transactions linked to customers via mailing campaigns.
**Synonyms:** Transactions, Orders, Purchases

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| EVENTID | BIGINT | Unique transaction identifier | TransactionID, OrderID, SaleID |
| REFID | BIGINT | Reference/customer identifier | ReferenceID, CustomerRef, ID |
| EVENT_DATE | TIMESTAMP | Transaction date and time | SaleDate, PurchaseDate, TransactionDate |
| AMOUNT | DOUBLE | Transaction amount in currency units | SaleAmount, Revenue, Price, Total |

---

### SAP.mailings3
**Meaning:** Mailing campaign records for campaign 3 with customer response tracking.
**Synonyms:** Campaign3, MailingCampaign3, CampaignResponse3

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| REFID | BIGINT | Reference/customer identifier | ReferenceID, CustomerRef, ID |
| REF_DATE | TIMESTAMP | Mailing send date and time | MailDate, SendDate, CampaignDate |
| RESPONSE | VARCHAR | Customer response indicator | Responded, ResponseFlag, Result |

**Notable Values:**
- RESPONSE: `false`, `true`

---

## Join Paths

| From | To | Condition |
|------|----|-----------| 
| SAP.Customers | SAP.Demog | `Customers.GEOID = Demog.GEOID` |
| SAP.Customers | SAP.Mailings1_2 | `Customers.ID = Mailings1_2.REFID` |
| SAP.Customers | SAP.mailings3 | `Customers.ID = mailings3.REFID` |
| SAP.Mailings1_2 | SAP.Sales | `Mailings1_2.REFID = Sales.REFID` |
| SAP.mailings3 | SAP.Sales | `mailings3.REFID = Sales.REFID` |

---

## Business Rules as SQL

No explicit business rules provided in schema documentation. Apply standard data validation:
- RESPONSE values are strictly `true` or `false` (string comparison)
- GEOID links Customers to Demog; missing GEOID values indicate unmatched geographic areas
- REFID in Mailings1_2 and mailings3 must match Customers.ID to associate campaigns with customers
- REFID in Sales must match Mailings1_2.REFID or mailings3.REFID to link transactions to campaigns

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| customer age | `Customers.age` |
| customer gender | `Customers.SEX` |
| marital status | `Customers.MARITAL_STATUS` |
| job/occupation | `Customers.OCCUPATION` |
| education level | `Customers.EDUCATIONNUM` |
| geographic area | `Customers.GEOID` or `Demog.GEOID` |
| population | `Demog.INHABITANTS_K` |
| area income | `Demog.INCOME_K` |
| mailing response | `Mailings1_2.RESPONSE` or `mailings3.RESPONSE` |
| campaign 1 or 2 | `SAP.Mailings1_2` |
| campaign 3 | `SAP.mailings3` |
| mailing date | `Mailings1_2.REF_DATE` or `mailings3.REF_DATE` |
| sale amount | `Sales.AMOUNT` |
| sale date | `Sales.EVENT_DATE` |
| responded to mailing | `WHERE RESPONSE = 'true'` |
| did not respond | `WHERE RESPONSE = 'false'` |
| total sales by customer | `SUM(Sales.AMOUNT) GROUP BY Sales.REFID` |
| average area income | `AVG(Demog.INCOME_K)` |
| customer count by occupation | `COUNT(Customers.ID) GROUP BY Customers.OCCUPATION` |