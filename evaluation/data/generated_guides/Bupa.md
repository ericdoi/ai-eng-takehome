# Bupa Schema Reference Guide

## Schema Summary
The Bupa schema contains medical test results and liver function indicators for individuals, with measurements including alkaline phosphatase, gamma-glutamyl transferase, mean corpuscular volume, serum glutamic-oxaloacetic transaminase, serum glutamic-pyruvic transaminase, and alcohol consumption data.

---

## Table Reference

### `Bupa.alkphos`
**Meaning:** Alkaline phosphatase test results (liver enzyme measurement)  
**Synonyms:** ALP, alkaline phosphatase levels

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `arg1` | VARCHAR | Individual identifier | ID, person ID, subject ID |
| `arg2` | BIGINT | Alkaline phosphatase value (units/L) | ALP value, enzyme level |

**Notable values:** arg1 contains identifiers like `T1`, `T10`, `T100`, `T101`, `T102`

---

### `Bupa.bupa`
**Meaning:** Primary dataset linking individuals to a binary classification (likely liver disease indicator)  
**Synonyms:** Main table, classification table, disease status

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `arg1` | VARCHAR | Individual identifier | ID, person ID, subject ID |
| `arg2` | VARCHAR | Classification flag | Status, indicator, class, disease_flag |

**Notable values:** arg2 contains `F` (false/negative), `T` (true/positive)

---

### `Bupa.bupa_name`
**Meaning:** Reference list of valid individual identifiers  
**Synonyms:** ID reference, name lookup, identifier list

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `arg1` | VARCHAR | Individual identifier | ID, person ID, subject ID |

**Notable values:** arg1 contains identifiers like `T1`, `T10`, `T100`, `T101`, `T102`

---

### `Bupa.bupa_type`
**Meaning:** Reference list of valid classification values  
**Synonyms:** Type reference, classification reference, status values

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `arg1` | VARCHAR | Valid classification value | Type, status, class |

**Notable values:** arg1 contains `F`, `T`

---

### `Bupa.drinks`
**Meaning:** Alcohol consumption data per individual  
**Synonyms:** Alcohol intake, drinking frequency, consumption level

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `arg1` | VARCHAR | Individual identifier | ID, person ID, subject ID |
| `arg2` | DOUBLE | Alcohol consumption (drinks per day or frequency) | Consumption amount, intake level, frequency |

**Notable values:** arg2 ranges from `0.0` to `3.0`

---

### `Bupa.gammagt`
**Meaning:** Gamma-glutamyl transferase test results (liver enzyme measurement)  
**Synonyms:** GGT, gamma-GT, gamma-glutamyl transpeptidase

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `arg1` | VARCHAR | Individual identifier | ID, person ID, subject ID |
| `arg2` | BIGINT | Gamma-glutamyl transferase value (units/L) | GGT value, enzyme level |

**Notable values:** arg2 ranges from `5` to `81`

---

### `Bupa.mcv`
**Meaning:** Mean corpuscular volume test results (red blood cell size measurement)  
**Synonyms:** MCV, mean cell volume, RBC volume

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `arg1` | VARCHAR | Individual identifier | ID, person ID, subject ID |
| `arg2` | BIGINT | Mean corpuscular volume value (femtoliters) | MCV value, cell volume |

**Notable values:** arg2 ranges from `85` to `92`

---

### `Bupa.sgot`
**Meaning:** Serum glutamic-oxaloacetic transaminase test results (liver enzyme measurement)  
**Synonyms:** SGOT, AST, aspartate aminotransferase

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `arg1` | VARCHAR | Individual identifier | ID, person ID, subject ID |
| `arg2` | BIGINT | SGOT value (units/L) | AST value, enzyme level |

**Notable values:** arg2 ranges from `13` to `27`

---

### `Bupa.sgpt`
**Meaning:** Serum glutamic-pyruvic transaminase test results (liver enzyme measurement)  
**Synonyms:** SGPT, ALT, alanine aminotransferase

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `arg1` | VARCHAR | Individual identifier | ID, person ID, subject ID |
| `arg2` | BIGINT | SGPT value (units/L) | ALT value, enzyme level |

**Notable values:** arg2 ranges from `18` to `45`

---

## Join Paths

**All measurement tables to main dataset:**
```sql
Bupa.bupa.arg1 = Bupa.alkphos.arg1
Bupa.bupa.arg1 = Bupa.gammagt.arg1
Bupa.bupa.arg1 = Bupa.mcv.arg1
Bupa.bupa.arg1 = Bupa.sgot.arg1
Bupa.bupa.arg1 = Bupa.sgpt.arg1
Bupa.bupa.arg1 = Bupa.drinks.arg1
```

**Identifier validation:**
```sql
Bupa.bupa.arg1 IN (SELECT arg1 FROM Bupa.bupa_name)
Bupa.bupa.arg2 IN (SELECT arg1 FROM Bupa.bupa_type)
```

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| Individual/person/subject | `arg1` (VARCHAR identifier) |
| Positive/disease present/affected | `WHERE arg2 = 'T'` |
| Negative/disease absent/unaffected | `WHERE arg2 = 'F'` |
| Alkaline phosphatase level | `Bupa.alkphos.arg2` |
| GGT level | `Bupa.gammagt.arg2` |
| MCV level | `Bupa.mcv.arg2` |
| SGOT/AST level | `Bupa.sgot.arg2` |
| SGPT/ALT level | `Bupa.sgpt.arg2` |
| Alcohol consumption | `Bupa.drinks.arg2` |
| High drinker | `WHERE Bupa.drinks.arg2 >= 2.0` |
| Non-drinker | `WHERE Bupa.drinks.arg2 = 0.0` |