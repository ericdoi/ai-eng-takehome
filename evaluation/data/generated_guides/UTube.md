# UTube Schema Reference Guide

## 1. Schema Summary

The UTube schema contains state classifications and their associated attributes with directional value changes.

---

## 2. Table Reference

### Table: `UTube.utube_states`

**Meaning:** State records with classification labels.  
**Synonyms:** states, classifications

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id` | BIGINT | Unique state identifier | state_id, state_key |
| `class` | VARCHAR | State classification category | classification, type, category |

**Enumerated Values:**
- `class`: `positive`, `negative`

---

### Table: `UTube.utube_attributes`

**Meaning:** Attributes assigned to states with value transitions and directional behavior.  
**Synonyms:** state_attributes, attribute_mappings

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `id_states` | BIGINT | Foreign key reference to state | state_id, state_key |
| `name` | VARCHAR | Attribute name identifier | attribute_name, attribute_type |
| `value1` | VARCHAR | Initial or primary value | start_value, from_value, initial_value |
| `value2` | VARCHAR | Secondary or terminal value | end_value, to_value, final_value |
| `direction` | VARCHAR | Directional behavior of value change | trend, change_type, transition_type |

**Enumerated Values:**
- `name`: `fab`, `fba`, `la`, `lb`
- `value1`: `0`, `f0`, `inf`, `la0`, `lb0`, `mf0`, `minf`
- `value2`: `0`, `f0`, `inf`, `la0`, `lb0`, `mf0`
- `direction`: `dec` (decrease), `inc` (increase), `std` (standard/static)

---

## 3. Join Paths

**Primary join between tables:**
```sql
UTube.utube_attributes ua
INNER JOIN UTube.utube_states us ON ua.id_states = us.id
```

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation.

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| positive states | `WHERE us.class = 'positive'` |
| negative states | `WHERE us.class = 'negative'` |
| increasing attributes | `WHERE ua.direction = 'inc'` |
| decreasing attributes | `WHERE ua.direction = 'dec'` |
| static attributes | `WHERE ua.direction = 'std'` |
| fab attribute | `WHERE ua.name = 'fab'` |
| fba attribute | `WHERE ua.name = 'fba'` |
| la attribute | `WHERE ua.name = 'la'` |
| lb attribute | `WHERE ua.name = 'lb'` |
| infinite values | `WHERE ua.value1 IN ('inf', 'minf') OR ua.value2 IN ('inf', 'minf')` |
| zero values | `WHERE ua.value1 = '0' OR ua.value2 = '0'` |