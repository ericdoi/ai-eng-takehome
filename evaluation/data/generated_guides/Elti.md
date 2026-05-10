# Elti Schema Reference Guide

## Schema Summary
This schema models family relationships (kinship) among a set of persons, recording parent-child, sibling, spousal, and cousin-like (elti) connections.

## Join Paths

**Parent-child relationships:**
```sql
FROM Elti.father f
JOIN Elti.person p ON f.name2 = p.name
```

```sql
FROM Elti.mother m
JOIN Elti.person p ON m.name2 = p.name
```

**Spousal relationships:**
```sql
FROM Elti.husband h
JOIN Elti.wife w ON h.name1 = w.name2 AND h.name2 = w.name1
```

**Sibling relationships:**
```sql
FROM Elti.brother b
JOIN Elti.sister s ON b.name1 = s.name2 AND b.name2 = s.name1
```

**Children of a person:**
```sql
FROM Elti.son s
WHERE s.name1 = ?
UNION ALL
FROM Elti.daughter d
WHERE d.name1 = ?
```

**Elti (cousin-like) relationships:**
```sql
FROM Elti.elti e1
JOIN Elti.elti e2 ON e1.name1 = e2.name2 AND e1.name2 = e2.name1
```

## Table Reference

### `Elti.person`
All individuals in the dataset.
- **name**: unique person identifier

### `Elti.father`
Father-child relationships. `name1` is father, `name2` is child.
- **name1** values: ali1, gunay, huseyin, ismail, levent, mehmet1, mehmet2, muhammer, muhittin, recep, sadullah, yildirim, yusuf1, yusuf2

### `Elti.mother`
Mother-child relationships. `name1` is mother, `name2` is child.
- **name1** values: ayse, ayten, bedriye, cemile, dilber, fatma, firdevs, kubra, mediha1, mediha2, nalan, neriman, nesrin, sibel

### `Elti.son`
Father-son relationships. `name1` is father, `name2` is son.
- **name1** values: ali1, ali2, alp, anil, batuhan, cagdas, erdem, halis, ismail, mehmet1, mete, murat1, murat2, sadullah, yavuz, yildirim, yusuf2, yusuf3

### `Elti.daughter`
Father-daughter relationships. `name1` is father, `name2` is daughter.
- **name1** values: dilber, dilek, esra, fatma, firdevs, kubra, mediha2, melis, neriman, nesrin, nida, secil, sevcan, zeynep

### `Elti.brother`
Brother-sibling relationships. `name1` is brother, `name2` is sibling (any gender).
- **name1** values: ali1, ali2, alp, anil, batuhan, cagdas, erdem, halis, ismail, mehmet1, mete, murat1, murat2, sadullah, yildirim, yusuf2, yusuf3

### `Elti.sister`
Sister-sibling relationships. `name1` is sister, `name2` is sibling (any gender).
- **name1** values: dilber, dilek, fatma, firdevs, kubra, mediha2, melis, neriman, nesrin, nida, secil, sevcan, zeynep
- **name2** values: ali1, ali2, anil, cagdas, dilek, erdem, fatma, ismail, kubra, mehmet1, mete, murat1, neriman, nesrin, sadullah, yildirim, yusuf2, yusuf3

### `Elti.husband`
Spousal relationships. `name1` is husband, `name2` is wife.
- **name1** values: ali1, gunay, huseyin, ismail, levent, mehmet1, mehmet2, muhammer, muhittin, recep, sadullah, yildirim, yusuf1, yusuf2
- **name2** values: ayse, ayten, bedriye, cemile, dilber, fatma, firdevs, kubra, mediha1, mediha2, nalan, neriman, nesrin, sibel

### `Elti.wife`
Spousal relationships (inverse of husband). `name1` is wife, `name2` is husband.
- **name1** values: ayse, ayten, bedriye, cemile, dilber, fatma, firdevs, kubra, mediha1, mediha2, nalan, neriman, nesrin, sibel
- **name2** values: ali1, gunay, huseyin, ismail, levent, mehmet1, mehmet2, muhammer, muhittin, recep, sadullah, yildirim, yusuf1, yusuf2

### `Elti.elti`
Cousin-like or extended kinship relationships. `name1` and `name2` are elti to each other (symmetric).
- **name1** values: ayse, ayten, bedriye, cemile, nalan
- **name2** values: ayse, ayten, bedriye, cemile, nalan

### `Elti.target`
Classification dataset for relationship prediction.
- **name1**: first person
- **name2**: second person
- **is_elti**: binary label (0 or 1) indicating whether name1 and name2 are elti