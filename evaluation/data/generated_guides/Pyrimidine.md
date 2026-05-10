# Pyrimidine Schema Reference Guide

## Schema Summary
The Pyrimidine schema contains molecular activity measurements and position-specific chemical property descriptors for a set of pyrimidine compounds.

---

## Table Reference

### Table: `Pyrimidine.molecule`
**Meaning:** Core molecule records with measured biological activity values.
**Synonyms:** compounds, molecules

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `molecule_id` | BIGINT | Unique identifier for each molecule | compound_id, mol_id |
| `activity` | DOUBLE | Measured biological activity value (range: 0–1) | potency, efficacy, response |

**Notable values:** activity ranges from 0.531 to 0.634 in sample data.

---

### Table: `Pyrimidine.position`
**Meaning:** Chemical property descriptors for each position within a molecule structure.
**Synonyms:** position_properties, molecular_descriptors, site_properties

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `molecule_id` | BIGINT | Foreign key linking to molecule | compound_id, mol_id |
| `position` | BIGINT | Position index within the molecule structure (1-indexed) | site, location, index |
| `flex` | DOUBLE | Flexibility descriptor | flexibility |
| `h_acceptor` | DOUBLE | Hydrogen bond acceptor property | h_bond_acceptor, acceptor |
| `h_doner` | DOUBLE | Hydrogen bond donor property | h_bond_donor, donor |
| `pi_acceptor` | DOUBLE | Pi-electron acceptor property | pi_accept, aromatic_acceptor |
| `pi_doner` | DOUBLE | Pi-electron donor property | pi_donor, aromatic_donor |
| `polar` | DOUBLE | Polarity descriptor | polarity |
| `polarisable` | DOUBLE | Polarizability descriptor | polarizability |
| `sigma` | DOUBLE | Sigma descriptor (electronic effect) | sigma_effect |
| `size` | DOUBLE | Size descriptor | molecular_size, steric |

**Notable values:** All descriptors are normalized values (0.0–0.367 in sample data).

---

## Join Paths

**molecule ↔ position:**
```sql
Pyrimidine.molecule m
INNER JOIN Pyrimidine.position p ON m.molecule_id = p.molecule_id
```

---

## Business Rules as SQL

No explicit business rules provided in schema documentation. Standard constraints:
- `molecule_id` is the primary key in `Pyrimidine.molecule`
- `(molecule_id, position)` forms a composite key in `Pyrimidine.position`
- All descriptor columns (`flex`, `h_acceptor`, etc.) contain normalized numeric values

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| molecule activity | `Pyrimidine.molecule.activity` |
| compound potency | `Pyrimidine.molecule.activity` |
| position properties | `Pyrimidine.position.*` (all descriptor columns) |
| hydrogen bonding capacity | `Pyrimidine.position.h_acceptor`, `Pyrimidine.position.h_doner` |
| aromatic character | `Pyrimidine.position.pi_acceptor`, `Pyrimidine.position.pi_doner` |
| electronic properties | `Pyrimidine.position.sigma`, `Pyrimidine.position.polar` |
| steric properties | `Pyrimidine.position.size`, `Pyrimidine.position.flex` |
| high activity molecule | `WHERE Pyrimidine.molecule.activity > 0.6` |
| all positions for a molecule | `WHERE Pyrimidine.position.molecule_id = <id>` |