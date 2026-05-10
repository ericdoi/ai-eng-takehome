# classicmodels Schema Reference Guide

## Schema Summary
This schema models a classic model car business, tracking customers, sales orders, products, employees, offices, and payments across multiple regions.

---

## Join Paths

**Customers → Orders → Order Details → Products**
```sql
FROM classicmodels.customers c
JOIN classicmodels.orders o ON c.customerNumber = o.customerNumber
JOIN classicmodels.orderdetails od ON o.orderNumber = od.orderNumber
JOIN classicmodels.products p ON od.productCode = p.productCode
```

**Customers → Sales Rep (Employee)**
```sql
FROM classicmodels.customers c
JOIN classicmodels.employees e ON c.salesRepEmployeeNumber = e.employeeNumber
```

**Employees → Office**
```sql
FROM classicmodels.employees e
JOIN classicmodels.offices o ON e.officeCode = o.officeCode
```

**Customers → Payments**
```sql
FROM classicmodels.customers c
JOIN classicmodels.payments p ON c.customerNumber = p.customerNumber
```

**Products → Product Line**
```sql
FROM classicmodels.products p
JOIN classicmodels.productlines pl ON p.productLine = pl.productLine
```

---

## Table Reference

### `classicmodels.customers`
Customer accounts and contact information.

| Column | Notes |
|--------|-------|
| `customerNumber` | Primary key |
| `salesRepEmployeeNumber` | Foreign key to `classicmodels.employees.employeeNumber`; may be NULL |
| `creditLimit` | Maximum credit extended to customer |
| `state` | Enumerated: `BC, CA, CT, Co. Cork, Isle of Wight, MA, NH, NJ, NSW, NV, NY, Osaka, PA, Pretoria, Queensland, Québec, Tokyo, Victoria` |

---

### `classicmodels.orders`
Sales orders placed by customers.

| Column | Notes |
|--------|-------|
| `orderNumber` | Primary key |
| `customerNumber` | Foreign key to `classicmodels.customers.customerNumber` |
| `status` | Enumerated: `Cancelled, Disputed, In Process, On Hold, Resolved, Shipped` |
| `orderDate` | Date order was placed |
| `requiredDate` | Requested delivery date |
| `shippedDate` | Actual shipment date; NULL if not yet shipped |

---

### `classicmodels.orderdetails`
Line items within orders; links orders to products.

| Column | Notes |
|--------|-------|
| `orderNumber` | Foreign key to `classicmodels.orders.orderNumber` |
| `productCode` | Foreign key to `classicmodels.products.productCode` |
| `quantityOrdered` | Units ordered on this line |
| `priceEach` | Unit price at time of order |
| `orderLineNumber` | Sequence within order |

---

### `classicmodels.products`
Product catalog with pricing and inventory.

| Column | Notes |
|--------|-------|
| `productCode` | Primary key |
| `productLine` | Foreign key to `classicmodels.productlines.productLine`; enumerated: `Classic Cars, Motorcycles, Planes, Ships, Trains, Trucks and Buses, Vintage Cars` |
| `productScale` | Enumerated: `1:10, 1:12, 1:18, 1:24, 1:32, 1:50, 1:700, 1:72` |
| `productVendor` | Manufacturer/supplier name |
| `quantityInStock` | Current inventory level |
| `buyPrice` | Cost to acquire product |
| `MSRP` | Manufacturer's suggested retail price |

---

### `classicmodels.productlines`
Product category definitions.

| Column | Notes |
|--------|-------|
| `productLine` | Primary key; enumerated: `Classic Cars, Motorcycles, Planes, Ships, Trains, Trucks and Buses, Vintage Cars` |
| `textDescription` | Long-form category description |

---

### `classicmodels.payments`
Customer payment transactions.

| Column | Notes |
|--------|-------|
| `customerNumber` | Foreign key to `classicmodels.customers.customerNumber` |
| `checkNumber` | Check/payment reference identifier |
| `paymentDate` | Date payment was received |
| `amount` | Payment amount |

---

### `classicmodels.employees`
Sales and management staff.

| Column | Notes |
|--------|-------|
| `employeeNumber` | Primary key |
| `officeCode` | Foreign key to `classicmodels.offices.officeCode`; enumerated: `1, 2, 3, 4, 5, 6, 7` |
| `reportsTo` | Foreign key to `classicmodels.employees.employeeNumber` (manager); NULL for President |
| `jobTitle` | Enumerated: `President, Sale Manager (EMEA), Sales Manager (APAC), Sales Manager (NA), Sales Rep, VP Marketing, VP Sales` |
| `extension` | Phone extension |

---

### `classicmodels.offices`
Regional sales offices.

| Column | Notes |
|--------|-------|
| `officeCode` | Primary key; enumerated: `1, 2, 3, 4, 5, 6, 7` |
| `city` | Enumerated: `Boston, London, NYC, Paris, San Francisco, Sydney, Tokyo` |
| `territory` | Sales region; enumerated: `APAC, EMEA, Japan, NA` |
| `country` | Enumerated: `Australia, France, Japan, UK, USA` |