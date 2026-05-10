# FNHK Schema Reference Guide

## Schema Summary
The FNHK schema contains Czech healthcare hospitalization records, including patient cases (pripady), medical procedures performed (vykony), and pharmaceutical/material supplies used (zup).

---

## Table Reference

### Table: `FNHK.pripady`
**Meaning:** Hospital admission cases; patient hospitalization episodes.
**Synonyms:** cases, admissions, episodes, hospitalizations

| Column Name | Type | Meaning | Synonyms |
|---|---|---|---|
| `Identifikace_pripadu` | BIGINT | Unique case identifier | case ID, case number |
| `Identifikator_pacienta` | BIGINT | Unique patient identifier | patient ID, patient number |
| `Kod_zdravotni_pojistovny` | BIGINT | Health insurance provider code | insurance code, payer code |
| `Datum_prijeti` | DATE | Hospital admission date | admission date, check-in date |
| `Datum_propusteni` | DATE | Hospital discharge date | discharge date, check-out date |
| `Delka_hospitalizace` | BIGINT | Length of hospital stay in days | stay length, LOS, hospitalization days |
| `Vekovy_Interval_Pacienta` | VARCHAR | Patient age group bracket | age group, age interval, age bracket |
| `Pohlavi_pacienta` | VARCHAR | Patient biological sex | gender, sex |
| `Zakladni_diagnoza` | VARCHAR | Primary diagnosis code | primary diagnosis, main diagnosis |
| `Seznam_vedlejsich_diagnoz` | VARCHAR | Secondary/comorbid diagnosis codes (space-separated) | secondary diagnoses, comorbidities, additional diagnoses |
| `DRG_skupina` | BIGINT | Diagnosis-Related Group classification | DRG code, DRG group |
| `PSC` | VARCHAR | Postal code (Czech: poštovní směrovací číslo) | zip code, postal code |

**Enumerated Values:**
- `Vekovy_Interval_Pacienta`: `0-10`, `10-20`, `20-30`, `30-40`, `40-50`, `50-60`, `60-70`, `70-80`, `80+`
- `Pohlavi_pacienta`: `F` (female), `M` (male)

---

### Table: `FNHK.vykony`
**Meaning:** Medical procedures and services performed during hospitalization.
**Synonyms:** procedures, services, medical acts, interventions

| Column Name | Type | Meaning | Synonyms |
|---|---|---|---|
| `Identifikace_pripadu` | BIGINT | Reference to case in pripady table | case ID |
| `Datum_provedeni_vykonu` | DATE | Date procedure was performed | procedure date, service date |
| `Typ_polozky` | BIGINT | Procedure type/category code | item type, procedure type |
| `Kod_polozky` | BIGINT | Procedure code identifier | procedure code, service code |
| `Pocet` | BIGINT | Quantity of procedures performed | count, number, quantity |
| `Body` | BIGINT | Points/credits assigned to procedure | points, credits, score |

---

### Table: `FNHK.zup`
**Meaning:** Pharmaceutical and material supplies (Czech: zdravotnický a zdravotnický materiál) used during hospitalization.
**Synonyms:** supplies, medications, materials, drugs, pharmaceuticals

| Column Name | Type | Meaning | Synonyms |
|---|---|---|---|
| `Identifikace_pripadu` | BIGINT | Reference to case in pripady table | case ID |
| `Datum_provedeni_vykonu` | DATE | Date supply was used/administered | supply date, usage date |
| `Typ_polozky` | BIGINT | Supply type/category code | item type, supply type |
| `Kod_polozky` | BIGINT | Supply code identifier | supply code, item code |
| `Pocet` | DOUBLE | Quantity of supply used | count, amount, quantity |
| `Cena` | DOUBLE | Unit price or total cost in Czech koruna (CZK) | price, cost, amount |

---

## Join Paths

**vykony → pripady:**
```sql
INNER JOIN FNHK.pripady p ON v.Identifikace_pripadu = p.Identifikace_pripadu
```

**zup → pripady:**
```sql
INNER JOIN FNHK.pripady p ON z.Identifikace_pripadu = p.Identifikace_pripadu
```

**vykony ↔ zup (via pripady):**
```sql
INNER JOIN FNHK.vykony v ON z.Identifikace_pripadu = v.Identifikace_pripadu
```

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|---|---|
| patient age group | `pripady.Vekovy_Interval_Pacienta` |
| patient sex/gender | `pripady.Pohlavi_pacienta` |
| admission date | `pripady.Datum_prijeti` |
| discharge date | `pripady.Datum_propusteni` |
| length of stay | `pripady.Delka_hospitalizace` |
| primary diagnosis | `pripady.Zakladni_diagnoza` |
| secondary diagnoses | `pripady.Seznam_vedlejsich_diagnoz` |
| DRG classification | `pripady.DRG_skupina` |
| insurance provider | `pripady.Kod_zdravotni_pojistovny` |
| procedure points/credits | `vykony.Body` |
| procedure quantity | `vykony.Pocet` |
| supply cost | `zup.Cena` |
| supply quantity | `zup.Pocet` |
| female patients | `WHERE pripady.Pohlavi_pacienta = 'F'` |
| male patients | `WHERE pripady.Pohlavi_pacienta = 'M'` |
| elderly patients (60+) | `WHERE pripady.Vekovy_Interval_Pacienta IN ('60-70', '70-80', '80+')` |
| pediatric patients (0-10) | `WHERE pripady.Vekovy_Interval_Pacienta = '0-10'` |