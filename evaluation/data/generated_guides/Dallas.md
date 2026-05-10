# Dallas Police Officer-Involved Shootings Schema Reference

## Schema Summary
This schema documents officer-involved shooting (OIS) incidents in Dallas, with details on incidents, officers involved, and subjects involved.

---

## Join Paths

**Incidents with officers:**
```sql
FROM Dallas.incidents i
JOIN Dallas.officers o ON i.case_number = o.case_number
```

**Incidents with subjects:**
```sql
FROM Dallas.incidents i
JOIN Dallas.subjects s ON i.case_number = s.case_number
```

**All three tables:**
```sql
FROM Dallas.incidents i
JOIN Dallas.officers o ON i.case_number = o.case_number
JOIN Dallas.subjects s ON i.case_number = s.case_number
```

---

## Table Reference

### `Dallas.incidents`
Officer-involved shooting incidents. Primary key: `case_number`.

| Column | Notes |
|--------|-------|
| `case_number` | Unique incident identifier |
| `date` | Incident date |
| `location` | Street address or location description |
| `subject_statuses` | Outcome for subject(s). Enum: `Deceased`, `Injured`, `Deceased Injured`, `1 Deceased 1 Injured`, `2 Injured`, `Shoot and Miss`, `Other` |
| `subject_weapon` | Weapon possessed by subject. Examples: `Vehicle`, `Handgun`, `Shotgun` |
| `subject_count` | Number of subjects involved |
| `officer_count` | Number of officers involved |
| `grand_jury_disposition` | Legal outcome. Enum: `No Bill`, `True Bill`, `Pending`, `Redden`, `Craig W/M`, `See Summary` |
| `latitude`, `longitude` | Incident coordinates |
| `attorney_general_forms_url` | Link to AG forms (often NULL) |
| `summary_url` | Link to incident narrative |
| `summary_text` | Full incident narrative text |

### `Dallas.officers`
Officers involved in incidents. Foreign key: `case_number` → `Dallas.incidents.case_number`.

| Column | Notes |
|--------|-------|
| `case_number` | Links to incident |
| `race` | Enum: `W` (White), `B` (Black), `L` (Latino), `A` (Asian) |
| `gender` | Enum: `M` (Male), `F` (Female) |
| `full_name` | Format: "LastName, FirstName" |

### `Dallas.subjects`
Subjects involved in incidents. Foreign key: `case_number` → `Dallas.incidents.case_number`.

| Column | Notes |
|--------|-------|
| `case_number` | Links to incident |
| `race` | Enum: `W` (White), `B` (Black), `L` (Latino), `A` (Asian) |
| `gender` | Enum: `M` (Male), `F` (Female) |
| `full_name` | Format: "LastName, FirstName" |

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| Fatal shooting | `WHERE Dallas.incidents.subject_statuses = 'Deceased'` |
| Non-lethal outcome | `WHERE Dallas.incidents.subject_statuses IN ('Injured', 'Shoot and Miss', 'Other')` |
| Pending case | `WHERE Dallas.incidents.grand_jury_disposition = 'Pending'` |
| Indicted | `WHERE Dallas.incidents.grand_jury_disposition = 'True Bill'` |
| No charges | `WHERE Dallas.incidents.grand_jury_disposition = 'No Bill'` |
| Officer demographics | `Dallas.officers.race`, `Dallas.officers.gender` |
| Subject demographics | `Dallas.subjects.race`, `Dallas.subjects.gender` |