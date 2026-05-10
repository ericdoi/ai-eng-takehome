# FNHK Schema Reference Guide

## Schema Summary
This schema contains Czech healthcare hospitalization records with patient demographics, diagnoses, DRG classifications, and associated medical procedures and costs.

---

## Join Paths

**Cases to procedures:**
```sql
FROM FNHK.pripady p
JOIN FNHK.vykony v ON p.Identifikace_pripadu = v.Identifikace_pripadu
```

**Cases to supplies/materials:**
```sql
FROM FNHK.pripady p
JOIN FNHK.zup z ON p.Identifikace_pripadu = z.Identifikace_pripadu
```

**All case data (procedures + supplies):**
```sql
FROM FNHK.pripady p
LEFT JOIN FNHK.vykony v ON p.Identifikace_pripadu = v.Identifikace_pripadu
LEFT JOIN FNHK.zup z ON p.Identifikace_pripadu = z.Identifikace_pripadu
```

---

## Table Reference

### `FNHK.pripady`
Hospitalization cases with patient and clinical classification.

| Column | Semantics |
|--------|-----------|
| `Identifikace_pripadu` | Case identifier; foreign key to `vykony` and `zup` |
| `Identifikator_pacienta` | Patient identifier (may appear in multiple cases) |
| `Kod_zdravotni_pojistovny` | Health insurance provider code |
| `Datum_prijeti` | Admission date |
| `Datum_propusteni` | Discharge date |
| `Delka_hospitalizace` | Length of stay in days |
| `Vekovy_Interval_Pacienta` | Patient age bracket; enum: `0-10`, `10-20`, `20-30`, `30-40`, `40-50`, `50-60`, `60-70`, `70-80`, `80+` |
| `Pohlavi_pacienta` | Patient sex; enum: `F` (female), `M` (male) |
| `Zakladni_diagnoza` | Primary diagnosis code (ICD-10 format) |
| `Seznam_vedlejsich_diagnoz` | Secondary diagnoses (space-separated ICD-10 codes) |
| `DRG_skupina` | DRG (Diagnosis-Related Group) classification code |
| `PSC` | Postal code (patient residence) |

### `FNHK.vykony`
Medical procedures and services performed during hospitalization.

| Column | Semantics |
|--------|-----------|
| `Identifikace_pripadu` | Foreign key to `pripady` |
| `Datum_provedeni_vykonu` | Procedure date |
| `Typ_polozky` | Procedure type code (e.g., `0` for standard procedures) |
| `Kod_polozky` | Procedure code identifier |
| `Pocet` | Quantity of procedure performed |
| `Body` | Points/credits assigned to procedure (reimbursement basis) |

### `FNHK.zup`
Supplies, materials, and drugs used during hospitalization.

| Column | Semantics |
|--------|-----------|
| `Identifikace_pripadu` | Foreign key to `pripady` |
| `Datum_provedeni_vykonu` | Supply/material date |
| `Typ_polozky` | Supply type code (e.g., `1` for drugs, `3` for materials) |
| `Kod_polozky` | Supply/material code identifier |
| `Pocet` | Quantity (decimal; may represent units or weight) |
| `Cena` | Unit or total price in CZK |

---

## Synonym Glossary

| Common Term | Schema Reference |
|-------------|------------------|
| hospitalization case | `FNHK.pripady.Identifikace_pripadu` |
| admission | `FNHK.pripady.Datum_prijeti` |
| discharge | `FNHK.pripady.Datum_propusteni` |
| stay length | `FNHK.pripady.Delka_hospitalizace` |
| primary diagnosis | `FNHK.pripady.Zakladni_diagnoza` |
| comorbidities | `FNHK.pripady.Seznam_vedlejsich_diagnoz` |
| DRG code | `FNHK.pripady.DRG_skupina` |
| procedure | `FNHK.vykony` |
| supply/material/drug | `FNHK.zup` |
| insurance provider | `FNHK.pripady.Kod_zdravotni_pojistovny` |