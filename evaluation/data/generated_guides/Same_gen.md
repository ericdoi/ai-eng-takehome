# Same_gen Schema Reference Guide

## Schema Summary
This schema models generational relationships between people, tracking parent-child connections and identifying individuals who belong to the same generation.

## Join Paths

**Find people in the same generation as a target person:**
```sql
SELECT sg.name2
FROM Same_gen.same_gen sg
WHERE sg.name1 = 'ali1'
```

**Find all parent-child pairs:**
```sql
SELECT p.name1, p.name2
FROM Same_gen.parent p
```

**Cross-reference person with same-generation relationships:**
```sql
SELECT sg.name1, sg.name2
FROM Same_gen.same_gen sg
JOIN Same_gen.person p ON sg.name1 = p.name
```

**Retrieve target classification for a person pair:**
```sql
SELECT t.target
FROM Same_gen.target t
WHERE t.name1 = 'ali1' AND t.name2 = 'ali2'
```

## Table Reference

### `Same_gen.parent`
Parent-child relationships. Each row represents one parent (name1) and one child (name2).
- **name1**: Parent name
- **name2**: Child name

### `Same_gen.person`
Master list of all individuals in the dataset.
- **name**: Person identifier

### `Same_gen.same_gen`
Pairs of people belonging to the same generation.
- **name1**: First person (reference individual)
- **name2**: Second person in same generation as name1

### `Same_gen.target`
Classification labels for person pairs.
- **name1**: First person
- **name2**: Second person
- **target**: Binary classification (0 or 1); 0 indicates not same generation, 1 indicates same generation