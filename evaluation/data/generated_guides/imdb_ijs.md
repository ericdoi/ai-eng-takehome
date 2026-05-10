# IMDB IJS Schema Reference Guide

## Schema Summary
The `imdb_ijs` schema contains Internet Movie Database information modeling relationships between actors, directors, movies, and their associated genres with probability distributions.

---

## Table Reference

### `imdb_ijs.actors`
**Meaning:** Individual actors/performers in the database.  
**Synonyms:** performers, cast members

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique actor identifier | actor_id |
| `first_name` | VARCHAR | Actor's first name | given_name |
| `last_name` | VARCHAR | Actor's last name | surname, family_name |
| `gender` | VARCHAR | Actor's gender | sex |

**Notable values:** `gender` ∈ {`F`, `M`}

---

### `imdb_ijs.directors`
**Meaning:** Individual directors in the database.  
**Synonyms:** filmmakers

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique director identifier | director_id |
| `first_name` | VARCHAR | Director's first name | given_name |
| `last_name` | VARCHAR | Director's last name | surname, family_name |

---

### `imdb_ijs.directors_genres`
**Meaning:** Probability distribution of genres associated with each director based on their filmography.  
**Synonyms:** director genre preferences, director genre probabilities

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `director_id` | BIGINT | References `directors.id` | — |
| `genre` | VARCHAR | Film genre classification | category, type |
| `prob` | DOUBLE | Probability/frequency of genre in director's work | probability, frequency, weight |

**Notable values:** `genre` ∈ {`Action`, `Adventure`, `Animation`, `Comedy`, `Crime`, `Documentary`, `Drama`, `Family`, `Fantasy`, `Film-Noir`, `Horror`, `Music`, `Musical`, `Mystery`, `Romance`, `Sci-Fi`, `Short`, `Thriller`, `War`, `Western`}

---

### `imdb_ijs.movies`
**Meaning:** Films in the database with metadata.  
**Synonyms:** films, titles

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique movie identifier | movie_id |
| `name` | VARCHAR | Movie title | title |
| `year` | BIGINT | Release year | release_year |
| `rank` | DOUBLE | IMDb rating/score | rating, score, imdb_rating |

---

### `imdb_ijs.movies_directors`
**Meaning:** Junction table linking movies to their directors (many-to-many).  
**Synonyms:** film directors, movie direction assignments

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `director_id` | BIGINT | References `directors.id` | — |
| `movie_id` | BIGINT | References `movies.id` | — |

---

### `imdb_ijs.movies_genres`
**Meaning:** Junction table linking movies to their genres (many-to-many).  
**Synonyms:** film genres, movie categories

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `movie_id` | BIGINT | References `movies.id` | — |
| `genre` | VARCHAR | Film genre classification | category, type |

**Notable values:** `genre` ∈ {`Action`, `Adventure`, `Animation`, `Comedy`, `Crime`, `Documentary`, `Drama`, `Family`, `Fantasy`, `Film-Noir`, `Horror`, `Music`, `Musical`, `Mystery`, `Romance`, `Sci-Fi`, `Short`, `Thriller`, `War`, `Western`}

---

### `imdb_ijs.roles`
**Meaning:** Character roles played by actors in specific movies.  
**Synonyms:** cast assignments, character appearances

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `actor_id` | BIGINT | References `actors.id` | — |
| `movie_id` | BIGINT | References `movies.id` | — |
| `role` | VARCHAR | Character name or role description | character, character_name |

---

## Join Paths

| From | To | Condition |
|------|----|-----------| 
| `actors` | `roles` | `actors.id = roles.actor_id` |
| `roles` | `movies` | `roles.movie_id = movies.id` |
| `movies` | `movies_directors` | `movies.id = movies_directors.movie_id` |
| `movies_directors` | `directors` | `movies_directors.director_id = directors.id` |
| `movies` | `movies_genres` | `movies.id = movies_genres.movie_id` |
| `directors` | `directors_genres` | `directors.id = directors_genres.director_id` |
| `directors` | `movies_directors` | `directors.id = movies_directors.director_id` |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| actor filmography | `SELECT movies.* FROM movies JOIN roles ON movies.id = roles.movie_id WHERE roles.actor_id = ?` |
| director filmography | `SELECT movies.* FROM movies JOIN movies_directors ON movies.id = movies_directors.movie_id WHERE movies_directors.director_id = ?` |
| movie cast | `SELECT actors.* FROM actors JOIN roles ON actors.id = roles.actor_id WHERE roles.movie_id = ?` |
| movie directors | `SELECT directors.* FROM directors JOIN movies_directors ON directors.id = movies_directors.director_id WHERE movies_directors.movie_id = ?` |
| movie genres | `SELECT genre FROM movies_genres WHERE movie_id = ?` |
| director genre preference | `directors_genres.genre WHERE directors_genres.prob` |
| highly rated movie | `movies.rank > 7.0` (example threshold) |
| recent movie | `movies.year >= 2000` (example threshold) |
| actor by gender | `actors.gender = 'M'` or `actors.gender = 'F'` |