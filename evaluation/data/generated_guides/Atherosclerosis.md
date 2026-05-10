# Atherosclerosis Schema Reference Guide

## Schema Summary
Longitudinal cardiovascular disease study tracking control subjects with baseline entry data, periodic follow-up measurements, clinical events, and mortality outcomes.

---

## Join Paths

**All subjects with their entry baseline and follow-up measurements:**
```sql
FROM Atherosclerosis.Entry e
LEFT JOIN Atherosclerosis.Contr c ON e.ICO = c.ICO
```

**All subjects with mortality data:**
```sql
FROM Atherosclerosis.Entry e
LEFT JOIN Atherosclerosis.Death d ON e.ICO = d.ICO
```

**All subjects with clinical letter records:**
```sql
FROM Atherosclerosis.Entry e
LEFT JOIN Atherosclerosis.Letter l ON e.ICO = l.ICO
```

**Complete subject history (entry + follow-up + death + letters):**
```sql
FROM Atherosclerosis.Entry e
LEFT JOIN Atherosclerosis.Contr c ON e.ICO = c.ICO
LEFT JOIN Atherosclerosis.Death d ON e.ICO = d.ICO
LEFT JOIN Atherosclerosis.Letter l ON e.ICO = l.ICO
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| subject ID | `ICO` |
| baseline visit | `Atherosclerosis.Entry` |
| follow-up visit | `Atherosclerosis.Contr` |
| death date | `Atherosclerosis.Death.ROKUMR`, `MESUMR` |
| cholesterol level | `CHLST` (mmol/L) or `CHLSTMG` (mg/dL) |
| triglycerides | `TRIGL` (mmol/L) or `TRIGLMG` (mg/dL) |
| systolic/diastolic BP | `SYST`/`DIAST` or `SYST1`/`DIAST1` |
| BMI proxy | weight (`HMOT`, `VAHA`) and height (`VYSKA`) |
| smoking status | `KOURENI`, `KURAK` |
| diabetes | `DIABET`, `DIAB` |
| hypertension | `HT`, `HYPERT` |
| myocardial infarction | `IM` |
| stroke/ICT | `ICT` |
| chest pain | `BOLHR` |
| dyspnea | `DUSNOST`, `DUSN` |

---

## Table Reference

### `Atherosclerosis.Entry` (64 columns)
**Baseline enrollment visit data for all subjects.**

| Column | Type | Notes |
|--------|------|-------|
| `ICO` | BIGINT | Subject identifier (primary key) |
| `ROKNAR` | BIGINT | Birth year |
| `ROKVSTUP` | BIGINT | Enrollment year |
| `MESVSTUP` | BIGINT | Enrollment month |
| `VZDELANI` | BIGINT | Education level |
| `KOURENI` | BIGINT | Smoking status at baseline |
| `DOBAKOUR` | VARCHAR | Duration of smoking; values: `10, 7, 8, 9` |
| `BYVKURAK` | VARCHAR | Former smoker; values: `11, 12` |
| `ALKOHOL` | BIGINT | Alcohol consumption |
| `IM` | BIGINT | History of myocardial infarction |
| `IML` | VARCHAR | MI laterality; values: `4, 5, 6` |
| `HT` | BIGINT | Hypertension diagnosis |
| `HTD` | VARCHAR | HTN drug treatment; values: `3, 6` |
| `HTL` | VARCHAR | HTN drug type; values: `4, 5, 6` |
| `ICT` | BIGINT | Ischemic stroke/TIA |
| `ICTL` | VARCHAR | ICT laterality; values: `6` |
| `DIABET` | BIGINT | Diabetes diagnosis |
| `DIABD` | BIGINT | Diabetes drug treatment |
| `DIABL` | BIGINT | Diabetes drug type |
| `HYPLIP` | BIGINT | Hyperlipidemia diagnosis |
| `HYPLD` | VARCHAR | Hyperlipidemia drug treatment; values: `3, 6` |
| `HYPLL` | VARCHAR | Hyperlipidemia drug type; values: `4, 5, 6` |
| `IMTRV` | VARCHAR | Years since MI; values: `0, 1, 10, 11, 13, 14, 16, 2, 3, 4, 5, 6, 7, 8, 9` |
| `HTTRV` | VARCHAR | Years since HTN diagnosis |
| `ICTTRV` | VARCHAR | Years since ICT; values: `1, 6` |
| `DIABTRV` | BIGINT | Years since diabetes diagnosis |
| `HYPLTRV` | VARCHAR | Years since hyperlipidemia; values: `0, 1, 11, 2, 3, 4, 5, 6, 7, 8, 9` |
| `BOLHR` | BIGINT | Chest pain (angina) |
| `BOLDK` | BIGINT | Back pain |
| `DUSNOST` | BIGINT | Dyspnea |
| `VYSKA` | BIGINT | Height (cm) |
| `VAHA` | BIGINT | Weight (kg) |
| `SYST1` | BIGINT | Systolic BP (mmHg) |
| `DIAST1` | BIGINT | Diastolic BP (mmHg) |
| `SYST2` | VARCHAR | Second systolic BP reading |
| `DIAST2` | VARCHAR | Second diastolic BP reading |
| `TRIC` | BIGINT | Triceps skinfold (mm) |
| `SUBSC` | BIGINT | Subscapular skinfold (mm) |
| `CHLST` | BIGINT | Total cholesterol (mmol/L) |
| `TRIGL` | BIGINT | Triglycerides (mmol/L) |
| `MOC` | BIGINT | Urine glucose |
| `RARISK` | BIGINT | Race/ethnicity risk category |
| `OBEZRISK` | BIGINT | Obesity risk category |
| `KOURRISK` | BIGINT | Smoking risk category |
| `HTRISK` | BIGINT | Hypertension risk category |
| `CHOLRISK` | BIGINT | Cholesterol risk category |

---

### `Atherosclerosis.Contr` (66 columns)
**Periodic follow-up measurements (multiple visits per subject).**

| Column | Type | Notes |
|--------|------|-------|
| `ICO` | BIGINT | Subject identifier |
| `ROKVYS` | BIGINT | Follow-up year |
| `MESVYS` | BIGINT | Follow-up month |
| `PORADK` | BIGINT | Visit sequence number |
| `ZMCHARZA` | BIGINT | Behavior change indicator |
| `ZMTELAKT` | BIGINT | Physical activity change |
| `AKTPOZAM` | BIGINT | Physical activity level |
| `ZMDIET` | BIGINT | Diet change |
| `LEKCHOL` | VARCHAR | Cholesterol medication; values: `70, 71, 72, 73, 75` |
| `LEKTLAK` | BIGINT | Blood pressure medication |
| `ZMKOUR` | BIGINT | Smoking change |
| `POCCIG` | BIGINT | Cigarettes per day |
| `PRACNES` | BIGINT | Work-related stress |
| `SRDCE` | VARCHAR | Cardiac symptoms; values: `2, 3, 4` |
| `HYPERT` | VARCHAR | Hypertension status; values: `2` |
| `CEVMOZ` | VARCHAR | Cerebrovascular symptoms; values: `2, 3, 5` |
| `DIAB` | VARCHAR | Diabetes status; values: `2, 3` |
| `JINAONE` | BIGINT | Other disease |
| `BOLHR` | BIGINT | Chest pain |
| `BOLDK` | BIGINT | Back pain |
| `DUSN` | BIGINT | Dyspnea |
| `HODN0`–`HODN23` | VARCHAR | Disease codes at various timepoints; values: `1, 2, 3, 4, 11, 12, 13, 14, 15, 21, 23` |
| `ROK0`–`ROK23` | VARCHAR/BIGINT | Year of disease code; values: `77–99` (two-digit years) |
| `HMOT` | BIGINT | Weight (kg) |
| `SYST` | BIGINT | Systolic BP (mmHg) |
| `DIAST` | BIGINT | Diastolic BP (mmHg) |
| `TRIC` | BIGINT | Triceps skinfold (mm) |
| `SUBSC` | BIGINT | Subscapular skinfold (mm) |
| `HYPERSD` | BIGINT | Systolic hypertension indicator |
| `HYPERS` | BIGINT | Systolic BP category |
| `HYPERD` | BIGINT | Diastolic hypertension indicator |
| `HYPCHL` | BIGINT | Hypercholesterolemia indicator |
| `HYPTGL` | BIGINT | Hypertriglyceridemia indicator |
| `CHLST` | DOUBLE | Total cholesterol (mmol/L) |
| `CHLSTMG` | BIGINT | Total cholesterol (mg/dL) |
| `TRIGL` | DOUBLE | Triglycerides (mmol/L) |
| `TRIGLMG` | BIGINT | Triglycerides (mg/dL) |
| `HDL` | VARCHAR | HDL cholesterol (mmol/L) |
| `HDLMG` | VARCHAR | HDL cholesterol (mg/dL) |
| `MOC` | BIGINT | Urine glucose |
| `GLYKEMIE` | VARCHAR | Blood glucose |
| `KYSMOC` | VARCHAR | Urine ketones |
| `LDL` | VARCHAR | LDL cholesterol (mmol/L) |

---

### `Atherosclerosis.Death` (5 columns)
**Mortality records for deceased subjects.**

| Column | Type | Notes |
|--------|------|-------|
| `ICO` | BIGINT | Subject identifier |
| `DENUMR` | VARCHAR | Day of death |
| `MESUMR` | VARCHAR | Month of death; values: `1–12` |
| `ROKUMR` | BIGINT | Year of death (two-digit: 77–99) |
| `PRICUMR` | BIGINT | Cause of death code |

---

### `Atherosclerosis.Letter` (60 columns)
**Clinical letter records with disease history, medications, and lifestyle updates.**

| Column | Type | Notes |
|--------|------|-------|
| `ICO` | BIGINT | Subject identifier |
| `MESDOT` | VARCHAR | Letter month; values: `1–12` |
| `ROKDOT` | BIGINT | Letter year (two-digit) |
| `LEKCHOL` | BIGINT | Cholesterol medication |
| `LEKTK` | BIGINT | Blood pressure medication |
| `NEMOC1`–`NEMOC5` | VARCHAR | Disease codes; values: `01–23` |
| `ROK1`–`ROK5` | VARCHAR/BIGINT | Year of disease code |
| `HYPTK` | BIGINT | Hypertension treatment |
| `ROKHYPTK` | VARCHAR | Year HTN treatment started |
| `HYPLP` | BIGINT | Hyperlipidemia treatment |
| `ROKHYPLP` | VARCHAR | Year hyperlipidemia treatment started; values: `60–99` |
| `CUKROVKA` | BIGINT | Diabetes treatment |
| `ROKCUKR` | VARCHAR | Year diabetes treatment started |
| `CUKRTAB` | VARCHAR | Diabetes tablet therapy; values: `1, 2` |
| `CUKRINS` | VARCHAR | Diabetes insulin therapy; values: `1, 2` |
| `ODCUTAB`/`DOCUTAB` | VARCHAR | Diabetes tablet start/stop years |
| `ODCUINS`/`DOCUINS` | VARCHAR | Diabetes insulin start/stop years |
| `AP` | BIGINT | Antiplatelet therapy |
| `SI` | BIGINT | Anticoagulation therapy |
| `MM` | VARCHAR | Beta-blocker therapy; values: `1, 2` |
| `BDK` | BIGINT | ACE inhibitor therapy |
| `DUSNOST` | VARCHAR | Dyspnea present; values: `1, 2` |
| `DUSCHUZE` | VARCHAR | Dyspnea on exertion; values: `1, 2` |
| `DUSBEH` | VARCHAR | Dyspnea at rest; values: `1, 2` |
| `DUSROVIN` | VARCHAR | Paroxysmal nocturnal dyspnea; values: `1, 2` |
| `DUKLID` | VARCHAR | Orthopnea; values: `1, 2` |
| `DUSNOC` | VARCHAR | Nocturnal dyspnea; values: `1, 2` |
| `KURAK` | VARCHAR | Current smoker; values: `1, 2` |
| `KURAKBYV` | VARCHAR | Former smoker; values: `1, 2` |
| `CIGDEN` | VARCHAR | Cigarettes per day; values: `0, 2–35` |
| `DYMKA` | VARCHAR | Pipe/cigar use; values: `1, 2` |
| `PASED` | VARCHAR | Passive smoking; values: `1, 2` |
| `DIETA` | VARCHAR | Dietary modification; values: `1, 2` |
| `JINADIE` | VARCHAR | Other diet type; values: `1, 2` |
| `VAHA` | VARCHAR | Current weight (kg) |
| `VAHAPRED10` | VARCHAR | Weight 10 years prior (kg) |