# Business Logic Failures — Run 6 Analysis

33 of 54 right-table cases produced wrong SQL in Run 6. The failures cluster into
five distinct patterns, documented below with representative cases from the traces.

---

## Pattern 1 — Airline: joining lookup/dimension tables the gold doesn't use

**Cases:** [9], [11], [22], [43] — all 6 Airline failures share this root cause.

The agent joins to secondary lookup tables (carrier codes→names, airport IDs→names,
day-of-week numbers→descriptions) when the gold query uses raw codes directly from
the main `On_Time_On_Time_Performance_2016_1` table.

| Case | Agent joined | Gold used |
|------|-------------|-----------|
| Carrier performance | `c.Code` from carrier lookup | `UniqueCarrier` directly |
| Day of week analysis | `w.Description` from DOW lookup | `DayOfWeek` integer directly |
| Origin/dest routes | `OriginAirportID`, `DestAirportID` | `Origin`, `Dest` (3-letter codes) |

**Root cause:** The Airline guide likely lists the lookup tables and suggests joins.
The guide needs to explicitly state that the main performance table's string columns
(`UniqueCarrier`, `Origin`, `Dest`) are self-describing codes — no joins needed for
reporting by carrier or route.

**Fix:** Add a note to the Airline guide: "For carrier/route/DOW aggregations, use
`UniqueCarrier`, `Origin`, `Dest`, and `DayOfWeek` directly from the main table.
Do not join to lookup tables unless the question explicitly asks for full names."

---

## Pattern 2 — financial: imprecise loan status business rules

**Cases:** [4], [7], [26], [28], [36] — 5 of 7 financial failures.

The `financial.loan.status` column has 4 values with specific semantics:
- `A` = performing
- `B` = watch list (exclude from default rate denominator; include in portfolio)
- `C` = defaulted (finished contract, payment failed)
- `D` = defaulted (ongoing contract, client in debt)

Agent consistently reduces this to `status = 'D'` for defaults and misses the
watch-list exclusion in the denominator.

```sql
-- Gold default rate (Run 6 case [7]):
SELECT CAST(COUNT(CASE WHEN status IN ('C', 'D') THEN 1 END) AS REAL)
     / COUNT(CASE WHEN status NOT IN ('B') THEN 1 END)
FROM financial.loan

-- Agent submitted:
SELECT CAST(SUM(CASE WHEN status = 'D' THEN 1 ELSE 0 END) AS DOUBLE) / COUNT(*)
FROM financial.loan
```

Also: district join path. Gold: `district → account → loan` (via `district_id →
account.district_id → loan.account_id`). Agent often does `loan JOIN district`
directly, which misses the account intermediary.

**Fix:** The financial guide's business rules section must spell out each status
value with its exact SQL filter AND the denominator rule for rates explicitly:
- "Performing: `status = 'A'`"
- "Watch list: `status = 'B'` — include in portfolio counts, EXCLUDE from default rate denominator"
- "Defaulted: `status IN ('C', 'D')`"
- "Default rate denominator: `WHERE status != 'B'` (i.e., exclude watch-list)"
- "District→loan join: must go through account: `district d JOIN account a ON d.district_id = a.district_id JOIN loan l ON a.account_id = l.account_id`"

---

## Pattern 3 — Credit: charge filters not consistently applied

**Cases:** [19], [21], [25], [37] — 4 Credit failures.

Several business rules apply to nearly every Credit query but the agent applies
them inconsistently:

1. **Refund exclusion:** `charge_code != 'RF'` must be applied to exclude refunds.
   Case [21] omits this; case [37] uses a category join instead of `category_no` ranges.

2. **Spending type classification** uses `category_no` numeric ranges:
   - Essential: `category_no BETWEEN 1 AND 10`
   - Discretionary: `BETWEEN 11 AND 20`
   - Luxury: `> 20`
   Agent (case [37]) joins to the `category` table for descriptions instead of using
   the range logic on `category_no`.

3. **Schema confusion:** Case [19] ("Calculate the average transaction value") landed
   on `ccs` schema instead of `Credit` — the question has no Credit-specific vocabulary,
   so embedding retrieval failed. This is a retrieval problem, not a logic problem.

