# TPC-C Schema Reference Guide

## Schema Summary
This schema implements the TPC-C benchmark: a transactional workload modeling a wholesale supplier with warehouses, districts, customers, orders, inventory, and payment history.

---

## Join Paths

**Customer to Order:**
```sql
FROM tpcc.C_Customer c
JOIN tpcc.C_Order o ON c.c_id = o.o_c_id AND c.c_d_id = o.o_d_id AND c.c_w_id = o.o_w_id
```

**Order to Order Line:**
```sql
FROM tpcc.C_Order o
JOIN tpcc.C_Order_Line ol ON o.o_id = ol.ol_o_id AND o.o_d_id = ol.ol_d_id AND o.o_w_id = ol.ol_w_id
```

**Order Line to Item:**
```sql
FROM tpcc.C_Order_Line ol
JOIN tpcc.C_Item i ON ol.ol_i_id = i.i_id
```

**Order Line to Stock:**
```sql
FROM tpcc.C_Order_Line ol
JOIN tpcc.C_Stock s ON ol.ol_i_id = s.s_i_id AND ol.ol_supply_w_id = s.s_w_id
```

**Customer to History:**
```sql
FROM tpcc.C_Customer c
JOIN tpcc.C_History h ON c.c_id = h.h_c_id AND c.c_d_id = h.h_c_d_id AND c.c_w_id = h.h_c_w_id
```

**District to Warehouse:**
```sql
FROM tpcc.C_District d
JOIN tpcc.C_Warehouse w ON d.d_w_id = w.w_id
```

