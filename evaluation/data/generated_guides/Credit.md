# Credit Schema Reference Guide

## Schema Summary
This schema tracks credit card member accounts, charges, payments, and statements across providers and regions, with business rules for charge classification, member segmentation, and fraud detection.

---

## Join Paths

### Member → Charge
```sql
FROM Credit.member m
JOIN Credit.charge c ON m.member_no = c.member_no
```
**[REQUIRED]** — all charge analysis must identify the member.

### Charge → Provider
```sql
FROM Credit.charge c
JOIN Credit.provider p ON c.provider_no = p.provider_no
```
**[REQUIRED]** — to filter or group charges by provider.

### Charge → Category
```sql
FROM Credit.charge c
JOIN Credit.category cat ON c.category_no = cat.category_no
```
**[OPTIONAL — display only]** — use `c.category_no` for filtering; join only when `category_desc` is needed in output.

### Charge → Statement
```sql
FROM Credit.charge c
JOIN Credit.statement s ON c.statement_no = s.statement_no
```
**[REQUIRED]** — to assign charges to statement periods (do not use `charge_dt` for period assignment per reconciliation rules).

### Member → Statement
```sql
FROM Credit.member m
JOIN Credit.statement s ON m.member_no = s.member_no
```
**[REQUIRED]** — to reconcile statement amounts.

### Member → Payment
```sql
FROM Credit.member m
JOIN Credit.payment py ON m.member_no = py.member_no
```
**[REQUIRED]** — to analyze payment behavior.

### Member/Provider/Corporation → Region
```sql
FROM Credit.member m
JOIN Credit.region r ON m.region_no = r.region_no
```
**[OPTIONAL — display only]** — use `region_no` for filtering; join only when `region_name` is needed in output.

### Member → Corporation
```sql
FROM Credit.member m
JOIN Credit.corporation c ON m.corp_no = c.corp_no
```
**[OPTIONAL — display only]** — use `corp_no` for filtering; join only when `corp_name` is needed in output.

---

## Business Rules as SQL

### Charge Classification

**IDENTIFY refund:** `WHERE charge_code = 'RF'` — charges marked as refunds must be subtracted from gross volume, not counted as separate transactions.

**EXCLUDE micro-transaction:** `WHERE charge_amt >= 5.0` — exclude charges under $5.00 from average transaction value calculations.

**EXCLUDE test transaction:** `WHERE charge_amt != 0.01` — exclude any charge exactly equal to $0.01 from all analytics.

**Combined refund + micro + test exclusion for valid charges:**
```sql
WHERE charge_code != 'RF' 
  AND charge_amt >= 5.0 
  AND charge_amt != 0.01
```

### Member Segmentation

**IDENTIFY inactive member:** `WHERE member_no IN (SELECT member_no FROM Credit.charge GROUP BY member_no HAVING COUNT(*) < 3)` — members with fewer than 3 charges in a 12-month period.

**IDENTIFY premium member:** `WHERE member_no IN (SELECT member_no FROM Credit.charge GROUP BY member_no HAVING SUM(charge_amt) > 10000)` — members with lifetime charges exceeding $10,000.

**IDENTIFY transacting member (current period):** `WHERE member_no IN (SELECT DISTINCT member_no FROM Credit.charge WHERE statement_no IN (SELECT statement_no FROM Credit.statement WHERE statement_dt >= DATE_TRUNC('month', CURRENT_DATE)))` — members with at least one charge in the current statement period.

**IDENTIFY total member:** `SELECT COUNT(DISTINCT member_no) FROM Credit.member` — all members, including those without charges in current period.

### Provider Analysis

**IDENTIFY essential spending category:** `WHERE category_no BETWEEN 1 AND 10` — categories 1–10 map to essential spending.

**IDENTIFY discretionary spending category:** `WHERE category_no BETWEEN 11 AND 20` — categories 11–20 map to discretionary spending.

**IDENTIFY other spending category:** `WHERE category_no > 20` — categories 21+ map to other.

**EXCLUDE long-tail provider:** `WHERE provider_no NOT IN (SELECT provider_no FROM Credit.charge GROUP BY provider_no HAVING COUNT(*) >= 100)` — exclude providers with fewer than 100 total charges from individual provider-level metrics; aggregate as "Long tail providers."

### Statement Reconciliation

**Statement reconciliation check:**
```sql
SELECT s.statement_no, s.statement_amt,
  SUM(CASE WHEN c.charge_code = 'RF' THEN -c.charge_amt ELSE c.charge_amt END) AS reconciled_amt
FROM Credit.statement s
LEFT JOIN Credit.charge c ON s.statement_no = c.statement_no
GROUP BY s.statement_no, s.statement_amt
HAVING s.statement_amt != SUM(CASE WHEN c.charge_code = 'RF' THEN -c.charge_amt ELSE c.charge_amt END)
```
— statements where `statement_amt` does not equal sum of charges minus refunds indicate reconciliation issues.

**IDENTIFY negative balance statement:** `WHERE statement_amt < 0` — flag for data quality review but do not exclude from reporting.

**IDENTIFY month-end statement (timing difference flag):** `WHERE EXTRACT(DAY FROM charge_dt) BETWEEN 28 AND 31` — use `statement_no` for period assignment, not `charge_dt`.

### Fraud Rules

