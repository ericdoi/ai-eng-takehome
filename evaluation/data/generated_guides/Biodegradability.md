# Biodegradability Schema Reference Guide

## 1. Schema Summary

The Biodegradability schema contains molecular structure data including atoms, bonds, functional groups, and molecular properties for biodegradability analysis.

---

## 2. Table Reference

### Table: `Biodegradability.atom`
**Meaning:** Individual atoms within molecules; represents nodes in molecular structures.
**Synonyms:** atomic component, atom record

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `atom_id` | VARCHAR | Unique identifier for an atom within a molecule | atom identifier, atomic ID |
| `molecule_id` | VARCHAR | Foreign key linking atom to parent molecule | mol ID, compound ID |
| `type` | VARCHAR | Chemical element symbol | element, atomic type, element type |

**Enumerated values for `type`:** `br`, `c`, `ca`, `cl`, `f`, `h`, `i`, `n`, `o`, `p`, `pb`, `s`

---

### Table: `Biodegradability.bond`
**Meaning:** Chemical bonds connecting pairs of atoms; represents edges in molecular structures.
**Synonyms:** chemical bond, atomic connection, bond record

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `atom_id` | VARCHAR | First atom in the bond pair | source atom, atom 1 |
| `atom_id2` | VARCHAR | Second atom in the bond pair | target atom, atom 2 |
| `type` | VARCHAR | Bond order/type | bond order, bond classification |

**Enumerated values for `type`:** `1` (single), `2` (double), `3` (triple), `7` (aromatic)

---

### Table: `Biodegradability.gmember`
**Meaning:** Membership mapping of atoms to functional groups; represents group composition.
**Synonyms:** group membership, atom-group association, functional group member

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `atom_id` | VARCHAR | Atom that belongs to a functional group | member atom, atomic component |
| `group_id` | VARCHAR | Functional group identifier | group ID, functional group ID |

---

### Table: `Biodegradability.group`
**Meaning:** Functional group definitions and classifications.
**Synonyms:** functional group, group type, chemical group

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `group_id` | VARCHAR | Unique identifier for a functional group | group identifier, group code |
| `type` | VARCHAR | Functional group classification | group type, group name, functional group type |

**Sample enumerated values for `type`:** `sulfo`, `nitro`, `methyl`, `c2n`

---

### Table: `Biodegradability.molecule`
**Meaning:** Molecular compounds with calculated properties and biodegradability activity.
**Synonyms:** compound, chemical compound, molecular record

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `molecule_id` | VARCHAR | Unique identifier for a molecule | mol ID, compound ID, molecule identifier |
| `activity` | DOUBLE | Biodegradability activity measure (numeric score) | biodegradability score, activity value |
| `logp` | DOUBLE | Partition coefficient (lipophilicity measure) | log P, octanol-water partition |
| `mweight` | DOUBLE | Molecular weight in g/mol | molecular mass, mass, weight |

---

## 3. Join Paths

| Join | Condition | Purpose |
|------|-----------|---------|
| molecule → atom | `molecule.molecule_id = atom.molecule_id` | Retrieve all atoms in a molecule |
| atom → bond | `atom.atom_id = bond.atom_id OR atom.atom_id = bond.atom_id2` | Find bonds connected to an atom |
| atom → gmember | `atom.atom_id = gmember.atom_id` | Find functional groups containing an atom |
| gmember → group | `gmember.group_id = group.group_id` | Retrieve functional group details for group members |
| molecule → atom → gmember → group | Chain above joins | Retrieve all functional groups in a molecule |

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation. Rules should be inferred from domain knowledge of molecular chemistry and biodegradability assessment.

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| atom count in molecule | `COUNT(atom.atom_id)` WHERE `atom.molecule_id = ?` |
| carbon atoms | `WHERE atom.type = 'c'` |
| hydrogen atoms | `WHERE atom.type = 'h'` |
| nitrogen atoms | `WHERE atom.type = 'n'` |
| oxygen atoms | `WHERE atom.type = 'o'` |
| sulfur atoms | `WHERE atom.type = 's'` |
| halogen atoms | `WHERE atom.type IN ('br', 'cl', 'f', 'i')` |
| single bonds | `WHERE bond.type = '1'` |
| double bonds | `WHERE bond.type = '2'` |
| triple bonds | `WHERE bond.type = '3'` |
| aromatic bonds | `WHERE bond.type = '7'` |
| functional groups in molecule | `SELECT DISTINCT group.type FROM group JOIN gmember ON group.group_id = gmember.group_id JOIN atom ON gmember.atom_id = atom.atom_id WHERE atom.molecule_id = ?` |
| high activity molecules | `WHERE molecule.activity > [threshold]` |
| lipophilic molecules | `WHERE molecule.logp > [threshold]` |
| heavy molecules | `WHERE molecule.mweight > [threshold]` |