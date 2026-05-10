# Accidents Schema Reference Guide

## Schema Summary
The Accidents schema contains traffic incident records with involved persons, administrative jurisdictions, and geographic coordinates for safety analysis and compliance reporting.

---

## Table Reference

### Table: `Accidents.nesreca`
**Meaning:** Traffic accident/incident record (synonyms: incident, crash, accident event)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_nesreca` | VARCHAR | Unique accident identifier | accident ID, incident ID |
| `klas_nesreca` | VARCHAR | Accident severity classification | severity class, classification |
| | | **Values:** B (minor), H (serious), L (light), P (property damage), S (severe), U (unknown) | |
| `upravna_enota` | VARCHAR | Administrative unit code where accident occurred | admin unit, jurisdiction |
| `cas_nesreca` | TIMESTAMP | Date and time of accident | accident time, incident time, datetime |
| `naselje_ali_izven` | VARCHAR | Urban (D) or rural (N) location | settlement type, location type |
| | | **Values:** D (urban/settlement), N (rural/outside) | |
| `kategorija_cesta` | VARCHAR | Road category | road type, road class |
| | | **Values:** 0–5 (numeric), A, H, L, M, N, R, T, V (letter codes) | |
| `oznaka_cesta_ali_naselje` | VARCHAR | Road or settlement code | road code, location code |
| `tekst_cesta_ali_naselje` | VARCHAR | Road or settlement name | road name, location name |
| `oznaka_odsek_ali_ulica` | VARCHAR | Road section or street code | section code, street code |
| `tekst_odsek_ali_ulica` | VARCHAR | Road section or street name | section name, street name |
| `stacionazna_ali_hisna_st` | VARCHAR | Station number or house number | station number, address number |
| `opis_prizorisce` | VARCHAR | Scene description/type | scene type, location description |
| | | **Values:** A, C, K, M, N, P, R, Z, Ž | |
| `vzrok_nesreca` | VARCHAR | Cause of accident | accident cause, cause code |
| | | **Values:** CE, HI, NP, OS, PD, PR, PV, SV, TO, VO, VR | |
| `tip_nesreca` | VARCHAR | Type of accident | accident type, incident type |
| | | **Values:** BT, NT, OP, OS, PP, PR, PZ, TO, TV, ÈT | |
| `vreme_nesreca` | VARCHAR | Weather conditions | weather, weather code |
| | | **Values:** D, J, M, N, O, S, T, V | |
| `stanje_promet` | VARCHAR | Traffic conditions | traffic state, traffic condition |
| | | **Values:** E, G, N, R, Z | |
| `stanje_vozisce` | VARCHAR | Road surface condition | road condition, surface condition |
| | | **Values:** BL, MO, OS, PN, PP, SL, SN, SP, SU | |
| `stanje_povrsina_vozisce` | VARCHAR | Road surface type | surface type, pavement type |
| | | **Values:** A, M, O | |
| `x` | BIGINT | X coordinate (local projection) | x coord, easting |
| `y` | BIGINT | Y coordinate (local projection) | y coord, northing |
| `x_wgs84` | DOUBLE | X coordinate (WGS84 longitude) | longitude, wgs84_x |
| `y_wgs84` | DOUBLE | Y coordinate (WGS84 latitude) | latitude, wgs84_y |

---

### Table: `Accidents.oseba`
**Meaning:** Person involved in accident (synonyms: participant, person record, individual)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_nesreca` | VARCHAR | Foreign key to accident | accident ID, incident ID |
| `povzrocitelj_ali_udelezenec` | VARCHAR | Role: cause/responsible (D) or participant (N) | role, responsibility, participant type |
| | | **Values:** D (cause/responsible), N (participant) | |
| `starost` | BIGINT | Age in years | age, years old |
| `spol` | VARCHAR | Gender | gender, sex |
| | | **Values:** 0 (unknown), 1 (male), 2 (female) | |
| `upravna_enota` | VARCHAR | Administrative unit of person's residence | admin unit, jurisdiction |
| `drzavljanstvo` | VARCHAR | Citizenship code | citizenship, nationality |
| `poskodba` | VARCHAR | Injury severity | injury, injury type, injury severity |
| | | **Values:** (empty), B, H, L, P, S, U | |
| `vrsta_udelezenca` | VARCHAR | Type of participant | participant type, person type |
| `varnostni_pas_ali_celada` | VARCHAR | Safety belt or helmet use | safety equipment, belt/helmet |
| | | **Values:** * (unknown), 0, 1, 2, D, N | |
| `vozniski_staz_LL` | BIGINT | Driving experience (years) | driving experience, years driving |
| `vozniski_staz_MM` | BIGINT | Driving experience (months) | driving experience months |
| `alkotest` | DOUBLE | Alcohol test result (BAC) | alcohol level, BAC, breathalyzer |
| `strokovni_pregled` | DOUBLE | Expert examination result | expert test, technical test |
| `starost_d` | VARCHAR | Age category | age group, age category |
| | | **Values:** A–J, N (categories) | |
| `vozniski_staz_d` | VARCHAR | Driving experience category | experience category, experience group |
| | | **Values:** A–J, N (categories) | |
| `alkotest_d` | VARCHAR | Alcohol level category | alcohol category, BAC category |
| | | **Values:** A–J, N (categories) | |
| `strokovni_pregled_d` | VARCHAR | Expert test result category | expert test category, test category |
| | | **Values:** A–J, N (categories) | |

---

