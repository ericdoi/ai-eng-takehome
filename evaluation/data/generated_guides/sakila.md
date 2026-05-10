# Sakila Schema Reference Guide

## Schema Summary
The Sakila schema is a sample movie rental database containing information about films, actors, customers, rentals, payments, and store operations.

---

## Table Reference

### sakila.actor
**Meaning**: Film actors/performers  
**Synonyms**: performer, cast member

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| actor_id | BIGINT | Unique actor identifier | actor number |
| first_name | VARCHAR | Actor's first name | given name |
| last_name | VARCHAR | Actor's surname | family name |
| last_update | TIMESTAMP | Record last modification time | updated |

---

### sakila.address
**Meaning**: Physical addresses for customers, staff, and stores  
**Synonyms**: location, street address

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| address_id | BIGINT | Unique address identifier | address number |
| address | VARCHAR | Street address line 1 | street, street_address |
| address2 | VARCHAR | Street address line 2 (optional) | apartment, suite |
| district | VARCHAR | Administrative district/region | state, province, region |
| city_id | BIGINT | Foreign key to city | city reference |
| postal_code | VARCHAR | ZIP/postal code | zip |
| phone | VARCHAR | Phone number | telephone |
| last_update | TIMESTAMP | Record last modification time | updated |

---

### sakila.category
**Meaning**: Film genre/content categories  
**Synonyms**: genre, film type

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| category_id | BIGINT | Unique category identifier | category number |
| name | VARCHAR | Category name | genre name |
| last_update | TIMESTAMP | Record last modification time | updated |

**Enumerated Values**: Action, Animation, Children, Classics, Comedy, Documentary, Drama, Family, Foreign, Games, Horror, Music, New, Sci-Fi, Sports, Travel

---

### sakila.city
**Meaning**: Cities worldwide  
**Synonyms**: municipality, town

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| city_id | BIGINT | Unique city identifier | city number |
| city | VARCHAR | City name | city name |
| country_id | BIGINT | Foreign key to country | country reference |
| last_update | TIMESTAMP | Record last modification time | updated |

---

### sakila.country
**Meaning**: Countries worldwide  
**Synonyms**: nation, region

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| country_id | BIGINT | Unique country identifier | country number |
| country | VARCHAR | Country name | country name |
| last_update | TIMESTAMP | Record last modification time | updated |

---

### sakila.customer
**Meaning**: Film rental customers  
**Synonyms**: renter, client, patron

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| customer_id | BIGINT | Unique customer identifier | customer number |
| store_id | BIGINT | Foreign key to store | store reference |
| first_name | VARCHAR | Customer's first name | given name |
| last_name | VARCHAR | Customer's surname | family name |
| email | VARCHAR | Email address | email address |
| address_id | BIGINT | Foreign key to address | address reference |
| active | BOOLEAN | Whether customer account is active | status, enabled |
| create_date | TIMESTAMP | Account creation date | registered, joined |
| last_update | TIMESTAMP | Record last modification time | updated |

---

### sakila.film
**Meaning**: Film/movie catalog  
**Synonyms**: movie, title

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| film_id | BIGINT | Unique film identifier | film number, movie id |
| title | VARCHAR | Film title | film name, movie title |
| description | VARCHAR | Film plot summary | synopsis, summary |
| release_year | BIGINT | Year film was released | year |
| language_id | BIGINT | Foreign key to language (primary) | language reference |
| original_language_id | BIGINT | Foreign key to language (original) | original language reference |
| rental_duration | BIGINT | Number of days rental period | rental days |
| rental_rate | DOUBLE | Daily rental cost | rental price |
| length | BIGINT | Film duration in minutes | duration, runtime |
| replacement_cost | DOUBLE | Cost to replace damaged copy | replacement price |
| rating | VARCHAR | Content rating | mpaa_rating |
| special_features | VARCHAR | Bonus features included | features |
| last_update | TIMESTAMP | Record last modification time | updated |

**Enumerated Values (rating)**: G, NC-17, PG, PG-13, R

**Enumerated Values (special_features)**: Behind the Scenes, Commentaries, Deleted Scenes, Trailers (in various combinations)

---

### sakila.film_actor
**Meaning**: Junction table linking films to actors (many-to-many)  
**Synonyms**: cast, film_cast

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| actor_id | BIGINT | Foreign key to actor | actor reference |
| film_id | BIGINT | Foreign key to film | film reference |
| last_update | TIMESTAMP | Record last modification time | updated |

---

### sakila.film_category
**Meaning**: Junction table linking films to categories (many-to-many)  
**Synonyms**: film_genre

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| film_id | BIGINT | Foreign key to film | film reference |
| category_id | BIGINT | Foreign key to category | category reference |
| last_update | TIMESTAMP | Record last modification time | updated |

---

### sakila.film_text
**Meaning**: Full-text search index for films  
**Synonyms**: film_search, film_index

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| film_id | BIGINT | Unique film identifier | film number |
| title | VARCHAR | Film title | film name |
| description | VARCHAR | Film plot summary | synopsis |

---

### sakila.inventory
**Meaning**: Physical film copies in stock at stores  
**Synonyms**: stock, copy, item

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| inventory_id | BIGINT | Unique inventory item identifier | copy id, item id |
| film_id | BIGINT | Foreign key to film | film reference |
| store_id | BIGINT | Foreign key to store | store reference |
| last_update | TIMESTAMP | Record last modification time | updated |

---

### sakila.language
**Meaning**: Languages used in films  
**Synonyms**: film language

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| language_id | BIGINT | Unique language identifier | language number |
| name | VARCHAR | Language name | language name |
| last_update | TIMESTAMP | Record last modification time | updated |

**Enumerated Values**: English, French, German, Italian, Japanese, Mandarin

