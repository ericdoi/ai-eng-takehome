# Carcinogenesis Schema Reference Guide

## Schema Summary
The Carcinogenesis schema contains molecular structure and carcinogenicity classification data for chemical compounds, including atom properties, bond connectivity, and cancer class labels.

---

## Table Reference

### `Carcinogenesis.atom`
**Meaning:** Atomic composition of drug molecules; represents individual atoms within chemical structures.
**Synonyms:** atoms, atomic properties, atom features

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `atomid` | VARCHAR | Unique identifier for an atom within a drug | atom identifier, atom ID |
| `drug` | VARCHAR | Drug/compound identifier that contains this atom | drug ID, compound ID, molecule ID |
| `atomtype` | VARCHAR | Numeric classification of atom type (e.g., 22 = carbon, 3 = hydrogen) | atom class, atomic number, element type |
| `charge` | VARCHAR | Partial atomic charge binned into ranges | atomic charge, charge range, charge bin |
| `name` | VARCHAR | Chemical element symbol (e.g., 'c' = carbon, 'h' = hydrogen) | element, element symbol |

**Notable charge values:** `a0=-0_0175<x<=0_0615`, `a0=-0_1355<x<=-0_0175`, `a0=-inf<x<=-0_1355`, `a0=0_0615<x<=0_1375`, `a0=0_1375<x<=+inf`

---

### `Carcinogenesis.canc`
**Meaning:** Carcinogenicity classification labels for drugs; indicates whether a compound is carcinogenic.
**Synonyms:** carcinogenicity, cancer class, drug labels, classification

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `drug_id` | VARCHAR | Unique identifier for a drug/compound | drug ID, compound ID, molecule ID |
| `class` | VARCHAR | Binary carcinogenicity label (0 = non-carcinogenic, 1 = carcinogenic) | carcinogenic class, label, target, outcome |

**Notable class values:** `0`, `1`

---

### `Carcinogenesis.sbond_1`
**Meaning:** Single bonds (bond order 1) connecting atoms within drug molecules.
**Synonyms:** single bonds, bond type 1, aromatic bonds

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique bond record identifier | bond ID, record ID |
| `drug` | VARCHAR | Drug/compound containing this bond | drug ID, compound ID, molecule ID |
| `atomid` | VARCHAR | First atom identifier in the bond | atom 1, source atom |
| `atomid_2` | VARCHAR | Second atom identifier in the bond | atom 2, target atom |

---

### `Carcinogenesis.sbond_2`
**Meaning:** Double bonds (bond order 2) connecting atoms within drug molecules.
**Synonyms:** double bonds, bond type 2

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique bond record identifier | bond ID, record ID |
| `drug` | VARCHAR | Drug/compound containing this bond | drug ID, compound ID, molecule ID |
| `atomid` | VARCHAR | First atom identifier in the bond | atom 1, source atom |
| `atomid_2` | VARCHAR | Second atom identifier in the bond | atom 2, target atom |

---

### `Carcinogenesis.sbond_3`
**Meaning:** Triple bonds (bond order 3) connecting atoms within drug molecules.
**Synonyms:** triple bonds, bond type 3

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique bond record identifier | bond ID, record ID |
| `drug` | VARCHAR | Drug/compound containing this bond | drug ID, compound ID, molecule ID |
| `atomid` | VARCHAR | First atom identifier in the bond | atom 1, source atom |
| `atomid_2` | VARCHAR | Second atom identifier in the bond | atom 2, target atom |

**Notable drug values:** `d130`, `d262`, `d321`, `d98`

---

### `Carcinogenesis.sbond_7`
**Meaning:** Aromatic bonds (bond order 7) connecting atoms within drug molecules.
**Synonyms:** aromatic bonds, bond type 7

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique bond record identifier | bond ID, record ID |
| `drug` | VARCHAR | Drug/compound containing this bond | drug ID, compound ID, molecule ID |
| `atomid` | VARCHAR | First atom identifier in the bond | atom 1, source atom |
| `atomid_2` | VARCHAR | Second atom identifier in the bond | atom 2, target atom |

---

## Join Paths

**Atoms to Carcinogenicity:**
```sql
Carcinogenesis.atom a
JOIN Carcinogenesis.canc c ON a.drug = c.drug_id
```

**Atoms to Single Bonds:**
```sql
Carcinogenesis.atom a
JOIN Carcinogenesis.sbond_1 b ON a.atomid = b.atomid AND a.drug = b.drug
```

**Atoms to Double Bonds:**
```sql
Carcinogenesis.atom a
JOIN Carcinogenesis.sbond_2 b ON a.atomid = b.atomid AND a.drug = b.drug
```

**Atoms to Triple Bonds:**
```sql
Carcinogenesis.atom a
JOIN Carcinogenesis.sbond_3 b ON a.atomid = b.atomid AND a.drug = b.drug
```

**Atoms to Aromatic Bonds:**
```sql
Carcinogenesis.atom a
JOIN Carcinogenesis.sbond_7 b ON a.atomid = b.atomid AND a.drug = b.drug
```

**Bond Endpoints to Atoms (for bond analysis):**
```sql
Carcinogenesis.sbond_1 b
JOIN Carcinogenesis.atom a1 ON b.atomid = a1.atomid AND b.drug = a1.drug
JOIN Carcinogenesis.atom a2 ON b.atomid_2 = a2.atomid AND b.drug = a2.drug
```

---

## Business Rules as SQL

**Rule: Identify carcinogenic compounds**
```sql
WHERE c.class = 1
```

**Rule: Identify non-carcinogenic compounds**
```sql
WHERE c.class = 0
```

**Rule: Find atoms with positive charge**
```sql
WHERE a.charge IN ('a0=0_0615<x<=0_1375', 'a0=0_1375<x<=+inf')
```

**Rule: Find atoms with negative charge**
```sql
WHERE a.charge IN ('a0=-inf<x<=-0_1355', 'a0=-0_1355<x<=-0_0175')
```

**Rule: Find atoms with near-zero charge**
```sql
WHERE a.charge = 'a0=-0_0175<x<=0_0615'
```

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| carcinogenic drug | `canc.class = 1` |
| non-carcinogenic drug | `canc.class = 0` |
| drug atoms | `atom.drug` |
| atom type | `atom.atomtype` |
| element symbol | `atom.name` |
| atomic charge | `atom.charge` |
| single bond | `sbond_1` table |
| double bond | `sbond_2` table |
| triple bond | `sbond_3` table |
| aromatic bond | `sbond_7` table |
| bonded atoms | `sbond_*.atomid`, `sbond_*.atomid_2` |
| carbon atom | `atom.name = 'c'` |
| hydrogen atom | `atom.name = 'h'` |
| molecule structure | `atom` + `sbond_*` tables joined on `drug` |
| compound classification | `canc.class` |