**Fix:** Guide business rules need:
- "ALWAYS exclude refunds: `WHERE charge_code != 'RF'`" (flag it as a universal filter)
- Explicit `category_no` range definitions for spending types rather than referring
  to the category table

---

## Pattern 4 — employee: "current" salary filter and unnecessary joins

**Cases:** [18], [31], [34], [39] — all 4 employee failures.

The `employee.salaries` table has `from_date`/`to_date` columns. Current salary rows
have `to_date = '9999-01-01'`. The agent adds unnecessary `dept_emp` joins and
sometimes misses the currency filter entirely.

```sql
-- Gold (case [31]): simple, no dept_emp
SELECT e.gender, AVG(s.salary)
FROM employee.employees e
JOIN employee.salaries s ON e.emp_no = s.emp_no
WHERE s.to_date = '9999-01-01'
GROUP BY e.gender

-- Agent added:
JOIN employee.dept_emp de ON e.emp_no = de.emp_no
```

Case [34] ("How many employees are in the legacy workforce?") — gold is a single-table
count with `WHERE hire_date < '1990-01-01'`; agent joins dept_emp and uses DISTINCT,
changing the count.

**Fix:** Add to the employee guide:
- "Current salary: `WHERE salaries.to_date = '9999-01-01'`"
- "Questions about employees alone (hire_date, gender, count) do NOT require dept_emp.
  Only join dept_emp when the question asks about departments."

---

## Pattern 5 — lahman_2014: computed field formulas

**Cases:** [3], [8], [10], [15], [17] — all 5 lahman_2014 failures.

Baseball sabermetric formulas must be derived from raw columns since they are not
stored pre-computed:

| Metric | Formula | Column source |
|--------|---------|---------------|
| Innings pitched | `IPouts / 3.0` | `pitching.IPouts` |
| ERA | `(ER * 9.0) / (IPouts / 3.0)` | `pitching.ER`, `pitching.IPouts` |
| WHIP | `(BB + H) / (IPouts / 3.0)` | `pitching.BB`, `pitching.H`, `pitching.IPouts` |
| Batting average | `CAST(H AS REAL) / AB` | `batting.H`, `batting.AB` |
| Career BA | `SUM(H) * 1.0 / SUM(AB)` aggregated across seasons | same |

Agent submissions mostly get the formula right but differ on column aliases or include
extra columns not in the gold (e.g., returns `playerID` + `nameFirst` + `nameLast`
when gold wants just `nameFirst`, `nameLast`).

**Fix:** Add a "Derived metrics" section to the lahman_2014 guide with exact formula
SQL for each common sabermetric, and note which columns the gold typically selects
for player identity (`nameFirst`, `nameLast` — not `playerID`).

---

## Pattern 6 — Output format / column mismatch (cross-cutting)

Several mismatches are not wrong logic but wrong output shape:
- Agent adds extra columns not in gold (e.g., `games` alongside `win_rate`)
- Agent uses different column aliases (`first_name` vs the bare `nameFirst`)
- Agent concatenates name columns (`nameFirst || ' ' || nameLast`) when gold selects them separately

The grader compares values not column names, so extra columns are fine — but
wrong row counts (from extra GROUP BY keys) or wrong values (from concatenation)
fail. This is partially a prompt issue: the system prompt says "extra columns are
fine" but doesn't say "don't concatenate columns the question didn't ask you to merge."

**Possible fix:** Add to the system prompt: "Select columns as-is unless the question
explicitly asks for concatenation or transformation. Don't combine `nameFirst` and
`nameLast` into a single column unless asked."

---

## Summary of recommended guide fixes

| Schema | Fix |
|--------|-----|
| Airline | Document that `UniqueCarrier`, `Origin`, `Dest`, `DayOfWeek` are self-describing; warn against lookup joins for aggregation queries |
| financial | Spell out all 4 loan status codes + denominator rule for rates; document district→account→loan join path explicitly |
| Credit | Flag `charge_code != 'RF'` as a universal filter; document `category_no` ranges for spending types |
| employee | Document `to_date = '9999-01-01'` for current salary; warn against unnecessary `dept_emp` join |
| lahman_2014 | Add derived metric formulas (ERA, WHIP, BA, career BA); note preferred output columns for player identity |
