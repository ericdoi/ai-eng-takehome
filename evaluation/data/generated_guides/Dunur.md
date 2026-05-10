# Dunur Schema Reference Guide

## Schema Summary
This schema models family relationships (kinship) between individuals, with tables representing specific relation types (parent, sibling, spouse, aunt/uncle, niece/nephew) and a target table for classification tasks.

---

## Join Paths

**Find all children of a person:**
```sql
SELECT c.name2 FROM Dunur.son c WHERE c.name1 = 'Alfonso'
UNION ALL
SELECT c.name2 FROM Dunur.daughter c WHERE c.name1 = 'Alfonso'
```

**Find all parents of a person:**
```sql
SELECT p.name2 FROM Dunur.father p WHERE p.name1 = 'Andrew'
UNION ALL
SELECT p.name2 FROM Dunur.mother p WHERE p.name1 = 'Andrew'
```

**Find all siblings of a person:**
```sql
SELECT s.name2 FROM Dunur.brother s WHERE s.name1 = 'Alfonso'
UNION ALL
SELECT s.name2 FROM Dunur.sister s WHERE s.name1 = 'Angela'
```

**Find spouse(s) of a person:**
```sql
SELECT h.name2 FROM Dunur.husband h WHERE h.name1 = 'Andrew'
UNION ALL
SELECT h.name2 FROM Dunur.husband2 h WHERE h.name1 = 'Arthur'
UNION ALL
SELECT w.name2 FROM Dunur.wife w WHERE w.name1 = 'Angela'
UNION ALL
SELECT w.name2 FROM Dunur.wife2 w WHERE w.name1 = 'Angela'
```

**Find dunur relations (specific kinship type):**
```sql
SELECT d.name2 FROM Dunur.dunur d WHERE d.name1 = 'Andrew'
```

---

## Table Reference

### `Dunur.person`
Master list of all individuals in the family tree.
- **name**: Individual identifier (e.g., Alfonso, Andrew, Angela, Arthur, Charles)

### `Dunur.son`
Father-to-son relationships.
- **name1**: Father
- **name2**: Son (child)

### `Dunur.daughter`
Father-to-daughter relationships.
- **name1**: Father
- **name2**: Daughter (child)

### `Dunur.father`
Child-to-father relationships (inverse of son/daughter).
- **name1**: Child
- **name2**: Father

### `Dunur.mother`
Child-to-mother relationships.
- **name1**: Child
- **name2**: Mother

### `Dunur.brother`
Sibling relationships (male perspective).
- **name1**: Brother
- **name2**: Sister or brother's sibling

### `Dunur.sister`
Sibling relationships (female perspective).
- **name1**: Sister
- **name2**: Brother or sister's sibling

### `Dunur.husband`
Primary spouse relationships (male to female).
- **name1**: Husband
- **name2**: Wife

### `Dunur.husband2`
Secondary/alternate spouse relationships (male to female).
- **name1**: Husband
- **name2**: Wife (second marriage or alternate record)

### `Dunur.wife`
Primary spouse relationships (female to male, inverse of husband).
- **name1**: Wife
- **name2**: Husband

### `Dunur.wife2`
Secondary/alternate spouse relationships (female to male, inverse of husband2).
- **name1**: Wife
- **name2**: Husband (second marriage or alternate record)

### `Dunur.aunt`
Aunt relationships.
- **name1**: Aunt
- **name2**: Niece or nephew

### `Dunur.uncle`
Uncle relationships.
- **name1**: Uncle
- **name2**: Niece or nephew

### `Dunur.niece`
Niece relationships.
- **name1**: Niece
- **name2**: Aunt or uncle

### `Dunur.nephew`
Nephew relationships.
- **name1**: Nephew
- **name2**: Aunt or uncle

### `Dunur.dunur`
Special kinship relation (exact semantics not specified in schema; appears symmetric).
- **name1**: First person
- **name2**: Second person (dunur relation)

### `Dunur.target`
Classification dataset with ground truth labels.
- **name1**: First person
- **name2**: Second person
- **is_dunur**: Binary label (0 or 1) indicating whether name1 and name2 have a dunur relationship