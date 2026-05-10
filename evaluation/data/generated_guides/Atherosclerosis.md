# Atherosclerosis Schema Reference Guide

## Schema Summary
This schema contains longitudinal cardiovascular health data for a cohort study, tracking participant demographics, clinical measurements, diagnoses, medications, and mortality outcomes across multiple follow-up visits from the 1970s–1990s.

---

## Table Reference

### Table: `Atherosclerosis.Contr`
**Meaning:** Control/follow-up visit records; repeated measurements and clinical assessments for study participants.
**Synonyms:** Follow-up visit, Control visit, Measurement record

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ICO` | BIGINT | Participant identifier | Subject ID, Patient ID |
| `ROKVYS` | BIGINT | Year of visit | Visit year |
| `MESVYS` | BIGINT | Month of visit | Visit month |
| `PORADK` | BIGINT | Visit sequence number | Visit order, Visit number |
| `ZMCHARZA` | BIGINT | Change in behavior/lifestyle (coded) | Behavior change |
| `ZMTELAKT` | BIGINT | Change in physical activity (coded) | Activity change |
| `AKTPOZAM` | BIGINT | Physical activity level (coded) | Activity level |
| `ZMDIET` | BIGINT | Change in diet (coded) | Diet change |
| `LEKCHOL` | VARCHAR | Cholesterol medication use | Cholesterol drug; Values: 70, 71, 72, 73, 75 |
| `LEKTLAK` | BIGINT | Blood pressure medication use (coded) | BP medication |
| `ZMKOUR` | BIGINT | Change in smoking (coded) | Smoking change |
| `POCCIG` | BIGINT | Number of cigarettes per day | Daily cigarettes |
| `PRACNES` | BIGINT | Work-related stress (coded) | Occupational stress |
| `SRDCE` | VARCHAR | Heart disease status | Cardiac status; Values: 2, 3, 4 |
| `HYPERT` | VARCHAR | Hypertension status | High blood pressure; Values: 2 |
| `CEVMOZ` | VARCHAR | Cerebrovascular disease status | Stroke/brain vessel disease; Values: 2, 3, 5 |
| `DIAB` | VARCHAR | Diabetes status | Diabetes; Values: 2, 3 |
| `JINAONE` | BIGINT | Other disease (coded) | Other condition |
| `BOLHR` | BIGINT | Chest pain presence (coded) | Angina, Chest pain |
| `BOLDK` | BIGINT | Back pain presence (coded) | Back pain |
| `DUSN` | BIGINT | Dyspnea/shortness of breath (coded) | Breathlessness |
| `HODNSK` | BIGINT | Baseline measurement value | Initial value |
| `HODN0` | BIGINT | Measurement 0 value | Measurement at time 0 |
| `ROK0` | BIGINT | Year of measurement 0 | Year at time 0 |
| `HODN1` | VARCHAR | Measurement 1 value | Values: 1 |
| `ROK1` | VARCHAR | Year of measurement 1 | |
| `HODN2` | VARCHAR | Measurement 2 value | Values: 2 |
| `ROK2` | VARCHAR | Year of measurement 2 | |
| `HODN3` | VARCHAR | Measurement 3 value | Values: 3 |
| `ROK3` | VARCHAR | Year of measurement 3 | Values: 77–98 |
| `HODN4` | VARCHAR | Measurement 4 value | Values: 4 |
| `ROK4` | VARCHAR | Year of measurement 4 | Values: 78–98 |
| `HODN11` | VARCHAR | Measurement 11 value | Values: 11 |
| `ROK11` | VARCHAR | Year of measurement 11 | Values: 80–99 |
| `HODN12` | VARCHAR | Measurement 12 value | Values: 12 |
| `ROK12` | VARCHAR | Year of measurement 12 | Values: 77–97 |
| `HODN13` | VARCHAR | Measurement 13 value | Values: 13 |
| `ROK13` | VARCHAR | Year of measurement 13 | Values: 79–99 |
| `HODN14` | VARCHAR | Measurement 14 value | Values: 14 |
| `ROK14` | VARCHAR | Year of measurement 14 | Values: 79, 91, 96 |
| `HODN15` | VARCHAR | Measurement 15 value | Values: 15 |
| `ROK15` | VARCHAR | Year of measurement 15 | Values: 87–98 |
| `HODN21` | VARCHAR | Measurement 21 value | Values: 21 |
| `ROK21` | VARCHAR | Year of measurement 21 | Values: 90, 94, 96 |
| `HODN23` | VARCHAR | Measurement 23 value | Values: 23 |
| `ROK23` | VARCHAR | Year of measurement 23 | Values: 97 |
| `HMOT` | BIGINT | Body weight (kg) | Weight |
| `SYST` | BIGINT | Systolic blood pressure (mmHg) | Systolic BP |
| `DIAST` | BIGINT | Diastolic blood pressure (mmHg) | Diastolic BP |
| `TRIC` | BIGINT | Triceps skinfold (mm) | Triceps fold |
| `SUBSC` | BIGINT | Subscapular skinfold (mm) | Subscapular fold |
| `HYPERSD` | BIGINT | Systolic hypertension indicator (coded) | Systolic HTN |
| `HYPERS` | BIGINT | Systolic hypertension severity (coded) | Systolic HTN severity |
| `HYPERD` | BIGINT | Diastolic hypertension indicator (coded) | Diastolic HTN |
| `HYPCHL` | BIGINT | Hypercholesterolemia indicator (coded) | High cholesterol |
| `HYPTGL` | BIGINT | Hypertriglyceridemia indicator (coded) | High triglycerides |
| `CHLST` | DOUBLE | Total cholesterol (mmol/L) | Cholesterol |
| `CHLSTMG` | BIGINT | Total cholesterol (mg/dL) | Cholesterol (mg/dL) |
| `TRIGL` | DOUBLE | Triglycerides (mmol/L) | Triglycerides |
| `TRIGLMG` | BIGINT | Triglycerides (mg/dL) | Triglycerides (mg/dL) |
| `HDL` | VARCHAR | HDL cholesterol (mmol/L) | HDL |
| `HDLMG` | VARCHAR | HDL cholesterol (mg/dL) | HDL (mg/dL) |
| `MOC` | BIGINT | Urine output/kidney function (coded) | Urine, Kidney function |
| `GLYKEMIE` | VARCHAR | Blood glucose/glycemia (coded) | Blood sugar, Glucose |
| `KYSMOC` | VARCHAR | Urine ketones (coded) | Ketones |
| `LDL` | VARCHAR | LDL cholesterol (mmol/L) | LDL |

---

### Table: `Atherosclerosis.Death`
**Meaning:** Mortality records; date and cause of death for deceased participants.
**Synonyms:** Mortality, Outcome, Death record

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ICO` | BIGINT | Participant identifier | Subject ID, Patient ID |
| `DENUMR` | VARCHAR | Day of death | Death day |
| `MESUMR` | VARCHAR | Month of death | Death month; Values: 1–12 |
| `ROKUMR` | BIGINT | Year of death | Death year |
| `PRICUMR` | BIGINT | Cause of death (coded) | Death cause, ICD code |

