# Employee Schema Reference Guide

## Schema Summary
This schema contains employee master data, department assignments, compensation history, and job titles with effective date ranges for a multi-department organization.

---

## Join Paths

### Current Employee with Department
```sql
FROM employee.employees e
JOIN employee.dept_emp de ON e.emp_no = de.emp_no
  AND de.to_date = '9999-01-01'
JOIN employee.departments d ON de.dept_no = d.dept_no
```
**[REQUIRED]** — to identify which department each active employee currently belongs to.

### Current Employee with Title
```sql
FROM employee.employees e
JOIN employee.titles t ON e.emp_no = t.emp_no
  AND t.to_date = '9999-01-01'
```
**[REQUIRED]** — to identify current job title.

### Current Employee with Salary
```sql
FROM employee.employees e
JOIN employee.salaries s ON e.emp_no = s.emp_no
  AND s.to_date = '9999-01-01'
```
**[REQUIRED]** — to identify current compensation.

### Current Department Manager
```sql
FROM employee.departments d
JOIN employee.dept_manager dm ON d.dept_no = dm.dept_no
  AND dm.to_date = '9999-01-01'
JOIN employee.employees e ON dm.emp_no = e.emp_no
```
**[REQUIRED]** — to identify active manager for each department.

### Employee Full History (All Departments)
```sql
FROM employee.employees e
JOIN employee.dept_emp de ON e.emp_no = de.emp_no
JOIN employee.departments d ON de.dept_no = d.dept_no
```
**[OPTIONAL — display only]** — use `d.dept_name` only when question explicitly asks for department names; otherwise filter/group by `de.dept_no` directly.

### Employee Full History (All Titles)
```sql
FROM employee.employees e
JOIN employee.titles t ON e.emp_no = t.emp_no
```
**[OPTIONAL — display only]** — use `t.title` only when question explicitly asks for job titles; otherwise filter/group by title string directly.

### Employee Full History (All Salaries)
```sql
FROM employee.employees e
JOIN employee.salaries s ON e.emp_no = s.emp_no
```
**[OPTIONAL — display only]** — use for compensation trend analysis across all historical records.

---

## Business Rules as SQL

### Legacy Workforce Identification
- **IDENTIFY legacy workforce:** `WHERE e.hire_date < '1990-01-01'` — employees hired before 1990-01-01 are part of the legacy workforce and must be analyzed separately in retention studies.

### Current Department Assignment (Headcount)
- **IDENTIFY current department:** `WHERE de.to_date = '9999-01-01'` — only these records represent active assignments.
- **EXCLUDE duplicate employees:** Use `ROW_NUMBER() OVER (PARTITION BY e.emp_no ORDER BY de.from_date DESC)` and filter `WHERE rn = 1` to count each employee only once by most recent department.

### Department Manager Exclusion
- **EXCLUDE managers from headcount:** `WHERE e.emp_no NOT IN (SELECT emp_no FROM employee.dept_manager WHERE to_date = '9999-01-01')` — department managers must not be counted in non-management headcount metrics.

### Customer Service Department Split (d009)
- **FLAG historical comparisons:** `WHERE de.dept_no = 'd009' AND de.from_date < '2005-01-01'` — Customer Service (d009) was split in 2005; headcount comparisons before and after this date are not directly comparable.

### Title Correction (Hire-Date Proximity)
- **IDENTIFY title corrections:** `WHERE t.from_date <= DATE_ADD(e.hire_date, INTERVAL 90 DAY) AND t.from_date >= e.hire_date` — title changes within 90 days of hire are corrections and do not count as promotions.

### Senior Engineer Comparability
- **IDENTIFY comparable Senior Engineer records:** `WHERE t.title = 'Senior Engineer' AND t.from_date >= '1995-01-01'` — Senior Engineer title can only be compared with records from 1995 onward due to title inflation.

### Tenure Risk Flag
- **IDENTIFY tenure risk:** `WHERE t.title = t_current.title AND DATEDIFF(CURDATE(), t.from_date) > 2555` (7 years in days) — employees with the same title for more than 7 years should be flagged as retention risk.

### Salary Outlier Detection
- **IDENTIFY outliers:** `WHERE ABS(s.salary - dept_mean) > 3 * dept_stddev` — salaries more than 3 standard deviations from department mean; flag but do not exclude.
- **Numerator (outlier count):** `COUNT(CASE WHEN ABS(s.salary - dept_mean) > 3 * dept_stddev THEN 1 END)`
- **Denominator (total salaries in department):** `COUNT(*)`

### Salary Privacy Threshold
- **EXCLUDE small groups:** `HAVING COUNT(DISTINCT e.emp_no) < 5` — never report salary ranges with fewer than 5 employees; aggregate to broader grouping.

