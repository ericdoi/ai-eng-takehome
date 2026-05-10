# Legal Acts Schema Reference Guide

## Schema Summary
This schema contains Bulgarian court legal acts (judicial decisions and orders), linked people (judges, jurors), and data quality fixes from web scraping.

---

## Join Paths

**Legal acts with related acts:**
```sql
FROM legalActs.legalacts la1
JOIN legalActs.legalact_link ll ON la1.id = ll.actId1
JOIN legalActs.legalacts la2 ON ll.actId2 = la2.id
```

**Legal acts with associated people:**
```sql
FROM legalActs.legalacts la
JOIN legalActs.legalact_people lp ON la.id = lp.actId
JOIN legalActs.people p ON lp.peopleId = p.personId
```

**Legal acts with data quality notes:**
```sql
FROM legalActs.legalacts la
LEFT JOIN legalActs.scrapefix sf ON la.id = sf.actId
```

---

## Table Reference

### `legalActs.legalacts`
Core legal acts table. Represents individual court decisions, orders, and protocols.

**Key columns:**
- `id` — unique act identifier
- `hash` — document fingerprint
- `update` — last record modification timestamp
- `Court` — issuing court name
- `CaseKind` — case category (e.g., "НОХД", "Гражданско дело", "Частно гражданско дело")
- `CaseNumber` — case identifier within court
- `ActYear` — year of act issuance
- `Judge` — judge name and composition identifier
- `ActKind` — type of judicial act (enum: `Заповед`, `Определение`, `Присъда`, `Протокол`, `Разпореждане`, `Решение`, `Споразумение`)
- `ActNumber` — sequential act number
- `StartDate` — case initiation date
- `LegalDate` — act effective date
- `Status` — legal standing (enum: `Влязъл в сила`, `Изменен`, `Не е влязъл в сила`, `Отменен`, `Потвърден`)
- `ActLink` — boolean flag indicating linked related acts exist
- `MotiveDate` — date of appeal/motive document
- `MotiveLink` — boolean flag for motive document availability
- `HighCourt` — appellate court name (if applicable)
- `OutNumber` — appellate court case number
- `YearHigherCourt` — appellate court year
- `TypeOfDocument` — document category (enum: `Писмо`, `Писмо - молба за опр. срок при бавност`, `Писмо - предложение за възобновяване`)
- `SendDate` — document transmission date
- `ResultOfAppeal` — appeal outcome description

### `legalActs.legalact_link`
Relationship table linking related legal acts (e.g., original decision and appeal).

**Columns:**
- `actId1` — primary act identifier (foreign key to `legalActs.legalacts.id`)
- `actId2` — related act identifier (foreign key to `legalActs.legalacts.id`)

### `legalActs.legalact_people`
Junction table associating people (judges, jurors) with legal acts.

**Columns:**
- `peopleId` — person identifier (foreign key to `legalActs.people.personId`)
- `actId` — act identifier (foreign key to `legalActs.legalacts.id`)

### `legalActs.people`
Judicial personnel registry (judges and jurors).

**Key columns:**
- `personId` — unique person identifier
- `name` — full name
- `jury` — boolean; `True` indicates juror, `False` indicates judge
- `court` — assigned court name

### `legalActs.scrapefix`
Data quality corrections applied to scraped records.

**Columns:**
- `actId` — act identifier (foreign key to `legalActs.legalacts.id`)
- `fix_description` — correction applied (enum values document specific data issues: year corrections, date corrections, document problems)
- `contributor` — person who applied the fix