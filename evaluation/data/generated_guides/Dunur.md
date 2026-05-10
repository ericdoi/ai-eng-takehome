# Dunur Schema Reference Guide

## Schema Summary
The Dunur schema models family relationships (kinship) between individuals, capturing direct relations (parent-child, spouse) and derived relations (sibling, aunt, uncle, niece, nephew) along with a special "dunur" relationship category.

---

## Table Reference

### Dunur.person
**Meaning:** Master list of all individuals in the family network.  
**Synonyms:** individual, entity, family member

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Unique identifier for a person | person_name, individual_name |

**Notable values:** Alfonso, Andrew, Angela, Arthur, Charles, Charlotte, Christine, Christopher, Emilio, Francesca, Gina, James, Jennifer, Lucia, Margaret, Maria, Marco, Penelope, Pierro, Roberto, Sophia, Tomaso, Victoria

---

### Dunur.father
**Meaning:** Records where name1 is the father of name2.  
**Synonyms:** paternal_relation, parent_child (paternal)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The father | father_name, parent |
| name2 | VARCHAR | The child | child_name, offspring |

**Notable name1 values:** Andrew, Christopher, James, Marco, Pierro, Roberto  
**Notable name2 values:** Alfonso, Angela, Arthur, Charlotte, Colin, Emilio, James, Jennifer, Lucia, Marco, Sophia, Victoria

---

### Dunur.mother
**Meaning:** Records where name1 is the mother of name2.  
**Synonyms:** maternal_relation, parent_child (maternal)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The mother | mother_name, parent |
| name2 | VARCHAR | The child | child_name, offspring |

**Notable name1 values:** Christine, Francesca, Lucia, Maria, Penelope, Victoria  
**Notable name2 values:** Alfonso, Angela, Arthur, Charlotte, Colin, Emilio, James, Jennifer, Lucia, Marco, Sophia, Victoria

---

### Dunur.son
**Meaning:** Records where name1 is the father and name2 is the son.  
**Synonyms:** paternal_male_child, father_son

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The father | father_name, parent |
| name2 | VARCHAR | The son | son_name, male_child |

**Notable name1 values:** Alfonso, Arthur, Colin, Emilio, James, Marco  
**Notable name2 values:** Andrew, Christine, Christopher, Francesca, James, Lucia, Marco, Maria, Penelope, Pierro, Roberto, Victoria

---

### Dunur.daughter
**Meaning:** Records where name1 is the mother and name2 is the daughter.  
**Synonyms:** maternal_female_child, mother_daughter

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The mother | mother_name, parent |
| name2 | VARCHAR | The daughter | daughter_name, female_child |

**Notable name1 values:** Angela, Charlotte, Jennifer, Lucia, Sophia, Victoria  
**Notable name2 values:** Andrew, Christine, Christopher, Francesca, James, Lucia, Marco, Maria, Penelope, Pierro, Roberto, Victoria

---

### Dunur.brother
**Meaning:** Records where name1 is the brother of name2.  
**Synonyms:** sibling (male), fraternal_relation

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The brother | brother_name, male_sibling |
| name2 | VARCHAR | The sibling (any gender) | sibling_name |

**Notable name1 values:** Alfonso, Arthur, Colin, Emilio, James, Marco  
**Notable name2 values:** Angela, Charlotte, Jennifer, Lucia, Sophia, Victoria

---

### Dunur.sister
**Meaning:** Records where name1 is the sister of name2.  
**Synonyms:** sibling (female), sororal_relation

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The sister | sister_name, female_sibling |
| name2 | VARCHAR | The sibling (any gender) | sibling_name |

**Notable name1 values:** Angela, Charlotte, Jennifer, Lucia, Sophia, Victoria  
**Notable name2 values:** Alfonso, Arthur, Colin, Emilio, James, Marco

---

### Dunur.husband
**Meaning:** Records where name1 is the husband of name2 (first marriage).  
**Synonyms:** spouse (male), married_to (primary)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The husband | husband_name, male_spouse |
| name2 | VARCHAR | The wife | wife_name, female_spouse |

**Notable name1 values:** Andrew, Arthur, Charles, Christopher, Emilio, James, Marco, Pierro, Roberto, Tomaso  
**Notable name2 values:** Angela, Christine, Francesca, Gina, Jennifer, Lucia, Margaret, Maria, Penelope, Victoria

---

