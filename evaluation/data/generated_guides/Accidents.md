# Accidents Schema Reference Guide

## Schema Summary
This schema contains traffic accident incident records with involved persons, administrative jurisdictions, and geographic coordinates for safety analysis and compliance reporting.

---

## Join Paths

**Accidents by administrative unit:**
```sql
FROM Accidents.nesreca n
JOIN Accidents.upravna_enota u ON n.upravna_enota = u.id_upravna_enota
```

**Persons involved in accidents:**
```sql
FROM Accidents.nesreca n
JOIN Accidents.oseba o ON n.id_nesreca = o.id_nesreca
```

**Full incident with persons and jurisdiction:**
```sql
FROM Accidents.nesreca n
JOIN Accidents.oseba o ON n.id_nesreca = o.id_nesreca
JOIN Accidents.upravna_enota u ON n.upravna_enota = u.id_upravna_enota
```

---

## Business Rules as SQL

**Rule: Include only completed investigations in official statistics**
```sql
WHERE n.klas_nesreca IS NOT NULL 
  AND n.vzrok_nesreca IS NOT NULL 
  AND n.tip_nesreca IS NOT NULL
```

**Rule: Fatality incidents take priority classification**
```sql
WHERE n.klas_nesreca = 'S' OR o.poskodba = 'S'
```

**Rule: Exclude unknown injury severity from severity distribution**
```sql
WHERE o.poskodba NOT IN ('', NULL)
```

**Rule: Vulnerable road users (pedestrians, cyclists)**
```sql
WHERE o.vrsta_udelezenca IN ('PT', 'KO')
```

**Rule: Time-of-day blocks (extract hour from cas_nesreca)**
```sql
-- Night (0-4): EXTRACT(HOUR FROM n.cas_nesreca) < 4
-- Early (4-8): EXTRACT(HOUR FROM n.cas_nesreca) >= 4 AND < 8
-- Morning (8-12): EXTRACT(HOUR FROM n.cas_nesreca) >= 8 AND < 12
-- Afternoon (12-16): EXTRACT(HOUR FROM n.cas_nesreca) >= 12 AND < 16
-- Evening (16-20): EXTRACT(HOUR FROM n.cas_nesreca) >= 16 AND < 20
-- Late (20-24): EXTRACT(HOUR FROM n.cas_nesreca) >= 20
```

**Rule: Weekend incidents (Saturday 6PM – Monday 6AM)**
```sql
WHERE (EXTRACT(DOW FROM n.cas_nesreca) = 6 AND EXTRACT(HOUR FROM n.cas_nesreca) >= 18)
   OR (EXTRACT(DOW FROM n.cas_nesreca) = 0)
   OR (EXTRACT(DOW FROM n.cas_nesreca) = 1 AND EXTRACT(HOUR FROM n.cas_nesreca) < 6)
```

