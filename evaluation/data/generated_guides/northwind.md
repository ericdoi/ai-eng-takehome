# Northwind Sales Database Reference Guide

## Schema Summary
Northwind is a transactional sales database tracking orders, products, customers, employees, and suppliers with historical sales views and category/regional aggregations.

---

## Join Paths

**Orders → Customers:**
```sql
FROM northwind.Orders o
JOIN northwind.Customers c ON o.CustomerID = c.CustomerID
```

**Orders → Order Details → Products:**
```sql
FROM northwind.Orders o
JOIN northwind."Order Details" od ON o.OrderID = od.OrderID
JOIN northwind.Products p ON od.ProductID = p.ProductID
```

**Orders → Employees:**
```sql
FROM northwind.Orders o
JOIN northwind.Employees e ON o.EmployeeID = e.EmployeeID
```

**Employees → Territories:**
```sql
FROM northwind.Employees e
JOIN northwind.EmployeeTerritories et ON e.EmployeeID = et.EmployeeID
JOIN northwind.Territories t ON et.TerritoryID = t.TerritoryID
```

**Products → Suppliers:**
```sql
FROM northwind.Products p
JOIN northwind.Suppliers s ON p.SupplierID = s.SupplierID
```

**Products → Categories:**
```sql
FROM northwind.Products p
JOIN northwind.Categories c ON p.CategoryID = c.CategoryID
```

**Orders → Shippers:**
```sql
FROM northwind.Orders o
JOIN northwind.Shippers sh ON o.ShipVia = sh.ShipperID
```

---

## Business Rules as SQL

**Rule: Revenue recognized on order date, not ship date**
```sql
WHERE o.OrderDate IS NOT NULL
-- Use OrderDate for all revenue metrics, ignore ShippedDate
```

**Rule: Exclude cancelled orders from revenue**
```sql
-- Note: No "Status" column exists in Orders table; verify cancellation logic with business owner
```

**Rule: Enterprise tier (lifetime > $50,000)**
```sql
HAVING SUM(od.Quantity * od.UnitPrice * (1 - od.Discount)) > 50000
```

**Rule: Professional tier (lifetime $10,000–$50,000)**
```sql
HAVING SUM(od.Quantity * od.UnitPrice * (1 - od.Discount)) BETWEEN 10000 AND 50000
```

**Rule: Standard tier (all others with ≥1 completed order)**
```sql
HAVING SUM(od.Quantity * od.UnitPrice * (1 - od.Discount)) < 10000
```

**Rule: Exclude discontinued products from active catalog**
```sql
WHERE p.Discontinued = FALSE
```

**Rule: Exclude zero-price items from revenue (samples/promos)**
```sql
WHERE od.UnitPrice > 0
```

**Rule: Net revenue calculation**
```sql
SUM(od.Quantity * od.UnitPrice * (1 - od.Discount)) AS NetRevenue
```

**Rule: Gross revenue (before discount)**
```sql
SUM(od.Quantity * od.UnitPrice) AS GrossRevenue
```

**Rule: High-discount orders (>25%) flagged for compliance**
```sql
WHERE od.Discount > 0.25
```

**Rule: Fiscal quarters (calendar-aligned)**
```sql
WHERE QUARTER(o.OrderDate) = 1  -- Q1 = Jan–Mar
```

**Rule: Freeze period (Dec 20–31)**
```sql
WHERE MONTH(o.OrderDate) = 12 AND DAY(o.OrderDate) >= 20
```

---

## Synonym Glossary

| Business Term | Schema Reference |
|---|---|
| Revenue, Sales | `SUM(od.Quantity * od.UnitPrice * (1 - od.Discount))` from `northwind."Order Details"` |
| Gross revenue | `SUM(od.Quantity * od.UnitPrice)` |
| Order value | `od.Quantity * od.UnitPrice * (1 - od.Discount)` |
| Discount rate | `od.Discount` (decimal 0.0–1.0, not percentage) |
| Salesperson, Sales rep | `northwind.Employees` with `Title` containing "Sales" |
| Territory | `northwind.Territories.TerritoryDescription` |
| Shipper, Carrier | `northwind.Shippers.CompanyName` |
| Supplier, Vendor | `northwind.Suppliers` |
| Product line, Category | `northwind.Categories.CategoryName` |
| Inventory on hand | `northwind.Products.UnitsInStock` |
| Reorder point | `northwind.Products.ReorderLevel` |
| Customer lifetime value | `SUM(od.Quantity * od.UnitPrice * (1 - od.Discount))` grouped by `CustomerID` |
| Active products | `WHERE northwind.Products.Discontinued = FALSE` |
| Discontinued products | `WHERE northwind.Products.Discontinued = TRUE` |

