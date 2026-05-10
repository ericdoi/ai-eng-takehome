# Medical Schema Reference Guide for SQL Agent

## Schema Summary

The `medical` schema contains patient clinical records with examination results, laboratory test values, and patient demographics for autoimmune and thrombotic disease research.

---

## Table Reference

### Table: `medical.Patient`
**Meaning:** Patient master records with demographics and admission status.
**Synonyms:** Patient registry, patient master file, demographics

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ID` | BIGINT | Unique patient identifier | Patient ID, PID |
| `SEX` | VARCHAR | Biological sex | Gender; values: `F`, `M`, `` (empty) |
| `Birthday` | DATE | Date of birth | DOB, birth date |
| `Description` | DATE | Record description date (purpose unclear in schema) | Description date |
| `First Date` | DATE | First visit/admission date | Initial visit, first contact |
| `Admission` | VARCHAR | Admission status | Admission flag; values: `+`, `+(`, `-`, `` (empty) |
| `Diagnosis` | VARCHAR | Primary diagnosis or suspected diagnosis | Clinical diagnosis, primary condition |

---

### Table: `medical.Examination`
**Meaning:** Serological and coagulation test results for autoimmune/thrombotic disease diagnosis.
**Synonyms:** Serology results, immunology tests, coagulation studies

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ID` | BIGINT | Patient identifier (foreign key to Patient) | Patient ID |
| `Examination Date` | DATE | Date test was performed | Test date, exam date |
| `aCL IgG` | DOUBLE | Anticardiolipin IgG antibody level | Anticardiolipin IgG, aCL-IgG |
| `aCL IgM` | DOUBLE | Anticardiolipin IgM antibody level | Anticardiolipin IgM, aCL-IgM |
| `ANA` | BIGINT | Antinuclear antibody titer | ANA titer, nuclear antibody |
| `ANA Pattern` | VARCHAR | ANA immunofluorescence pattern | ANA pattern type; values: `D`, `D,P`, `D,P,S`, `D,S`, `N`, `P`, `P,D`, `P,S`, `P.D`, `P.S`, `S`, `S,D`, `S,N`, `S,P`, `p` |
| `aCL IgA` | BIGINT | Anticardiolipin IgA antibody level | Anticardiolipin IgA, aCL-IgA |
| `Diagnosis` | VARCHAR | Clinical diagnosis at time of exam | Exam diagnosis, clinical impression |
| `KCT` | VARCHAR | Kaolin clotting time result | KCT; values: `+`, `-` |
| `RVVT` | VARCHAR | Dilute Russell viper venom time result | RVVT, viper venom time; values: `+`, `-` |
| `LAC` | VARCHAR | Lupus anticoagulant result | Lupus AC, anticoagulant; values: `+`, `-` |
| `Symptoms` | VARCHAR | Clinical symptoms at time of exam | Presenting symptoms, clinical features |
| `Thrombosis` | BIGINT | Thrombotic event indicator | Thrombosis flag, clot event; values: `0` (no), `1` (yes) |

---

### Table: `medical.Laboratory`
**Meaning:** Comprehensive laboratory test results including hematology, chemistry, immunology, and coagulation panels.
**Synonyms:** Lab results, laboratory values, lab panel

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `ID` | BIGINT | Patient identifier (foreign key to Patient) | Patient ID |
| `Date` | DATE | Date specimen collected/analyzed | Lab date, test date |
| `GOT` | BIGINT | Glutamic-oxaloacetic transaminase (AST) | AST, SGOT |
| `GPT` | BIGINT | Glutamic-pyruvic transaminase (ALT) | ALT, SGPT |
| `LDH` | BIGINT | Lactate dehydrogenase | LD, LDH enzyme |
| `ALP` | BIGINT | Alkaline phosphatase | Alk phos |
| `TP` | DOUBLE | Total protein | Total serum protein |
| `ALB` | DOUBLE | Albumin | Serum albumin |
| `UA` | DOUBLE | Uric acid | Urate |
| `UN` | BIGINT | Blood urea nitrogen | BUN, urea |
| `CRE` | DOUBLE | Creatinine | Serum creatinine |
| `T-BIL` | DOUBLE | Total bilirubin | Total bilirubin |
| `T-CHO` | BIGINT | Total cholesterol | Cholesterol |
| `TG` | BIGINT | Triglycerides | Triglyceride |
| `CPK` | BIGINT | Creatine phosphokinase | CK, muscle enzyme |
| `GLU` | BIGINT | Glucose | Blood glucose, fasting glucose |
| `WBC` | DOUBLE | White blood cell count | WBC, leukocyte count |
| `RBC` | DOUBLE | Red blood cell count | RBC, erythrocyte count |
| `HGB` | DOUBLE | Hemoglobin | Hgb, hemoglobin concentration |
| `HCT` | DOUBLE | Hematocrit | Hct, packed cell volume |
| `PLT` | BIGINT | Platelet count | Platelets, thrombocyte count |
| `PT` | DOUBLE | Prothrombin time | PT, INR-related |
| `APTT` | BIGINT | Activated partial thromboplastin time | aPTT, PTT |
| `FG` | DOUBLE | Fibrinogen | Fibrinogen level |
| `PIC` | BIGINT | Prothrombin-induced clotting time | PIC |
| `TAT` | BIGINT | Thrombin-antithrombin complex | TAT, thrombin marker |
| `TAT2` | BIGINT | Thrombin-antithrombin complex (alternate) | TAT2 |
| `U-PRO` | VARCHAR | Urine protein | Urine protein; values: `%%`, `+1(30)`, `+2(100)`, `-`, `-15`, `0`, `1`, `100`, `2`, `3`, `30`, `300`, `4`, `>=1000`, `>=300`, `TR` |
| `IGG` | BIGINT | Immunoglobulin G | IgG |
| `IGA` | BIGINT | Immunoglobulin A | IgA |
| `IGM` | BIGINT | Immunoglobulin M | IgM |
| `CRP` | VARCHAR | C-reactive protein | CRP, acute phase reactant |
| `RA` | VARCHAR | Rheumatoid arthritis factor | RA factor; values: `+`, `+-`, `-`, `2+`, `7-` |
| `RF` | VARCHAR | Rheumatoid factor | RF, RA factor |
| `C3` | BIGINT | Complement C3 | C3 complement |
| `C4` | BIGINT | Complement C4 | C4 complement |
| `RNP` | VARCHAR | Ribonucleoprotein antibody | RNP, anti-RNP; values: `0`, `1`, `15`, `16`, `256`, `4`, `64`, `negative` |
| `SM` | VARCHAR | Smith antibody | SM, anti-Smith; values: `0`, `1`, `2`, `8`, `negative` |
| `SC170` | VARCHAR | Centromere antibody (Scl-70) | SC170, anti-Scl70; values: `0`, `1`, `16`, `4`, `negative` |
| `SSA` | VARCHAR | Sjögren's syndrome A antibody | SSA, anti-SSA, Ro; values: `0`, `1`, `16`, `256`, `4`, `64`, `negative` |
| `SSB` | VARCHAR | Sjögren's syndrome B antibody | SSB, anti-SSB, La; values: `0`, `1`, `2`, `32`, `8`, `negative` |
| `CENTROMEA` | VARCHAR | Centromere antibody | Centromere; values: `0`, `negative` |
| `DNA` | VARCHAR | Anti-double-stranded DNA antibody | Anti-DNA, dsDNA antibody |
| `DNA-II` | BIGINT | Anti-double-stranded DNA antibody (numeric) | DNA-II, anti-DNA numeric |

---

## Join Paths

**Patient to Examination:**
```sql
medical.Patient p
INNER JOIN medical.Examination e ON p.ID = e.ID
```

**Patient to Laboratory:**
```sql
medical.Patient p
INNER JOIN medical.Laboratory l ON p.ID = l.ID
```

**Examination to Laboratory (same patient, by date proximity):**
```sql
medical.Examination e
INNER JOIN medical.Laboratory l ON e.ID = l.ID
  AND ABS(DATEDIFF(DAY, e."Examination Date", l."Date")) <= 30
```

---

## Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| Exclude pending/null examination results | `WHERE e."Examination Date" IS NOT NULL AND e.Diagnosis IS NOT NULL` |
| Exclude follow-up exams within 30 days of same patient | `WHERE NOT EXISTS (SELECT 1 FROM medical.Examination e2 WHERE e2.ID = e.ID AND e2."Examination Date" < e."Examination Date" AND DATEDIFF(DAY, e2."Examination Date", e."Examination Date") <= 30)` |
| Minimum cohort size enforcement | `HAVING COUNT(DISTINCT p.ID) >= 10` |
| Exclude outlier lab values (>5 SD from mean) | `WHERE l.ColumnName BETWEEN (SELECT AVG(ColumnName) - 5*STDEV(ColumnName) FROM medical.Laboratory) AND (SELECT AVG(ColumnName) + 5*STDEV(ColumnName) FROM medical.Laboratory)` |
| Patient age at examination (not current age) | `DATEDIFF(YEAR, p.Birthday, e."Examination Date") - CASE WHEN MONTH(p.Birthday) > MONTH(e."Examination Date") OR (MONTH(p.Birthday) = MONTH(e."Examination Date") AND DAY(p.Birthday) > DAY(e."Examination Date")) THEN 1 ELSE 0 END` |
| Age band reporting (not exact age) | `CASE WHEN age < 18 THEN '<18' WHEN age <= 30 THEN '18-30' WHEN age <= 45 THEN '31-45' WHEN age <= 60 THEN '46-60' ELSE '60+' END` |
| First positive test (not subsequent confirmatory) | `WHERE e."Examination Date" = (SELECT MIN("Examination Date") FROM medical.Examination e2 WHERE e2.ID = e.ID AND (e2."aCL IgG" > 0 OR e2."aCL IgM" > 0 OR e2.ANA > 0))` |
| Thrombotic event indicator | `WHERE e.Thrombosis = 1` |
| Positive coagulation test (LAC/RVVT/KCT) | `WHERE e.LAC = '+' OR e.RVVT = '+' OR e.KCT = '+'` |
| Positive ANA result | `WHERE e.ANA > 0 AND e.ANA IS NOT NULL` |
| Valid admission status | `WHERE p.Admission IN ('+', '+(', '-')` |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| Patient age | `DATEDIFF(YEAR, p.Birthday, e."Examination Date")` |
| Age band | `CASE WHEN age BETWEEN 18 AND 30 THEN '18-30' ... END` |
| Anticardiolipin positive | `e."aCL IgG" > 0 OR e."aCL IgM" > 0 OR e."aCL IgA" > 0` |
| Lupus anticoagulant positive | `e.LAC = '+'` |
| Thrombosis event | `e.Thrombosis = 1` |
| ANA positive | `e.ANA > 0` |
| ANA pattern | `e."ANA Pattern"` |
| Coagulation abnormality | `e.LAC = '+' OR e.RVVT = '+' OR e.KCT = '+'` |
| Liver function | `l.GOT, l.GPT, l.ALP` |
| Renal function | `l.CRE, l.UN` |
| Hemoglobin/hematocrit | `l.HGB, l.HCT` |
| Platelet count | `l.PLT` |
| Immunoglobulin levels | `l.IGG, l.IGA, l.IGM` |
| Complement levels | `l.C3, l.C4` |
| Autoantibody panel | `l.RNP, l.SM, l.SSA, l.SSB, l.DNA` |
| Rheumatoid factor | `l.RA, l.RF` |
| C-reactive protein | `l.CRP` |
| Urine protein | `l."U-PRO"` |
| First visit date | `p."First Date"` |
| Admission status | `p.Admission` |
| Patient diagnosis | `p.Diagnosis` |
| Exam diagnosis | `e.Diagnosis` |
| Exam date | `e."Examination Date"` |
| Lab date | `l.Date` |
| Cohort size | `COUNT(DISTINCT p.ID)` |
| Minimum reportable cohort | `HAVING COUNT(DISTINCT p.ID) >= 10` |