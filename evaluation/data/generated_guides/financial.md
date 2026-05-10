# Financial Schema Reference Guide

## Schema Summary
The `financial` schema contains Czech banking data with client accounts, transactions, loans, cards, and district-level demographics, spanning approximately 1993–1998.

---

## Table Reference

### financial.account
**Meaning:** Bank accounts with fee structures and opening dates.
**Synonyms:** accounts, checking accounts

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `account_id` | BIGINT | Unique account identifier | account number |
| `district_id` | BIGINT | Foreign key to district | region, location |
| `frequency` | VARCHAR | Fee payment schedule | fee type, billing cycle |
| `date` | DATE | Account opening date | created, opened |

**Enumerated values for `frequency`:**
- `POPLATEK MESICNE` (monthly fee)
- `POPLATEK PO OBRATU` (fee per transaction)
- `POPLATEK TYDNE` (weekly fee)

---

### financial.card
**Meaning:** Credit/debit cards issued to account dispositions.
**Synonyms:** cards, plastic cards

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `card_id` | BIGINT | Unique card identifier | card number |
| `disp_id` | BIGINT | Foreign key to disposition | disposition |
| `type` | VARCHAR | Card product tier | card type, product |
| `issued` | DATE | Card issuance date | created, issued date |

**Enumerated values for `type`:**
- `classic`
- `gold`
- `junior`

---

### financial.client
**Meaning:** Individual clients/customers with demographics.
**Synonyms:** customers, persons, individuals

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `client_id` | BIGINT | Unique client identifier | customer ID, person ID |
| `gender` | VARCHAR | Biological sex | sex |
| `birth_date` | DATE | Date of birth | DOB, birthday |
| `district_id` | BIGINT | Foreign key to district | region, location |

**Enumerated values for `gender`:**
- `F` (female)
- `M` (male)

---

### financial.disp
**Meaning:** Account dispositions linking clients to accounts with role types.
**Synonyms:** dispositions, account holders, account relationships

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `disp_id` | BIGINT | Unique disposition identifier | disposition ID |
| `client_id` | BIGINT | Foreign key to client | customer ID |
| `account_id` | BIGINT | Foreign key to account | account number |
| `type` | VARCHAR | Role of client on account | role, relationship type |

**Enumerated values for `type`:**
- `OWNER` (account owner)
- `DISPONENT` (authorized user, co-signer)

---

### financial.district
**Meaning:** Geographic district metadata including population, economic, and crime statistics.
**Synonyms:** regions, locations, areas

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `district_id` | BIGINT | Unique district identifier | region ID |
| `A2` | VARCHAR | District name | name |
| `A3` | VARCHAR | Region classification | region, area |
| `A4` | BIGINT | Population | inhabitants, residents |
| `A5` | BIGINT | Number of municipalities | municipalities |
| `A6` | BIGINT | Number of cities | cities |
| `A7` | BIGINT | Number of villages | villages |
| `A8` | BIGINT | Number of urban districts | urban districts |
| `A9` | BIGINT | Number of rural districts | rural districts |
| `A10` | DOUBLE | Average salary | avg salary, mean income |
| `A11` | BIGINT | Unemployment rate (basis points) | unemployment |
| `A12` | DOUBLE | Entrepreneurship rate | business rate |
| `A13` | DOUBLE | Committed crimes rate | crime rate |
| `A14` | BIGINT | Number of committed crimes | crimes |
| `A15` | BIGINT | Number of solved crimes | solved crimes |
| `A16` | BIGINT | Number of criminal offenders | offenders |

**Enumerated values for `A3`:**
- `Prague`
- `central Bohemia`
- `east Bohemia`
- `north Bohemia`
- `north Moravia`
- `south Bohemia`
- `south Moravia`
- `west Bohemia`

---

### financial.loan
**Meaning:** Loan contracts with amounts, terms, and repayment status.
**Synonyms:** loans, credit facilities, advances

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `loan_id` | BIGINT | Unique loan identifier | loan number |
| `account_id` | BIGINT | Foreign key to account | account number |
| `date` | DATE | Loan origination date | created, issued |
| `amount` | BIGINT | Principal loan amount | principal, loan size |
| `duration` | BIGINT | Loan term in months | term, months |
| `payments` | DOUBLE | Monthly payment amount | monthly payment, installment |
| `status` | VARCHAR | Loan performance status | state, condition |

**Enumerated values for `status`:**
- `A` (performing)
- `B` (watch list)
- `C` (non-performing)
- `D` (non-performing)

---

### financial.order
**Meaning:** Standing orders for recurring transfers between accounts.
**Synonyms:** standing orders, transfer orders, payment orders

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `order_id` | BIGINT | Unique order identifier | order number |
| `account_id` | BIGINT | Foreign key to originating account | from account |
| `bank_to` | VARCHAR | Destination bank code | destination bank, bank code |
| `account_to` | BIGINT | Destination account number | to account |
| `amount` | DOUBLE | Transfer amount | transfer amount |
| `k_symbol` | VARCHAR | Transaction category/purpose | category, purpose, symbol |

**Enumerated values for `k_symbol`:**
- `` (empty/unspecified)
- `LEASING` (leasing payment)
- `POJISTNE` (insurance)
- `SIPO` (social insurance)
- `UVER` (loan/credit)

---

