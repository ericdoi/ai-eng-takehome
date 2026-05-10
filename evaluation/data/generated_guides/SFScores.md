# SFScores Schema Reference Guide

## Schema Summary
The SFScores schema contains San Francisco food safety inspection records, tracking businesses, their health inspections with scores, and violations cited during those inspections.

---

## Table Reference

### Table: `SFScores.businesses`
**Meaning:** Master registry of food service businesses in San Francisco.
**Synonyms:** establishments, food businesses, restaurants, vendors

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `business_id` | BIGINT | Unique identifier for each business | business number, establishment ID |
| `name` | VARCHAR | Official business name | business name, establishment name |
| `address` | VARCHAR | Street address of business location | street address, location |
| `city` | VARCHAR | City where business operates | municipality |
| `postal_code` | VARCHAR | ZIP code of business location | zip code, zip |
| `latitude` | DOUBLE | Geographic latitude coordinate | lat |
| `longitude` | DOUBLE | Geographic longitude coordinate | lon |
| `phone_number` | BIGINT | Business contact phone number | phone, telephone |
| `tax_code` | VARCHAR | Tax classification code | tax classification |
| `business_certificate` | BIGINT | Business permit/certificate number | permit number, certificate number |
| `application_date` | DATE | Date business application was submitted | application submission date |
| `owner_name` | VARCHAR | Name of business owner(s) | proprietor, operator |
| `owner_address` | VARCHAR | Street address of owner | owner street address |
| `owner_city` | VARCHAR | City where owner resides | owner municipality |
| `owner_state` | VARCHAR | State where owner resides | owner state code |
| `owner_zip` | VARCHAR | ZIP code of owner residence | owner postal code |

---

### Table: `SFScores.inspections`
**Meaning:** Health inspection records for businesses, including inspection dates, scores, and inspection types.
**Synonyms:** inspection records, health inspections, scores, audits

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `business_id` | BIGINT | Foreign key linking to business | establishment ID |
| `score` | BIGINT | Numerical health inspection score (0–100) | inspection score, health score |
| `date` | DATE | Date inspection was conducted | inspection date |
| `type` | VARCHAR | Category/classification of inspection | inspection type, inspection category |

**Enumerated Values for `type`:**
- `Administrative or Document Review`
- `Complaint`
- `Complaint Reinspection/Followup`
- `Foodborne Illness Investigation`
- `Multi-agency Investigation`
- `New Construction`
- `New Ownership`
- `Non-inspection site visit`
- `Reinspection/Followup`
- `Routine - Scheduled`
- `Routine - Unscheduled`
- `Special Event`
- `Structural Inspection`

---

### Table: `SFScores.violations`
**Meaning:** Health code violations cited during inspections, with risk severity classification.
**Synonyms:** citations, violations cited, infractions, deficiencies

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `business_id` | BIGINT | Foreign key linking to business | establishment ID |
| `date` | DATE | Date violation was cited (inspection date) | violation date, citation date |
| `violation_type_id` | VARCHAR | Code identifying the specific violation type | violation code, violation ID, citation code |
| `risk_category` | VARCHAR | Severity classification of violation | risk level, severity, risk |
| `description` | VARCHAR | Human-readable description of violation | violation description, citation text |

**Enumerated Values for `risk_category`:**
- `High Risk`
- `Moderate Risk`
- `Low Risk`

---

## Join Paths

**Businesses to Inspections:**
```sql
SFScores.businesses b
INNER JOIN SFScores.inspections i ON b.business_id = i.business_id
```

**Businesses to Violations:**
```sql
SFScores.businesses b
INNER JOIN SFScores.violations v ON b.business_id = v.business_id
```

**Inspections to Violations (via business_id and date):**
```sql
SFScores.inspections i
INNER JOIN SFScores.violations v 
  ON i.business_id = v.business_id 
  AND i.date = v.date
```

**All three tables:**
```sql
SFScores.businesses b
INNER JOIN SFScores.inspections i ON b.business_id = i.business_id
INNER JOIN SFScores.violations v 
  ON i.business_id = v.business_id 
  AND i.date = v.date
```

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| business name | `SFScores.businesses.name` |
| inspection score | `SFScores.inspections.score` |
| inspection date | `SFScores.inspections.date` |
| inspection type | `SFScores.inspections.type` |
| violation | `SFScores.violations.description` |
| violation risk | `SFScores.violations.risk_category` |
| high-risk violation | `WHERE SFScores.violations.risk_category = 'High Risk'` |
| moderate-risk violation | `WHERE SFScores.violations.risk_category = 'Moderate Risk'` |
| low-risk violation | `WHERE SFScores.violations.risk_category = 'Low Risk'` |
| routine inspection | `WHERE SFScores.inspections.type = 'Routine - Scheduled' OR SFScores.inspections.type = 'Routine - Unscheduled'` |
| complaint inspection | `WHERE SFScores.inspections.type = 'Complaint'` |
| business location | `SFScores.businesses.address, SFScores.businesses.city, SFScores.businesses.postal_code` |
| business coordinates | `SFScores.businesses.latitude, SFScores.businesses.longitude` |
| owner information | `SFScores.businesses.owner_name, SFScores.businesses.owner_address, SFScores.businesses.owner_city, SFScores.businesses.owner_state, SFScores.businesses.owner_zip` |