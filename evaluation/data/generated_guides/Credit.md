# Credit Schema Reference Guide

## Schema Summary
The Credit schema tracks credit card member transactions, charges, payments, and statements across providers and regions, with business rules for charge classification, member segmentation, and fraud detection.

---

## Join Paths

**Member → Charges → Providers:**
```sql
FROM Credit.member m
JOIN Credit.charge c ON m.member_no = c.member_no
JOIN Credit.provider p ON c.provider_no = p.provider_no
```

**Member → Statements → Charges:**
```sql
FROM Credit.member m
JOIN Credit.statement s ON m.member_no = s.member_no
JOIN Credit.charge c ON s.statement_no = c.statement_no
```

**Charge → Category:**
```sql
FROM Credit.charge c
JOIN Credit.category cat ON c.category_no = cat.category_no
```

**Member → Corporation → Region:**
```sql
FROM Credit.member m
JOIN Credit.corporation corp ON m.corp_no = corp.corp_no
JOIN Credit.region r ON corp.region_no = r.region_no
```

**Member → Payments → Statements:**
```sql
FROM Credit.member m
JOIN Credit.payment pay ON m.member_no = pay.member_no
JOIN Credit.statement s ON pay.statement_no = s.statement_no
```

---

## Business Rules as SQL

**Refund exclusion (charge_code = 'RF'):**
```sql
WHERE c.charge_code != 'RF'
```

**Micro-transaction exclusion (< $5):**
```sql
WHERE c.charge_amt >= 5.00
```

**Test transaction exclusion (exactly $0.01):**
```sql
WHERE c.charge_amt != 0.01
```

**Inactive member filter (< 3 charges in 12 months):**
```sql
HAVING COUNT(c.charge_no) >= 3
```

**Premium member segment (lifetime charges > $10,000):**
```sql
WHERE SUM(c.charge_amt) > 10000
```

**Active transacting members (exclude zero-charge members in current period):**
```sql
WHERE c.charge_no IS NOT NULL
```

**Essential spending categories (1–10):**
```sql
WHERE c.category_no BETWEEN 1 AND 10
```

**Discretionary spending categories (11–20):**
```sql
WHERE c.category_no BETWEEN 11 AND 20
```

**Provider minimum threshold (≥ 100 charges):**
```sql
HAVING COUNT(c.charge_no) >= 100
```

**Fraud flag: high charge + refund within 24 hours:**
```sql
WHERE c.charge_amt > 5000
  AND EXISTS (
    SELECT 1 FROM Credit.charge c2
    WHERE c2.provider_no = c.provider_no
      AND c2.charge_code = 'RF'
      AND c2.charge_dt BETWEEN c.charge_dt AND c.charge_dt + INTERVAL 24 HOUR
  )
```

**Fraud flag: duplicate processing (same provider within 60 seconds):**
```sql
WHERE EXISTS (
  SELECT 1 FROM Credit.charge c2
  WHERE c2.provider_no = c.provider_no
    AND c2.member_no = c.member_no
    AND c2.charge_no != c.charge_no
    AND ABS(EXTRACT(EPOCH FROM (c2.charge_dt - c.charge_dt))) <= 60
)
```

**Statement reconciliation (charges minus refunds):**
```sql
SELECT s.statement_no,
  SUM(CASE WHEN c.charge_code = 'RF' THEN -c.charge_amt ELSE c.charge_amt END) AS reconciled_amt
FROM Credit.statement s
LEFT JOIN Credit.charge c ON s.statement_no = c.statement_no
GROUP BY s.statement_no
```

