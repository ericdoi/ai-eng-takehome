# Facebook Schema Reference Guide

## Schema Summary
This schema contains Facebook user social network data with a graph of user connections and a feature matrix encoding user profile attributes across multiple categories.

---

## Table Reference

### Table: `Facebook.edges`
**Meaning:** User connection graph; represents friendships or follows between users.
**Synonyms:** connections, friendships, links, relationships, graph edges

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id1` | BIGINT | First user identifier in connection | user_id_1, source_user, from_user |
| `id2` | BIGINT | Second user identifier in connection | user_id_2, target_user, to_user |

**Notable values:** User IDs are large integers (e.g., 567, 3454, 3487, 3723, 3861, 3961)

---

### Table: `Facebook.feat`
**Meaning:** User feature matrix; encodes user profile attributes as binary or categorical indicators across 262 feature dimensions.
**Synonyms:** features, user_features, profile_features, attributes

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | User identifier | user_id |
| `birthday1`–`birthday8` | BIGINT | Birthday-related feature indicators (8 features) | birthday_features |
| `education1`–`education99` | BIGINT | Education-related feature indicators (99 features) | education_features, school_features |
| `first_name1`–`first_name10` | BIGINT | First name-related feature indicators (10 features) | first_name_features |
| `gender1`–`gender2` | BIGINT | Gender-related feature indicators (2 features) | gender_features |
| `hometown1`–`hometown11` | BIGINT | Hometown-related feature indicators (11 features) | hometown_features, origin_features |
| `languages1`–`languages12` | BIGINT | Language-related feature indicators (12 features) | language_features, spoken_languages |
| `last_name1`–`last_name30` | BIGINT | Last name-related feature indicators (30 features) | last_name_features, surname_features |
| `locale1`–`locale5` | BIGINT | Locale-related feature indicators (5 features) | locale_features, region_features |
| `location1`–`location16` | BIGINT | Location-related feature indicators (16 features) | location_features, current_location |
| `name1` | BIGINT | Name-related feature indicator (1 feature) | name_feature |
| `work1`–`work68` | BIGINT | Work/employment-related feature indicators (68 features) | work_features, job_features, employment_features |

**Notable values:** All feature columns contain binary indicators (0 or 1), where 1 indicates presence/match of that feature category for the user.

---

## Join Paths

**Connect users to their features:**
```sql
Facebook.edges e
JOIN Facebook.feat f1 ON e.id1 = f1.id
JOIN Facebook.feat f2 ON e.id2 = f2.id
```

**Find direct connections for a user:**
```sql
Facebook.edges
WHERE id1 = <user_id> OR id2 = <user_id>
```

**Find mutual connections between two users:**
```sql
Facebook.edges e1
JOIN Facebook.edges e2 ON (e1.id2 = e2.id1 OR e1.id2 = e2.id2)
WHERE e1.id1 = <user_id_1> AND e2.id1 = <user_id_2>
```

---

## Business Rules as SQL

No explicit business rules provided in schema documentation. Feature columns are binary indicators where:
- **Rule: User has feature X** → `WHERE feat.feature_column = 1`
- **Rule: User lacks feature X** → `WHERE feat.feature_column = 0`
- **Rule: Two users are connected** → `WHERE (edges.id1 = user_a AND edges.id2 = user_b) OR (edges.id1 = user_b AND edges.id2 = user_a)`

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| friend, connection, link | `Facebook.edges` row |
| user profile, user attributes | `Facebook.feat` row |
| connected users, friends | `edges.id1`, `edges.id2` |
| user identifier | `feat.id`, `edges.id1`, `edges.id2` |
| education background | `feat.education1` through `feat.education99` |
| work history, employment | `feat.work1` through `feat.work68` |
| spoken languages | `feat.languages1` through `feat.languages12` |
| current location | `feat.location1` through `feat.location16` |
| hometown, origin | `feat.hometown1` through `feat.hometown11` |
| name information | `feat.first_name1`–`feat.first_name10`, `feat.last_name1`–`feat.last_name30`, `feat.name1` |
| gender | `feat.gender1`, `feat.gender2` |
| birthday | `feat.birthday1` through `feat.birthday8` |
| locale, region | `feat.locale1` through `feat.locale5` |
| has feature | `= 1` |
| lacks feature | `= 0` |
| network neighbors | `edges` joined on `id1` or `id2` |