# Mooney_Family Schema Reference Guide

## Schema Summary
This schema contains family relationship data for the Mooney family, with tables representing kinship roles (parent, sibling, spouse, child, aunt, uncle, niece, nephew) and a master person table.

---

## Table Reference

### Mooney_Family.person
**Meaning:** Master list of all individuals in the Mooney family.  
**Synonyms:** people, individuals, family members

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Person's name | individual name, person name |

**Notable values:** alfred, alice, angela, ann, art, beatrice, bob, calvin, carl, carlos, christy, cornelia, david, deanna, elisa, eric, fannie, fred, gail, james, janet, jack, melvin, nancy, nero, nonnie, ray, umo, wendy

---

### Mooney_Family.husband / husband1–5
**Meaning:** Husband-wife relationships. name1 is the husband; name2 is the wife.  
**Synonyms:** spouse (male), married to (male perspective)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | Husband's name | male spouse |
| name2 | VARCHAR | Wife's name | female spouse |

**Notable relationships:** alfred–ann, art–alice, bob–beatrice, carl–callie, carlos–christy

---

### Mooney_Family.wife / wife1–5
**Meaning:** Wife-husband relationships. name1 is the wife; name2 is the husband.  
**Synonyms:** spouse (female), married to (female perspective)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | Wife's name | female spouse |
| name2 | VARCHAR | Husband's name | male spouse |

**Notable relationships:** alice–art, ann–alfred, beatrice–bob, callie–carl, christy–carlos

---

### Mooney_Family.father / father1–5
**Meaning:** Father-child relationships. name1 is the father; name2 is the child.  
**Synonyms:** parent (male), sire

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | Father's name | male parent |
| name2 | VARCHAR | Child's name | offspring |

**Notable relationships:** alfred–david, alfred–elisa, art–f14, art–m13, art–m15

---

### Mooney_Family.mother / mother1–5
**Meaning:** Mother-child relationships. name1 is the mother; name2 is the child.  
**Synonyms:** parent (female), dam

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | Mother's name | female parent |
| name2 | VARCHAR | Child's name | offspring |

**Notable relationships:** alice–f14, alice–m13, alice–m15, ann–david, ann–elisa

---

### Mooney_Family.son / son1–5
**Meaning:** Parent-son relationships. name1 is the parent; name2 is the son.  
**Synonyms:** male child, boy

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | Parent's name | father or mother |
| name2 | VARCHAR | Son's name | male offspring |

**Notable relationships:** art–elisa, art–eric, calvin–james, calvin–janet, david–alfred

---

### Mooney_Family.daughter / daughter1–5
**Meaning:** Parent-daughter relationships. name1 is the parent; name2 is the daughter.  
**Synonyms:** female child, girl

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | Parent's name | father or mother |
| name2 | VARCHAR | Daughter's name | female offspring |

**Notable relationships:** angela–nero, angela–nonnie, christy–james, christy–janet, cornelia–fannie

---

### Mooney_Family.brother / brother1–5
**Meaning:** Sibling relationships where name1 and name2 are brothers or name1 is a brother of name2.  
**Synonyms:** male sibling, fraternal sibling

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | First person's name | sibling 1 |
| name2 | VARCHAR | Second person's name | sibling 2 |

**Notable relationships:** art–umo, art–wendy, calvin–christy, calvin–jack, david–elisa

---

### Mooney_Family.sister / sister1–5
**Meaning:** Sibling relationships where name1 and name2 are sisters or name1 is a sister of name2.  
**Synonyms:** female sibling, sororal sibling

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | First person's name | sibling 1 |
| name2 | VARCHAR | Second person's name | sibling 2 |

**Notable relationships:** angela–ray, christy–calvin, christy–jack, cornelia–melvin, cornelia–nancy

---

### Mooney_Family.aunt / aunt1–5
**Meaning:** Aunt-niece/nephew relationships. name1 is the aunt; name2 is the niece or nephew.  
**Synonyms:** paternal/maternal aunt, father's/mother's sister

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | Aunt's name | female relative (parent's sister) |
| name2 | VARCHAR | Niece or nephew's name | child of aunt's sibling |

**Notable relationships:** alice–f12, alice–m11, angela–m29, christy–f23, christy–f25

---

### Mooney_Family.uncle / uncle1–5
**Meaning:** Uncle-niece/nephew relationships. name1 is the uncle; name2 is the niece or nephew.  
**Synonyms:** paternal/maternal uncle, father's/mother's brother

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | Uncle's name | male relative (parent's brother) |
| name2 | VARCHAR | Niece or nephew's name | child of uncle's sibling |

