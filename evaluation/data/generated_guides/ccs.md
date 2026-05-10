# CCS Schema Reference Guide

## 1. Schema Summary

The `ccs` schema contains fuel transaction data from gas stations across Central Europe, including customer profiles, station information, products sold, and transaction records with consumption tracking by month.

---

## 2. Table Reference

### Table: `ccs.customers`
**Meaning:** Customer master data; also called "accounts" or "client profiles"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `CustomerID` | BIGINT | Unique customer identifier | Customer number, account ID |
| `Segment` | VARCHAR | Customer classification tier | Customer type, classification |
| `Currency` | VARCHAR | Billing currency | Payment currency |

**Enumerated Values:**
- `Segment`: `KAM`, `LAM`, `SME`
- `Currency`: `CZK`, `EUR`

---

### Table: `ccs.gasstations`
**Meaning:** Gas station location and chain data; also called "stations" or "outlets"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `GasStationID` | BIGINT | Unique gas station identifier | Station ID, outlet ID |
| `ChainID` | BIGINT | Parent fuel chain/brand identifier | Brand ID, operator ID |
| `Country` | VARCHAR | Country of operation | Location country |
| `Segment` | VARCHAR | Station market positioning | Station type, category |

**Enumerated Values:**
- `Country`: `CZE`, `SVK`
- `Segment`: `Discount`, `Noname`, `Other`, `Premium`, `Value for money`

---

### Table: `ccs.products`
**Meaning:** Fuel product catalog; also called "fuel types" or "SKUs"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ProductID` | BIGINT | Unique product identifier | Product code, fuel type ID |
| `Description` | VARCHAR | Product name or type | Product name, fuel type |

**Sample Values:** `Rucní zadání`, `Nafta`, `Special`, `Super`, `Natural`

---

### Table: `ccs.transactions`
**Meaning:** Individual fuel purchase transactions; also called "sales" or "pump records"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Date` | DATE | Transaction date | Purchase date, sale date |
| `Time` | TIME | Transaction time | Purchase time, sale time |
| `CustomerID` | BIGINT | Purchasing customer | Buyer ID, account ID |
| `CardID` | BIGINT | Payment card used | Card number, payment method ID |
| `GasStationID` | BIGINT | Station where purchased | Outlet ID, location ID |
| `ProductID` | BIGINT | Fuel product purchased | Fuel type ID |
| `Amount` | BIGINT | Quantity purchased (liters) | Volume, quantity, liters |
| `Price` | DOUBLE | Total transaction price | Cost, total amount |

---

### Table: `ccs.transactions_1k`
**Meaning:** Sample transaction dataset (1,000 records); also called "transaction sample" or "test transactions"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `TransactionID` | BIGINT | Unique transaction identifier | Transaction number, sale ID |
| `Date` | DATE | Transaction date | Purchase date, sale date |
| `Time` | TIME | Transaction time | Purchase time, sale time |
| `CustomerID` | BIGINT | Purchasing customer | Buyer ID, account ID |
| `CardID` | BIGINT | Payment card used | Card number, payment method ID |
| `GasStationID` | BIGINT | Station where purchased | Outlet ID, location ID |
| `ProductID` | BIGINT | Fuel product purchased | Fuel type ID |
| `Amount` | BIGINT | Quantity purchased (liters) | Volume, quantity, liters |
| `Price` | DOUBLE | Total transaction price | Cost, total amount |

---

### Table: `ccs.yearmonth`
**Meaning:** Monthly consumption aggregation by customer; also called "monthly summary" or "consumption tracking"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `CustomerID` | BIGINT | Customer identifier | Account ID, buyer ID |
| `Date` | BIGINT | Year-month in YYYYMM format | Period, month, year-month code |
| `Consumption` | DOUBLE | Total fuel consumed (liters) | Volume, total amount, usage |

---

## 3. Join Paths

| Join | Condition |
|------|-----------|
| transactions → customers | `transactions.CustomerID = customers.CustomerID` |
| transactions → gasstations | `transactions.GasStationID = gasstations.GasStationID` |
| transactions → products | `transactions.ProductID = products.ProductID` |
| transactions_1k → customers | `transactions_1k.CustomerID = customers.CustomerID` |
| transactions_1k → gasstations | `transactions_1k.GasStationID = gasstations.GasStationID` |
| transactions_1k → products | `transactions_1k.ProductID = products.ProductID` |
| yearmonth → customers | `yearmonth.CustomerID = customers.CustomerID` |

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation. Apply standard data integrity:
- `CustomerID` values must exist in `ccs.customers` for referential integrity
- `GasStationID` values must exist in `ccs.gasstations` for referential integrity
- `ProductID` values must exist in `ccs.products` for referential integrity
- `Amount` and `Price` are non-negative in transactions
- `Date` in `yearmonth` follows YYYYMM format (e.g., `201207` = July 2012)

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| customer | `ccs.customers` |
| gas station, outlet, station | `ccs.gasstations` |
| fuel type, product | `ccs.products` |
| transaction, sale, purchase | `ccs.transactions` or `ccs.transactions_1k` |
| monthly consumption, consumption tracking | `ccs.yearmonth` |
| customer segment | `customers.Segment` |
| station segment, station type | `gasstations.Segment` |
| country | `gasstations.Country` |
| Czech Republic | `WHERE gasstations.Country = 'CZE'` |
| Slovakia | `WHERE gasstations.Country = 'SVK'` |
| premium station | `WHERE gasstations.Segment = 'Premium'` |
| discount station | `WHERE gasstations.Segment = 'Discount'` |
| SME customer | `WHERE customers.Segment = 'SME'` |
| KAM customer | `WHERE customers.Segment = 'KAM'` |
| LAM customer | `WHERE customers.Segment = 'LAM'` |
| liters, volume, quantity | `transactions.Amount` |
| total price, cost | `transactions.Price` |
| consumption | `yearmonth.Consumption` |