**IDENTIFY high-value refund pair (fraud flag):** 
```sql
SELECT c1.charge_no, c1.provider_no, c1.charge_amt, c2.charge_no
FROM Credit.charge c1
JOIN Credit.charge c2 ON c1.provider_no = c2.provider_no 
  AND c1.member_no = c2.member_no
  AND c2.charge_code = 'RF'
  AND c2.charge_dt > c1.charge_dt
  AND c2.charge_dt <= c1.charge_dt + INTERVAL '24 hours'
WHERE c1.charge_amt > 5000
  AND c1.charge_code != 'RF'
```
— any charge over $5,000 followed by a refund within 24 hours.

**IDENTIFY duplicate processing (fraud flag):**
```sql
SELECT provider_no, member_no, charge_dt, COUNT(*) AS charge_count
FROM Credit.charge
GROUP BY provider_no, member_no, charge_dt
HAVING COUNT(*) > 1 
  AND MAX(charge_dt) - MIN(charge_dt) <= INTERVAL '60 seconds'
```
— multiple charges from the same provider within 60 seconds.

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| refund | `WHERE charge_code = 'RF'` |
| micro-transaction | `WHERE charge_amt < 5.0` |
| test charge | `WHERE charge_amt = 0.01` |
| inactive member | `HAVING COUNT(charge_no) < 3` |
| premium member | `HAVING SUM(charge_amt) > 10000` |
| active member / transacting member | member with ≥1 charge in current statement period |
| total member | all rows in `Credit.member` |
| essential spending | `category_no BETWEEN 1 AND 10` |
| discretionary spending | `category_no BETWEEN 11 AND 20` |
| long-tail provider | `COUNT(charge_no) < 100` |
| statement reconciliation | `SUM(charges) - SUM(refunds) = statement_amt` |
| fraud flag (high-value refund) | charge > $5,000 + refund within 24 hours |
| fraud flag (duplicate) | multiple charges same provider within 60 seconds |

---

## Table Reference

### `Credit.member`
Member credit card accounts. Synonym: cardholder, account holder.

| Column | Notes |
|--------|-------|
| `member_no` | Primary key. |
| `prev_balance` | Balance from prior statement. |
| `curr_balance` | Current balance. |
| `issue_dt` | Card issue date. |
| `expr_dt` | Card expiration date. |
| `region_no` | Foreign key to `Credit.region`. |
| `corp_no` | Foreign key to `Credit.corporation`; may be NULL. |

### `Credit.charge`
Individual transactions. Synonym: transaction, purchase.

| Column | Notes |
|--------|-------|
| `charge_no` | Primary key. |
| `member_no` | Foreign key to `Credit.member`. |
| `provider_no` | Foreign key to `Credit.provider`. |
| `category_no` | Foreign key to `Credit.category`. |
| `charge_dt` | Transaction timestamp. **Do not use for statement period assignment; use `statement_no` instead.** |
| `charge_amt` | Transaction amount in dollars. |
| `charge_code` | Enumerated: `'RF'` = refund; empty/NULL = normal charge. |
| `statement_no` | Foreign key to `Credit.statement`; use for period assignment. |

### `Credit.payment`
Member payments against statements. Synonym: payment, remittance.

| Column | Notes |
|--------|-------|
| `payment_no` | Primary key. |
| `member_no` | Foreign key to `Credit.member`. |
| `payment_dt` | Payment date. |
| `payment_amt` | Payment amount in dollars. |
| `statement_no` | Foreign key to `Credit.statement`. |

### `Credit.statement`
Monthly billing statements. Synonym: bill, invoice.

| Column | Notes |
|--------|-------|
| `statement_no` | Primary key. Use for period assignment, not `charge_dt`. |
| `member_no` | Foreign key to `Credit.member`. |
| `statement_dt` | Statement generation date. |
| `due_dt` | Payment due date. |
| `statement_amt` | Total statement balance. Must reconcile to `SUM(charges) - SUM(refunds)`. Negative values flag data quality issues. |

### `Credit.category`
Merchant category codes. Synonym: merchant category, spending category.

| Column | Notes |
|--------|-------|
| `category_no` | Primary key. |
| `category_desc` | Enumerated: `'Travel'`, `'Meals'`, `'Lodging'`, `'Groceries'`, `'Entertainment'`, `'Clothing'`, `'Communication'`, `'Electronics'`, `'Home Supplies'`, `'Misc'`. |

### `Credit.provider`
Merchants/service providers. Synonym: merchant, vendor.

| Column | Notes |
|--------|-------|
| `provider_no` | Primary key. |
| `provider_name` | Merchant name. |
| `region_no` | Foreign key to `Credit.region`. |
| `issue_dt` | Provider enrollment date. |
| `expr_dt` | Provider expiration date. |

### `Credit.corporation`
Corporate entities (employer/sponsor). Synonym: employer, sponsor.

| Column | Notes |
|--------|-------|
| `corp_no` | Primary key. |
| `corp_name` | Corporation name. |
| `region_no` | Foreign key to `Credit.region`. |
| `expr_dt` | Dominant value `'2004-10-12 10:41:26'` (likely sentinel); treat as potentially unreliable. |

### `Credit.region`
Geographic regions. Synonym: geography, territory.

| Column | Notes |
|--------|-------|
| `region_no` | Primary key. |
| `region_name` | Enumerated: `'North American'`, `'South American'`, `'Scandanavian'`, `'Western Europea'`, `'Eastern Europea'`, `'Africa'`, `'China'`, `'Japan'`, `'Mid East / Sout'`. |