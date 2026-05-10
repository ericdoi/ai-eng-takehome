# SalesDB Reference Guide for SQL Agent

## 1. Schema Summary

SalesDB contains transactional sales data linking customers, employees, products, and orders, enabling revenue analysis, sales attribution, and customer segmentation.

---

## 2. Table Reference

### Table: `SalesDB.Customers`
**Meaning:** Customer master records; also called "Accounts" or "Client List"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `CustomerID` | BIGINT | Unique customer identifier; primary key | Customer Number, Cust ID |
| `FirstName` | VARCHAR | Customer's given name | First Name, Given Name |
| `MiddleInitial` | VARCHAR | Customer's middle initial (single character or NULL) | MI, Middle Initial |
| `LastName` | VARCHAR | Customer's family name | Last Name, Surname |

**Notable values:** `MiddleInitial` contains NULL or single characters (a–z).

---

### Table: `SalesDB.Employees`
**Meaning:** Employee/salesperson master records; also called "Sales Team" or "Staff"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `EmployeeID` | BIGINT | Unique employee identifier; primary key | Employee Number, Emp ID, SalesPersonID |
| `FirstName` | VARCHAR | Employee's given name | First Name, Given Name |
| `MiddleInitial` | VARCHAR | Employee's middle initial (single character or NULL) | MI, Middle Initial |
| `LastName` | VARCHAR | Employee's family name | Last Name, Surname |

**Notable values:** `MiddleInitial` contains NULL or single characters: `'`, `a`, `c`, `e`, `h`, `i`, `l`, `m`, `o`, `r`, `t`, `u`.

---

