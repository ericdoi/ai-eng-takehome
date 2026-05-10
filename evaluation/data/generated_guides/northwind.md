# Northwind Sales Database Reference Guide

## Schema Summary

The `northwind` schema contains transactional sales data including customers, orders, products, employees, suppliers, and regional territories for a multi-national distribution business.

---

## Table Reference

### northwind.Categories
**Meaning:** Product categories (e.g., Beverages, Seafood). Synonym: product lines, classifications.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `CategoryID` | BIGINT | Unique category identifier | category code |
| `CategoryName` | VARCHAR | Category display name | category, type |
| `Description` | VARCHAR | Category description text | details |
| `Picture` | BLOB | Binary image data | image, photo |

**Notable values:** Beverages, Condiments, Confections, Dairy Products, Grains/Cereals, Meat/Poultry, Produce, Seafood

---

### northwind.Customers
**Meaning:** Customer company records. Synonyms: accounts, clients, buyers.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `CustomerID` | VARCHAR | Unique customer identifier (5-char code) | customer code, account ID |
| `CompanyName` | VARCHAR | Customer company legal name | company, account name |
| `ContactName` | VARCHAR | Primary contact person name | contact, person |
| `ContactTitle` | VARCHAR | Contact person's job title | title, role |
| `Address` | VARCHAR | Street address | street, location |
| `City` | VARCHAR | City name | municipality |
| `Region` | VARCHAR | State/province code | state, province |
| `PostalCode` | VARCHAR | Postal/ZIP code | zip, postal |
| `Country` | VARCHAR | Country name | nation |
| `Phone` | VARCHAR | Telephone number | phone, contact phone |
| `Fax` | VARCHAR | Fax number | fax |

**Notable values (ContactTitle):** Accounting Manager, Assistant Sales Agent, Marketing Manager, Owner, Sales Manager, Sales Representative

---

### northwind.Employees
**Meaning:** Employee staff records. Synonyms: staff, sales team, personnel.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `EmployeeID` | BIGINT | Unique employee identifier | employee code, staff ID |
| `LastName` | VARCHAR | Employee surname | last name, family name |
| `FirstName` | VARCHAR | Employee given name | first name, given name |
| `Title` | VARCHAR | Job title | position, role |
| `TitleOfCourtesy` | VARCHAR | Salutation (Mr., Mrs., Dr., Ms.) | courtesy, salutation |
| `BirthDate` | TIMESTAMP | Date of birth | DOB, birth |
| `HireDate` | TIMESTAMP | Employment start date | start date, hired |
| `Address` | VARCHAR | Home street address | street |
| `City` | VARCHAR | Home city | municipality |
| `Region` | VARCHAR | Home state/province | state |
| `PostalCode` | VARCHAR | Home postal code | zip |
| `Country` | VARCHAR | Home country | nation |
| `HomePhone` | VARCHAR | Home telephone | phone |
| `Extension` | VARCHAR | Office phone extension | ext, extension |
| `Photo` | BLOB | Employee photograph binary | image, picture |
| `Notes` | VARCHAR | Employee biography/background | bio, background |
| `ReportsTo` | BIGINT | Manager's EmployeeID (self-reference) | manager, supervisor |
| `PhotoPath` | VARCHAR | URL path to employee photo | photo URL, image path |
| `Salary` | DOUBLE | Annual compensation in currency units | compensation, pay |

**Notable values (Title):** Inside Sales Coordinator, Sales Manager, Sales Representative, Vice President, Sales

---

### northwind.EmployeeTerritories
**Meaning:** Assignment of employees to sales territories (many-to-many). Synonyms: territory assignments, coverage.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `EmployeeID` | BIGINT | Employee identifier (FK to Employees) | employee |
| `TerritoryID` | VARCHAR | Territory identifier (FK to Territories) | territory |

---

### northwind.Orders
**Meaning:** Sales orders placed by customers. Synonyms: transactions, sales orders, purchase orders.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `OrderID` | BIGINT | Unique order identifier | order number, order code |
| `CustomerID` | VARCHAR | Customer identifier (FK to Customers) | customer |
| `EmployeeID` | BIGINT | Salesperson identifier (FK to Employees) | salesperson, sales rep, employee |
| `OrderDate` | TIMESTAMP | Date order was placed | order date, date placed |
| `RequiredDate` | TIMESTAMP | Requested delivery date | due date, required by |
| `ShippedDate` | TIMESTAMP | Actual shipment date | shipped, delivery date |
| `ShipVia` | BIGINT | Shipper identifier (FK to Shippers) | shipper, carrier |
| `Freight` | DOUBLE | Shipping cost in currency units | shipping, shipping cost |
| `ShipName` | VARCHAR | Recipient company name | ship to, recipient |
| `ShipAddress` | VARCHAR | Recipient street address | ship address |
| `ShipCity` | VARCHAR | Recipient city | ship city |
| `ShipRegion` | VARCHAR | Recipient state/province | ship region, ship state |
| `ShipPostalCode` | VARCHAR | Recipient postal code | ship postal, ship zip |
| `ShipCountry` | VARCHAR | Recipient country | ship country |

