# DCG Schema Reference Guide

## Schema Summary
This schema stores sentences classified as positive or negative, with individual terms extracted and indexed for each sentence.

## Join Paths

**Sentences to their terms:**
```sql
FROM DCG.sentences s
JOIN DCG.terms t ON s.id = t.id_sentence
```

## Table Reference

### `DCG.sentences`
Classified sentences. Plain English: sentence records with sentiment labels.

| Column | Notes |
|--------|-------|
| `class` | Enumerated values: `pos`, `neg` |

### `DCG.terms`
Individual terms extracted from sentences. Plain English: term inventory indexed by sentence and position.

| Column | Notes |
|--------|-------|
| `id_sentence` | Foreign key to `DCG.sentences.id` |
| `id_term` | Position/sequence index of term within the sentence (1-based) |
| `term` | Enumerated values: `a`, `admires`, `annie`, `every`, `john`, `likes`, `man`, `monet`, `paints`, `that`, `woman` |