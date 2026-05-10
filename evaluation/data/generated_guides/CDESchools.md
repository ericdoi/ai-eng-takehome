# CDESchools Schema Reference Guide

## Schema Summary
This schema contains California Department of Education data on school demographics, free/reduced-price meal eligibility (FRPM), and SAT test scores for the 2014-2015 academic year.

---

## Join Paths

**Schools to FRPM (by school identifier):**
```sql
FROM CDESchools.schools s
JOIN CDESchools.frpm f ON s.CDSCode = f.CDSCode
```

**Schools to SAT Scores (by school identifier):**
```sql
FROM CDESchools.schools s
JOIN CDESchools.satscores sat ON s.CDSCode = sat.cds
```

**FRPM to SAT Scores (by school identifier):**
```sql
FROM CDESchools.frpm f
JOIN CDESchools.satscores sat ON f.CDSCode = sat.cds
```

**All three tables:**
```sql
FROM CDESchools.schools s
JOIN CDESchools.frpm f ON s.CDSCode = f.CDSCode
JOIN CDESchools.satscores sat ON s.CDSCode = sat.cds
```

---

## Synonym Glossary

| Question Term | Schema Reference |
|---|---|
| school code | `CDSCode` (frpm, schools) or `cds` (satscores) |
| district name | `District Name` (frpm) or `District` (schools) |
| county name | `County Name` (frpm) or `County` (schools) |
| school name | `School Name` (frpm) or `School` (schools) or `sname` (satscores) |
| free/reduced meal eligibility | `Percent (%) Eligible FRPM (K-12)` (frpm) |
| free meal only | `Percent (%) Eligible Free (K-12)` (frpm) |
| SAT reading score | `AvgScrRead` (satscores) |
| SAT math score | `AvgScrMath` (satscores) |
| SAT writing score | `AvgScrWrite` (satscores) |
| SAT test takers | `NumTstTakr` (satscores) |
| grade 12 enrollment | `enroll12` (satscores) |
| charter school | `Charter` (schools) = 1 or `Charter School (Y/N)` (frpm) = 1 |
| active school | `StatusType` (schools) = 'Active' |

---

## Table Reference

### `CDESchools.frpm`
**Meaning:** Free and Reduced-Price Meal program eligibility by school for 2014-2015.

| Column | Notes |
|---|---|
| `CDSCode` | California Department Schools code; join key to schools and satscores |
| `Academic Year` | Fixed value: `2014-2015` |
| `County Code`, `District Code`, `School Code` | Component parts of CDSCode |
| `District Type` | Enum: `County Office of Education (COE)`, `Elementary School District`, `High School District`, `Unified School District`, `State Special Schools`, `Statewide Benefit Charter`, `Non-School Locations`, `State Board of Education` |
| `School Type` | Enum: `Elementary Schools (Public)`, `High Schools (Public)`, `K-12 Schools (Public)`, `Intermediate/Middle Schools (Public)`, `Junior High Schools (Public)`, `Continuation High Schools`, `Alternative Schools of Choice`, `Special Education Schools (Public)`, `County Community`, `District Community Day Schools`, `Juvenile Court Schools`, `Opportunity Schools`, `Preschool`, `State Special Schools`, `Youth Authority Facilities` |
| `Educational Option Type` | Enum: `Traditional`, `Alternative School of Choice`, `Continuation School`, `Community Day School`, `Special Education School`, `State Special School`, `County Community School`, `Home and Hospital`, `Juvenile Court School`, `Opportunity School`, `District Special Education Consortia School`, `Youth Authority School` |
| `NSLP Provision Status` | Enum: `Provision 1`, `Provision 2`, `Provision 3`, `CEP`, `Breakfast Provision 2`, `Lunch Provision 2`, `Multiple Provision Types` |
| `Charter School (Y/N)` | Binary: 0 or 1 |
| `Charter Funding Type` | Enum: `Directly funded`, `Locally funded`, `Not in CS funding model` |
| `Low Grade`, `High Grade` | Grade range served; values: `K`, `P`, `1`–`12`, `Adult`, `Post Secondary` |
| `Enrollment (K-12)` | Total K-12 enrollment |
| `Free Meal Count (K-12)`, `Percent (%) Eligible Free (K-12)` | Free meal program eligibility |
| `FRPM Count (K-12)`, `Percent (%) Eligible FRPM (K-12)` | Free and reduced-price meal eligibility (primary metric) |
| `Enrollment (Ages 5-17)`, `Free Meal Count (Ages 5-17)`, `Percent (%) Eligible Free (Ages 5-17)`, `FRPM Count (Ages 5-17)`, `Percent (%) Eligible FRPM (Ages 5-17)` | Same metrics for ages 5-17 subset |

