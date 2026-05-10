# UW_std Schema Reference Guide

## Schema Summary
This schema models academic advising relationships, course offerings, and teaching assignments within a university department, tracking person roles (professor/student), positions, and program phases.

---

## Join Paths

**Students and their advisors:**
```sql
FROM UW_std.person student
JOIN UW_std.advisedBy ab ON student.p_id = ab.p_id
JOIN UW_std.person advisor ON ab.p_id_dummy = advisor.p_id
WHERE student.student = '1' AND advisor.professor = '1'
```

**Courses and instructors:**
```sql
FROM UW_std.course c
JOIN UW_std.taughtBy tb ON c.course_id = tb.course_id
JOIN UW_std.person prof ON tb.p_id = prof.p_id
WHERE prof.professor = '1'
```

**Professors and their advisees:**
```sql
FROM UW_std.person prof
JOIN UW_std.advisedBy ab ON prof.p_id = ab.p_id_dummy
JOIN UW_std.person student ON ab.p_id = student.p_id
WHERE prof.professor = '1' AND student.student = '1'
```

---

## Table Reference

### `UW_std.advisedBy`
Advising relationships between students and faculty.
- **p_id**: Student person ID
- **p_id_dummy**: Advisor person ID

### `UW_std.course`
Course offerings.
- **course_id**: Unique course identifier
- **courseLevel**: Course classification — `Level_300`, `Level_400`, `Level_500`

### `UW_std.person`
University members (students, professors, or both).
- **p_id**: Unique person identifier
- **professor**: Binary flag — `'1'` = professor, `'0'` = not professor
- **student**: Binary flag — `'1'` = student, `'0'` = not student
- **hasPosition**: Employment status — `'0'` (none), `'Faculty'`, `'Faculty_adj'`, `'Faculty_aff'`, `'Faculty_eme'`
- **inPhase**: Graduate program phase — `'0'` (N/A), `'Pre_Quals'`, `'Post_Quals'`, `'Post_Generals'`
- **yearsInProgram**: Tenure in program — `'0'` (N/A), `'Year_1'` through `'Year_12'`

### `UW_std.taughtBy`
Course-instructor assignments.
- **course_id**: Course being taught
- **p_id**: Instructor person ID