# Credit Schema Reference Guide

## Schema Summary
The Credit schema contains credit card operations data including member accounts, charges, payments, statements, merchants (providers), and regional information for a global credit card system.

---

## Table Reference

### Credit.category
**Meaning:** Merchant category classifications for charges.
**Synonyms:** merchant category, spending category, transaction type

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `category_no` | BIGINT | Unique category identifier | category ID |
| `category_desc` | VARCHAR | Category description | category name, type |
| `category_code` | VARCHAR | Category code (currently empty) | code |

**Notable Values (category_desc):** Clothing, Communication, Electronics, Entertainment, Groceries, Home Supplies, Lodging, Meals, Misc, Travel

---

### Credit.charge
**Meaning:** Individual credit card transactions/charges made by members at providers.
**Synonyms:** transaction, purchase, charge record

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `charge_no` | BIGINT | Unique charge identifier | transaction ID, charge ID |
| `member_no` | BIGINT | Member who made the charge | cardholder ID |
| `provider_no` | BIGINT | Merchant/provider where charge occurred | merchant ID, vendor ID |
| `category_no` | BIGINT | Spending category of the charge | category ID |
| `charge_dt` | TIMESTAMP | Date and time charge was posted | transaction date, posting date |
| `charge_amt` | DOUBLE | Amount of the charge in currency units | transaction amount, purchase amount |
| `statement_no` | BIGINT | Statement period this charge belongs to | billing period |
| `charge_code` | VARCHAR | Charge classification code | code, type code |

**Notable Values (charge_code):** 'RF' (refund)

---

### Credit.corporation
**Meaning:** Corporate entities that employ members or sponsor accounts.
**Synonyms:** employer, company, organization

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `corp_no` | BIGINT | Unique corporation identifier | company ID, employer ID |
| `corp_name` | VARCHAR | Corporation name | company name |
| `street` | VARCHAR | Street address | address line 1 |
| `city` | VARCHAR | City | municipality |
| `state_prov` | VARCHAR | State or province | region, state |
| `country` | VARCHAR | Country | nation |
| `mail_code` | VARCHAR | Postal code | zip code, postal code |
| `phone_no` | VARCHAR | Phone number | contact number |
| `expr_dt` | TIMESTAMP | Expiration/end date | expiry date, end date |
| `region_no` | BIGINT | Geographic region | region ID |
| `corp_code` | VARCHAR | Corporation code | code |

---

### Credit.member
**Meaning:** Credit card members/cardholders and their account information.
**Synonyms:** cardholder, account holder, customer, user

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `member_no` | BIGINT | Unique member identifier | member ID, cardholder ID, account ID |
| `lastname` | VARCHAR | Member's last name | surname, family name |
| `firstname` | VARCHAR | Member's first name | given name |
| `middleinitial` | VARCHAR | Middle initial | middle name initial |
| `street` | VARCHAR | Street address | address line 1 |
| `city` | VARCHAR | City | municipality |
| `state_prov` | VARCHAR | State or province | region, state |
| `country` | VARCHAR | Country | nation |
| `mail_code` | VARCHAR | Postal code | zip code, postal code |
| `phone_no` | VARCHAR | Phone number | contact number |
| `photograph` | BLOB | Member photograph | photo, image |
| `issue_dt` | TIMESTAMP | Card issue date | card start date |
| `expr_dt` | TIMESTAMP | Card expiration date | card end date, expiry date |
| `region_no` | BIGINT | Geographic region | region ID |
| `corp_no` | BIGINT | Sponsoring corporation | employer ID, company ID |
| `prev_balance` | DOUBLE | Previous statement balance | prior balance |
| `curr_balance` | DOUBLE | Current account balance | current balance, balance due |
| `member_code` | VARCHAR | Member code | code |

---

### Credit.payment
**Meaning:** Payments made by members toward their credit card balances.
**Synonyms:** payment record, payment transaction, remittance

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `payment_no` | BIGINT | Unique payment identifier | payment ID |
| `member_no` | BIGINT | Member making the payment | cardholder ID |
| `payment_dt` | TIMESTAMP | Date payment was received | payment date, posting date |
| `payment_amt` | DOUBLE | Payment amount in currency units | amount paid |
| `statement_no` | BIGINT | Statement period this payment applies to | billing period |
| `payment_code` | VARCHAR | Payment code/type | code |

---