**New Order to Order:**
```sql
FROM tpcc.C_New_Order no
JOIN tpcc.C_Order o ON no.no_o_id = o.o_id AND no.no_d_id = o.o_d_id AND no.no_w_id = o.o_w_id
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| customer balance | `tpcc.C_Customer.c_balance` |
| customer credit limit | `tpcc.C_Customer.c_credit_lim` |
| customer discount | `tpcc.C_Customer.c_discount` |
| year-to-date payment | `tpcc.C_Customer.c_ytd_payment` |
| payment count | `tpcc.C_Customer.c_payment_cnt` |
| delivery count | `tpcc.C_Customer.c_delivery_cnt` |
| order entry date | `tpcc.C_Order.o_entry_d` |
| order line count | `tpcc.C_Order.o_ol_cnt` |
| order line quantity | `tpcc.C_Order_Line.ol_quantity` |
| order line amount | `tpcc.C_Order_Line.ol_amount` |
| delivery date | `tpcc.C_Order_Line.ol_delivery_d` |
| item price | `tpcc.C_Item.i_price` |
| stock quantity | `tpcc.C_Stock.s_quantity` |
| stock year-to-date | `tpcc.C_Stock.s_ytd` |
| stock order count | `tpcc.C_Stock.s_order_cnt` |
| stock remote count | `tpcc.C_Stock.s_remote_cnt` |
| district tax | `tpcc.C_District.d_tax` |
| district year-to-date | `tpcc.C_District.d_ytd` |
| warehouse tax | `tpcc.C_Warehouse.w_tax` |
| warehouse year-to-date | `tpcc.C_Warehouse.w_ytd` |

---

## Table Reference

### `tpcc.C_Customer`
**Meaning:** Customer master records with credit and payment tracking.

| Column | Semantics |
|--------|-----------|
| `c_id`, `c_d_id`, `c_w_id` | Composite key: customer ID, district ID, warehouse ID |
| `c_credit` | Enum: `'GC'` (good credit), `'BC'` (bad credit) |
| `c_credit_lim` | Credit limit (DOUBLE) |
| `c_discount` | Discount percentage (DOUBLE, 0–1 range) |
| `c_balance` | Current account balance (DOUBLE, can be negative) |
| `c_ytd_payment` | Year-to-date payment total (DOUBLE) |
| `c_payment_cnt` | Count of payments made (BIGINT) |
| `c_delivery_cnt` | Count of deliveries received (BIGINT) |
| `c_since` | Account creation timestamp |

---

### `tpcc.C_District`
**Meaning:** District master records within warehouses; tracks next order ID and tax/revenue.

| Column | Semantics |
|--------|-----------|
| `d_id`, `d_w_id` | Composite key: district ID, warehouse ID |
| `d_tax` | District tax rate (DOUBLE) |
| `d_ytd` | District year-to-date revenue (DOUBLE) |
| `d_next_o_id` | Next order ID to assign (BIGINT) |

---

### `tpcc.C_Warehouse`
**Meaning:** Warehouse master records; top-level organizational unit.

| Column | Semantics |
|--------|-----------|
| `w_id` | Primary key: warehouse ID |
| `w_tax` | Warehouse tax rate (DOUBLE) |
| `w_ytd` | Warehouse year-to-date revenue (DOUBLE) |

---

### `tpcc.C_Order`
**Meaning:** Customer orders with carrier and line item count.

| Column | Semantics |
|--------|-----------|
| `o_id`, `o_d_id`, `o_w_id` | Composite key: order ID, district ID, warehouse ID |
| `o_c_id` | Customer ID (foreign key to `tpcc.C_Customer`) |
| `o_entry_d` | Order entry timestamp |
| `o_carrier_id` | Assigned carrier ID (BIGINT, nullable for new orders) |
| `o_ol_cnt` | Number of line items in order (BIGINT) |
| `o_all_local` | Flag: 1 if all items from same warehouse, 0 otherwise (BIGINT) |

---

### `tpcc.C_Order_Line`
**Meaning:** Individual line items within orders; links to items and stock.

| Column | Semantics |
|--------|-----------|
| `ol_o_id`, `ol_d_id`, `ol_w_id` | Composite key: order ID, district ID, warehouse ID |
| `ol_number` | Line item sequence number (BIGINT) |
| `ol_i_id` | Item ID (foreign key to `tpcc.C_Item`) |
| `ol_supply_w_id` | Warehouse supplying this item (foreign key to `tpcc.C_Stock`) |
| `ol_delivery_d` | Delivery timestamp (NULL for undelivered items) |
| `ol_quantity` | Quantity ordered (BIGINT) |
| `ol_amount` | Line item total amount (DOUBLE) |

---

### `tpcc.C_Item`
**Meaning:** Item master catalog with pricing.

| Column | Semantics |
|--------|-----------|
| `i_id` | Primary key: item ID |
| `i_im_id` | Image ID (BIGINT) |
| `i_price` | Unit price (DOUBLE) |

---

### `tpcc.C_Stock`
**Meaning:** Inventory levels by item and warehouse; tracks order and remote fulfillment counts.

| Column | Semantics |
|--------|-----------|
| `s_i_id`, `s_w_id` | Composite key: item ID, warehouse ID |
| `s_quantity` | Current stock quantity (BIGINT) |
| `s_dist_01` through `s_dist_10` | Distribution center info strings (VARCHAR) for 10 districts |
| `s_ytd` | Year-to-date orders fulfilled (BIGINT) |
| `s_order_cnt` | Count of orders for this item (BIGINT) |
| `s_remote_cnt` | Count of remote orders (BIGINT) |

---

### `tpcc.C_New_Order`
**Meaning:** Pending orders not yet assigned to a carrier; subset of `tpcc.C_Order`.

| Column | Semantics |
|--------|-----------|
| `no_o_id`, `no_d_id`, `no_w_id` | Composite key: order ID, district ID, warehouse ID (foreign key to `tpcc.C_Order`) |

---

### `tpcc.C_History`
**Meaning:** Payment and order history audit trail for customers.

| Column | Semantics |
|--------|-----------|
| `h_c_id`, `h_c_d_id`, `h_c_w_id` | Customer reference (foreign key to `tpcc.C_Customer`) |
| `h_d_id`, `h_w_id` | District and warehouse where transaction occurred |
| `h_date` | Transaction timestamp |
| `h_amount` | Transaction amount (DOUBLE) |