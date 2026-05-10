# Facebook Schema Reference Guide

## Schema Summary
This schema contains Facebook user social network data with user-to-user connections and encoded feature vectors representing user profile attributes across multiple categories.

## Join Paths

**Connect users via edges (social network):**
```sql
FROM Facebook.edges e
JOIN Facebook.feat f1 ON e.id1 = f1.id
JOIN Facebook.feat f2 ON e.id2 = f2.id
```

**Find all features for a connected user pair:**
```sql
FROM Facebook.edges e
JOIN Facebook.feat f ON e.id1 = f.id
WHERE e.id2 = <target_user_id>
```

## Table Reference

### `Facebook.edges`
User-to-user social connections in an undirected graph.

| Column | Meaning |
|--------|---------|
| `id1` | First user identifier |
| `id2` | Second user identifier (connected to id1) |

**Notes:** Represents friendship/connection relationships. No directionality specified; treat as undirected edges.

---

### `Facebook.feat`
Encoded user profile feature vectors. Each row represents one user; columns are binary indicators (0/1) for profile attributes.

| Column Group | Meaning | Count |
|--------------|---------|-------|
| `id` | User identifier (primary key) | 1 |
| `birthday1`–`birthday8` | Birthday attribute features | 8 |
| `education1`–`education99` | Education history features | 99 |
| `first_name1`–`first_name10` | First name features | 10 |
| `gender1`–`gender2` | Gender features | 2 |
| `hometown1`–`hometown11` | Hometown location features | 11 |
| `languages1`–`languages12` | Language proficiency features | 12 |
| `last_name1`–`last_name30` | Last name features | 30 |
| `locale1`–`locale5` | Locale/regional features | 5 |
| `location1`–`location16` | Current location features | 16 |
| `name1` | Name feature | 1 |
| `work1`–`work68` | Work/employment history features | 68 |

**Notes:** All feature columns are binary (0 or 1). Each numbered suffix represents a distinct encoded category within that attribute type. Features are one-hot or multi-hot encoded representations of categorical profile data. No direct mapping to human-readable values is provided in the schema.