# Dallas Police Officer-Involved Shooting (OIS) Schema Reference Guide

## Schema Summary
This schema documents officer-involved shooting incidents in Dallas, including incident details, officer demographics, and subject demographics.

---

## Table Reference

### Table: `Dallas.incidents`
**Meaning:** Officer-involved shooting incidents reported by Dallas Police Department.  
**Synonyms:** OIS cases, shooting incidents, police encounters

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `case_number` | VARCHAR | Unique identifier for the incident | case ID, incident ID |
| `date` | DATE | Date the incident occurred | incident date, occurrence date |
| `location` | VARCHAR | Street address or location description | address, incident location |
| `subject_statuses` | VARCHAR | Outcome status of subject(s) involved | subject outcome, result status |
| `subject_weapon` | VARCHAR | Type of weapon subject possessed | weapon type, subject's weapon |
| `subjects` | VARCHAR | Comma-separated names of subjects involved | subject names, involved parties |
| `subject_count` | BIGINT | Number of subjects in the incident | number of subjects |
| `officers` | VARCHAR | Comma-separated names of officers involved | officer names, responding officers |
| `officer_count` | BIGINT | Number of officers in the incident | number of officers |
| `grand_jury_disposition` | VARCHAR | Grand jury decision on the case | jury decision, disposition |
| `attorney_general_forms_url` | VARCHAR | URL to Attorney General forms | AG forms link, forms URL |
| `summary_url` | VARCHAR | URL to incident summary narrative | narrative URL, summary link |
| `summary_text` | VARCHAR | Full text of incident summary | narrative text, incident description |
| `latitude` | DOUBLE | Geographic latitude of incident location | lat |
| `longitude` | DOUBLE | Geographic longitude of incident location | lon |

**Notable Values:**
- `subject_statuses`: "1 Deceased 1 Injured", "2 Injured", "Deceased", "Deceased Injured", "Injured", "Other", "Shoot and Miss"
- `grand_jury_disposition`: "No Bill", "Pending", "Redden", "Craig W/M", "See Summary", "True Bill"

---

### Table: `Dallas.officers`
**Meaning:** Individual officer records for officers involved in OIS incidents.  
**Synonyms:** responding officers, police officers, officer details

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `case_number` | VARCHAR | Foreign key linking to incidents table | case ID, incident ID |
| `race` | VARCHAR | Officer's race/ethnicity code | ethnicity, racial category |
| `gender` | VARCHAR | Officer's gender | sex |
| `last_name` | VARCHAR | Officer's surname | surname, family name |
| `first_name` | VARCHAR | Officer's given name | given name, first name |
| `full_name` | VARCHAR | Officer's complete name formatted as "Last, First" | officer name, name |

**Notable Values:**
- `race`: "A" (Asian), "B" (Black), "L" (Latino), "W" (White)
- `gender`: "F" (Female), "M" (Male)

---

### Table: `Dallas.subjects`
**Meaning:** Individual subject records for subjects involved in OIS incidents.  
**Synonyms:** involved subjects, civilians, suspects, incident subjects

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `case_number` | VARCHAR | Foreign key linking to incidents table | case ID, incident ID |
| `race` | VARCHAR | Subject's race/ethnicity code | ethnicity, racial category |
| `gender` | VARCHAR | Subject's gender | sex |
| `last_name` | VARCHAR | Subject's surname | surname, family name |
| `first_name` | VARCHAR | Subject's given name | given name, first name |
| `full_name` | VARCHAR | Subject's complete name formatted as "Last, First" | subject name, name |

**Notable Values:**
- `race`: "A" (Asian), "B" (Black), "L" (Latino), "W" (White)
- `gender`: "F" (Female), "M" (Male)

---

## Join Paths

**Incidents to Officers:**
```sql
Dallas.incidents i
JOIN Dallas.officers o ON i.case_number = o.case_number
```

**Incidents to Subjects:**
```sql
Dallas.incidents i
JOIN Dallas.subjects s ON i.case_number = s.case_number
```

**All three tables:**
```sql
Dallas.incidents i
JOIN Dallas.officers o ON i.case_number = o.case_number
JOIN Dallas.subjects s ON i.case_number = s.case_number
```

---

## Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| Subject was deceased | `WHERE i.subject_statuses LIKE '%Deceased%'` |
| Subject was injured | `WHERE i.subject_statuses LIKE '%Injured%'` |
| Officer shot and missed | `WHERE i.subject_statuses = 'Shoot and Miss'` |
| Grand jury issued true bill | `WHERE i.grand_jury_disposition = 'True Bill'` |
| Grand jury issued no bill | `WHERE i.grand_jury_disposition = 'No Bill'` |
| Case pending grand jury | `WHERE i.grand_jury_disposition = 'Pending'` |
| Subject had weapon | `WHERE i.subject_weapon IS NOT NULL AND i.subject_weapon != ''` |
| Subject had vehicle as weapon | `WHERE i.subject_weapon = 'Vehicle'` |
| Subject had handgun | `WHERE i.subject_weapon = 'Handgun'` |
| Subject had shotgun | `WHERE i.subject_weapon = 'Shotgun'` |
| Multiple subjects involved | `WHERE i.subject_count > 1` |
| Multiple officers involved | `WHERE i.officer_count > 1` |
| Officer is male | `WHERE o.gender = 'M'` |
| Officer is female | `WHERE o.gender = 'F'` |
| Officer is White | `WHERE o.race = 'W'` |
| Officer is Black | `WHERE o.race = 'B'` |
| Officer is Latino | `WHERE o.race = 'L'` |
| Officer is Asian | `WHERE o.race = 'A'` |
| Subject is male | `WHERE s.gender = 'M'` |
| Subject is female | `WHERE s.gender = 'F'` |
| Subject is White | `WHERE s.race = 'W'` |
| Subject is Black | `WHERE s.race = 'B'` |
| Subject is Latino | `WHERE s.race = 'L'` |
| Subject is Asian | `WHERE s.race = 'A'` |

---

## Synonym Glossary

| Common Term | Schema Reference |
|-------------|------------------|
| fatal shooting | `WHERE i.subject_statuses = 'Deceased'` |
| non-fatal shooting | `WHERE i.subject_statuses IN ('Injured', 'Shoot and Miss')` |
| officer-involved shooting | `FROM Dallas.incidents` |
| OIS case | `FROM Dallas.incidents` |
| incident outcome | `i.subject_statuses` |
| jury decision | `i.grand_jury_disposition` |
| case disposition | `i.grand_jury_disposition` |
| officer demographics | `Dallas.officers (race, gender)` |
| subject demographics | `Dallas.subjects (race, gender)` |
| incident location | `i.location` |
| incident coordinates | `i.latitude, i.longitude` |
| incident narrative | `i.summary_text` |
| weapon type | `i.subject_weapon` |
| number of people involved | `i.subject_count + i.officer_count` |
| officer count | `i.officer_count` |
| subject count | `i.subject_count` |