**Notable values (ShipRegion):** AK, BC, CA, DF, ID, MT, NM, OR, WA, WY, and international codes

---

### northwind.Order Details
**Meaning:** Line items within orders (one order → many line items). Synonyms: order lines, line items, order items.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `OrderID` | BIGINT | Order identifier (FK to Orders) | order |
| `ProductID` | BIGINT | Product identifier (FK to Products) | product |
| `UnitPrice` | DOUBLE | Price per unit at time of order | price, unit price |
| `Quantity` | BIGINT | Number of units ordered | qty, units |
| `Discount` | DOUBLE | Discount as decimal (0.0–1.0, e.g., 0.15 = 15%) | discount rate, discount % |

---

### northwind.Products
**Meaning:** Product catalog. Synonyms: items, SKUs, merchandise.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ProductID` | BIGINT | Unique product identifier | product code, SKU |
| `ProductName` | VARCHAR | Product display name | name, title |
| `SupplierID` | BIGINT | Supplier identifier (FK to Suppliers) | supplier |
| `CategoryID` | BIGINT | Category identifier (FK to Categories) | category |
| `QuantityPerUnit` | VARCHAR | Packaging description (e.g., "10 boxes x 20 bags") | packaging, unit description |
| `UnitPrice` | DOUBLE | Current list price in currency units | price, list price |
| `UnitsInStock` | BIGINT | Current inventory quantity on hand | stock, inventory, on hand |
| `UnitsOnOrder` | BIGINT | Quantity on pending purchase orders | on order, pending |
| `ReorderLevel` | BIGINT | Minimum inventory threshold for reorder | reorder point, min stock |
| `Discontinued` | BOOLEAN | Whether product is no longer sold | active, status |

---

### northwind.Suppliers
**Meaning:** Vendor/supplier company records. Synonyms: vendors, sources, manufacturers.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `SupplierID` | BIGINT | Unique supplier identifier | supplier code |
| `CompanyName` | VARCHAR | Supplier company legal name | company, vendor name |
| `ContactName` | VARCHAR | Primary contact person name | contact |
| `ContactTitle` | VARCHAR | Contact person's job title | title, role |
| `Address` | VARCHAR | Street address | street |
| `City` | VARCHAR | City name | municipality |
| `Region` | VARCHAR | State/province code | state, province |
| `PostalCode` | VARCHAR | Postal code | zip |
| `Country` | VARCHAR | Country name | nation |
| `Phone` | VARCHAR | Telephone number | phone |
| `Fax` | VARCHAR | Fax number | fax |
| `HomePage` | VARCHAR | Website URL or HTML reference | website, URL |

---

### northwind.Shippers
**Meaning:** Shipping/logistics carrier companies. Synonyms: carriers, logistics providers.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ShipperID` | BIGINT | Unique shipper identifier | shipper code |
| `CompanyName` | VARCHAR | Carrier company name | carrier, company |
| `Phone` | VARCHAR | Contact telephone | phone |

**Notable values (CompanyName):** Speedy Express, United Package, Federal Shipping

---

### northwind.Territories
**Meaning:** Geographic sales territories. Synonyms: regions, sales areas, zones.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `TerritoryID` | VARCHAR | Unique territory identifier (5-digit code) | territory code |
| `TerritoryDescription` | VARCHAR | Territory name/description | territory name, description |
| `RegionID` | BIGINT | Region identifier (FK to Region) | region |

---

### northwind.Region
**Meaning:** High-level geographic regions grouping territories. Synonyms: sales regions, divisions.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `RegionID` | BIGINT | Unique region identifier | region code |
| `RegionDescription` | VARCHAR | Region name | region name |

**Notable values (RegionDescription):** Eastern, Northern, Southern, Westerns

---

### northwind.CustomerDemographics
**Meaning:** Customer demographic classification types. Synonyms: customer types, segments.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `CustomerTypeID` | VARCHAR | Unique demographic type identifier | type code |
| `CustomerDesc` | VARCHAR | Description of demographic type | description, type name |

---

### northwind.CustomerCustomerDemo
**Meaning:** Assignment of customers to demographic types (many-to-many). Synonyms: customer classifications, segment assignments.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `CustomerID` | VARCHAR | Customer identifier (FK to Customers) | customer |
| `CustomerTypeID` | VARCHAR | Demographic type identifier (FK to CustomerDemographics) | type |

---

### View Tables (Read-Only)

The following are pre-built views and should be queried as-is; they aggregate or filter base tables:

