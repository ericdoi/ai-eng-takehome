# WebKP Schema Reference Guide

## 1. Schema Summary

The WebKP schema contains a web knowledge portal tracking relationships between webpages, their content (indexed by words), and citation links between pages, with webpage classification into five categories.

---

## 2. Table Reference

### Table: `WebKP.cites`
**Meaning:** Citation relationships between webpages; records which pages cite which other pages.
**Synonyms:** citations, links, references

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `cited_paper_id` | VARCHAR | URL of the webpage being cited (target of citation) | cited_url, target_page, referenced_page |
| `citing_paper_id` | VARCHAR | URL of the webpage that contains the citation (source of citation) | citing_url, source_page, referencing_page |

---

### Table: `WebKP.content`
**Meaning:** Word content index; maps webpages to the words they contain.
**Synonyms:** word_index, page_content, indexed_words

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `webpage_id` | VARCHAR | URL identifier of the webpage | page_url, page_id, url |
| `word_cited_id` | VARCHAR | Unique identifier for a word appearing in the webpage (format: `word####`) | word_id, word_token, indexed_word |

---

### Table: `WebKP.webpage`
**Meaning:** Webpage registry with classification; master list of all webpages and their category labels.
**Synonyms:** pages, page_registry, page_classification

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `webpage_id` | VARCHAR | URL identifier of the webpage (primary key) | page_url, page_id, url |
| `class_label` | VARCHAR | Classification category of the webpage | category, page_type, classification |

**Enumerated Values for `class_label`:**
- `course`
- `faculty`
- `project`
- `staff`
- `student`

---

## 3. Join Paths

**Webpages to their content:**
```sql
WebKP.webpage w
JOIN WebKP.content c ON w.webpage_id = c.webpage_id
```

**Citation relationships (cited page to citing page):**
```sql
WebKP.cites ct
JOIN WebKP.webpage cited ON ct.cited_paper_id = cited.webpage_id
JOIN WebKP.webpage citing ON ct.citing_paper_id = citing.webpage_id
```

**Webpages by class with their citations:**
```sql
WebKP.webpage w
JOIN WebKP.cites ct ON w.webpage_id = ct.citing_paper_id
```

**All three tables (content + citations):**
```sql
WebKP.webpage w
JOIN WebKP.content c ON w.webpage_id = c.webpage_id
JOIN WebKP.cites ct ON w.webpage_id = ct.citing_paper_id
```

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation. Apply standard data integrity assumptions:
- `webpage_id` values in `cites` and `content` should reference valid `webpage_id` values in `webpage`
- `class_label` must be one of the five enumerated values

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| webpage URL | `webpage.webpage_id`, `cites.cited_paper_id`, `cites.citing_paper_id`, `content.webpage_id` |
| page type / category | `webpage.class_label` |
| student pages | `WHERE webpage.class_label = 'student'` |
| faculty pages | `WHERE webpage.class_label = 'faculty'` |
| course pages | `WHERE webpage.class_label = 'course'` |
| project pages | `WHERE webpage.class_label = 'project'` |
| staff pages | `WHERE webpage.class_label = 'staff'` |
| cited by | `cites.citing_paper_id` references `cites.cited_paper_id` |
| cites / references | `cites.citing_paper_id` → `cites.cited_paper_id` |
| page contains word | `content.webpage_id` with `content.word_cited_id` |
| incoming citations | `COUNT(cites.citing_paper_id)` grouped by `cites.cited_paper_id` |
| outgoing citations | `COUNT(cites.cited_paper_id)` grouped by `cites.citing_paper_id` |
| vocabulary of page | `SELECT DISTINCT word_cited_id FROM content WHERE webpage_id = ?` |