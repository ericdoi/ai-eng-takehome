# Hepatitis_std Schema Reference Guide

## Schema Summary
This schema contains clinical hepatitis patient data with biometric measurements, demographic information, laboratory indicators, infection details, and relationships linking patients to their records.

---

## Join Paths

**Patient → Demographics:**
```sql
FROM Hepatitis_std.Bio b
JOIN Hepatitis_std.rel11 r ON b.b_id = r.b_id
JOIN Hepatitis_std.dispat d ON r.m_id = d.m_id
```

**Patient → Laboratory Indicators:**
```sql
FROM Hepatitis_std.dispat d
JOIN Hepatitis_std.rel12 r ON d.m_id = r.m_id
JOIN Hepatitis_std.indis i ON r.in_id = i.in_id
```

**Patient → Infection Data:**
```sql
FROM Hepatitis_std.dispat d
JOIN Hepatitis_std.rel13 r ON d.m_id = r.m_id
JOIN Hepatitis_std.inf f ON r.a_id = f.a_id
```

**Complete Patient Profile:**
```sql
FROM Hepatitis_std.dispat d
LEFT JOIN Hepatitis_std.rel11 r11 ON d.m_id = r11.m_id
LEFT JOIN Hepatitis_std.Bio b ON r11.b_id = b.b_id
LEFT JOIN Hepatitis_std.rel12 r12 ON d.m_id = r12.m_id
LEFT JOIN Hepatitis_std.indis i ON r12.in_id = i.in_id
LEFT JOIN Hepatitis_std.rel13 r13 ON d.m_id = r13.m_id
LEFT JOIN Hepatitis_std.inf f ON r13.a_id = f.a_id
```

---

## Table Reference

### `Hepatitis_std.Bio`
**Meaning:** Biometric/fibrosis assessment data  
**Synonyms:** biopsy, fibrosis staging

| Column | Type | Values | Notes |
|--------|------|--------|-------|
| `fibros` | VARCHAR | 0, 1, 2, 3, 4 | Fibrosis stage (0=none to 4=cirrhosis) |
| `activity` | VARCHAR | 0, 1, 2, 3, 4 | Inflammation/activity grade |
| `b_id` | BIGINT | — | Primary key; links via `Hepatitis_std.rel11.b_id` |

---

### `Hepatitis_std.dispat`
**Meaning:** Patient demographic and classification data  
**Synonyms:** patient, demographics, patient record

| Column | Type | Values | Notes |
|--------|------|--------|-------|
| `m_id` | BIGINT | — | Primary key; central patient identifier |
| `sex` | VARCHAR | 0, 1 | 0=female, 1=male |
| `age` | VARCHAR | 0, 1, 2, 3, 4, 5, 6 | Age group/category |
| `Type` | VARCHAR | 0, 1 | Hepatitis type classification |

---

### `Hepatitis_std.indis`
**Meaning:** Laboratory indicator/test results  
**Synonyms:** lab results, indicators, biochemistry

| Column | Type | Values | Notes |
|--------|------|--------|-------|
| `got` | VARCHAR | 0, 1, 2, 3, 4 | Glutamic-oxaloacetic transaminase level |
| `gpt` | VARCHAR | 0, 1, 2, 3 | Glutamic-pyruvic transaminase level |
| `alb` | VARCHAR | 0, 1 | Albumin level |
| `tbil` | VARCHAR | 0, 1 | Total bilirubin level |
| `dbil` | VARCHAR | 0, 1 | Direct bilirubin level |
| `che` | VARCHAR | 0–9 | Cholinesterase level |
| `ttt` | VARCHAR | 0, 1, 2, 3, 4, 5 | Thymol turbidity test |
| `ztt` | VARCHAR | 0, 1, 2, 3, 4, 5 | Zinc sulfate turbidity test |
| `tcho` | VARCHAR | 0, 1, 2, 3 | Total cholesterol level |
| `tp` | VARCHAR | 0, 1, 2, 3 | Total protein level |
| `in_id` | BIGINT | — | Primary key; links via `Hepatitis_std.rel12.in_id` |

---

### `Hepatitis_std.inf`
**Meaning:** Infection/disease duration data  
**Synonyms:** infection, duration, disease course

| Column | Type | Values | Notes |
|--------|------|--------|-------|
| `dur` | VARCHAR | 0, 1, 2, 3, 4 | Disease duration category |
| `a_id` | BIGINT | — | Primary key; links via `Hepatitis_std.rel13.a_id` |

---

### `Hepatitis_std.rel11`
**Meaning:** Links biometric data to patients  
**Synonyms:** bio-patient relationship

| Column | Type | Notes |
|--------|------|-------|
| `b_id` | BIGINT | Foreign key to `Hepatitis_std.Bio.b_id` |
| `m_id` | BIGINT | Foreign key to `Hepatitis_std.dispat.m_id` |

---

### `Hepatitis_std.rel12`
**Meaning:** Links laboratory indicators to patients  
**Synonyms:** lab-patient relationship

| Column | Type | Notes |
|--------|------|-------|
| `in_id` | BIGINT | Foreign key to `Hepatitis_std.indis.in_id` |
| `m_id` | BIGINT | Foreign key to `Hepatitis_std.dispat.m_id` |

---

### `Hepatitis_std.rel13`
**Meaning:** Links infection data to patients  
**Synonyms:** infection-patient relationship

| Column | Type | Notes |
|--------|------|-------|
| `a_id` | BIGINT | Foreign key to `Hepatitis_std.inf.a_id` |
| `m_id` | BIGINT | Foreign key to `Hepatitis_std.dispat.m_id` |