### Dunur.wife
**Meaning:** Records where name1 is the wife of name2 (first marriage).  
**Synonyms:** spouse (female), married_to (primary)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The wife | wife_name, female_spouse |
| name2 | VARCHAR | The husband | husband_name, male_spouse |

**Notable name1 values:** Angela, Christine, Francesca, Gina, Jennifer, Lucia, Margaret, Maria, Penelope, Victoria  
**Notable name2 values:** Andrew, Arthur, Charles, Christopher, Emilio, James, Marco, Pierro, Roberto, Tomaso

---

### Dunur.husband2
**Meaning:** Records where name1 is the husband of name2 (second marriage).  
**Synonyms:** spouse (male, secondary), remarried_to

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The husband (second marriage) | husband_name, male_spouse |
| name2 | VARCHAR | The wife (second marriage) | wife_name, female_spouse |

**Notable name1 values:** Arthur, Charles, Emilio, James, Marco, Tomaso  
**Notable name2 values:** Angela, Gina, Jennifer, Lucia, Margaret, Victoria

---

### Dunur.wife2
**Meaning:** Records where name1 is the wife of name2 (second marriage).  
**Synonyms:** spouse (female, secondary), remarried_to

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The wife (second marriage) | wife_name, female_spouse |
| name2 | VARCHAR | The husband (second marriage) | husband_name, male_spouse |

**Notable name1 values:** Angela, Gina, Jennifer, Lucia, Margaret, Victoria  
**Notable name2 values:** Arthur, Charles, Emilio, James, Marco, Tomaso

---

### Dunur.uncle
**Meaning:** Records where name1 is the uncle of name2.  
**Synonyms:** paternal/maternal uncle, avuncular_relation

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The uncle | uncle_name |
| name2 | VARCHAR | The niece/nephew | niece_nephew_name |

**Notable name1 values:** Arthur, Charles, Emilio, Tomaso  
**Notable name2 values:** Alfonso, Charlotte, Colin, Sophia

---

### Dunur.aunt
**Meaning:** Records where name1 is the aunt of name2.  
**Synonyms:** paternal/maternal aunt, avuncular_relation (female)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The aunt | aunt_name |
| name2 | VARCHAR | The niece/nephew | niece_nephew_name |

**Notable name1 values:** Angela, Gina, Jennifer, Margaret  
**Notable name2 values:** Alfonso, Charlotte, Colin, Sophia

---

### Dunur.nephew
**Meaning:** Records where name1 is the nephew of name2.  
**Synonyms:** male_niece_nephew, avuncular_relation (reverse)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The nephew | nephew_name, male_niece_nephew |
| name2 | VARCHAR | The uncle/aunt | uncle_aunt_name |

**Notable name1 values:** Alfonso, Colin  
**Notable name2 values:** Angela, Arthur, Charles, Emilio, Gina, Jennifer, Margaret, Tomaso

---

### Dunur.niece
**Meaning:** Records where name1 is the niece of name2.  
**Synonyms:** female_niece_nephew, avuncular_relation (reverse)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The niece | niece_name, female_niece_nephew |
| name2 | VARCHAR | The uncle/aunt | uncle_aunt_name |

**Notable name1 values:** Charlotte, Sophia  
**Notable name2 values:** Angela, Arthur, Charles, Emilio, Gina, Jennifer, Margaret, Tomaso

---

### Dunur.dunur
**Meaning:** Records a special relationship category between name1 and name2 (exact semantic meaning not specified in schema; may represent cousin, in-law, or other derived kinship).  
**Synonyms:** special_relation, derived_kinship, dunur_relation

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | First person in dunur relation | person_a, related_person |
| name2 | VARCHAR | Second person in dunur relation | person_b, related_person |

**Notable values:** Andrew, Christine, Christopher, Francesca, Maria, Penelope, Pierro, Roberto

---

### Dunur.target
**Meaning:** Classification dataset: pairs of individuals labeled with whether they have a dunur relationship.  
**Synonyms:** training_data, classification_labels, dunur_classification

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | First person | person_a, individual_1 |
| name2 | VARCHAR | Second person | person_b, individual_2 |
| is_dunur | BIGINT | Binary label: 1 if dunur relation exists, 0 otherwise | dunur_flag, dunur_label, classification |

---

## Join Paths

### Parent-Child Relations
```sql
-- Father-child
Dunur.father f
  JOIN Dunur.person p1 ON f.name1 = p1.name
  JOIN Dunur.person p2 ON f.name2 = p2.name

-- Mother-child
Dunur.mother m
  JOIN Dunur.person p1 ON m.name1 = p1.name
  JOIN Dunur.person p2 ON m.name2 = p2.name
```

