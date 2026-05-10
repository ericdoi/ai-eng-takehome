# SQL Reference Guide: geneea Schema

## Schema Summary
The geneea schema contains Czech parliamentary (Poslanecká sněmovna) legislative data including sessions, voting records, deputies, organizational structures, and committee memberships.

---

## Table Reference

### geneea.bod_schuze
**Meaning**: Agenda items (body) of parliamentary sessions; individual topics/motions discussed in sessions.
**Synonyms**: agenda item, motion, topic, session point

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_bod` | BIGINT | Unique agenda item identifier | agenda item ID |
| `id_schuze` | BIGINT | Foreign key to session | session ID |
| `id_tisk` | VARCHAR | Document/print number | document ID, print ID |
| `id_typ` | VARCHAR | Agenda item type code | type ID |
| `bod` | BIGINT | Sequence number within session | item number, order |
| `uplny_naz` | VARCHAR | Full name/title of agenda item | full name, title, description |
| `uplny_kon` | VARCHAR | Full conclusion/outcome text | conclusion, outcome |
| `poznamka` | VARCHAR | Note/remark | note, comment |
| `id_bod_stav` | BIGINT | Foreign key to agenda item status | status ID |
| `pozvanka` | VARCHAR | Invitation flag (0=no, 1=yes) | invitation |
| `rj` | VARCHAR | Regulatory jurisdiction code (0, 1, 2) | jurisdiction |
| `pozn2` | VARCHAR | Secondary note | note 2, remark 2 |
| `druh_bodu` | VARCHAR | Type of agenda point (0, 1, 2, 3) | point type |
| `id_sd` | VARCHAR | Subdepartment ID | subdept ID |
| `zkratka` | VARCHAR | Abbreviation | abbrev |

---

### geneea.bod_stav
**Meaning**: Status/state codes for agenda items.
**Synonyms**: agenda status, item status, point status

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_bod_stav` | BIGINT | Status identifier | status ID |
| `popis` | VARCHAR | Status description | status, description |

**Enumerated values** (exact):
- `projednán` (discussed/processed)
- `neprojednán` (not discussed)
- `přerušen` (interrupted)
- `neprojednatelný` (not discussable)
- `právě projednávaný` (currently being discussed)
- `jiz projednan` (already discussed)
- `odročen` (postponed)

---

### geneea.funkce
**Meaning**: Specific function/role assignments within organizations (clubs, committees).
**Synonyms**: role, position, function assignment

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_funkce` | BIGINT | Unique function identifier | function ID, role ID |
| `id_organ` | BIGINT | Foreign key to organization | organization ID, organ ID |
| `id_typ_funkce` | BIGINT | Foreign key to function type | function type ID |
| `nazev_funkce_cz` | VARCHAR | Czech name of function | function name, role name |
| `priorita` | BIGINT | Priority/rank order | priority, rank |

---

### geneea.hl_check
**Meaning**: Validation/check records for voting sessions; tracks voting round metadata.
**Synonyms**: voting check, vote validation, voting metadata

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_hlasovani` | BIGINT | Foreign key to voting session | voting ID, vote ID |
| `turn` | BIGINT | Round/turn number | round, turn number |
| `mode` | BIGINT | Mode/type code | mode, type |
| `id_h2` | VARCHAR | Related voting ID 2 | related vote 2 |
| `id_h3` | VARCHAR | Related voting ID 3 | related vote 3 |

---

