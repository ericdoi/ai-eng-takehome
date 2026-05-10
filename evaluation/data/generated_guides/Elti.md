# Elti Schema Reference Guide

## Schema Summary
The Elti schema models family relationships (kinship) among a group of individuals, recording connections such as parent-child, sibling, spousal, and extended family ties.

---

## Table Reference

### Elti.brother
**Meaning:** Sibling relationships where name1 is a brother of name2.  
**Synonyms:** male sibling, fraternal relationship

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The brother (male sibling) | brother, male sibling |
| name2 | VARCHAR | The person who has name1 as a brother | sibling, relative |

**Notable values (name1):** ali1, ali2, alp, anil, batuhan, cagdas, erdem, halis, ismail, mehmet1, mete, murat1, murat2, sadullah, yildirim, yusuf2, yusuf3

---

### Elti.daughter
**Meaning:** Parent-child relationships where name1 is a daughter of name2.  
**Synonyms:** female child, girl

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The daughter (female child) | daughter, female child |
| name2 | VARCHAR | The parent of name1 | parent, father, mother |

**Notable values (name1):** dilber, dilek, esra, fatma, firdevs, kubra, mediha2, melis, neriman, nesrin, nida, secil, sevcan, zeynep

---

### Elti.elti
**Meaning:** Extended family relationships (aunts/uncles or cousins); specifically non-nuclear family connections.  
**Synonyms:** extended family, aunt/uncle relationship, cousin relationship

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | First person in the elti relationship | person, relative |
| name2 | VARCHAR | Second person in the elti relationship | person, relative |

**Notable values:** ayse, ayten, bedriye, cemile, nalan

---

### Elti.father
**Meaning:** Parent-child relationships where name1 is the father of name2.  
**Synonyms:** paternal parent, male parent

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The father (male parent) | father, male parent |
| name2 | VARCHAR | The child of name1 | child, son, daughter |

**Notable values (name1):** ali1, gunay, huseyin, ismail, levent, mehmet1, mehmet2, muhammer, muhittin, recep, sadullah, yildirim, yusuf1, yusuf2

---

### Elti.husband
**Meaning:** Spousal relationships where name1 is the husband of name2.  
**Synonyms:** male spouse, married to

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The husband (male spouse) | husband, male spouse |
| name2 | VARCHAR | The wife of name1 | wife, female spouse |

**Notable values (name1):** ali1, gunay, huseyin, ismail, levent, mehmet1, mehmet2, muhammer, muhittin, recep, sadullah, yildirim, yusuf1, yusuf2  
**Notable values (name2):** ayse, ayten, bedriye, cemile, dilber, fatma, firdevs, kubra, mediha1, mediha2, nalan, neriman, nesrin, sibel

---

### Elti.mother
**Meaning:** Parent-child relationships where name1 is the mother of name2.  
**Synonyms:** maternal parent, female parent

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The mother (female parent) | mother, female parent |
| name2 | VARCHAR | The child of name1 | child, son, daughter |

**Notable values (name1):** ayse, ayten, bedriye, cemile, dilber, fatma, firdevs, kubra, mediha1, mediha2, nalan, neriman, nesrin, sibel

---

### Elti.person
**Meaning:** Master list of all individuals in the family network.  
**Synonyms:** individual, member, person record

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Unique identifier for a person | person name, individual |

---

### Elti.sister
**Meaning:** Sibling relationships where name1 is a sister of name2.  
**Synonyms:** female sibling, sisterly relationship

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The sister (female sibling) | sister, female sibling |
| name2 | VARCHAR | The person who has name1 as a sister | sibling, relative |

**Notable values (name1):** dilber, dilek, fatma, firdevs, kubra, mediha2, melis, neriman, nesrin, nida, secil, sevcan, zeynep  
**Notable values (name2):** ali1, ali2, anil, cagdas, dilek, erdem, fatma, ismail, kubra, mehmet1, mete, murat1, neriman, nesrin, sadullah, yildirim, yusuf2, yusuf3

---

### Elti.son
**Meaning:** Parent-child relationships where name1 is the father of name2 (male child).  
**Synonyms:** male child, boy

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The father (male parent) | father, male parent |
| name2 | VARCHAR | The son (male child) | son, male child |

**Notable values (name1):** ali1, ali2, alp, anil, batuhan, cagdas, erdem, halis, ismail, mehmet1, mete, murat1, murat2, sadullah, yavuz, yildirim, yusuf2, yusuf3

---

### Elti.target
**Meaning:** Classification dataset indicating whether pairs of individuals have an elti relationship.  
**Synonyms:** training data, relationship classification, label set

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | First person in the pair | person, individual |
| name2 | VARCHAR | Second person in the pair | person, individual |
| is_elti | BIGINT | Binary indicator: 1 if name1 and name2 have an elti relationship, 0 otherwise | label, classification, relationship flag |

