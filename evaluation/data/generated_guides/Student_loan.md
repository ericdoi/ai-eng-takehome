# Student Loan Schema Reference Guide

## Schema Summary
The `Student_loan` schema tracks student enrollment, financial status, military service, employment, and loan payment information for a cohort of students across multiple institutions.

---

## Table Reference

### `Student_loan.person`
**Meaning:** Master list of all students in the dataset.  
**Synonyms:** student roster, student directory

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name` | VARCHAR | Unique student identifier | student ID, student name |

---

### `Student_loan.male`
**Meaning:** Students identified as male.  
**Synonyms:** gender, male students

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name` | VARCHAR | Student identifier | student ID |

---

### `Student_loan.disabled`
**Meaning:** Students with disability status.  
**Synonyms:** disability, disabled students

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name` | VARCHAR | Student identifier | student ID |

---

### `Student_loan.unemployed`
**Meaning:** Students currently unemployed.  
**Synonyms:** unemployment, jobless students

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name` | VARCHAR | Student identifier | student ID |

---

### `Student_loan.enrolled`
**Meaning:** Student enrollment records at schools with enrollment month.  
**Synonyms:** school enrollment, student registration

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name` | VARCHAR | Student identifier | student ID |
| `school` | VARCHAR | School code | institution, university |
| `month` | BIGINT | Month of enrollment (numeric) | enrollment month, month enrolled |

**Enumerated Values (school):**
- `occ` — Orange Coast College
- `smc` — Santa Monica College
- `ucb` — UC Berkeley
- `uci` — UC Irvine
- `ucla` — UCLA
- `ucsd` — UC San Diego

---

### `Student_loan.longest_absense_from_school`
**Meaning:** Maximum consecutive months each student was absent from school.  
**Synonyms:** absence duration, school absence, gap from school

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name` | VARCHAR | Student identifier | student ID |
| `month` | BIGINT | Longest absence duration in months | absence months, gap months |

---

### `Student_loan.enlist`
**Meaning:** Students who enlisted in military or service organizations.  
**Synonyms:** military service, military enlistment

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name` | VARCHAR | Student identifier | student ID |
| `organ` | VARCHAR | Military or service organization | organization, branch, service |

**Enumerated Values (organ):**
- `air_force` — U.S. Air Force
- `army` — U.S. Army
- `fire_department` — Fire Department
- `foreign_legion` — Foreign Legion
- `marines` — U.S. Marines
- `navy` — U.S. Navy
- `peace_corps` — Peace Corps

---

### `Student_loan.filed_for_bankrupcy`
**Meaning:** Students who filed for bankruptcy.  
**Synonyms:** bankruptcy, bankruptcy filing

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name` | VARCHAR | Student identifier | student ID |

---

### `Student_loan.no_payment_due`
**Meaning:** Student loan payment status (whether payment is due).  
**Synonyms:** payment status, payment due status

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name` | VARCHAR | Student identifier | student ID |
| `bool` | VARCHAR | Payment due indicator | payment due, status |

**Enumerated Values (bool):**
- `neg` — Payment is due (negative/no exemption)
- `pos` — Payment is not due (positive/exemption)

---

### `Student_loan.bool`
**Meaning:** Boolean value reference table.  
**Synonyms:** boolean values, status codes

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name` | VARCHAR | Boolean representation | value, status |

**Enumerated Values (name):**
- `neg` — Negative/No/False
- `pos` — Positive/Yes/True

---

## Join Paths

All tables join on student identity via the `name` column:

```sql
-- Join any table to person (master list)
FROM Student_loan.person p
LEFT JOIN Student_loan.male m ON p.name = m.name
LEFT JOIN Student_loan.disabled d ON p.name = d.name
LEFT JOIN Student_loan.unemployed u ON p.name = u.name
LEFT JOIN Student_loan.enrolled e ON p.name = e.name
LEFT JOIN Student_loan.longest_absense_from_school las ON p.name = las.name
LEFT JOIN Student_loan.enlist en ON p.name = en.name
LEFT JOIN Student_loan.filed_for_bankrupcy fb ON p.name = fb.name
LEFT JOIN Student_loan.no_payment_due npd ON p.name = npd.name
```

---

## Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| Student is male | `name IN (SELECT name FROM Student_loan.male)` |
| Student is disabled | `name IN (SELECT name FROM Student_loan.disabled)` |
| Student is unemployed | `name IN (SELECT name FROM Student_loan.unemployed)` |
| Student enlisted in military/service | `name IN (SELECT name FROM Student_loan.enlist)` |
| Student filed for bankruptcy | `name IN (SELECT name FROM Student_loan.filed_for_bankrupcy)` |
| Student has payment due | `npd.bool = 'neg'` (from `no_payment_due` table) |
| Student has no payment due | `npd.bool = 'pos'` (from `no_payment_due` table) |
| Student enrolled at specific school | `e.school = 'ucb'` (or other school code) |
| Student has absence record | `name IN (SELECT name FROM Student_loan.longest_absense_from_school)` |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| male student | `Student_loan.male.name` |
| disabled student | `Student_loan.disabled.name` |
| unemployed student | `Student_loan.unemployed.name` |
| enlisted student | `Student_loan.enlist.name` |
| bankruptcy filer | `Student_loan.filed_for_bankrupcy.name` |
| payment due | `Student_loan.no_payment_due.bool = 'neg'` |
| payment exempt | `Student_loan.no_payment_due.bool = 'pos'` |
| school enrollment | `Student_loan.enrolled.school` |
| enrollment month | `Student_loan.enrolled.month` |
| absence duration | `Student_loan.longest_absense_from_school.month` |
| military branch | `Student_loan.enlist.organ` |
| UC Berkeley | `Student_loan.enrolled.school = 'ucb'` |
| UCLA | `Student_loan.enrolled.school = 'ucla'` |
| UC San Diego | `Student_loan.enrolled.school = 'ucsd'` |
| UC Irvine | `Student_loan.enrolled.school = 'uci'` |
| Santa Monica College | `Student_loan.enrolled.school = 'smc'` |
| Orange Coast College | `Student_loan.enrolled.school = 'occ'` |