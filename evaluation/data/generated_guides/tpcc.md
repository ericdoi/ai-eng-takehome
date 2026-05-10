# TPC-C Schema Reference Guide

## Schema Summary

The `tpcc` schema implements the TPC-C benchmark, a transactional workload simulating a wholesale supplier's order-entry system with warehouses, districts, customers, orders, inventory, and payment history.

---

## Table Reference

### tpcc.C_Warehouse
**Meaning:** Warehouse master data; represents distribution centers.
**Synonyms:** Warehouse, Distribution Center

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `w_id` | BIGINT | Warehouse identifier (primary key) | warehouse_id, warehouse_number |
| `w_name` | VARCHAR | Warehouse name | warehouse_name |
| `w_street_1` | VARCHAR | Warehouse street address line 1 | street_1, address_1 |
| `w_street_2` | VARCHAR | Warehouse street address line 2 | street_2, address_2 |
| `w_city` | VARCHAR | Warehouse city | city |
| `w_state` | VARCHAR | Warehouse state code | state |
| `w_zip` | VARCHAR | Warehouse ZIP code | zip, postal_code |
| `w_tax` | DOUBLE | Warehouse sales tax rate | tax_rate |
| `w_ytd` | DOUBLE | Warehouse year-to-date sales | ytd_sales, year_to_date |

**Notable Values:**
- `w_name`: "mwLkm4"
- `w_state`: "mR"

---

### tpcc.C_District
**Meaning:** District master data; represents sales districts within warehouses.
**Synonyms:** District, Sales District

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `d_id` | BIGINT | District identifier (part of composite key) | district_id, district_number |
| `d_w_id` | BIGINT | Warehouse ID (foreign key to C_Warehouse) | warehouse_id, w_id |
| `d_name` | VARCHAR | District name | district_name |
| `d_street_1` | VARCHAR | District street address line 1 | street_1, address_1 |
| `d_street_2` | VARCHAR | District street address line 2 | street_2, address_2 |
| `d_city` | VARCHAR | District city | city |
| `d_state` | VARCHAR | District state code | state |
| `d_zip` | VARCHAR | District ZIP code | zip, postal_code |
| `d_tax` | DOUBLE | District sales tax rate | tax_rate |
| `d_ytd` | DOUBLE | District year-to-date sales | ytd_sales, year_to_date |
| `d_next_o_id` | BIGINT | Next order ID to be assigned | next_order_id |

**Composite Key:** `(d_id, d_w_id)`

---

### tpcc.C_Customer
**Meaning:** Customer master data; represents customers within districts.
**Synonyms:** Customer, Account

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `c_id` | BIGINT | Customer identifier (part of composite key) | customer_id, customer_number |
| `c_d_id` | BIGINT | District ID (part of composite key) | district_id, d_id |
| `c_w_id` | BIGINT | Warehouse ID (part of composite key) | warehouse_id, w_id |
| `c_first` | VARCHAR | Customer first name | first_name |
| `c_middle` | VARCHAR | Customer middle initial | middle_initial |
| `c_last` | VARCHAR | Customer last name | last_name |
| `c_street_1` | VARCHAR | Customer street address line 1 | street_1, address_1 |
| `c_street_2` | VARCHAR | Customer street address line 2 | street_2, address_2 |
| `c_city` | VARCHAR | Customer city | city |
| `c_state` | VARCHAR | Customer state code | state |
| `c_zip` | VARCHAR | Customer ZIP code | zip, postal_code |
| `c_phone` | VARCHAR | Customer phone number | phone |
| `c_since` | TIMESTAMP | Customer account creation date | account_date, since_date |
| `c_credit` | VARCHAR | Customer credit status | credit_status |
| `c_credit_lim` | DOUBLE | Customer credit limit | credit_limit |
| `c_discount` | DOUBLE | Customer discount percentage | discount_rate |
| `c_balance` | DOUBLE | Customer account balance | balance, current_balance |
| `c_ytd_payment` | DOUBLE | Customer year-to-date payments | ytd_payment, ytd_paid |
| `c_payment_cnt` | BIGINT | Customer payment count | payment_count, num_payments |
| `c_delivery_cnt` | BIGINT | Customer delivery count | delivery_count, num_deliveries |
| `c_data1` | VARCHAR | Customer data field 1 | data_1, notes_1 |
| `c_data2` | VARCHAR | Customer data field 2 | data_2, notes_2 |