### Sibling Relations
```sql
-- Brother-sibling
Dunur.brother b
  JOIN Dunur.person p1 ON b.name1 = p1.name
  JOIN Dunur.person p2 ON b.name2 = p2.name

-- Sister-sibling
Dunur.sister s
  JOIN Dunur.person p1 ON s.name1 = p1.name
  JOIN Dunur.person p2 ON s.name2 = p2.name
```

### Spousal Relations
```sql
-- First marriage (husband-wife)
Dunur.husband h
  JOIN Dunur.wife w ON h.name1 = w.name2 AND h.name2 = w.name1

-- Second marriage (husband2-wife2)
Dunur.husband2 h2
  JOIN Dunur.wife2 w2 ON h2.name1 = w2.name2 AND h2.name2 = w2.name1
```

### Avuncular Relations
```sql
-- Uncle-niece/nephew
Dunur.uncle u
  JOIN Dunur.person p1 ON u.name1 = p1.name
  JOIN Dunur.person p2 ON u.name2 = p2.name

-- Aunt-niece/nephew
Dunur.aunt a
  JOIN Dunur.person p1 ON a.name1 = p1.name
  JOIN Dunur.person p2 ON a.name2 = p2.name

-- Nephew-uncle/aunt
Dunur.nephew n
  JOIN Dunur.person p1 ON n.name1 = p1.name
  JOIN Dunur.person p2 ON n.name2 = p2.name

-- Niece-uncle/aunt
Dunur.niece ni
  JOIN Dunur.person p1 ON ni.name1 = p1.name
  JOIN Dunur.person p2 ON ni.name2 = p2.name
```

### Dunur Relation
```sql
Dunur.dunur d
  JOIN Dunur.person p1 ON d.name1 = p1.name
  JOIN Dunur.person p2 ON d.name2 = p2.name
```

### Target Classification
```sql
Dunur.target t
  JOIN Dunur.person p1 ON t.name1 = p1.name
  JOIN Dunur.person p2 ON t.name2 = p2.name
  LEFT JOIN Dunur.dunur d ON t.name1 = d.name1 AND t.name2 = d.name2
```

---

## Business Rules as SQL

**Rule: Identify dunur relationships**
```sql
WHERE EXISTS (SELECT 1 FROM Dunur.dunur d WHERE d.name1 = t.name1 AND d.name2 = t.name2)
```

**Rule: Identify non-dunur relationships**
```sql
WHERE NOT EXISTS (SELECT 1 FROM Dunur.dunur d WHERE d.name1 = t.name1 AND d.name2 = t.name2)
```

**Rule: Person is a father**
```sql
WHERE EXISTS (SELECT 1 FROM Dunur.father f WHERE f.name1 = p.name)
```

**Rule: Person is a mother**
```sql
WHERE EXISTS (SELECT 1 FROM Dunur.mother m WHERE m.name1 = p.name)
```

**Rule: Person is a brother**
```sql
WHERE EXISTS (SELECT 1 FROM Dunur.brother b WHERE b.name1 = p.name)
```

**Rule: Person is a sister**
```sql
WHERE EXISTS (SELECT 1 FROM Dunur.sister s WHERE s.name1 = p.name)
```

**Rule: Person is married (first marriage)**
```sql
WHERE EXISTS (SELECT 1 FROM Dunur.husband h WHERE h.name1 = p.name OR h.name2 = p.name)
   OR EXISTS (SELECT 1 FROM Dunur.wife w WHERE w.name1 = p.name OR w.name2 = p.name)
```

**Rule: Person is remarried (second marriage)**
```sql
WHERE EXISTS (SELECT 1 FROM Dunur.husband2 h2 WHERE h2.name1 = p.name OR h2.name2 = p.name)
   OR EXISTS (SELECT 1 FROM Dunur.wife2 w2 WHERE w2.name1 = p.name OR w2.name2 = p.name)
```

**Rule: Person is an uncle**
```sql
WHERE EXISTS (SELECT 1 FROM Dunur.uncle u WHERE u.name1 = p.name)
```

**Rule: Person is an aunt**
```sql
WHERE EXISTS (SELECT 1 FROM Dunur.aunt a WHERE a.name1 = p.name)
```

**Rule: Person is a nephew**
```sql