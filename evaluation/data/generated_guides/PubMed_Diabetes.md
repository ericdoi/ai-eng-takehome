# PubMed_Diabetes Schema Reference Guide

## Schema Summary
This schema contains PubMed research papers on diabetes, their citation relationships, and word-frequency content indexed by TF-IDF scores.

## Join Paths

**Papers with their cited references:**
```sql
FROM PubMed_Diabetes.paper p
JOIN PubMed_Diabetes.cites c ON p.paper_id = c.citing_paper_id
```

**Papers with their content (words and scores):**
```sql
FROM PubMed_Diabetes.paper p
JOIN PubMed_Diabetes.content ct ON p.paper_id = ct.paper_id
```

**Citation chain (citing paper → cited paper details):**
```sql
FROM PubMed_Diabetes.cites c
JOIN PubMed_Diabetes.paper p_citing ON c.citing_paper_id = p_citing.paper_id
JOIN PubMed_Diabetes.paper p_cited ON c.cites_paper_id = p_cited.paper_id
```

## Table Reference

### `PubMed_Diabetes.paper`
Metadata for each research paper.

| Column | Semantics |
|--------|-----------|
| `paper_id` | Unique paper identifier |
| `class_label` | Paper classification; observed value: `1` |

### `PubMed_Diabetes.cites`
Citation relationships between papers.

| Column | Semantics |
|--------|-----------|
| `citing_paper_id` | Paper ID of the citing work |
| `cites_paper_id` | Paper ID of the cited work |

### `PubMed_Diabetes.content`
Word frequency data for paper content.

| Column | Semantics |
|--------|-----------|
| `paper_id` | Paper ID |
| `word` | Tokenized word identifier (format: `w-###`) |
| `tf_idf` | TF-IDF score (relevance weight); range observed: 0.017–0.040+ |