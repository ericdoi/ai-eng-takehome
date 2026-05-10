# Financial Schema Reference Guide

## Schema Summary
This schema contains Czech banking data with accounts, clients, dispositions, cards, loans, standing orders, and transaction history across multiple districts.

---

## Join Paths

**Client to Account (via disposition):**
```sql
FROM financial.client c
JOIN financial.disp d ON c.client_id = d.client_id
JOIN financial.account a ON d.account_id = a.account_id
```

**Account to Loan:**
```sql
FROM financial.account a
JOIN financial.loan l ON a.account_id = l.account_id
```

**Account to Transactions:**
```sql
FROM financial.account a
JOIN financial.trans t ON a.account_id = t.account_id
```

**Account to Cards (via disposition):**
```sql
FROM financial.account a
JOIN financial.disp d ON a.account_id = d.account_id
JOIN financial.card c ON d.disp_id = c.disp_id
```

**Account to District:**
```sql
FROM financial.account a
JOIN financial.district dist ON a.district_id = dist.district_id
```

**Client to District:**
```sql
FROM financial.client c
JOIN financial.district dist ON c.district_id = dist.district_id
```

---

## Business Rules as SQL

**Rule: Performing loans (exclude watch/non-performing):**
```sql
WHERE financial.loan.status = 'A'
```

**Rule: Watch list loans (exclude from default rate, include in portfolio):**
```sql
WHERE financial.loan.status = 'B'
```

**Rule: Non-performing loans (never count in profitability):**
```sql
WHERE financial.loan.status NOT IN ('C', 'D')
```

**Rule: Exclude legacy transactions (before 1995-01-01):**
```sql
WHERE financial.trans.date >= '1995-01-01'
```

**Rule: Exclude interest and uncategorized transactions from revenue:**
```sql
WHERE financial.trans.k_symbol NOT IN ('UROK', ' ')
  AND financial.trans.k_symbol IS NOT NULL
```

**Rule: Micro-deposits (credit < 1000 units, exclude from average deposit):**
```sql
WHERE NOT (financial.trans.type = 'PRIJEM' AND financial.trans.amount < 1000)
```

**Rule: Prague district (always report separately):**
```sql
WHERE financial.district.district_id = 1
```

**Rule: Eastern Region (districts 70–77 aggregated):**
```sql
WHERE financial.district.district_id BETWEEN 70 AND 77
```

