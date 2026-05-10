# VOC Schema Reference Guide

## Schema Summary
This schema documents Dutch East India Company (VOC) voyages, vessels, and personnel records from the 16th–17th centuries, tracking crew composition, mortality, and voyage logistics across multiple personnel categories.

---

## Join Paths

**Voyages with all personnel categories:**
```sql
SELECT v.*, c.onboard_at_departure as craftsmen_departure, s.onboard_at_departure as soldiers_departure
FROM voc.voyages v
LEFT JOIN voc.craftsmen c ON v.number = c.number AND v.trip = c.trip
LEFT JOIN voc.soldiers s ON v.number = s.number AND v.trip = s.trip
LEFT JOIN voc.seafarers sf ON v.number = sf.number AND v.trip = sf.trip
LEFT JOIN voc.passengers p ON v.number = p.number AND v.trip = p.trip
LEFT JOIN voc.impotenten i ON v.number = i.number AND v.trip = i.trip
WHERE v.number = ? AND v.trip = ?
```

**Voyage with invoice records:**
```sql
FROM voc.voyages v
LEFT JOIN voc.invoices inv ON v.number = inv.number AND v.trip = inv.trip
```

**Aggregate personnel by voyage:**
```sql
SELECT v.number, v.trip, v.boatname,
  SUM(c.onboard_at_departure) as total_craftsmen,
  SUM(s.onboard_at_departure) as total_soldiers,
  SUM(sf.onboard_at_departure) as total_seafarers,
  SUM(p.onboard_at_departure) as total_passengers
FROM voc.voyages v
LEFT JOIN voc.craftsmen c ON v.number = c.number AND v.trip = c.trip
LEFT JOIN voc.soldiers s ON v.number = s.number AND v.trip = s.trip
LEFT JOIN voc.seafarers sf ON v.number = sf.number AND v.trip = sf.trip
LEFT JOIN voc.passengers p ON v.number = p.number AND v.trip = p.trip
GROUP BY v.number, v.trip, v.boatname
```

---

## Synonym Glossary

| Question Term | Schema Mapping |
|---|---|
| crew, personnel | `voc.craftsmen`, `voc.soldiers`, `voc.seafarers`, `voc.passengers`, `voc.impotenten` |
| deaths at Cape | `death_at_cape` column (across personnel tables) |
| deaths during voyage | `death_during_voyage` column |
| survivors, arrivals | `onboard_at_arrival` column |
| departures | `onboard_at_departure` column |
| desertions, left ship | `left_at_cape` column |
| vessel, ship | `voc.voyages` (boatname, type_of_boat) |
| voyage leg, journey | `number` + `trip` composite key |
| chamber, port authority | `chamber` column (A, D, E, H, R, Z) |

---

## Table Reference

### `voc.voyages`
**Meaning:** Individual voyage records with vessel details, dates, and routing.  
**Synonyms:** ships, expeditions, legs

| Column | Notes |
|---|---|
| `number`, `trip` | Composite key identifying unique voyage |
| `number_sup`, `trip_sup` | Supplementary identifiers; `trip_sup` values: empty, A, B, a, b |
| `artificial_id` | Unique surrogate identifier |
| `boatname` | Vessel name |
| `master` | Captain/commanding officer |
| `tonnage` | Ship displacement (BIGINT) |
| `type_of_boat` | Vessel class (e.g., "pinas") |
| `built`, `bought`, `hired` | Acquisition year/status |
| `yard` | Chamber/port code: 1, A, B, C, D, E, H, R, Z |
| `chamber` | VOC chamber authority: A, D, E, H, R, Z, ? |
| `departure_date`, `departure_harbour` | Voyage origin |
| `cape_arrival`, `cape_departure` | Cape of Good Hope transit dates |
| `cape_call` | Cape stop indicator: "t" (true), "f" (false) |
| `arrival_date`, `arrival_harbour` | Voyage destination |
| `next_voyage` | Link to subsequent voyage (BIGINT) |
| `particulars` | Free-text notes on voyage events |

---

### `voc.craftsmen`
**Meaning:** Skilled tradespeople aboard voyages.  
**Synonyms:** artisans, technicians

| Column | Notes |
|---|---|
| `number`, `trip` | Foreign key to `voc.voyages` |
| `number_sup` | Supplementary identifier; values: empty, A |
| `trip_sup` | Supplementary trip identifier (empty) |
| `onboard_at_departure` | Headcount at voyage start |
| `death_at_cape` | Fatalities at Cape of Good Hope |
| `left_at_cape` | Desertions/departures at Cape |
| `onboard_at_cape` | Headcount after Cape call |
| `death_during_voyage` | Fatalities during ocean transit |
| `onboard_at_arrival` | Survivors at destination |

---

### `voc.soldiers`
**Meaning:** Military personnel aboard voyages.  
**Synonyms:** troops, garrison, military crew

| Column | Notes |
|---|---|
| `number`, `trip` | Foreign key to `voc.voyages` |
| `number_sup` | Supplementary identifier; values: empty, A |
| `trip_sup` | Supplementary trip identifier; values: empty, b |
| `onboard_at_departure` through `onboard_at_arrival` | Same mortality/headcount tracking as craftsmen |

---

### `voc.seafarers`
**Meaning:** Sailors and maritime crew.  
**Synonyms:** sailors, mariners, deck crew

| Column | Notes |
|---|---|
| `number`, `trip` | Foreign key to `voc.voyages` |
| `number_sup` | Supplementary identifier; values: empty, A |
| `trip_sup` | Supplementary trip identifier; values: empty, b |
| `onboard_at_departure` through `onboard_at_arrival` | Same mortality/headcount tracking |

---

### `voc.passengers`
**Meaning:** Non-crew passengers (merchants, officials, families).  
**Synonyms:** civilians, non-crew, travelers

| Column | Notes |
|---|---|
| `number`, `trip` | Foreign key to `voc.voyages` |
| `number_sup` | Supplementary identifier (empty) |
| `trip_sup` | Supplementary trip identifier (empty) |
| `onboard_at_departure` through `onboard_at_arrival` | Same mortality/headcount tracking |

---

### `voc.impotenten`
**Meaning:** Sick, disabled, or unfit personnel.  
**Synonyms:** invalids, sick crew, disabled personnel

| Column | Notes |
|---|---|
| `number`, `trip` | Foreign key to `voc.voyages` |
| `number_sup` | Supplementary identifier; values: empty, A |
| `trip_sup` | Supplementary trip identifier (empty) |
| `onboard_at_departure` through `onboard_at_arrival` | Same mortality/headcount tracking |

---

### `voc.total`
**Meaning:** Aggregate personnel counts per voyage (sum of all categories).  
**Synonyms:** summary, aggregate crew

| Column | Notes |
|---|---|
| `number`, `trip` | Foreign key to `voc.voyages` |
| `number_sup` | Supplementary identifier (empty) |
| `trip_sup` | Supplementary trip identifier; values: empty, B |
| `onboard_at_departure` through `onboard_at_arrival` | Aggregate headcount across all personnel types |

---

### `voc.invoices`
**Meaning:** Financial/cargo records associated with voyages.  
**Synonyms:** cargo manifests, financial records, ledgers

| Column | Notes |
|---|---|
| `number`, `trip` | Foreign key to `voc.voyages` |
| `number_sup` | Supplementary identifier; values: empty, A |
| `trip_sup` | Supplementary trip identifier (empty) |
| `invoice` | Invoice/manifest identifier (BIGINT) |
| `chamber` | VOC chamber authority: A, D, E, H, R, Z |