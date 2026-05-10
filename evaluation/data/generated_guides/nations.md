# Nations Schema Reference Guide

## Schema Summary
The `nations` schema contains geopolitical, economic, and social statistics for 14 countries during a Cold War-era period, including country identifiers, bilateral relations between nations, and comprehensive country-level metrics.

---

## Table Reference

### Table: `nations.country`
**Meaning:** Country master data; lookup table for country identifiers and names.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `country_id` | BIGINT | Unique country identifier | nation_id, country code |
| `country` | VARCHAR | Country name | nation, country_name |

**Notable Values (exact strings):**
`'Brazil'`, `'Burma'`, `'China'`, `'Cuba'`, `'Egypt'`, `'India'`, `'Indonesia'`, `'Israel'`, `'Jordan'`, `'Netherlands'`, `'Poland'`, `'UK'`, `'USA'`, `'USSR'`

---

### Table: `nations.relation`
**Meaning:** Bilateral relations between pairs of countries; records directed relationships and interactions between two nations.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `nation_id1` | BIGINT | First country in relation (from country_id) | source_country_id, country1_id |
| `nation_id2` | BIGINT | Second country in relation (from country_id) | target_country_id, country2_id |
| `relation` | VARCHAR | Type of bilateral relation or interaction | relation_type, interaction_type |
| `value` | BIGINT | Numeric value or count associated with relation | relation_value, count |

**Notable Relation Types (from sample data):**
`'accusation'`, `'aidenemy'`, `'attackembassy'`, `'blockpositionindex'`, `'booktranslations'`

---

