# PTE Schema Reference Guide

## Schema Summary

The PTE schema contains molecular drug data with structural properties, chemical functional groups, and mutagenicity/activity classifications for pharmaceutical toxicity evaluation.

---

## Table Reference

### PTE.active
**Meaning:** List of active drug compounds (baseline active set)  
**Synonyms:** active compounds, active drugs

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |

**Notable values:** d1, d10, d100–d102

---

### PTE.postestactive
**Meaning:** Post-test active compounds (positive test results)  
**Synonyms:** post-test positive, test-active compounds

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |

**Notable values:** d296, d305–d337 (subset)

---

### PTE.postestactive_Neg
**Meaning:** Post-test negative compounds (negative test results)  
**Synonyms:** post-test negative, test-inactive compounds

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |

**Notable values:** d297–d335 (subset)

---

### PTE.pte_active
**Meaning:** Drug activity classification (binary active/inactive)  
**Synonyms:** activity status, active flag

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| drug_id | VARCHAR | Drug identifier | Arg0, compound_id |
| is_active | VARCHAR | Activity status | active_flag, activity |

**Notable values:** `F` (inactive), `T` (active)

---

### PTE.pte_alcohol
**Meaning:** Alcohol functional groups detected in drug molecules  
**Synonyms:** hydroxyl groups, alcohol moieties

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Set | VARCHAR | Atom IDs forming alcohol group | atom_set, atoms |

**Notable values:** d65, d72, d78, d89, d97; sets like `[d65_14,d65_18,d65_12]`

---

### PTE.pte_alkyl_halide
**Meaning:** Alkyl halide functional groups (C-halogen bonds)  
**Synonyms:** halogenated alkyl, alkyl halides

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Set | VARCHAR | Atom IDs forming alkyl halide | atom_set, atoms |

---

### PTE.pte_ames
**Meaning:** Compounds tested in Ames mutagenicity assay  
**Synonyms:** Ames test, Ames positive

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |

**Notable values:** d1, d10–d12, d113

---

### PTE.pte_amine
**Meaning:** Amine functional groups (nitrogen-containing)  
**Synonyms:** amino groups, amines

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Set | VARCHAR | Atom IDs forming amine group | atom_set, atoms |

**Notable values:** d1, d11, d109; sets like `[d1_24,d1_25,d1_26,d1_17]`

---

### PTE.pte_atm
**Meaning:** Atomic properties for each atom in drug molecules  
**Synonyms:** atoms, atom properties, atomic data

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| drug_id | VARCHAR | Drug identifier | Arg0, compound_id |
| atom_id | VARCHAR | Unique atom identifier | Arg1 |
| atom_type | VARCHAR | Element symbol | element, atomic_symbol |
| Arg3 | VARCHAR | Atom type code/classification | atom_class, type_code |
| Arg4 | DOUBLE | Atomic charge | charge, partial_charge |

**Notable values:** atom_type: `c`, `h`; Arg3: `22`, `3`; Arg4: range –0.812 to 0.156

---

### PTE.pte_atm_bond_count
**Meaning:** Number of bonds per atom  
**Synonyms:** bond count, valence count

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| atom_id | VARCHAR | Unique atom identifier | Arg0 |
| Cnt | BIGINT | Number of bonds | bond_count, valence |

---

### PTE.pte_atm_count
**Meaning:** Total atom count per drug  
**Synonyms:** atom count, molecular size

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Cnt | BIGINT | Total atoms in molecule | atom_count, size |

---

### PTE.pte_atm_max_charge
**Meaning:** Maximum atomic charge in drug molecule  
**Synonyms:** max charge, highest charge

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Mx | DOUBLE | Maximum partial charge | max_charge, charge_max |

**Notable values:** range 0.052–0.079

---

### PTE.pte_atm_min_charge
**Meaning:** Minimum atomic charge in drug molecule  
**Synonyms:** min charge, lowest charge

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Mn | DOUBLE | Minimum partial charge | min_charge, charge_min |

**Notable values:** range –0.812 to –0.798

---

### PTE.pte_bond
**Meaning:** Chemical bonds between atoms  
**Synonyms:** bonds, chemical bonds, connectivity

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| drug_id | VARCHAR | Drug identifier | Arg0, compound_id |
| atom_id1 | VARCHAR | First atom in bond | atom1 |
| atom_id2 | VARCHAR | Second atom in bond | atom2 |
| Arg3 | VARCHAR | Bond type/order | bond_type, bond_order |

**Notable values:** Arg3: `1` (single), `2` (double), `3` (triple), `7` (aromatic)

---

### PTE.pte_bond_count
**Meaning:** Total bond count per drug  
**Synonyms:** bond count, connectivity count

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Cnt | BIGINT | Total bonds in molecule | bond_count |

---

### PTE.pte_drug
**Meaning:** Master list of all drugs in dataset  
**Synonyms:** drugs, compounds, molecules

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| drug_id | VARCHAR | Unique drug identifier | Arg0, compound_id |

**Notable values:** d1–d337 (subset)

---

