# Mondial Schema Reference Guide

## Schema Summary

The Mondial schema contains comprehensive geographic, political, and demographic data for world countries, including borders, cities, natural features (mountains, rivers, lakes, deserts, seas, islands), economic indicators, languages, religions, ethnic groups, and organizational memberships.

---

## Table Reference

### Mondial.borders
**Meaning**: Direct land and maritime borders between countries.
**Synonyms**: country boundaries, shared borders, frontier

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Country1 | VARCHAR | First country code in border pair | country code, nation |
| Country2 | VARCHAR | Second country code in border pair | country code, nation |
| Length | DOUBLE | Border length in kilometers | distance, boundary length |

**Notable values**: Country codes are 1–3 character strings (e.g., 'A', 'CH', 'D', 'USA')

---

### Mondial.city
**Meaning**: Cities and urban areas with population and geographic coordinates.
**Synonyms**: urban center, municipality, town

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Name | VARCHAR | City name | city name, urban area |
| Country | VARCHAR | Country code where city is located | country code, nation |
| Province | VARCHAR | Province/state/region name | state, region, administrative division |
| Population | BIGINT | City population count | inhabitants, residents |
| Longitude | DOUBLE | East-west geographic coordinate | longitude coordinate |
| Latitude | DOUBLE | North-south geographic coordinate | latitude coordinate |

**Notable values**: Population and coordinates may be NULL/NaN

---

### Mondial.continent
**Meaning**: Continental landmasses with total area.
**Synonyms**: world region, landmass

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Name | VARCHAR | Continent name | continent name, region |
| Area | DOUBLE | Total area in square kilometers | total area, landmass area |

**Notable values**: Name ∈ {Africa, America, Asia, Australia/Oceania, Europe}

---

### Mondial.country
**Meaning**: Sovereign and dependent countries with basic attributes.
**Synonyms**: nation, state, territory

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Name | VARCHAR | Country name | country name, nation name |
| Code | VARCHAR | ISO country code (primary key) | country code, ISO code |
| Capital | VARCHAR | Capital city name | capital city |
| Province | VARCHAR | Province where capital is located | capital province |
| Area | DOUBLE | Total country area in square kilometers | total area, land area |
| Population | BIGINT | Total country population | total population, inhabitants |

**Notable values**: Code is 1–3 character string; Area and Population may be NULL

---

### Mondial.desert
**Meaning**: Named deserts with area and location.
**Synonyms**: arid region, wasteland

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Name | VARCHAR | Desert name | desert name |
| Area | DOUBLE | Desert area in square kilometers | area, size |
| Longitude | DOUBLE | Center longitude coordinate | longitude |
| Latitude | DOUBLE | Center latitude coordinate | latitude |

---

### Mondial.economy
**Meaning**: Economic indicators by country.
**Synonyms**: economic data, financial metrics

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Country | VARCHAR | Country code | country code, nation |
| GDP | DOUBLE | Gross Domestic Product in millions USD | gross domestic product |
| Agriculture | DOUBLE | Agriculture sector percentage of GDP | agriculture %, farm sector |
| Service | DOUBLE | Service sector percentage of GDP | service %, tertiary sector |
| Industry | DOUBLE | Industry sector percentage of GDP | industry %, manufacturing |
| Inflation | DOUBLE | Annual inflation rate percentage | inflation rate, price increase |

**Notable values**: All numeric fields may be NULL/NaN

---

### Mondial.encompasses
**Meaning**: Country-to-continent mapping with percentage of country in each continent.
**Synonyms**: country location, continental distribution

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Country | VARCHAR | Country code | country code, nation |
| Continent | VARCHAR | Continent name | continent name, region |
| Percentage | DOUBLE | Percentage of country area in this continent | area percentage, distribution |

**Notable values**: Continent ∈ {Africa, America, Asia, Australia/Oceania, Europe}; Percentage typically 100.0 for single-continent countries

---

### Mondial.ethnicGroup
**Meaning**: Ethnic composition of countries.
**Synonyms**: ethnic demographics, population ethnicity

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Country | VARCHAR | Country code | country code, nation |
| Name | VARCHAR | Ethnic group name | ethnic group, ethnicity |
| Percentage | DOUBLE | Percentage of population in this ethnic group | population percentage, share |

---

### Mondial.geo_desert
**Meaning**: Geographic association of deserts to countries and provinces.
**Synonyms**: desert location, desert geography

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Desert | VARCHAR | Desert name | desert name |
| Country | VARCHAR | Country code where desert is located | country code, nation |
| Province | VARCHAR | Province/region name within country | province, region |

