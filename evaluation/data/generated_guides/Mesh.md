# Mesh Schema Reference Guide

## Schema Summary
The Mesh schema contains element definitions and their relationships for a finite element mesh structure, including boundary conditions (fixed, loaded, free), geometric classifications (circuits, sides), and spatial neighbor relationships.

---

## Table Reference

### Mesh.circuit
**Meaning:** Full circuit boundary elements  
**Synonyms:** full circuit, complete circuit

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** c15, c16, c17, c18, c19

---

### Mesh.circuit_hole
**Meaning:** Circuit boundary elements around holes  
**Synonyms:** hole circuit, circuit with hole

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** c20, c21, c22, c23

---

### Mesh.cont_loaded
**Meaning:** Elements with continuous loading applied  
**Synonyms:** continuously loaded, distributed load

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a10, a11, a12, a13, a14

---

### Mesh.element
**Meaning:** All mesh elements in the domain  
**Synonyms:** mesh element, node, entity

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a1, a10, a11, a12, a13

---

### Mesh.equal
**Meaning:** Element pairs with equivalent properties or constraints  
**Synonyms:** equivalent elements, paired elements, symmetric pairs

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | First element identifier | element_1, left_element |
| name2 | VARCHAR | Second element identifier | element_2, right_element |

**Notable values:** (a16, a18), (a29, a7), (a31, a9), (a33, a23), (a34, a54)

---

### Mesh.fixed
**Meaning:** Elements with fixed boundary conditions  
**Synonyms:** constrained, pinned, immobile

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a1, a10, a11, a12, a13

---

### Mesh.free
**Meaning:** Elements with free (unconstrained) boundary conditions  
**Synonyms:** unconstrained, unloaded, free boundary

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a39, a40, c11, c12, c13

---

### Mesh.half_circuit
**Meaning:** Half-circuit boundary elements  
**Synonyms:** semi-circuit, half boundary

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a36, a37, a45, a46, a47, a48, a49, a50, a51, a52, a53, b12, b17, b20, b3, b41, b42, b6, b9

---

### Mesh.half_circuit_hole
**Meaning:** Half-circuit boundary elements around holes  
**Synonyms:** semi-circuit hole, half hole boundary

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a38, a42, a43, a55, b1, b14, b22, b29, b38, b40, e10, e11, e39, e47

---

### Mesh.llong
**Meaning:** Long-length elements  
**Synonyms:** long elements, extended elements

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a1, a34, a54, b19, b39, e19, e22

---

### Mesh.long_for_hole
**Meaning:** Long-length elements adjacent to holes  
**Synonyms:** long hole elements, extended hole boundary

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** c2, e41, e79

---

### Mesh.mesh
**Meaning:** Mesh assignment with mesh number classification  
**Synonyms:** mesh classification, mesh grouping

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |
| num | VARCHAR | Mesh number/group identifier | mesh_id, mesh_group, classification |

**Notable values (num):** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12

---

### Mesh.mesh_test
**Meaning:** Test mesh elements with test mesh number  
**Synonyms:** test classification, validation mesh

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |
| num | VARCHAR | Test mesh number/group identifier | test_id, test_group, test_classification |

**Notable values (num):** 1, 2, 3, 4, 5, 8, 11, 12, 17

---

### Mesh.mesh_test_Neg
**Meaning:** Negative/excluded test mesh elements  
**Synonyms:** negative test, excluded elements, test exclusion

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |
| num | VARCHAR | Negative test mesh number | neg_test_id, exclusion_group |

**Notable values (num):** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 17

---

### Mesh.neighbour_xy
**Meaning:** Spatial neighbor relationships in XY plane  
**Synonyms:** xy neighbors, xy adjacency, xy connectivity

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | First element identifier | element_1, source |
| name2 | VARCHAR | Neighboring element identifier | element_2, target, adjacent |

**Notable values:** (a1, a44), (a10, a49), (a12, a51), (a14, a53), (a15, a38)

---

### Mesh.neighbour_yz
**Meaning:** Spatial neighbor relationships in YZ plane  
**Synonyms:** yz neighbors, yz adjacency, yz connectivity

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | First element identifier | element_1, source |
| name2 | VARCHAR | Neighboring element identifier | element_2, target, adjacent |

**Notable values:** (a24, a42), (a42, a25), (a25, a35), (a35, a40), (a40, a39)

---

### Mesh.neighbour_zx
**Meaning:** Spatial neighbor relationships in ZX plane  
**Synonyms:** zx neighbors, zx adjacency, zx connectivity

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | First element identifier | element_1, source |
| name2 | VARCHAR | Neighboring element identifier | element_2, target, adjacent |

**Notable values:** (a1, a2), (a10, a11), (a11, a12), (a12, a13), (a13, a14)

---

### Mesh.nnumber
**Meaning:** Valid mesh number enumeration  
**Synonyms:** mesh numbers, valid numbers, number list

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Numeric identifier as string | number, mesh_num, id |

**Notable values:** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 17

---

### Mesh.noload
**Meaning:** Elements with no load applied  
**Synonyms:** unloaded, no loading, load-free

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a1, a2, a23, a24, a25

---

### Mesh.notimportant
**Meaning:** Elements marked as not important for analysis  
**Synonyms:** non-critical, secondary, low-priority

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a10, a12, a14, a2, a20

