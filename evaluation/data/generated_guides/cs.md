# SQL Reference Guide: cs Schema

## 1. Schema Summary

The `cs` schema contains banking customer account data including account hierarchies, transaction records, account types, products, organizations, and parties (customers), with a churn prediction target variable.

---

## 2. Table Reference

### cs.ACCOUNTS
**Meaning:** Bank accounts with their type, product, organization, and party associations; includes open and close dates.
**Synonyms:** Account master, account records

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ACC_KEY` | BIGINT | Unique account identifier | Account ID, account number |
| `ACCTP_KEY` | BIGINT | Foreign key to account type | Account type key |
| `PROD_KEY` | BIGINT | Foreign key to product | Product key |
| `ORG_KEY` | BIGINT | Foreign key to organization | Organization key |
| `PT_UNIFIED_KEY` | BIGINT | Foreign key to party (customer) | Party key, customer key |
| `ACCH_OPEN_DATE` | DATE | Account opening date | Open date, creation date |
| `ACCH_CLOSE_DATE` | DATE | Account closing date | Close date, termination date |

**Notable values:** `ACC_KEY = -2` represents invalid/placeholder records; `ACCH_CLOSE_DATE = 3000-01-01` indicates open accounts.

---

### cs.ACCOUNT_TRANSACTIONS
**Meaning:** Individual transactions posted to accounts, including amounts, direction (credit/debit), and transaction type classification.
**Synonyms:** Transactions, posting records, account activity

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ACCTRN_KEY` | BIGINT | Unique transaction identifier | Transaction ID |
| `ACC_KEY` | BIGINT | Foreign key to account | Account key |
| `ACCTP_KEY` | BIGINT | Foreign key to account type | Account type key |
| `ACTRNTP_KEY` | BIGINT | Foreign key to transaction type | Transaction type key |
| `ACCTRN_ACCOUNTING_DATE` | DATE | Transaction posting date | Posting date, transaction date |
| `ACCTRN_AMOUNT_CZK` | BIGINT | Transaction amount in CZK | Amount, local amount |
| `ACCTRN_AMOUNT_FX` | BIGINT | Transaction amount in foreign currency | FX amount |
| `CURR_ISO_CODE` | VARCHAR | Currency code | Currency |
| `ACCTRN_CRDR_FLAG` | VARCHAR | Credit (C) or Debit (D) flag | Direction, CR/DR |
| `ACCTRN_CASH_FLAG` | VARCHAR | Cash transaction indicator (Y/N) | Cash flag |
| `ACCTRN_INTEREST_FLAG` | VARCHAR | Interest transaction indicator (N) | Interest flag |
| `ACCTRN_TAX_FLAG` | VARCHAR | Tax transaction indicator (N) | Tax flag |
| `ACCTRN_FEE_FLAG` | VARCHAR | Fee transaction indicator (N) | Fee flag |
| `ACC_OTHER_ACCOUNT_KEY` | BIGINT | Related account in transfer | Other account key |
| `ACCTP_OTHER_ACCOUNT_KEY` | BIGINT | Related account type in transfer | Other account type key |

**Notable values:** `ACCTRN_CRDR_FLAG` values: `C` (credit), `D` (debit); `ACCTRN_CASH_FLAG` values: `Y`, `N`; all flag columns show `N` in samples except cash flag.

---

### cs.ACCOUNT_TRANSACT_TYPES
**Meaning:** Lookup table defining transaction type classifications.
**Synonyms:** Transaction types, transaction categories

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ACTRNTP_KEY` | BIGINT | Transaction type identifier | Transaction type ID |
| `ACTRNTP_DESC` | VARCHAR | Transaction type description | Type description |

**Notable values:** `ACTRNTP_DESC` values: `Typ transakce 3293`, `Typ transakce 3295`, `Typ transakce 3299`, `Typ transakce 3305`, `Typ transakce 3335`, `Typ transakce 3361`, `Typ transakce 3363`

---

### cs.ACCOUNT_TYPES
**Meaning:** Lookup table defining account type classifications.
**Synonyms:** Account type master, account categories

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ACCTP_KEY` | BIGINT | Account type identifier | Account type ID |
| `ACCTP_DESC` | VARCHAR | Account type description | Type description |

