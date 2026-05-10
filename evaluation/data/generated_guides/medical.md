# Medical Schema Reference Guide

## Schema Summary
This schema contains patient demographics, clinical examination results (autoimmune markers, coagulation tests), and laboratory test values for rheumatologic and thrombotic disease assessment.

---

## Join Paths

**Patient to Examination:**
```sql
FROM medical.Patient p
JOIN medical.Examination e ON p.ID = e.ID
```

**Patient to Laboratory:**
```sql
FROM medical.Patient p
JOIN medical.Laboratory l ON p.ID = l.ID
```

**Examination to Laboratory (same patient, by date proximity):**
```sql
FROM medical.Examination e
JOIN medical.Laboratory l ON e.ID = l.ID
WHERE ABS(DATEDIFF(DAY, e."Examination Date", l.Date)) <= 30
```

**All three tables:**
```sql
FROM medical.Patient p
JOIN medical.Examination e ON p.ID = e.ID
JOIN medical.Laboratory l ON p.ID = l.ID
```

---

## Business Rules as SQL

**Minimum cell size (aggregation threshold):**
```sql
HAVING COUNT(DISTINCT p.ID) >= 10
-- Report as "< 10" if result falls below this threshold
```

**Valid examination results only (exclude pending/null diagnoses):**
```sql
WHERE e.Diagnosis IS NOT NULL AND e.Diagnosis != 'NaN'
```

**Patient age calculation (as of examination date, not current date):**
```sql
DATEDIFF(YEAR, p.Birthday, e."Examination Date") 
  - CASE WHEN MONTH(p.Birthday) > MONTH(e."Examination Date") 
         OR (MONTH(p.Birthday) = MONTH(e."Examination Date") 
             AND DAY(p.Birthday) > DAY(e."Examination Date")) 
         THEN 1 ELSE 0 END
```

**Age bands (instead of exact ages):**
```sql
CASE 
  WHEN age BETWEEN 18 AND 30 THEN '18-30'
  WHEN age BETWEEN 31 AND 45 THEN '31-45'
  WHEN age BETWEEN 46 AND 60 THEN '46-60'
  WHEN age > 60 THEN '60+'
END
```

**Exclude outlier lab values (> 5 standard deviations from mean):**
```sql
WHERE ABS(l.ColumnName - (SELECT AVG(ColumnName) FROM medical.Laboratory)) 
  <= 5 * (SELECT STDEV(ColumnName) FROM medical.Laboratory)
```

**First positive test only (for time-to-diagnosis):**
```sql
WHERE e.ID IN (
  SELECT ID FROM medical.Examination 
  WHERE (aCL_IgG > 0 OR aCL_IgM > 0 OR ANA > 0)
  ORDER BY "Examination Date" ASC
)
```

---

## Synonym Glossary

| Common Term | Schema Reference |
|---|---|
| Anticardiolipin IgG | `medical.Examination.aCL IgG` |
| Anticardiolipin IgM | `medical.Examination.aCL IgM` |
| Anticardiolipin IgA | `medical.Examination.aCL IgA` |
| ANA titer | `medical.Examination.ANA` |
| ANA pattern | `medical.Examination.ANA Pattern` |
| Coagulation test (KCT, RVVT, LAC) | `medical.Examination.KCT`, `.RVVT`, `.LAC` |
| Thrombotic event | `medical.Examination.Thrombosis` (1 = yes, 0 = no) |
| Liver enzymes | `medical.Laboratory.GOT`, `.GPT`, `.ALP` |
| Renal function | `medical.Laboratory.CRE`, `.UN` |
| Hemoglobin/hematocrit | `medical.Laboratory.HGB`, `.HCT` |
| Platelet count | `medical.Laboratory.PLT` |
| Immunoglobulins | `medical.Laboratory.IGG`, `.IGA`, `.IGM` |
| Complement levels | `medical.Laboratory.C3`, `.C4` |
| Autoantibodies (RNP, SM, SSA, SSB, Centromere, DNA) | `medical.Laboratory.RNP`, `.SM`, `.SSA`, `.SSB`, `.CENTROMEA`, `.DNA` |
| Rheumatoid factor | `medical.Laboratory.RA`, `.RF` |
| C-reactive protein | `medical.Laboratory.CRP` |
| Coagulation times | `medical.Laboratory.PT`, `.APTT` |
| Fibrinogen | `medical.Laboratory.FG` |

---

## Table Reference

### `medical.Patient`
**Meaning:** Patient demographics and admission status.

