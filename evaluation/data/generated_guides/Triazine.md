# Triazine Schema Reference Guide

## Schema Summary
This schema contains molecular activity data with per-position chemical property descriptors for triazine compounds.

## Join Paths

**Molecule to position properties:**
```sql
FROM Triazine.molecule m
JOIN Triazine.position p ON m.molecule_id = p.molecule_id
```

## Table Reference

### `Triazine.molecule`
Core molecule records with measured activity values.

| Column | Meaning |
|--------|---------|
| `molecule_id` | Unique molecule identifier; foreign key to `Triazine.position` |
| `activity` | Measured biological activity (DOUBLE, range ~0.5–0.8 in samples) |

### `Triazine.position`
Chemical property descriptors at each position (1–5) within a molecule.

| Column | Meaning |
|--------|---------|
| `molecule_id` | Foreign key to `Triazine.molecule` |
| `position` | Position index within molecule (1–5 in samples) |
| `branch` | Branching descriptor (DOUBLE) |
| `flex` | Flexibility descriptor (DOUBLE) |
| `h_acceptor` | Hydrogen acceptor property (DOUBLE) |
| `h_doner` | Hydrogen donor property (DOUBLE) |
| `pi_acceptor` | π-electron acceptor property (DOUBLE) |
| `pi_doner` | π-electron donor property (DOUBLE) |
| `polar` | Polarity descriptor (DOUBLE) |
| `polarisable` | Polarizability descriptor (DOUBLE) |
| `sigma` | Sigma descriptor (DOUBLE) |
| `size` | Size descriptor (DOUBLE) |