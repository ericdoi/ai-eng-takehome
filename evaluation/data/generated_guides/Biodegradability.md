# Biodegradability Schema Reference Guide

## Schema Summary
This schema represents molecular structures and their biodegradability properties, storing atoms, bonds, functional groups, and activity measurements for chemical compounds.

## Join Paths

**Molecule to its atoms:**
```sql
FROM Biodegradability.molecule m
JOIN Biodegradability.atom a ON m.molecule_id = a.molecule_id
```

**Atoms connected by bonds:**
```sql
FROM Biodegradability.atom a1
JOIN Biodegradability.bond b ON a1.atom_id = b.atom_id
JOIN Biodegradability.atom a2 ON b.atom_id2 = a2.atom_id
```

**Atoms to their functional groups:**
```sql
FROM Biodegradability.atom a
JOIN Biodegradability.gmember gm ON a.atom_id = gm.atom_id
JOIN Biodegradability.group g ON gm.group_id = g.group_id
```

**Complete molecular composition:**
```sql
FROM Biodegradability.molecule m
JOIN Biodegradability.atom a ON m.molecule_id = a.molecule_id
JOIN Biodegradability.gmember gm ON a.atom_id = gm.atom_id
JOIN Biodegradability.group g ON gm.group_id = g.group_id
```

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| biodegradability score | `Biodegradability.molecule.activity` |
| lipophilicity | `Biodegradability.molecule.logp` |
| molecular weight | `Biodegradability.molecule.mweight` |
| atom element type | `Biodegradability.atom.type` |
| bond order | `Biodegradability.bond.type` |
| functional group | `Biodegradability.group.type` |

## Table Reference

### `Biodegradability.molecule`
Chemical compounds with measured properties.

| Column | Semantics |
|--------|-----------|
| `activity` | Biodegradability activity score (DOUBLE) |
| `logp` | Partition coefficient / lipophilicity (DOUBLE) |
| `mweight` | Molecular weight in g/mol (DOUBLE) |

### `Biodegradability.atom`
Individual atoms within molecules.

| Column | Semantics |
|--------|-----------|
| `type` | Element type: `br`, `c`, `ca`, `cl`, `f`, `h`, `i`, `n`, `o`, `p`, `pb`, `s` |

### `Biodegradability.bond`
Chemical bonds connecting atoms.

| Column | Semantics |
|--------|-----------|
| `type` | Bond order: `1` (single), `2` (double), `3` (triple), `7` (aromatic) |

### `Biodegradability.group`
Functional group classifications.

| Column | Semantics |
|--------|-----------|
| `type` | Functional group name: `sulfo`, `nitro`, `methyl`, `c2n`, etc. |

### `Biodegradability.gmember`
Junction table linking atoms to functional groups.