---

### Elti.wife
**Meaning:** Spousal relationships where name1 is the wife of name2.  
**Synonyms:** female spouse, married to

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | The wife (female spouse) | wife, female spouse |
| name2 | VARCHAR | The husband of name1 | husband, male spouse |

**Notable values (name1):** ayse, ayten, bedriye, cemile, dilber, fatma, firdevs, kubra, mediha1, mediha2, nalan, neriman, nesrin, sibel  
**Notable values (name2):** ali1, gunay, huseyin, ismail, levent, mehmet1, mehmet2, muhammer, muhittin, recep, sadullah, yildirim, yusuf1, yusuf2

---

## Join Paths

### Parent-Child Relationships
```sql
-- Father-child
Elti.father f JOIN Elti.person p ON f.name2 = p.name

-- Mother-child
Elti.mother m JOIN Elti.person p ON m.name2 = p.name

-- Son (father-son)
Elti.son s JOIN Elti.person p ON s.name2 = p.name

-- Daughter (parent-daughter)
Elti.daughter d JOIN Elti.person p ON d.name2 = p.name
```

### Sibling Relationships
```sql
-- Brother-sibling
Elti.brother b JOIN Elti.person p ON b.name2 = p.name

-- Sister-sibling
Elti.sister s JOIN Elti.person p ON s.name2 = p.name
```

### Spousal Relationships
```sql
-- Husband-wife
Elti.husband h JOIN Elti.wife w ON h.name1 = w.name2 AND h.name2 = w.name1

-- Wife-husband
Elti.wife w JOIN Elti.husband h ON w.name2 = h.name1 AND w.name1 = h.name2
```

### Extended Family
```sql
-- Elti relationships
Elti.elti e JOIN Elti.person p ON e.name1 = p.name OR e.name2 = p.name
```

### All Relationships via Person
```sql
-- Any relationship involving a person
Elti.person p 
LEFT JOIN Elti.father f ON p.name = f.name1 OR p.name = f.name2
LEFT JOIN Elti.mother m ON p.name = m.name1 OR p.name = m.name2
LEFT JOIN Elti.son s ON p.name = s.name1 OR p.name = s.name2
LEFT JOIN Elti.daughter d ON p.name = d.name1 OR p.name = d.name2
LEFT JOIN Elti.brother b ON p.name = b.name1 OR p.name = b.name2
LEFT JOIN Elti.sister si ON p.name = si.name1 OR p.name = si.name2
LEFT JOIN Elti.husband h ON p.name = h.name1 OR p.name = h.name2
LEFT JOIN Elti.wife w ON p.name = w.name1 OR p.name = w.name2
LEFT JOIN Elti.elti e ON p.name = e.name1 OR p.name = e.name2
```

---

## Business Rules as SQL

**Rule: Identify elti relationships**
```sql
WHERE is_elti = 1
```

**Rule: Identify non-elti relationships**
```sql
WHERE is_elti = 0
```

**Rule: Find all children of a parent**
```sql
SELECT name2 FROM Elti.father WHERE name1 = 'parent_name'
UNION
SELECT name2 FROM Elti.mother WHERE name1 = 'parent_name'
```

**Rule: Find all parents of a child**
```sql
SELECT name1 FROM Elti.father WHERE name2 = 'child_name'
UNION
SELECT name1 FROM Elti.mother WHERE name2 = 'child_name'
```

**Rule: Find all siblings of a person**
```sql
SELECT name2 FROM Elti.brother WHERE name1 = 'person_name'
UNION
SELECT name2 FROM Elti.sister WHERE name1 = 'person_name'
```

**Rule: Find spouse of a person**
```sql
SELECT name2 FROM Elti.husband WHERE name1 = 'person_name'
UNION
SELECT name2 FROM Elti.wife WHERE name1 = 'person_name'
```

---

## Synonym Glossary

| Common Term | Schema Reference |
|-------------|------------------|
| brother | `Elti.brother.name1` |
| sister | `Elti.sister.name1` |
| father | `Elti.father.name1` |
| mother | `Elti.mother.name1` |
| son | `Elti.son.name2` |
| daughter | `Elti.daughter.name1` |
| husband | `Elti.husband.name1` |
| wife | `Elti.wife.name1` |
| child | `Elti.father.name2` or `Elti.mother.name2` |
| parent | `Elti.father.name1` or `Elti.mother.name1` |
| sibling | `Elti.brother.name2` or `Elti.sister.name2` |
| spouse | `Elti.husband.name2` or `Elti.wife.name2` |
| extended family | `Elti.elti` |
| elti relationship | `Elti.target WHERE is_elti = 1` |
| non-elti relationship | `Elti.target WHERE is_elti = 0` |
| all people | `Elti.person.name` |