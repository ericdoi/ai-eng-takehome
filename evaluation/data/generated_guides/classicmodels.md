# ClassicModels Schema Reference Guide

## Schema Summary
The `classicmodels` schema contains a relational database of a classic model car business, tracking customers, employees, offices, products, orders, order details, payments, and product lines.

---

## Table Reference

### classicmodels.customers
**Meaning:** Customer accounts and contact information.
**Synonyms:** Accounts, clients, buyers.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `customerNumber` | BIGINT | Unique customer identifier | customer ID, account number |
| `customerName` | VARCHAR | Company/business name | account name, company |
| `contactLastName` | VARCHAR | Last name of primary contact person | surname |
| `contactFirstName` | VARCHAR | First name of primary contact person | given name |
| `phone` | VARCHAR | Customer phone number | telephone |
| `addressLine1` | VARCHAR | Primary street address | street, address |
| `addressLine2` | VARCHAR | Secondary address info (suite, floor, etc.) | address line 2 |
| `city` | VARCHAR | City of customer location | |
| `state` | VARCHAR | State/province code | province, region |
| `postalCode` | VARCHAR | Postal/ZIP code | ZIP, postal code |
| `country` | VARCHAR | Country name | nation |
| `salesRepEmployeeNumber` | BIGINT | Employee ID of assigned sales representative | sales rep, account manager |
| `creditLimit` | DOUBLE | Maximum credit extended to customer | credit line, limit |

**Notable state values:** BC, CA, CT, Co. Cork, Isle of Wight, MA, NH, NJ, NSW, NV, NY, Osaka, PA, Pretoria, Queensland, Québec, Tokyo, Victoria

---

### classicmodels.employees
**Meaning:** Employee records including contact, office assignment, and reporting structure.
**Synonyms:** Staff, team members, personnel.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `employeeNumber` | BIGINT | Unique employee identifier | employee ID, staff ID |
| `lastName` | VARCHAR | Employee surname | last name, family name |
| `firstName` | VARCHAR | Employee given name | first name |
| `extension` | VARCHAR | Phone extension | ext, phone extension |
| `email` | VARCHAR | Employee email address | |
| `officeCode` | VARCHAR | Office location code (1–7) | office, location |
| `reportsTo` | BIGINT | Employee number of direct manager | manager, supervisor |
| `jobTitle` | VARCHAR | Job position/role | title, position, role |

**Notable lastName values:** Bondur, Bott, Bow, Castillo, Firrelli, Fixter, Gerard, Hernandez, Jennings, Jones, Kato, King, Marsh, Murphy, Nishi, Patterson, Thompson, Tseng, Vanauf

**Notable extension values:** x101, x102, x103, x2028, x2173, x2248, x2311, x2312, x2759, x3291, x4065, x4102, x4334, x4611, x4871, x5408, x5428, x5800, x6493, x9273

**Notable jobTitle values:** President, Sale Manager (EMEA), Sales Manager (APAC), Sales Manager (NA), Sales Rep, VP Marketing, VP Sales

---

### classicmodels.offices
**Meaning:** Office locations and regional headquarters.
**Synonyms:** Locations, branches, facilities.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `officeCode` | VARCHAR | Unique office identifier (1–7) | office ID, location code |
| `city` | VARCHAR | City where office is located | |
| `phone` | VARCHAR | Office phone number | telephone |
| `addressLine1` | VARCHAR | Primary street address | street, address |
| `addressLine2` | VARCHAR | Secondary address info (suite, floor, etc.) | address line 2 |
| `state` | VARCHAR | State/province code | province, region |
| `country` | VARCHAR | Country name | nation |
| `postalCode` | VARCHAR | Postal/ZIP code | ZIP, postal code |
| `territory` | VARCHAR | Sales territory (NA, EMEA, APAC, Japan) | region, sales region |

**Notable city values:** Boston, London, NYC, Paris, San Francisco, Sydney, Tokyo

**Notable territory values:** APAC, EMEA, Japan, NA

---

### classicmodels.orders
**Meaning:** Customer purchase orders.
**Synonyms:** Transactions, sales orders, purchase orders.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `orderNumber` | BIGINT | Unique order identifier | order ID |
| `orderDate` | DATE | Date order was placed | purchase date, date ordered |
| `requiredDate` | DATE | Date customer requires delivery | due date, delivery date |
| `shippedDate` | DATE | Date order was shipped | ship date, sent date |
| `status` | VARCHAR | Current order status | order status, state |
| `comments` | VARCHAR | Order notes or special instructions | notes, remarks |
| `customerNumber` | BIGINT | Customer who placed order | customer ID |

**Notable status values:** Cancelled, Disputed, In Process, On Hold, Resolved, Shipped

---

