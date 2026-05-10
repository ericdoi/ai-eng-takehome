# CiteSeer Schema Reference Guide

## 1. Schema Summary

The CiteSeer schema contains academic paper metadata, citation relationships, and word content associations for papers classified into six research domains.

---

## 2. Table Reference

### Table: `CiteSeer.cites`
**Meaning:** Citation relationships between papers (which papers cite which other papers).
**Synonyms:** citations, references, citation graph

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `cited_paper_id` | VARCHAR | The paper being cited (referenced) | cited_id, target_paper, referenced_paper |
| `citing_paper_id` | VARCHAR | The paper that contains the citation | citing_id, source_paper, referencing_paper |

**Notable values:** Paper IDs are numeric strings (e.g., `100157`) or alphanumeric identifiers (e.g., `bradshaw97introduction`).

---

### Table: `CiteSeer.content`
**Meaning:** Word-to-paper associations; maps which words appear in which papers.
**Synonyms:** paper_words, word_content, paper_vocabulary

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `paper_id` | VARCHAR | Identifier of the paper | paper, document_id |
| `word_cited_id` | VARCHAR | Identifier of a word appearing in the paper | word_id, term_id, vocabulary_term |

**Notable values:** Word IDs follow pattern `word####` (e.g., `word1163`).

---

### Table: `CiteSeer.paper`
**Meaning:** Paper metadata including research domain classification.
**Synonyms:** papers, documents, publications

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `paper_id` | VARCHAR | Unique paper identifier | paper, document_id, publication_id |
| `class_label` | VARCHAR | Research domain classification | category, domain, research_area, subject |

**Enumerated values (exact):** `AI`, `Agents`, `DB`, `HCI`, `IR`, `ML`

---

## 3. Join Paths

| Join | SQL Condition |
|------|---------------|
| Paper to its citations (outgoing) | `CiteSeer.paper.paper_id = CiteSeer.cites.citing_paper_id` |
| Paper to papers that cite it (incoming) | `CiteSeer.paper.paper_id = CiteSeer.cites.cited_paper_id` |
| Paper to its word content | `CiteSeer.paper.paper_id = CiteSeer.content.paper_id` |
| Citation chain (paper A cites paper B) | `CiteSeer.cites.cited_paper_id = CiteSeer.paper.paper_id` AND `CiteSeer.cites.citing_paper_id = CiteSeer.paper.paper_id` |

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation. All columns accept non-null values based on sample data.

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| papers in a domain | `WHERE CiteSeer.paper.class_label = '[domain]'` |
| papers citing a paper | `CiteSeer.cites.cited_paper_id = [paper_id]` |
| papers cited by a paper | `CiteSeer.cites.citing_paper_id = [paper_id]` |
| citation count (incoming) | `COUNT(CiteSeer.cites.cited_paper_id)` |
| citation count (outgoing) | `COUNT(CiteSeer.cites.citing_paper_id)` |
| papers containing a word | `CiteSeer.content.word_cited_id = '[word_id]'` |
| words in a paper | `CiteSeer.content.paper_id = '[paper_id]'` |
| AI papers | `WHERE CiteSeer.paper.class_label = 'AI'` |
| Machine Learning papers | `WHERE CiteSeer.paper.class_label = 'ML'` |
| Database papers | `WHERE CiteSeer.paper.class_label = 'DB'` |
| Information Retrieval papers | `WHERE CiteSeer.paper.class_label = 'IR'` |
| Agent papers | `WHERE CiteSeer.paper.class_label = 'Agents'` |
| Human-Computer Interaction papers | `WHERE CiteSeer.paper.class_label = 'HCI'` |