### Table: `SalesDB.Products`
**Meaning:** Product catalog; also called "Inventory", "SKU List", or "Item Master"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ProductID` | BIGINT | Unique product identifier; primary key | Product Number, SKU, Item ID |
| `Name` | VARCHAR | Product description or name | Product Name, Description, Title |
| `Price` | DOUBLE | Unit retail price in dollars | Unit Price, List Price, MSRP |

**Notable values:** `Price` can be `0.0` (samples/promotional items—exclude from revenue). Sample products: "Adjustable Race" (1.6), "Bearing Ball" (0.8), "Headset Ball Bearings" (0.0).

---

### Table: `SalesDB.Sales`
**Meaning:** Individual sales transactions; also called "Orders", "Order Details", or "Line Items"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `SalesID` | BIGINT | Unique sales transaction identifier; primary key | Order ID, Transaction ID, Sale Number |
| `SalesPersonID` | BIGINT | Employee ID of assigned salesperson at order time | EmployeeID, Sales Rep ID, Assigned Employee |
| `CustomerID` | BIGINT | Customer ID purchasing the product | Cust ID, Buyer ID |
| `ProductID` | BIGINT | Product ID being sold | Item ID, SKU |
| `Quantity` | BIGINT | Number of units sold in this transaction | Units, Order Qty, Qty |

**Notable values:** All columns are non-null in sample data.

---

## 3. Join Paths

| Join | Condition | Purpose |
|------|-----------|---------|
| Sales → Customers | `SalesDB.Sales.CustomerID = SalesDB.Customers.CustomerID` | Attach customer name/details to sales |
| Sales → Employees | `SalesDB.Sales.SalesPersonID = SalesDB.Employees.EmployeeID` | Attach salesperson name/details to sales |
| Sales → Products | `SalesDB.Sales.ProductID = SalesDB.Products.ProductID` | Attach product name/price to sales |
| Customers ← Sales (aggregation) | `SalesDB.Customers.CustomerID = SalesDB.Sales.CustomerID` | Summarize customer lifetime value |
| Employees ← Sales (aggregation) | `SalesDB.Employees.EmployeeID = SalesDB.Sales.SalesPersonID` | Summarize employee sales performance |

---

## 4. Business Rules as SQL

### Revenue Recognition
**Rule:** Revenue is recognized on order date, not ship date; cancelled orders excluded; partial shipments reported at full order value.
- **SQL:** No `OrderDate` or `ShipDate` column exists in schema. No `Status` column exists. **Agent must clarify:** Are these columns missing, or should all `SalesDB.Sales` records be treated as confirmed orders?
- **Interim SQL:** `SELECT SalesID FROM SalesDB.Sales` (assumes all rows are valid revenue)

### Product Metrics
**Rule:** Products with `Price = 0.0` are samples/promotional—track separately, exclude from revenue calculations.
- **SQL:** `WHERE SalesDB.Products.Price > 0.0` (for revenue metrics)
- **SQL:** `WHERE SalesDB.Products.Price = 0.0` (for sample/promo tracking)

### Customer Segmentation
**Rule:** Lifetime purchases > $50,000 = "Enterprise"; > $10,000 and < $50,000 = "Professional"; else = "Standard". Count only customers with ≥1 completed order.
- **SQL (Enterprise):** 
  ```sql
  WHERE (SELECT SUM(SalesDB.Sales.Quantity * SalesDB.Products.Price) 
         FROM SalesDB.Sales 
         JOIN SalesDB.Products ON SalesDB.Sales.ProductID = SalesDB.Products.ProductID 
         WHERE SalesDB.Sales.CustomerID = SalesDB.Customers.CustomerID 
         AND SalesDB.Products.Price > 0.0) > 50000
  ```
- **SQL (Professional):** 
  ```sql
  WHERE (SELECT SUM(...) ...) BETWEEN 10000.01 AND 50000
  ```
- **SQL (Standard):** 
  ```sql
  WHERE (SELECT SUM(...) ...) <= 10000
  ```
- **SQL (completed orders only):** `HAVING COUNT(SalesDB.Sales.SalesID) >= 1`

### Employee Attribution
**Rule:** Sales attributed to employee assigned at order time (`SalesPersonID`); no retrospective reassignment; managers do not receive credit for team member sales.
- **SQL:** Use `SalesDB.Sales.SalesPersonID` directly; do NOT join to current employee assignment table (does not exist in schema).
- **SQL:** `GROUP BY SalesDB.Sales.SalesPersonID` (individual attribution only)

### Discount Handling
**Rule:** No "Discount" column exists in schema. **Agent must clarify:** Is discount stored elsewhere, or should all sales be treated as full-price?
- **Interim SQL:** `SELECT SalesID, Quantity * Products.Price AS GrossRevenue FROM SalesDB.Sales JOIN SalesDB.Products ...`

### Time Period Rules
**Rule:** Fiscal quarters are calendar-aligned (Q1 = Jan–Mar). No date column in schema. **Agent must clarify:** Where is order date stored?
- **Interim SQL:** Cannot implement without `OrderDate` column.

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| Customer name | `CONCAT(SalesDB.Customers.FirstName, ' ', SalesDB.Customers.LastName)` |
| Employee name | `CONCAT(SalesDB.Employees.FirstName, ' ', SalesDB.Employees.LastName)` |
| Salesperson | `SalesDB.Employees` joined via `SalesDB.Sales.SalesPersonID` |
| Sales rep | `SalesDB.Employees` joined via `SalesDB.Sales.SalesPersonID` |
| Order | `SalesDB.Sales` |
| Transaction | `SalesDB.Sales` |
| Line item | `SalesDB.Sales` |
| Revenue | `SUM(SalesDB.Sales.Quantity * SalesDB.Products.Price)` where `SalesDB.Products.Price > 0.0` |
| Gross revenue | `SUM(SalesDB.Sales.Quantity * SalesDB.Products.Price)` |
| Net revenue | Not calculable (no discount column) |
| Customer lifetime value | `SUM(SalesDB.Sales.Quantity * SalesDB.Products.Price)` grouped by `CustomerID` |
| Sales by employee | `SUM(SalesDB.Sales.Quantity * SalesDB.Products.Price)` grouped by `SalesPersonID` |
| Units sold | `SUM(SalesDB.Sales.Quantity)` |
| Sample/promo items | `WHERE SalesDB.Products.Price = 0.0` |
| Active products | `SalesDB.Products` (no discontinuation flag in schema) |
| Enterprise customer | Lifetime value > 50000 |
| Professional customer | Lifetime value 10000.01–50000 |
| Standard customer | Lifetime value ≤ 10000 |

---

## Critical Schema Gaps

The following business rules **cannot be implemented** without additional columns:

1. **Order date / Ship date** – Required for revenue recognition timing and fiscal period reporting.
2. **Order status** (Cancelled, Pending, Completed) – Required to exclude cancelled orders.
3. **Discount field** – Required for net revenue and compliance reporting.
4. **Product discontinuation flag** – Required to distinguish active vs. historical products.
5. **Employee manager assignment** – Required to prevent manager credit for team sales.

**Agent action:** Request schema extension or clarify which rules are out of scope.