### Credit.provider
**Meaning:** Merchants/vendors where members can make charges.
**Synonyms:** merchant, vendor, business, establishment

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `provider_no` | BIGINT | Unique provider identifier | merchant ID, vendor ID |
| `provider_name` | VARCHAR | Provider/merchant name | merchant name, business name |
| `street` | VARCHAR | Street address | address line 1 |
| `city` | VARCHAR | City | municipality |
| `state_prov` | VARCHAR | State or province | region, state |
| `mail_code` | VARCHAR | Postal code | zip code, postal code |
| `country` | VARCHAR | Country | nation |
| `phone_no` | VARCHAR | Phone number | contact number |
| `issue_dt` | TIMESTAMP | Provider enrollment date | start date |
| `expr_dt` | TIMESTAMP | Provider expiration date | end date, expiry date |
| `region_no` | BIGINT | Geographic region | region ID |
| `provider_code` | VARCHAR | Provider code | code |

---

### Credit.region
**Meaning:** Geographic regions for organizing members, providers, and corporations.
**Synonyms:** geographic region, territory, area

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `region_no` | BIGINT | Unique region identifier | region ID |
| `region_name` | VARCHAR | Region name | region description |
| `street` | VARCHAR | Region office street address | address line 1 |
| `city` | VARCHAR | Region office city | municipality |
| `state_prov` | VARCHAR | Region office state/province | state, region |
| `country` | VARCHAR | Region office country | nation |
| `mail_code` | VARCHAR | Region office postal code | zip code, postal code |
| `phone_no` | VARCHAR | Region office phone | contact number |
| `region_code` | VARCHAR | Region code | code |

**Notable Values (region_name):** Africa, China, Eastern Europea, Japan, Mid East / Sout, North American, Scandanavian, South American, Western Europea

---

### Credit.statement
**Meaning:** Monthly billing statements for members summarizing charges and payments.
**Synonyms:** billing statement, bill, invoice, statement period

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `statement_no` | BIGINT | Unique statement identifier | statement ID, billing period ID |
| `member_no` | BIGINT | Member this statement belongs to | cardholder ID |
| `statement_dt` | TIMESTAMP | Statement generation date | billing date, statement date |
| `due_dt` | TIMESTAMP | Payment due date | due date |
| `statement_amt` | DOUBLE | Total statement amount due | statement balance, amount due |
| `statement_code` | VARCHAR | Statement code | code |

---

## Join Paths

| From | To | Join Condition |
|------|----|----|
| `charge` | `member` | `charge.member_no = member.member_no` |
| `charge` | `provider` | `charge.provider_no = provider.provider_no` |
| `charge` | `category` | `charge.category_no = category.category_no` |
| `charge` | `statement` | `charge.statement_no = statement.statement_no` |
| `member` | `region` | `member.region_no = region.region_no` |
| `member` | `corporation` | `member.corp_no = corporation.corp_no` |
| `member` | `statement` | `member.member_no = statement.member_no` |
| `member` | `payment` | `member.member_no = payment.member_no` |
| `provider` | `region` | `provider.region_no = region.region_no` |
| `corporation` | `region` | `corporation.region_no = region.region_no` |
| `payment` | `statement` | `payment.statement_no = statement.statement_no` |
| `statement` | `region` | `statement.member_no = member.member_no AND member.region_no = region.region_no` |

---

## Business Rules as SQL

### Charge Classification

**Rule: Refunds should be subtracted from gross charge volume, not counted separately**
```sql
WHERE charge.charge_code != 'RF'
-- OR for refund-adjusted totals:
SUM(CASE WHEN charge.charge_code = 'RF' THEN -charge.charge_amt ELSE charge.charge_amt END)
```

**Rule: Micro-transactions (under $5.00) excluded from average transaction value calculations**
```sql
WHERE charge.charge_amt >= 5.00
```

**Rule: Test transactions ($0.01 exactly) excluded from all analytics**
```sql
WHERE charge.charge_amt != 0.01
```

### Member Segmentation

**Rule: Inactive members have fewer than 3 charges in a 12-month period**
```sql
HAVING COUNT(charge.charge_no) < 3
-- AND charge.charge_dt >= CURRENT_DATE - INTERVAL '12 months'
```

**Rule: Premium members have lifetime charges exceeding $10,000**
```sql
WHERE SUM(charge.charge_amt) > 10000.00
```

