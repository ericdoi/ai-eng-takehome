# VOC Schema Reference Guide

## Schema Summary
The `voc` schema contains historical records of Dutch East India Company (VOC) voyages, including vessel information, crew composition by role, passenger manifests, and voyage logistics from the 16th–17th centuries.

---

## Table Reference

### voc.voyages
**Meaning:** Voyage records; ship manifests; voyage logs  
**Synonyms:** ships, vessels, expeditions, journeys

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `artificial_id` | VARCHAR | System-generated unique identifier | ID, record_id |
| `number` | BIGINT | Voyage number | voyage_number, trip_id |
| `number_sup` | VARCHAR | Voyage number supplement (qualifier) | number_suffix, qualifier |
| `trip` | BIGINT | Trip identifier | trip_id, voyage_trip |
| `trip_sup` | VARCHAR | Trip supplement (qualifier) | trip_suffix, trip_qualifier |
| `boatname` | VARCHAR | Name of the vessel | ship_name, vessel_name |
| `master` | VARCHAR | Captain/commanding officer name | captain, commander, skipper |
| `tonnage` | BIGINT | Ship capacity in tons | displacement, capacity |
| `type_of_boat` | VARCHAR | Vessel classification | ship_type, vessel_type, boat_class |
| `built` | VARCHAR | Year or date vessel was constructed | construction_year, build_year |
| `bought` | VARCHAR | Year or date vessel was purchased | purchase_year, acquisition_year |
| `hired` | VARCHAR | Year or date vessel was hired/chartered | charter_year, rental_year |
| `yard` | VARCHAR | Shipyard or chamber code | chamber_code, location_code |
| `chamber` | VARCHAR | VOC chamber/regional office | office, region, administrative_unit |
| `departure_date` | DATE | Date vessel left port | sailing_date, embarkation_date |
| `departure_harbour` | VARCHAR | Port of departure | departure_port, origin_port |
| `cape_arrival` | DATE | Date of arrival at Cape of Good Hope | cape_arrival_date |
| `cape_departure` | DATE | Date of departure from Cape of Good Hope | cape_departure_date |
| `cape_call` | VARCHAR | Whether vessel stopped at Cape (t/f) | cape_stop, cape_visited |
| `arrival_date` | DATE | Date of arrival at destination | destination_arrival_date, final_arrival |
| `arrival_harbour` | VARCHAR | Port of arrival/destination | arrival_port, destination_port |
| `next_voyage` | BIGINT | Voyage number of next voyage by same vessel | subsequent_voyage, follow_up_voyage |
| `particulars` | VARCHAR | Notes, remarks, special events | notes, remarks, comments |

**Notable values:**
- `yard`: 1, A, B, C, D, E, H, R, Z
- `chamber`: ?, A, D, E, H, R, Z
- `cape_call`: t, f
- `trip_sup`: (empty), A, B, a, b
- `number_sup`: (empty), A

---

### voc.seafarers
**Meaning:** Crew members with maritime/sailing roles; sailors; deck crew  
**Synonyms:** sailors, crew, maritime_personnel, deck_crew

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `number` | BIGINT | Seafarer identifier | seafarer_id, person_id |
| `number_sup` | VARCHAR | Seafarer number supplement | number_suffix, qualifier |
| `trip` | BIGINT | Trip identifier | trip_id, voyage_trip |
| `trip_sup` | VARCHAR | Trip supplement | trip_suffix, trip_qualifier |
| `onboard_at_departure` | BIGINT | Count embarked at departure | embarked, initial_count |
| `death_at_cape` | BIGINT | Deaths at Cape of Good Hope | cape_deaths, mortality_cape |
| `left_at_cape` | BIGINT | Personnel disembarked at Cape | cape_departures, cape_disembarked |
| `onboard_at_cape` | BIGINT | Count aboard when at Cape | cape_count, present_at_cape |
| `death_during_voyage` | BIGINT | Deaths during ocean transit | voyage_deaths, mortality_voyage |
| `onboard_at_arrival` | BIGINT | Count arrived at destination | final_count, arrival_count |

**Notable values:**
- `number_sup`: (empty), A
- `trip_sup`: (empty), b

---

### voc.soldiers
**Meaning:** Military personnel; armed forces; garrison troops  
**Synonyms:** military, troops, armed_personnel, garrison

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `number` | BIGINT | Soldier identifier | soldier_id, person_id |
| `number_sup` | VARCHAR | Soldier number supplement | number_suffix, qualifier |
| `trip` | BIGINT | Trip identifier | trip_id, voyage_trip |
| `trip_sup` | VARCHAR | Trip supplement | trip_suffix, trip_qualifier |
| `onboard_at_departure` | BIGINT | Count embarked at departure | embarked, initial_count |
| `death_at_cape` | BIGINT | Deaths at Cape of Good Hope | cape_deaths, mortality_cape |
| `left_at_cape` | BIGINT | Personnel disembarked at Cape | cape_departures, cape_disembarked |
| `onboard_at_cape` | BIGINT | Count aboard when at Cape | cape_count, present_at_cape |
| `death_during_voyage` | BIGINT | Deaths during ocean transit | voyage_deaths, mortality_voyage |
| `onboard_at_arrival` | BIGINT | Count arrived at destination | final_count, arrival_count |

