# Geneea Schema Reference Guide

## Schema Summary
This schema contains Czech parliamentary data: deputies (poslanec), voting records (hl_hlasovani), parliamentary bodies (organy), sessions (schuze), and agenda items (bod_schuze), spanning multiple legislative periods.

---

## Join Paths

**Deputy to person details:**
```sql
FROM geneea.poslanec p
JOIN geneea.osoby o ON p.id_osoba = o.id_osoba
```

**Voting record to individual deputy votes:**
```sql
FROM geneea.hl_hlasovani hh
JOIN geneea.hl_poslanec hp ON hh.id_hlasovani = hp.id_hlasovani
JOIN geneea.poslanec p ON hp.id_poslanec = p.id_poslanec
```

**Deputy to organizational roles:**
```sql
FROM geneea.poslanec p
JOIN geneea.zarazeni z ON p.id_osoba = z.id_osoba
JOIN geneea.funkce f ON z.id_of = f.id_organ AND z.cl_funkce = f.id_funkce
JOIN geneea.organy org ON f.id_organ = org.id_organ
```

**Session to agenda items:**
```sql
FROM geneea.schuze s
JOIN geneea.bod_schuze bs ON s.id_schuze = bs.id_schuze
```

**Voting to session and agenda:**
```sql
FROM geneea.hl_hlasovani hh
JOIN geneea.schuze s ON hh.schuze = s.schuze AND hh.id_organ = s.id_organ
JOIN geneea.bod_schuze bs ON hh.bod = bs.bod AND s.id_schuze = bs.id_schuze
```

**Deputy absence records:**
```sql
FROM geneea.poslanec p
JOIN geneea.omluvy om ON p.id_poslanec = om.id_poslanec
```

---

## Table Reference

### `geneea.bod_schuze`
Agenda items (body) within parliamentary sessions.

| Column | Semantics |
|--------|-----------|
| `id_bod` | Unique agenda item identifier |
| `id_schuze` | Session reference |
| `id_tisk` | Document/bill reference (often NULL) |
| `id_typ` | Item type code: `0, 1, 2, 3, 4, 5, 6, 7, 10, 13, 14, 18, 43, 54` |
| `bod` | Sequence number within session |
| `uplny_naz` | Full title of agenda item |
| `uplny_kon` | Full conclusion/outcome text |
| `id_bod_stav` | Status reference (→ `geneea.bod_stav.id_bod_stav`) |
| `pozvanka` | Invitation flag: `0` (no), `1` (yes) |
| `rj` | Regulatory jurisdiction: `0, 1, 2` |
| `druh_bodu` | Item type category: `0, 1, 2, 3` |

### `geneea.bod_stav`
Agenda item status codes.

| Column | Values |
|--------|--------|
| `id_bod_stav` | `0` (projednán), `1` (neprojednán), `2` (přerušen), `3` (neprojednatelný), `4` (právě projednávaný) |
| `popis` | Status description |

### `geneea.hl_hlasovani`
Voting records (roll calls) in parliamentary sessions.

| Column | Semantics |
|--------|-----------|
| `id_hlasovani` | Unique voting record identifier |
| `id_organ` | Voting body (usually 171 for Chamber of Deputies) |
| `schuze` | Session number |
| `cislo` | Vote sequence number within session |
| `bod` | Agenda item number |
| `datum` | Vote date |
| `cas` | Vote time |
| `pro` | Count voting FOR |
| `proti` | Count voting AGAINST |
| `zdrzel` | Count ABSTAINING |
| `nehlasoval` | Count NOT VOTING |
| `prihlaseno` | Total present |
| `kvorum` | Quorum required |
| `druh_hlasovani` | Vote type: `N` (standard) |
| `vysledek` | Result: `A` (approved), `R` (rejected) |
| `nazev_dlouhy` | Full vote description |
| `nazev_kratky` | Short vote description |