---

## Table Reference

### `northwind.Orders`
**Meaning:** Order header records; one row per order placed.  
**Synonyms:** Sales orders, transactions.

| Column | Notes |
|---|---|
| `OrderID` | Primary key. |
| `CustomerID` | Foreign key to `northwind.Customers`. |
| `EmployeeID` | Foreign key to `northwind.Employees`; employee assigned at order time (not current). |
| `OrderDate` | **Revenue recognition date** (not `ShippedDate`). |
| `RequiredDate` | Requested delivery date. |
| `ShippedDate` | Actual ship date; may be NULL if not yet shipped. |
| `ShipVia` | Foreign key to `northwind.Shippers.ShipperID`. |
| `Freight` | Shipping cost (DOUBLE). |
| `ShipName`, `ShipAddress`, `ShipCity`, `ShipRegion`, `ShipPostalCode`, `ShipCountry` | Delivery address; may differ from customer address. |

---

### `northwind."Order Details"`
**Meaning:** Line items within orders; one row per product per order.  
**Synonyms:** Order lines, line items.

| Column | Notes |
|---|---|
| `OrderID` | Foreign key to `northwind.Orders`. |
| `ProductID` | Foreign key to `northwind.Products`. |
| `UnitPrice` | Price at time of order (DOUBLE); may differ from current `northwind.Products.UnitPrice`. |
| `Quantity` | Units ordered (BIGINT). |
| `Discount` | Decimal 0.0–1.0 (e.g., 0.15 = 15% off); **not a dollar amount**. Orders with `Discount > 0.25` require compliance review. |

---

### `northwind.Customers`
**Meaning:** Customer master; one row per customer account.  
**Synonyms:** Accounts, clients.

| Column | Notes |
|---|---|
| `CustomerID` | Primary key (VARCHAR). |
| `CompanyName` | Customer organization name. |
| `ContactName`, `ContactTitle` | Primary contact. `ContactTitle` values: Accounting Manager, Assistant Sales Agent, Marketing Manager, Owner, Sales Representative, etc. |
| `Address`, `City`, `Region`, `PostalCode`, `Country` | Billing/primary address. |
| `Phone`, `Fax` | Contact numbers. |

---

### `northwind.Products`
**Meaning:** Product catalog; one row per SKU.  
**Synonyms:** Items, SKUs.

| Column | Notes |
|---|---|
| `ProductID` | Primary key. |
| `ProductName` | Product description. |
| `SupplierID` | Foreign key to `northwind.Suppliers`. |
| `CategoryID` | Foreign key to `northwind.Categories`. |
| `QuantityPerUnit` | Packaging description (e.g., "10 boxes x 20 bags"). |
| `UnitPrice` | Current list price (DOUBLE). **Do not use for historical revenue**; use `northwind."Order Details".UnitPrice` instead. |
| `UnitsInStock` | Current inventory quantity. |
| `UnitsOnOrder` | Quantity on pending purchase orders. |
| `ReorderLevel` | Minimum stock threshold. |
| `Discontinued` | BOOLEAN; `TRUE` = no longer sold. Exclude from active catalog counts; include in historical analysis. |

---

### `northwind.Employees`
**Meaning:** Employee roster; one row per employee.  
**Synonyms:** Staff, sales team.