**Month-end statement assignment (use statement_no, not charge_dt):**
```sql
FROM Credit.charge c
JOIN Credit.statement s ON c.statement_no = s.statement_no
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| transaction | `Credit.charge` |
| refund | `WHERE charge_code = 'RF'` |
| cardholder | `Credit.member` |
| merchant | `Credit.provider` |
| spending category | `Credit.category` |
| billing period | `Credit.statement` |
| transaction amount | `charge.charge_amt` |
| transaction date | `charge.charge_dt` |
| payment received | `Credit.payment` |
| inactive member | `HAVING COUNT(charge_no) < 3` |
| premium member | `WHERE SUM(charge_amt) > 10000` |
| essential spending | `WHERE category_no BETWEEN 1 AND 10` |
| discretionary spending | `WHERE category_no BETWEEN 11 AND 20` |
| long tail provider | `HAVING COUNT(charge_no) < 100` |

---

## Table Reference

### `Credit.member`
**Meaning:** Credit card members (cardholders).  
**Synonyms:** cardholder, account holder

| Column | Notes |
|--------|-------|
| `member_no` | Primary key |
| `issue_dt`, `expr_dt` | Card issuance and expiration dates |
| `region_no` | Foreign key to `Credit.region` |
| `corp_no` | Foreign key to `Credit.corporation` (nullable) |
| `prev_balance`, `curr_balance` | Previous and current statement balances |

---

### `Credit.charge`
**Meaning:** Individual credit card transactions.  
**Synonyms:** transaction, purchase, charge

| Column | Notes |
|--------|-------|
| `charge_no` | Primary key |
| `member_no` | Foreign key to `Credit.member` |
| `provider_no` | Foreign key to `Credit.provider` |
| `category_no` | Foreign key to `Credit.category` |
| `charge_dt` | Transaction timestamp; use `statement_no` for period assignment, not this field |
| `charge_amt` | Transaction amount; exclude if < $5.00 or = $0.01 |
| `charge_code` | Enumerated: `'RF'` = refund (subtract from gross volume); other values are normal charges |
| `statement_no` | Foreign key to `Credit.statement`; authoritative for period assignment |

---

### `Credit.category`
**Meaning:** Spending categories for charge classification.  
**Synonyms:** merchant category, spending type

| Column | Notes |
|--------|-------|
| `category_no` | Primary key |
| `category_desc` | Enumerated values: Clothing, Communication, Electronics, Entertainment, Groceries, Home Supplies, Lodging, Meals, Misc, Travel |

---

### `Credit.statement`
**Meaning:** Monthly billing statements for members.  
**Synonyms:** billing period, invoice, bill

| Column | Notes |
|--------|-------|
| `statement_no` | Primary key; use for period assignment instead of charge dates |
| `member_no` | Foreign key to `Credit.member` |
| `statement_dt` | Statement generation date |
| `due_dt` | Payment due date |
| `statement_amt` | Total statement balance; should reconcile to SUM(charges) - SUM(refunds) |

---

### `Credit.payment`
**Meaning:** Member payments received against statements.  
**Synonyms:** payment received, payment transaction

| Column | Notes |
|--------|-------|
| `payment_no` | Primary key |
| `member_no` | Foreign key to `Credit.member` |
| `payment_dt` | Payment date |
| `payment_amt` | Amount paid |
| `statement_no` | Foreign key to `Credit.statement` |

---

### `Credit.provider`
**Meaning:** Merchants/vendors accepting the credit card.  
**Synonyms:** merchant, vendor, acquirer

| Column | Notes |
|--------|-------|
| `provider_no` | Primary key |
| `region_no` | Foreign key to `Credit.region` |
| `issue_dt`, `expr_dt` | Provider agreement dates |

---

### `Credit.corporation`
**Meaning:** Corporate entities sponsoring member accounts.  
**Synonyms:** employer, sponsor, corporate account

| Column | Notes |
|--------|-------|
| `corp_no` | Primary key |
| `region_no` | Foreign key to `Credit.region` |
| `expr_dt` | Corporate agreement expiration date |

---

### `Credit.region`
**Meaning:** Geographic regions for members, providers, and corporations.  
**Synonyms:** geography, territory, location

| Column | Notes |
|--------|-------|
| `region_no` | Primary key |
| `region_name` | Enumerated values: Africa, China, Eastern Europea, Japan, Mid East / Sout, North American, Scandanavian, South American, Western Europea |