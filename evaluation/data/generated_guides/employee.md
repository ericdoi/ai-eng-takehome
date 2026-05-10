# SQL Reference Guide: Employee Schema

## 1. Schema Summary

The `employee` schema contains human resources data tracking employees, their department assignments, management hierarchies, compensation history, and job titles over time.

---

## 2. Table Reference

### Table: `employee.departments`
**Meaning:** Master list of organizational departments.  
**Synonyms:** org units, divisions

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `dept_no` | VARCHAR | Department identifier (primary key) | dept_id, department_code |
| `dept_name` | VARCHAR | Department name | name, department_name |

**Enumerated Values:**
- `d001` = Marketing
- `d002` = Finance
- `d003` = Human Resources
- `d004` = Production
- `d005` = Development
- `d006` = Quality Management
- `d007` = Research
- `d008` = Sales
- `d009` = Customer Service

---

### Table: `employee.employees`
**Meaning:** Core employee master data with demographics and hire information.  
**Synonyms:** staff, personnel, workers

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `emp_no` | BIGINT | Employee identifier (primary key) | employee_id, emp_id |
| `birth_date` | DATE | Date of birth | dob, date_of_birth |
| `first_name` | VARCHAR | Given name | fname, given_name |
| `last_name` | VARCHAR | Family name | lname, surname |
| `gender` | VARCHAR | Gender classification | sex |
| `hire_date` | DATE | Employment start date | start_date, employment_date |

**Enumerated Values:**
- `M` = Male
- `F` = Female

---

### Table: `employee.dept_emp`
**Meaning:** Historical record of employee department assignments with effective date ranges.  
**Synonyms:** department assignments, employee departments, org assignments

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `emp_no` | BIGINT | Employee identifier (foreign key to `employees`) | employee_id |
| `dept_no` | VARCHAR | Department identifier (foreign key to `departments`) | department_id |
| `from_date` | DATE | Assignment start date | start_date, effective_from |
| `to_date` | DATE | Assignment end date | end_date, effective_to |

**Special Values:**
- `to_date = '9999-01-01'` indicates current/active assignment

---

### Table: `employee.dept_manager`
**Meaning:** Historical record of department manager assignments with effective date ranges.  
**Synonyms:** management assignments, manager history

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `dept_no` | VARCHAR | Department identifier (foreign key to `departments`) | department_id |
| `emp_no` | BIGINT | Employee identifier (foreign key to `employees`) | employee_id, manager_id |
| `from_date` | DATE | Management assignment start date | start_date, effective_from |
| `to_date` | DATE | Management assignment end date | end_date, effective_to |

**Special Values:**
- `to_date = '9999-01-01'` indicates current/active management role

---

### Table: `employee.salaries`
**Meaning:** Historical compensation records with effective date ranges.  
**Synonyms:** compensation, pay history, wage records

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `emp_no` | BIGINT | Employee identifier (foreign key to `employees`) | employee_id |
| `salary` | BIGINT | Compensation amount (currency units) | compensation, pay, wage |
| `from_date` | DATE | Salary effective start date | start_date, effective_from |
| `to_date` | DATE | Salary effective end date | end_date, effective_to |

**Special Values:**
- `to_date = '9999-01-01'` indicates current/active salary

---

### Table: `employee.titles`
**Meaning:** Historical record of employee job titles with effective date ranges.  
**Synonyms:** job titles, position history, role history

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `emp_no` | BIGINT | Employee identifier (foreign key to `employees`) | employee_id |
| `title` | VARCHAR | Job title or position name | job_title, position, role |
| `from_date` | DATE | Title effective start date | start_date, effective_from |
| `to_date` | DATE | Title effective end date | end_date, effective_to |

**Enumerated Values:**
- `Assistant Engineer`
- `Engineer`
- `Manager`
- `Senior Engineer`
- `Senior Staff`
- `Staff`
- `Technique Leader`

**Special Values:**
- `to_date = '9999-01-01'` indicates current/active title

---

## 3. Join Paths

| Join Type | Condition |
|-----------|-----------|
| `employees` → `dept_emp` | `employees.emp_no = dept_emp.emp_no` |
| `employees` → `dept_manager` | `employees.emp_no = dept_manager.emp_no` |
| `employees` → `salaries` | `employees.emp_no = salaries.emp_no` |
| `employees` → `titles` | `employees.emp_no = titles.emp_no` |
| `dept_emp` → `departments` | `dept_emp.dept_no = departments.dept_no` |
| `dept_manager` → `departments` | `dept_manager.dept_no = departments.dept_no` |

---

## 4. Business Rules as SQL

### Tenure Calculations

