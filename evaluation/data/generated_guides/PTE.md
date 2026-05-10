# PTE Schema Reference Guide

## Schema Summary
The PTE schema contains molecular drug data with structural properties, chemical functional groups, and mutagenicity/activity classifications for pharmaceutical toxicity prediction.

---

## Join Paths

**Drug to activity status:**
```sql
FROM PTE.pte_drug d
LEFT JOIN PTE.pte_active a ON d.drug_id = a.drug_id
```

**Drug to structural atoms and bonds:**
```sql
FROM PTE.pte_drug d
LEFT JOIN PTE.pte_atm atm ON d.drug_id = atm.drug_id
LEFT JOIN PTE.pte_bond b ON d.drug_id = b.drug_id
```

**Drug to functional groups (any group type):**
```sql
FROM PTE.pte_drug d
LEFT JOIN PTE.pte_amine am ON d.drug_id = am.Arg0
-- Repeat for other groups: pte_alcohol, pte_ether, pte_ketone, pte_nitro, etc.
```

**Drug to test/post-test activity:**
```sql
FROM PTE.pte_drug d
LEFT JOIN PTE.pte_testactive t ON d.drug_id = t.Arg0
LEFT JOIN PTE.postestactive pe ON d.drug_id = pe.Arg0
```

---

## Business Rules as SQL

**Active compounds (training set):**
```sql
WHERE drug_id IN (SELECT Arg0 FROM PTE.active)
```

**Mutagenic compounds:**
```sql
WHERE drug_id IN (SELECT Arg0 FROM PTE.pte_mutagenic)
```

**Ames test positive:**
```sql
WHERE drug_id IN (SELECT Arg0 FROM PTE.pte_ames)
```

**Test set active (positive):**
```sql
WHERE drug_id IN (SELECT Arg0 FROM PTE.pte_testactive WHERE Set = 'T')
```

**Test set inactive (negative):**
```sql
WHERE drug_id IN (SELECT Arg0 FROM PTE.pte_testactive WHERE Set = 'F')
```

**Post-test active (positive):**
```sql
WHERE drug_id IN (SELECT Arg0 FROM PTE.postestactive)
```

**Post-test inactive (negative):**
```sql
WHERE drug_id IN (SELECT Arg0 FROM PTE.postestactive_Neg)
```