### Table: `Accidents.upravna_enota`
**Meaning:** Administrative unit/jurisdiction reference (synonyms: administrative region, jurisdiction, district)

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_upravna_enota` | VARCHAR | Administrative unit code (primary key) | admin unit ID, jurisdiction code |
| `ime_upravna_enota` | VARCHAR | Administrative unit name | admin unit name, jurisdiction name |
| `st_prebivalcev` | BIGINT | Population count | population, inhabitants |
| `povrsina` | BIGINT | Area in square kilometers | area, surface area, km² |

---

## Join Paths

**Accident to Person:**
```sql
nesreca.id_nesreca = oseba.id_nesreca
```

**Accident to Administrative Unit:**
```sql
nesreca.upravna_enota = upravna_enota.id_upravna_enota
```

**Person to Administrative Unit (residence):**
```sql
oseba.upravna_enota = upravna_enota.id_upravna_enota
```

---

## Business Rules as SQL

| Rule | SQL Implementation |
|------|-------------------|
| Only completed investigations in official statistics | `WHERE id_nesreca IS NOT NULL AND cas_nesreca IS NOT NULL AND upravna_enota IS NOT NULL` |
| Fatality incidents take priority | `ORDER BY CASE WHEN klas_nesreca = 'S' THEN 0 ELSE 1 END` |
| Injury severity hierarchy | `CASE WHEN poskodba = 'S' THEN 1 WHEN poskodba = 'H' THEN 2 WHEN poskodba = 'L' THEN 3 WHEN poskodba = 'P' THEN 4 WHEN poskodba = 'B' THEN 5 ELSE 6 END` |
| Exclude unknown injury severity from distribution | `WHERE poskodba NOT IN ('U', '')` |
| Urban vs. rural classification | `WHERE naselje_ali_izven = 'D'` (urban) or `WHERE naselje_ali_izven = 'N'` (rural) |
| Responsible party identification | `WHERE povzrocitelj_ali_udelezenec = 'D'` |
| Vulnerable road users | `WHERE vrsta_udelezenca IN ('PT', 'KO')` (pedestrian, cyclist) |
| Night time block (0-4 hours) | `WHERE EXTRACT(HOUR FROM cas_nesreca) >= 0 AND EXTRACT(HOUR FROM cas_nesreca) < 4` |
| Early morning block (4-8 hours) | `WHERE EXTRACT(HOUR FROM cas_nesreca) >= 4 AND EXTRACT(HOUR FROM cas_nesreca) < 8` |
| Morning block (8-12 hours) | `WHERE EXTRACT(HOUR FROM cas_nesreca) >= 8 AND EXTRACT(HOUR FROM cas_nesreca) < 12` |
| Afternoon block (12-16 hours) | `WHERE EXTRACT(HOUR FROM cas_nesreca) >= 12 AND EXTRACT(HOUR FROM cas_nesreca) < 16` |
| Evening block (16-20 hours) | `WHERE EXTRACT(HOUR FROM cas_nesreca) >= 16 AND EXTRACT(HOUR FROM cas_nesreca) < 20` |
| Late block (20-24 hours) | `WHERE EXTRACT(HOUR FROM cas_nesreca) >= 20 AND EXTRACT(HOUR FROM cas_nesreca) < 24` |
| Weekend period (Sat 6PM–Mon 6AM) | `WHERE (EXTRACT(DOW FROM cas_nesreca) = 6 AND EXTRACT(HOUR FROM cas_nesreca) >= 18) OR (EXTRACT(DOW FROM cas_nesreca) = 0) OR (EXTRACT(DOW FROM cas_nesreca) = 1 AND EXTRACT(HOUR FROM cas_nesreca) < 6)` |
| Impaired driving indicator | `WHERE alkotest > 0.5` |
| Safety equipment not used | `WHERE varnostni_pas_ali_celada IN ('N', '0')` |
| Per 100,000 population rate | `(COUNT(*) * 100000.0) / st_prebivalcev` |

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| accident | `nesreca` table |
| incident | `nesreca` table |
| crash | `nesreca` table |
| person involved | `oseba` table |
| participant | `oseba` table |
| severity | `nesreca.klas_nesreca` |
| injury | `oseba.poskodba` |
| cause | `nesreca.vzrok_nesreca` |
| accident type | `nesreca.tip_nesreca` |
| weather | `nesreca.vreme_nesreca` |
| road condition | `nesreca.stanje_vozisce` |
| traffic condition | `nesreca.stanje_promet` |
| location | `nesreca.tekst_cesta_ali_naselje` |
| urban | `nesreca.naselje_ali_izven = 'D'` |
| rural | `nesreca.naselje_ali_izven = 'N'` |
| responsible party | `oseba.povzrocitelj_ali_udelezenec = 'D'` |
| participant | `oseba.povzrocitelj_ali_udelezenec = 'N'` |
| age | `oseba.starost` |
| gender | `oseba.spol` |
| driving experience | `oseba.vozniski_staz_LL` |
| alcohol level | `oseba.alkotest` |
| BAC | `oseba.alkotest` |
| safety belt | `oseba.varnostni_pas_ali_celada` |
| helmet | `oseba.varnostni_pas_ali_celada` |
| administrative unit | `upravna_enota` table |
| jurisdiction | `upravna_enota` table |
| population | `upravna_enota.st_prebivalcev` |
| area | `upravna_enota.povrsina` |
| coordinates | `nesreca.x_wgs84, nesreca.y_wgs84` |
| latitude | `nesreca.y_wgs84` |
| longitude | `nesreca.x_wgs84` |
| date/time | `nesreca.cas_nesreca` |
| time of day | `EXTRACT(HOUR FROM nesreca.cas_nesreca)` |
| day of week | `EXTRACT(DOW FROM nesreca.cas_nesreca)` |