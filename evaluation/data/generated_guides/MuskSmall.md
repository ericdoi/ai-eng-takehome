# MuskSmall Schema Reference Guide

## Schema Summary
This schema contains molecular conformation data for musk compounds, with 166 computed features per conformation and classification labels per molecule.

---

## Table Reference

### Table: `MuskSmall.conformation`
**Meaning:** Individual 3D conformations (spatial arrangements) of musk molecules, each with 166 computed molecular features.

**Synonyms:** conformer, structure, pose, configuration

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `conformation_name` | VARCHAR | Unique identifier for a specific conformation | conformer_id, structure_id |
| `molecule_name` | VARCHAR | Name of the parent molecule; foreign key to `molecule.molecule_name` | molecule_id, compound_name |
| `f1` through `f166` | BIGINT (166 columns) | Computed molecular descriptors/features (e.g., topological, geometric, or chemical properties) | feature_1–feature_166, descriptor_1–descriptor_166, property_1–property_166 |

**Notable values:**
- `conformation_name` format: `{molecule_id}_{index}+{variant}` (e.g., `188_1+1`, `190_1+1`)
- `molecule_name` values: `MUSK-188`, `MUSK-190`, `MUSK-211`, `MUSK-212`, `MUSK-213`
- Feature values (`f1`–`f166`): signed integers, typically in range [–330, 200]

---

### Table: `MuskSmall.molecule`
**Meaning:** Musk compounds with their biological activity classification.

**Synonyms:** compound, chemical, drug

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `molecule_name` | VARCHAR | Unique identifier for a molecule | molecule_id, compound_name |
| `class` | BIGINT | Binary classification label (activity/inactivity) | label, activity, classification, target |

**Notable values:**
- `molecule_name` values: `MUSK-188`, `MUSK-190`, `MUSK-211`, `MUSK-212`, `MUSK-213`
- `class` values: `1` (observed in sample data; likely 0 or 1 for binary classification)

---

## Join Paths

**Conformation to Molecule:**
```sql
conformation c
INNER JOIN molecule m ON c.molecule_name = m.molecule_name
```

---

## Business Rules as SQL

No explicit business rules provided in schema documentation. Common filtering patterns:

- **Active molecules only:** `WHERE m.class = 1`
- **Inactive molecules only:** `WHERE m.class = 0`
- **Conformations of a specific molecule:** `WHERE c.molecule_name = 'MUSK-188'`

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| musk compound | `molecule.molecule_name` |
| molecular structure | `conformation` table row |
| activity label | `molecule.class` |
| active musk | `WHERE molecule.class = 1` |
| molecular feature | `conformation.f1` through `conformation.f166` |
| feature vector | All `f*` columns for a single conformation |
| conformer ID | `conformation.conformation_name` |
| descriptor | `conformation.f1` through `conformation.f166` |
| count of conformations | `COUNT(DISTINCT conformation.conformation_name)` |
| count of molecules | `COUNT(DISTINCT molecule.molecule_name)` |
| conformations per molecule | `COUNT(conformation.conformation_name) GROUP BY conformation.molecule_name` |