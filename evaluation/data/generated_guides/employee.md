# Employee Schema Reference Guide

## Schema Summary
The `employee` schema contains HR master data: employee demographics, department assignments, management hierarchies, compensation history, and job titles with effective date ranges.

---

## Join Paths

**Current department assignment for an employee:**
```sql
SELECT e.emp_no, e.first_name, e.last_name, d.dept_no, d.dept_name
FROM employee.employees e
JOIN employee.dept_emp de ON e.emp_no = de.emp_no
JOIN employee.departments d ON de.dept_no = d.dept_no
WHERE de.to_date = '9999-01-01'
```

**Current salary for an employee:**
```sql
SELECT e.emp_no, e.first_name, s.salary, s.from_date, s.to_date
FROM employee.employees e
JOIN employee.salaries s ON e.emp_no = s.emp_no
WHERE s.to_date = '9999-01-01'
```

**Current title for an employee:**
```sql
SELECT e.emp_no, e.first_name, t.title, t.from_date, t.to_date
FROM employee.employees e
JOIN employee.titles t ON e.emp_no = t.emp_no
WHERE t.to_date = '9999-01-01'
```

**Department manager details:**
```sql
SELECT d.dept_no, d.dept_name, dm.emp_no, e.first_name, e.last_name, dm.from_date, dm.to_date
FROM employee.dept_manager dm
JOIN employee.departments d ON dm.dept_no = d.dept_no
JOIN employee.employees e ON dm.emp_no = e.emp_no
WHERE dm.to_date = '9999-01-01'
```

---

## Business Rules as SQL

**Legacy workforce (hired before 1990):**
```sql
WHERE e.hire_date < '1990-01-01'
```

**Current employees only:**
```sql
WHERE de.to_date = '9999-01-01'
```

**Exclude department managers from headcount:**
```sql
WHERE e.emp_no NOT IN (
  SELECT emp_no FROM employee.dept_manager WHERE to_date = '9999-01-01'
)
```

**Most recent department assignment (for single-count headcount):**
```sql
WHERE de.emp_no IN (
  SELECT emp_no FROM employee.dept_emp
  WHERE to_date = '9999-01-01'
)
```

**Title change within 90 days of hire (correction, not promotion):**
```sql
WHERE DATEDIFF(DAY, e.hire_date, t.from_date) <= 90
```

**Tenure risk (same title for 7+ years):**
```sql
WHERE DATEDIFF(DAY, t.from_date, t.to_date) >= 2555
  AND t.to_date = '9999-01-01'
```

**Senior Engineer title (valid from 1995 onward only):**
```sql
WHERE t.title = 'Senior Engineer' AND t.from_date >= '1995-01-01'
```

**Minimum cell size for gender reporting (10+ employees):**
```sql
GROUP BY e.gender
HAVING COUNT(e.emp_no) >= 10
```

**Salary outlier flag (3+ standard deviations from department mean):**
```sql
WHERE ABS(s.salary - dept_mean) > 3 * dept_stddev
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| tenure (years) | `DATEDIFF(YEAR, e.hire_date, GETDATE())` |
| age by decade | `FLOOR(DATEDIFF(YEAR, e.birth_date, GETDATE()) / 10) * 10` |
| current salary | `s.salary WHERE s.to_date = '9999-01-01'` |
| current title | `t.title WHERE t.to_date = '9999-01-01'` |
| current department | `d.dept_name WHERE de.to_date = '9999-01-01'` |
| promotion | `t.title change WHERE DATEDIFF(DAY, e.hire_date, t.from_date) > 90` |
| active employee | `de.to_date = '9999-01-01'` |
| terminated employee | `de.to_date < '9999-01-01'` |
| manager | `emp_no IN (SELECT emp_no FROM employee.dept_manager WHERE to_date = '9999-01-01')` |

---

## Table Reference

### `employee.employees`
Master employee records. **Synonyms:** staff, workforce, personnel.

| Column | Notes |
|--------|-------|
| `emp_no` | Primary key; BIGINT. |
| `birth_date` | DATE. Never report individual ages; use decade aggregation only. |
| `first_name`, `last_name` | VARCHAR. |
| `gender` | VARCHAR. Enum: `'M'`, `'F'`. Requires minimum 10-person cell size for reporting. |
| `hire_date` | DATE. Use to calculate tenure and identify legacy workforce (< 1990-01-01). |

---

### `employee.departments`
Department master list. **Synonyms:** org, division, unit.

| Column | Notes |
|--------|-------|
| `dept_no` | Primary key; VARCHAR. Enum: `d001`–`d009`. |
| `dept_name` | VARCHAR. Enum: `'Customer Service'`, `'Development'`, `'Finance'`, `'Human Resources'`, `'Marketing'`, `'Production'`, `'Quality Management'`, `'Research'`, `'Sales'`. **Note:** `d009` (Customer Service) was split in 2005; adjust historical comparisons. |

---

### `employee.dept_emp`
Employee-to-department assignments with effective dates. **Synonyms:** department membership, assignment history.

| Column | Notes |
|--------|-------|
| `emp_no` | BIGINT; foreign key to `employee.employees`. |
| `dept_no` | VARCHAR; foreign key to `employee.departments`. |
| `from_date` | DATE; assignment start. |
| `to_date` | DATE; assignment end. `'9999-01-01'` = current. **Critical:** Employees can hold multiple department records; use `to_date = '9999-01-01'` to identify current assignment. For headcount, count each employee once using most recent department only. |

---

### `employee.dept_manager`
Department manager assignments with effective dates. **Synonyms:** management, leadership.

| Column | Notes |
|--------|-------|
| `dept_no` | VARCHAR; foreign key to `employee.departments`. |
| `emp_no` | BIGINT; foreign key to `employee.employees`. |
| `from_date` | DATE; management start. |
| `to_date` | DATE; management end. `'9999-01-01'` = current. **Critical:** Exclude these employees from non-management headcount metrics. |

---

### `employee.salaries`
Compensation history with effective date ranges. **Synonyms:** compensation, pay, wages.

| Column | Notes |
|--------|-------|
| `emp_no` | BIGINT; foreign key to `employee.employees`. |
| `salary` | BIGINT. **Critical:** Point-in-time data; always specify effective date range. Flag outliers (>3 σ from department mean) but do not exclude. Never disclose ranges with <5 employees; aggregate to broader grouping. |
| `from_date` | DATE; salary period start. |
| `to_date` | DATE; salary period end. `'9999-01-01'` = current. |

---

### `employee.titles`
Job title history with effective date ranges. **Synonyms:** position, role, job.

| Column | Notes |
|--------|-------|
| `emp_no` | BIGINT; foreign key to `employee.employees`. |
| `title` | VARCHAR. Enum: `'Assistant Engineer'`, `'Engineer'`, `'Manager'`, `'Senior Engineer'`, `'Senior Staff'`, `'Staff'`, `'Technique Leader'`. **Critical:** Title changes within 90 days of hire are corrections, not promotions. `'Senior Engineer'` valid for comparison only from 1995 onward (title inflation). |
| `from_date` | DATE; title period start. |
| `to_date` | DATE; title period end. `'9999-01-01'` = current. **Tenure risk flag:** Same title for ≥7 years with `to_date = '9999-01-01'`. |