### Table: `nations.stat`
**Meaning:** Comprehensive country-level statistics covering demographics, economics, military, politics, geography, and social indicators for each country.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `country_id` | BIGINT | Country identifier (from country_id) | nation_id |
| `telephone` | BIGINT | Telephone infrastructure metric | phones, telephone_count |
| `agriculturalpop` | BIGINT | Agricultural population count or percentage | farm_pop, agricultural_workers |
| `energyconsume` | BIGINT | Energy consumption metric | energy_use, power_consumption |
| `illiterates` | BIGINT | Illiterate population count | illiteracy_count, non_literate |
| `GNP` | BIGINT | Gross National Product | gnp_value, national_product |
| `popxenergabs` | BIGINT | Population times energy absolute value | pop_energy_product |
| `incomeabs` | BIGINT | Income absolute value | income_total, total_income |
| `popabs` | BIGINT | Population absolute value | population, total_pop |
| `unassessment` | BIGINT | UN assessment or contribution | un_contribution, un_payment |
| `defenseexpabs` | BIGINT | Defense expenditure absolute value | military_spending, defense_budget |
| `englishtitles` | BIGINT | Count of English-language titles or publications | english_pubs, english_works |
| `blocmembership0` | BIGINT | Bloc membership indicator (base/reference) | bloc_member, alliance_status |
| `usaidreceived` | BIGINT | US aid received | us_assistance, american_aid |
| `freedomofopposition0` | BIGINT | Freedom of opposition indicator (base) | opposition_freedom, political_freedom |
| `IFCandIBRD` | BIGINT | International Finance Corporation and IBRD membership/participation | world_bank_status |
| `threats` | BIGINT | Count of threats received or issued | threat_count |
| `accusations` | BIGINT | Count of accusations | accusation_count |
| `killedforeignviolence` | BIGINT | Deaths from foreign violence | foreign_deaths, killed_by_foreign |
| `militaryaction` | BIGINT | Military action count or indicator | military_incidents, combat_actions |
| `protests` | BIGINT | Protest count | protest_count, demonstrations_count |
| `killeddomesticviolence` | BIGINT | Deaths from domestic violence | domestic_deaths, killed_by_domestic |
| `riots` | BIGINT | Riot count | riot_count |
| `purges` | BIGINT | Political purge count | purge_count |
| `demonstrations` | BIGINT | Demonstration count | demo_count |
| `catholics` | BIGINT | Catholic population count or percentage | catholic_pop |
| `airdistance` | BIGINT | Air distance metric | air_miles, flight_distance |
| `medicinengo` | BIGINT | Medicine-related NGO count or indicator | health_ngo, medical_organizations |
| `diplomatexpelled` | BIGINT | Diplomats expelled count | expelled_diplomats, diplomatic_incidents |
| `divorces` | BIGINT | Divorce count | divorce_count |
| `popn/land` | BIGINT | Population per land area (population density) | population_density, pop_per_area |
| `arable` | BIGINT | Arable land area or percentage | arable_land, farmable_land |
| `area` | BIGINT | Total country area | land_area, total_area |
| `roadlength` | BIGINT | Total road length | roads, road_network |
| `railroadlength` | BIGINT | Total railroad length | railways, rail_network |
| `religions` | BIGINT | Count of religions present | religion_count, religious_groups |
| `immigrants/migrants` | BIGINT | Immigrant or migrant population count | immigration, migration_count |
| `rainfall` | BIGINT | Annual rainfall metric | precipitation, rain_amount |
| `largestrelgn` | BIGINT | Largest religion population count or percentage | dominant_religion, major_religion |
| `runningwater` | BIGINT | Running water access count or percentage | water_access, clean_water |
| `foreigncollegestud` | BIGINT | Foreign college students count | international_students, foreign_students |
| `neutralblock` | BIGINT | Neutral bloc membership indicator | non_aligned, neutral_status |
| `age` | BIGINT | Median or average age | median_age, avg_age |
| `religioustitles` | BIGINT | Religious titles or publications count | religious_works, religious_pubs |
| `emigrants` | BIGINT | Emigrant population count | emigration_count, people_leaving |
| `seabornegoods` | BIGINT | Seaborne goods trade volume | maritime_trade, sea_trade |
| `lawngos` | BIGINT | Law-related NGO count | legal_organizations, law_ngo |
| `unemployed` | BIGINT | Unemployed population count or percentage | unemployment, jobless |
| `export` | BIGINT | Export value or count | exports_value, trade_exports |
| `languages` | BIGINT | Count of languages spoken | language_count, linguistic_diversity |
| `largestlang` | BIGINT | Largest language speaker population count or percentage | dominant_language, major_language |
| `ethnicgrps` | BIGINT | Count of ethnic groups | ethnic_diversity, ethnic_groups_count |
| `economicaidtaken` | BIGINT | Economic aid received | aid_received, economic_assistance |
| `techassistancetaken` | BIGINT | Technical assistance received | tech_aid, technical_support |
| `goveducationspend` | BIGINT | Government education spending | education_budget, school_spending |
| `femaleworkers` | BIGINT | Female workforce count or percentage | women_workers, female_employment |
| `exports` | BIGINT | Export value or count (alternate) | export_value, trade_exports |
| `foreignmail` | BIGINT | Foreign mail volume | international_mail, mail_traffic |
| `imports` | BIGINT | Import value or count | import_value, trade_imports |
| `caloriesconsumed` | BIGINT | Average calories consumed per capita | caloric_intake, food_consumption |
| `protein` | BIGINT | Average protein consumption | protein_intake, nutrition |
| `russiantitles` | BIGINT | Russian-language titles or publications count | russian_pubs, russian_works |
| `militarypersonnel` | BIGINT | Military personnel count | armed_forces, military_size |
| `investments` | BIGINT | Foreign investment value or count | investment_inflow, capital_investment |
| `politicalparties` | BIGINT | Count of political parties | party_count, num_parties |
| `artsculturengo` | BIGINT | Arts and culture NGO count | cultural_organizations, arts_ngo |
| `communistparty` | BIGINT | Communist party membership or indicator | communist_members, communist_status |
| `govspending` | BIGINT | Government spending total | government_budget, total_spending |
| `monarchy` | BIGINT | Monarchy indicator or status | royal_status, monarchical_rule |
| `primaryschool` | BIGINT | Primary school enrollment or count | elementary_school, primary_education |
| `govchangelegal0` | BIGINT | Government change via legal means indicator (base) | legal_transition, constitutional_change |
| `legitgov0` | BIGINT | Legitimate government indicator (base) | government_legitimacy, legit_status |
| `largestethnic` | BIGINT | Largest ethnic group population count or percentage | dominant_ethnic, major_ethnic_group |
| `assassinations` | BIGINT | Assassination count | assassination_count, political_murders |
| `majgovcrisis` | BIGINT | Major government crisis count | gov_crisis_count, political_crisis |
| `unpaymentdelinq` | BIGINT | UN payment delinquency indicator | un_debt, payment_default |
| `balancepayments` | BIGINT | Balance of payments value | payment_balance, trade_balance |
| `balanceinvestments` | BIGINT | Balance of investments value | investment_balance |
| `systemstyle0` | BIGINT | Government system style indicator (base) | gov_system, political_system |
| `constitutional0` | BIGINT | Constitutional status indicator (base) | constitutional_status, constitution_type |
| `electoralsystem0` | BIGINT | Electoral system indicator (base) | election_system, voting_system |
| `noncommunist` | BIGINT | Non-communist indicator or status | anti_communist, non_communist_status |
| `politicalleadership0` | BIGINT | Political leadership type indicator (base) | leadership_style, leader_type |
| `horizontalpower0` | BIGINT | Horizontal power distribution indicator (base) | power_distribution, separation_of_powers |
| `military0` | BIGINT | Military influence indicator (base) | military_influence, military_power |
| `bureaucracy0` | BIGINT | Bureaucracy strength indicator (base) | bureaucratic_power, admin_strength |
| `censorship0` | BIGINT | Censorship level indicator (base) | censorship_level, press_freedom |
| `geographyx` | BIGINT | Geographic coordinate X | longitude, geo_x |
| `geographyy` | BIGINT | Geographic coordinate Y | latitude, geo_y |
| `geographyz` | BIGINT | Geographic coordinate Z | altitude, geo_z |
| `blocmembership1` | BIGINT | Bloc membership indicator (variant 1) | bloc_member_alt1 |
| `blocmembership2` | BIGINT | Bloc membership indicator (variant 2) | bloc_member_alt2 |
| `freedomofopposition1` | BIGINT | Freedom of opposition indicator (variant 1) | opposition_freedom_alt1 |
| `freedomofopposition2` | BIGINT | Freedom of opposition indicator (variant 2) | opposition_freedom_alt2 |
| `govchangelegal1` | BIGINT | Government change via legal means (variant 1) | legal_transition_alt1 |
| `govchangelegal2` | BIGINT | Government change via legal means (variant 2) | legal_transition_alt2 |
| `legitgov1` | BIGINT | Legitimate government indicator (variant 1) | legit_status_alt1 |
| `systemstyle1` | BIGINT | Government system style (variant 1) | gov_system_alt1 |
| `systemstyle2` | BIGINT | Government system style (variant 2) | gov_system_alt2 |
| `constitutional1` | BIGINT | Constitutional status (variant 1) | constitutional_status_alt1 |
| `constitutional2` | BIGINT | Constitutional status (variant 2) | constitutional_status_alt2 |
| `electoralsystem1` | BIGINT | Electoral system (variant 1) | election_system_alt1 |
| `electoralsystem2` | BIGINT | Electoral system (variant 2) | election_system_alt2 |
| `politicalleadership1` | BIGINT | Political leadership type (variant 1) | leadership_style_alt1 |
| `politicalleadership2` | BIGINT | Political leadership type (variant 2) | leadership_style_alt2 |
| `horizontalpower2` | BIGINT | Horizontal power distribution (variant 2) | power_distribution_alt2 |
| `military1` | BIGINT | Military influence (variant 1) | military_influence_alt1 |
| `military2` | BIGINT | Military influence (variant 2) | military_influence_alt2 |
| `bureaucracy1` | BIGINT | Bureaucracy strength (variant 1) | bureaucratic_power_alt1 |
| `bureaucracy2` | BIGINT | Bureaucracy strength (variant 2) | bureaucratic_power_alt2 |
| `censorship1` | BIGINT | Censorship level (variant 1) | censorship_level_alt1 |
| `censorship2` | BIGINT | Censorship level (variant 2) | censorship_level_alt2 |

