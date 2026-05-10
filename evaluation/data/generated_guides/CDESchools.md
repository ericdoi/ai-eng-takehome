# CDESchools Schema Reference Guide

## Schema Summary
The CDESchools schema contains California Department of Education data on school enrollment, free/reduced-price meal eligibility (FRPM), SAT test scores, and school administrative information for the 2014-2015 academic year.

---

## Table Reference

### Table: `CDESchools.frpm`
**Meaning:** Free and Reduced-Price Meal (FRPM) program eligibility and enrollment data by school.
**Synonyms:** meal eligibility, lunch program data, poverty indicators

| Column Name | Type | Meaning | Synonyms |
|---|---|---|---|
| `CDSCode` | VARCHAR | California Department Schools unique identifier | school code, CDS |
| `Academic Year` | VARCHAR | School year (values: `2014-2015`) | year, school year |
| `County Code` | VARCHAR | County numeric code | county ID |
| `District Code` | BIGINT | School district numeric code | district ID |
| `School Code` | VARCHAR | School numeric code within district | school ID |
| `County Name` | VARCHAR | County name | county |
| `District Name` | VARCHAR | School district name | district |
| `School Name` | VARCHAR | School name | school |
| `District Type` | VARCHAR | Type of district organization | district category |
| `School Type` | VARCHAR | Type of school | school category |
| `Educational Option Type` | VARCHAR | Educational program type | program type, option |
| `NSLP Provision Status` | VARCHAR | National School Lunch Program provision level | lunch provision, meal provision |
| `Charter School (Y/N)` | BIGINT | 1 if charter school, 0 otherwise | is charter |
| `Charter School Number` | VARCHAR | Charter school identifier | charter ID |
| `Charter Funding Type` | VARCHAR | How charter is funded | funding model |
| `IRC` | BIGINT | Instructional Resource Code | resource code |
| `Low Grade` | VARCHAR | Lowest grade served (values: `K`, `1`–`12`, `Adult`, `P`, `Post Secondary`) | minimum grade |
| `High Grade` | VARCHAR | Highest grade served (values: `K`, `1`–`13`, `Adult`, `P`, `Post Secondary`) | maximum grade |
| `Enrollment (K-12)` | DOUBLE | Total K-12 enrollment | K-12 students, total enrollment |
| `Free Meal Count (K-12)` | DOUBLE | Students eligible for free meals (K-12) | free meal students |
| `Percent (%) Eligible Free (K-12)` | DOUBLE | Percentage eligible for free meals (K-12) | free meal percentage |
| `FRPM Count (K-12)` | DOUBLE | Students eligible for free or reduced meals (K-12) | FRPM students, eligible count |
| `Percent (%) Eligible FRPM (K-12)` | DOUBLE | Percentage eligible for FRPM (K-12) | FRPM percentage |
| `Enrollment (Ages 5-17)` | DOUBLE | Enrollment ages 5-17 | age 5-17 enrollment |
| `Free Meal Count (Ages 5-17)` | DOUBLE | Free meal eligible ages 5-17 | free meal ages 5-17 |
| `Percent (%) Eligible Free (Ages 5-17)` | DOUBLE | Free meal percentage ages 5-17 | free meal % ages 5-17 |
| `FRPM Count (Ages 5-17)` | DOUBLE | FRPM eligible ages 5-17 | FRPM ages 5-17 |
| `Percent (%) Eligible FRPM (Ages 5-17)` | DOUBLE | FRPM percentage ages 5-17 | FRPM % ages 5-17 |
| `2013-14 CALPADS Fall 1 Certification Status` | BIGINT | Prior year certification status | certification status |

---

### Table: `CDESchools.satscores`
**Meaning:** SAT test score results by school and district.
**Synonyms:** test scores, SAT results, academic performance

| Column Name | Type | Meaning | Synonyms |
|---|---|---|---|
| `cds` | VARCHAR | California Department Schools unique identifier | school code, CDS code |
| `rtype` | VARCHAR | Record type: `D` (district aggregate) or `S` (school) | record type, level |
| `sname` | VARCHAR | School name | school |
| `dname` | VARCHAR | District name | district |
| `cname` | VARCHAR | County name | county |
| `enroll12` | BIGINT | Grade 12 enrollment | senior enrollment, 12th grade |
| `NumTstTakr` | BIGINT | Number of SAT test takers | test takers, participants |
| `AvgScrRead` | BIGINT | Average SAT reading score | reading score, verbal score |
| `AvgScrMath` | BIGINT | Average SAT math score | math score |
| `AvgScrWrite` | BIGINT | Average SAT writing score | writing score |
| `NumGE1500` | BIGINT | Number of students scoring ≥1500 | high scorers, 1500+ count |
| `PctGE1500` | DOUBLE | Percentage of students scoring ≥1500 | high score percentage, 1500+ % |

