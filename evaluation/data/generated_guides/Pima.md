# Pima Schema Reference Guide

## Schema Summary
The Pima schema contains medical and demographic measurements for individuals, organized as separate tables keyed by patient identifier, supporting analysis of health metrics and diabetes indicators.

## Join Paths

All patient records are joined via `arg1` (patient identifier). Standard join pattern:

```sql
FROM Pima.pima p
JOIN Pima.age a ON p.arg1 = a.arg1
JOIN Pima.bmi b ON p.arg1 = b.arg1
JOIN Pima.plasma pl ON p.arg1 = pl.arg1
JOIN Pima.diastolic d ON p.arg1 = d.arg1
JOIN Pima.serum s ON p.arg1 = s.arg1
JOIN Pima.tricepts t ON p.arg1 = t.arg1
JOIN Pima.numPreg np ON p.arg1 = np.arg1
JOIN Pima.pedigree pd ON p.arg1 = pd.arg1
```

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| patient ID | `arg1` (VARCHAR identifier) |
| diabetes status | `Pima.pima.arg2` (F/T) |
| age (years) | `Pima.age.arg2` |
| BMI | `Pima.bmi.arg2` |
| blood pressure (diastolic) | `Pima.diastolic.arg2` |
| pregnancies | `Pima.numPreg.arg2` |
| family history score | `Pima.pedigree.arg2` |
| glucose level | `Pima.plasma.arg2` |
| insulin level | `Pima.serum.arg2` |
| triceps skinfold | `Pima.tricepts.arg2` |

## Table Reference

### `Pima.pima`
Diabetes diagnosis indicator per patient.
- **arg1**: Patient identifier (VARCHAR)
- **arg2**: Diabetes status — enumerated values: `T` (positive), `F` (negative)

### `Pima.age`
Patient age in years.
- **arg1**: Patient identifier (VARCHAR)
- **arg2**: Age (DOUBLE)

### `Pima.bmi`
Body Mass Index.
- **arg1**: Patient identifier (VARCHAR)
- **arg2**: BMI value (DOUBLE); note: 0.0 indicates missing/invalid data

### `Pima.plasma`
Fasting plasma glucose concentration (mg/dL).
- **arg1**: Patient identifier (VARCHAR)
- **arg2**: Glucose level (DOUBLE)

### `Pima.diastolic`
Diastolic blood pressure (mmHg).
- **arg1**: Patient identifier (VARCHAR)
- **arg2**: Diastolic pressure (DOUBLE)

### `Pima.serum`
Serum insulin level (mu U/ml).
- **arg1**: Patient identifier (VARCHAR)
- **arg2**: Insulin level (DOUBLE); note: 0.0 indicates missing/invalid data

### `Pima.tricepts`
Triceps skinfold thickness (mm).
- **arg1**: Patient identifier (VARCHAR)
- **arg2**: Skinfold thickness (DOUBLE); note: 0.0 indicates missing/invalid data

### `Pima.numPreg`
Number of pregnancies.
- **arg1**: Patient identifier (VARCHAR)
- **arg2**: Pregnancy count (DOUBLE)

### `Pima.pedigree`
Diabetes pedigree function (family history score).
- **arg1**: Patient identifier (VARCHAR)
- **arg2**: Pedigree score (DOUBLE)