**Rule: Normalize statistics per 100,000 population**
```sql
SELECT COUNT(*) * 100000.0 / u.st_prebivalcev AS rate_per_100k
FROM Accidents.nesreca n
JOIN Accidents.upravna_enota u ON n.upravna_enota = u.id_upravna_enota
GROUP BY u.id_upravna_enota, u.st_prebivalcev
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| accident severity | `Accidents.nesreca.klas_nesreca` |
| injury type | `Accidents.oseba.poskodba` |
| cause of accident | `Accidents.nesreca.vzrok_nesreca` |
| accident type | `Accidents.nesreca.tip_nesreca` |
| road category | `Accidents.nesreca.kategorija_cesta` |
| scene description | `Accidents.nesreca.opis_prizorisce` |
| traffic state | `Accidents.nesreca.stanje_promet` |
| road surface condition | `Accidents.nesreca.stanje_vozisce` |
| surface material | `Accidents.nesreca.stanje_povrsina_vozisce` |
| weather/time of day | `Accidents.nesreca.vreme_nesreca` |
| person role | `Accidents.oseba.povzrocitelj_ali_udelezenec` |
| participant type | `Accidents.oseba.vrsta_udelezenca` |
| safety equipment | `Accidents.oseba.varnostni_pas_ali_celada` |
| alcohol test result | `Accidents.oseba.alkotest` |
| driving experience (years) | `Accidents.oseba.vozniski_staz_LL` |
| jurisdiction | `Accidents.upravna_enota.ime_upravna_enota` |
| population | `Accidents.upravna_enota.st_prebivalcev` |

---

## Table Reference

### `Accidents.nesreca`
**Meaning:** Individual accident incident record.  
**Synonyms:** accident, incident, crash, event.

| Column | Semantics |
|--------|-----------|
| `id_nesreca` | Unique incident identifier. |
| `klas_nesreca` | **Severity classification.** Enum: `B` (minor), `H` (serious), `L` (light), `P` (property damage), `S` (fatal), `U` (unknown). |
| `upravna_enota` | Foreign key to `Accidents.upravna_enota.id_upravna_enota`. Administrative jurisdiction. |
| `cas_nesreca` | Incident timestamp (YYYY-MM-DD HH:MM:SS). Use for temporal analysis and time-of-day blocks. |
| `naselje_ali_izven` | Urban/rural indicator. Enum: `D` (urban/settlement), `N` (rural/outside). |
| `kategorija_cesta` | Road category. Enum: `0–5` (local roads), `A` (motorway), `H` (highway), `L` (local), `M` (main), `N` (national), `R` (regional), `T` (transit), `V` (village). |
| `vzrok_nesreca` | **Cause of accident.** Enum: `CE` (weather), `HI` (speed), `NP` (inattention), `OS` (other), `PD` (pedestrian), `PR` (driver error), `PV` (vehicle defect), `SV` (visibility), `TO` (road condition), `VO` (vehicle operation), `VR` (road design). |
| `tip_nesreca` | **Accident type.** Enum: `BT` (rear-end), `NT` (head-on), `OP` (general), `OS` (side), `PP` (pedestrian), `PR` (property), `PZ` (parked vehicle), `TO` (rollover), `TV` (multi-vehicle), `ÈT` (other). |
| `vreme_nesreca` | **Weather/time of day.** Enum: `D` (day), `J` (fog), `M` (darkness), `N` (night), `O` (rain), `S` (snow), `T` (twilight), `V` (wind). |
| `stanje_promet` | Traffic state. Enum: `E` (congested), `G` (dense), `N` (normal), `R` (free-flowing), `Z` (stopped). |
| `stanje_vozisce` | Road surface condition. Enum: `BL` (muddy), `MO` (wet), `OS` (icy), `PN` (snow), `PP` (flooded), `SL` (slippery), `SN` (snowy), `SP` (dry), `SU` (sandy). |
| `stanje_povrsina_vozisce` | Surface material. Enum: `A` (asphalt), `M` (macadam), `O` (other). |
| `x`, `y` | Coordinates in local projection system. |
| `x_wgs84`, `y_wgs84` | WGS84 geographic coordinates (longitude, latitude). |

### `Accidents.oseba`
**Meaning:** Individual person involved in an accident.  
**Synonyms:** participant, person, victim, driver, passenger, pedestrian.

| Column | Semantics |
|--------|-----------|
| `id_nesreca` | Foreign key to `Accidents.nesreca.id_nesreca`. Links person to incident. |
| `povzrocitelj_ali_udelezenec` | **Person role.** Enum: `D` (at-fault/driver), `N` (not at-fault/other participant). |
| `starost` | Age in years. |
| `spol` | Gender. Enum: `0` (unknown), `1` (male), `2` (female). |
| `upravna_enota` | Administrative jurisdiction of person's residence. |
| `drzavljanstvo` | Citizenship code (numeric). |
| `poskodba` | **Injury severity.** Enum: `` (none/property only), `B` (minor), `H` (serious), `L` (light), `P` (property), `S` (fatal), `U` (unknown). Exclude empty/unknown from severity distributions. |
| `vrsta_udelezenca` | Participant type. Examples: `TV` (driver), `OA` (passenger), `PT` (pedestrian), `KO` (cyclist). |
| `varnostni_pas_ali_celada` | Safety equipment use. Enum: `*` (not applicable), `0` (not used), `1` (used), `2` (partial), `D` (unknown), `N` (not applicable). |
| `vozniski_staz_LL` | Driving experience in years (months component). |
| `vozniski_staz_MM` | Driving experience in months. |
| `alkotest` | Alcohol test result (BAC value, numeric). |
| `strokovni_pregled` | Expert examination result (numeric). |
| `starost_d`, `vozniski_staz_d`, `alkotest_d`, `strokovni_pregled_d` | Data quality/completeness flags. Enum: `A–J` (data quality categories), `N` (not applicable/missing). |

### `Accidents.upravna_enota`
**Meaning:** Administrative jurisdiction (district/region).  
**Synonyms:** administrative unit, jurisdiction, district, region.

| Column | Semantics |
|--------|-----------|
| `id_upravna_enota` | Unique jurisdiction identifier. Foreign key in `Accidents.nesreca` and `Accidents.oseba`. |
| `ime_upravna_enota` | Jurisdiction name (e.g., "Ljubljana", "Celje"). |
| `st_prebivalcev` | Population count. Use for rate normalization (per 100,000 population). |
| `povrsina` | Area in km². |