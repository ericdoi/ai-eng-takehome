# Mooney_Family Schema Reference Guide

## Schema Summary
This schema models family relationships across the Mooney family, with tables representing kinship roles (parent, sibling, spouse, child, aunt, uncle, niece, nephew) connecting pairs of individuals.

---

## Join Paths

**Find all parent-child relationships:**
```sql
SELECT p.name1 AS parent, p.name2 AS child
FROM Mooney_Family.father p
UNION ALL
SELECT m.name1 AS parent, m.name2 AS child
FROM Mooney_Family.mother m
```

**Find all spouse pairs:**
```sql
SELECT h.name1 AS husband, h.name2 AS wife
FROM Mooney_Family.husband h
UNION ALL
SELECT w.name2 AS husband, w.name1 AS wife
FROM Mooney_Family.wife w
```

**Find all siblings:**
```sql
SELECT b.name1 AS person1, b.name2 AS person2
FROM Mooney_Family.brother b
UNION ALL
SELECT s.name1 AS person1, s.name2 AS person2
FROM Mooney_Family.sister s
```

**Find all extended family (aunts, uncles, nieces, nephews):**
```sql
SELECT a.name1 AS aunt, a.name2 AS niece_nephew
FROM Mooney_Family.aunt a
UNION ALL
SELECT u.name1 AS uncle, u.name2 AS niece_nephew
FROM Mooney_Family.uncle u
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| parent | `Mooney_Family.father` or `Mooney_Family.mother` |
| father | `Mooney_Family.father` (name1 = father, name2 = child) |
| mother | `Mooney_Family.mother` (name1 = mother, name2 = child) |
| spouse | `Mooney_Family.husband` or `Mooney_Family.wife` |
| husband | `Mooney_Family.husband` (name1 = husband, name2 = wife) |
| wife | `Mooney_Family.wife` (name1 = wife, name2 = husband) |
| sibling | `Mooney_Family.brother` or `Mooney_Family.sister` |
| brother | `Mooney_Family.brother` (name1 = person, name2 = sibling) |
| sister | `Mooney_Family.sister` (name1 = person, name2 = sibling) |
| child | `Mooney_Family.son` or `Mooney_Family.daughter` |
| son | `Mooney_Family.son` (name1 = parent, name2 = son) |
| daughter | `Mooney_Family.daughter` (name1 = parent, name2 = daughter) |
| aunt | `Mooney_Family.aunt` (name1 = aunt, name2 = niece/nephew) |
| uncle | `Mooney_Family.uncle` (name1 = uncle, name2 = niece/nephew) |
| niece | `Mooney_Family.niece` (name1 = aunt/uncle, name2 = niece) |
| nephew | `Mooney_Family.nephew` (name1 = aunt/uncle, name2 = nephew) |
| all people | `Mooney_Family.person` |

---

## Table Reference

### `Mooney_Family.person`
**Meaning:** Master list of all individuals in the Mooney family.

| Column | Type | Notes |
|--------|------|-------|
| name | VARCHAR | Unique person identifier; used as name1 or name2 in relationship tables |

---

### `Mooney_Family.father` (and father1–father5)
**Meaning:** Father-child relationships. name1 is the father, name2 is the child.

| Column | Type | Notes |
|--------|------|-------|
| name1 | VARCHAR | Father's name |
| name2 | VARCHAR | Child's name |

---

### `Mooney_Family.mother` (and mother1–mother5)
**Meaning:** Mother-child relationships. name1 is the mother, name2 is the child.

| Column | Type | Notes |
|--------|------|-------|
| name1 | VARCHAR | Mother's name |
| name2 | VARCHAR | Child's name |

---

### `Mooney_Family.son` (and son1–son5)
**Meaning:** Parent-son relationships. name1 is the parent, name2 is the son.

| Column | Type | Notes |
|--------|------|-------|
| name1 | VARCHAR | Parent's name |
| name2 | VARCHAR | Son's name |

---

### `Mooney_Family.daughter` (and daughter1–daughter5)
**Meaning:** Parent-daughter relationships. name1 is the parent, name2 is the daughter.

| Column | Type | Notes |
|--------|------|-------|
| name1 | VARCHAR | Parent's name |
| name2 | VARCHAR | Daughter's name |

---

### `Mooney_Family.husband` (and husband1–husband5)
**Meaning:** Husband-wife relationships. name1 is the husband, name2 is the wife.

| Column | Type | Notes |
|--------|------|-------|
| name1 | VARCHAR | Husband's name |
| name2 | VARCHAR | Wife's name |

---

### `Mooney_Family.wife` (and wife1–wife5)
**Meaning:** Wife-husband relationships (inverse of husband table). name1 is the wife, name2 is the husband.

| Column | Type | Notes |
|--------|------|-------|
| name1 | VARCHAR | Wife's name |
| name2 | VARCHAR | Husband's name |

---

### `Mooney_Family.brother` (and brother1–brother5)
**Meaning:** Sibling relationships where name2 is a brother of name1.

| Column | Type | Notes |
|--------|------|-------|
| name1 | VARCHAR | Person's name |
| name2 | VARCHAR | Brother's name |

---

### `Mooney_Family.sister` (and sister1–sister5)
**Meaning:** Sibling relationships where name2 is a sister of name1.

| Column | Type | Notes |
|--------|------|-------|
| name1 | VARCHAR | Person's name |
| name2 | VARCHAR | Sister's name |

---

### `Mooney_Family.aunt` (and aunt1–aunt5)
**Meaning:** Aunt-niece/nephew relationships. name1 is the aunt, name2 is the niece or nephew.

| Column | Type | Notes |
|--------|------|-------|
| name1 | VARCHAR | Aunt's name |
| name2 | VARCHAR | Niece or nephew's name |

---

### `Mooney_Family.uncle` (and uncle1–uncle5)
**Meaning:** Uncle-niece/nephew relationships. name1 is the uncle, name2 is the niece or nephew.

| Column | Type | Notes |
|--------|------|-------|
| name1 | VARCHAR | Uncle's name |
| name2 | VARCHAR | Niece or nephew's name |

---

### `Mooney_Family.niece` (and niece1–niece5)
**Meaning:** Niece relationships. name1 is the aunt/uncle, name2 is the niece.

| Column | Type | Notes |
|--------|------|-------|
| name1 | VARCHAR | Aunt or uncle's name |
| name2 | VARCHAR | Niece's name |

---

### `Mooney_Family.nephew` (and nephew1–nephew5)
**Meaning:** Nephew relationships. name1 is the aunt/uncle, name2 is the nephew.

| Column | Type | Notes |
|--------|------|-------|
| name1 | VARCHAR | Aunt or uncle's name |
| name2 | VARCHAR | Nephew's name |

---

## Notes on Duplicate Tables

Tables suffixed with `1` through `5` (e.g., `father1`, `father2`, `mother1`, etc.) are exact duplicates of their base tables (e.g., `father`, `mother`). Query the base table unless a specific versioned table is required.