### `geneea.hl_poslanec`
Individual deputy votes within a voting record.

| Column | Semantics |
|--------|-----------|
| `id_poslanec` | Deputy identifier (→ `geneea.poslanec.id_poslanec`) |
| `id_hlasovani` | Voting record reference |
| `vysledek` | Vote cast: `A` (for), `B` (against), `K` (abstain), `W` (absent), `@` (other) |

### `geneea.hl_zposlanec`
Excluded/substitute deputies in voting records.

| Column | Semantics |
|--------|-----------|
| `id_hlasovani` | Voting record reference |
| `id_osoba` | Person identifier (→ `geneea.osoby.id_osoba`) |
| `mode` | Exclusion mode: `0` (substitute), `1` (excluded) |

### `geneea.hl_check`
Voting record validation/linking metadata.

| Column | Semantics |
|--------|-----------|
| `id_hlasovani` | Voting record reference |
| `turn` | Turn/round number |
| `mode` | Check mode |
| `id_h2`, `id_h3` | Related voting record IDs (often NULL) |

### `geneea.hl_vazby`
Voting record relationships/dependencies.

| Column | Semantics |
|--------|-----------|
| `id_hlasovani` | Voting record reference |
| `turn` | Turn number |
| `typ` | Relationship type |

### `geneea.zmatecne`
Flagged/disputed voting records.

| Column | Semantics |
|--------|-----------|
| `id_hlasovani` | Voting record marked as disputed |

### `geneea.schuze`
Parliamentary sessions.

| Column | Semantics |
|--------|-----------|
| `id_schuze` | Unique session identifier |
| `id_organ` | Governing body (usually 166 for Chamber of Deputies) |
| `schuze` | Session sequence number |
| `od_schuze` | Session start date/time |
| `do_schuze` | Session end date/time |
| `aktualizace` | Last update timestamp |

### `geneea.schuze_stav`
Session status and special events.

| Column | Semantics |
|--------|-----------|
| `id_schuze` | Session reference |
| `stav` | Status code |
| `typ` | Event type: `1`, `2` |
| `text_st` | Status text (e.g., "vyslovena důvěra vládě ČR", "přerušeno", "žádost o svolání schůze byla stažena") |
| `tm_line` | Timeline note |

### `geneea.poslanec`
Deputy records linking persons to parliamentary periods.

