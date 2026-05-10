# Mesh Schema Reference Guide

## Schema Summary
This schema models a finite element mesh structure with element classifications, boundary conditions (fixed/loaded/free), geometric relationships (neighbors, opposites, equivalences), and circuit topology.

---

## Join Paths

**Elements with their boundary conditions:**
```sql
SELECT e.name, f.name AS fixed_status, fr.name AS free_status, l.name AS loaded_status
FROM Mesh.element e
LEFT JOIN Mesh.fixed f ON e.name = f.name
LEFT JOIN Mesh.free fr ON e.name = fr.name
LEFT JOIN Mesh.cont_loaded l ON e.name = l.name
```

**Elements with geometric neighbors (all axes):**
```sql
SELECT e.name, nxy.name2 AS neighbor_xy, nyz.name2 AS neighbor_yz, nzx.name2 AS neighbor_zx
FROM Mesh.element e
LEFT JOIN Mesh.neighbour_xy nxy ON e.name = nxy.name1
LEFT JOIN Mesh.neighbour_yz nyz ON e.name = nyz.name1
LEFT JOIN Mesh.neighbour_zx nzx ON e.name = nzx.name1
```

**Elements with equivalent pairs:**
```sql
SELECT e.name, eq.name2 AS equivalent_element
FROM Mesh.element e
LEFT JOIN Mesh.equal eq ON e.name = eq.name1
```

**Elements with opposite pairs:**
```sql
SELECT e.name, opp.name2 AS opposite_element
FROM Mesh.element e
LEFT JOIN Mesh.opposite opp ON e.name = opp.name1
```

**Mesh assignments:**
```sql
SELECT e.name, m.num AS mesh_number
FROM Mesh.element e
LEFT JOIN Mesh.mesh m ON e.name = m.name
```

---

## Table Reference

### `Mesh.element`
All mesh elements in the domain.
- **name**: element identifier (e.g., `a1`, `a10`, `b2`, `c15`, `e75`)

### `Mesh.fixed`
Elements with fixed boundary conditions.
- **name**: element identifier

### `Mesh.free`
Elements with free (unconstrained) boundary conditions.
- **name**: element identifier

### `Mesh.cont_loaded`
Elements with continuous loading applied.
- **name**: element identifier

### `Mesh.noload`
Elements with no load applied.
- **name**: element identifier

### `Mesh.one_side_fixed`
Elements fixed on exactly one side/face.
- **name**: element identifier

### `Mesh.two_side_fixed`
Elements fixed on two sides/faces.
- **name**: element identifier

### `Mesh.one_side_loaded`
Elements with loading on exactly one side/face.
- **name**: element identifier

### `Mesh.two_side_loaded`
Elements with loading on two sides/faces.
- **name**: element identifier

### `Mesh.equal`
Pairs of equivalent/symmetric elements.
- **name1, name2**: paired element identifiers

### `Mesh.opposite`
Pairs of opposite elements (e.g., across a domain).
- **name1, name2**: paired element identifiers

### `Mesh.neighbour_xy`
Adjacency relationships in the XY plane.
- **name1, name2**: adjacent element identifiers

### `Mesh.neighbour_yz`
Adjacency relationships in the YZ plane.
- **name1, name2**: adjacent element identifiers

### `Mesh.neighbour_zx`
Adjacency relationships in the ZX plane.
- **name1, name2**: adjacent element identifiers

### `Mesh.circuit`
Circuit boundary elements (full perimeter).
- **name**: element identifier; values: `c15`, `c16`, `c17`, `c18`, `c19`

### `Mesh.half_circuit`
Half-circuit boundary elements.
- **name**: element identifier; values: `a36`, `a37`, `a45`, `a46`, `a47`, `a48`, `a49`, `a50`, `a51`, `a52`, `a53`, `b12`, `b17`, `b20`, `b3`, `b41`, `b42`, `b6`, `b9`

### `Mesh.quarter_circuit`
Quarter-circuit boundary elements.
- **name**: element identifier; values: `e75`, `e76`, `e77`, `e78`, `e84`, `e85`

### `Mesh.circuit_hole`
Circuit boundary elements around holes.
- **name**: element identifier; values: `c20`, `c21`, `c22`, `c23`

### `Mesh.half_circuit_hole`
Half-circuit boundary elements around holes.
- **name**: element identifier; values: `a38`, `a42`, `a43`, `a55`, `b1`, `b14`, `b22`, `b29`, `b38`, `b40`, `e10`, `e11`, `e39`, `e47`

### `Mesh.llong`
Long edge elements.
- **name**: element identifier; values: `a1`, `a34`, `a54`, `b19`, `b39`, `e19`, `e22`

### `Mesh.sshort`
Short edge elements.
- **name**: element identifier; values: `a11`, `a13`, `a15`, `a19`, `a22`

### `Mesh.long_for_hole`
Long edge elements adjacent to holes.
- **name**: element identifier; values: `c2`, `e41`, `e79`

### `Mesh.short_for_hole`
Short edge elements adjacent to holes.
- **name**: element identifier; values: `a16`, `a17`, `a18`, `a23`, `a33`, `b28`, `b30`, `b34`, `b35`, `c3`, `c4`, `e13`, `e96`

### `Mesh.usual`
Standard/typical elements (not on boundaries or special regions).
- **name**: element identifier

### `Mesh.notimportant`
Elements marked as non-critical for analysis.
- **name**: element identifier

### `Mesh.mesh`
Mesh assignment mapping.
- **name**: element identifier
- **num**: mesh group number; values: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `12`

### `Mesh.mesh_test`
Test mesh assignment.
- **name**: element identifier
- **num**: test mesh group number; values: `1`, `2`, `3`, `4`, `5`, `8`, `11`, `12`, `17`

### `Mesh.mesh_test_Neg`
Negative/control test mesh assignment.
- **name**: element identifier
- **num**: test mesh group number; values: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `17`

### `Mesh.nnumber`
Valid mesh number identifiers.
- **name**: numeric identifier; values: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `17`