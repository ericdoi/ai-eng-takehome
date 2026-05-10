# Toxicology Schema Reference Guide

## Schema Summary
This schema stores molecular structures for toxicology research, representing atoms, bonds, and connectivity within molecules, each labeled with mutagenic activity classification.

---

## Join Paths

**Molecule to its atoms:**
```sql
FROM Toxicology.molecule m
JOIN Toxicology.atom a ON m.molecule_id = a.molecule_id
```

**Molecule to its bonds:**
```sql
FROM Toxicology.molecule m
JOIN Toxicology.bond b ON m.molecule_id = b.molecule_id
```

**Complete molecular structure (atoms + bonds + connectivity):**
```sql
FROM Toxicology.molecule m
JOIN Toxicology.atom a ON m.molecule_id = a.molecule_id
JOIN Toxicology.connected c ON a.atom_id = c.atom_id
JOIN Toxicology.bond b ON c.bond_id = b.bond_id
```

**Bonded atom pairs:**
```sql
FROM Toxicology.connected c
JOIN Toxicology.atom a1 ON c.atom_id = a1.atom_id
JOIN Toxicology.atom a2 ON c.atom_id2 = a2.atom_id
JOIN Toxicology.bond b ON c.bond_id = b.bond_id
```

---

## Business Rules as SQL

**Rule: Only molecules with complete bond information in structural analysis**
```sql
WHERE m.molecule_id IN (
  SELECT molecule_id FROM Toxicology.bond
  GROUP BY molecule_id HAVING COUNT(*) > 0
)
```

**Rule: Classify molecules without activity label as "untested"**
```sql
SELECT molecule_id, COALESCE(label, 'untested') AS activity_status
FROM Toxicology.molecule
```

**Rule: Bond type mapping (schema stores -, =, # symbols)**
```sql
-- Single bond: '-'
-- Double bond: '='
-- Triple bond: '#'
WHERE Toxicology.bond.bond_type IN ('-', '=', '#')
```

**Rule: Activity classification (binary mutagenic)**
```sql
-- Positive (mutagenic): label = '+'
-- Negative (non-mutagenic): label = '-'
WHERE Toxicology.molecule.label IN ('+', '-')
```

**Rule: Exclude untested molecules from model training**
```sql
WHERE Toxicology.molecule.label IS NOT NULL
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| mutagenic activity | `Toxicology.molecule.label` ('+' = positive, '-' = negative) |
| chemical element | `Toxicology.atom.element` |
| bond connectivity | `Toxicology.connected` table |
| bond order | `Toxicology.bond.bond_type` ('-' = single, '=' = double, '#' = triple) |
| molecular structure | joined `Toxicology.atom` + `Toxicology.bond` + `Toxicology.connected` |
| untested compound | `Toxicology.molecule.label IS NULL` |

---

## Table Reference

### `Toxicology.molecule`
**Meaning:** Unique chemical compounds with mutagenic activity labels.

| Column | Notes |
|--------|-------|
| `molecule_id` | Primary identifier (e.g., TR000, TR001) |
| `label` | Activity classification: `'+'` (mutagenic), `'-'` (non-mutagenic), or NULL (untested). Binary classification only. |

---

### `Toxicology.atom`
**Meaning:** Individual atoms within molecules; represents nodes in molecular graph.

| Column | Notes |
|--------|-------|
| `atom_id` | Unique atom identifier within molecule (e.g., TR000_1) |
| `molecule_id` | Foreign key to `Toxicology.molecule` |
| `element` | Periodic table symbol, lowercase (e.g., 'cl', 'c', 'h', 'n', 'o'). Standardize to uppercase for analysis. Hydrogen may be implicit. |

---

### `Toxicology.bond`
**Meaning:** Chemical bonds between atoms; represents edges in molecular graph.

| Column | Notes |
|--------|-------|
| `bond_id` | Unique bond identifier (e.g., TR000_1_2) |
| `molecule_id` | Foreign key to `Toxicology.molecule` |
| `bond_type` | Bond order: `'-'` (single), `'='` (double), `'#'` (triple). No aromatic notation in current schema. |

---

### `Toxicology.connected`
**Meaning:** Atom-pair connectivity; maps which atoms are bonded via which bonds. Bidirectional (both directions stored).

| Column | Notes |
|--------|-------|
| `atom_id` | First atom in bond pair |
| `atom_id2` | Second atom in bond pair |
| `bond_id` | Foreign key to `Toxicology.bond` linking this pair |

**Note:** Each bond appears twice in this table (once for each direction). For unique bond count, use `Toxicology.bond` directly.