- **northwind.Alphabetical list of products** — Products sorted alphabetically with category name
- **northwind.Current Product List** — Active (non-discontinued) products
- **northwind.Category Sales for 1997** — Total sales by category for 1997
- **northwind.Product Sales for 1997** — Sales by product for 1997
- **northwind.Order Details Extended** — Order line items with extended price
- **northwind.Order Subtotals** — Order totals before freight
- **northwind.Sales Totals by Amount** — Orders ranked by sale amount
- **northwind.Sales by Category** — Sales breakdown by category
- **northwind.Summary of Sales by Quarter** — Quarterly sales summary
- **northwind.Summary of Sales by Year** — Annual sales summary
- **northwind.Products Above Average Price** — Products priced above catalog average
- **northwind.Products by Category** — Products grouped by category
- **northwind.Customer and Suppliers by City** — Customers and suppliers co-located by city
- **northwind.Quarterly Orders** — Orders grouped by quarter
- **northwind.Orders Qry** — Orders with customer details joined

---

## Join Paths

### Orders → Customers
```sql
Orders o
INNER JOIN Customers c ON o.CustomerID = c.CustomerID
```

### Orders → Employees
```sql
Orders o
INNER JOIN Employees e ON o.EmployeeID = e.EmployeeID
```

### Orders → Shippers
```sql
Orders o
INNER JOIN Shippers s ON o.ShipVia = s.ShipperID
```

### Order Details → Products
```sql
"Order Details" od
INNER JOIN Products p ON od.ProductID = p.ProductID
```

### Order Details → Orders
```sql
"Order Details" od
INNER JOIN Orders o ON od.OrderID = o.OrderID
```

### Products → Categories
```sql
Products p
INNER JOIN Categories c ON p.CategoryID = c.CategoryID
```

### Products → Suppliers
```sql
Products p
INNER JOIN Suppliers s ON p.SupplierID = s.SupplierID
```

### Employees → Employees (Manager Hierarchy)
```sql
Employees e
LEFT JOIN Employees m ON e.ReportsTo = m.EmployeeID
```

### Employees → Territories
```sql
Employees e
INNER JOIN EmployeeTerritories et ON e.EmployeeID = et.EmployeeID
INNER JOIN Territories t ON et.TerritoryID = t.TerritoryID
```

### Territories → Region
```sql
Territories t
INNER JOIN Region r ON t.RegionID = r.RegionID
```

### Customers → Demographics
```sql
Customers c
INNER JOIN CustomerCustomerDemo ccd ON c.CustomerID = ccd.CustomerID
INNER JOIN CustomerDemographics cd ON ccd.CustomerTypeID = cd.CustomerTypeID
```

---

## Business Rules as SQL

### Revenue Recognition
**Rule:** Revenue is recognized on the order date, NOT the ship date.
```sql
WHERE Orders.OrderDate IS NOT NULL
-- Use OrderDate for all revenue period assignment
```

**Rule:** Orders with "Cancelled" status should be completely excluded from all revenue metrics.
```sql
-- Note: No explicit "Status" column exists in Orders table.
-- Cancelled orders may be identified by NULL ShippedDate + RequiredDate < CURRENT_DATE
-- Verify with business owner; currently no direct cancellation flag.
WHERE Orders.ShippedDate IS NOT NULL OR Orders.OrderDate >= DATEADD(day, -30, CURRENT_DATE)
```

**Rule:** Partial shipments should be reported at full order value when order is placed, not when items ship.
```sql
-- Sum Order Details line items by OrderID; do not filter by ShippedDate
SELECT 
  od.OrderID,
  SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS NetRevenue
FROM "Order Details" od
GROUP BY od.OrderID
```

---

### Product Metrics
**Rule:** Discontinued products should be excluded from "active catalog" counts but included in historical sales analysis.
```sql
-- Active catalog:
WHERE Products.Discontinued = FALSE

-- Historical sales (include discontinued):
-- No WHERE clause on Discontinued
```

**Rule:** Products with unit price = $0 are samples or promotional items—track separately, not as revenue.
```sql
-- Exclude from revenue:
WHERE Products.UnitPrice > 0

-- Track separately:
WHERE Products.UnitPrice = 0
```

**Rule:** Inventory value is calculated at cost, not at retail price—never mix these in reports.
```sql
-- Use UnitPrice from Products table (list price) only for revenue.
-- Cost data not present in schema; flag for data model review.
```

---

### Customer Segmentation
**Rule:** Customers with lifetime purchases > $50,000 are "Enterprise" tier.
```sql
HAVING SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) > 50000
-- Tier = 'Enterprise'
```

**Rule:** Customers with lifetime purchases > $10,000 but < $50,000 are "Professional" tier.
```sql
HAVING SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) > 10000
  AND SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) <= 50