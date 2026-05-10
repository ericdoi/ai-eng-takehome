# CS Schema Reference Guide

## Schema Summary
This schema contains customer account and transaction data for a financial institution, including account hierarchies, transaction records, customer parties, products, and a churn prediction target.

---

## Join Paths

**Account to transactions:**
```sql
FROM cs.ACCOUNTS a
JOIN cs.ACCOUNT_TRANSACTIONS at ON a.ACC_KEY = at.ACC_KEY
```

**Account to account type:**
```sql
FROM cs.ACCOUNTS a
JOIN cs.ACCOUNT_TYPES act ON a.ACCTP_KEY = act.ACCTP_KEY
```

**Account to product:**
```sql
FROM cs.ACCOUNTS a
JOIN cs.PRODUCTS p ON a.PROD_KEY = p.PROD_KEY
```

**Account to party (customer):**
```sql
FROM cs.ACCOUNTS a
JOIN cs.PARTIES pt ON a.PT_UNIFIED_KEY = pt.PT_UNIFIED_KEY
```

**Account to organization:**
```sql
FROM cs.ACCOUNTS a
JOIN cs.ORGANIZATIONS o ON a.ORG_KEY = o.ORG_KEY
```

**Transaction to transaction type:**
```sql
FROM cs.ACCOUNT_TRANSACTIONS at
JOIN cs.ACCOUNT_TRANSACT_TYPES att ON at.ACTRNTP_KEY = att.ACTRNTP_KEY
```

**Account to churn target:**
```sql
FROM cs.ACCOUNTS a
JOIN cs.target_churn tc ON a.ACC_KEY = tc.ACC_KEY
```

---

## Table Reference

### `cs.ACCOUNTS`
Customer accounts. Primary key: `ACC_KEY`.

| Column | Semantics |
|--------|-----------|
| `ACCTP_KEY` | Foreign key to `cs.ACCOUNT_TYPES` |
| `PROD_KEY` | Foreign key to `cs.PRODUCTS` |
| `ORG_KEY` | Foreign key to `cs.ORGANIZATIONS` |
| `PT_UNIFIED_KEY` | Foreign key to `cs.PARTIES` (account holder) |
| `ACCH_OPEN_DATE` | Account opening date |
| `ACCH_CLOSE_DATE` | Account closing date; `3000-01-01` indicates open account |

---

### `cs.ACCOUNT_TRANSACTIONS`
Individual transactions on accounts. Primary key: `ACCTRN_KEY`.

| Column | Semantics |
|--------|-----------|
| `ACC_KEY` | Foreign key to `cs.ACCOUNTS` |
| `ACCTP_KEY` | Account type at transaction time |
| `ACTRNTP_KEY` | Foreign key to `cs.ACCOUNT_TRANSACT_TYPES` |
| `ACCTRN_ACCOUNTING_DATE` | Transaction date |
| `ACCTRN_AMOUNT_CZK` | Amount in CZK |
| `ACCTRN_CRDR_FLAG` | Credit (`C`) or Debit (`D`) |
| `ACCTRN_CASH_FLAG` | Cash transaction: `Y` or `N` |
| `ACCTRN_INTEREST_FLAG` | Interest transaction: `N` (only value observed) |
| `ACCTRN_TAX_FLAG` | Tax transaction: `N` (only value observed) |
| `ACCTRN_FEE_FLAG` | Fee transaction: `N` (only value observed) |
| `ACC_OTHER_ACCOUNT_KEY` | Counterparty account (if applicable); `-2` for none |
| `ACCTP_OTHER_ACCOUNT_KEY` | Counterparty account type; `-2` for none |

---

### `cs.ACCOUNT_TRANSACT_TYPES`
Transaction type lookup. Primary key: `ACTRNTP_KEY`.

| Column | Semantics |
|--------|-----------|
| `ACTRNTP_DESC` | Transaction type description. Values: `Typ transakce 3293`, `Typ transakce 3295`, `Typ transakce 3299`, `Typ transakce 3305`, `Typ transakce 3335`, `Typ transakce 3361`, `Typ transakce 3363` |

---

### `cs.ACCOUNT_TYPES`
Account type lookup. Primary key: `ACCTP_KEY`.

| Column | Semantics |
|--------|-----------|
| `ACCTP_DESC` | Account type description. Values: `INVALID` (`-2`), `N/A` (`-1`), `Typ účtu 101`, `Typ účtu 201`, `Typ účtu 202`, `Typ účtu 203`, `Typ účtu 204`, `Typ účtu 301`, `Typ účtu 501`, `Typ účtu 602`, `Typ účtu 1001`, `Typ účtu 1002`, `Typ účtu 1801` |

---

### `cs.ORGANIZATIONS`
Organizations (branches/locations). Primary key: `ORG_KEY`.

| Column | Semantics |
|--------|-----------|
| `ORGH_UNIFIED_ID` | Organization identifier (format: `HR0_` prefix) |
| `CITY` | City name |
| `ZIP` | Postal code |

---

### `cs.PARTIES`
Customers (parties). Primary key: `PT_UNIFIED_KEY`.

| Column | Semantics |
|--------|-----------|
| `ORG_KEY` | Foreign key to `cs.ORGANIZATIONS` |
| `PTH_BIRTH_DATE` | Birth date; `1000-01-01` indicates unknown/corporate |
| `PTH_CLIENT_FROM_DATE` | Customer relationship start date |
| `PTH_CLIENT_FROM_DATE_ALT` | Alternative customer start date |
| `PTTP_UNIFIED_ID` | Party type: `F` (individual) or `P` (corporate) |
| `PSGEN_UNIFIED_ID` | Gender: `M` (male), `Z` (female), `X` (unknown/corporate) |

---

### `cs.PRODUCTS`
Product catalog. Primary key: `PROD_KEY`.

| Column | Semantics |
|--------|-----------|
| `PROD_AGENDA_CODE` | Product code. Values: `1B`, `1S`, `2L`, `3S`, `3U`, `3Z`, `4V`, `XER` |
| `PROD_AGENDA_NAME` | Product name |

---

### `cs.target_churn`
Churn prediction target. Primary key: `(ACC_KEY, date_horizon)`.

| Column | Semantics |
|--------|-----------|
| `ACC_KEY` | Foreign key to `cs.ACCOUNTS` |
| `date_horizon` | Observation date for churn label |
| `target_churn` | Churn indicator: `0` (no churn) or `1` (churn) |