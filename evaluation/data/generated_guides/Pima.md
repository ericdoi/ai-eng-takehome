# Pima Schema Reference Guide

## Schema Summary
The Pima schema contains medical and demographic measurements for individuals identified by patient codes, organized across nine normalized tables with a common patient identifier.

---

## Table Reference

### Pima.age
**Meaning:** Patient age in years  
**Synonyms:** years, patient age, age in years

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| arg1 | VARCHAR | Patient identifier | patient ID, ID, code |
| arg2 | DOUBLE | Age value | years, age |

---

### Pima.bmi
**Meaning:** Body Mass Index measurement  
**Synonyms:** body mass index, BMI

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| arg1 | VARCHAR | Patient identifier | patient ID, ID, code |
| arg2 | DOUBLE | BMI value | body mass index, BMI |

---

### Pima.diastolic
**Meaning:** Diastolic blood pressure measurement  
**Synonyms:** diastolic pressure, blood pressure diastolic

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| arg1 | VARCHAR | Patient identifier | patient ID, ID, code |
| arg2 | DOUBLE | Diastolic pressure in mmHg | diastolic, pressure |

---

### Pima.numPreg
**Meaning:** Number of pregnancies  
**Synonyms:** pregnancies, pregnancy count, number of pregnancies

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| arg1 | VARCHAR | Patient identifier | patient ID, ID, code |
| arg2 | DOUBLE | Count of pregnancies | pregnancies, count |

---

### Pima.pedigree
**Meaning:** Diabetes pedigree function score  
**Synonyms:** pedigree function, diabetes pedigree, family history score

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| arg1 | VARCHAR | Patient identifier | patient ID, ID, code |
| arg2 | DOUBLE | Pedigree function value | score, pedigree score |

---

### Pima.pima
**Meaning:** Diabetes diagnosis outcome  
**Synonyms:** diagnosis, outcome, diabetes status, result

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| arg1 | VARCHAR | Patient identifier | patient ID, ID, code |
| arg2 | VARCHAR | Diagnosis result | outcome, status, result |

**Enumeration:** `T` (positive/true), `F` (negative/false)

---

### Pima.plasma
**Meaning:** Plasma glucose concentration  
**Synonyms:** glucose, plasma glucose, blood glucose

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| arg1 | VARCHAR | Patient identifier | patient ID, ID, code |
| arg2 | DOUBLE | Plasma glucose in mg/dL | glucose, concentration |

---

### Pima.serum
**Meaning:** Serum insulin measurement  
**Synonyms:** insulin, serum insulin, insulin level

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| arg1 | VARCHAR | Patient identifier | patient ID, ID, code |
| arg2 | DOUBLE | Serum insulin in mu U/ml | insulin, level |

---

### Pima.tricepts
**Meaning:** Triceps skin fold thickness measurement  
**Synonyms:** triceps, skin fold, triceps thickness

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| arg1 | VARCHAR | Patient identifier | patient ID, ID, code |
| arg2 | DOUBLE | Triceps thickness in mm | thickness, measurement |

---

## Join Paths

All tables join on patient identifier using the common column `arg1`:

```sql
Pima.age a
JOIN Pima.bmi b ON a.arg1 = b.arg1
JOIN Pima.diastolic d ON a.arg1 = d.arg1
JOIN Pima.numPreg np ON a.arg1 = np.arg1
JOIN Pima.pedigree p ON a.arg1 = p.arg1
JOIN Pima.pima pi ON a.arg1 = pi.arg1
JOIN Pima.plasma pl ON a.arg1 = pl.arg1
JOIN Pima.serum s ON a.arg1 = s.arg1
JOIN Pima.tricepts t ON a.arg1 = t.arg1
```

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| patient age | `Pima.age.arg2` |
| BMI | `Pima.bmi.arg2` |
| diastolic pressure | `Pima.diastolic.arg2` |
| pregnancies | `Pima.numPreg.arg2` |
| pedigree score | `Pima.pedigree.arg2` |
| diabetes positive | `Pima.pima.arg2 = 'T'` |
| diabetes negative | `Pima.pima.arg2 = 'F'` |
| glucose | `Pima.plasma.arg2` |
| insulin | `Pima.serum.arg2` |
| skin fold thickness | `Pima.tricepts.arg2` |
| patient ID | `arg1` (any table) |