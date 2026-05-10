# Triazine Schema Reference Guide

## Schema Summary
The Triazine schema contains molecular activity data with chemical property measurements at multiple positions within each molecule.

---

## Table Reference

### Table: `Triazine.molecule`
**Meaning:** Master table of molecules with their measured biological activity values.
**Synonyms:** compounds, samples, molecules

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `molecule_id` | BIGINT | Unique identifier for each molecule | compound_id, sample_id |
| `activity` | DOUBLE | Measured biological activity value (range: 0–1) | bioactivity, response, potency |

**Notable values:** activity ranges from 0.564 to 0.772 in sample data.

---

### Table: `Triazine.position`
**Meaning:** Chemical property measurements for each position (1–5) within a molecule. Each molecule has multiple position records.
**Synonyms:** molecular_positions, substituents, sites

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `molecule_id` | BIGINT | Foreign key linking to `Triazine.molecule` | compound_id |
| `position` | BIGINT | Position index within the molecule (1–5) | site, location, index |
| `branch` | DOUBLE | Branching property descriptor | branching |
| `flex` | DOUBLE | Flexibility property descriptor | flexibility |
| `h_acceptor` | DOUBLE | Hydrogen acceptor property descriptor | h_accept, acceptor |
| `h_doner` | DOUBLE | Hydrogen donor property descriptor | h_donor, donor |
| `pi_acceptor` | DOUBLE | Pi electron acceptor property descriptor | pi_accept |
| `pi_doner` | DOUBLE | Pi electron donor property descriptor | pi_donor |
| `polar` | DOUBLE | Polarity property descriptor | polarity |
| `polarisable` | DOUBLE | Polarizability property descriptor | polarizability |
| `sigma` | DOUBLE | Sigma descriptor (electronic effect) | sigma_value |
| `size` | DOUBLE | Size property descriptor | molecular_size |

**Notable values:** All property descriptors are numeric (0.0–0.1 in sample data).

---

## Join Paths

**Primary join between molecule and position:**
```sql
Triazine.molecule m
INNER JOIN Triazine.position p ON m.molecule_id = p.molecule_id
```

---

## Business Rules as SQL

No explicit business rules provided in schema documentation. Standard constraints:
- `molecule_id` is the primary key in `Triazine.molecule`
- `(molecule_id, position)` forms a composite key in `Triazine.position`
- All property descriptors in `Triazine.position` are numeric values

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| molecule activity | `Triazine.molecule.activity` |
| compound potency | `Triazine.molecule.activity` |
| position properties | `Triazine.position.[branch, flex, h_acceptor, h_doner, pi_acceptor, pi_doner, polar, polarisable, sigma, size]` |
| hydrogen bonding capacity | `Triazine.position.h_acceptor`, `Triazine.position.h_doner` |
| electronic properties | `Triazine.position.pi_acceptor`, `Triazine.position.pi_doner`, `Triazine.position.sigma` |
| molecular flexibility | `Triazine.position.flex` |
| molecular size | `Triazine.position.size` |
| all molecules | `SELECT * FROM Triazine.molecule` |
| all positions for a molecule | `SELECT * FROM Triazine.position WHERE molecule_id = ?` |