**Rule: Legacy workforce (hired before 1990-01-01)**
```sql
WHERE employees.hire_date < '1990-01-01'
```

**Rule: Calculate tenure in days**
```sql
DATEDIFF(day, employees.hire_date, CURRENT_DATE) AS tenure_days
```

**Rule: Aggregate age statistics by decade (not individual ages)**
```sql
FLOOR(DATEDIFF(year, employees.birth_date, CURRENT_DATE) / 10) * 10 AS age_decade
-- Do NOT select individual birth_date or calculate individual age
```

---

### Department Rules

**Rule: Customer Service department split in 2005**
```sql
-- For historical comparisons before 2005-01-01, exclude or flag:
WHERE dept_emp.to_date >= '2005-01-01' OR dept_emp.dept_no != 'd009'
```

**Rule: Count each employee only once using most recent department**
```sql
-- Use window function to identify most recent assignment:
WHERE dept_emp.to_date = (
  SELECT MAX(de2.to_date) 
  FROM employee.dept_emp de2 
  WHERE de2.emp_no = dept_emp.emp_no
)
```

**Rule: Exclude department managers from non-management headcount**
```sql
WHERE dept_emp.emp_no NOT IN (
  SELECT DISTINCT emp_no 
  FROM employee.dept_manager 
  WHERE dept_manager.to_date = '9999-01-01'
)
```

---

### Salary Analytics

**Rule: Report salary with effective date range**
```sql
-- Always include in output:
salaries.from_date, salaries.to_date
-- Specify query date context in documentation
```

**Rule: Flag outlier salaries (>3 standard deviations from department mean)**
```sql
-- Calculate per department:
WHERE ABS(salaries.salary - dept_mean) > 3 * dept_stddev
-- Flag but do not exclude from results
```

**Rule: Suppress salary ranges with fewer than 5 employees**
```sql
HAVING COUNT(DISTINCT salaries.emp_no) >= 5
```

---

### Title Progression

**Rule: Title changes within 90 days of hire are corrections (exclude from promotion count)**
```sql
WHERE DATEDIFF(day, employees.hire_date, titles.from_date) > 90
```

**Rule: Senior Engineer comparisons only after 1995**
```sql
WHERE titles.title = 'Senior Engineer' AND titles.from_date >= '1995-01-01'
```

**Rule: Flag tenure risk (same title >7 years)**
```sql
WHERE DATEDIFF(day, titles.from_date, titles.to_date) > 2555
-- 2555 days ≈ 7 years
-- AND titles.to_date = '9999-01-01' (still in role)
```

---

### Gender Reporting

**Rule: Minimum cell size of 10 for gender-based analytics**
```sql
GROUP BY employees.gender
HAVING COUNT(*) >= 10
```

**Rule: Include gender difference column**
```sql
-- Calculate metric for each gender, then:
MAX(CASE WHEN employees.gender = 'M' THEN metric_value END) -
MAX(CASE WHEN employees.gender = 'F' THEN metric_value END) AS gender_difference
```

**Rule: Pay equity analysis must control for department, title, and tenure**
```sql
-- Include in GROUP BY and WHERE:
GROUP BY 
  employees.gender,
  dept_emp.dept_no,
  titles.title,
  FLOOR(DATEDIFF(year, employees.hire_date, CURRENT_DATE) / 5) * 5 AS tenure_bucket
```

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| employee count, headcount | `COUNT(DISTINCT employees.emp_no)` |
| current department | `dept_emp WHERE dept_emp.to_date = '9999-01-01'` |
| current salary | `salaries WHERE salaries.to_date = '9999-01-01'` |
| current title | `titles WHERE titles.to_date = '9999-01-01'` |
| current manager | `dept_manager WHERE dept_manager.to_date = '9999-01-01'` |
| tenure, years of service | `DATEDIFF(year, employees.hire_date, CURRENT_DATE)` |
| legacy employee | `employees WHERE hire_date < '1990-01-01'` |
| promotion | `titles WHERE DATEDIFF(day, employees.hire_date, titles.from_date) > 90` |
| department transfer | `dept_emp WHERE dept_emp.to_date < '9999-01-01'` |
| pay raise | `salaries WHERE salaries.salary > previous_salary_record` |
| age bracket | `FLOOR(DATEDIFF(year, birth_date, CURRENT_DATE) / 10) * 10` |
| gender gap | `metric_M - metric_F` (with `COUNT >= 10` per gender) |
| management headcount | `COUNT(DISTINCT dept_manager.emp_no)` |
| non-management headcount | `COUNT(DISTINCT dept_emp.emp_no) excluding dept_manager.emp_no` |