**Notable values:**
- `number_sup`: (empty), A
- `trip_sup`: (empty), b

---

### voc.craftsmen
**Meaning:** Skilled tradespeople; artisans; technical specialists  
**Synonyms:** artisans, tradespeople, skilled_workers, technicians

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `number` | BIGINT | Craftsman identifier | craftsman_id, person_id |
| `number_sup` | VARCHAR | Craftsman number supplement | number_suffix, qualifier |
| `trip` | BIGINT | Trip identifier | trip_id, voyage_trip |
| `trip_sup` | VARCHAR | Trip supplement | trip_suffix, trip_qualifier |
| `onboard_at_departure` | BIGINT | Count embarked at departure | embarked, initial_count |
| `death_at_cape` | BIGINT | Deaths at Cape of Good Hope | cape_deaths, mortality_cape |
| `left_at_cape` | BIGINT | Personnel disembarked at Cape | cape_departures, cape_disembarked |
| `onboard_at_cape` | BIGINT | Count aboard when at Cape | cape_count, present_at_cape |
| `death_during_voyage` | BIGINT | Deaths during ocean transit | voyage_deaths, mortality_voyage |
| `onboard_at_arrival` | BIGINT | Count arrived at destination | final_count, arrival_count |

**Notable values:**
- `number_sup`: (empty), A
- `trip_sup`: (empty)

---

### voc.passengers
**Meaning:** Non-crew civilian travelers; paying passengers; colonists  
**Synonyms:** travelers, civilians, colonists, paying_passengers

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `number` | BIGINT | Passenger identifier | passenger_id, person_id |
| `number_sup` | VARCHAR | Passenger number supplement | number_suffix, qualifier |
| `trip` | BIGINT | Trip identifier | trip_id, voyage_trip |
| `trip_sup` | VARCHAR | Trip supplement | trip_suffix, trip_qualifier |
| `onboard_at_departure` | BIGINT | Count embarked at departure | embarked, initial_count |
| `death_at_cape` | BIGINT | Deaths at Cape of Good Hope | cape_deaths, mortality_cape |
| `left_at_cape` | BIGINT | Personnel disembarked at Cape | cape_departures, cape_disembarked |
| `onboard_at_cape` | BIGINT | Count aboard when at Cape | cape_count, present_at_cape |
| `death_during_voyage` | BIGINT | Deaths during ocean transit | voyage_deaths, mortality_voyage |
| `onboard_at_arrival` | BIGINT | Count arrived at destination | final_count, arrival_count |

**Notable values:**
- `number_sup`: (empty)
- `trip_sup`: (empty)

---

### voc.impotenten
**Meaning:** Sick, disabled, or incapacitated personnel; invalids; unfit crew  
**Synonyms:** invalids, sick_personnel, disabled, incapacitated

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `number` | BIGINT | Impotent identifier | impotent_id, person_id |
| `number_sup` | VARCHAR | Impotent number supplement | number_suffix, qualifier |
| `trip` | BIGINT | Trip identifier | trip_id, voyage_trip |
| `trip_sup` | VARCHAR | Trip supplement | trip_suffix, trip_qualifier |
| `onboard_at_departure` | BIGINT | Count embarked at departure | embarked, initial_count |
| `death_at_cape` | BIGINT | Deaths at Cape of Good Hope | cape_deaths, mortality_cape |
| `left_at_cape` | BIGINT | Personnel disembarked at Cape | cape_departures, cape_disembarked |
| `onboard_at_cape` | BIGINT | Count aboard when at Cape | cape_count, present_at_cape |
| `death_during_voyage` | BIGINT | Deaths during ocean transit | voyage_deaths, mortality_voyage |
| `onboard_at_arrival` | BIGINT | Count arrived at destination | final_count, arrival_count |

**Notable values:**
- `number_sup`: (empty), A
- `trip_sup`: (empty)

---

### voc.total
**Meaning:** Aggregate crew and passenger counts per voyage; summary totals  
**Synonyms:** summary, aggregate, totals, manifest_totals

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `number` | BIGINT | Total record identifier | total_id, record_id |
| `number_sup` | VARCHAR | Total number supplement | number_suffix, qualifier |
| `trip` | BIGINT | Trip identifier | trip_id, voyage_trip |
| `trip_sup` | VARCHAR | Trip supplement | trip_suffix, trip_qualifier |
| `onboard_at_departure` | BIGINT | Total count embarked at departure | total_embarked, total_initial |
| `death_at_cape` | BIGINT | Total deaths at Cape of Good Hope | total_cape_deaths |
| `left_at_cape` | BIGINT | Total disembarked at Cape | total_cape_departures |
| `onboard_at_cape` | BIGINT | Total count aboard when at Cape | total_cape_count |
| `death_during_voyage` | BIGINT | Total deaths during ocean transit | total_voyage_deaths |
| `onboard_at_arrival` | BIGINT | Total count arrived at destination | total_final_count |

