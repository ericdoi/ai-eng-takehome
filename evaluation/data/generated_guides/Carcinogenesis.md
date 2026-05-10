# Carcinogenesis Schema Reference Guide

## Schema Summary
This schema contains molecular structure data for drugs with carcinogenicity classifications, represented as atoms and their chemical bonds at varying bond orders.

---

## Join Paths

**Drug to carcinogenicity class:**
```sql
FROM Carcinogenesis.canc c
```

**Drug atoms:**
```sql
FROM Carcinogenesis.atom a
WHERE a.drug = <drug_id>
```

**Drug bonds (single order):**
```sql
FROM Carcinogenesis.sbond_1 s
WHERE s.drug = <drug_id>
```

**Drug bonds (double order):**
```sql
FROM Carcinogenesis.sbond_2 s
WHERE s.drug = <drug_id>
```

**Drug bonds (triple order):**
```sql
FROM Carcinogenesis.sbond_3 s
WHERE s.drug = <drug_id>
```

**Drug bonds (aromatic/7-order):**
```sql
FROM Carcinogenesis.sbond_7 s
WHERE s.drug = <drug_id>
```

**Atom to carcinogenicity:**
```sql
FROM Carcinogenesis.atom a
JOIN Carcinogenesis.canc c ON a.drug = c.drug_id
```

**Bond endpoints to atom properties:**
```sql
FROM Carcinogenesis.sbond_1 s
JOIN Carcinogenesis.atom a1 ON s.atomid = a1.atomid
JOIN Carcinogenesis.atom a2 ON s.atomid_2 = a2.atomid
```

---

## Table Reference

### `Carcinogenesis.canc`
Drug carcinogenicity classification.

| Column | Semantics |
|--------|-----------|
| `drug_id` | Drug identifier (e.g., `d1`, `d100`) |
| `class` | Carcinogenic class: `0` (non-carcinogenic), `1` (carcinogenic) |

---

### `Carcinogenesis.atom`
Atomic structure of drugs.

| Column | Semantics |
|--------|-----------|
| `atomid` | Unique atom identifier (e.g., `d100_1`) |
| `drug` | Parent drug identifier |
| `atomtype` | Atomic number or type code (e.g., `22`, `3`) |
| `charge` | Partial atomic charge in ranges: `a0=-inf<x<=-0_1355`, `a0=-0_1355<x<=-0_0175`, `a0=-0_0175<x<=0_0615`, `a0=0_0615<x<=0_1375`, `a0=0_1375<x<=+inf` |
| `name` | Element symbol (e.g., `c`, `h`) |

---

### `Carcinogenesis.sbond_1`
Single bonds between atoms.

| Column | Semantics |
|--------|-----------|
| `drug` | Parent drug identifier |
| `atomid` | First atom endpoint |
| `atomid_2` | Second atom endpoint |

---

### `Carcinogenesis.sbond_2`
Double bonds between atoms.

| Column | Semantics |
|--------|-----------|
| `drug` | Parent drug identifier |
| `atomid` | First atom endpoint |
| `atomid_2` | Second atom endpoint |

---

### `Carcinogenesis.sbond_3`
Triple bonds between atoms.

| Column | Semantics |
|--------|-----------|
| `drug` | Parent drug identifier |
| `atomid` | First atom endpoint |
| `atomid_2` | Second atom endpoint |

---

### `Carcinogenesis.sbond_7`
Aromatic/7-order bonds between atoms.

| Column | Semantics |
|--------|-----------|
| `drug` | Parent drug identifier |
| `atomid` | First atom endpoint |
| `atomid_2` | Second atom endpoint |

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| carcinogenic drug | `WHERE Carcinogenesis.canc.class = 1` |
| non-carcinogenic drug | `WHERE Carcinogenesis.canc.class = 0` |
| atom charge range | `Carcinogenesis.atom.charge` |
| bond order 1 | `Carcinogenesis.sbond_1` |
| bond order 2 | `Carcinogenesis.sbond_2` |
| bond order 3 | `Carcinogenesis.sbond_3` |
| aromatic bond | `Carcinogenesis.sbond_7` |
| element type | `Carcinogenesis.atom.name` |