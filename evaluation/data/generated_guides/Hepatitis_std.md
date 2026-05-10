# Hepatitis_std Schema Reference Guide

## 1. Schema Summary

The `Hepatitis_std` schema contains clinical and laboratory data for hepatitis patients, including demographic information, diagnostic indices, biopsy results, infection duration, and relationships linking patients to their associated records.

---

## 2. Table Reference

### Table: `Hepatitis_std.Bio`
**Meaning:** Biopsy results; histological assessment of liver tissue.  
**Synonyms:** Biopsy, Histology, Fibrosis staging

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `fibros` | VARCHAR | Fibrosis stage (0–4 scale) | Fibrosis stage, Fibrosis score |
| `activity` | VARCHAR | Inflammatory activity (0–4 scale) | Activity score, Inflammation grade |
| `b_id` | BIGINT | Biopsy record identifier (primary key) | Biopsy ID |

**Notable values:** `fibros` and `activity` each range 0–4.

---

### Table: `Hepatitis_std.dispat`
**Meaning:** Demographic and patient classification data.  
**Synonyms:** Demographics, Patient, Patient master

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `m_id` | BIGINT | Master patient identifier (primary key) | Patient ID, Master ID |
| `sex` | VARCHAR | Biological sex (0=female, 1=male) | Gender, Sex code |
| `age` | VARCHAR | Age group (0–6 scale) | Age category, Age band |
| `Type` | VARCHAR | Patient type or disease classification (0 or 1) | Patient type, Classification |

**Notable values:** `sex` ∈ {0, 1}; `age` ∈ {0, 1, 2, 3, 4, 5, 6}; `Type` ∈ {0, 1}.

---

### Table: `Hepatitis_std.indis`
**Meaning:** Laboratory indices and diagnostic test results.  
**Synonyms:** Lab results, Indices, Laboratory tests, Diagnostic markers

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `got` | VARCHAR | Glutamic-oxaloacetic transaminase (0–4 scale) | GOT, AST equivalent |
| `gpt` | VARCHAR | Glutamic-pyruvic transaminase (0–3 scale) | GPT, ALT equivalent |
| `alb` | VARCHAR | Albumin level (0–1 scale) | Albumin |
| `tbil` | VARCHAR | Total bilirubin (0–1 scale) | Total bilirubin |
| `dbil` | VARCHAR | Direct bilirubin (0–1 scale) | Direct bilirubin |
| `che` | VARCHAR | Cholinesterase (0–9 scale) | Cholinesterase, CHE |
| `ttt` | VARCHAR | Thymol turbidity test (0–5 scale) | TTT, Thymol turbidity |
| `ztt` | VARCHAR | Zinc sulfate turbidity test (0–5 scale) | ZTT, Zinc sulfate turbidity |
| `tcho` | VARCHAR | Total cholesterol (0–3 scale) | Total cholesterol, TCHO |
| `tp` | VARCHAR | Total protein (0–3 scale) | Total protein, TP |
| `in_id` | BIGINT | Indices record identifier (primary key) | Indices ID |

**Notable values:** All columns are categorical/ordinal scales; ranges vary per test.

---

### Table: `Hepatitis_std.inf`
**Meaning:** Infection duration or disease progression data.  
**Synonyms:** Infection, Duration, Disease progression

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `dur` | VARCHAR | Duration category (0–4 scale) | Duration, Duration category |
| `a_id` | BIGINT | Infection/assessment record identifier (primary key) | Assessment ID, Infection ID |

**Notable values:** `dur` ∈ {0, 1, 2, 3, 4}.

---

### Table: `Hepatitis_std.rel11`
**Meaning:** Relationship linking biopsy records to master patients.  
**Synonyms:** Biopsy–patient link, Bio–dispat relationship

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `b_id` | BIGINT | Biopsy record identifier (foreign key to `Bio.b_id`) | Biopsy ID |
| `m_id` | BIGINT | Master patient identifier (foreign key to `dispat.m_id`) | Patient ID, Master ID |

---

### Table: `Hepatitis_std.rel12`
**Meaning:** Relationship linking laboratory indices to master patients.  
**Synonyms:** Indices–patient link, Indis–dispat relationship

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `in_id` | BIGINT | Indices record identifier (foreign key to `indis.in_id`) | Indices ID |
| `m_id` | BIGINT | Master patient identifier (foreign key to `dispat.m_id`) | Patient ID, Master ID |

---

### Table: `Hepatitis_std.rel13`
**Meaning:** Relationship linking infection/assessment records to master patients.  
**Synonyms:** Infection–patient link, Inf–dispat relationship

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `a_id` | BIGINT | Infection/assessment record identifier (foreign key to `inf.a_id`) | Assessment ID, Infection ID |
| `m_id` | BIGINT | Master patient identifier (foreign key to `dispat.m_id`) | Patient ID, Master ID |

---

## 3. Join Paths

**Biopsy to Patient:**
```sql
Bio b
INNER JOIN rel11 r11 ON b.b_id = r11.b_id
INNER JOIN dispat d ON r11.m_id = d.m_id
```

**Indices to Patient:**
```sql
indis i
INNER JOIN rel12 r12 ON i.in_id = r12.in_id
INNER JOIN dispat d ON r12.m_id = d.m_id
```

**Infection to Patient:**
```sql
inf f
INNER JOIN rel13 r13 ON f.a_id = r13.a_id
INNER JOIN dispat d ON r13.m_id = d.m_id
```

**All three data types to Patient (via master patient):**
```sql
dispat d
LEFT JOIN rel11 r11 ON d.m_id = r11.m_id
LEFT JOIN Bio b ON r11.b_id = b.b_id
LEFT JOIN rel12 r12 ON d.m_id = r12.m_id
LEFT JOIN indis i ON r12.in_id = i.in_id
LEFT JOIN rel13 r13 ON d.m_id = r13.m_id
LEFT JOIN inf f ON r13.a_id = f.a_id
```

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation. All columns are categorical/ordinal scales; validation of value ranges should reference the enumeration lists above.

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| Patient | `dispat.m_id` |
| Patient ID | `dispat.m_id` |
| Male patient | `WHERE dispat.sex = '1'` |
| Female patient | `WHERE dispat.sex = '0'` |
| Fibrosis stage | `Bio.fibros` |
| Inflammation | `Bio.activity` |
| Liver enzyme (AST) | `indis.got` |
| Liver enzyme (ALT) | `indis.gpt` |
| Bilirubin | `indis.tbil` or `indis.dbil` |
| Albumin | `indis.alb` |
| Cholinesterase | `indis.che` |
| Protein | `indis.tp` |
| Cholesterol | `indis.tcho` |
| Infection duration | `inf.dur` |
| Disease type | `dispat.Type` |
| Age group | `dispat.age` |
| Biopsy result | `Bio` table |
| Lab result | `indis` table |
| Patient demographics | `dispat` table |