| Column | Semantics |
|--------|-----------|
| `id_poslanec` | Unique deputy identifier |
| `id_osoba` | Person reference (→ `geneea.osoby.id_osoba`) |
| `id_kraj` | District/region code |
| `id_kandidatka` | Candidate list reference |
| `id_obdobi` | Legislative period identifier |
| `web`, `ulice`, `obec`, `psc`, `email`, `telefon`, `fax`, `psp_telefon`, `facebook` | Contact details (mostly `\` for missing) |
| `foto` | Photo flag |

### `geneea.osoby`
Person master data.

| Column | Semantics |
|--------|-----------|
| `id_osoba` | Unique person identifier |
| `pred` | Title/prefix (e.g., "Ing.", "Dr.") |
| `jmeno` | First name |
| `prijmeni` | Surname |
| `za` | Suffix/particle |
| `narozeni` | Birth date |
| `pohlavi` | Gender: `M` (male), `Z` or `Ž` (female) |
| `zmena` | Name change date |
| `umrti` | Death date |

### `geneea.zarazeni`
Deputy assignments to organizations and roles.

| Column | Semantics |
|--------|-----------|
| `id_osoba` | Person reference |
| `id_of` | Organization reference (→ `geneea.organy.id_organ`) |
| `cl_funkce` | Function/role code within organization |
| `od_o` | Organization assignment start date |
| `do_o` | Organization assignment end date |
| `od_f` | Function assignment start date |
| `do_f` | Function assignment end date |

### `geneea.funkce`
Defined roles within organizations.

| Column | Semantics |
|--------|-----------|
| `id_funkce` | Unique role identifier |
| `id_organ` | Organization reference |
| `id_typ_funkce` | Role type reference (→ `geneea.typ_funkce.id_typ_funkce`) |
| `nazev_funkce_cz` | Role name in Czech |
| `priorita` | Display priority (lower = higher priority) |

### `geneea.typ_funkce`
Role type definitions.

| Column | Semantics |
|--------|-----------|
| `id_typ_funkce` | Unique role type identifier |
| `id_typ_org` | Organization type scope |
| `typ_funkce_cz` | Role type name (Czech) |
| `typ_funkce_en` | Role type name (English): "Chairman", "Vice-chairman", "Member", "President", "Secretary", "Verifier", etc. |
| `priorita` | Display priority |
| `typ_funkce_obecny` | Generic role category |

### `geneea.organy`
Parliamentary and political organizations (clubs, committees, delegations).

| Column | Semantics |
|--------|-----------|
| `id_organ` | Unique organization identifier |
| `organ_id_organ` | Parent organization reference |
| `id_typ_organu` | Organization type (→ `geneea.typ_organu.id_typ_org`) |
| `zkratka` | Abbreviation (e.g., "ČSSD", "ČMSS") |
| `nazev_organu_cz` | Organization name (Czech) |
| `nazev_organu_en` | Organization name (English) |
| `od_organ` | Organization start date |
| `do_organ` | Organization end date |
| `cl_organ_base` | Base member count |

### `geneea.typ_organu`
Organization type definitions.

| Column | Semantics |
|--------|-----------|
| `id_typ_org` | Unique organization type identifier |
| `nazev_typ_org_cz` | Type name (Czech): "Klub", "Komise", "Výbor", "Podvýbor", "Vláda", etc. |
| `nazev_typ_org_en` | Type name (English): "Political Group", "Commission", "Committee", "Subcommittee", "Government", etc. |
| `typ_org_obecny` | Generic category: `0, 1, 2, 3, 7` |
| `priorita` | Display priority |

### `geneea.omluvy`
Deputy absence/excuse records.

| Column | Semantics |
|--------|-----------|
| `id_organ` | Organization reference |
| `id_poslanec` | Deputy reference |
| `den` | Absence date (format: DD.MM.YYYY) |
| `od` | Absence start time |
| `do` | Absence end time |

### `geneea.pkgps`
Deputy geographic coordinates and address.

| Column | Semantics |
|--------|-----------|
| `id_poslanec` | Deputy reference |
| `adresa` | Full address string |
| `sirka` | Latitude (WGS84) |
| `delka` | Longitude (WGS84) |

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| Deputy / MP / Representative | `geneea.poslanec` |
| Person / Individual | `geneea.osoby` |
| Vote / Roll call / Voting record | `geneea.hl_hlasovani` |
| Individual vote / Vote cast | `geneea.hl_poslanec.vysledek` |
| Session / Meeting | `geneea.schuze` |
| Agenda item / Agenda point / Body | `geneea.bod_schuze` |
| Organization / Club / Committee / Body | `geneea.organy` |
| Role / Function / Position | `geneea.funkce` |
| Assignment / Membership | `geneea.zarazeni` |
| Absence / Excuse / Apology | `geneea.omluvy` |
| Approved / Passed | `geneea.hl_hlasovani.vysledek = 'A'` |
| Rejected / Failed | `geneea.hl_hlasovani.vysledek = 'R'` |
| For / Voted yes | `geneea.hl_poslanec.vysledek = 'A'` |
| Against / Voted no | `geneea.hl_poslanec.vysledek = 'B'` |
| Abstain / Abstained | `geneea.hl_poslanec.vysledek = 'K'` |
| Absent / Did not vote | `geneea.hl_poslanec.vysledek = 'W'` |
| Disputed / Flagged vote | `geneea.zmatecne.id_hlasovani` |