**Notable values:** `ACCTP_DESC` values: `INVALID`, `N/A`, `Typ účtu 101`, `Typ účtu 201`, `Typ účtu 202`, `Typ účtu 203`, `Typ účtu 204`, `Typ účtu 301`, `Typ účtu 501`, `Typ účtu 602`, `Typ účtu 1001`, `Typ účtu 1002`, `Typ účtu 1801`

---

### cs.ORGANIZATIONS
**Meaning:** Organizations (branches or entities) associated with accounts and parties.
**Synonyms:** Branches, organizational units, entities

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ORG_KEY` | BIGINT | Unique organization identifier | Organization ID |
| `ORGH_UNIFIED_ID` | VARCHAR | Organization unified identifier code | Organization code, ID code |
| `CITY` | VARCHAR | City where organization is located | Location, city name |
| `ZIP` | BIGINT | Postal code | Postal code, ZIP code |

**Notable values:** `ORG_KEY = -2` represents invalid/placeholder records.

---

### cs.PARTIES
**Meaning:** Customers (parties) who own accounts; includes personal/business classification and demographic data.
**Synonyms:** Customers, clients, individuals, entities

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `PT_UNIFIED_KEY` | BIGINT | Unique party identifier | Party ID, customer ID |
| `ORG_KEY` | BIGINT | Foreign key to organization | Organization key |
| `PTH_BIRTH_DATE` | VARCHAR | Birth date (for individuals) | Birth date, DOB |
| `PTH_CLIENT_FROM_DATE` | VARCHAR | Date customer relationship began | Client start date, relationship date |
| `PTH_CLIENT_FROM_DATE_ALT` | VARCHAR | Alternative client start date | Alternative start date |
| `PTTP_UNIFIED_ID` | VARCHAR | Party type: F (individual) or P (business) | Party type, customer type |
| `PSGEN_UNIFIED_ID` | VARCHAR | Gender: M (male), Z (female), X (other) | Gender |

**Notable values:** `PTTP_UNIFIED_ID` values: `F` (individual), `P` (business); `PSGEN_UNIFIED_ID` values: `M` (male), `Z` (female), `X` (other); `PTH_BIRTH_DATE = 1000-01-01` indicates missing/invalid data.

---

### cs.PRODUCTS
**Meaning:** Product catalog defining banking products offered.
**Synonyms:** Product master, product catalog

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `PROD_KEY` | BIGINT | Unique product identifier | Product ID |
| `PROD_AGENDA_CODE` | VARCHAR | Product agenda/category code | Product code, category code |
| `PROD_AGENDA_NAME` | VARCHAR | Product name | Product name, description |

**Notable values:** `PROD_AGENDA_CODE` values: `1B`, `1S`, `2L`, `3S`, `3U`, `3Z`, `4V`, `XER`; `PROD_KEY = -2` represents invalid/placeholder records.

---

### cs.target_churn
**Meaning:** Churn prediction target variable indicating whether an account churned by a given date horizon.
**Synonyms:** Churn target, churn label, churn indicator

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ACC_KEY` | BIGINT | Foreign key to account | Account key, account ID |
| `date_horizon` | DATE | Observation date for churn prediction | Horizon date, prediction date |
| `target_churn` | BIGINT | Churn indicator (0 = no churn, 1 = churn) | Churn flag, churn label |

**Notable values:** `target_churn` values: `0` (no churn), `1` (churn)

---

## 3. Join Paths

| From | To | Join Condition |
|------|----|----|
| `cs.ACCOUNTS` | `cs.ACCOUNT_TYPES` | `ACCOUNTS.ACCTP_KEY = ACCOUNT_TYPES.ACCTP_KEY` |
| `cs.ACCOUNTS` | `cs.PRODUCTS` | `ACCOUNTS.PROD_KEY = PRODUCTS.PROD_KEY` |
| `cs.ACCOUNTS` | `cs.ORGANIZATIONS` | `ACCOUNTS.ORG_KEY = ORGANIZATIONS.ORG_KEY` |
| `cs.ACCOUNTS` | `cs.PARTIES` | `ACCOUNTS.PT_UNIFIED_KEY = PARTIES.PT_UNIFIED_KEY` |
| `cs.ACCOUNTS` | `cs.target_churn` | `ACCOUNTS.ACC_KEY = target_churn.ACC_KEY` |
| `cs.ACCOUNT_TRANSACTIONS` | `cs.ACCOUNTS` | `ACCOUNT_TRANSACTIONS.ACC_KEY = ACCOUNTS.ACC_KEY` |
| `cs.ACCOUNT_TRANSACTIONS` | `cs.ACCOUNT_TYPES` | `ACCOUNT_TRANSACTIONS.ACCTP_KEY = ACCOUNT_TYPES.ACCTP_KEY` |
| `cs.ACCOUNT_TRANSACTIONS` | `cs.ACCOUNT_TRANSACT_TYPES` | `ACCOUNT_TRANSACTIONS.ACTRNTP_KEY = ACCOUNT_TRANSACT_TYPES.ACTRNTP_KEY` |
| `cs.PARTIES` | `cs.ORGANIZATIONS` | `PARTIES.ORG_KEY = ORGANIZATIONS.ORG_KEY` |

