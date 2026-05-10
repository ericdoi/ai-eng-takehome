# Student Loan Schema Reference Guide

## Schema Summary
This schema tracks student loan borrower attributes including enrollment status, employment, military service, disability, bankruptcy filing, and payment obligations across a population of students.

## Join Paths

**Student to enrollment history:**
```sql
FROM Student_loan.person p
LEFT JOIN Student_loan.enrolled e ON p.name = e.name
```

**Student to all attributes (comprehensive):**
```sql
FROM Student_loan.person p
LEFT JOIN Student_loan.enrolled e ON p.name = e.name
LEFT JOIN Student_loan.male m ON p.name = m.name
LEFT JOIN Student_loan.unemployed u ON p.name = u.name
LEFT JOIN Student_loan.disabled d ON p.name = d.name
LEFT JOIN Student_loan.enlist en ON p.name = en.name
LEFT JOIN Student_loan.filed_for_bankrupcy fb ON p.name = fb.name
LEFT JOIN Student_loan.longest_absense_from_school las ON p.name = las.name
LEFT JOIN Student_loan.no_payment_due npd ON p.name = npd.name
```

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| student identifier | `Student_loan.person.name` |
| gender (male) | `Student_loan.male.name` (presence indicates male) |
| unemployed status | `Student_loan.unemployed.name` (presence indicates unemployed) |
| disability status | `Student_loan.disabled.name` (presence indicates disabled) |
| military service | `Student_loan.enlist.organ` |
| bankruptcy | `Student_loan.filed_for_bankrupcy.name` (presence indicates filed) |
| payment obligation | `Student_loan.no_payment_due.bool` (values: 'neg'=payment due, 'pos'=no payment due) |
| school enrollment | `Student_loan.enrolled.school` |
| enrollment month | `Student_loan.enrolled.month` |
| longest gap from school | `Student_loan.longest_absense_from_school.month` |

## Table Reference

### `Student_loan.person`
Master student roster. All other tables join on `name`.

---

### `Student_loan.enrolled`
Current or historical school enrollment records.

| Column | Notes |
|--------|-------|
| `school` | Enumerated: `occ`, `smc`, `ucb`, `uci`, `ucla`, `ucsd` |
| `month` | Month of enrollment (BIGINT) |

---

### `Student_loan.male`
Presence in this table indicates student is male. No other attributes.

---

### `Student_loan.unemployed`
Presence in this table indicates student is currently unemployed. No other attributes.

---

### `Student_loan.disabled`
Presence in this table indicates student has a disability. No other attributes.

---

### `Student_loan.enlist`
Military or service organization enrollment.

| Column | Notes |
|--------|-------|
| `organ` | Enumerated: `air_force`, `army`, `fire_department`, `foreign_legion`, `marines`, `navy`, `peace_corps` |

---

### `Student_loan.filed_for_bankrupcy`
Presence in this table indicates student has filed for bankruptcy. No other attributes.

---

### `Student_loan.longest_absense_from_school`
Duration of longest continuous absence from school.

| Column | Notes |
|--------|-------|
| `month` | Number of months absent (BIGINT) |

---

### `Student_loan.no_payment_due`
Payment obligation status.

| Column | Notes |
|--------|-------|
| `bool` | Enumerated: `neg` (payment is due), `pos` (no payment due) |

---

### `Student_loan.bool`
Reference table for boolean values. Not typically queried directly.

| Column | Notes |
|--------|-------|
| `name` | Enumerated: `neg`, `pos` |