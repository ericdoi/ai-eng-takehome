# WebKP Schema Reference Guide

## Schema Summary
This schema models a web knowledge base of Cornell University webpages, tracking their classification, content (word associations), and citation relationships.

## Join Paths

**Webpage to its content words:**
```sql
FROM WebKP.webpage w
JOIN WebKP.content c ON w.webpage_id = c.webpage_id
```

**Webpage citations (citing → cited):**
```sql
FROM WebKP.cites ct
JOIN WebKP.webpage citing ON ct.citing_paper_id = citing.webpage_id
JOIN WebKP.webpage cited ON ct.cited_paper_id = cited.webpage_id
```

**Webpage class and its citations:**
```sql
FROM WebKP.webpage w
JOIN WebKP.cites ct ON w.webpage_id = ct.citing_paper_id
```

## Table Reference

### `WebKP.webpage`
Classified webpages in the Cornell domain.

| Column | Semantics |
|--------|-----------|
| `webpage_id` | Full URL; primary identifier |
| `class_label` | Enumerated page type: `course`, `faculty`, `project`, `staff`, `student` |

### `WebKP.content`
Word-to-webpage associations (inverted index).

| Column | Semantics |
|--------|-----------|
| `webpage_id` | Foreign key to `WebKP.webpage.webpage_id` |
| `word_cited_id` | Word identifier (e.g., `word1020`); links to external word vocabulary |

### `WebKP.cites`
Directional citation edges between webpages.

| Column | Semantics |
|--------|-----------|
| `citing_paper_id` | URL of page containing the citation (source) |
| `cited_paper_id` | URL of page being cited (target) |