---

### `CDESchools.satscores`
**Meaning:** SAT test results by school and district for grade 12.

| Column | Notes |
|---|---|
| `cds` | California Department Schools code; join key to frpm and schools |
| `rtype` | Enum: `S` (school-level), `D` (district-level) |
| `sname` | School name (null for district-level rows) |
| `dname` | District name |
| `cname` | County name |
| `enroll12` | Grade 12 enrollment |
| `NumTstTakr` | Number of SAT test takers |
| `AvgScrRead`, `AvgScrMath`, `AvgScrWrite` | Average SAT section scores (0–800 scale); may be `<NA>` if insufficient test takers |
| `NumGE1500`, `PctGE1500` | Count and percentage of test takers scoring ≥1500 combined |

---

### `CDESchools.schools`
**Meaning:** School directory with contact, location, and operational status.

| Column | Notes |
|---|---|
| `CDSCode` | California Department Schools code; join key to frpm and satscores |
| `StatusType` | Enum: `Active`, `Closed`, `Merged`, `Pending` |
| `County`, `District`, `School` | Geographic and organizational hierarchy |
| `Street`, `City`, `Zip`, `State` | Physical address |
| `MailStreet`, `MailCity`, `MailZip`, `MailState` | Mailing address |
| `Phone`, `Website` | Contact information |
| `OpenDate`, `ClosedDate` | Operational dates |
| `Charter` | Binary: 0 or 1 |
| `CharterNum` | Charter school authorization number |
| `FundingType` | Enum: `Directly funded`, `Locally funded`, `Not in CS funding model` |
| `DOCType` | District Organization Code type; enum: `County Office of Education (COE)`, `Elementary School District`, `High School District`, `Unified School District`, `State Special Schools`, `Statewide Benefit Charter`, `Joint Powers Authority (JPA)`, `Community College District`, `Regional Occupation Center/Program (ROC/P)`, `Administration Only`, `Non-School Locations`, `State Board of Education` |
| `SOCType` | School Organization Code type; enum: `Elementary Schools (Public)`, `High Schools (Public)`, `K-12 Schools (Public)`, `Intermediate/Middle Schools (Public)`, `Junior High Schools (Public)`, `Continuation High Schools`, `Alternative Schools of Choice`, `Special Education Schools (Public)`, `County Community`, `District Community Day Schools`, `Juvenile Court Schools`, `Opportunity Schools`, `Preschool`, `Adult Education Centers`, `ROC/ROP`, `State Special Schools`, `Youth Authority Facilities`, `Other County Or District Programs` |
| `EdOpsName` | Educational operations type; enum: `Traditional`, `Alternative School of Choice`, `Continuation School`, `Community Day School`, `Special Education School`, `State Special School`, `County Community School`, `Home and Hospital`, `Juvenile Court School`, `Opportunity School`, `ROP`, `Youth Authority School` |
| `EILName` | Educational Institution Level; enum: `Elementary`, `High School`, `Elementary-High Combination`, `Intermediate/Middle/Junior High`, `Preschool`, `Adult`, `Ungraded` |
| `GSoffered`, `GSserved` | Grade span offered and served (e.g., `K-12`, `9-12`) |
| `Virtual` | Enum: `N` (not virtual), `P` (partial), `F` (full) |
| `Magnet` | Binary: 0 or 1 |
| `Latitude`, `Longitude` | Geographic coordinates |
| `AdmFName1`, `AdmLName1`, `AdmEmail1` (and 2, 3) | Administrator contact information |
| `LastUpdate` | Date of last record update |