### geneea.hl_hlasovani
**Meaning**: Voting sessions/records; individual votes held in parliament.
**Synonyms**: vote, voting session, ballot, roll call

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_hlasovani` | BIGINT | Unique voting session identifier | vote ID, voting ID |
| `id_organ` | BIGINT | Foreign key to organization | organization ID, organ ID |
| `schuze` | BIGINT | Session number | session number |
| `cislo` | BIGINT | Vote number within session | vote number |
| `bod` | BIGINT | Agenda item number | agenda item, point |
| `datum` | DATE | Date of vote | date, voting date |
| `cas` | TIME | Time of vote | time, voting time |
| `pro` | BIGINT | Count of votes in favor | votes for, yes votes |
| `proti` | BIGINT | Count of votes against | votes against, no votes |
| `zdrzel` | BIGINT | Count of abstentions | abstain, abstentions |
| `nehlasoval` | BIGINT | Count of non-voters | did not vote, absent |
| `prihlaseno` | BIGINT | Total registered/present | registered, present |
| `kvorum` | BIGINT | Quorum requirement | quorum |
| `druh_hlasovani` | VARCHAR | Type of voting | voting type |
| `vysledek` | VARCHAR | Result (A=approved, R=rejected) | result, outcome |
| `nazev_dlouhy` | VARCHAR | Long name/description of vote | long name, description |
| `nazev_kratky` | VARCHAR | Short name/abbreviation | short name, abbrev |

**Enumerated values** (exact):
- `vysledek`: `A` (approved/accepted), `R` (rejected/refused)
- `druh_hlasovani`: `N`

---

### geneea.hl_poslanec
**Meaning**: Individual deputy voting records; how each deputy voted on each vote.
**Synonyms**: deputy vote, individual vote, member vote

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_poslanec` | BIGINT | Foreign key to deputy | deputy ID, member ID |
| `id_hlasovani` | BIGINT | Foreign key to voting session | vote ID, voting ID |
| `vysledek` | VARCHAR | Individual vote result | vote result, result |

**Enumerated values** (exact):
- `A` (approved/yes)
- `B` (against/no)
- `K` (abstain)
- `W` (did not vote/absent)
- `@` (special code, unclear meaning)

---

### geneea.hl_vazby
**Meaning**: Relationships/dependencies between voting sessions.
**Synonyms**: vote relationship, voting link, vote dependency

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_hlasovani` | BIGINT | Foreign key to voting session | vote ID, voting ID |
| `turn` | BIGINT | Turn/round number | turn, round |
| `typ` | BIGINT | Relationship type code | type, relationship type |

---

### geneea.hl_zposlanec
**Meaning**: Excluded/absent deputies for voting sessions; records deputies not participating in a vote.
**Synonyms**: absent deputy, excluded deputy, non-voting deputy

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_hlasovani` | BIGINT | Foreign key to voting session | vote ID, voting ID |
| `id_osoba` | BIGINT | Foreign key to person | person ID |
| `mode` | BIGINT | Absence mode/reason code | mode, reason |

---

### geneea.omluvy
**Meaning**: Excuses/apologies; records of deputy absences with reasons.
**Synonyms**: absence, excuse, apology, leave

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_organ` | BIGINT | Foreign key to organization | organization ID, organ ID |
| `id_poslanec` | BIGINT | Foreign key to deputy | deputy ID, member ID |
| `den` | VARCHAR | Date of absence (DD.MM.YYYY format) | date, day |
| `od` | VARCHAR | Start time | from time, start |
| `do` | VARCHAR | End time | to time, end |

---

### geneea.organy
**Meaning**: Organizations/bodies (parliamentary clubs, committees, commissions, etc.).
**Synonyms**: organization, body, organ, committee, club, commission

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_organ` | BIGINT | Unique organization identifier | organization ID, organ ID |
| `organ_id_organ` | BIGINT | Parent organization ID (hierarchical) | parent organ ID |
| `id_typ_organu` | BIGINT | Foreign key to organization type | type ID, org type ID |
| `zkratka` | VARCHAR | Abbreviation/acronym | abbrev, acronym |
| `nazev_organu_cz` | VARCHAR | Czech name of organization | name, organization name |
| `nazev_organu_en` | VARCHAR | English name of organization | English name |
| `od_organ` | VARCHAR | Start date (YYYY-MM-DD format) | from date, start date |
| `do_organ` | VARCHAR | End date (YYYY-MM-DD format) | to date, end date |
| `priorita` | VARCHAR | Priority/rank | priority, rank |
| `cl_organ_base` | BIGINT | Base member count | base members, member count |

---

### geneea.osoby
**Meaning**: Persons/individuals; biographical data for all people in the system.
**Synonyms**: person, individual, deputy, member, person record

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_osoba` | BIGINT | Unique person identifier | person ID |
| `pred` | VARCHAR | Title/prefix (e.g., "Ing.", "Dr.") | title, prefix |
| `jmeno` | VARCHAR | First name | first name, given name |
| `prijmeni` | VARCHAR | Last name/surname | last name, surname, family name |
| `za` | VARCHAR | "Za" field (unclear purpose, typically NULL) | za |
| `narozeni` | VARCHAR | Birth date (DD.MM.YYYY format) | birth date, DOB |
| `pohlavi` | VARCHAR | Gender (M=male, Z/Ž=female) | gender, sex |
| `zmena` | VARCHAR | Change/modification date | change date, modification |
| `umrti` | VARCHAR | Death date | death date, died |

**Enumerated values** (exact):
- `pohlavi`: `M` (male), `Z` (female), `Ž` (female)

---

### geneea.pkgps
**Meaning**: GPS coordinates and addresses for deputies.
**Synonyms**: deputy address, GPS location, coordinates

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_poslanec` | BIGINT | Foreign key to deputy | deputy ID, member ID |
| `adresa` | VARCHAR | Full address | address |
| `sirka` | DOUBLE | Latitude coordinate | latitude |
| `delka` | DOUBLE | Longitude coordinate | longitude |

