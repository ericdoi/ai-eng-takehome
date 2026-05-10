# SQL Reference Guide: imdb_MovieLens Schema

## 1. Schema Summary

The `imdb_MovieLens` schema contains integrated IMDB and MovieLens data: movies with metadata (year, language, country, runtime), actors and directors with quality metrics, cast/crew assignments, user ratings, and user demographics.

---

## 2. Table Reference

### Table: `imdb_MovieLens.actors`
**Meaning:** Actor records with demographic and quality information.
**Synonyms:** cast members, performers, talent

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `actorid` | BIGINT | Unique actor identifier | actor_id, performer_id |
| `a_gender` | VARCHAR | Actor gender | gender, sex |
| `a_quality` | BIGINT | Quality/rating metric for actor | quality_score, talent_rating |

**Enumerated values:** `a_gender` = `'F'`, `'M'`

---

### Table: `imdb_MovieLens.directors`
**Meaning:** Director records with quality and revenue metrics.
**Synonyms:** filmmakers, helmer records

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `directorid` | BIGINT | Unique director identifier | director_id |
| `d_quality` | BIGINT | Quality/rating metric for director | quality_score, directorial_rating |
| `avg_revenue` | BIGINT | Average revenue metric | revenue_score, box_office_metric |

---

### Table: `imdb_MovieLens.movies`
**Meaning:** Movie records with release metadata and technical specifications.
**Synonyms:** films, titles, productions

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `movieid` | BIGINT | Unique movie identifier | movie_id, title_id |
| `year` | BIGINT | Release year | release_year, production_year |
| `isEnglish` | VARCHAR | Language flag (English or not) | language_flag, english_language |
| `country` | VARCHAR | Production country | origin_country, production_country |
| `runningtime` | BIGINT | Duration in minutes | duration, length, runtime_minutes |

**Enumerated values:** `isEnglish` = `'T'`, `'F'` | `country` = `'USA'`, `'UK'`, `'France'`, `'other'`

---

### Table: `imdb_MovieLens.movies2actors`
**Meaning:** Junction table mapping actors to movies with cast position.
**Synonyms:** cast assignments, actor-movie relationships

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `movieid` | BIGINT | Movie identifier (FK to movies) | movie_id |
| `actorid` | BIGINT | Actor identifier (FK to actors) | actor_id |
| `cast_num` | BIGINT | Cast position/billing order | cast_position, billing_order |

---

### Table: `imdb_MovieLens.movies2directors`
**Meaning:** Junction table mapping directors to movies with genre classification.
**Synonyms:** director assignments, director-movie relationships

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `movieid` | BIGINT | Movie identifier (FK to movies) | movie_id |
| `directorid` | BIGINT | Director identifier (FK to directors) | director_id |
| `genre` | VARCHAR | Film genre | film_genre, category |

**Enumerated values:** `genre` = `'Action'`, `'Adventure'`, `'Animation'`, `'Comedy'`, `'Crime'`, `'Documentary'`, `'Drama'`, `'Horror'`, `'Other'`

---

### Table: `imdb_MovieLens.u2base`
**Meaning:** User ratings of movies (user-movie-rating relationships).
**Synonyms:** ratings, user reviews, user-movie interactions

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `userid` | BIGINT | User identifier (FK to users) | user_id |
| `movieid` | BIGINT | Movie identifier (FK to movies) | movie_id |
| `rating` | VARCHAR | User's numeric rating (1-5 scale) | user_rating, score |

**Enumerated values:** `rating` = `'1'`, `'2'`, `'3'`, `'4'`, `'5'`

---

### Table: `imdb_MovieLens.users`
**Meaning:** User demographic and profile information.
**Synonyms:** user profiles, audience members, raters

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `userid` | BIGINT | Unique user identifier | user_id |
| `age` | VARCHAR | Age bracket/category | age_group, age_bracket |
| `u_gender` | VARCHAR | User gender | gender, sex |
| `occupation` | VARCHAR | Occupation code/category | job_code, profession_code |

**Enumerated values:** `age` = `'1'`, `'18'`, `'25'`, `'35'`, `'45'`, `'50'`, `'56'` | `u_gender` = `'F'`, `'M'` | `occupation` = `'1'`, `'2'`, `'3'`, `'4'`, `'5'`

---

## 3. Join Paths

