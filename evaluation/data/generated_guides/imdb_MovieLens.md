# IMDB MovieLens Schema Reference Guide

## 1. Schema Summary

This schema integrates IMDb movie metadata (films, actors, directors, genres) with MovieLens user ratings to enable entertainment analytics across cast, crew, film characteristics, and audience sentiment.

---

## 2. Join Paths

**Movies to actors:**
```sql
FROM imdb_MovieLens.movies m
JOIN imdb_MovieLens.movies2actors ma ON m.movieid = ma.movieid
JOIN imdb_MovieLens.actors a ON ma.actorid = a.actorid
```

**Movies to directors:**
```sql
FROM imdb_MovieLens.movies m
JOIN imdb_MovieLens.movies2directors md ON m.movieid = md.movieid
JOIN imdb_MovieLens.directors d ON md.directorid = d.directorid
```

**User ratings to movies:**
```sql
FROM imdb_MovieLens.u2base ub
JOIN imdb_MovieLens.movies m ON ub.movieid = m.movieid
JOIN imdb_MovieLens.users u ON ub.userid = u.userid
```

**Full cast + crew for a movie:**
```sql
FROM imdb_MovieLens.movies m
LEFT JOIN imdb_MovieLens.movies2actors ma ON m.movieid = ma.movieid
LEFT JOIN imdb_MovieLens.actors a ON ma.actorid = a.actorid
LEFT JOIN imdb_MovieLens.movies2directors md ON m.movieid = md.movieid
LEFT JOIN imdb_MovieLens.directors d ON md.directorid = d.directorid
```

---

## 3. Business Rules as SQL

| Rule | SQL Condition |
|------|---------------|
| Negative sentiment | `WHERE CAST(ub.rating AS INT) < 3` |
| Max rating (5-star) | `WHERE ub.rating = '5'` |
| Super-rater adjustment | Apply `0.9x` factor when `COUNT(CASE WHEN ub.rating = '5' THEN 1 END) / COUNT(*) > 0.5` per user |
| Sufficient rating signal | `WHERE (SELECT COUNT(*) FROM imdb_MovieLens.u2base WHERE movieid = m.movieid) >= 10` |
| Classic cinema | `WHERE m.year < 1970` |
| Exclude documentaries | `WHERE md.genre != 'Documentary'` |
| Exclude shorts | Flagged separately; no explicit column—use `m.runningtime` heuristic if needed |
| Actor career analysis | `HAVING COUNT(DISTINCT ma.movieid) >= 3` |
| One-time directors | `WHERE (SELECT COUNT(DISTINCT movieid) FROM imdb_MovieLens.movies2directors WHERE directorid = d.directorid) = 1` |
| Meaningful actor-director collaboration | `HAVING COUNT(DISTINCT m.movieid) >= 2` (grouped by actorid, directorid) |
| Super users | `WHERE (SELECT COUNT(*) FROM imdb_MovieLens.u2base WHERE userid = u.userid) > 1000` |
| Exclude low-engagement users | `WHERE (SELECT COUNT(*) FROM imdb_MovieLens.u2base WHERE userid = u.userid) >= 10` |
| Early adopter rating | Requires external release date; use `m.year` as proxy |

---

## 4. Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| actor quality score | `imdb_MovieLens.actors.a_quality` |
| director quality score | `imdb_MovieLens.directors.d_quality` |
| director revenue metric | `imdb_MovieLens.directors.avg_revenue` |
| cast position | `imdb_MovieLens.movies2actors.cast_num` |
| film genre | `imdb_MovieLens.movies2directors.genre` |
| user age bracket | `imdb_MovieLens.users.age` |
| user job category | `imdb_MovieLens.users.occupation` |
| film language | `imdb_MovieLens.movies.isEnglish` (T/F) |
| film origin | `imdb_MovieLens.movies.country` |
| film duration | `imdb_MovieLens.movies.runningtime` |
| user sentiment score | `imdb_MovieLens.u2base.rating` |
| actor gender | `imdb_MovieLens.actors.a_gender` |
| user gender | `imdb_MovieLens.users.u_gender` |

---

## 5. Table Reference

### `imdb_MovieLens.actors`
**Meaning:** Actor profiles with demographic and quality metrics.

| Column | Notes |
|--------|-------|
| `actorid` | Primary key |
| `a_gender` | Enum: `F`, `M` |
| `a_quality` | Quality score (0–4 range observed); higher = better |

---

### `imdb_MovieLens.directors`
**Meaning:** Director profiles with quality and revenue metrics.

| Column | Notes |
|--------|-------|
| `directorid` | Primary key |
| `d_quality` | Quality score (0–4 range observed); higher = better |
| `avg_revenue` | Revenue tier (0–4 range observed) |

---

### `imdb_MovieLens.movies`
**Meaning:** Film metadata including release year, language, origin, and runtime.

| Column | Notes |
|--------|-------|
| `movieid` | Primary key |
| `year` | Release year; values < 1970 = classic cinema |
| `isEnglish` | Enum: `T` (English), `F` (non-English) |
| `country` | Enum: `USA`, `UK`, `France`, `other` |
| `runningtime` | Duration in minutes; 0 may indicate missing data |

---

### `imdb_MovieLens.movies2actors`
**Meaning:** Junction table linking movies to cast members with billing order.

| Column | Notes |
|--------|-------|
| `movieid` | Foreign key to `imdb_MovieLens.movies` |
| `actorid` | Foreign key to `imdb_MovieLens.actors` |
| `cast_num` | Billing position (0 = lead); lower = higher billing |

---

### `imdb_MovieLens.movies2directors`
**Meaning:** Junction table linking movies to directors with genre classification.

| Column | Notes |
|--------|-------|
| `movieid` | Foreign key to `imdb_MovieLens.movies` |
| `directorid` | Foreign key to `imdb_MovieLens.directors` |
| `genre` | Enum: `Action`, `Adventure`, `Animation`, `Comedy`, `Crime`, `Documentary`, `Drama`, `Horror`, `Other`; one genre per row (movies may have multiple rows) |

---

### `imdb_MovieLens.u2base`
**Meaning:** User ratings of movies; core fact table for sentiment analysis.

| Column | Notes |
|--------|-------|
| `userid` | Foreign key to `imdb_MovieLens.users` |
| `movieid` | Foreign key to `imdb_MovieLens.movies` |
| `rating` | Enum: `1`, `2`, `3`, `4`, `5` (stored as VARCHAR); < 3 = negative sentiment |

---

### `imdb_MovieLens.users`
**Meaning:** User profiles with demographics and engagement metadata.

| Column | Notes |
|--------|-------|
| `userid` | Primary key |
| `age` | Enum: `1`, `18`, `25`, `35`, `45`, `50`, `56` (age bracket or code) |
| `u_gender` | Enum: `F`, `M` |
| `occupation` | Enum: `1`, `2`, `3`, `4`, `5` (occupation category code) |