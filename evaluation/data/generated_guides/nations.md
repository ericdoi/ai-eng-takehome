# Nations Schema Reference Guide

## Schema Summary
This schema contains geopolitical and socioeconomic data for 14 countries, including bilateral relations between nations and comprehensive statistics on economic, social, political, and military indicators.

---

## Join Paths

**Country to relations (bilateral):**
```sql
SELECT c1.country, c2.country, r.relation, r.value
FROM nations.country c1
JOIN nations.relation r ON c1.country_id = r.nation_id1
JOIN nations.country c2 ON c2.country_id = r.nation_id2
```

**Country to statistics:**
```sql
SELECT c.country, s.*
FROM nations.country c
JOIN nations.stat s ON c.country_id = s.country_id
```

---

## Table Reference

### `nations.country`
Country master list. Synonym: nation.

| Column | Semantics |
|--------|-----------|
| `country_id` | Primary key; used to join `relation` and `stat` tables |
| `country` | Country name. Values: 'Brazil', 'Burma', 'China', 'Cuba', 'Egypt', 'India', 'Indonesia', 'Israel', 'Jordan', 'Netherlands', 'Poland', 'UK', 'USA', 'USSR' |

---

### `nations.relation`
Bilateral relations between country pairs. Represents directed edges from `nation_id1` → `nation_id2`.

| Column | Semantics |
|--------|-----------|
| `nation_id1` | Source country ID; foreign key to `nations.country.country_id` |
| `nation_id2` | Target country ID; foreign key to `nations.country.country_id` |
| `relation` | Relation type. Examples: 'accusation', 'aidenemy', 'attackembassy', 'blockpositionindex', 'booktranslations' |
| `value` | Relation magnitude or count; often NULL |

---

### `nations.stat`
Comprehensive country statistics across 112 dimensions. One row per country.

| Column | Semantics |
|--------|-----------|
| `country_id` | Foreign key to `nations.country.country_id` |
| **Economic** | `GNP`, `export`, `exports`, `imports`, `investments`, `economicaidtaken`, `techassistancetaken`, `usaidreceived`, `IFCandIBRD`, `balancepayments`, `balanceinvestments`, `unpaymentdelinq` |
| **Population & Demographics** | `popabs` (absolute population), `popn/land` (population density), `agriculturalpop`, `age`, `immigrants/migrants`, `emigrants`, `femaleworkers`, `unemployed` |
| **Military & Defense** | `militarypersonnel`, `defenseexpabs`, `militaryaction` |
| **Conflict & Violence** | `killedforeignviolence`, `killeddomesticviolence`, `threats`, `accusations`, `protests`, `riots`, `purges`, `demonstrations`, `assassinations`, `majgovcrisis` |
| **Infrastructure** | `telephone`, `roadlength`, `railroadlength`, `airdistance`, `runningwater`, `seabornegoods` |
| **Resources & Environment** | `energyconsume`, `popxenergabs`, `rainfall`, `arable`, `area` |
| **Health & Nutrition** | `caloriesconsumed`, `protein` |
| **Education** | `primaryschool`, `goveducationspend`, `foreigncollegestud` |
| **Religion & Culture** | `catholics`, `religions`, `largestrelgn`, `religioustitles`, `englishtitles`, `russiantitles`, `artsculturengo` |
| **Language & Ethnicity** | `languages`, `largestlang`, `ethnicgrps`, `largestethnic` |
| **Governance** | `monarchy`, `politicalparties`, `communistparty`, `govspending`, `noncommunist`, `govchangelegal0/1/2`, `legitgov0/1`, `systemstyle0/1/2`, `constitutional0/1/2`, `electoralsystem0/1/2`, `politicalleadership0/1/2`, `horizontalpower0/2`, `military0/1/2`, `bureaucracy0/1/2`, `censorship0/1/2` |
| **Bloc Membership** | `blocmembership0/1/2`, `neutralblock` |
| **Freedom & Opposition** | `freedomofopposition0/1/2` |
| **NGOs & International** | `medicinengo`, `lawngos`, `diplomatexpelled`, `foreignmail` |
| **Geography** | `geographyx`, `geographyy`, `geographyz` (coordinate system) |
| **Literacy** | `illiterates` |

Columns suffixed `0`, `1`, `2` represent categorical encodings (e.g., governance system types). Many cells contain NULL.

---

## Synonym Glossary

| Question Term | Schema Reference |
|---|---|
| country pair, bilateral relation | `nations.relation` |
| nation, state | `nations.country` |
| military spending | `nations.stat.defenseexpabs` |
| population | `nations.stat.popabs` |
| economic output | `nations.stat.GNP` |
| trade | `nations.stat.exports`, `nations.stat.imports` |
| conflict events | `nations.stat.militaryaction`, `nations.stat.killedforeignviolence` |
| political system | `nations.stat.systemstyle0/1/2`, `nations.stat.constitutional0/1/2` |
| bloc alignment | `nations.stat.blocmembership0/1/2` |