---

### Table: `Atherosclerosis.Entry`
**Meaning:** Baseline/enrollment visit records; initial demographic, lifestyle, and clinical data at study entry.
**Synonyms:** Baseline, Enrollment, Initial visit, Intake

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ICO` | BIGINT | Participant identifier | Subject ID, Patient ID |
| `KONSKUP` | BIGINT | Cohort/group assignment (coded) | Group, Cohort |
| `ROKNAR` | BIGINT | Year of birth | Birth year |
| `ROKVSTUP` | BIGINT | Year of enrollment | Enrollment year |
| `MESVSTUP` | BIGINT | Month of enrollment | Enrollment month |
| `STAV` | BIGINT | Marital status (coded) | Marital status |
| `VZDELANI` | BIGINT | Education level (coded) | Education |
| `ZODPOV` | BIGINT | Occupational responsibility level (coded) | Job responsibility |
| `TELAKTZA` | BIGINT | Physical activity at work (coded) | Work activity |
| `AKTPOZAM` | BIGINT | Physical activity in leisure (coded) | Leisure activity |
| `DOPRAVA` | BIGINT | Mode of transportation (coded) | Transport |
| `DOPRATRV` | BIGINT | Transportation duration (coded) | Transport time |
| `KOURENI` | BIGINT | Smoking status (coded) | Smoking |
| `DOBAKOUR` | VARCHAR | Duration of smoking (coded) | Smoking duration; Values: 7, 8, 9, 10 |
| `BYVKURAK` | VARCHAR | Former smoker status (coded) | Ex-smoker; Values: 11, 12 |
| `ALKOHOL` | BIGINT | Alcohol consumption (coded) | Alcohol use |
| `PIVO7` | VARCHAR | Beer consumption frequency (coded) | Beer; Values: 8 |
| `PIVO10` | BIGINT | Beer consumption quantity (coded) | Beer amount |
| `PIVO12` | VARCHAR | Beer consumption pattern (coded) | Beer pattern; Values: 10 |
| `VINO` | BIGINT | Wine consumption (coded) | Wine |
| `LIHOV` | BIGINT | Spirits consumption (coded) | Liquor, Hard liquor |
| `PIVOMN` | BIGINT | Beer consumption (monthly) | Monthly beer |
| `VINOMN` | BIGINT | Wine consumption (monthly) | Monthly wine |
| `LIHMN` | BIGINT | Spirits consumption (monthly) | Monthly spirits |
| `KAVA` | BIGINT | Coffee consumption (coded) | Coffee |
| `CAJ` | BIGINT | Tea consumption (coded) | Tea |
| `CUKR` | BIGINT | Sugar consumption (coded) | Sugar |
| `IM` | BIGINT | Myocardial infarction history (coded) | MI, Heart attack |
| `IML` | VARCHAR | MI onset age (coded) | MI age; Values: 4, 5, 6 |
| `HT` | BIGINT | Hypertension history (coded) | High blood pressure history |
| `HTD` | VARCHAR | Hypertension diagnosis age (coded) | HTN age; Values: 3, 6 |
| `HTL` | VARCHAR | Hypertension treatment duration (coded) | HTN treatment; Values: 4, 5, 6 |
| `ICT` | BIGINT | Ischemic stroke history (coded) | Stroke history |
| `ICTL` | VARCHAR | Stroke onset age (coded) | Stroke age; Values: 6 |
| `DIABET` | BIGINT | Diabetes history (coded) | Diabetes |
| `DIABD` | BIGINT | Diabetes diagnosis age (coded) | Diabetes age |
| `DIABL` | BIGINT | Diabetes treatment duration (coded) | Diabetes treatment |
| `HYPLIP` | BIGINT | Hyperlipidemia history (coded) | High lipids history |
| `HYPLD` | VARCHAR | Hyperlipidemia diagnosis age (coded) | Hyperlipidemia age; Values: 3, 6 |
| `HYPLL` | VARCHAR | Hyperlipidemia treatment duration (coded) | Hyperlipidemia treatment; Values: 4, 5, 6 |
| `IMTRV` | VARCHAR | MI treatment duration (coded) | MI treatment; Values: 0–16 |
| `HTTRV` | VARCHAR | Hypertension treatment duration (coded) | HTN treatment duration |
| `ICTTRV` | VARCHAR | Stroke treatment duration (coded) | Stroke treatment; Values: 1, 6 |
| `DIABTRV` | BIGINT | Diabetes treatment duration (coded) | Diabetes treatment duration |
| `HYPLTRV` | VARCHAR | Hyperlipidemia treatment duration (coded) | Hyperlipidemia treatment duration; Values: 0–9, 11 |
| `BOLHR` | BIGINT | Chest pain presence (coded) | Angina, Chest pain |
| `BOLDK` | BIGINT | Back pain presence (coded) | Back pain |
| `DUSNOST` | BIGINT | Dyspnea presence (coded) | Shortness of breath |
| `VYSKA` | BIGINT | Height (cm) | Height |
| `VAHA` | BIGINT | Body weight (kg) | Weight |
| `SYST1` | BIGINT | Systolic BP, measurement 1 (mmHg) | Systolic BP 1 |
| `DIAST1` | BIGINT | Diastolic BP, measurement 1 (mmHg) | Diastolic BP 1 |
| `SYST2` | VARCHAR | Systolic BP, measurement 2 (mmHg) | Systolic BP 2 |
| `DIAST2` | VARCHAR | Diastolic BP, measurement 2 (mmHg) | Diastolic BP 2 |
| `TRIC` | BIGINT | Triceps skinfold (mm) | Triceps fold |
| `SUBSC` | BIGINT | Subscapular skinfold (mm) | Subscapular fold |
| `CHLST` | BIGINT | Total cholesterol (mg/dL) | Cholesterol |
| `TRIGL` | BIGINT | Triglycerides (mg/dL) | Triglycerides |
| `MOC` | BIGINT | Urine output/kidney function (coded) | Urine, Kidney function |
| `RARISK` | BIGINT | Race/ethnicity risk indicator (coded) | Race risk |
| `OBEZRISK` | BIGINT | Obesity risk indicator (coded) | Obesity risk |
| `KOURRISK` | BIGINT | Smoking risk indicator (coded) | Smoking risk |
| `HTRISK` | BIGINT | Hypertension risk indicator (coded) | HTN risk |
| `CHOLRISK` | BIGINT | Cholesterol risk indicator (coded) | Cholesterol risk |

---

### Table: `Atherosclerosis.Letter`
**Meaning:** Follow-up letter/questionnaire records; clinical status updates, medication use, and lifestyle data collected via correspondence.
**Synonyms:** Follow-up questionnaire, Letter response, Correspondence record

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ICO` | BIGINT | Participant identifier | Subject ID, Patient ID |
| `MESDOT` | VARCHAR | Month of letter/questionnaire | Letter month; Values: 1–12 |
| `ROKDOT` | BIGINT | Year of letter/questionnaire | Letter year |
| `LEKCHOL` | BIGINT | Cholesterol medication use (coded) | Cholesterol drug |
| `LEKTK` | BIGINT | Blood pressure medication use (coded) | BP medication |
| `NEMOC1` | BIGINT | Primary disease diagnosis (coded) | Primary diagnosis |
| `ROK1`