### Gender Reporting Minimum Cell Size
- **EXCLUDE small gender groups:** `HAVING COUNT(*) < 10` — gender-based analytics require minimum cell size of 10 to be reported.

### Pay Equity Analysis (Control Variables)
- **Control for department, title, tenure:** Group by `de.dept_no`, `t.title`, and tenure bucket (e.g., `CASE WHEN DATEDIFF(CURDATE(), e.hire_date) < 1825 THEN '0-5y' ...`), then calculate salary difference by gender within each group before reporting aggregate gaps.

---

## Synonym Glossary

| Question Term | Schema Identifier |
|---|---|
| current department | `employee.dept_emp WHERE to_date = '9999-01-01'` |
| active employee | `employee.employees` with `employee.dept_emp.to_date = '9999-01-01'` |
| current salary | `employee.salaries WHERE to_date = '9999-01-01'` |
| current title | `employee.titles WHERE to_date = '9999-01-01'` |
| current manager | `employee.dept_manager WHERE to_date = '9999-01-01'` |
| tenure (years) | `DATEDIFF(CURDATE(), employee.employees.hire_date) / 365.25` |
| legacy employee | `employee.employees WHERE hire_date < '1990-01-01'` |
| promotion | Title change where `from_date > DATE_ADD(hire_date, INTERVAL 90 DAY)` |
| headcount | `COUNT(DISTINCT e.emp_no)` with `ROW_NUMBER()` to select most recent dept_emp |
| compensation history | `employee.salaries` with all `to_date` values (not filtered to current) |
| job history | `employee.titles` with all `to_date` values (not filtered to current) |

---

## Table Reference

### `employee.employees`
Master employee records. Synonyms: *staff*, *personnel*, *workforce*.

| Column | Notes |
|---|---|
| `emp_no` | Primary key; BIGINT. |
| `hire_date` | Used to calculate tenure and identify legacy workforce (< 1990-01-01). |
| `birth_date` | Never report individual ages; aggregate by decade only (30s, 40s, 50s). |
| `gender` | Enum: `'F'`, `'M'`. Requires minimum cell size of 10 for reporting. |

---

### `employee.departments`
Department master list. Synonyms: *org unit*, *division*, *team*.

| Column | Notes |
|---|---|
| `dept_no` | Primary key; VARCHAR. Enum: `'d001'` (Marketing), `'d002'` (Finance), `'d003'` (Human Resources), `'d004'` (Production), `'d005'` (Development), `'d006'` (Quality Management), `'d007'` (Sales), `'d008'` (Research), `'d009'` (Customer Service — split in 2005). |
| `dept_name` | Human-readable department name; use only for display. |

---

### `employee.dept_emp`
Employee-to-department assignments with effective date ranges. Synonyms: *department membership*, *org assignment*.

| Column | Notes |
|---|---|
| `emp_no` | Foreign key to `employee.employees`. |
| `dept_no` | Foreign key to `employee.departments`. |
| `from_date` | Assignment start date. |
| `to_date` | Assignment end date. Sentinel value `'9999-01-01'` indicates currently active. For headcount, use only records where `to_date = '9999-01-01'` and select most recent by `from_date` per employee. |

---

### `employee.salaries`
Compensation history with effective date ranges. Synonyms: *compensation*, *pay*, *wage*.

| Column | Notes |
|---|---|
| `emp_no` | Foreign key to `employee.employees`. |
| `salary` | BIGINT; point-in-time value. Always specify effective date range when reporting. Flag outliers (> 3 std dev from department mean) but do not exclude. |
| `from_date` | Salary effective start date. |
| `to_date` | Salary effective end date. Sentinel value `'9999-01-01'` indicates currently active. |

---

### `employee.titles`
Job title history with effective date ranges. Synonyms: *job title*, *position*, *role*.

| Column | Notes |
|---|---|
| `emp_no` | Foreign key to `employee.employees`. |
| `title` | Enum: `'Assistant Engineer'`, `'Engineer'`, `'Manager'`, `'Senior Engineer'` (comparable only from 1995 onward), `'Senior Staff'`, `'Staff'`, `'Technique Leader'`. |
| `from_date` | Title effective start date. Title changes within 90 days of hire are corrections, not promotions. |
| `to_date` | Title effective end date. Sentinel value `'9999-01-01'` indicates currently active. Employees with same title for > 7 years should be flagged as tenure risk. |

---

### `employee.dept_manager`
Department manager assignments with effective date ranges. Synonyms: *management*, *leadership*.

| Column | Notes |
|---|---|
| `dept_no` | Foreign key to `employee.departments`. |
| `emp_no` | Foreign key to `employee.employees`. |
| `from_date` | Management assignment start date. |
| `to_date` | Management assignment end date. Sentinel value `'9999-01-01'` indicates currently active. Exclude these employees from non-management headcount metrics. |