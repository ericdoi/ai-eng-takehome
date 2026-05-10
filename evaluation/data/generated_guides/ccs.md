# CCS Schema Reference Guide

## Schema Summary
This schema contains fuel transaction data from gas stations across Czech Republic and Slovakia, tracking customer purchases by product type with associated customer and station metadata.

---

## Join Paths

**Transactions to customers:**
```sql
FROM ccs.transactions t
JOIN ccs.customers c ON t.CustomerID = c.CustomerID
```

**Transactions to gas stations:**
```sql
FROM ccs.transactions t
JOIN ccs.gasstations g ON t.GasStationID = g.GasStationID
```

**Transactions to products:**
```sql
FROM ccs.transactions t
JOIN ccs.products p ON t.ProductID = p.ProductID
```

**Full transaction context:**
```sql
FROM ccs.transactions t
JOIN ccs.customers c ON t.CustomerID = c.CustomerID
JOIN ccs.gasstations g ON t.GasStationID = g.GasStationID
JOIN ccs.products p ON t.ProductID = p.ProductID
```

**Customer consumption history:**
```sql
FROM ccs.yearmonth ym
JOIN ccs.customers c ON ym.CustomerID = c.CustomerID
```

---

## Table Reference

### `ccs.customers`
Customer master data with segmentation and billing currency.

| Column | Notes |
|--------|-------|
| **Segment** | Enum: `KAM` (key account), `LAM` (large account), `SME` (small/medium enterprise) |
| **Currency** | Enum: `CZK` (Czech koruna), `EUR` (euro) |

### `ccs.gasstations`
Gas station locations and chain affiliations.

| Column | Notes |
|--------|-------|
| **ChainID** | Identifies fuel station chain/operator |
| **Country** | Enum: `CZE` (Czech Republic), `SVK` (Slovakia) |
| **Segment** | Station category. Enum: `Discount`, `Noname`, `Other`, `Premium`, `Value for money` |

### `ccs.products`
Fuel product types.

| Column | Notes |
|--------|-------|
| **Description** | Product name (e.g., "Nafta" = diesel, "Super" = premium gasoline, "Natural" = natural gas) |

### `ccs.transactions`
Individual fuel purchase transactions (no transaction ID).

| Column | Notes |
|--------|-------|
| **Date** | Transaction date |
| **Time** | Transaction time |
| **Amount** | Quantity purchased (unit depends on product; typically liters) |
| **Price** | Total transaction price in customer's currency |

### `ccs.transactions_1k`
Sample of 1,000 transactions with explicit transaction ID.

| Column | Notes |
|--------|-------|
| **TransactionID** | Unique transaction identifier |
| **Date** | Transaction date |
| **Time** | Transaction time |
| **Amount** | Quantity purchased |
| **Price** | Total transaction price |

### `ccs.yearmonth`
Monthly consumption aggregates by customer.

| Column | Notes |
|--------|-------|
| **Date** | Year-month as integer (YYYYMM format, e.g., 201207 = July 2012) |
| **Consumption** | Total fuel consumption for the month |

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| fuel purchase, transaction | `ccs.transactions` or `ccs.transactions_1k` |
| customer segment | `ccs.customers.Segment` |
| station type, station category | `ccs.gasstations.Segment` |
| fuel type, product | `ccs.products.Description` |
| quantity, volume | `ccs.transactions.Amount` |
| transaction value, cost | `ccs.transactions.Price` |
| monthly usage | `ccs.yearmonth.Consumption` |
| location | `ccs.gasstations.Country` |