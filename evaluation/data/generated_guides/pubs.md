# SQL Reference Guide: pubs Schema

## Schema Summary
The `pubs` schema contains a publishing business database tracking authors, titles, publishers, employees, sales transactions, and royalty schedules.

---

## Table Reference

### pubs.authors
**Meaning**: Author records; also called "writers" or "contributors"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `au_id` | VARCHAR | Unique author identifier | author ID, author code |
| `au_lname` | VARCHAR | Author last name | surname, family name |
| `au_fname` | VARCHAR | Author first name | given name |
| `phone` | VARCHAR | Author phone number | contact phone |
| `address` | VARCHAR | Street address | street, location |
| `city` | VARCHAR | City name | **Values**: Ann Arbor, Berkeley, Corvallis, Covelo, Gary, Lawrence, Menlo Park, Nashville, Oakland, Palo Alto, Rockville, Salt Lake City, San Francisco, San Jose, Vacaville, Walnut Creek |
| `state` | VARCHAR | US state code | **Values**: CA, IN, KS, MD, MI, OR, TN, UT |
| `zip` | VARCHAR | Postal code | postal code, zip code |
| `contract` | BOOLEAN | Whether author has active contract | contracted, has_contract |

---

### pubs.publishers
**Meaning**: Publisher company records; also called "publishing houses" or "imprints"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `pub_id` | VARCHAR | Unique publisher identifier | publisher ID, publisher code |
| `pub_name` | VARCHAR | Publisher company name | publisher, company name |
| `city` | VARCHAR | Publisher headquarters city | headquarters city |
| `state` | VARCHAR | US state code | **Values**: CA, DC, IL, MA, NY, TX |
| `country` | VARCHAR | Country name | **Values**: France, Germany, USA |

---

### pubs.titles
**Meaning**: Book/title records; also called "books" or "publications"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `title_id` | VARCHAR | Unique title identifier | book ID, ISBN-like code |
| `title` | VARCHAR | Book title name | book title, name |
| `type` | VARCHAR | Genre/category | genre, category, **Values**: UNDECIDED, business, mod_cook, popular_comp, psychology, trad_cook |
| `pub_id` | VARCHAR | Publisher ID (FK to publishers) | publisher ID |
| `price` | DOUBLE | Retail price in dollars | retail price, cost |
| `advance` | DOUBLE | Advance payment to author | advance payment |
| `royalty` | BIGINT | Royalty percentage | royalty percent, royalty rate |
| `ytd_sales` | BIGINT | Year-to-date unit sales | sales, units sold, YTD sales |
| `notes` | VARCHAR | Description/synopsis | description, synopsis |
| `pubdate` | TIMESTAMP | Publication date | published date, release date |

---

### pubs.titleauthor
**Meaning**: Junction table linking authors to titles; also called "author-title relationships" or "book authorship"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `au_id` | VARCHAR | Author ID (FK to authors) | author ID |
| `title_id` | VARCHAR | Title ID (FK to titles) | title ID, book ID |
| `au_ord` | BOOLEAN | Whether author is primary/first author | is_primary, is_first, author_order |
| `royaltyper` | BIGINT | Author's royalty percentage share | royalty share, royalty percent |

---

### pubs.publishers (see above)

### pubs.pub_info
**Meaning**: Publisher supplementary information; also called "publisher details" or "publisher metadata"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `pub_id` | VARCHAR | Publisher ID (FK to publishers) | publisher ID |
| `logo` | BLOB | Publisher logo image binary | logo image, image |
| `pr_info` | VARCHAR | Public relations/marketing description | description, PR text, marketing info |

---

### pubs.roysched
**Meaning**: Royalty schedule tiers; also called "royalty brackets" or "royalty rates by volume"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `title_id` | VARCHAR | Title ID (FK to titles) | title ID, book ID |
| `lorange` | BIGINT | Lower bound of sales quantity range | low range, minimum quantity |
| `hirange` | BIGINT | Upper bound of sales quantity range | high range, maximum quantity |
| `royalty` | BIGINT | Royalty percentage for this range | royalty rate, royalty percent |

