# FTP Schema Reference Guide

## 1. Schema Summary

The `ftp` schema contains user session data with hierarchical product category information, tracking browsing behavior across four category levels with timestamps and demographic attributes.

---

## 2. Table Reference

### Table: `ftp.session`

**Meaning:** User session records with temporal and demographic metadata.  
**Synonyms:** sessions, user sessions, visits

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `session_id` | VARCHAR | Unique session identifier | user_id, session identifier |
| `start_time` | TIMESTAMP | Session start datetime | session_start, begin_time |
| `end_time` | TIMESTAMP | Session end datetime | session_end, finish_time |
| `gender` | VARCHAR | User gender classification | user_gender, demographic |

**Enumerated Values:**
- `gender`: `female`, `male`

---

### Table: `ftp.product`

**Meaning:** Product category hierarchy records within sessions, ordered sequentially.  
**Synonyms:** products, browsing history, category records, product views

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `session_id` | VARCHAR | Foreign key to session | user_id, session identifier |
| `sequence_order` | BIGINT | Sequential position within session (1-indexed) | order, position, step, sequence |
| `category_a` | VARCHAR | Top-level product category | level_1, primary_category |
| `category_b` | VARCHAR | Second-level product category | level_2, secondary_category |
| `category_c` | VARCHAR | Third-level product category | level_3, tertiary_category |
| `category_d` | VARCHAR | Fourth-level product category | level_4, quaternary_category |

**Enumerated Values:**
- `category_a`: `A00001`, `A00002`, `A00003`, `A00004`, `A00005`, `A00006`, `A00007`, `A00008`, `A00009`, `A00010`, `A00011`

---

## 3. Join Paths

**Primary join between tables:**

```sql
ftp.product p
INNER JOIN ftp.session s ON p.session_id = s.session_id
```

**Relationship:** One session has many products; one product belongs to one session.

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation. Common implicit rules:

- **Valid session:** `WHERE s.start_time <= s.end_time`
- **Session duration (seconds):** `EXTRACT(EPOCH FROM (s.end_time - s.start_time))`
- **Products in sequence:** `WHERE p.sequence_order >= 1` (1-indexed ordering)

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| user | `session_id` |
| session duration | `EXTRACT(EPOCH FROM (end_time - start_time))` |
| session length | `EXTRACT(EPOCH FROM (end_time - start_time))` |
| browsing history | `ftp.product` |
| product view | Row in `ftp.product` |
| category level 1 | `ftp.product.category_a` |
| category level 2 | `ftp.product.category_b` |
| category level 3 | `ftp.product.category_c` |
| category level 4 | `ftp.product.category_d` |
| top category | `ftp.product.category_a` |
| female users | `WHERE ftp.session.gender = 'female'` |
| male users | `WHERE ftp.session.gender = 'male'` |
| products per session | `COUNT(ftp.product.sequence_order)` |
| session count | `COUNT(DISTINCT ftp.session.session_id)` |