---

## 4. Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| Account is open | `WHERE ACCH_CLOSE_DATE = '3000-01-01'` |
| Account is closed | `WHERE ACCH_CLOSE_DATE < '3000-01-01'` |
| Valid account (exclude placeholder) | `WHERE ACC_KEY > 0` |
| Valid organization (exclude placeholder) | `WHERE ORG_KEY > 0` |
| Valid party (exclude placeholder) | `WHERE PT_UNIFIED_KEY > 0` |
| Individual customer | `WHERE PTTP_UNIFIED_ID = 'F'` |
| Business customer | `WHERE PTTP_UNIFIED_ID = 'P'` |
| Cash transaction | `WHERE ACCTRN_CASH_FLAG = 'Y'` |
| Non-cash transaction | `WHERE ACCTRN_CASH_FLAG = 'N'` |
| Debit transaction | `WHERE ACCTRN_CRDR_FLAG = 'D'` |
| Credit transaction | `WHERE ACCTRN_CRDR_FLAG = 'C'` |
| Churned account | `WHERE target_churn.target_churn = 1` |
| Active account (not churned) | `WHERE target_churn.target_churn = 0` |

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| Account | `cs.ACCOUNTS.ACC_KEY` |
| Account type | `cs.ACCOUNT_TYPES.ACCTP_DESC` |
| Product | `cs.PRODUCTS.PROD_AGENDA_NAME` |
| Product code | `cs.PRODUCTS.PROD_AGENDA_CODE` |
| Organization / Branch | `cs.ORGANIZATIONS.ORGH_UNIFIED_ID` |
| City | `cs.ORGANIZATIONS.CITY` |
| Customer / Party | `cs.PARTIES.PT_UNIFIED_KEY` |
| Customer type | `cs.PARTIES.PTTP_UNIFIED_ID` |
| Individual | `WHERE PTTP_UNIFIED_ID = 'F'` |
| Business | `WHERE PTTP_UNIFIED_ID = 'P'` |
| Gender | `cs.PARTIES.PSGEN_UNIFIED_ID` |
| Transaction | `cs.ACCOUNT_TRANSACTIONS.ACCTRN_KEY` |
| Transaction amount | `cs.ACCOUNT_TRANSACTIONS.ACCTRN_AMOUNT_CZK` |
| Transaction date | `cs.ACCOUNT_TRANSACTIONS.ACCTRN_ACCOUNTING_DATE` |
| Transaction type | `cs.ACCOUNT_TRANSACT_TYPES.ACTRNTP_DESC` |
| Debit / Withdrawal | `WHERE ACCTRN_CRDR_FLAG = 'D'` |
| Credit / Deposit | `WHERE ACCTRN_CRDR_FLAG = 'C'` |
| Cash transaction | `WHERE ACCTRN_CASH_FLAG = 'Y'` |
| Account open date | `cs.ACCOUNTS.ACCH_OPEN_DATE` |
| Account close date | `cs.ACCOUNTS.ACCH_CLOSE_DATE` |
| Open account | `WHERE ACCH_CLOSE_DATE = '3000-01-01'` |
| Closed account | `WHERE ACCH_CLOSE_DATE < '3000-01-01'` |
| Churn | `cs.target_churn.target_churn = 1` |
| No churn | `cs.target_churn.target_churn = 0` |
| Observation date | `cs.target_churn.date_horizon` |
| Client start date | `cs.PARTIES.PTH_CLIENT_FROM_DATE` |
| Birth date | `cs.PARTIES.PTH_BIRTH_DATE` |