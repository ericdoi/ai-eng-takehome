# CORA Schema Reference Guide

## 1. Schema Summary

The CORA schema contains academic paper metadata, including paper classifications, citation relationships, and word content associations for machine learning research papers.

---

## 2. Table Reference

### Table: `CORA.paper`
**Meaning:** Master table of academic papers with their research classification.  
**Synonyms:** papers, documents, research papers

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `paper_id` | BIGINT | Unique identifier for a paper | paper identifier, document ID |
| `class_label` | VARCHAR | Research category classification | category, classification, research area, topic |

**Enumerated Values for `class_label`:**
- `Case_Based`
- `Genetic_Algorithms`
- `Neural_Networks`
- `Probabilistic_Methods`
- `Reinforcement_Learning`
- `Rule_Learning`
- `Theory`

---

### Table: `CORA.cites`
**Meaning:** Citation relationships between papers; records which papers cite which other papers.  
**Synonyms:** citations, references, citation graph, edges

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `cited_paper_id` | BIGINT | Paper ID of the cited work (target) | referenced paper, cited work |
| `citing_paper_id` | BIGINT | Paper ID of the citing work (source) | referencing paper, citing work |

---

### Table: `CORA.content`
**Meaning:** Word-to-paper associations; maps vocabulary terms to papers in which they appear.  
**Synonyms:** words, vocabulary, content words, paper words

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `paper_id` | BIGINT | Paper ID containing the word | document ID |
| `word_cited_id` | VARCHAR | Vocabulary term identifier | word ID, term, vocabulary term |

---

## 3. Join Paths

| Join | Condition | Purpose |
|------|-----------|---------|
| `paper` ↔ `cites` (cited) | `CORA.paper.paper_id = CORA.cites.cited_paper_id` | Get metadata of cited papers |
| `paper` ↔ `cites` (citing) | `CORA.paper.paper_id = CORA.cites.citing_paper_id` | Get metadata of citing papers |
| `paper` ↔ `content` | `CORA.paper.paper_id = CORA.content.paper_id` | Get words in a paper or papers containing a word |
| `cites` ↔ `paper` (both directions) | `CORA.cites.cited_paper_id = p1.paper_id AND CORA.cites.citing_paper_id = p2.paper_id` | Get full metadata for both papers in a citation |

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation. The following are structural constraints:

- **Valid classification:** `WHERE class_label IN ('Case_Based', 'Genetic_Algorithms', 'Neural_Networks', 'Probabilistic_Methods', 'Reinforcement_Learning', 'Rule_Learning', 'Theory')`
- **Citation relationship exists:** `WHERE cited_paper_id IS NOT NULL AND citing_paper_id IS NOT NULL`
- **Paper has content:** `WHERE paper_id IN (SELECT DISTINCT paper_id FROM CORA.content)`

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| paper classification | `CORA.paper.class_label` |
| research category | `CORA.paper.class_label` |
| cited by | `CORA.cites.citing_paper_id` |
| cites | `CORA.cites.cited_paper_id` |
| citation count | `COUNT(CORA.cites.citing_paper_id)` |
| papers citing X | `SELECT citing_paper_id FROM CORA.cites WHERE cited_paper_id = X` |
| papers cited by X | `SELECT cited_paper_id FROM CORA.cites WHERE citing_paper_id = X` |
| paper vocabulary | `CORA.content.word_cited_id` |
| papers containing word | `SELECT paper_id FROM CORA.content WHERE word_cited_id = 'wordX'` |
| words in paper | `SELECT word_cited_id FROM CORA.content WHERE paper_id = X` |
| papers in category | `SELECT paper_id FROM CORA.paper WHERE class_label = 'CategoryName'` |