# University Schema Reference Guide

## Schema Summary
This schema tracks student academic records, course offerings, professor attributes, and research assistant assignments within a university system.

---

## Join Paths

**Students and their course registrations:**
```sql
FROM university.student s
JOIN university.registration r ON s.student_id = r.student_id
JOIN university.course c ON r.course_id = c.course_id
```

**Students and their RA assignments:**
```sql
FROM university.student s
JOIN university.RA ra ON s.student_id = ra.student_id
JOIN university.prof p ON ra.prof_id = p.prof_id
```

**Professors and their RA supervisees:**
```sql
FROM university.prof p
JOIN university.RA ra ON p.prof_id = ra.prof_id
JOIN university.student s ON ra.student_id = s.student_id
```

**Complete student academic profile:**
```sql
FROM university.student s
LEFT JOIN university.registration r ON s.student_id = r.student_id
LEFT JOIN university.course c ON r.course_id = c.course_id
LEFT JOIN university.RA ra ON s.student_id = ra.student_id
```

---

## Business Rules as SQL

| Rule | SQL Condition |
|------|---------------|
| Active student (has registration) | `WHERE EXISTS (SELECT 1 FROM university.registration WHERE student_id = s.student_id)` |
| Course flagged for cancellation | `WHERE (SELECT COUNT(*) FROM university.registration WHERE course_id = c.course_id) < 5` |
| RA compliance check | `WHERE ra.salary IN ('high', 'med', 'low')` — aggregate by prof_id, never individual |
| Professor evaluation flagged for review | `WHERE p.popularity = '1'` (below 3.0 threshold on 5-point scale) |
| RA capability threshold | `WHERE ra.capability >= 3` |

---

## Synonym Glossary

| Common Term | Schema Reference |
|-------------|------------------|
| Student performance | `university.student.intelligence`, `university.student.ranking` |
| Course difficulty | `university.course.diff` (values: 1, 2) |
| Course quality | `university.course.rating` (values: 1, 2) |
| Student satisfaction | `university.registration.sat` (values: 1, 2, 3) |
| Student grade | `university.registration.grade` (values: 1, 2, 3, 4) |
| Professor teaching quality | `university.prof.teachingability` (values: 2, 3) |
| Professor popularity | `university.prof.popularity` (values: 1, 2) |
| RA skill level | `university.RA.capability` (values: 1–5) |
| RA compensation | `university.RA.salary` (values: high, med, low) |

---

## Table Reference

### `university.student`
**Meaning:** Individual student records.

| Column | Semantics |
|--------|-----------|
| `student_id` | Primary key; unique student identifier |
| `intelligence` | Enumerated: 1, 2, 3 (higher = more capable) |
| `ranking` | Enumerated: 1, 2, 3, 4, 5 (1 = top rank) |

---

### `university.registration`
**Meaning:** Course enrollment records linking students to courses with performance data.

| Column | Semantics |
|--------|-----------|
| `student_id` | Foreign key to `university.student` |
| `course_id` | Foreign key to `university.course` |
| `grade` | Enumerated: 1, 2, 3, 4 (numeric grade representation; no direct 4.0 scale mapping provided in schema) |
| `sat` | Student satisfaction; enumerated: 1, 2, 3 (higher = more satisfied) |

---

### `university.course`
**Meaning:** Course catalog with difficulty and quality ratings.

| Column | Semantics |
|--------|-----------|
| `course_id` | Primary key; unique course identifier |
| `rating` | Course quality; enumerated: 1, 2 |
| `diff` | Course difficulty; enumerated: 1, 2 |

---

### `university.prof`
**Meaning:** Professor attributes and evaluation metrics.

| Column | Semantics |
|--------|-----------|
| `prof_id` | Primary key; unique professor identifier |
| `popularity` | Enumerated: 1, 2 (1 = below review threshold; 2 = acceptable) |
| `teachingability` | Enumerated: 2, 3 (higher = stronger teaching performance) |

---

### `university.RA`
**Meaning:** Research assistant assignments linking students to supervising professors with capability and compensation data.

| Column | Semantics |
|--------|-----------|
| `student_id` | Foreign key to `university.student`; RA is also a student |
| `prof_id` | Foreign key to `university.prof`; supervising professor |
| `capability` | RA skill level; enumerated: 1, 2, 3, 4, 5 (higher = more capable) |
| `salary` | Compensation tier; enumerated: high, med, low (aggregate by prof_id only; never report individually) |