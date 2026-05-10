# PUB Schema Reference Guide

## Schema Summary
This schema models a book publishing business, tracking authors, titles, publishers, employees, sales transactions, and royalty schedules.

---

## Join Paths

**Authors to Titles (via titleauthor)**
```sql
FROM pubs.authors a
JOIN pubs.titleauthor ta ON a.au_id = ta.au_id
JOIN pubs.titles t ON ta.title_id = t.title_id
```

**Titles to Sales**
```sql
FROM pubs.titles t
JOIN pubs.sales s ON t.title_id = s.title_id
JOIN pubs.stores st ON s.stor_id = st.stor_id
```

**Titles to Publishers**
```sql
FROM pubs.titles t
JOIN pubs.publishers p ON t.pub_id = p.pub_id
```

**Titles to Royalty Schedule**
```sql
FROM pubs.titles t
JOIN pubs.roysched rs ON t.title_id = rs.title_id
```

**Employees to Publishers**
```sql
FROM pubs.employee e
JOIN pubs.publishers p ON e.pub_id = p.pub_id
```

**Employees to Jobs**
```sql
FROM pubs.employee e
JOIN pubs.jobs j ON e.job_id = j.job_id
```

---

## Table Reference

### `pubs.authors`
Author records. Synonyms: *writer, contributor*

| Column | Notes |
|--------|-------|
| `au_id` | Primary key; format "###-##-####" |
| `contract` | Boolean; whether author has active contract |
| `state` | US state codes: CA, IN, KS, MD, MI, OR, TN, UT |
| `city` | Author location |

### `pubs.titles`
Book catalog. Synonyms: *book, publication*

| Column | Notes |
|--------|-------|
| `title_id` | Primary key; format "XX####" |
| `type` | Enumerated: `business`, `mod_cook`, `popular_comp`, `psychology`, `trad_cook`, `UNDECIDED` |
| `pub_id` | Foreign key to `pubs.publishers` |
| `price` | Retail price (DOUBLE) |
| `advance` | Advance payment to author (DOUBLE) |
| `royalty` | Royalty percentage (BIGINT, 0–100) |
| `ytd_sales` | Year-to-date unit sales |
| `pubdate` | Publication date (TIMESTAMP) |

### `pubs.titleauthor`
Author–title associations. Synonyms: *authorship, contribution*

| Column | Notes |
|--------|-------|
| `au_id` | Foreign key to `pubs.authors` |
| `title_id` | Foreign key to `pubs.titles` |
| `au_ord` | Boolean; author order/sequence indicator |
| `royaltyper` | Author's royalty percentage share (0–100) |

### `pubs.publishers`
Publisher organizations. Synonyms: *publishing house, imprint*

| Column | Notes |
|--------|-------|
| `pub_id` | Primary key; format "####" |
| `pub_name` | Publisher name |
| `state` | US state code or null for international |
| `country` | Enumerated: `USA`, `France`, `Germany` |

### `pubs.pub_info`
Publisher metadata and branding.

| Column | Notes |
|--------|-------|
| `pub_id` | Foreign key to `pubs.publishers` |
| `logo` | Binary image data (BLOB) |
| `pr_info` | Public relations/marketing text |

### `pubs.sales`
Sales transactions. Synonyms: *order, transaction, purchase*

| Column | Notes |
|--------|-------|
| `stor_id` | Foreign key to `pubs.stores` |
| `title_id` | Foreign key to `pubs.titles` |
| `ord_num` | Order number (alphanumeric) |
| `ord_date` | Order date (TIMESTAMP) |
| `qty` | Quantity sold (BIGINT) |
| `payterms` | Enumerated: `Net 30`, `Net 60`, `ON invoice` |

### `pubs.stores`
Retail bookstores. Synonyms: *retailer, bookshop, vendor*

| Column | Notes |
|--------|-------|
| `stor_id` | Primary key; format "####" |
| `stor_name` | Store name |
| `state` | US state code: CA, OR, WA |
| `city` | Store location |

### `pubs.roysched`
Tiered royalty schedules by sales volume. Synonyms: *royalty tier, royalty bracket*

| Column | Notes |
|--------|-------|
| `title_id` | Foreign key to `pubs.titles` |
| `lorange` | Lower bound of sales volume (BIGINT) |
| `hirange` | Upper bound of sales volume (BIGINT) |
| `royalty` | Royalty percentage for this tier (BIGINT) |

### `pubs.employee`
Publisher staff. Synonyms: *staff, worker, personnel*

| Column | Notes |
|--------|-------|
| `emp_id` | Primary key; format "X-######X" |
| `job_id` | Foreign key to `pubs.jobs` |
| `job_lvl` | Job level/seniority (BIGINT); higher = more senior |
| `pub_id` | Foreign key to `pubs.publishers` |
| `hire_date` | Employment start date (TIMESTAMP) |
| `minit` | Middle initial (single character, may be empty) |

### `pubs.jobs`
Job classifications and levels. Synonyms: *position, role, title*

| Column | Notes |
|--------|-------|
| `job_id` | Primary key (BIGINT) |
| `job_desc` | Enumerated: `Chief Executive Officer`, `Publisher`, `Editor`, `Sales Representative`, `Designer`, `Marketing Manager`, `New Hire - Job not specified`, etc. |
| `min_lvl` | Minimum job level for this role (BIGINT) |
| `max_lvl` | Maximum job level for this role (BIGINT) |

### `pubs.discounts`
Discount policies by store and volume. Synonyms: *promotion, discount tier*

| Column | Notes |
|--------|-------|
| `discounttype` | Enumerated: `Customer Discount`, `Initial Customer`, `Volume Discount` |
| `stor_id` | Foreign key to `pubs.stores` (may be NULL for global discounts) |
| `lowqty` | Minimum quantity threshold (BIGINT, may be NULL) |
| `highqty` | Maximum quantity threshold (BIGINT, may be NULL) |
| `discount` | Discount percentage (DOUBLE) |

---

## Synonym Glossary

| Question Term | Schema Reference |
|---------------|------------------|
| author contract status | `pubs.authors.contract` |
| book type/category | `pubs.titles.type` |
| royalty tier | `pubs.roysched` (join on `title_id`, filter by `lorange`/`hirange`) |
| sales volume | `pubs.sales.qty` |
| payment terms | `pubs.sales.payterms` |
| job seniority | `pubs.employee.job_lvl` |
| store location | `pubs.stores.city`, `pubs.stores.state` |
| publisher location | `pubs.publishers.city`, `pubs.publishers.country` |
| author location | `pubs.authors.city`, `pubs.authors.state` |
| publication date | `pubs.titles.pubdate` |
| advance payment | `pubs.titles.advance` |
| year-to-date sales | `pubs.titles.ytd_sales` |
| author royalty share | `pubs.titleauthor.royaltyper` |