---

### pubs.sales
**Meaning**: Sales transaction records; also called "orders" or "purchase orders"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `stor_id` | VARCHAR | Store ID (FK to stores) | store ID |
| `ord_num` | VARCHAR | Order/transaction number | order number, order ID |
| `ord_date` | TIMESTAMP | Order date | transaction date, purchase date |
| `qty` | BIGINT | Quantity ordered | quantity, units |
| `payterms` | VARCHAR | Payment terms | payment terms, **Values**: Net 30, Net 60, ON invoice |
| `title_id` | VARCHAR | Title ID (FK to titles) | title ID, book ID |

---

### pubs.stores
**Meaning**: Retail store records; also called "bookstores" or "retailers"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `stor_id` | VARCHAR | Unique store identifier | store ID, store code |
| `stor_name` | VARCHAR | Store name | store, retailer name |
| `stor_address` | VARCHAR | Street address | address, street |
| `city` | VARCHAR | City name | **Values**: Fremont, Los Gatos, Portland, Remulade, Seattle, Tustin |
| `state` | VARCHAR | US state code | **Values**: CA, OR, WA |
| `zip` | VARCHAR | Postal code | postal code, zip code |

---

### pubs.employee
**Meaning**: Employee records; also called "staff" or "personnel"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `emp_id` | VARCHAR | Unique employee identifier | employee ID, emp code |
| `fname` | VARCHAR | Employee first name | first name, given name |
| `minit` | VARCHAR | Middle initial | middle initial |
| `lname` | VARCHAR | Employee last name | last name, surname |
| `job_id` | BIGINT | Job classification ID (FK to jobs) | job ID, position ID |
| `job_lvl` | BIGINT | Job level/seniority (0–250 scale) | job level, seniority level, level |
| `pub_id` | VARCHAR | Publisher employer ID (FK to publishers) | publisher ID, employer |
| `hire_date` | TIMESTAMP | Employment start date | start date, hired date |

---

### pubs.jobs
**Meaning**: Job classification/title definitions; also called "positions" or "roles"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `job_id` | BIGINT | Unique job classification ID | job ID, position ID |
| `job_desc` | VARCHAR | Job title/description | job title, position, **Values**: Acquisitions Manager, Business Operations Manager, Chief Executive Officer, Chief Financial Officier, Designer, Editor, Managing Editor, Marketing Manager, New Hire - Job not specified, Operations Manager, Productions Manager, Public Relations Manager, Publisher, Sales Representative |
| `min_lvl` | BIGINT | Minimum job level for this role | minimum level |
| `max_lvl` | BIGINT | Maximum job level for this role | maximum level |

---

### pubs.discounts
**Meaning**: Discount rules/tiers; also called "discount schedules" or "pricing tiers"

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `discounttype` | VARCHAR | Discount category | discount type, **Values**: Customer Discount, Initial Customer, Volume Discount |
| `stor_id` | VARCHAR | Store ID (FK to stores, nullable) | store ID |
| `lowqty` | BIGINT | Minimum quantity for discount (nullable) | low quantity, minimum qty |
| `highqty` | BIGINT | Maximum quantity for discount (nullable) | high quantity, maximum qty |
| `discount` | DOUBLE | Discount percentage | discount percent, discount rate |

---

## Join Paths

### Authors to Titles
```sql
authors a
INNER JOIN titleauthor ta ON a.au_id = ta.au_id
INNER JOIN titles t ON ta.title_id = t.title_id
```

### Titles to Publishers
```sql
titles t
INNER JOIN publishers p ON t.pub_id = p.pub_id
```

### Titles to Sales
```sql
titles t
INNER JOIN sales s ON t.title_id = s.title_id
```

### Sales to Stores
```sql
sales s
INNER JOIN stores st ON s.stor_id = st.stor_id
```