**Rule: Members without charges in current statement period excluded from transacting members**
```sql
WHERE member.member_no IN (
  SELECT DISTINCT charge.member_no 
  FROM charge 
  WHERE charge.statement_no = [current_statement_no]
)
```

### Provider Analysis

**Rule: Categories 1-10 are Essential spending**
```sql
WHERE category.category_no BETWEEN 1 AND 10
```

**Rule: Categories 11-20 are Discretionary spending**
```sql
WHERE category.category_no BETWEEN 11 AND 20
```

**Rule: Categories 21+ are Other**
```sql
WHERE category.category_no >= 21
```

**Rule: Exclude providers with fewer than 100 total charges from individual reporting**
```sql
HAVING COUNT(charge.charge_no) >= 100
-- Aggregate others as "Long tail providers"
```

### Statement Reconciliation

**Rule: Statement amount should equal sum of charges minus sum of refunds**
```sql
statement.statement_amt = (
  SELECT SUM(CASE WHEN charge.charge_code = 'RF' THEN -charge.charge_amt ELSE charge.charge_amt END)
  FROM charge
  WHERE charge.statement_no = statement.statement_no
)
```

**Rule: Flag statements with negative balances**
```sql
WHERE statement.statement_amt < 0
```

**Rule: Month-end statements (28th-31st) use statement_no for period assignment, not charge_dt**
```sql
-- Use: charge.statement_no
-- NOT: EXTRACT(MONTH FROM charge.charge_dt)
```

### Fraud Rules

**Rule: Charge over $5,000 followed by refund within 24 hours flags fraud review**
```sql
WHERE charge.charge_amt > 5000.00
  AND EXISTS (
    SELECT 1 FROM charge c2
    WHERE c2.charge_code = 'RF'
      AND c2.provider_no = charge.provider_no
      AND c2.member_no = charge.member_no
      AND c2.charge_dt > charge.charge_dt
      AND c2.charge_dt <= charge.charge_dt + INTERVAL '24 hours'
  )
```

**Rule: Multiple charges from same provider within 60 seconds indicate duplicate processing**
```sql
WHERE (
  SELECT COUNT(*)
  FROM charge c2
  WHERE c2.provider_no = charge.provider_no
    AND c2.member_no = charge.member_no
    AND c2.charge_dt > charge.charge_dt
    AND c2.charge_dt <= charge.charge_dt + INTERVAL '60 seconds'
) > 1
```

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| active member | `member.member_no` with `COUNT(charge.charge_no) >= 3` in 12-month period |
| average transaction value | `AVG(charge.charge_amt)` WHERE `charge.charge_amt >= 5.00` AND `charge.charge_amt != 0.01` AND `charge.charge_code != 'RF'` |
| balance due | `member.curr_balance` or `statement.statement_amt` |
| billing period | `statement.statement_no` |
| cardholder | `member.member_no` |
| charge volume | `SUM(charge.charge_amt)` WHERE `charge.charge_code != 'RF'` |
| current balance | `member.curr_balance` |
| customer | `member.member_no` |
| discretionary spending | `charge` WHERE `category.category_no BETWEEN 11 AND 20` |
| duplicate charge | Multiple `charge` records with same `provider_no`, `member_no` within 60 seconds |
| essential spending | `charge` WHERE `category.category_no BETWEEN 1 AND 10` |
| fraud flag | `charge.charge_amt > 5000.00` followed by `charge.charge_code = 'RF'` within 24 hours |
| inactive member | `member.member_no` with `COUNT(charge.charge_no) < 3` in 12-month period |
| long tail provider | `provider.provider_no` with `COUNT(charge.charge_no) < 100` |
| merchant | `provider.provider_no` |
| micro-transaction | `charge` WHERE `charge.charge_amt < 5.00` |
| payment | `payment.payment_no` |
| premium member | `member.member_no` with `SUM(charge.charge_amt) > 10000.00` |
| prior balance | `member.prev_balance` |
| refund | `charge` WHERE `charge.charge_code = 'RF'` |
| spending category | `category.category_no` |
| statement balance | `statement.statement_amt` |
| test transaction | `charge` WHERE `charge.charge_amt = 0.01` |
| transaction | `charge.charge_no` |
| transacting member | `member.member_no` with at least one `charge` in current `statement.statement_no` |
| vendor | `provider.provider_no` |