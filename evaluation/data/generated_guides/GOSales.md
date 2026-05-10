# GOSales Schema Reference Guide

## Schema Summary
The GOSales schema contains retail sales transaction data for outdoor and sporting goods, including daily sales records, product catalogs, retailer information, and order methods.

---

## Table Reference

### GOSales.go_1k
**Meaning:** Historical sales transactions (1,000 records); simplified sales fact table.
**Synonyms:** Sales history, transaction log, sales records.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Retailer code` | BIGINT | Unique identifier for the retailer | Retailer ID, store code |
| `Product number` | BIGINT | Unique identifier for the product | Product ID, SKU |
| `Date` | DATE | Transaction date | Sale date, order date |
| `Quantity` | BIGINT | Units sold in transaction | Units, volume, amount |

---

### GOSales.go_daily_sales
**Meaning:** Detailed daily sales transactions with pricing and order method; primary transactional fact table.
**Synonyms:** Sales transactions, daily orders, order details.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Retailer code` | BIGINT | Unique identifier for the retailer | Retailer ID, store code |
| `Product number` | BIGINT | Unique identifier for the product | Product ID, SKU |
| `Order method code` | BIGINT | Code identifying how order was placed | Method ID, channel code |
| `Date` | DATE | Transaction date | Sale date, order date |
| `Quantity` | BIGINT | Units sold in transaction | Units, volume, amount |
| `Unit price` | DOUBLE | Cost per unit (wholesale/cost price) | Cost, unit cost |
| `Unit sale price` | DOUBLE | Selling price per unit (retail price) | Sale price, retail price |

---

### GOSales.go_methods
**Meaning:** Lookup table for order methods/channels.
**Synonyms:** Order channels, sales channels, methods.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Order method code` | BIGINT | Unique identifier for order method | Method ID, channel code |
| `Order method type` | VARCHAR | Name of order method | Channel type, method name |

**Enumerated Values (exact):**
- `Fax`
- `Telephone`
- `Mail`
- `E-mail`
- `Web`
- `Sales visit`
- `Special`
- `Other`

---

### GOSales.go_products
**Meaning:** Product master data with classification, branding, and pricing.
**Synonyms:** Product catalog, product master, inventory.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Product number` | BIGINT | Unique identifier for the product | Product ID, SKU |
| `Product line` | VARCHAR | High-level product category | Category, line |
| `Product type` | VARCHAR | Mid-level product classification | Type, subcategory |
| `Product` | VARCHAR | Product name/description | Product name, description |
| `Product brand` | VARCHAR | Brand name | Brand, manufacturer |
| `Product color` | VARCHAR | Color variant | Color, shade |
| `Unit cost` | DOUBLE | Cost to acquire/produce per unit | Cost, COGS |
| `Unit price` | DOUBLE | Standard wholesale/list price per unit | List price, wholesale price |

**Enumerated Values for `Product line` (exact):**
- `Camping Equipment`
- `Golf Equipment`
- `Mountaineering Equipment`
- `Outdoor Protection`
- `Personal Accessories`

---

### GOSales.go_retailers
**Meaning:** Retailer master data with location and business type.
**Synonyms:** Retailers, stores, locations, accounts.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `Retailer code` | BIGINT | Unique identifier for the retailer | Retailer ID, store code, account |
| `Retailer name` | VARCHAR | Name of retailer/store | Store name, account name |
| `Type` | VARCHAR | Business type/format of retailer | Retailer type, store type, channel |
| `Country` | VARCHAR | Country where retailer is located | Location, region |

**Enumerated Values for `Type` (exact):**
- `Department Store`
- `Direct Marketing`
- `Equipment Rental Store`
- `Eyewear Store`
- `Golf Shop`
- `Outdoors Shop`
- `Sports Store`
- `Warehouse Store`

---

## Join Paths

| From | To | Condition |
|------|----|-----------| 
| `go_daily_sales` | `go_retailers` | `go_daily_sales.Retailer code = go_retailers.Retailer code` |
| `go_daily_sales` | `go_products` | `go_daily_sales.Product number = go_products.Product number` |
| `go_daily_sales` | `go_methods` | `go_daily_sales.Order method code = go_methods.Order method code` |
| `go_1k` | `go_retailers` | `go_1k.Retailer code = go_retailers.Retailer code` |
| `go_1k` | `go_products` | `go_1k.Product number = go_products.Product number` |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| Sales by retailer | `GROUP BY go_retailers.Retailer name` |
| Sales by product | `GROUP BY go_products.Product` |
| Sales by category | `GROUP BY go_products.Product line` |
| Sales by channel/method | `GROUP BY go_methods.Order method type` |
| Sales by country | `GROUP BY go_retailers.Country` |
| Total revenue | `SUM(go_daily_sales.Quantity * go_daily_sales.Unit sale price)` |
| Total cost | `SUM(go_daily_sales.Quantity * go_daily_sales.Unit price)` |
| Profit/margin | `SUM(go_daily_sales.Quantity * (go_daily_sales.Unit sale price - go_daily_sales.Unit price))` |
| Units sold | `SUM(go_daily_sales.Quantity)` or `SUM(go_1k.Quantity)` |
| Web orders | `WHERE go_methods.Order method type = 'Web'` |
| Email orders | `WHERE go_methods.Order method type = 'E-mail'` |
| Direct sales | `WHERE go_retailers.Type = 'Direct Marketing'` |
| Golf products | `WHERE go_products.Product line = 'Golf Equipment'` |
| Camping products | `WHERE go_products.Product line = 'Camping Equipment'` |