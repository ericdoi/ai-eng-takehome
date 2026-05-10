# Financial Schema Reference Guide

## 1. Schema Summary

The `financial` schema contains a Czech bank's operational data covering client accounts, loans, transactions, standing orders, payment cards, and geographic district attributes.

---

## 2. Join Paths

**account → district** [OPTIONAL — display only]
```sql
FROM financial.account a
JOIN financial.district d ON a.district_id = d.district_id
```

**account → client** (via disp) [REQUIRED]
```sql
FROM financial.account a
JOIN financial.disp dp ON a.account_id = dp.account_id
JOIN financial.client c ON dp.client_id = c.client_id
```

**account → loan** [REQUIRED]
```sql
FROM financial.account a
JOIN financial.loan l ON a.account_id = l.account_id
```

**account → trans** [REQUIRED]
```sql
FROM financial.account a
JOIN financial.trans t ON a.account_id = t.account_id
```

**account → order** [REQUIRED]
```sql
FROM financial.account a
JOIN financial.order o ON a.account_id = o.account_id
```

**client → card** (via disp) [REQUIRED]
```sql
FROM financial.client c
JOIN financial.disp dp ON c.client_id = dp.client_id
JOIN financial.card cd ON dp.disp_id = cd.disp_id
```

**account owner only** (filter disp to single owner per account) [REQUIRED when isolating account owner]
```sql
FROM financial.account a
JOIN financial.disp dp ON a.account_id = dp.account_id AND dp.type = 'OWNER'
JOIN financial.client c ON dp.client_id = c.client_id
```

---

## 3. Business Rules as SQL

### Loan Status

- **IDENTIFY performing loans:** `WHERE status = 'A'` — rows matching this condition ARE performing loans
- **IDENTIFY watch-list loans:** `WHERE status = 'B'` — rows matching this condition ARE watch-list loans
- **IDENTIFY non-performing loans:** `WHERE status IN ('C', 'D')` — rows matching this condition ARE non-performing loans
- **EXCLUDE non-performing from profitability:** `WHERE status NOT IN ('C', 'D')`
- **EXCLUDE watch-list from default rate denominator:** `WHERE status != 'B'`

**Combined status label mapping:**
```sql
CASE
    WHEN status = 'A' THEN 'Performing'
    WHEN status = 'B' THEN 'Watch List'
    WHEN status IN ('C', 'D') THEN 'Non-Performing'
END AS loan_status_label
```

**Default rate:**
```sql
-- default_rate = non-performing count / eligible portfolio count (excludes Watch List)
COUNT(CASE WHEN status IN ('C', 'D') THEN 1 END)
  / NULLIF(COUNT(CASE WHEN status != 'B' THEN 1 END), 0)
  AS default_rate
FROM financial.loan
```

---

### Transaction Handling

- **EXCLUDE interest/unclassified from revenue:** `WHERE k_symbol NOT IN ('UROK') AND k_symbol IS NOT NULL`
- **EXCLUDE legacy transactions from balance calculations:** `WHERE date >= '1995-01-01'`
- **IDENTIFY micro-deposits:** `WHERE type = 'PRIJEM' AND amount < 1000` — rows matching this condition ARE micro-deposits
- **EXCLUDE micro-deposits from average deposit calculations:** `WHERE type = 'PRIJEM' AND amount >= 1000`

---

### District Aggregations

- **IDENTIFY Prague (always separate):** `WHERE district_id = 1`
- **IDENTIFY Eastern Region:** `WHERE district_id BETWEEN 70 AND 77`

```sql
-- Eastern Region aggregation
CASE
    WHEN district_id = 1 THEN 'Prague'
    WHEN district_id BETWEEN 70 AND 77 THEN 'Eastern Region'
    ELSE d.A2
END AS district_label
```

- **EXCLUDE small districts from district-level metrics:**
```sql
-- Use "Other" for districts with fewer than 50 accounts
SELECT
    CASE WHEN COUNT(a.account_id) < 50 THEN 'Other' ELSE CAST(a.district_id AS VARCHAR) END AS district_group
FROM financial.account a
GROUP BY a.district_id
```

---

## 4. Synonym Glossary

| Common Term | Schema Mapping |
|---|---|
| "account holder" / "account owner" | `financial.disp.type = 'OWNER'` |
| "authorized user" / "secondary user" | `financial.disp.type = 'DISPONENT'` |
| "region" / "area" | `financial.district.A3` |
| "district name" | `financial.district.A2` |
| "card holder" | `financial.client` joined via `financial.disp` → `financial.card` |
| "credit card type" | `financial.card.type` (`classic`, `gold`, `junior`) |
| "deposit" / "credit transaction" | `financial.trans WHERE type = 'PRIJEM'` |
| "withdrawal" | `financial.trans WHERE type IN ('VYBER', 'VYDAJ')` |
| "standing order" / "payment order" | `financial.order` |
| "loan default" | `financial.loan WHERE status IN ('C', 'D')` |
| "performing loan" | `financial.loan WHERE status = 'A'` |
| "interest income" | `financial.trans WHERE k_symbol = 'UROK'` |
| "insurance payment" | `financial.trans WHERE k_symbol = 'POJISTNE'` or `financial.order WHERE k_symbol = 'POJISTNE'` |
| "statement frequency" / "billing cycle" | `financial.account.frequency` |
| "monthly statement" | `financial.account WHERE frequency = 'POPLATEK MESICNE'` |
| "weekly statement" | `financial.account WHERE frequency = 'POPLATEK TYDNE'` |
| "transaction-triggered statement" | `financial.account WHERE frequency = 'POPLATEK PO OBRATU'` |
| "age" / "birth year" | `financial.client.birth_date` (sentinel value `'1970-12-13'` = possible data artifact) |
| "Prague" | `financial.district WHERE district_id = 1` |
| "Eastern Region" | `financial.district WHERE district_id BETWEEN 70 AND 77` |
| "micro-deposit" | `financial.trans WHERE type = 'PRIJEM' AND amount < 1000` |