**Rule: Minimum district threshold (exclude districts with < 50 accounts):**
```sql
HAVING COUNT(DISTINCT financial.account.account_id) >= 50
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| performing loan | `financial.loan.status = 'A'` |
| watch list loan | `financial.loan.status = 'B'` |
| defaulted/non-performing loan | `financial.loan.status IN ('C', 'D')` |
| account owner | `financial.disp.type = 'OWNER'` |
| account disponent | `financial.disp.type = 'DISPONENT'` |
| credit/deposit | `financial.trans.type = 'PRIJEM'` |
| withdrawal | `financial.trans.type = 'VYBER'` |
| outgoing payment | `financial.trans.type = 'VYDAJ'` |
| card transfer | `financial.trans.operation = 'PREVOD NA UCET'` |
| card withdrawal | `financial.trans.operation = 'VYBER KARTOU'` |
| deposit | `financial.trans.operation = 'VKLAD'` |
| interest transaction | `financial.trans.k_symbol = 'UROK'` |
| fee-based income | `financial.trans.k_symbol IN ('POJISTNE', 'SIPO', 'SLUZBY')` |
| pension/salary | `financial.trans.k_symbol = 'DUCHOD'` |
| loan payment | `financial.trans.k_symbol = 'UVER'` |
| monthly fee account | `financial.account.frequency = 'POPLATEK MESICNE'` |
| weekly fee account | `financial.account.frequency = 'POPLATEK TYDNE'` |
| per-transaction fee account | `financial.account.frequency = 'POPLATEK PO OBRATU'` |
| Prague | `financial.district.A3 = 'Prague'` |
| central Bohemia | `financial.district.A3 = 'central Bohemia'` |

---

## Table Reference

### `financial.account`
Account master records with fee structure and opening date.

| Column | Notes |
|--------|-------|
| `account_id` | Primary key; links to `disp`, `loan`, `trans`, `order` |
| `district_id` | Foreign key to `financial.district` |
| `frequency` | Fee billing model: `POPLATEK MESICNE` (monthly), `POPLATEK TYDNE` (weekly), `POPLATEK PO OBRATU` (per-transaction) |
| `date` | Account opening date |

---

### `financial.client`
Individual clients with demographics.

| Column | Notes |
|--------|-------|
| `client_id` | Primary key; links to `disp` |
| `gender` | `F` or `M` |
| `birth_date` | Date of birth |
| `district_id` | Foreign key to `financial.district` |

---

### `financial.disp`
Disposition: relationship between client and account (ownership/authorization).

| Column | Notes |
|--------|-------|
| `disp_id` | Primary key; links to `card` |
| `client_id` | Foreign key to `financial.client` |
| `account_id` | Foreign key to `financial.account` |
| `type` | `OWNER` (account holder) or `DISPONENT` (authorized user) |

---

### `financial.card`
Payment cards issued to dispositions.

| Column | Notes |
|--------|-------|
| `card_id` | Primary key |
| `disp_id` | Foreign key to `financial.disp` |
| `type` | `classic`, `gold`, or `junior` |
| `issued` | Card issuance date |

---

### `financial.loan`
Loan contracts with repayment status.

| Column | Notes |
|--------|-------|
| `loan_id` | Primary key |
| `account_id` | Foreign key to `financial.account` |
| `date` | Loan origination date |
| `amount` | Principal amount |
| `duration` | Loan term in months |
| `payments` | Monthly payment amount |
| `status` | `A` (performing), `B` (watch list), `C` (non-performing), `D` (defaulted). **Business rule: exclude C/D from profitability metrics.** |

---

### `financial.trans`
Individual transactions on accounts.

| Column | Notes |
|--------|-------|
| `trans_id` | Primary key |
| `account_id` | Foreign key to `financial.account` |
| `date` | Transaction date. **Business rule: exclude dates before 1995-01-01.** |
| `type` | `PRIJEM` (credit), `VYBER` (withdrawal), `VYDAJ` (outgoing payment) |
| `operation` | Transaction method: `VKLAD` (deposit), `VYBER` (ATM withdrawal), `VYBER KARTOU` (card withdrawal), `PREVOD NA UCET` (transfer to account), `PREVOD Z UCTU` (transfer from account) |
| `amount` | Transaction amount |
| `balance` | Account balance after transaction |
| `k_symbol` | Transaction category: `UROK` (interest), `POJISTNE` (insurance), `SIPO` (standing order), `UVER` (loan payment), `SLUZBY` (fees), `DUCHOD` (pension), `SANKC. UROK` (penalty interest), or space/NULL. **Business rule: exclude UROK and NULL from revenue calculations; exclude micro-deposits (PRIJEM < 1000) from averages.** |
| `bank` | Counterparty bank code (2-letter): `AB`, `CD`, `EF`, `GH`, `IJ`, `KL`, `MN`, `OP`, `QR`, `ST`, `UV`, `WX`, `YZ` |
| `account` | Counterparty account number |

---

### `financial.order`
Standing orders (recurring transfers).

| Column | Notes |
|--------|-------|
| `order_id` | Primary key |
| `account_id` | Foreign key to `financial.account` |
| `bank_to` | Destination bank code (2-letter) |
| `account_to` | Destination account number |
| `amount` | Transfer amount |
| `k_symbol` | Purpose: `SIPO` (standing order), `UVER` (loan), `POJISTNE` (insurance), `LEASING` (lease), or space/NULL |

---

### `financial.district`
Geographic and demographic district metadata.

| Column | Notes |
|--------|-------|
| `district_id` | Primary key; 1 = Prague (report separately per business rule); 70–77 = Eastern Region (aggregate per business rule) |
| `A2` | District name |
| `A3` | Region: `Prague`, `central Bohemia`, `east Bohemia`, `north Bohemia`, `north Moravia`, `south Bohemia`, `south Moravia`, `west Bohemia` |
| `A4` | Population |
| `A5` | Number of municipalities with 1,000–10,000 inhabitants |
| `A6` | Number of municipalities with 10,000+ inhabitants |
| `A7` | Number of cities |
| `A8` | Ratio of urban to rural population |
| `A9` | Average salary |
| `A10` | Unemployment rate (%) |
| `A11` | Number of entrepreneurs |
| `A12` | Crimes per 1,000 inhabitants |
| `A13` | Crimes per 1,000 inhabitants (alternative measure) |
| `A14` | Number of committed crimes |
| `A15` | Number of solved crimes |
| `A16` | Population (alternative measure) |