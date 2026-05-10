# SFScores Schema Reference Guide

## Schema Summary
This schema contains San Francisco food safety inspection records, tracking businesses, their health inspections with scores, and violations cited during those inspections.

---

## Join Paths

**Businesses to inspections:**
```sql
FROM SFScores.businesses b
JOIN SFScores.inspections i ON b.business_id = i.business_id
```

**Businesses to violations:**
```sql
FROM SFScores.businesses b
JOIN SFScores.violations v ON b.business_id = v.business_id
```

**Inspections to violations (via date and business_id):**
```sql
FROM SFScores.inspections i
JOIN SFScores.violations v 
  ON i.business_id = v.business_id 
  AND i.date = v.date
```

**All three tables:**
```sql
FROM SFScores.businesses b
JOIN SFScores.inspections i ON b.business_id = i.business_id
JOIN SFScores.violations v 
  ON i.business_id = v.business_id 
  AND i.date = v.date
```

---

## Table Reference

### `SFScores.businesses`
Business establishment records with owner information.

| Column | Notes |
|--------|-------|
| `business_id` | Primary key; links to inspections and violations |
| `address`, `city`, `postal_code` | Business location |
| `latitude`, `longitude` | Coordinates for geospatial queries |
| `tax_code` | All sampled records show `H24` (food service) |
| `owner_name`, `owner_address`, `owner_city`, `owner_state`, `owner_zip` | Owner/operator details |

---

### `SFScores.inspections`
Health inspection records with scores and inspection type.

| Column | Notes |
|--------|-------|
| `business_id` | Foreign key to businesses |
| `score` | Numeric health score (0–100 range typical); NULL for non-scored inspection types |
| `date` | Inspection date; links violations to inspections |
| `type` | Inspection category (enumerated) |

**Inspection type values:**
- `Routine - Scheduled`
- `Routine - Unscheduled`
- `Complaint`
- `Complaint Reinspection/Followup`
- `Reinspection/Followup`
- `Foodborne Illness Investigation`
- `New Construction`
- `New Ownership`
- `Administrative or Document Review`
- `Non-inspection site visit`
- `Multi-agency Investigation`
- `Special Event`
- `Structural Inspection`

---

### `SFScores.violations`
Violations cited during inspections, linked by business_id and date.

| Column | Notes |
|--------|-------|
| `business_id` | Foreign key to businesses |
| `date` | Inspection date; matches `SFScores.inspections.date` to link violations to specific inspections |
| `violation_type_id` | Violation code (e.g., `103129`, `103144`) |
| `risk_category` | Severity level (enumerated) |

**Risk category values:**
- `High Risk`
- `Moderate Risk`
- `Low Risk`

---

## Synonym Glossary

| Common Term | Schema Reference |
|-------------|------------------|
| health score | `SFScores.inspections.score` |
| inspection date | `SFScores.inspections.date` |
| violation date | `SFScores.violations.date` |
| inspection type | `SFScores.inspections.type` |
| violation severity | `SFScores.violations.risk_category` |
| restaurant location | `SFScores.businesses.address`, `city`, `postal_code` |
| operator/owner | `SFScores.businesses.owner_name` |