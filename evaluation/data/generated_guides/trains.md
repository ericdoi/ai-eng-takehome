# SQL Reference Guide: trains Schema

## 1. Schema Summary
This schema contains data about trains and their individual cars, including physical characteristics (shape, size, roof type) and load information.

---

## 2. Table Reference

### Table: `trains.trains`
**Meaning:** Individual trains with directional information.  
**Synonyms:** train records, train instances

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique train identifier | train_id, train number |
| `direction` | VARCHAR | Cardinal direction of train travel | heading, bearing |

**Enumerated values for `direction`:**
- `east`
- `west`

---

### Table: `trains.cars`
**Meaning:** Individual railroad cars that compose trains, with physical and load specifications.  
**Synonyms:** car records, car instances, train cars, rail cars

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique car identifier | car_id, car number |
| `train_id` | BIGINT | Foreign key reference to parent train | train identifier |
| `position` | BIGINT | Sequential position of car within train (1-indexed) | order, sequence, index |
| `shape` | VARCHAR | Outer geometric shape of car body | body_shape, car_shape, form |
| `len` | VARCHAR | Length classification of car | length, size |
| `sides` | VARCHAR | Whether car has double-sided walls | wall_type, side_type |
| `roof` | VARCHAR | Roof style of car | roof_type, roof_style, top |
| `wheels` | BIGINT | Number of wheels on car | wheel_count, axles |
| `load_shape` | VARCHAR | Geometric shape of cargo/load | cargo_shape, payload_shape |
| `load_num` | BIGINT | Quantity or count of loads | load_count, cargo_count, quantity |

**Enumerated values for `shape`:**
- `bucket`
- `ellipse`
- `hexagon`
- `rectangle`
- `u_shaped`

**Enumerated values for `len`:**
- `long`
- `short`

**Enumerated values for `sides`:**
- `double`
- `not_double`

**Enumerated values for `roof`:**
- `arc`
- `flat`
- `jagged`
- `none`
- `peaked`

**Enumerated values for `load_shape`:**
- `circle`
- `diamond`
- `hexagon`
- `rectangle`
- `triangle`

---

## 3. Join Paths

**Train to Cars (one-to-many):**
```sql
trains.trains
INNER JOIN trains.cars ON trains.trains.id = trains.cars.train_id
```

**Alias form:**
```sql
trains.trains t
INNER JOIN trains.cars c ON t.id = c.train_id
```

---

## 4. Business Rules as SQL
*(No business rules provided in schema documentation)*

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| train direction | `trains.trains.direction` |
| train heading | `trains.trains.direction` |
| car body shape | `trains.cars.shape` |
| car length | `trains.cars.len` |
| car roof type | `trains.cars.roof` |
| car position in train | `trains.cars.position` |
| number of wheels | `trains.cars.wheels` |
| cargo shape | `trains.cars.load_shape` |
| cargo quantity | `trains.cars.load_num` |
| double-sided walls | `trains.cars.sides = 'double'` |
| single-sided walls | `trains.cars.sides = 'not_double'` |
| cars in a train | `trains.cars WHERE train_id = X` |
| all cars for direction | `trains.cars c INNER JOIN trains.trains t ON c.train_id = t.id WHERE t.direction = 'X'` |