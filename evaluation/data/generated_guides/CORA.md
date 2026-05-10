# CORA Schema Reference Guide

## Schema Summary
The CORA schema contains academic papers, their classification labels, citation relationships, and word content associations for machine learning research papers.

## Join Paths

**Papers with their citations (papers that cite a given paper):**
```sql
FROM CORA.paper p
JOIN CORA.cites c ON p.paper_id = c.cited_paper_id
```

**Papers with their references (papers that a given paper cites):**
```sql
FROM CORA.paper p
JOIN CORA.cites c ON p.paper_id = c.citing_paper_id
```

**Papers with their word content:**
```sql
FROM CORA.paper p
JOIN CORA.content ct ON p.paper_id = ct.paper_id
```

**Complete citation network with both paper classifications:**
```sql
FROM CORA.cites c
JOIN CORA.paper p_cited ON c.cited_paper_id = p_cited.paper_id
JOIN CORA.paper p_citing ON c.citing_paper_id = p_citing.paper_id
```

## Table Reference

### `CORA.paper`
Academic papers with research classification.

| Column | Semantics |
|--------|-----------|
| `paper_id` | Unique paper identifier |
| `class_label` | Research category. Enum values: `Case_Based`, `Genetic_Algorithms`, `Neural_Networks`, `Probabilistic_Methods`, `Reinforcement_Learning`, `Rule_Learning`, `Theory` |

### `CORA.cites`
Citation relationships between papers.

| Column | Semantics |
|--------|-----------|
| `cited_paper_id` | Paper being referenced (target of citation) |
| `citing_paper_id` | Paper that contains the reference (source of citation) |

### `CORA.content`
Word tokens associated with papers.

| Column | Semantics |
|--------|-----------|
| `paper_id` | Paper containing the word |
| `word_cited_id` | Word token identifier (format: `word` + numeric ID) |