---

### sakila.payment
**Meaning**: Customer rental payments  
**Synonyms**: transaction, charge

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| payment_id | BIGINT | Unique payment identifier | payment number |
| customer_id | BIGINT | Foreign key to customer | customer reference |
| staff_id | BIGINT | Foreign key to staff (processor) | staff reference |
| rental_id | BIGINT | Foreign key to rental | rental reference |
| amount | DOUBLE | Payment amount in currency units | price, cost |
| payment_date | TIMESTAMP | Date/time payment was made | paid, transaction date |
| last_update | TIMESTAMP | Record last modification time | updated |

---

### sakila.rental
**Meaning**: Film rental transactions  
**Synonyms**: checkout, loan

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| rental_id | BIGINT | Unique rental identifier | rental number |
| rental_date | TIMESTAMP | Date/time rental began | checkout date |
| inventory_id | BIGINT | Foreign key to inventory | inventory reference |
| customer_id | BIGINT | Foreign key to customer | customer reference |
| return_date | TIMESTAMP | Date/time film was returned | checkin date |
| staff_id | BIGINT | Foreign key to staff (processor) | staff reference |
| last_update | TIMESTAMP | Record last modification time | updated |

---

### sakila.staff
**Meaning**: Store employees  
**Synonyms**: employee, worker

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| staff_id | BIGINT | Unique staff identifier | staff number, employee id |
| first_name | VARCHAR | Staff member's first name | given name |
| last_name | VARCHAR | Staff member's surname | family name |
| address_id | BIGINT | Foreign key to address | address reference |
| picture | BLOB | Staff photo/image | photo, image |
| email | VARCHAR | Email address | email address |
| store_id | BIGINT | Foreign key to store | store reference |
| active | BOOLEAN | Whether staff account is active | status, enabled |
| username | VARCHAR | Login username | user |
| password | VARCHAR | Hashed password | pwd |
| last_update | TIMESTAMP | Record last modification time | updated |

**Enumerated Values (first_name)**: Jon, Mike  
**Enumerated Values (last_name)**: Hillyer, Stephens  
**Enumerated Values (username)**: Jon, Mike  
**Enumerated Values (email)**: Jon.Stephens@sakilastaff.com, Mike.Hillyer@sakilastaff.com

---

### sakila.store
**Meaning**: Rental store locations  
**Synonyms**: branch, location

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| store_id | BIGINT | Unique store identifier | store number |
| manager_staff_id | BIGINT | Foreign key to staff (manager) | manager reference |
| address_id | BIGINT | Foreign key to address | address reference |
| last_update | TIMESTAMP | Record last modification time | updated |

---

## Join Paths

### Core Rental Flow
```sql
rental
  JOIN inventory ON rental.inventory_id = inventory.inventory_id
  JOIN film ON inventory.film_id = film.film_id
  JOIN customer ON rental.customer_id = customer.customer_id
  JOIN staff ON rental.staff_id = staff.staff_id
```

### Film Details
```sql
film
  JOIN language ON film.language_id = language.language_id
  LEFT JOIN language AS original_lang ON film.original_language_id = original_lang.language_id
```

### Film Catalog
```sql
film
  JOIN film_actor ON film.film_id = film_actor.film_id
  JOIN actor ON film_actor.actor_id = actor.actor_id

film
  JOIN film_category ON film.film_id = film_category.film_id
  JOIN category ON film_category.category_id = category.category_id
```

### Customer Location
```sql
customer
  JOIN address ON customer.address_id = address.address_id
  JOIN city ON address.city_id = city.city_id
  JOIN country ON city.country_id = country.country_id
```

### Store Structure
```sql
store
  JOIN staff ON store.manager_staff_id = staff.staff_id
  JOIN address ON store.address_id = address.address_id
  JOIN city ON address.city_id = city.city_id
  JOIN country ON city.country_id = country.country_id
```

### Payment Tracking
```sql
payment
  JOIN customer ON payment.customer_id = customer.customer_id
  JOIN rental ON payment.rental_id = rental.rental_id
  JOIN staff ON payment.staff_id = staff.staff_id
```

### Inventory by Store
```sql
inventory
  JOIN film ON inventory.film_id = film.film_id
  JOIN store ON inventory.store_id = store.store_id
```

---

## Synonym Glossary

| Common Term | Schema Reference |
|-------------|------------------|
| actor | `sakila.actor` |
| film / movie / title | `sakila.film` |
| category / genre | `sakila.category` |
| customer / renter / patron | `sakila.customer` |
| rental / checkout / loan | `sakila.rental` |
| payment / transaction / charge | `sakila.payment` |
| staff / employee / worker | `sakila.staff` |
| store / branch / location | `sakila.store` |
| inventory / stock / copy | `sakila.inventory` |
| address / location / street | `sakila.address` |
| city / municipality / town | `sakila.city` |
| country / nation / region | `sakila.country` |
| language / film language | `sakila.language` |
| film cast | `sakila.film_actor` |
| film genre | `sakila.film_category` |
| active customer | `WHERE customer.active = TRUE` |
| active staff | `WHERE staff.active = TRUE` |
| rental duration | `film.rental_duration` |
| rental rate / daily cost | `film.rental_rate` |
| replacement cost | `film.replacement_cost` |
| film length / runtime / duration | `film.length` |
| content rating / MPAA rating | `film.rating` |
| special features / bonus features | `film.special_features` |
| returned rental | `WHERE rental.return_date IS NOT NULL` |
| unreturned rental | `WHERE rental.return_date IS NULL` |
| film description / synopsis / plot | `film.description` |
| customer email | `customer.email` |
| staff email | `staff.email` |
| store manager | `store.manager_staff_id` |
| film language | `film.language_id` |
| original language | `film.original_language_id` |