| Column | Notes |
|---|---|
| `EmployeeID` | Primary key. |
| `LastName`, `FirstName` | Employee name. |
| `Title` | Job title. Values: Sales Representative, Sales Manager, Vice President Sales, Inside Sales Coordinator. |
| `TitleOfCourtesy` | Salutation (Mr., Mrs., Ms., Dr.). |
| `BirthDate`, `HireDate` | TIMESTAMP. |
| `Address`, `City`, `Region`, `PostalCode`, `Country` | Home address. |
| `HomePhone`, `Extension` | Contact. |
| `ReportsTo` | Foreign key to `northwind.Employees` (manager's EmployeeID); NULL for top-level. |
| `Salary` | DOUBLE. |

---

### `northwind.Categories`
**Meaning:** Product category master.  
**Synonyms:** Product lines, segments.

| Column | Notes |
|---|---|
| `CategoryID` | Primary key. |
| `CategoryName` | Exact values: Beverages, Condiments, Confections, Dairy Products, Grains/Cereals, Meat/Poultry, Produce, Seafood. |
| `Description` | Category description. |

---

### `northwind.Suppliers`
**Meaning:** Supplier/vendor master.  
**Synonyms:** Vendors.

| Column | Notes |
|---|---|
| `SupplierID` | Primary key. |
| `CompanyName` | Supplier organization. |
| `ContactName`, `ContactTitle` | Primary contact and role. |
| `Address`, `City`, `Region`, `PostalCode`, `Country` | Supplier location. |
| `Phone`, `Fax` | Contact numbers. |
| `HomePage` | URL or reference (may contain markup). |

---

### `northwind.Shippers`
**Meaning:** Shipping carrier master.  
**Synonyms:** Carriers, logistics providers.

| Column | Notes |
|---|---|
| `ShipperID` | Primary key. |
| `CompanyName` | Exact values: Speedy Express, United Package, Federal Shipping. |
| `Phone` | Carrier contact. |

---

### `northwind.Territories`
**Meaning:** Sales territory definitions.  
**Synonyms:** Sales regions, zones.

| Column | Notes |
|---|---|
| `TerritoryID` | Primary key (VARCHAR, e.g., "01581"). |
| `TerritoryDescription` | Territory name (e.g., "Westboro"). |
| `RegionID` | Foreign key to `northwind.Region`. |

---

### `northwind.EmployeeTerritories`
**Meaning:** Many-to-many mapping of employees to territories.

| Column | Notes |
|---|---|
| `EmployeeID` | Foreign key to `northwind.Employees`. |
| `TerritoryID` | Foreign key to `northwind.Territories`. |

---

### `northwind.Region`
**Meaning:** High-level regional groupings.

| Column | Notes |
|---|---|
| `RegionID` | Primary key. |
| `RegionDescription` | Exact values: Eastern, Northern, Southern, Westerns. |

---

### `northwind.CustomerDemographics`
**Meaning:** Customer demographic type definitions.

| Column | Notes |
|---|---|
| `CustomerTypeID` | Primary key (VARCHAR). |
| `CustomerDesc` | Demographic description. |

---

### `northwind.CustomerCustomerDemo`
**Meaning:** Many-to-many mapping of customers to demographic types.

| Column | Notes |
|---|---|
| `CustomerID` | Foreign key to `northwind.Customers`. |
| `CustomerTypeID` | Foreign key to `northwind.CustomerDemographics`. |

---

### View Tables (Read-Only Aggregations)

**`northwind.Invoices`**  
Denormalized invoice view combining Orders, Order Details, Products, Customers, Employees, Shippers. Use for reporting; do not join with base tables to avoid duplication.

**`northwind."Order Details Extended"`**  
Order Details with product name and extended price pre-calculated.

**`northwind."Order Subtotals"`**  
Order-level subtotals (before freight).

**`northwind."Category Sales for 1997"`**  
Aggregated sales by category for 1997 only.

**`northwind."Product Sales for 1997"`**  
Aggregated sales by product for 1997 only.

**`northwind."Sales by Category"`**  
Product-level sales by category.

**`northwind."Sales Totals by Amount"`**  
Orders ranked/grouped by sale amount.

**`northwind."Summary of Sales by Quarter"`, `northwind."Summary of Sales by Year"`**  
Time-series aggregations by ship date.

**`northwind."Alphabetical list of products"`, `northwind."Current Product List"`, `northwind."Products Above Average Price"`, `northwind."Products by Category"`**  
Filtered/sorted product views.

**`northwind."Customer and Suppliers by City"`, `northwind."Quarterly Orders"`**  
Denormalized customer/supplier views.

---

## Notes

- **No cancellation status column:** Verify with business owner how cancelled orders are identified (if at all).
- **Discount is decimal, not percentage:** Always multiply by 100 for display or compare to 0.25 (not 25).
- **Historical pricing:** Always use `northwind."Order Details".UnitPrice`, never current `northwind.Products.UnitPrice`, for revenue calculations.
- **Employee attribution:** Use `northwind.Orders.EmployeeID` at order time; do not use current employee assignment.
- **Freeze period:** December 20–31 orders may inflate period-end metrics; flag separately in reports.