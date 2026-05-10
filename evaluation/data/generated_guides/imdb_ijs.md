# IMDB Schema Reference Guide

## Schema Summary
This schema contains IMDb data on movies, actors, directors, and their relationships, including genre classifications and actor roles.

---

## Join Paths

**Actors to movies (via roles):**
```sql
FROM imdb_ijs.actors a
JOIN imdb_ijs.roles r ON a.id = r.actor_id
JOIN imdb_ijs.movies m ON r.movie_id = m.id
```

**Directors to movies:**
```sql
FROM imdb_ijs.directors d
JOIN imdb_ijs.movies_directors md ON d.id = md.director_id
JOIN imdb_ijs.movies m ON md.movie_id = m.id
```

**Movies to genres:**
```sql
FROM imdb_ijs.movies m
JOIN imdb_ijs.movies_genres mg ON m.id = mg.movie_id
```

**Directors to genres (probabilistic):**
```sql
FROM imdb_ijs.directors d
JOIN imdb_ijs.directors_genres dg ON d.id = dg.director_id
```

**Complete actor-movie-director chain:**
```sql
FROM imdb_ijs.actors a
JOIN imdb_ijs.roles r ON a.id = r.actor_id
JOIN imdb_ijs.movies m ON r.movie_id = m.id
JOIN imdb_ijs.movies_directors md ON m.id = md.movie_id
JOIN imdb_ijs.directors d ON md.director_id = d.id
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| actor filmography | `imdb_ijs.roles` joined to `imdb_ijs.movies` |
| director filmography | `imdb_ijs.movies_directors` joined to `imdb_ijs.movies` |
| movie rating | `imdb_ijs.movies.rank` |
| movie release year | `imdb_ijs.movies.year` |
| actor gender | `imdb_ijs.actors.gender` (values: F, M) |
| director genre affinity | `imdb_ijs.directors_genres.prob` |
| actor character name | `imdb_ijs.roles.role` |

---

## Table Reference

### `imdb_ijs.actors`
Actors in the database.

| Column | Notes |
|--------|-------|
| `gender` | Enumerated: `F`, `M` |

---

### `imdb_ijs.directors`
Directors in the database.

| Column | Notes |
|--------|-------|
| `first_name`, `last_name` | May contain non-standard characters and nicknames |

---

### `imdb_ijs.directors_genres`
Genre probability distribution for each director (derived from their filmography).

| Column | Notes |
|--------|-------|
| `genre` | Enumerated: Action, Adventure, Animation, Comedy, Crime, Documentary, Drama, Family, Fantasy, Film-Noir, Horror, Music, Musical, Mystery, Romance, Sci-Fi, Short, Thriller, War, Western |
| `prob` | Probability value (0.0–1.0); sum of probabilities per director may equal 1.0 |

---

### `imdb_ijs.movies`
Movies in the database.

| Column | Notes |
|--------|-------|
| `rank` | IMDb rating; may be `NaN` (null) |
| `year` | Release year |

---

### `imdb_ijs.movies_directors`
Junction table linking movies to their directors.

---

### `imdb_ijs.movies_genres`
Junction table linking movies to their genres (actual genres, not probabilistic).

| Column | Notes |
|--------|-------|
| `genre` | Enumerated: Action, Adventure, Animation, Comedy, Crime, Documentary, Drama, Family, Fantasy, Film-Noir, Horror, Music, Musical, Mystery, Romance, Sci-Fi, Short, Thriller, War, Western |

---

### `imdb_ijs.roles`
Actor appearances in movies.

| Column | Notes |
|--------|-------|
| `role` | Character name or description (e.g., "Himself", "Various/lyricist") |