### PTE.pte_ester
**Meaning:** Ester functional groups (R-COO-R')  
**Synonyms:** esters, ester moieties

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Set | VARCHAR | Atom IDs forming ester group | atom_set, atoms |

**Notable values:** d136; sets like `[d136_15,d136_18,d136_19,d136_14,d136_16]`

---

### PTE.pte_ether
**Meaning:** Ether functional groups (R-O-R')  
**Synonyms:** ethers, ether moieties

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Set | VARCHAR | Atom IDs forming ether group | atom_set, atoms |

**Notable values:** d10, d11, d108, d109, d111; sets like `[d10_14,d10_12,d10_15]`

---

### PTE.pte_five_ring
**Meaning:** Five-membered rings in molecular structure  
**Synonyms:** 5-rings, cyclopentane rings, five-member rings

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Set | VARCHAR | Atom IDs forming five-ring | atom_set, atoms |

**Notable values:** d101, d106; sets like `[d101_1,d101_2,d101_14,d101_5,d101_6]`

---

### PTE.pte_has_property
**Meaning:** Toxicity test results for drugs  
**Synonyms:** test results, toxicity properties, assay results

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Arg1 | VARCHAR | Test/assay type | test_type, assay_name |
| Arg2 | VARCHAR | Test result | result, outcome |

**Notable values:**  
Arg1: `chromaberr`, `chromex`, `cytogen_ca`, `cytogen_sce`, `drosophila_rt`, `drosophila_slrl`, `micronuc_f`, `micronuc_m`, `mouse_lymph`, `salmonella`, `salmonella_n`, `salmonella_reduc`  
Arg2: `p` (positive), `n` (negative)

---

### PTE.pte_imine
**Meaning:** Imine functional groups (C=N)  
**Synonyms:** imines, imine moieties

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Set | VARCHAR | Atom IDs forming imine group | atom_set, atoms |

**Notable values:** d7, d27–d29, d37, d51, d66, d175, d211, d217, d252

---

### PTE.pte_ind
**Meaning:** Indicator/descriptor flags for molecular features  
**Synonyms:** indicators, descriptors, features

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Arg1 | VARCHAR | Feature/indicator name | feature_type, descriptor_name |
| Arg2 | VARCHAR | Feature value/count | feature_value, count |

**Notable values:**  
Arg1: `amino`, `cyanate`, `di10`, `di227`, `di23`, `di232`, `di260`, `di281`, `di48`, `di51`, `di64`, `di66`, `di67a`, `di8`, `ethoxy`, `halide10`, `methanol`, `methoxy`, `nitro`, `ring_size_4`  
Arg2: `1`–`20` (numeric values)

---

### PTE.pte_ketone
**Meaning:** Ketone functional groups (C=O)  
**Synonyms:** ketones, carbonyl groups

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Set | VARCHAR | Atom IDs forming ketone group | atom_set, atoms |

**Notable values:** d1, d109, d114, d123; sets like `[d1_22,d1_14,d1_13,d1_4]`

---

### PTE.pte_methoxy
**Meaning:** Methoxy functional groups (OCH₃)  
**Synonyms:** methoxy groups, methoxy moieties

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Set | VARCHAR | Atom IDs forming methoxy group | atom_set, atoms |

**Notable values:** d11, d122, d131, d137; sets like `[d11_13,d11_12,d11_14,d11_15,d11_16]`

---

### PTE.pte_methyl
**Meaning:** Methyl functional groups (CH₃)  
**Synonyms:** methyl groups, methyl moieties

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Set | VARCHAR | Atom IDs forming methyl group | atom_set, atoms |

**Notable values:** d107; sets like `[d107c_47,d107c_44,d107c_50,d107c_51,d107c_52]`

---

### PTE.pte_mutagenic
**Meaning:** Compounds classified as mutagenic  
**Synonyms:** mutagenic compounds, mutagens

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |

**Notable values:** d101, d104, d106, d107, d112

---

### PTE.pte_nitro
**Meaning:** Nitro functional groups (NO₂)  
**Synonyms:** nitro groups, nitro moieties

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Set | VARCHAR | Atom IDs forming nitro group | atom_set, atoms |

**Notable values:** d13, d16, d18, d127, d131; sets like `[d127_12,d127_5,d127_13,d127_14]`

---

### PTE.pte_non_ar_5c_ring
**Meaning:** Non-aromatic five-carbon rings  
**Synonyms:** non-aromatic 5-rings, alicyclic 5-rings

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Set | VARCHAR | Atom IDs forming ring | atom_set, atoms |

**Notable values:** d19, d89, d96, d101, d106, d112, d121, d128, d173, d231, d246, d249, d328

---

### PTE.pte_non_ar_6c_ring
**Meaning:** Non-aromatic six-carbon rings  
**Synonyms:** non-aromatic 6-rings, alicyclic 6-rings, cyclohexane rings

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Arg0 | VARCHAR | Drug identifier | drug_id, compound_id |
| Set | VARCHAR | Atom IDs forming ring | atom_set, atoms |

**Notable values:** d1, d10, d100; sets like `[d1_1,d1_2,d1_3,d1_4,d1_5,d1_6]`

---

### PTE.pte_non_ar_hetero_5_ring
**Meaning:** Non-aromatic five-membered rings with heteroatoms  
**Synonyms:** non-