### financial.trans
**Meaning:** Individual account transactions with amounts, balances, and categorization.
**Synonyms:** transactions, movements, postings

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `trans_id` | BIGINT | Unique transaction identifier | transaction number |
| `account_id` | BIGINT | Foreign key to account | account number |
| `date` | DATE | Transaction date | posted date, value date |
| `type` | VARCHAR | Transaction direction | direction, flow |
| `operation` | VARCHAR | Transaction operation type | operation type, method |
| `amount` | BIGINT | Transaction amount (absolute value) | amt |
| `balance` | BIGINT | Account balance after transaction | ending balance |
| `k_symbol` | VARCHAR | Transaction category/purpose | category, purpose, symbol |
| `bank` | VARCHAR | Counterparty bank code | bank code, other bank |
| `account` | BIGINT | Counterparty account number | other account |

**Enumerated values for `type`:**
- `PRIJEM` (credit/inbound)
- `VYBER` (withdrawal)
- `VYDAJ` (expense/outbound)

**Enumerated values for `operation`:**
- `PREVOD NA UCET` (transfer to account)
- `PREVOD Z UCTU` (transfer from account)
- `VKLAD` (deposit)
- `VYBER` (withdrawal)
- `VYBER KARTOU` (card withdrawal)

**Enumerated values for `k_symbol`:**
- `` (empty/unspecified)
- `DUCHOD` (pension)
- `POJISTNE` (insurance)
- `SANKC. UROK` (penalty interest)
- `SIPO` (social insurance)
- `SLUZBY` (services/fees)
- `UROK` (interest)
- `UVER` (loan/credit)

---

## Join Paths

| From | To | Condition |
|------|----|-----------| 
| `account` | `district` | `account.district_id = district.district_id` |
| `account` | `disp` | `account.account_id = disp.account_id` |
| `account` | `loan` | `account.account_id = loan.account_id` |
| `account` | `order` | `account.account_id = order.account_id` |
| `account` | `trans` | `account.account_id = trans.account_id` |
| `client` | `disp` | `client.client_id = disp.client_id` |
| `client` | `district` | `client.district_id = district.district_id` |
| `disp` | `card` | `disp.disp_id = card.disp_id` |

---

## Business Rules as SQL

### Loan Classifications

**Rule: Performing loans (status A)**
```sql
WHERE loan.status = 'A'
```

**Rule: Watch list loans (status B) – include in portfolio size, exclude from defaults**
```sql
WHERE loan.status = 'B'
```

**Rule: Non-performing loans (status C or D) – exclude from profitability metrics**
```sql
WHERE loan.status NOT IN ('C', 'D')
-- OR for non-performing only:
WHERE loan.status IN ('C', 'D')
```

### Transaction Handling

**Rule: Exclude interest and uncategorized transactions from revenue**
```sql
WHERE trans.k_symbol NOT IN ('UROK', '') AND trans.k_symbol IS NOT NULL
```

**Rule: Exclude legacy transactions before 1995-01-01**
```sql
WHERE trans.date >= '1995-01-01'
```

**Rule: Micro-deposits (credit < 1000) – exclude from average deposit calculations**
```sql
WHERE NOT (trans.type = 'PRIJEM' AND trans.amount < 1000)
-- OR for micro-deposits only:
WHERE trans.type = 'PRIJEM' AND trans.amount < 1000
```

### District Aggregations

**Rule: Prague (district 1) – report separately**
```sql
WHERE district.district_id = 1
```

**Rule: Eastern Region (districts 70–77) – aggregate as single entity**
```sql
WHERE district.district_id BETWEEN 70 AND 77
```

**Rule: Exclude districts with fewer than 50 accounts**
```sql
HAVING COUNT(account.account_id) >= 50
-- OR for filtering:
WHERE district.district_id IN (
  SELECT district_id FROM financial.account 
  GROUP BY district_id 
  HAVING COUNT(*) >= 50
)
```

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| account owner | `disp.type = 'OWNER'` |
| authorized user / co-signer | `disp.type = 'DISPONENT'` |
| average salary | `district.A10` |
| card type | `card.type` |
| crime rate | `district.A13` |
| customer | `client` table |
| default rate | `COUNT(loan.loan_id) WHERE loan.status IN ('C', 'D')` |
| deposit | `trans.type = 'PRIJEM'` |
| district name | `district.A2` |
| district region | `district.A3` |
| Eastern Region | `district.district_id BETWEEN 70 AND 77` |
| entrepreneurship rate | `district.A12` |
| fee-based income | `trans.k_symbol NOT IN ('UROK', '')` |
| female client | `client.gender = 'F'` |
| gold card | `card.type = 'gold'` |
| interest transaction | `trans.k_symbol = 'UROK'` |
| loan amount | `loan.amount` |
| loan term | `loan.duration` |
| male client | `client.gender = 'M'` |
| micro-deposit | `trans.type = 'PRIJEM' AND trans.amount < 1000` |
| monthly fee | `account.frequency = 'POPLATEK MESICNE'` |
| non-performing loan | `loan.status IN ('C', 'D')` |
| performing loan | `loan.status = 'A'` |
| population | `district.A4` |
| Prague | `district.district_id = 1` |
| transaction balance | `trans.balance` |
| unemployment rate | `district.A11` |
| watch list loan | `loan.status = 'B'` |
| withdrawal | `trans.type = 'VYBER'` |