---

### geneea.poslanec
**Meaning**: Deputies/members of parliament; contact and biographical information.
**Synonyms**: deputy, member, MP, parliament member

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_poslanec` | BIGINT | Unique deputy identifier | deputy ID, member ID |
| `id_osoba` | BIGINT | Foreign key to person | person ID |
| `id_kraj` | BIGINT | District/region ID | district ID, region ID |
| `id_kandidatka` | BIGINT | Candidate list ID | candidate ID, list ID |
| `id_obdobi` | BIGINT | Period/term ID | period ID, term ID |
| `web` | VARCHAR | Website URL | website, web |
| `ulice` | VARCHAR | Street address | street, address |
| `obec` | VARCHAR | Municipality/city | city, municipality |
| `psc` | VARCHAR | Postal code | postal code, zip |
| `email` | VARCHAR | Email address | email |
| `telefon` | VARCHAR | Phone number | phone, telephone |
| `fax` | VARCHAR | Fax number | fax |
| `psp_telefon` | VARCHAR | Parliament office phone | office phone, PSP phone |
| `facebook` | VARCHAR | Facebook profile | facebook |
| `foto` | BIGINT | Photo ID/flag | photo, photo ID |

---

### geneea.schuze
**Meaning**: Parliamentary sessions; scheduled meetings of parliament.
**Synonyms**: session, meeting, sitting, parliament session

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_schuze` | BIGINT | Unique session identifier | session ID |
| `id_organ` | BIGINT | Foreign key to organization | organization ID, organ ID |
| `schuze` | BIGINT | Session number | session number |
| `od_schuze` | VARCHAR | Session start (YYYY-MM-DD HH format) | start date, from date |
| `do_schuze` | VARCHAR | Session end (YYYY-MM-DD HH format) | end date, to date |
| `aktualizace` | VARCHAR | Last update timestamp | update, last updated |

---

### geneea.schuze_stav
**Meaning**: Status/state records for sessions; tracks session state changes and special events.
**Synonyms**: session status, session state, session event

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_schuze` | BIGINT | Foreign key to session | session ID |
| `stav` | BIGINT | State code | state, status |
| `typ` | VARCHAR | Type code (1 or 2) | type |
| `text_dt` | VARCHAR | Date/time text | date text, time text |
| `text_st` | VARCHAR | Status text description | status text, description |
| `tm_line` | VARCHAR | Timeline/summary line | timeline, summary |

**Enumerated values** (exact) for `text_st`:
- `nedůvěra vládě nebyla vyslovena` (no-confidence not passed)
- `návrh na vyslovení nedůvěry vládě ČR` (no-confidence proposal)
- `návrh na vyslovení nedůvěry vládě ČR nebyl schválen` (no-confidence not approved)
- `návrh prezidentu republiky na rozpuštění PS` (dissolution proposal)
- `projednávání návrhů ve stavu legislativní nouze` (emergency legislation)
- `přerušeno` (interrupted)
- `přerušeno do středy 25. listopadu do 9 hodin` (interrupted until specific date/time)
- `volba veřejného ochránce práv` (ombudsman election)
- `vyslovena důvěra vládě ČR` (confidence in government passed)
- `žádost o svolání schůze byla stažena` (session request withdrawn)
- `žádost vlády o vyslovení důvěry` (government confidence request)
- `žádost vlády ČR o vyslovení důvěry` (government confidence request)
- `žádost vlády ČR o vyslovení důvěry - vyslovena` (government confidence passed)

---

### geneea.typ_funkce
**Meaning**: Function/role types; definitions of possible roles in organizations.
**Synonyms**: role type, function type, position type

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_typ_funkce` | BIGINT | Unique function type identifier | function type ID |
| `i