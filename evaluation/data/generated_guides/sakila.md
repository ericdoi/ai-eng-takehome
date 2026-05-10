# Sakila Schema Reference Guide

## Schema Summary
The Sakila schema models a DVD rental business, tracking films, actors, customers, rentals, payments, and store operations.

---

## Join Paths

**Film → Actor**
```sql
FROM sakila.film f
JOIN sakila.film_actor fa ON f.film_id = fa.film_id
JOIN sakila.actor a ON fa.actor_id = a.actor_id
```

**Film → Category**
```sql
FROM sakila.film f
JOIN sakila.film_category fc ON f.film_id = fc.film_id
JOIN sakila.category c ON fc.category_id = c.category_id
```

**Film → Language**
```sql
FROM sakila.film f
JOIN sakila.language l ON f.language_id = l.language_id
```

**Customer → Rental → Inventory → Film**
```sql
FROM sakila.customer c
JOIN sakila.rental r ON c.customer_id = r.customer_id
JOIN sakila.inventory i ON r.inventory_id = i.inventory_id
JOIN sakila.film f ON i.film_id = f.film_id
```

**Customer → Payment**
```sql
FROM sakila.customer c
JOIN sakila.payment p ON c.customer_id = p.customer_id
```

**Customer → Address → City → Country**
```sql
FROM sakila.customer c
JOIN sakila.address a ON c.address_id = a.address_id
JOIN sakila.city ci ON a.city_id = ci.city_id
JOIN sakila.country co ON ci.country_id = co.country_id
```

**Store → Inventory → Film**
```sql
FROM sakila.store s
JOIN sakila.inventory i ON s.store_id = i.store_id
JOIN sakila.film f ON i.film_id = f.film_id
```

---

## Table Reference

### `sakila.actor`
Actors in films.
- `actor_id`: Primary key
- `first_name`, `last_name`: Actor name

### `sakila.address`
Physical addresses for customers and stores.
- `address_id`: Primary key
- `address`, `address2`: Street address
- `district`: State/province
- `city_id`: Foreign key to `sakila.city`
- `postal_code`, `phone`: Contact details

### `sakila.category`
Film categories.
- `category_id`: Primary key
- `name`: Enumerated values: `Action`, `Animation`, `Children`, `Classics`, `Comedy`, `Documentary`, `Drama`, `Family`, `Foreign`, `Games`, `Horror`, `Music`, `New`, `Sci-Fi`, `Sports`, `Travel`

### `sakila.city`
Cities worldwide.
- `city_id`: Primary key
- `city`: City name
- `country_id`: Foreign key to `sakila.country`

### `sakila.country`
Countries worldwide.
- `country_id`: Primary key
- `country`: Country name

### `sakila.customer`
Rental customers.
- `customer_id`: Primary key
- `store_id`: Foreign key to `sakila.store` (store where customer registered)
- `first_name`, `last_name`, `email`: Customer contact
- `address_id`: Foreign key to `sakila.address`
- `active`: Boolean; `True` = active customer
- `create_date`: Account creation timestamp
- `last_update`: Last modification timestamp

### `sakila.film`
Films available for rental.
- `film_id`: Primary key
- `title`: Film title
- `description`: Plot summary
- `release_year`: Year released
- `language_id`: Foreign key to `sakila.language` (primary language)
- `original_language_id`: Foreign key to `sakila.language` (if dubbed; nullable)
- `rental_duration`: Days available for rental
- `rental_rate`: Price per rental (DOUBLE)
- `length`: Duration in minutes
- `replacement_cost`: Cost to replace damaged copy (DOUBLE)
- `rating`: Enumerated values: `G`, `PG`, `PG-13`, `R`, `NC-17`
- `special_features`: Comma-separated list; values include: `Behind the Scenes`, `Commentaries`, `Deleted Scenes`, `Trailers`

### `sakila.film_actor`
Junction table linking films to actors.
- `actor_id`: Foreign key to `sakila.actor`
- `film_id`: Foreign key to `sakila.film`

### `sakila.film_category`
Junction table linking films to categories.
- `film_id`: Foreign key to `sakila.film`
- `category_id`: Foreign key to `sakila.category`

### `sakila.film_text`
Full-text search index for films (denormalized copy of title and description).
- `film_id`: Foreign key to `sakila.film`
- `title`, `description`: Searchable text

### `sakila.inventory`
Physical copies of films in stores.
- `inventory_id`: Primary key
- `film_id`: Foreign key to `sakila.film`
- `store_id`: Foreign key to `sakila.store`

### `sakila.language`
Languages available for films.
- `language_id`: Primary key
- `name`: Enumerated values: `English`, `French`, `German`, `Italian`, `Japanese`, `Mandarin`

### `sakila.payment`
Customer rental payments.
- `payment_id`: Primary key
- `customer_id`: Foreign key to `sakila.customer`
- `staff_id`: Foreign key to `sakila.staff` (staff member who processed payment)
- `rental_id`: Foreign key to `sakila.rental`
- `amount`: Payment amount (DOUBLE)
- `payment_date`: When payment was made

### `sakila.rental`
Rental transactions.
- `rental_id`: Primary key
- `rental_date`: When rental began
- `inventory_id`: Foreign key to `sakila.inventory`
- `customer_id`: Foreign key to `sakila.customer`
- `return_date`: When film was returned (nullable if not yet returned)
- `staff_id`: Foreign key to `sakila.staff` (staff member who processed rental)

### `sakila.staff`
Store employees.
- `staff_id`: Primary key
- `first_name`, `last_name`: Enumerated values: `Jon`, `Mike` / `Hillyer`, `Stephens`
- `address_id`: Foreign key to `sakila.address`
- `email`: Enumerated values: `Jon.Stephens@sakilastaff.com`, `Mike.Hillyer@sakilastaff.com`
- `store_id`: Foreign key to `sakila.store`
- `active`: Boolean; `True` = active staff member
- `username`: Enumerated values: `Jon`, `Mike`
- `password`: Hashed password

### `sakila.store`
Rental store locations.
- `store_id`: Primary key
- `manager_staff_id`: Foreign key to `sakila.staff` (store manager)
- `address_id`: Foreign key to `sakila.address`