---

### Mondial.geo_estuary
**Meaning**: Geographic association of river estuaries to countries and provinces.
**Synonyms**: estuary location, river mouth geography

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| River | VARCHAR | River name | river name |
| Country | VARCHAR | Country code where estuary is located | country code, nation |
| Province | VARCHAR | Province/region name within country | province, region |

---

### Mondial.geo_island
**Meaning**: Geographic association of islands to countries and provinces.
**Synonyms**: island location, island geography

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Island | VARCHAR | Island name | island name |
| Country | VARCHAR | Country code where island is located | country code, nation |
| Province | VARCHAR | Province/region name within country | province, region |

---

### Mondial.geo_lake
**Meaning**: Geographic association of lakes to countries and provinces.
**Synonyms**: lake location, lake geography

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Lake | VARCHAR | Lake name | lake name |
| Country | VARCHAR | Country code where lake is located | country code, nation |
| Province | VARCHAR | Province/region name within country | province, region |

---

### Mondial.geo_mountain
**Meaning**: Geographic association of mountains to countries and provinces.
**Synonyms**: mountain location, mountain geography

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Mountain | VARCHAR | Mountain name | mountain name |
| Country | VARCHAR | Country code where mountain is located | country code, nation |
| Province | VARCHAR | Province/region name within country | province, region |

---

### Mondial.geo_river
**Meaning**: Geographic association of rivers to countries and provinces.
**Synonyms**: river location, river geography

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| River | VARCHAR | River name | river name |
| Country | VARCHAR | Country code where river is located | country code, nation |
| Province | VARCHAR | Province/region name within country | province, region |

---

### Mondial.geo_sea
**Meaning**: Geographic association of seas to countries and provinces.
**Synonyms**: sea location, sea geography

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Sea | VARCHAR | Sea name | sea name |
| Country | VARCHAR | Country code bordering sea | country code, nation |
| Province | VARCHAR | Province/region name within country | province, region |

---

### Mondial.geo_source
**Meaning**: Geographic association of river sources to countries and provinces.
**Synonyms**: river source location, river origin

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| River | VARCHAR | River name | river name |
| Country | VARCHAR | Country code where river source is located | country code, nation |
| Province | VARCHAR | Province/region name within country | province, region |

---

### Mondial.island
**Meaning**: Named islands with area, height, type, and coordinates.
**Synonyms**: isle, landmass

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Name | VARCHAR | Island name | island name |
| Islands | VARCHAR | Island group/archipelago name | island group, archipelago |
| Area | DOUBLE | Island area in square kilometers | area, size |
| Height | DOUBLE | Maximum elevation in meters | elevation, altitude, peak height |
| Type | VARCHAR | Island formation type | island type, formation |
| Longitude | DOUBLE | Center longitude coordinate | longitude |
| Latitude | DOUBLE | Center latitude coordinate | latitude |

**Notable values**: Type ∈ {atoll, coral, lime, volcanic}; Area, Height, Longitude, Latitude may be NULL/NaN

---

### Mondial.islandIn
**Meaning**: Association of islands with water bodies (seas, lakes, rivers).
**Synonyms**: island water body, island location

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Island | VARCHAR | Island name | island name |
| Sea | VARCHAR | Sea name if island is in sea | sea name |
| Lake | VARCHAR | Lake name if island is in lake | lake name |
| River | VARCHAR | River name if island is in river | river name |

**Notable values**: Lake ∈ {Lake Huron, Lake Manicouagan, Lake Nicaragua, Lake Toba, Ozero Baikal}; exactly one of Sea, Lake, River is non-NULL per row

---

### Mondial.lake
**Meaning**: Named lakes with area, depth, altitude, type, and coordinates.
**Synonyms**: body of water, freshwater lake

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Name | VARCHAR | Lake name | lake name |
| Area | DOUBLE | Lake surface area in square kilometers | area, size |
| Depth | DOUBLE | Maximum depth in meters | depth, maximum depth |
| Altitude | DOUBLE | Lake surface elevation in meters | elevation, altitude |
| Type | VARCHAR | Lake formation or water type | lake type, water type |
| River | VARCHAR | River that feeds or drains lake | river name, outflow |
| Longitude | DOUBLE | Center longitude coordinate | longitude |
| Latitude | DOUBLE | Center latitude coordinate | latitude |

**Notable values**: Type ∈ {acid, artificial, caldera, crater, impact, salt}; all numeric fields may be NULL/NaN

---

