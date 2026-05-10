# SQL Reference Guide: Mutagenesis Schema

## 1. Schema Summary

The `mutagenesis` schema contains molecular structure and toxicology data for pharmaceutical compounds, including atomic composition, chemical bonds, and mutagenic activity classifications.

---

## 2. Table Reference

### Table: `mutagenesis.molecule`
**Meaning:** Individual chemical compounds tested for mutagenic activity.  
**Synonyms:** compound, chemical entity, test subject

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `molecule_id` | VARCHAR | Unique identifier for the molecule | compound_id, chemical_id |
| `ind1` | BIGINT | Indicator variable 1 (structural feature flag) | indicator_1, feature_1 |
| `inda` | BIGINT | Indicator variable A (structural feature flag) | indicator_a, feature_a |
| `logp` | DOUBLE | Partition coefficient (lipophilicity measure) | log_partition, lipophilicity |
| `lumo` | DOUBLE | Lowest unoccupied molecular orbital energy | orbital_energy, lumo_energy |
| `mutagenic` | VARCHAR | Activity classification | activity, mutagenicity, toxicity_class |

**Enumerated values for `mutagenic`:** `yes`, `no`

---

### Table: `mutagenesis.atom`
**Meaning:** Individual atoms within molecules, with elemental identity and chemical properties.  
**Synonyms:** atomic node, atom record, element instance

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `atom_id` | VARCHAR | Unique identifier for the atom | atomic_id, node_id |
| `molecule_id` | VARCHAR | Foreign key linking to parent molecule | compound_id |
| `element` | VARCHAR | Chemical element symbol (lowercase) | element_type, atomic_symbol |
| `type` | BIGINT | Atom type code (standardized classification) | atom_type_code, atom_class |
| `charge` | DOUBLE | Partial atomic charge (electrostatic property) | partial_charge, atomic_charge |

**Enumerated values for `element`:** `b`, `c`, `f`, `h`, `i`, `n`, `o`

---

### Table: `mutagenesis.bond`
**Meaning:** Chemical bonds connecting pairs of atoms within molecules.  
**Synonyms:** edge, connection, linkage

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `atom1_id` | VARCHAR | First atom in the bond pair | source_atom, atom_a |
| `atom2_id` | VARCHAR | Second atom in the bond pair | target_atom, atom_b |
| `type` | BIGINT | Bond type classification code | bond_type_code, bond_class |

**Bond type enumeration:** `1` = single, `2` = double, `3` = triple, `4` = aromatic

---

## 3. Join Paths

**Molecule to Atom:**
```sql
mutagenesis.molecule m
INNER JOIN mutagenesis.atom a ON m.molecule_id = a.molecule_id
```

**Molecule to Bond (via Atom):**
```sql
mutagenesis.molecule m
INNER JOIN mutagenesis.atom a ON m.molecule_id = a.molecule_id
INNER JOIN mutagenesis.bond b ON (b.atom1_id = a.atom_id OR b.atom2_id = a.atom_id)
```

**Bond endpoints to Atoms:**
```sql
mutagenesis.bond b
INNER JOIN mutagenesis.atom a1 ON b.atom1_id = a1.atom_id
INNER JOIN mutagenesis.atom a2 ON b.atom2_id = a2.atom_id
```

---

## 4. Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| Only molecules with complete bond information in structural analysis | `WHERE molecule_id IN (SELECT DISTINCT molecule_id FROM mutagenesis.bond)` |
| Molecules without activity label classified as "untested" | `WHERE mutagenic IS NULL` (or use CASE: `CASE WHEN mutagenic IS NULL THEN 'untested' ELSE mutagenic END`) |
| Mutagenic activity is binary positive classification | `WHERE mutagenic = 'yes'` |
| Non-mutagenic activity is binary negative classification | `WHERE mutagenic = 'no'` |
| Aromatic bonds identified separately | `WHERE type = 4` (aromatic); `WHERE type IN (1, 2, 3)` (non-aromatic) |
| Single bonds | `WHERE type = 1` |
| Double bonds | `WHERE type = 2` |
| Triple bonds | `WHERE type = 3` |
| Charged atoms flagged for electrostatic calculations | `WHERE charge <> 0` or `WHERE charge IS NOT NULL AND charge <> 0` |
| Hydrogen atoms (implicit handling) | `WHERE element = 'h'` |
| Ring membership: bond is "in-ring" if both atoms are ring members | Requires external ring detection algorithm; SQL identifies candidate bonds: `SELECT b.* FROM mutagenesis.bond b INNER JOIN mutagenesis.atom a1 ON b.atom1_id = a1.atom_id INNER JOIN mutagenesis.atom a2 ON b.atom2_id = a2.atom_id WHERE a1.molecule_id = a2.molecule_id` |

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| mutagenic compound | `WHERE mutagenic = 'yes'` |
| non-mutagenic compound | `WHERE mutagenic = 'no'` |
| active molecule | `WHERE mutagenic = 'yes'` |
| inactive molecule | `WHERE mutagenic = 'no'` |
| untested molecule | `WHERE mutagenic IS NULL` |
| lipophilicity | `molecule.logp` |
| orbital energy | `molecule.lumo` |
| atomic charge | `atom.charge` |
| charged atom | `WHERE atom.charge <> 0` |
| element type | `atom.element` |
| bond connectivity | `bond.atom1_id`, `bond.atom2_id` |
| aromatic bond | `WHERE bond.type = 4` |
| single bond | `WHERE bond.type = 1` |
| double bond | `WHERE bond.type = 2` |
| triple bond | `WHERE bond.type = 3` |
| atom count per molecule | `COUNT(DISTINCT atom.atom_id) GROUP BY molecule.molecule_id` |
| bond count per molecule | `COUNT(*) FROM mutagenesis.bond GROUP BY molecule_id` |
| structural feature 1 | `molecule.ind1` |
| structural feature A | `molecule.inda` |