### classicmodels.orderdetails
**Meaning:** Line items within orders; the detail/breakdown of each order.
**Synonyms:** Order lines, line items, order items.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `orderNumber` | BIGINT | Order this line item belongs to | order ID |
| `productCode` | VARCHAR | Product identifier | product ID, SKU |
| `quantityOrdered` | BIGINT | Number of units ordered | quantity, units |
| `priceEach` | DOUBLE | Unit price at time of order | unit price, price |
| `orderLineNumber` | BIGINT | Sequence number within order (1, 2, 3, ...) | line number, sequence |

---

### classicmodels.payments
**Meaning:** Customer payment transactions.
**Synonyms:** Transactions, receipts, invoices paid.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `customerNumber` | BIGINT | Customer making payment | customer ID |
| `checkNumber` | VARCHAR | Check or payment reference number | check, reference, payment ID |
| `paymentDate` | DATE | Date payment was received | date paid, transaction date |
| `amount` | DOUBLE | Payment amount in currency units | payment amount, total |

---

### classicmodels.products
**Meaning:** Product catalog with pricing and inventory.
**Synonyms:** Items, SKUs, merchandise.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `productCode` | VARCHAR | Unique product identifier | product ID, SKU |
| `productName` | VARCHAR | Product display name | name, title |
| `productLine` | VARCHAR | Product category/line | category, line, type |
| `productScale` | VARCHAR | Model scale ratio (1:10, 1:24, etc.) | scale |
| `productVendor` | VARCHAR | Manufacturer/supplier name | vendor, manufacturer, maker |
| `productDescription` | VARCHAR | Detailed product description | description, details |
| `quantityInStock` | BIGINT | Current inventory count | stock, inventory, on hand |
| `buyPrice` | DOUBLE | Cost to acquire product | cost, wholesale price |
| `MSRP` | DOUBLE | Manufacturer's suggested retail price | retail price, list price |

**Notable productLine values:** Classic Cars, Motorcycles, Planes, Ships, Trains, Trucks and Buses, Vintage Cars

**Notable productScale values:** 1:10, 1:12, 1:18, 1:24, 1:32, 1:50, 1:700, 1:72

**Notable productVendor values:** Autoart Studio Design, Carousel DieCast Legends, Classic Metal Creations, Exoto Designs, Gearbox Collectibles, Highway 66 Mini Classics, Min Lin Diecast, Motor City Art Classics, Red Start Diecast, Second Gear Diecast, Studio M Art Models, Unimax Art Galleries, Welly Diecast Productions

---

### classicmodels.productlines
**Meaning:** Product line metadata and descriptions.
**Synonyms:** Categories, product categories.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `productLine` | VARCHAR | Product line name (primary key) | category, line, type |
| `textDescription` | VARCHAR | Long-form text description | description |
| `htmlDescription` | VARCHAR | HTML-formatted description | HTML description |
| `image` | BLOB | Product line image binary data | image data |

**Notable productLine values:** Classic Cars, Motorcycles, Planes, Ships, Trains, Trucks and Buses, Vintage Cars

---

## Join Paths

| From | To | Condition |
|------|----|-----------| 
| `customers` | `employees` | `customers.salesRepEmployeeNumber = employees.employeeNumber` |
| `customers` | `orders` | `customers.customerNumber = orders.customerNumber` |
| `customers` | `payments` | `customers.customerNumber = payments.customerNumber` |
| `employees` | `offices` | `employees.officeCode = offices.officeCode` |
| `employees` | `employees` (self) | `employees.reportsTo = employees.employeeNumber` |
| `orders` | `orderdetails` | `orders.orderNumber = orderdetails.orderNumber` |
| `orderdetails` | `products` | `orderdetails.productCode = products.productCode` |
| `products` | `productlines` | `products.productLine = productlines.productLine` |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| customer account | `customers.customerNumber` |
| customer name | `customers.customerName` |
| sales representative | `employees.employeeNumber` WHERE `employees.jobTitle LIKE '%Sales%'` |
| sales manager | `employees.employeeNumber` WHERE `employees.jobTitle LIKE '%Manager%'` |
| office location | `offices.officeCode` |
| sales territory | `offices.territory` |
| product category | `products.productLine` |
| product inventory | `products.quantityInStock` |
| retail price | `products.MSRP` |
| cost price | `products.buyPrice` |
| order total | `SUM(orderdetails.quantityOrdered * orderdetails.priceEach)` |
| order line item | `orderdetails` |
| order status | `orders.status` |
| shipped order | `orders.status = 'Shipped'` |
| cancelled order | `orders.status = 'Cancelled'` |
| payment received | `payments.paymentDate` |
| payment amount | `payments.amount` |
| customer credit limit | `customers.creditLimit` |
| employee manager | `employees.reportsTo` |
| model scale | `products.productScale` |
| manufacturer | `products.productVendor` |