### Mondial.language
**Meaning**: Languages spoken in countries with percentage of speakers.
**Synonyms**: spoken language, linguistic data

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Country | VARCHAR | Country code | country code, nation |
| Name | VARCHAR | Language name | language name |
| Percentage | DOUBLE | Percentage of population speaking this language | speaker percentage, share |

---

### Mondial.located
**Meaning**: Association of cities with geographic features (rivers, lakes, seas).
**Synonyms**: city location, geographic feature association

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| City | VARCHAR | City name | city name |
| Province | VARCHAR | Province/region name | province, region |
| Country | VARCHAR | Country code | country code, nation |
| River | VARCHAR | River name if city is on river | river name |
| Lake | VARCHAR | Lake name if city is on lake | lake name |
| Sea | VARCHAR | Sea name if city is on sea | sea name |

**Notable values**: River, Lake, Sea may be NULL or string "None"; typically one geographic feature per city

---

### Mondial.locatedOn
**Meaning**: Association of cities with islands.
**Synonyms**: city island location, island settlement

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| City | VARCHAR | City name | city name |
| Province | VARCHAR | Province/region name | province, region |
| Country | VARCHAR | Country code | country code, nation |
| Island | VARCHAR | Island name where city is located | island name |

---

### Mondial.mergesWith
**Meaning**: Adjacency relationships between seas (which seas connect/merge).
**Synonyms**: sea connection, sea adjacency

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Sea1 | VARCHAR | First sea name | sea name |
| Sea2 | VARCHAR | Second sea name | sea name |

---

### Mondial.mountain
**Meaning**: Named mountains with height, type, and coordinates.
**Synonyms**: peak, summit, mountain range member

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Name | VARCHAR | Mountain name | mountain name |
| Mountains | VARCHAR | Mountain range/group name | mountain range, range |
| Height | DOUBLE | Peak elevation in meters | elevation, altitude, peak height |
| Type | VARCHAR | Mountain formation type | mountain type, formation |
| Longitude | DOUBLE | Peak longitude coordinate | longitude |
| Latitude | DOUBLE | Peak latitude coordinate | latitude |

**Notable values**: Type ∈ {granite, monolith, volcanic, volcano}; Mountains, Type, Height may be NULL

---

### Mondial.mountainOnIsland
**Meaning**: Association of mountains with islands.
**Synonyms**: island mountain, mountain location

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Mountain | VARCHAR | Mountain name | mountain name |
| Island | VARCHAR | Island name where mountain is located | island name |

---

### Mondial.organization
**Meaning**: International organizations with headquarters location and establishment date.
**Synonyms**: international body, institution

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Abbreviation | VARCHAR | Organization abbreviation/code | org code, acronym |
| Name | VARCHAR | Full organization name | organization name |
| City | VARCHAR | Headquarters city name | headquarters city |
| Country | VARCHAR | Headquarters country code | headquarters country |
| Province | VARCHAR | Headquarters province/region name | headquarters province |
| Established | DATE | Organization establishment date | founded date, creation date |

**Notable values**: City, Country, Province may be NULL

---

### Mondial.politics
**Meaning**: Political status of countries including independence date, dependency, and government type.
**Synonyms**: political status, government information

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Country | VARCHAR | Country code | country code, nation |
| Independence | DATE | Date of independence from colonial power | independence date, founding date |
| Dependent | VARCHAR | Country code of parent nation if dependent territory | parent country, sovereign |
| Government | VARCHAR | Government system type | government type, regime |

**Notable values**: Dependent ∈ {AUS, DK, F, GB, N, NL, NZ, TJ, USA}; Independence and Dependent may be NULL

---

### Mondial.population
**Meaning**: Population demographics including growth rate and infant mortality.
**Synonyms**: demographic data, population statistics

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Country | VARCHAR | Country code | country code, nation |
| Population_Growth | DOUBLE | Annual population growth rate percentage | growth rate, annual growth |
| Infant_Mortality | DOUBLE | Infant mortality rate per 1000 live births | mortality rate, infant deaths |

**Notable values**: Both fields may be NULL/NaN

---

### Mondial.province
**Meaning**: Administrative subdivisions (provinces, states, regions) within countries.
**Synonyms**: state, region, administrative division

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| Name | VARCHAR | Province name | province name, region name |
| Country | VARCHAR | Country code containing province | country code, nation |
| Population | BIGINT | Province population | inhabitants, residents |
| Area | DOUBLE | Province area in square kilometers | area, size |
| Capital | VARCHAR | Capital city name | capital city |
| CapProv | VARCHAR | Capital province name (for capital city location) | capital province |

**Notable values**: Population, Area, Capital, CapProv may be NULL