**Has specific toxicity property:**
```sql
WHERE drug_id IN (SELECT Arg0 FROM PTE.pte_has_property WHERE Arg1 = 'salmonella' AND Arg2 = 'p')
-- Arg1 values: salmonella, salmonella_n, salmonella_reduc, cytogen_ca, cytogen_sce, drosophila_rt, drosophila_slrl, micronuc_f, micronuc_m, mouse_lymph, chromaberr, chromex
-- Arg2: 'p' (positive), 'n' (negative)
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| drug identifier | `drug_id` (PTE.pte_drug, PTE.pte_active, etc.) |
| active compound | `Arg0 IN (SELECT Arg0 FROM PTE.active)` |
| mutagenic | `Arg0 IN (SELECT Arg0 FROM PTE.pte_mutagenic)` |
| Ames positive | `Arg0 IN (SELECT Arg0 FROM PTE.pte_ames)` |
| test active | `Set = 'T'` in PTE.pte_testactive |
| test inactive | `Set = 'F'` in PTE.pte_testactive |
| post-test active | `Arg0 IN (SELECT Arg0 FROM PTE.postestactive)` |
| post-test inactive | `Arg0 IN (SELECT Arg0 FROM PTE.postestactive_Neg)` |
| atom charge | `Arg4` in PTE.pte_atm |
| bond type | `Arg3` in PTE.pte_bond (values: 1, 2, 3, 7) |
| functional group | pte_amine, pte_alcohol, pte_ether, pte_ketone, pte_nitro, pte_ester, pte_phenol, pte_sulfide, pte_sulfo, pte_methoxy, pte_methyl, pte_imine, pte_alkyl_halide |
| ring structure | pte_five_ring, pte_six_ring, pte_non_ar_5c_ring, pte_non_ar_6c_ring, pte_non_ar_hetero_5_ring, pte_non_ar_hetero_6_ring |

---

## Table Reference

### `PTE.pte_drug`
Master drug list. Single column: `drug_id` (VARCHAR, e.g., d1, d100, d296).

### `PTE.pte_active`
Training set active compounds. Column: `Arg0` (drug_id).

### `PTE.active`
Alias for training set. Column: `Arg0` (drug_id).

### `PTE.pte_testactive`
Test set activity labels. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): **T** (active), **F** (inactive)

### `PTE.pte_testactive_Neg`
Test set negative labels (alternative representation). Columns:
- `Arg0` (drug_id)
- `Binary` (VARCHAR): **T**, **F**

### `PTE.postestactive`
Post-test active compounds. Column: `Arg0` (drug_id).

### `PTE.postestactive_Neg`
Post-test inactive compounds. Column: `Arg0` (drug_id).

### `PTE.pte_ames`
Ames test positive compounds. Column: `Arg0` (drug_id).

### `PTE.pte_mutagenic`
Mutagenic compounds. Column: `Arg0` (drug_id).

### `PTE.pte_active`
Drug activity status. Columns:
- `drug_id` (VARCHAR)
- `is_active` (VARCHAR): **T** (active), **F** (inactive)

### `PTE.pte_atm`
Atom properties. Columns:
- `drug_id` (VARCHAR)
- `atom_id` (VARCHAR, e.g., d100_1)
- `atom_type` (VARCHAR): c, h, n, o, s, etc.
- `Arg3` (VARCHAR): atom class/type code
- `Arg4` (DOUBLE): partial charge

### `PTE.pte_atm_count`
Atom count per drug. Columns:
- `Arg0` (drug_id)
- `Cnt` (BIGINT): number of atoms

### `PTE.pte_atm_bond_count`
Bond count per atom. Columns:
- `atom_id` (VARCHAR)
- `Cnt` (BIGINT): number of bonds

### `PTE.pte_atm_max_charge`
Maximum partial charge per drug. Columns:
- `Arg0` (drug_id)
- `Mx` (DOUBLE)

### `PTE.pte_atm_min_charge`
Minimum partial charge per drug. Columns:
- `Arg0` (drug_id)
- `Mn` (DOUBLE)

### `PTE.pte_bond`
Bond connectivity. Columns:
- `drug_id` (VARCHAR)
- `atom_id1` (VARCHAR)
- `atom_id2` (VARCHAR)
- `Arg3` (VARCHAR): bond type **1** (single), **2** (double), **3** (triple), **7** (aromatic)

### `PTE.pte_bond_count`
Bond count per drug. Columns:
- `Arg0` (drug_id)
- `Cnt` (BIGINT)

### `PTE.pte_has_property`
Toxicity test results. Columns:
- `Arg0` (drug_id)
- `Arg1` (VARCHAR): test type: **salmonella**, **salmonella_n**, **salmonella_reduc**, **cytogen_ca**, **cytogen_sce**, **drosophila_rt**, **drosophila_slrl**, **micronuc_f**, **micronuc_m**, **mouse_lymph**, **chromaberr**, **chromex**
- `Arg2` (VARCHAR): **p** (positive), **n** (negative)

### `PTE.pte_ind`
Indicator/descriptor flags. Columns:
- `Arg0` (drug_id)
- `Arg1` (VARCHAR): descriptor name: **amino**, **cyanate**, **di10**, **di227**, **di23**, **di232**, **di260**, **di281**, **di48**, **di51**, **di64**, **di66**, **di67a**, **di8**, **ethoxy**, **halide10**, **methanol**, **methoxy**, **nitro**, **ring_size_4**
- `Arg2` (VARCHAR): count/flag value

### `PTE.pte_amine`
Amine functional groups. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set [atom_id, atom_id, ...]

### `PTE.pte_alcohol`
Alcohol functional groups. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_ether`
Ether functional groups. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_ketone`
Ketone functional groups. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_nitro`
Nitro functional groups. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_ester`
Ester functional groups. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_phenol`
Phenol functional groups. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_sulfide`
Sulfide functional groups. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_sulfo`
Sulfo functional groups. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_methoxy`
Methoxy functional groups. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_methyl`
Methyl functional groups. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_imine`
Imine functional groups. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_alkyl_halide`
Alkyl halide functional groups. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_five_ring`
Five-membered rings. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set (5 atoms)

### `PTE.pte_six_ring`
Six-membered rings. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set (6 atoms)

### `PTE.pte_non_ar_5c_ring`
Non-aromatic 5-carbon rings. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_non_ar_6c_ring`
Non-aromatic 6-carbon rings. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_non_ar_hetero_5_ring`
Non-aromatic 5-membered heterocycles. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_non_ar_hetero_6_ring`
Non-aromatic 6-membered heterocycles. Columns:
- `Arg0` (drug_id)
- `Set` (VARCHAR): atom set

### `PTE.pte_number`
Binary classification reference. Column: `Binary` (VARCHAR): **T**, **F**.