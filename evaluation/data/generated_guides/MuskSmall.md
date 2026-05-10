# MuskSmall Schema Reference Guide

## Schema Summary
This schema contains molecular conformations with 166 computed features and their associated molecule classifications for musky compound analysis.

## Join Paths

**Conformation to Molecule:**
```sql
FROM MuskSmall.conformation c
JOIN MuskSmall.molecule m ON c.molecule_name = m.molecule_name
```

## Table Reference

### `MuskSmall.conformation`
Molecular conformation records with computed feature vectors.

| Column | Semantics |
|--------|-----------|
| `conformation_name` | Unique identifier for a specific conformation (e.g., `188_1+1`) |
| `molecule_name` | Foreign key to `MuskSmall.molecule.molecule_name` |
| `f1` through `f166` | Computed molecular features (BIGINT). Each column represents a distinct structural or chemical descriptor. Features are indexed numerically with no semantic distinction between them. |

### `MuskSmall.molecule`
Molecule master records with classification labels.

| Column | Semantics |
|--------|-----------|
| `molecule_name` | Unique identifier (e.g., `MUSK-188`, `MUSK-190`) |
| `class` | Binary classification: `1` = active/positive class |