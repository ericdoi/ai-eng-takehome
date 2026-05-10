# Mutagenesis Schema Reference Guide

## Schema Summary
This schema contains molecular structures, atomic composition, bonding topology, and mutagenic activity labels for pharmaceutical toxicology research.

---

## Join Paths

**Molecule to atoms:**
```sql
FROM mutagenesis.molecule m
JOIN mutagenesis.atom a ON m.molecule_id = a.molecule_id
```

**Molecule to bonds (via atoms):**
```sql
FROM mutagenesis.molecule m
JOIN mutagenesis.atom a1 ON m.molecule_id = a1.molecule_id
JOIN mutagenesis.bond b ON (a1.atom_id = b.atom1_id OR a1.atom_id = b.atom2_id)
```

**Complete structural query (atoms + bonds):**
```sql
FROM mutagenesis.molecule m
JOIN mutagenesis.atom a ON m.molecule_id = a.molecule_id
LEFT JOIN mutagenesis.bond b ON (a.atom_id = b.atom1_id OR a.atom_id = b.atom2_id)
```

---

## Business Rules as SQL

**Rule: Only molecules with complete bond information in structural analysis**
```sql
WHERE m.molecule_id IN (
  SELECT DISTINCT a1.molecule_id 
  FROM mutagenesis.atom a1
  JOIN mutagenesis.atom a2 ON a1.molecule_id = a2.molecule_id
  JOIN mutagenesis.bond b ON (a1.atom_id = b.atom1_id AND a2.atom_id = b.atom2_id)
)
```

**Rule: Exclude molecules without activity label (untested)**
```sql
WHERE m.mutagenic IS NOT NULL
```

**Rule: Mutagenic activity is binary positive**
```sql
WHERE m.mutagenic = 'yes'
```

**Rule: Bond type classification**
- Single bond: `WHERE b.type = 1`
- Double bond: `WHERE b.type = 2`
- Triple bond: `WHERE b.type = 3`
- Aromatic bond: `WHERE b.type = 4`

**Rule: Charged atoms (electrostatic flag)**
```sql
WHERE a.charge <> 0
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| mutagenic compound | `WHERE mutagenesis.molecule.mutagenic = 'yes'` |
| non-mutagenic compound | `WHERE mutagenesis.molecule.mutagenic = 'no'` |
| untested molecule | `WHERE mutagenesis.molecule.mutagenic IS NULL` |
| atom element type | `mutagenesis.atom.element` (values: b, c, f, h, i, n, o) |
| bond connectivity | `mutagenesis.bond.atom1_id`, `mutagenesis.bond.atom2_id` |
| lipophilicity | `mutagenesis.molecule.logp` |
| LUMO energy | `mutagenesis.molecule.lumo` |
| structural indicator 1 | `mutagenesis.molecule.ind1` |
| structural indicator A | `mutagenesis.molecule.inda` |

---

## Table Reference

### `mutagenesis.atom`
**Meaning:** Individual atoms in molecular structures.

| Column | Semantics |
|--------|-----------|
| `atom_id` | Unique atom identifier; format `{molecule_id}_{sequence}` |
| `molecule_id` | Foreign key to `mutagenesis.molecule` |
| `element` | Periodic table element; enumerated: **b, c, f, h, i, n, o** |
| `type` | Atom type code (integer); standardize to periodic table symbols in output |
| `charge` | Partial charge (double); non-zero indicates charged atom for electrostatic calculations |

---

### `mutagenesis.bond`
**Meaning:** Chemical bonds connecting atoms within molecules.

| Column | Semantics |
|--------|-----------|
| `atom1_id` | First atom in bond; foreign key to `mutagenesis.atom.atom_id` |
| `atom2_id` | Second atom in bond; foreign key to `mutagenesis.atom.atom_id` |
| `type` | Bond order; enumerated: **1** (single), **2** (double), **3** (triple), **4** (aromatic) |

---

### `mutagenesis.molecule`
**Meaning:** Molecular compounds with structural properties and mutagenic activity labels.

| Column | Semantics |
|--------|-----------|
| `molecule_id` | Unique molecule identifier (anonymized compound ID) |
| `ind1` | Structural indicator 1 (binary: 0 or 1) |
| `inda` | Structural indicator A (binary: 0 or 1) |
| `logp` | Partition coefficient (lipophilicity); double precision |
| `lumo` | Lowest unoccupied molecular orbital energy; double precision |
| `mutagenic` | Activity label; enumerated: **yes** (mutagenic), **no** (non-mutagenic), **NULL** (untested) |