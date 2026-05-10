# DCG Schema Reference Guide

## 1. Schema Summary

The DCG schema contains sentences classified as positive or negative, with individual terms extracted and indexed for each sentence.

---

## 2. Table Reference

### Table: `DCG.sentences`
**Meaning:** Classified sentences (positive/negative sentiment or grammatical classification)  
**Synonyms:** sentence_data, labeled_sentences

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique sentence identifier | sentence_id, pk |
| `class` | VARCHAR | Sentence classification | classification, label, sentiment |

**Enumerated Values for `class`:**
- `pos` — positive classification
- `neg` — negative classification

---

### Table: `DCG.terms`
**Meaning:** Individual terms/words extracted from sentences with positional indexing  
**Synonyms:** words, tokens, sentence_terms

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_sentence` | BIGINT | Foreign key to `DCG.sentences.id` | sentence_id, fk_sentence |
| `id_term` | BIGINT | Position/sequence index of term within sentence | term_position, term_index, sequence |
| `term` | VARCHAR | The actual word or token | word, token, text |

**Enumerated Values for `term`:**
- `a`, `admires`, `annie`, `every`, `john`, `likes`, `man`, `monet`, `paints`, `that`, `woman`

---

## 3. Join Paths

**Sentences to Terms:**
```sql
DCG.sentences s
INNER JOIN DCG.terms t ON s.id = t.id_sentence
```

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation.

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| positive sentences | `WHERE class = 'pos'` |
| negative sentences | `WHERE class = 'neg'` |
| sentence words | `DCG.terms.term` |
| word position | `DCG.terms.id_term` |
| terms in a sentence | `DCG.terms t WHERE t.id_sentence = {id}` |
| all terms for positive sentences | `DCG.terms t INNER JOIN DCG.sentences s ON t.id_sentence = s.id WHERE s.class = 'pos'` |
| sentence classification | `DCG.sentences.class` |