**Notable relationships:** art–f12, art–m11, calvin–f23, calvin–f25, calvin–f26

---

### Mooney_Family.niece / niece1–5
**Meaning:** Niece-aunt/uncle relationships. name1 is the aunt or uncle; name2 is the niece.  
**Synonyms:** female niece, daughter of sibling

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | Aunt or uncle's name | parent's sibling |
| name2 | VARCHAR | Niece's name | female child of sibling |

**Notable relationships:** angela–james, angela–janet, christy–nero, christy–nonnie, cornelia–elisa

---

### Mooney_Family.nephew / nephew1–5
**Meaning:** Nephew-aunt/uncle relationships. name1 is the aunt or uncle; name2 is the nephew.  
**Synonyms:** male nephew, son of sibling

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | Aunt or uncle's name | parent's sibling |
| name2 | VARCHAR | Nephew's name | male child of sibling |

**Notable relationships:** art–david, art–deanna, art–fannie, art–fred, art–gail

---

## Join Paths

### Spouse relationships
```sql
-- Husband to wife
husband.name1 = wife.name2 AND husband.name2 = wife.name1

-- Wife to husband
wife.name1 = husband.name2 AND wife.name2 = husband.name1
```

### Parent-child relationships
```sql
-- Father to child (son or daughter)
father.name1 = son.name1 AND father.name2 = son.name2
father.name1 = daughter.name1 AND father.name2 = daughter.name2

-- Mother to child (son or daughter)
mother.name1 = son.name1 AND mother.name2 = son.name2
mother.name1 = daughter.name1 AND mother.name2 = daughter.name2
```

### Sibling relationships
```sql
-- Brother to sibling
brother.name1 = sister.name1 OR brother.name2 = sister.name2

-- Sister to sibling
sister.name1 = brother.name1 OR sister.name2 = brother.name2
```

### Extended family relationships
```sql
-- Aunt to niece/nephew
aunt.name1 = niece.name1 AND aunt.name2 = niece.name2
aunt.name1 = nephew.name1 AND aunt.name2 = nephew.name2

-- Uncle to niece/nephew
uncle.name1 = niece.name1 AND uncle.name2 = niece.name2
uncle.name1 = nephew.name1 AND uncle.name2 = nephew.name2
```

### Transitive relationships (via person table)
```sql
-- All people related to a specific person
person.name = 'alfred'
```

---

## Business Rules as SQL

**Rule: Identify all spouses of a person**
```sql
WHERE husband.name1 = 'alfred' OR wife.name1 = 'alfred'
```

**Rule: Identify all children of a person**
```sql
WHERE son.name1 = 'alfred' OR daughter.name1 = 'alfred'
```

**Rule: Identify all parents of a person**
```sql
WHERE father.name2 = 'david' OR mother.name2 = 'david'
```

**Rule: Identify all siblings of a person**
```sql
WHERE brother.name1 = 'art' OR brother.name2 = 'art' 
   OR sister.name1 = 'art' OR sister.name2 = 'art'
```

**Rule: Identify all aunts of a person**
```sql
WHERE aunt.name2 = 'f12'
```

**Rule: Identify all uncles of a person**
```sql
WHERE uncle.name2 = 'f12'
```

**Rule: Identify all nieces of a person**
```sql
WHERE niece.name1 = 'art'
```

**Rule: Identify all nephews of a person**
```sql
WHERE nephew.name1 = 'art'
```

---

## Synonym Glossary

| Common Term | Schema Reference |
|-------------|------------------|
| spouse | `husband` or `wife` table |
| married to | `husband.name1 = X AND husband.name2 = Y` |
| husband of | `husband.name2 = X` |
| wife of | `wife.name2 = X` |
| parent of | `father.name2 = X` or `mother.name2 = X` |
| father of | `father.name2 = X` |
| mother of | `mother.name2 = X` |
| child of | `son.name1 = X` or `daughter.name1 = X` |
| son of | `son.name1 = X` |
| daughter of | `daughter.name1 = X` |
| sibling of | `brother` or `sister` table |
| brother of | `brother.name1 = X` or `brother.name2 = X` |
| sister of | `sister.name1 = X` or `sister.name2 = X` |
| aunt of | `aunt.name2 = X` |
| uncle of | `uncle.name2 = X` |
| niece of | `niece.name1 = X` |
| nephew of | `nephew.name1 = X` |
| family member | `person.name` |
| all people | `SELECT DISTINCT name FROM person` |