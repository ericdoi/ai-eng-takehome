# PubMed_Diabetes Schema Reference Guide

## 1. Schema Summary

The `PubMed_Diabetes` schema contains PubMed research papers on diabetes, their text content represented as word-TF-IDF vectors, and citation relationships between papers.

---

## 2. Table Reference

### Table: `PubMed_Diabetes.paper`
**Meaning:** Research papers in the diabetes literature corpus.  
**Synonyms:** papers, documents, articles

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `paper_id` | BIGINT | Unique identifier for a paper | document_id, article_id |
| `class_label` | BIGINT | Classification category assigned to the paper | label, category, class |

**Notable values:** `class_label` observed as `1` in sample data (exact enumeration unknown; verify with domain expert).

---

### Table: `PubMed_Diabetes.content`
**Meaning:** Text content of papers represented as word tokens with TF-IDF scores.  
**Synonyms:** word_vectors, text_features, term_frequencies

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `paper_id` | BIGINT | Foreign key reference to paper | document_id |
| `word` | VARCHAR | Tokenized word or term from paper text | term, token, word_id |
| `tf_idf` | DOUBLE | Term frequency-inverse document frequency score (0.0–1.0 range typical) | score, weight, relevance |

**Notable values:** `word` format observed as `w-0`, `w-001`, `w-01`, `w-4`, `w-60` (hashed/anonymized tokens).

---

### Table: `PubMed_Diabetes.cites`
**Meaning:** Citation relationships between papers (directed edges in citation graph).  
**Synonyms:** citations, references, edges

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `citing_paper_id` | BIGINT | Paper ID of the citing paper (source) | source_paper_id, from_paper_id |
| `cites_paper_id` | BIGINT | Paper ID of the cited paper (target) | cited_paper_id, to_paper_id, reference_id |

**Notable values:** Both columns contain `paper_id` values; no null values in sample data.

---

## 3. Join Paths

| Join Type | Condition | Purpose |
|-----------|-----------|---------|
| **paper ↔ content** | `paper.paper_id = content.paper_id` | Link papers to their word content |
| **paper ↔ cites (citing)** | `paper.paper_id = cites.citing_paper_id` | Find papers that cite others |
| **paper ↔ cites (cited)** | `paper.paper_id = cites.cites_paper_id` | Find papers that are cited by others |
| **cites ↔ paper (both)** | `cites.citing_paper_id = p1.paper_id AND cites.cites_paper_id = p2.paper_id` | Link citing and cited papers with their metadata |

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation. Common patterns:

- **Rule:** "Find papers in a specific class"  
  → `WHERE paper.class_label = <value>`

- **Rule:** "Find high-relevance words in a paper"  
  → `WHERE content.tf_idf > <threshold>`

- **Rule:** "Find citation relationships between two papers"  
  → `WHERE cites.citing_paper_id = <id1> AND cites.cites_paper_id = <id2>`

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| paper, document, article | `paper.paper_id` |
| class, category, label | `paper.class_label` |
| word, term, token | `content.word` |
| relevance, weight, score | `content.tf_idf` |
| citation, reference | `cites` table |
| citing paper, source | `cites.citing_paper_id` |
| cited paper, target, reference | `cites.cites_paper_id` |
| paper content, text features | `content` table |
| citation graph, citation network | `cites` table joined with `paper` |