| Relationship | SQL JOIN Condition |
|--------------|-------------------|
| Movies to Actors | `INNER JOIN imdb_MovieLens.movies2actors m2a ON imdb_MovieLens.movies.movieid = m2a.movieid INNER JOIN imdb_MovieLens.actors a ON m2a.actorid = a.actorid` |
| Movies to Directors | `INNER JOIN imdb_MovieLens.movies2directors m2d ON imdb_MovieLens.movies.movieid = m2d.movieid INNER JOIN imdb_MovieLens.directors d ON m2d.directorid = d.directorid` |
| Movies to Ratings | `INNER JOIN imdb_MovieLens.u2base ub ON imdb_MovieLens.movies.movieid = ub.movieid` |
| Ratings to Users | `INNER JOIN imdb_MovieLens.users u ON imdb_MovieLens.u2base.userid = u.userid` |
| Movies to Ratings to Users | `INNER JOIN imdb_MovieLens.u2base ub ON imdb_MovieLens.movies.movieid = ub.movieid INNER JOIN imdb_MovieLens.users u ON ub.userid = u.userid` |

---

## 4. Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| Negative sentiment (low ratings) | `WHERE CAST(ub.rating AS NUMERIC) < 3.0` |
| Maximum rating (5-star) | `WHERE ub.rating = '5'` |
| Super-rater adjustment (>50% 5-star ratings) | `HAVING CAST(SUM(CASE WHEN ub.rating = '5' THEN 1 ELSE 0 END) AS NUMERIC) / COUNT(*) > 0.5` |
| Sufficient rating signal (≥10 ratings) | `HAVING COUNT(ub.movieid) >= 10` |
| Insufficient rating signal (<10 ratings) | `HAVING COUNT(ub.movieid) < 10` |
| Classic cinema (pre-1970) | `WHERE imdb_MovieLens.movies.year < 1970` |
| Documentary genre | `WHERE imdb_MovieLens.movies2directors.genre = 'Documentary'` |
| Actor career analysis threshold (≥3 credits) | `HAVING COUNT(m2a.movieid) >= 3` |
| One-time director (exactly 1 film) | `HAVING COUNT(m2d.movieid) = 1` |
| Meaningful actor-director collaboration (≥2 films) | `HAVING COUNT(DISTINCT m2d.movieid) >= 2` |
| Super user (>1000 ratings) | `HAVING COUNT(ub.movieid) > 1000` |
| Insufficient user history (<10 ratings) | `HAVING COUNT(ub.movieid) < 10` |
| Horror genre (distinct) | `WHERE imdb_MovieLens.movies2directors.genre = 'Horror'` |
| Comedy genre (distinct) | `WHERE imdb_MovieLens.movies2directors.genre = 'Comedy'` |
| Drama genre (overrepresented) | `WHERE imdb_MovieLens.movies2directors.genre = 'Drama'` |

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| actor | `imdb_MovieLens.actors.actorid` |
| director | `imdb_MovieLens.directors.directorid` |
| movie / film / title | `imdb_MovieLens.movies.movieid` |
| cast member | `imdb_MovieLens.movies2actors` + `imdb_MovieLens.actors` |
| crew / filmmaker | `imdb_MovieLens.movies2directors` + `imdb_MovieLens.directors` |
| user / rater / audience member | `imdb_MovieLens.users.userid` |
| rating / score / review | `imdb_MovieLens.u2base.rating` |
| gender | `imdb_MovieLens.actors.a_gender`, `imdb_MovieLens.users.u_gender` |
| quality / talent / skill | `imdb_MovieLens.actors.a_quality`, `imdb_MovieLens.directors.d_quality` |
| revenue / box office | `imdb_MovieLens.directors.avg_revenue` |
| release year | `imdb_MovieLens.movies.year` |
| language | `imdb_MovieLens.movies.isEnglish` |
| origin / production country | `imdb_MovieLens.movies.country` |
| duration / length | `imdb_MovieLens.movies.runningtime` |
| genre / category | `imdb_MovieLens.movies2directors.genre` |
| age group / age bracket | `imdb_MovieLens.users.age` |
| job / profession | `imdb_MovieLens.users.occupation` |
| cast position / billing order | `imdb_MovieLens.movies2actors.cast_num` |
| negative sentiment | `CAST(imdb_MovieLens.u2base.rating AS NUMERIC) < 3.0` |
| high rating / perfect score | `imdb_MovieLens.u2base.rating = '5'` |
| classic / old film | `imdb_MovieLens.movies.year < 1970` |
| super user | `COUNT(imdb_MovieLens.u2base.movieid) > 1000` |
| active rater | `COUNT(imdb_MovieLens.u2base.movieid) >= 10` |
| prolific actor | `COUNT(imdb_MovieLens.movies2actors.movieid) >= 3` |
| one-time director | `COUNT(imdb_MovieLens.movies2directors.movieid) = 1` |
| collaboration | `COUNT(DISTINCT imdb_MovieLens.movies2directors.movieid) >= 2` |