| Column | Notes |
|---|---|
| `ID` | Primary key; use for all joins. |
| `SEX` | Enum: `'F'`, `'M'`, `''` (blank/unknown). |
| `Birthday` | Date of birth; use to calculate age as of examination date. |
| `First Date` | Initial visit date; use for cohort entry point. |
| `Admission` | Enum: `'+'` (admitted), `'-'` (not admitted), `'+'` (incomplete), `''` (blank). |
| `Diagnosis` | Clinical diagnosis at enrollment (e.g., "SLE", "RA susp.", "PSS", "MCTD"). |

---

### `medical.Examination`
**Meaning:** Autoimmune serology and coagulation test results; one row per examination event.

| Column | Notes |
|---|---|
| `ID` | Foreign key to `medical.Patient.ID`. |
| `Examination Date` | Test date; use for age calculation and temporal ordering. |
| `aCL IgG`, `aCL IgM`, `aCL IgA` | Anticardiolipin antibody levels (DOUBLE/BIGINT). Values ≥ 1.0 typically positive. |
| `ANA` | Antinuclear antibody titer (BIGINT). Values: 0, 4, 16, 256, etc. Higher = stronger. |
| `ANA Pattern` | Enum: `'D'`, `'P'`, `'S'`, `'N'` (negative), or combinations (e.g., `'P,S'`, `'D,P,S'`). |
| `Diagnosis` | Clinical diagnosis at this exam (may differ from enrollment). Exclude rows where `'NaN'` or NULL. |
| `KCT`, `RVVT`, `LAC` | Coagulation tests. Enum: `'+'` (positive), `'-'` (negative), `'NaN'` (not performed). |
| `Symptoms` | Free text; often `'NaN'` or specific event (e.g., "AMI"). |
| `Thrombosis` | Binary: `1` = thrombotic event present, `0` = absent. |

---

### `medical.Laboratory`
**Meaning:** Biochemistry, hematology, immunology, and coagulation panel results; one row per lab draw date.

| Column | Notes |
|---|---|
| `ID` | Foreign key to `medical.Patient.ID`. |
| `Date` | Lab draw date; use for temporal alignment with examinations. |
| **Liver/Biliary** | `GOT`, `GPT` (transaminases), `ALP` (alkaline phosphatase), `T-BIL` (total bilirubin). |
| **Renal** | `CRE` (creatinine), `UN` (urea nitrogen), `UA` (uric acid). |
| **Lipids** | `T-CHO` (total cholesterol), `TG` (triglycerides). |
| **Hemostasis** | `PT` (prothrombin time), `APTT` (activated partial thromboplastin time), `FG` (fibrinogen), `PIC`, `TAT`, `TAT2` (thrombin-antithrombin complexes). |
| **Hematology** | `WBC` (white blood cells), `RBC` (red blood cells), `HGB` (hemoglobin), `HCT` (hematocrit), `PLT` (platelets). |
| **Immunology** | `IGG`, `IGA`, `IGM` (immunoglobulin levels). `CRP` (C-reactive protein, often `'NaN'` or numeric). `RA` (rheumatoid activity), `RF` (rheumatoid factor). |
| **Complement** | `C3`, `C4` (complement components). |
| **Autoantibodies** | `RNP`, `SM`, `SC170`, `SSA`, `SSB`, `CENTROMEA`, `DNA`, `DNA-II`. Enum values: `'0'`, `'1'`, `'2'`, `'4'`, `'8'`, `'16'`, `'32'`, `'64'`, `'256'`, `'negative'`. Higher numeric = stronger titer. |
| `U-PRO` | Urine protein. Enum: `'-'` (negative), `'TR'` (trace), `'+1(30)'`, `'+2(100)'`, `'+3(300)'`, `'+4(>=1000)'`, or numeric `'0'`, `'1'`, `'2'`, `'3'`, `'4'`, `'30'`, `'100'`, `'300'`, `'>=300'`, `'>=1000'`, `'%%'`. |
| `GLU` | Glucose (fasting status unknown; analyze separately from non-fasting if possible). |
| `CPK` | Creatine phosphokinase. |

---

## Critical Compliance Notes

- **Never expose patient IDs or exact ages** in any output; use age bands.
- **Minimum aggregation size is 10 patients**; report smaller cohorts as "< 10".
- **Exclude rows where `Diagnosis = 'NaN'`** from diagnostic accuracy analyses.
- **Older records (pre-2000) may have approximate dates**; flag in analysis if relevant.
- **Laboratory values outside normal range vary by test type**; define ranges per test before flagging outliers.
- **Fasting vs. non-fasting lab tests are not comparable**; separate in analysis if fasting status is known.