---

### Table: `CDESchools.schools`
**Meaning:** School administrative information, contact details, location, and operational status.
**Synonyms:** school directory, school master file, school information

| Column Name | Type | Meaning | Synonyms |
|---|---|---|---|
| `CDSCode` | VARCHAR | California Department Schools unique identifier | school code, CDS |
| `NCESDist` | VARCHAR | National Center for Education Statistics district code | NCES district |
| `NCESSchool` | VARCHAR | National Center for Education Statistics school code | NCES school |
| `StatusType` | VARCHAR | School status (values: `Active`, `Closed`, `Merged`, `Pending`) | status, operational status |
| `County` | VARCHAR | County name | county |
| `District` | VARCHAR | School district name | district |
| `School` | VARCHAR | School name | school |
| `Street` | VARCHAR | School street address | address, street |
| `StreetAbr` | VARCHAR | Abbreviated street address | street abbreviation |
| `City` | VARCHAR | School city | city |
| `Zip` | VARCHAR | School ZIP code | postal code, ZIP |
| `State` | VARCHAR | State (values: `CA`) | state |
| `MailStreet` | VARCHAR | Mailing street address | mail address, mailing street |
| `MailStrAbr` | VARCHAR | Abbreviated mailing street | mail street abbreviation |
| `MailCity` | VARCHAR | Mailing city | mail city |
| `MailZip` | VARCHAR | Mailing ZIP code | mail ZIP, mailing postal code |
| `MailState` | VARCHAR | Mailing state (values: `CA`) | mail state |
| `Phone` | VARCHAR | School phone number | telephone, contact number |
| `Ext` | VARCHAR | Phone extension | extension |
| `Website` | VARCHAR | School website URL | web address, URL |
| `OpenDate` | DATE | School opening date | opened, start date |
| `ClosedDate` | DATE | School closing date | closed, end date |
| `Charter` | BIGINT | 1 if charter school, 0 otherwise | is charter, charter flag |
| `CharterNum` | VARCHAR | Charter school number | charter ID |
| `FundingType` | VARCHAR | Charter funding model (values: `Directly funded`, `Locally funded`, `Not in CS funding model`) | funding model |
| `DOC` | VARCHAR | District Organization Code | DOC, district org code |
| `DOCType` | VARCHAR | District organization type | district type, DOC type |
| `SOC` | VARCHAR | School Organization Code | SOC, school org code |
| `SOCType` | VARCHAR | School organization type | school type, SOC type |
| `EdOpsCode` | VARCHAR | Educational operations code (values: `ALTSOC`, `COMM`, `COMMDAY`, `CON`, `HOMHOS`, `JUV`, `OPP`, `ROP`, `SPEC`, `SPECON`, `SSS`, `TRAD`, `YTH`) | ops code, program code |
| `EdOpsName` | VARCHAR | Educational operations name | program name, operations name |
| `EILCode` | VARCHAR | Educational Institution Level code (values: `A`, `ELEM`, `ELEMHIGH`, `HS`, `INTMIDJR`, `PS`, `UG`) | level code, EIL |
| `EILName` | VARCHAR | Educational Institution Level name (values: `Adult`, `Elementary`, `Elementary-High Combination`, `High School`, `Intermediate/Middle/Junior High`, `Preschool`, `Ungraded`) | level name, institution level |
| `GSoffered` | VARCHAR | Grades offered (range string, e.g., `K-12`) | grades offered, grade span |
| `GSserved` | VARCHAR | Grades served (range string, e.g., `K-12`) | grades served |
| `Virtual` | VARCHAR | Virtual school indicator (values: `F`, `N`, `P`) | virtual flag |
| `Magnet` | BIGINT | 1 if magnet school, 0 otherwise | is magnet, magnet flag |
| `Latitude` | DOUBLE | School latitude coordinate | lat, latitude |
| `Longitude` | DOUBLE | School longitude coordinate | lon, longitude |
| `AdmFName1` | VARCHAR | First administrator first name | admin 1 first name |
| `AdmLName1` | VARCHAR | First administrator last name | admin 1 last name |
| `AdmEmail1` | VARCHAR | First administrator email | admin 1 email |
| `AdmFName2` | VARCHAR | Second administrator first name | admin 2 first name |
| `AdmLName2` | VARCHAR | Second administrator last name | admin 2 last name |
| `AdmEmail2` | VARCHAR | Second administrator email | admin 2 email |
| `AdmFName3` | VARCHAR | Third administrator first name | admin 3 first name |
| `AdmLName3` | VARCHAR | Third administrator last name | admin 3 last name |
| `AdmEmail3` | VARCHAR | Third administrator email | admin 3 email |
| `LastUpdate` | DATE | Last record update date | updated, last modified |

