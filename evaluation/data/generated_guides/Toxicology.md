# Toxicology Schema Reference Guide

## 1. Schema Summary

The Toxicology schema contains molecular structure data with atom compositions, bond connectivity, and mutagenic activity classifications for pharmaceutical research.

---

## 2. Table Reference

### Table: `Toxicology.atom`
**Meaning:** Individual atoms within molecules; represents atomic composition of chemical structures.
**Synonyms:** atomic component, element node

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `atom_id` | VARCHAR | Unique identifier for an atom within a molecule | atom identifier, atomic ID |
| `molecule_id` | VARCHAR | Foreign key linking atom to parent molecule | mol ID, compound ID |
| `element` | VARCHAR | Chemical element symbol (periodic table notation) | element type, atomic symbol |

**Notable values:** `cl` (chlorine), `c` (carbon), `h` (hydrogen); values are lowercase

---

### Table: `Toxicology.bond`
**Meaning:** Chemical bonds connecting atoms; represents bond types in molecular structures.
**Synonyms:** chemical bond, connection type

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `bond_id` | VARCHAR | Unique identifier for a bond within a molecule | bond identifier |
| `molecule_id` | VARCHAR | Foreign key linking bond to parent molecule | mol ID, compound ID |
| `bond_type` | VARCHAR | Type of chemical bond | connection type, bond classification |

**Notable values:** `-` (single bond), `=` (double bond), `#` (triple bond)

---

### Table: `Toxicology.connected`
**Meaning:** Atom-to-atom connectivity records; represents which atoms are bonded together.
**Synonyms:** atom connection, bond endpoint, adjacency

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `atom_id` | VARCHAR | First atom in a bond connection | source atom, atom 1 |
| `atom_id2` | VARCHAR | Second atom in a bond connection | target atom, atom 2 |
| `bond_id` | VARCHAR | Foreign key linking to the bond record | bond identifier |

**Notable characteristics:** Each bond appears twice (bidirectional): once as `atom_id → atom_id2` and once as `atom_id2 → atom_id`

---

### Table: `Toxicology.molecule`
**Meaning:** Molecular compounds with mutagenic activity classification.
**Synonyms:** compound, chemical structure, test compound

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `molecule_id` | VARCHAR | Unique identifier for a molecule | mol ID, compound ID, structure ID |
| `label` | VARCHAR | Mutagenic activity classification | activity label, mutagenicity, toxicity class |

**Notable values:** `+` (mutagenic/positive), `-` (non-mutagenic/negative)

---

## 3. Join Paths

**Molecule to Atoms:**
```sql
Toxicology.molecule m
JOIN Toxicology.atom a ON m.molecule_id = a.molecule_id
```

**Molecule to Bonds:**
```sql
Toxicology.molecule m
JOIN Toxicology.bond b ON m.molecule_id = b.molecule_id
```

**Atoms via Connectivity:**
```sql
Toxicology.connected c
JOIN Toxicology.atom a1 ON c.atom_id = a1.atom_id
JOIN Toxicology.atom a2 ON c.atom_id2 = a2.atom_id
```

**Complete Molecular Structure (atoms + bonds + connectivity):**
```sql
Toxicology.molecule m
JOIN Toxicology.atom a ON m.molecule_id = a.molecule_id
JOIN Toxicology.bond b ON m.molecule_id = b.molecule_id
JOIN Toxicology.connected c ON b.bond_id = c.bond_id
```

---

## 4. Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| Only molecules with complete bond information | `WHERE molecule_id IN (SELECT molecule_id FROM bond GROUP BY molecule_id HAVING COUNT(*) > 0)` |
| Molecules without activity label are "untested" | `WHERE label IS NULL` → classify as untested; `WHERE label IS NOT NULL` → tested |
| Mutagenic activity is binary positive | `WHERE label = '+'` |
| Non-mutagenic activity is binary negative | `WHERE label = '-'` |
| Bond type: single bond | `WHERE bond_type = '-'` |
| Bond type: double bond | `WHERE bond_type = '='` |
| Bond type: triple bond | `WHERE bond_type = '#'` |
| Atom element standardization check | `WHERE element IN (SELECT DISTINCT element FROM atom)` — verify against periodic table symbols |
| Bidirectional connectivity (both directions exist) | `WHERE EXISTS (SELECT 1 FROM connected c2 WHERE c2.atom_id = c.atom_id2 AND c2.atom_id2 = c.atom_id)` |

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| mutagenic compound | `WHERE molecule.label = '+'` |
| non-mutagenic compound | `WHERE molecule.label = '-'` |
| untested molecule | `WHERE molecule.label IS NULL` |
| active molecule | `WHERE molecule.label = '+'` |
| inactive molecule | `WHERE molecule.label = '-'` |
| single bond | `WHERE bond.bond_type = '-'` |
| double bond | `WHERE bond.bond_type = '='` |
| triple bond | `WHERE bond.bond_type = '#'` |
| atom count | `COUNT(DISTINCT atom.atom_id)` |
| bond count | `COUNT(DISTINCT bond.bond_id)` |
| chlorine atoms | `WHERE atom.element = 'cl'` |
| carbon atoms | `WHERE atom.element = 'c'` |
| hydrogen atoms | `WHERE atom.element = 'h'` |
| connected atoms | `SELECT atom_id, atom_id2 FROM connected` |
| molecular structure | `molecule JOIN atom JOIN bond JOIN connected` |
| compound ID | `molecule.molecule_id` |
| activity classification | `molecule.label` |