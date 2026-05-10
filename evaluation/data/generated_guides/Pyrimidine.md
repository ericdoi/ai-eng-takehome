# Pyrimidine Schema Reference Guide

## Schema Summary
This schema contains molecular activity data with per-position chemical property descriptors for pyrimidine compounds.

## Join Paths

**Molecule to position properties:**
```sql
FROM Pyrimidine.molecule m
JOIN Pyrimidine.position p ON m.molecule_id = p.molecule_id
```

## Table Reference

### `Pyrimidine.molecule`
Core molecule records with measured activity values.

| Column | Meaning |
|--------|---------|
| `molecule_id` | Unique molecule identifier; foreign key to `Pyrimidine.position` |
| `activity` | Measured biological activity (DOUBLE, range ~0.5–0.6 in samples) |

### `Pyrimidine.position`
Chemical property descriptors at each position within a molecule.

| Column | Meaning |
|--------|---------|
| `molecule_id` | Foreign key to `Pyrimidine.molecule` |
| `position` | Position index within the molecule (BIGINT, 1-indexed) |
| `flex` | Flexibility descriptor (DOUBLE) |
| `h_acceptor` | Hydrogen bond acceptor property (DOUBLE) |
| `h_doner` | Hydrogen bond donor property (DOUBLE) |
| `pi_acceptor` | π-electron acceptor property (DOUBLE) |
| `pi_doner` | π-electron donor property (DOUBLE) |
| `polar` | Polarity descriptor (DOUBLE) |
| `polarisable` | Polarizability descriptor (DOUBLE) |
| `sigma` | Sigma descriptor (DOUBLE) |
| `size` | Size descriptor (DOUBLE) |