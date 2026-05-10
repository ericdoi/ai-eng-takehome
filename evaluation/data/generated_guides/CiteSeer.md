# CiteSeer Schema Reference Guide

## Schema Summary
This schema contains academic papers, their citation relationships, and word content associations, with papers classified into six research domains.

## Join Paths

**Papers to their citations (outgoing):**
```sql
FROM CiteSeer.paper p
JOIN CiteSeer.cites c ON p.paper_id = c.citing_paper_id
```

**Papers to papers that cite them (incoming):**
```sql
FROM CiteSeer.paper p
JOIN CiteSeer.cites c ON p.paper_id = c.cited_paper_id
```

**Papers to their word content:**
```sql
FROM CiteSeer.paper p
JOIN CiteSeer.content ct ON p.paper_id = ct.paper_id
```

**Citation chain (citing paper → cited paper):**
```sql
FROM CiteSeer.cites c
JOIN CiteSeer.paper p_citing ON c.citing_paper_id = p_citing.paper_id
JOIN CiteSeer.paper p_cited ON c.cited_paper_id = p_cited.paper_id
```

## Table Reference

### `CiteSeer.paper`
Academic papers with research domain classification.

| Column | Notes |
|--------|-------|
| `paper_id` | Unique paper identifier (VARCHAR); may be numeric or alphanumeric string |
| `class_label` | Research domain; enumerated values: **AI**, **Agents**, **DB**, **HCI**, **IR**, **ML** |

### `CiteSeer.cites`
Directed citation relationships between papers.

| Column | Notes |
|--------|-------|
| `citing_paper_id` | Paper that contains the citation (references another paper) |
| `cited_paper_id` | Paper being referenced/cited |
| | Self-citations possible (citing_paper_id = cited_paper_id) |

### `CiteSeer.content`
Word occurrences within papers.

| Column | Notes |
|--------|-------|
| `paper_id` | Paper containing the word |
| `word_cited_id` | Word identifier (e.g., "word1163"); represents vocabulary terms in the paper |

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| paper domain / research area / category | `CiteSeer.paper.class_label` |
| cites / references / citations | `CiteSeer.cites` table |
| cited by / incoming citations | `CiteSeer.cites.cited_paper_id` |
| cites / outgoing citations | `CiteSeer.cites.citing_paper_id` |
| paper content / vocabulary / terms | `CiteSeer.content` table |
| word / term | `CiteSeer.content.word_cited_id` |