### Titles to Royalty Schedule
```sql
titles t
INNER JOIN roysched rs ON t.title_id = rs.title_id
```

### Employees to Jobs
```sql
employee e
INNER JOIN jobs j ON e.job_id = j.job_id
```

### Employees to Publishers
```sql
employee e
INNER JOIN publishers p ON e.pub_id = p.pub_id
```

### Publishers to Publisher Info
```sql
publishers p
LEFT JOIN pub_info pi ON p.pub_id = pi.pub_id
```

### Stores to Discounts
```sql
stores st
LEFT JOIN discounts d ON st.stor_id = d.stor_id
```

---

## Business Rules as SQL

| Rule | SQL Condition |
|------|---------------|
| Author has active contract | `WHERE authors.contract = TRUE` |
| Title is business category | `WHERE titles.type = 'business'` |
| Title is cooking category | `WHERE titles.type IN ('mod_cook', 'trad_cook')` |
| Title is psychology category | `WHERE titles.type = 'psychology'` |
| Title is popular computing | `WHERE titles.type = 'popular_comp'` |
| Title is undecided category | `WHERE titles.type = 'UNDECIDED'` |
| Author is primary/first author | `WHERE titleauthor.au_ord = TRUE` |
| Payment terms: Net 30 | `WHERE sales.payterms = 'Net 30'` |
| Payment terms: Net 60 | `WHERE sales.payterms = 'Net 60'` |
| Payment terms: On Invoice | `WHERE sales.payterms = 'ON invoice'` |
| Discount type: Volume | `WHERE discounts.discounttype = 'Volume Discount'` |
| Discount type: Initial Customer | `WHERE discounts.discounttype = 'Initial Customer'` |
| Discount type: Customer | `WHERE discounts.discounttype = 'Customer Discount'` |
| Employee job level range valid | `WHERE employee.job_lvl BETWEEN jobs.min_lvl AND jobs.max_lvl` |
| Sales quantity in royalty bracket | `WHERE sales.qty BETWEEN roysched.lorange AND roysched.hirange` |
| Publisher in USA | `WHERE publishers.country = 'USA'` |
| Publisher in France | `WHERE publishers.country = 'France'` |
| Publisher in Germany | `WHERE publishers.country = 'Germany'` |
| Store in California | `WHERE stores.state = 'CA'` |
| Store in Washington | `WHERE stores.state = 'WA'` |
| Store in Oregon | `WHERE stores.state = 'OR'` |
| Author in California | `WHERE authors.state = 'CA'` |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| author | `authors` table |
| book, publication, title | `titles` table |
| publisher, publishing house | `publishers` table |
| store, bookstore, retailer | `stores` table |
| sale, order, transaction | `sales` table |
| employee, staff, personnel | `employee` table |
| job, position, role | `jobs` table |
| author-book relationship | `titleauthor` table |
| royalty tier, royalty bracket | `roysched` table |
| discount tier, pricing tier | `discounts` table |
| publisher details, publisher metadata | `pub_info` table |
| author ID | `authors.au_id` |
| author name | `CONCAT(authors.au_fname, ' ', authors.au_lname)` |
| book title | `titles.title` |
| book price | `titles.price` |
| book sales | `titles.ytd_sales` |
| book genre, book category | `titles.type` |
| publisher name | `publishers.pub_name` |
| store name | `stores.stor_name` |
| order date | `sales.ord_date` |
| order quantity | `sales.qty` |
| employee name | `CONCAT(employee.fname, ' ', employee.lname)` |
| job title | `jobs.job_desc` |
| job level, seniority | `employee.job_lvl` |
| hire date | `employee.hire_date` |
| primary author, first author | `titleauthor.au_ord = TRUE` |
| author royalty share | `titleauthor.royaltyper` |
| royalty percentage | `titles.royalty` or `roysched.royalty` |
| advance payment | `titles.advance` |
| publication date | `titles.pubdate` |
| discount rate | `discounts.discount` |
| payment terms | `sales.payterms` |