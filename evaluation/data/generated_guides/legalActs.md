# SQL Reference Guide: legalActs Schema

## Schema Summary
The `legalActs` schema contains Bulgarian legal court decisions (acts) with associated metadata, judge/people information, document links, and data quality fixes.

---

## Table Reference

### `legalActs.legalacts`
**Meaning:** Primary table of legal court decisions/acts.  
**Synonyms:** legal decisions, court rulings, judicial acts

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique act identifier | act ID, decision ID |
| `hash` | VARCHAR | Content hash fingerprint | document hash |
| `update` | TIMESTAMP | Last record update time | updated at, modification time |
| `Court` | VARCHAR | Issuing court name | court name, tribunal |
| `CaseKind` | VARCHAR | Type of case (e.g., НОХД, Гражданско дело) | case type, litigation type |
| `CaseNumber` | BIGINT | Case reference number | case ID, docket number |
| `ActYear` | BIGINT | Year act was issued | decision year, year |
| `Judge` | VARCHAR | Judge name and composition | judge name, judicial officer |
| `ActKind` | VARCHAR | Type of legal act | decision type, ruling type |
| `ActNumber` | BIGINT | Act reference number | decision number |
| `StartDate` | DATE | Case start date | filing date, case opened |
| `LegalDate` | DATE | Act legal effect date | effective date, ruling date |
| `Status` | VARCHAR | Current legal status | decision status, validity |
| `ActLink` | BOOLEAN | Whether act has linked documents | has links, linked |
| `MotiveDate` | DATE | Motive/reasoning document date | reasoning date |
| `MotiveLink` | BOOLEAN | Whether motive document exists | has motive, reasoning exists |
| `HighCourt` | VARCHAR | Higher court reference (if appeal) | appellate court, superior court |
| `OutNumber` | BIGINT | Output/reference number | out number |
| `YearHigherCourt` | BIGINT | Year at higher court | appeal year |
| `TypeOfDocument` | VARCHAR | Document category | document type |
| `SendDate` | DATE | Document send date | transmission date |
| `ResultOfAppeal` | VARCHAR | Appeal outcome | appeal result |

**ActKind enumeration (exact values):**
- Заповед (Order)
- Определение (Ruling)
- Присъда (Verdict)
- Протокол (Protocol)
- Разпореждане (Directive)
- Решение (Decision)
- Споразумение (Agreement)

**Status enumeration (exact values):**
- Влязъл в сила (Entered into force)
- Изменен (Modified)
- Не е влязъл в сила (Not entered into force)
- Отменен (Cancelled)
- Потвърден (Confirmed)

**TypeOfDocument enumeration (exact values):**
- Писмо (Letter)
- Писмо - молба за опр. срок при бавност (Letter - request for deadline extension)
- Писмо - предложение за възобновяване (Letter - proposal for renewal)

---

### `legalActs.legalact_people`
**Meaning:** Junction table linking people (judges/jury) to legal acts.  
**Synonyms:** act-person association, judge-act mapping

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `peopleId` | BIGINT | Reference to person | person ID, judge ID |
| `actId` | BIGINT | Reference to legal act | act ID, decision ID |

---

### `legalActs.people`
**Meaning:** Registry of judges and jury members.  
**Synonyms:** judges, judicial officers, court personnel

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `personId` | BIGINT | Unique person identifier | person ID, judge ID |
| `name` | VARCHAR | Full name | judge name, person name |
| `jury` | BOOLEAN | Whether person is jury member | is jury, jury status |
| `court` | VARCHAR | Court assignment | assigned court, court name |

---

### `legalActs.legalact_link`
**Meaning:** Links between related legal acts (e.g., appeals, related cases).  
**Synonyms:** act relationships, decision links, case connections

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `actId1` | BIGINT | First act in relationship | source act, primary act |
| `actId2` | BIGINT | Second act in relationship | target act, related act |

---

### `legalActs.scrapefix`
**Meaning:** Data quality corrections and issues logged during data collection.  
**Synonyms:** data fixes, corrections log, quality issues

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `actId` | BIGINT | Act requiring fix | act ID, decision ID |
| `fix_description` | VARCHAR | Description of issue/correction applied | fix note, issue description |
| `contributor` | VARCHAR | Person who logged/applied fix | fixer, contributor name |

**contributor enumeration (exact values):**
- Boyan Yurukov

---

## Join Paths

### Acts to People (via junction table)
```sql
legalActs.legalacts
  INNER JOIN legalActs.legalact_people ON legalActs.legalacts.id = legalActs.legalact_people.actId
  INNER JOIN legalActs.people ON legalActs.legalact_people.peopleId = legalActs.people.personId
```

### Related Acts (via link table)
```sql
legalActs.legalacts a1
  INNER JOIN legalActs.legalact_link ON a1.id = legalActs.legalact_link.actId1
  INNER JOIN legalActs.legalacts a2 ON legalActs.legalact_link.actId2 = a2.id
```

### Acts with Data Fixes
```sql
legalActs.legalacts
  LEFT JOIN legalActs.scrapefix ON legalActs.legalacts.id = legalActs.scrapefix.actId
```

---

## Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| Act has entered into force | `WHERE Status = 'Влязъл в сила'` |
| Act is cancelled/invalid | `WHERE Status = 'Отменен'` |
| Act is a verdict | `WHERE ActKind = 'Присъда'` |
| Act is an agreement | `WHERE ActKind = 'Споразумение'` |
| Act has linked documents | `WHERE ActLink = TRUE` |
| Act has motive/reasoning document | `WHERE MotiveLink = TRUE` |
| Act has been modified | `WHERE Status = 'Изменен'` |
| Person is judge (not jury) | `WHERE jury = FALSE` |
| Person is jury member | `WHERE jury = TRUE` |
| Act has data quality issues | `WHERE id IN (SELECT actId FROM legalActs.scrapefix)` |
| Act has been appealed | `WHERE HighCourt IS NOT NULL` |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| legal decision | `legalActs.legalacts` |
| court ruling | `legalActs.legalacts` |
| judge | `legalActs.people WHERE jury = FALSE` |
| jury member | `legalActs.people WHERE jury = TRUE` |
| decision type | `legalActs.legalacts.ActKind` |
| case type | `legalActs.legalacts.CaseKind` |
| decision status | `legalActs.legalacts.Status` |
| valid/in force | `Status = 'Влязъл в сила'` |
| cancelled/void | `Status = 'Отменен'` |
| verdict | `ActKind = 'Присъда'` |
| settlement/agreement | `ActKind = 'Споразумение'` |
| ruling | `ActKind = 'Определение'` |
| decision | `ActKind = 'Решение'` |
| order | `ActKind = 'Заповед'` |
| protocol | `ActKind = 'Протокол'` |
| directive | `ActKind = 'Разпореждане'` |
| issued year | `legalActs.legalacts.ActYear` |
| case filed date | `legalActs.legalacts.StartDate` |
| effective date | `legalActs.legalacts.LegalDate` |
| appeal court | `legalActs.legalacts.HighCourt` |
| related acts | `legalActs.legalact_link` |
| data quality issue | `legalActs.scrapefix` |
| has documentation | `ActLink = TRUE` |
| has reasoning | `MotiveLink = TRUE` |