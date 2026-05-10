# SalesDB Reference Guide for SQL Agent

## 1. Schema Summary

SalesDB contains transactional sales data: customers, employees, products, and individual sales orders with quantities.

---

## 2. Join Paths

**Sales to all dimensions:**
```sql
FROM SalesDB.Sales s
JOIN SalesDB.Employees e ON s.SalesPersonID = e.EmployeeID
JOIN SalesDB.Customers c ON s.CustomerID = c.CustomerID
JOIN SalesDB.Products p ON s.ProductID = p.ProductID
```

**Sales by salesperson:**
```sql
FROM SalesDB.Sales s
JOIN SalesDB.Employees e ON s.SalesPersonID = e.EmployeeID
```

**Sales by customer:**
```sql
FROM SalesDB.Sales s
JOIN SalesDB.Customers c ON s.CustomerID = c.CustomerID
```

**Product sales:**
```sql
FROM SalesDB.Sales s
JOIN SalesDB.Products p ON s.ProductID = p.ProductID
```

---

## 3. Business Rules as SQL

| Rule | SQL Condition |
|------|---------------|
| Exclude zero-price products from revenue | `WHERE SalesDB.Products.Price > 0` |
| Enterprise tier customers | `HAVING SUM(SalesDB.Sales.Quantity * SalesDB.Products.Price) > 50000` |
| Professional tier customers | `HAVING SUM(SalesDB.Sales.Quantity * SalesDB.Products.Price) BETWEEN 10000.01 AND 50000` |
| Standard tier customers | `HAVING SUM(SalesDB.Sales.Quantity * SalesDB.Products.Price) <= 10000` |
| Revenue calculation | `SalesDB.Sales.Quantity * SalesDB.Products.Price` |
| Attribution uses order-time employee | Use `SalesDB.Sales.SalesPersonID` (immutable at order creation) |

---

## 4. Synonym Glossary

| Common Term | Schema Reference |
|-------------|------------------|
| Revenue / Sales amount | `SalesDB.Sales.Quantity * SalesDB.Products.Price` |
| Salesperson / Sales rep / Agent | `SalesDB.Employees` joined via `SalesDB.Sales.SalesPersonID` |
| Buyer / Purchaser | `SalesDB.Customers` joined via `SalesDB.Sales.CustomerID` |
| Item / SKU | `SalesDB.Products` joined via `SalesDB.Sales.ProductID` |
| Order / Transaction | `SalesDB.Sales` row |
| Units sold / Order quantity | `SalesDB.Sales.Quantity` |
| Customer lifetime value | `SUM(SalesDB.Sales.Quantity * SalesDB.Products.Price)` grouped by `CustomerID` |
| Top performer / Leading salesperson | `SalesDB.Employees` ranked by total revenue from `SalesDB.Sales` |

---

## 5. Table Reference

### `SalesDB.Customers`
Plain-English: Customer master data.

| Column | Notes |
|--------|-------|
| `CustomerID` | Primary key; join to `SalesDB.Sales.CustomerID` |
| `FirstName`, `MiddleInitial`, `LastName` | Customer name components |

---

### `SalesDB.Employees`
Plain-English: Employee/salesperson master data.

| Column | Notes |
|--------|-------|
| `EmployeeID` | Primary key; join to `SalesDB.Sales.SalesPersonID` |
| `FirstName`, `MiddleInitial`, `LastName` | Employee name components |
| `MiddleInitial` | Enumerated values: `'', 'a', 'c', 'e', 'h', 'i', 'l', 'm', 'o', 'r', 't', 'u'` |

---

### `SalesDB.Products`
Plain-English: Product catalog.

| Column | Notes |
|--------|-------|
| `ProductID` | Primary key; join to `SalesDB.Sales.ProductID` |
| `Price` | Unit price in dollars; `0.0` indicates sample/promotional item (exclude from revenue metrics) |

---

### `SalesDB.Sales`
Plain-English: Individual sales transactions.

| Column | Notes |
|--------|-------|
| `SalesID` | Primary key |
| `SalesPersonID` | Foreign key to `SalesDB.Employees.EmployeeID`; immutable at order creation (use for historical attribution) |
| `CustomerID` | Foreign key to `SalesDB.Customers.CustomerID` |
| `ProductID` | Foreign key to `SalesDB.Products.ProductID` |
| `Quantity` | Units ordered; multiply by `SalesDB.Products.Price` for revenue |