**Composite Key:** `(c_id, c_d_id, c_w_id)`

**Notable Values:**
- `c_middle`: "OE"
- `c_credit`: "BC", "GC"

---

### tpcc.C_Order
**Meaning:** Order master data; represents customer orders.
**Synonyms:** Order, Sales Order

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `o_id` | BIGINT | Order identifier (part of composite key) | order_id, order_number |
| `o_d_id` | BIGINT | District ID (part of composite key) | district_id, d_id |
| `o_w_id` | BIGINT | Warehouse ID (part of composite key) | warehouse_id, w_id |
| `o_c_id` | BIGINT | Customer ID (foreign key to C_Customer) | customer_id, c_id |
| `o_entry_d` | TIMESTAMP | Order entry date/time | entry_date, order_date |
| `o_carrier_id` | BIGINT | Carrier ID for delivery | carrier_id, carrier_number |
| `o_ol_cnt` | BIGINT | Order line count | line_count, num_lines |
| `o_all_local` | BIGINT | Flag: all items from local warehouse (0/1) | all_local, local_flag |

**Composite Key:** `(o_id, o_d_id, o_w_id)`

---

### tpcc.C_Order_Line
**Meaning:** Order line items; represents individual items within orders.
**Synonyms:** Order Line, Line Item, Order Detail

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ol_o_id` | BIGINT | Order ID (part of composite key) | order_id, o_id |
| `ol_d_id` | BIGINT | District ID (part of composite key) | district_id, d_id |
| `ol_w_id` | BIGINT | Warehouse ID (part of composite key) | warehouse_id, w_id |
| `ol_number` | BIGINT | Line item number within order (part of composite key) | line_number, item_number |
| `ol_i_id` | BIGINT | Item ID (foreign key to C_Item) | item_id, i_id |
| `ol_supply_w_id` | BIGINT | Supplying warehouse ID | supply_warehouse_id, supplier_warehouse |
| `ol_delivery_d` | TIMESTAMP | Delivery date/time | delivery_date, delivered_date |
| `ol_quantity` | BIGINT | Quantity ordered | quantity, qty |
| `ol_amount` | DOUBLE | Line item total amount | amount, line_total |
| `ol_dist_info` | VARCHAR | Distribution information | dist_info, distribution_data |

**Composite Key:** `(ol_o_id, ol_d_id, ol_w_id, ol_number)`

---

### tpcc.C_New_Order
**Meaning:** New order tracking; represents orders not yet delivered.
**Synonyms:** New Order, Pending Order

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `no_o_id` | BIGINT | Order ID (part of composite key) | order_id, o_id |
| `no_d_id` | BIGINT | District ID (part of composite key) | district_id, d_id |
| `no_w_id` | BIGINT | Warehouse ID (part of composite key) | warehouse_id, w_id |

**Composite Key:** `(no_o_id, no_d_id, no_w_id)`

---

### tpcc.C_Item
**Meaning:** Item master data; represents products in inventory.
**Synonyms:** Item, Product, SKU

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `i_id` | BIGINT | Item identifier (primary key) | item_id, item_number |
| `i_im_id` | BIGINT | Image ID | image_id, im_id |
| `i_name` | VARCHAR | Item name | item_name, product_name |
| `i_price` | DOUBLE | Item unit price | price, unit_price |
| `i_data` | VARCHAR | Item data field | data, item_data |

---

### tpcc.C_Stock
**Meaning:** Stock/inventory data; represents item quantities at warehouses.
**Synonyms:** Stock, Inventory, Stock Level

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `s_i_id` | BIGINT | Item ID (part of composite key) | item_id, i_id |
| `s_w_id` | BIGINT | Warehouse ID (part of composite key) | warehouse_id, w_id |
| `s_quantity` | BIGINT | Current stock quantity | quantity, qty, on_hand |
| `s_dist_01` | VARCHAR | Distribution info for district 1 | dist_01, distribution_1 |
| `s_dist_02` | VARCHAR | Distribution info for district 2 | dist_02, distribution_2 |
| `s_dist_03` | VARCHAR | Distribution info for district 3 | dist_03, distribution_3 |
| `s_dist_04` | VARCHAR | Distribution info for district 4 | dist_04, distribution_4 |
| `s_dist_05` | VARCHAR | Distribution info for district 5 | dist_05, distribution_5 |
| `s_dist_06` | VARCHAR | Distribution info for district 6 | dist_06, distribution_6 |
| `s_dist_07` | VARCHAR | Distribution info for district 7 | dist_07, distribution_7 |
| `s_dist_08` | VARCHAR | Distribution info for district 8 | dist_08, distribution_8 |
| `s_dist_09` | VARCHAR | Distribution info for district 9 | dist_09, distribution_9 |
| `s_dist_10` | VARCHAR | Distribution info for district 10 | dist_10, distribution_10 |
| `s_ytd` | BIGINT | Stock year-to-date sales | ytd_sales, year_to_date |
| `s_order_cnt` | BIGINT | Stock order count | order_count, num_orders |
| `s_remote_cnt` | BIGINT | Stock remote order count | remote_count, num_remote |
| `s_data` | VARCHAR | Stock data field | data, stock_data |

**Composite Key:** `(s_i_id, s_w_id)`

---

### tpcc.C_History
**Meaning:** Payment history; represents customer payment transactions.
**Synonyms:** History, Payment History, Transaction

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `h_c_id` | BIGINT | Customer ID (part of composite key) | customer_id, c_id |
| `h_c_d_id` | BIGINT | Customer district ID (part of composite key) | district_id, d_id |
| `h_c_w_id` | BIGINT | Customer warehouse ID (part of composite key) | warehouse_id, w_id |
| `h_d_id` | BIGINT | District ID where payment occurred | district_id, d_id |
| `h_w_id` | BIGINT | Warehouse ID where payment occurred | warehouse_id, w_id |
| `h_date` | TIMESTAMP | Payment date/time | payment_date, transaction_date |
| `h_amount` | DOUBLE | Payment amount | amount, payment_amount |
| `h_data` | VARCHAR | Payment data field | data, payment_data |

---

## Join Paths

### Customer to District
```sql
C_Customer.c_d_id = C_District.d_id 
AND C_Customer.c_w_id = C_District.d_w_id
```

### Customer to Warehouse
```sql
C_Customer.c_w_id = C_Warehouse.w_id
```

### Order to Customer
```sql
C_Order.o_c_id = C_Customer.c_id 
AND C_Order.o_d_id = C_Customer.c_d_id 
AND C_Order.o_w_id = C_Customer.c_w_id
```

### Order to District
```sql
C_Order.o_d_id = C_District.d_id 
AND C_Order.o_w_id = C_District.d_w_id
```

### Order to Warehouse
```sql
C_Order.o_w_id = C_Warehouse.w_id
```

### Order_Line to Order
```sql
C_Order_Line.ol_o_id = C_Order.o_id 
AND C_Order_Line.ol_d_id = C_Order.o_d_id 
AND C_Order_Line.ol_w_id = C_Order.o_w_id
```

### Order_Line to Item
```sql
C_Order_Line.ol_i_id = C_Item.i_id
```

### Order_Line to Stock (supply warehouse)
```sql
C_Order_Line.ol_i_id = C_Stock.s_i_id 
AND C_Order_Line.ol_supply_w_id = C_Stock.s_w_id
```

### New_Order to Order
```sql
C_New_Order.no_o_id = C_Order.o_id 
AND C_New_Order.no_d_id = C_Order.o_d_id 
AND C_New_Order.no_w_id = C_Order.o_w_id
```

### Stock to Item
```sql
C_Stock.s_i_id = C_Item.i_id
```

### Stock to Warehouse
```sql
C_Stock.s_w_id = C_Warehouse.w_id
```

### History to Customer
```sql
C_History.h_c_id = C_Customer.c_id 
AND C_History.h_c_d_id = C_Customer.c_d_id 
AND C_History.h_c_w_id = C_Customer.c_w_id
```

### History to District (payment district)
```sql
C_History.h_d_id = C_District.d_id 
AND C_History.h_w_id = C_District.d_w_id
```

### History to Warehouse (payment warehouse)
```sql
C_History.h_w_id = C_Warehouse.w_id
```

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| warehouse | `tpcc.C_Warehouse` |
| district | `tpcc.C_District` |
| customer | `tpcc.C_Customer` |
| order | `tpcc.C_Order` |
| line item | `tpcc.C_Order_Line` |
| new order | `tpcc.C_New_Order` |
| item / product | `tpcc.C_Item` |
| stock /