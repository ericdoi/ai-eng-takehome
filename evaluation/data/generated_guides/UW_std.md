# SQL Reference Guide: UW_std Schema

## 1. Schema Summary

The `UW_std` schema contains academic data for a university program, tracking students, professors, courses, teaching assignments, and advising relationships.

---

## 2. Table Reference

### Table: `UW_std.advisedBy`
**Meaning:** Advising relationships between students and faculty advisors.  
**Synonyms:** advisor assignments, mentorship records

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `p_id` | BIGINT | ID of the student being advised | student_id, advisee_id |
| `p_id_dummy` | BIGINT | ID of the faculty advisor | advisor_id, faculty_id |

---

### Table: `UW_std.course`
**Meaning:** Course catalog with course identifiers and academic levels.  
**Synonyms:** course catalog, course offerings

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `course_id` | BIGINT | Unique course identifier | course_code |
| `courseLevel` | VARCHAR | Academic level of the course | level, course_tier |

**Enumerated Values (courseLevel):**
- `Level_300`
- `Level_400`
- `Level_500`

---

### Table: `UW_std.person`
**Meaning:** University members (students and faculty) with role and program status information.  
**Synonyms:** people, users, members, participants

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `p_id` | BIGINT | Unique person identifier | person_id, user_id |
| `professor` | VARCHAR | Binary flag: 1 = faculty member, 0 = not faculty | is_professor, faculty_flag |
| `student` | VARCHAR | Binary flag: 1 = student, 0 = not student | is_student, student_flag |
| `hasPosition` | VARCHAR | Employment/position status | position_type, employment_status |
| `inPhase` | VARCHAR | Current phase in graduate program | program_phase, phase_status |
| `yearsInProgram` | VARCHAR | Years enrolled in program | tenure, program_duration |

**Enumerated Values (hasPosition):**
- `0` (no position)
- `Faculty`
- `Faculty_adj` (adjunct faculty)
- `Faculty_aff` (affiliated faculty)
- `Faculty_eme` (emeritus faculty)

**Enumerated Values (inPhase):**
- `0` (not applicable)
- `Pre_Quals` (pre-qualifying exams)
- `Post_Quals` (post-qualifying exams)
- `Post_Generals` (post-general exams)

**Enumerated Values (yearsInProgram):**
- `0` (not applicable)
- `Year_1`, `Year_2`, `Year_3`, `Year_4`, `Year_5`, `Year_6`, `Year_7`, `Year_8`, `Year_9`, `Year_10`, `Year_12`

---

### Table: `UW_std.taughtBy`
**Meaning:** Teaching assignments linking courses to instructors.  
**Synonyms:** course_instructor, course_assignments, teaching_records

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `course_id` | BIGINT | ID of the course being taught | course_code |
| `p_id` | BIGINT | ID of the instructor teaching the course | instructor_id, professor_id, faculty_id |

---

## 3. Join Paths

| From | To | Condition |
|------|----|-----------| 
| `advisedBy` → `person` (student) | `advisedBy.p_id = person.p_id` | Retrieve student details |
| `advisedBy` → `person` (advisor) | `advisedBy.p_id_dummy = person.p_id` | Retrieve advisor details |
| `taughtBy` → `course` | `taughtBy.course_id = course.course_id` | Retrieve course details |
| `taughtBy` → `person` | `taughtBy.p_id = person.p_id` | Retrieve instructor details |
| `course` → `taughtBy` | `course.course_id = taughtBy.course_id` | Find instructors for a course |
| `person` → `taughtBy` | `person.p_id = taughtBy.p_id` | Find courses taught by a person |
| `person` → `advisedBy` (as advisor) | `person.p_id = advisedBy.p_id_dummy` | Find advisees for a faculty member |
| `person` → `advisedBy` (as student) | `person.p_id = advisedBy.p_id` | Find advisor for a student |

---

## 4. Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| Identify faculty members | `WHERE person.professor = '1'` |
| Identify students | `WHERE person.student = '1'` |
| Identify faculty with formal position | `WHERE person.hasPosition IN ('Faculty', 'Faculty_adj', 'Faculty_aff', 'Faculty_eme')` |
| Identify adjunct faculty | `WHERE person.hasPosition = 'Faculty_adj'` |
| Identify emeritus faculty | `WHERE person.hasPosition = 'Faculty_eme'` |
| Identify students in pre-qualifying phase | `WHERE person.inPhase = 'Pre_Quals'` |
| Identify students in post-qualifying phase | `WHERE person.inPhase = 'Post_Quals'` |
| Identify students in post-generals phase | `WHERE person.inPhase = 'Post_Generals'` |
| Filter 300-level courses | `WHERE course.courseLevel = 'Level_300'` |
| Filter 400-level courses | `WHERE course.courseLevel = 'Level_400'` |
| Filter 500-level courses | `WHERE course.courseLevel = 'Level_500'` |
| Find students with advisors | `INNER JOIN advisedBy ON person.p_id = advisedBy.p_id` |
| Find courses taught by a specific instructor | `INNER JOIN taughtBy ON person.p_id = taughtBy.p_id INNER JOIN course ON taughtBy.course_id = course.course_id` |

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| faculty member, professor | `person.professor = '1'` |
| student | `person.student = '1'` |
| advisor, faculty advisor | `advisedBy.p_id_dummy` (join to `person`) |
| advisee, student being advised | `advisedBy.p_id` (join to `person`) |
| instructor, course instructor, teacher | `taughtBy.p_id` (join to `person`) |
| course level, course tier | `course.courseLevel` |
| program phase, graduate phase | `person.inPhase` |
| years in program, program tenure | `person.yearsInProgram` |
| position type, employment status | `person.hasPosition` |
| teaching assignment | `taughtBy` table |
| advising relationship | `advisedBy` table |
| upper-level course | `course.courseLevel IN ('Level_400', 'Level_500')` |
| introductory course | `course.courseLevel = 'Level_300'` |