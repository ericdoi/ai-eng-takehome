# GOSales Schema Reference Guide

## Schema Summary
GOSales contains retail sales transactions across products, retailers, and order methods, with supporting product and retailer dimension tables.

---

## Join Paths

**Sales with product details:**
```sql
FROM GOSales.go_daily_sales s
JOIN GOSales.go_products p ON s.Product number = p.Product number
```

**Sales with retailer details:**
```sql
FROM GOSales.go_daily_sales s
JOIN GOSales.go_retailers r ON s.Retailer code = r.Retailer code
```

**Sales with order method:**
```sql
FROM GOSales.go_daily_sales s
JOIN GOSales.go_methods m ON s.Order method code = m.Order method code
```

**Full sales context (product + retailer + method):**
```sql
FROM GOSales.go_daily_sales s
JOIN GOSales.go_products p ON s.Product number = p.Product number
JOIN GOSales.go_retailers r ON s.Retailer code = r.Retailer code
JOIN GOSales.go_methods m ON s.Order method code = m.Order method code
```

**Historical sales (go_1k) with product and retailer:**
```sql
FROM GOSales.go_1k h
JOIN GOSales.go_products p ON h.Product number = p.Product number
JOIN GOSales.go_retailers r ON h.Retailer code = r.Retailer code
```

---

## Table Reference

### `GOSales.go_daily_sales`
Daily transaction-level sales records with pricing.

| Column | Type | Notes |
|--------|------|-------|
| `Retailer code` | BIGINT | Foreign key to `GOSales.go_retailers` |
| `Product number` | BIGINT | Foreign key to `GOSales.go_products` |
| `Order method code` | BIGINT | Foreign key to `GOSales.go_methods` |
| `Date` | DATE | Transaction date |
| `Quantity` | BIGINT | Units sold |
| `Unit price` | DOUBLE | Cost per unit |
| `Unit sale price` | DOUBLE | Selling price per unit |

---

### `GOSales.go_1k`
Historical sales snapshot (1000 records).

| Column | Type | Notes |
|--------|------|-------|
| `Retailer code` | BIGINT | Foreign key to `GOSales.go_retailers` |
| `Product number` | BIGINT | Foreign key to `GOSales.go_products` |
| `Date` | DATE | Transaction date |
| `Quantity` | BIGINT | Units sold |

---

### `GOSales.go_products`
Product catalog with cost and pricing.

| Column | Type | Notes |
|--------|------|-------|
| `Product number` | BIGINT | Primary key |
| `Product line` | VARCHAR | **Enum:** Camping Equipment, Golf Equipment, Mountaineering Equipment, Outdoor Protection, Personal Accessories |
| `Product type` | VARCHAR | Category within product line (e.g., "Cooking Gear") |
| `Product` | VARCHAR | Product name |
| `Product brand` | VARCHAR | Brand name |
| `Product color` | VARCHAR | Color variant |
| `Unit cost` | DOUBLE | Cost to retailer |
| `Unit price` | DOUBLE | Standard retail price |

---

### `GOSales.go_retailers`
Retailer master data.

| Column | Type | Notes |
|--------|------|-------|
| `Retailer code` | BIGINT | Primary key |
| `Retailer name` | VARCHAR | Store name |
| `Type` | VARCHAR | **Enum:** Department Store, Direct Marketing, Equipment Rental Store, Eyewear Store, Golf Shop, Outdoors Shop, Sports Store, Warehouse Store |
| `Country` | VARCHAR | Country of operation |

---

### `GOSales.go_methods`
Order method lookup.

| Column | Type | Notes |
|--------|------|-------|
| `Order method code` | BIGINT | Primary key |
| `Order method type` | VARCHAR | **Enum:** E-mail, Fax, Mail, Other, Sales visit, Special, Telephone, Web |

---

## Synonym Glossary

| Question Term | Schema Reference |
|---------------|------------------|
| revenue | `SUM(GOSales.go_daily_sales.Quantity * GOSales.go_daily_sales.Unit sale price)` |
| profit | `SUM(GOSales.go_daily_sales.Quantity * (GOSales.go_daily_sales.Unit sale price - GOSales.go_daily_sales.Unit price))` |
| margin | `(GOSales.go_daily_sales.Unit sale price - GOSales.go_daily_sales.Unit price) / GOSales.go_daily_sales.Unit sale price` |
| sales volume | `SUM(GOSales.go_daily_sales.Quantity)` |
| order channel | `GOSales.go_methods.Order method type` |
| retailer type | `GOSales.go_retailers.Type` |
| product category | `GOSales.go_products.Product line` |
| cost | `GOSales.go_products.Unit cost` |