---

### Mesh.one_side_fixed
**Meaning:** Elements fixed on one side only  
**Synonyms:** single-side fixed, partially fixed, one-side constraint

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a34, a35, a41, c10, c14

---

### Mesh.one_side_loaded
**Meaning:** Elements with load applied on one side only  
**Synonyms:** single-side loaded, partially loaded, one-side load

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a34, a35, a40, a41, a54, d45, d46, d47, d48, e36, e38, e59, e61

---

### Mesh.opposite
**Meaning:** Element pairs on opposite sides (symmetry pairs)  
**Synonyms:** opposite pairs, symmetric elements, opposing elements

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name1 | VARCHAR | First element identifier | element_1, left_element |
| name2 | VARCHAR | Opposite element identifier | element_2, right_element |

**Notable values:** (a11, a3), (a13, a1), (a15, a1), (a17, a1), (a19, a1)

---

### Mesh.quarter_circuit
**Meaning:** Quarter-circuit boundary elements  
**Synonyms:** quarter boundary, quarter circuit

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** e75, e76, e77, e78, e84, e85

---

### Mesh.short_for_hole
**Meaning:** Short-length elements adjacent to holes  
**Synonyms:** short hole elements, short boundary

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a16, a17, a18, a23, a33, b28, b30, b34, b35, c3, c4, e13, e96

---

### Mesh.sshort
**Meaning:** Short-length elements  
**Synonyms:** short elements, compact elements

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a11, a13, a15, a19, a22

---

### Mesh.two_side_fixed
**Meaning:** Elements fixed on two sides  
**Synonyms:** double-side fixed, fully fixed, two-side constraint

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a36, a37, a38, a42, a43

---

### Mesh.two_side_loaded
**Meaning:** Elements with load applied on two sides  
**Synonyms:** double-side loaded, fully loaded, two-side load

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** e37

---

### Mesh.usual
**Meaning:** Elements with usual/standard properties  
**Synonyms:** standard elements, typical elements, normal elements

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| name | VARCHAR | Element identifier | element_name, id |

**Notable values:** a3, a39, b11, b13, b15

---

## Join Paths

**Element to Boundary Conditions:**
```sql
Mesh.element e
LEFT JOIN Mesh.fixed f ON e.name = f.name
LEFT JOIN Mesh.free fr ON e.name = fr.name
LEFT JOIN Mesh.noload nl ON e.name = nl.name
```

**Element to Loading:**
```sql
Mesh.element e
LEFT JOIN Mesh.cont_loaded cl ON e.name = cl.name
LEFT JOIN Mesh.one_side_loaded osl ON e.name = osl.name
LEFT JOIN Mesh.two_side_loaded tsl ON e.name = tsl.name
```

**Element to Fixation:**
```sql
Mesh.element e
LEFT JOIN Mesh.one_side_fixed osf ON e.name = osf.name
LEFT JOIN Mesh.two_side_fixed tsf ON e.name = tsf.name
```

**Element to Geometry:**
```sql
Mesh.element e
LEFT JOIN Mesh.circuit c ON e.name = c.name
LEFT JOIN Mesh.circuit_hole ch ON e.name = ch.name
LEFT JOIN Mesh.half_circuit hc ON e.name = hc.name
LEFT JOIN Mesh.half_circuit_hole hch ON e.name = hch.name
LEFT JOIN Mesh.quarter_circuit qc ON e.name = qc.name
```

**Element to Size:**
```sql
Mesh.element e
LEFT JOIN Mesh.llong ll ON e.name = ll.name
LEFT JOIN Mesh.sshort ss ON e.name = ss.name
LEFT JOIN Mesh.long_for_hole lfh ON e.name = lfh.name
LEFT JOIN Mesh.short_for_hole sfh ON e.name = sfh.name
```

**Element to Mesh Classification:**
```sql
Mesh.element e
LEFT JOIN Mesh.mesh m ON e.name = m.name
LEFT JOIN Mesh.mesh_test mt ON e.name = mt.name
LEFT JOIN Mesh.mesh_test_Neg mtn ON e.name = mtn.name
```

**Element Equivalence:**
```sql
Mesh.equal eq
WHERE eq.name1 = 'element_name' OR eq.name2 = 'element_name'
```

**Element Symmetry:**
```sql
Mesh.opposite op
WHERE op.name1 = 'element_name' OR op.name2 = 'element_name'
```

**Spatial Neighbors (XY Plane):**
```sql
Mesh.neighbour_xy nxy
WHERE nxy.name1 = 'element_name' OR nxy.name2 = 'element_name'
```

**Spatial Neighbors (YZ Plane):**
```sql
Mesh.neighbour_yz nyz
WHERE nyz.name1 = 'element_name' OR nyz.name2 = 'element_name'
```

**Spatial Neighbors (ZX Plane):**
```sql
Mesh.neighbour_zx nzx
WHERE nzx.name1 = 'element_name' OR nzx.name2 = 'element_name'
```

---

## Business Rules as SQL

**Rule: Element is fixed**
```sql
WHERE name IN (SELECT name FROM Mesh.fixed)
```

**Rule: Element is free (unconstrained)**
```sql
WHERE name IN (SELECT name FROM Mesh