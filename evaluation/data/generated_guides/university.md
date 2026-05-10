# University Schema Reference Guide

## Schema Summary
The `university` schema contains academic data for students, courses, professors, course registrations, and research assistant assignments, enabling analysis of enrollment, performance, and academic staffing.

---

## Table Reference

### `university.student`
**Meaning:** Individual student records; synonyms: learner, enrollee, pupil

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `student_id` | BIGINT | Unique student identifier | student number, ID |
| `intelligence` | VARCHAR | Student academic aptitude level | ability, academic level |
| `ranking` | VARCHAR | Student class rank or tier | class rank, tier, standing |

**Notable Values:**
- `intelligence`: 1, 2, 3
- `ranking`: 1, 2, 3, 4, 5

---

### `university.course`
**Meaning:** Course catalog and metadata; synonyms: class, subject, offering

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `course_id` | BIGINT | Unique course identifier | class ID, course number |
| `rating` | VARCHAR | Course quality or difficulty rating | score, evaluation |
| `diff` | VARCHAR | Course difficulty level | difficulty, complexity |

**Notable Values:**
- `rating`: 1, 2
- `diff`: 1, 2

---

### `university.prof`
**Meaning:** Professor records and evaluation metrics; synonyms: instructor, faculty, teacher

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `prof_id` | BIGINT | Unique professor identifier | instructor ID, faculty ID |
| `popularity` | VARCHAR | Professor popularity or approval rating | approval, favorability |
| `teachingability` | VARCHAR | Professor teaching effectiveness score | teaching quality, effectiveness |

**Notable Values:**
- `popularity`: 1, 2
- `teachingability`: 2, 3

---

### `university.registration`
**Meaning:** Student course enrollments and performance; synonyms: enrollment, course registration, grade record

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `course_id` | BIGINT | Reference to enrolled course | class ID |
| `student_id` | BIGINT | Reference to enrolled student | learner ID |
| `grade` | VARCHAR | Letter grade or numeric grade value | mark, score |
| `sat` | VARCHAR | Student satisfaction rating | satisfaction, feedback score |

**Notable Values:**
- `grade`: 1, 2, 3, 4 (numeric representation; 1=F, 2=D, 3=C, 4=B/A range)
- `sat`: 1, 2, 3 (satisfaction scale)

---

### `university.RA`
**Meaning:** Research assistant assignments and compensation; synonyms: research assistant record, RA assignment, research staff

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `student_id` | BIGINT | Reference to student serving as RA | RA student, research assistant ID |
| `prof_id` | BIGINT | Reference to supervising professor | supervisor ID, faculty advisor |
| `capability` | VARCHAR | RA skill or performance level | skill level, competency |
| `salary` | VARCHAR | RA compensation tier | pay level, compensation |

**Notable Values:**
- `capability`: 1, 2, 3, 4, 5
- `salary`: high, low, med

---

## Join Paths

| Join | SQL Condition |
|------|---------------|
| Student to Registration | `student.student_id = registration.student_id` |
| Registration to Course | `registration.course_id = course.course_id` |
| RA to Student | `RA.student_id = student.student_id` |
| RA to Professor | `RA.prof_id = prof.prof_id` |
| Course to Professor (via Registration) | `registration.course_id = course.course_id` AND `registration.student_id = RA.student_id` AND `RA.prof_id = prof.prof_id` |

---

## Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| Active student (has course registration) | `WHERE registration.student_id IS NOT NULL` |
| Course enrollment under 5 students (cancellation candidate) | `HAVING COUNT(registration.student_id) < 5` |
| GPA calculation: grade 1 = 0.0 (F) | `CASE WHEN registration.grade = 1 THEN 0.0 ...` |
| GPA calculation: grade 2 = 1.0 (D) | `CASE WHEN registration.grade = 2 THEN 1.0 ...` |
| GPA calculation: grade 3 = 2.0 (C) | `CASE WHEN registration.grade = 3 THEN 2.0 ...` |
| GPA calculation: grade 4 = 3.0+ (B/A) | `CASE WHEN registration.grade = 4 THEN 3.0 ...` |
| Professor evaluation below 3.0 (flagged for review) | `WHERE prof.teachingability < 3` |
| RA flagged in enrollment metrics | `WHERE RA.student_id IS NOT NULL` |
| RA funding aggregation (by department, not individual) | `GROUP BY prof.prof_id` (never `GROUP BY RA.student_id`) |
| Repeat course attempt (student takes course >2 times) | `HAVING COUNT(registration.course_id) > 2 GROUP BY registration.student_id, registration.course_id` |
| Student satisfaction metric | `registration.sat` (values 1, 2, 3) |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| student record | `university.student` |
| learner ID | `student.student_id` |
| academic ability | `student.intelligence` |
| class rank | `student.ranking` |
| course offering | `university.course` |
| course ID | `course.course_id` |
| course difficulty | `course.diff` |
| course quality | `course.rating` |
| instructor | `university.prof` |
| professor ID | `prof.prof_id` |
| teaching effectiveness | `prof.teachingability` |
| instructor approval | `prof.popularity` |
| enrollment record | `university.registration` |
| student grade | `registration.grade` |
| student satisfaction | `registration.sat` |
| research assistant | `university.RA` |
| RA skill level | `RA.capability` |
| RA compensation | `RA.salary` |
| supervising professor | `RA.prof_id` |
| active enrollment | `registration.student_id` with non-null value |
| GPA scale | `registration.grade` mapped to 0.0–4.0 |
| low-enrollment course | `COUNT(registration.student_id) < 5` |
| professor review flag | `prof.teachingability < 3` |