---

## Join Paths

**Country to Statistics:**
```sql
nations.country c
JOIN nations.stat s ON c.country_id = s.country_id
```

**Country to Relations (as source nation):**
```sql
nations.country c
JOIN nations.relation r ON c.country_id = r.nation_id1
```

**Country to Relations (as target nation):**
```sql
nations.country c
JOIN nations.relation r ON c.country_id = r.nation_id2
```

**Relations with both countries:**
```sql
nations.relation r
JOIN nations.country c1 ON r.nation_id1 = c1.country_id
JOIN nations.country c2 ON r.nation_id2 = c2.country_id
```

**Full country statistics with relations:**
```sql
nations.country c
JOIN nations.stat s ON c.country_id = s.country_id
LEFT JOIN nations.relation r ON c.country_id = r.nation_id1 OR c.country_id = r.nation_id2
```

---

## Business Rules as SQL

No explicit business rules provided in schema documentation. The following are inferred structural constraints:

- **Valid country reference in stat:** `nations.stat.country_id IN (SELECT country_id FROM nations.country)`
- **Valid country references in relation:** `nations.relation.nation_id1 IN (SELECT country_id FROM nations.country) AND nations.relation.nation_id2 IN (SELECT country_id FROM nations.country)`
- **Relation is directional:** `nation_id1` and `nation_id2` are distinct dimensions; `(1, 2)` differs from `(2, 1)`

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| country name | `nations.country.country` |
| country code / nation ID | `nations.country.country_id` |
| bilateral relation | `nations.relation` table |
| relation type | `nations.relation.relation` |
| relation strength / count | `nations.relation.value` |
| country statistics | `nations.stat` table |
| population | `nations.stat.popabs` |
| population density | `nations.stat.popn/land` |
| military size | `nations