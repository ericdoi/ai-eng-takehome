# FTP Schema Reference Guide

## Schema Summary
This schema tracks user sessions and the sequence of product categories viewed during each session, with demographic information.

## Join Paths

**Sessions with their product views:**
```sql
FROM ftp.session s
JOIN ftp.product p ON s.session_id = p.session_id
```

**Product views ordered chronologically:**
```sql
FROM ftp.session s
JOIN ftp.product p ON s.session_id = p.session_id
ORDER BY s.start_time, p.sequence_order
```

## Table Reference

### `ftp.session`
User session records with timing and demographics.

| Column | Notes |
|--------|-------|
| `session_id` | VARCHAR; primary key; links to `ftp.product.session_id` |
| `start_time` | TIMESTAMP; session start |
| `end_time` | TIMESTAMP; session end |
| `gender` | VARCHAR; enumerated: `female`, `male` |

### `ftp.product`
Product category views within sessions, ordered sequentially.

| Column | Notes |
|--------|-------|
| `session_id` | VARCHAR; foreign key to `ftp.session.session_id` |
| `sequence_order` | BIGINT; view order within session (1-indexed); use for chronological ordering |
| `category_a` | VARCHAR; top-level category; enumerated: `A00001` through `A00011` |
| `category_b` | VARCHAR; second-level category |
| `category_c` | VARCHAR; third-level category |
| `category_d` | VARCHAR; fourth-level category; may contain non-standard values (e.g., `D24897`) |

## Synonym Glossary

| Term | Maps To |
|------|---------|
| user | `ftp.session.session_id` |
| view / product view | row in `ftp.product` |
| session duration | `EXTRACT(EPOCH FROM (ftp.session.end_time - ftp.session.start_time))` or `DATEDIFF(second, ftp.session.start_time, ftp.session.end_time)` |
| category hierarchy | `ftp.product.category_a`, `category_b`, `category_c`, `category_d` (nested levels) |
| view sequence | `ftp.product.sequence_order` |