---

## Join Paths

**FRPM to Schools:**
```sql
CDESchools.frpm f
JOIN CDESchools.schools s ON f.CDSCode = s.CDSCode
```

**SAT Scores to Schools:**
```sql
CDESchools.satscores st
JOIN CDESchools.schools s ON st.cds = s.CDSCode
```

**SAT Scores to FRPM:**
```sql
CDESchools.satscores st
JOIN CDESchools.frpm f ON st.cds = f.CDSCode
```

**All three tables:**
```sql
CDESchools.frpm f
JOIN CDESchools.schools s ON f.CDSCode = s.CDSCode
JOIN CDESchools.satscores st ON f.CDSCode = st.cds
```

---

## Business Rules as SQL

| Rule | SQL Implementation |
|---|---|
| High FRPM eligibility | `WHERE f.[Percent (%) Eligible FRPM (K-12)] > 50` |
| Active schools only | `WHERE s.StatusType = 'Active'` |
| Charter schools | `WHERE s.Charter = 1` |
| Traditional schools | `WHERE s.EdOpsCode = 'TRAD'` |
| High school level | `WHERE s.EILCode = 'HS'` |
| Elementary school level | `WHERE s.EILCode = 'ELEM'` |
| Combined elementary-high | `WHERE s.EILCode = 'ELEMHIGH'` |
| High SAT math performance | `WHERE st.AvgScrMath >= 550` |
| High SAT reading performance | `WHERE st.AvgScrRead >= 550` |
| Strong SAT participation | `WHERE st.NumTstTakr > 0 AND (st.NumTstTakr / st.enroll12) > 0.5` |
| High percentage scoring 1500+ | `WHERE st.PctGE1500 >= 50` |
| Closed schools | `WHERE s.StatusType = 'Closed'` |
| Magnet schools | `WHERE s.Magnet = 1` |
| Virtual schools | `WHERE s.Virtual IN ('P', 'F')` |
| Directly funded charters | `WHERE s.Charter = 1 AND s.FundingType = 'Directly funded'` |
| Locally funded charters | `WHERE s.Charter = 1 AND s.FundingType = 'Locally funded'` |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|---|---|
| school identifier | `CDSCode` (frpm, schools) or `cds` (satscores) |
| school name | `School Name` (frpm) or `School` (schools) or `sname` (satscores) |
| district name | `District Name` (frpm) or `District` (schools) or `dname` (satscores) |
| county name | `County Name` (frpm) or `County` (schools) or `cname` (satscores) |
| poverty rate | `Percent (%) Eligible FRPM (K-12)` (frpm) |
| free meal rate | `Percent (%) Eligible Free (K-12)` (frpm) |
| low-income students | `FRPM Count (K-12)` (frpm) |
| total students | `Enrollment (K-12)` (frpm) or `enroll12` (satscores) |
| test takers | `NumTstTakr` (satscores) |
| reading score | `AvgScrRead` (satscores) |
| math score | `AvgScrMath` (satscores) |
| writing score | `AvgScrWrite` (satscores) |
| high scorers | `NumGE1500` (satscores) |
| high score percentage | `PctGE1500` (satscores) |
| school type | `School Type` (frpm) or `SOCType` (schools) |
| program type | `Educational Option Type` (frpm) or `EdOpsName` (schools) |
| grade range | `Low Grade` / `High Grade` (frpm) or `GSoffered` / `GSserved` (schools) |
| school status | `StatusType` (schools) |
| charter school | `Charter School (Y/N)` (frpm) or `Charter` (schools) |
| school address | `Street` (schools) |
| school city | `City` (schools) |
| school phone | `Phone` (schools) |
| school website | `Website` (schools) |
| administrator name | `AdmFName1`, `AdmLName1`, etc. (schools) |
| administrator email | `AdmEmail1`, `AdmEmail2`, `AdmEmail3` (schools) |
| school location | `Latitude`, `Longitude` (schools) |
| open date | `OpenDate` (schools) |
| closed date | `ClosedDate` (schools) |
| magnet school | `Magnet` (schools) |
| virtual school | `Virtual` (schools) |