**Notable values:**
- `number_sup`: (empty)
- `trip_sup`: (empty), B

---

### voc.invoices
**Meaning:** Financial records; cargo manifests; invoice/transaction records  
**Synonyms:** financial_records, cargo_manifests, transactions, bills

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `number` | BIGINT | Invoice identifier | invoice_id, record_id |
| `number_sup` | VARCHAR | Invoice number supplement | number_suffix, qualifier |
| `trip` | BIGINT | Trip identifier | trip_id, voyage_trip |
| `trip_sup` | VARCHAR | Trip supplement | trip_suffix, trip_qualifier |
| `invoice` | BIGINT | Invoice amount or reference number | amount, invoice_number |
| `chamber` | VARCHAR | VOC chamber/regional office | office, region, administrative_unit |

**Notable values:**
- `number_sup`: (empty), A
- `trip_sup`: (empty)
- `chamber`: A, D, E, H, R, Z

---

## Join Paths

**Voyages to Personnel (all types):**
```sql
voc.voyages v
JOIN voc.seafarers s ON v.trip = s.trip
JOIN voc.soldiers so ON v.trip = so.trip
JOIN voc.craftsmen c ON v.trip = c.trip
JOIN voc.passengers p ON v.trip = p.trip
JOIN voc.impotenten i ON v.trip = i.trip
```

**Voyages to Totals:**
```sql
voc.voyages v
JOIN voc.total t ON v.trip = t.trip
```

**Voyages to Invoices:**
```sql
voc.voyages v
JOIN voc.invoices inv ON v.trip = inv.trip
```

**All Personnel to Voyages (union approach):**
```sql
(SELECT trip FROM voc.seafarers
 UNION ALL SELECT trip FROM voc.soldiers
 UNION ALL SELECT trip FROM voc.craftsmen
 UNION ALL SELECT trip FROM voc.passengers
 UNION ALL SELECT trip FROM voc.impotenten) AS personnel
JOIN voc.voyages v ON personnel.trip = v.trip
```

---

## Business Rules as SQL

**Rule: Personnel mortality at Cape of Good Hope**
```sql
WHERE death_at_cape IS NOT NULL AND death_at_cape > 0
```

**Rule: Personnel mortality during voyage (ocean transit)**
```sql
WHERE death_during_voyage IS NOT NULL AND death_during_voyage > 0
```

**Rule: Vessel stopped at Cape of Good Hope**
```sql
WHERE cape_call = 't'
```

**Rule: Vessel did not stop at Cape of Good Hope**
```sql
WHERE cape_call = 'f'
```

**Rule: Personnel disembarked at Cape**
```sql
WHERE left_at_cape IS NOT NULL AND left_at_cape > 0
```

**Rule: Voyage originated from Texel**
```sql
WHERE departure_harbour = 'Texel'
```

**Rule: Voyage arrived at Bantam**
```sql
WHERE arrival_harbour = 'Bantam'
```

**Rule: Voyage from Amsterdam chamber**
```sql
WHERE chamber = 'A'
```

**Rule: Voyage from Rotterdam chamber**
```sql
WHERE chamber = 'R'
```

**Rule: Voyage from Zeeland chamber**
```sql
WHERE chamber = 'Z'
```

**Rule: Vessel with recorded tonnage**
```sql
WHERE tonnage IS NOT NULL AND tonnage > 0
```

**Rule: Voyage with documented next voyage**
```sql
WHERE next_voyage IS NOT NULL
```

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| ship | `voc.voyages.boatname` |
| captain | `voc.voyages.master` |
| crew | `voc.seafarers`, `voc.soldiers`, `voc.craftsmen` |
| sailors | `voc.seafarers` |
| soldiers/military | `voc.soldiers` |
| artisans/tradespeople | `voc.craftsmen` |
| passengers | `voc.passengers` |
| sick/disabled personnel | `voc.impotenten` |
| voyage deaths | `death_during_voyage` |
| Cape deaths | `death_at_cape` |
| embarked/boarded | `onboard_at_departure` |
| disembarked/left | `left_at_cape` |
| arrived | `onboard_at_arrival` |
| ship capacity | `voc.voyages.tonnage` |
| departure port | `voc.voyages.departure_harbour` |
| arrival port | `voc.voyages.arrival_harbour` |
| sailing date | `voc.voyages.departure_date` |
| arrival date | `voc.voyages.arrival_date` |
| Cape stop | `voc.voyages.