---

## 5. Table Reference

### `financial.account`
Standing bank accounts. One account may have multiple clients linked via `financial.disp`.

| Column | Notes |
|---|---|
| `frequency` | Statement/fee billing cycle. Values: `'POPLATEK MESICNE'` (monthly), `'POPLATEK TYDNE'` (weekly), `'POPLATEK PO OBRATU'` (per-transaction) |
| `date` | Account opening date |

---

### `financial.card`
Payment cards issued to disposers (not directly to accounts).

| Column | Notes |
|---|---|
| `disp_id` | FK to `financial.disp` — card belongs to a specific client–account relationship, not the account alone |
| `type` | Card tier: `'classic'`, `'gold'`, `'junior'` |
| `issued` | Card issue date |

---

### `financial.client`
Individual bank customers.

| Column | Notes |
|---|---|
| `gender` | `'F'` = female, `'M'` = male |
| `birth_date` | Sentinel value `'1970-12-13'` may indicate missing/epoch-zero data — treat with caution |
| `district_id` | Client's home district; may differ from their account's `district_id` |

---

### `financial.disp`
Junction table linking clients to accounts; also the anchor for card issuance.

| Column | Notes |
|---|---|
| `type` | `'OWNER'` = primary account holder (one per account); `'DISPONENT'` = authorized secondary user (zero or more per account) |

---

### `financial.district`
Geographic and socioeconomic attributes of Czech districts. Column names are opaque codes.

| Column | Notes |
|---|---|
| `A2` | District name (human-readable) |
| `A3` | Region name. Values: `'Prague'`, `'central Bohemia'`, `'east Bohemia'`, `'north Bohemia'`, `'north Moravia'`, `'south Bohemia'`, `'south Moravia'`, `'west Bohemia'` |
| `A4` | Population |
| `A11` | Average salary |
| `A12` / `A13` | Unemployment rates (two measures) |
| `A14` | Number of entrepreneurs per 1000 inhabitants |
| `A15` / `A16` | Crime counts (two years) |
| `district_id = 1` | Always Prague — must be reported separately per business rules |
| `district_id 70–77` | Operationally merged as "Eastern Region" |

---

### `financial.loan`
One loan per account (accounts may have at most one loan).

| Column | Notes |
|---|---|
| `status` | `'A'` = performing (contract finished, no issues); `'B'` = watch list (contract finished, loan not paid); `'C'` = non-performing (contract running, OK so far); `'D'` = non-performing (contract running, client in debt). Exclude `'C'`/`'D'` from profitability; exclude `'B'` from default rate denominator. |
| `amount` | Total loan amount |
| `duration` | Loan term in months |
| `payments` | Monthly payment amount |

---

### `financial.order`
Standing payment orders (recurring outgoing transfers).

| Column | Notes |
|---|---|
| `bank_to` | Destination bank code (2-letter) |
| `account_to` | Destination account number |
| `k_symbol` | Payment category: `'POJISTNE'` (insurance), `'SIPO'` (household payments), `'LEASING'` (leasing), `'UVER'` (loan repayment), `''` (unspecified) |

---

### `financial.trans`
Individual account transactions. Largest table — filter early.

| Column | Notes |
|---|---|
| `type` | Direction: `'PRIJEM'` = credit/inflow, `'VYDAJ'` = debit/outflow, `'VYBER'` = cash withdrawal |
| `operation` | Method: `'VKLAD'` (cash deposit), `'PREVOD Z UCTU'` (incoming transfer), `'PREVOD NA UCET'` (outgoing transfer), `'VYBER'` (cash withdrawal), `'VYBER KARTOU'` (card withdrawal) |
| `k_symbol` | Category: `'UROK'` (interest — exclude from revenue), `'POJISTNE'` (insurance), `'SIPO'` (household), `'SLUZBY'` (services), `'SANKC. UROK'` (penalty interest), `'DUCHOD'` (pension), `'UVER'` (loan payment), `' '` or NULL (unclassified — exclude from revenue) |
| `balance` | Running account balance after transaction |
| `bank` | Counterparty bank code |
| `account` | Counterparty account number |
| `date` | Exclude dates before `'1995-01-01'` (legacy migration data — unreliable) |