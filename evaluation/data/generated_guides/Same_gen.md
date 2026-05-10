# Same_gen Schema Reference Guide

## 1. Schema Summary
The `Same_gen` schema contains genealogical data modeling family relationships, generational groupings, and classification targets for persons across parent-child and same-generation connections.

---

## 2. Table Reference

### Table: `Same_gen.parent`
**Meaning:** Parent-child relationships; records pairs where name1 is a parent of name2.
**Synonyms:** family_links, parentage, ancestry

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name1` | VARCHAR | Parent's name | parent_name |
| `name2` | VARCHAR | Child's name | child_name |

**Notable values (from samples):** ali1, dilber, yusuf2, ayse, ayten, mediha2

---

### Table: `Same_gen.person`
**Meaning:** Master list of all persons in the dataset.
**Synonyms:** individuals, people, entities

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name` | VARCHAR | Person's unique identifier | person_name, individual_id |

**Notable values (from samples):** ali1, ali2, alp, anil, ayse, ayten

---

### Table: `Same_gen.same_gen`
**Meaning:** Same-generation relationships; records pairs of persons belonging to the same generational cohort.
**Synonyms:** cohort_pairs, peer_relationships, generation_links

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name1` | VARCHAR | First person in same-generation pair | person_a |
| `name2` | VARCHAR | Second person in same-generation pair | person_b |

**Notable values (from samples):** ali1, fatma, ismail, mehmet1, neriman, nesrin

---

### Table: `Same_gen.target`
**Meaning:** Classification or prediction target; binary or categorical outcome for person pairs.
**Synonyms:** labels, outcomes, predictions, classification_results

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `name1` | VARCHAR | First person in pair | person_a |
| `name2` | VARCHAR | Second person in pair | person_b |
| `target` | BIGINT | Target value (0 or 1); classification label | label, outcome, prediction, class |

**Notable values (from samples):** target = 0 (observed in all samples; likely binary 0/1)

---

## 3. Join Paths

| Join Type | Condition | Purpose |
|-----------|-----------|---------|
| parent → person | `parent.name1 IN (person.name)` OR `parent.name2 IN (person.name)` | Validate parent/child names exist in person master list |
| same_gen → person | `same_gen.name1 IN (person.name)` OR `same_gen.name2 IN (person.name)` | Validate same-generation pair members exist in person master list |
| target → person | `target.name1 IN (person.name)` OR `target.name2 IN (person.name)` | Validate target pair members exist in person master list |
| target → same_gen | `target.name1 = same_gen.name1 AND target.name2 = same_gen.name2` | Match target pairs to same-generation relationships |
| target → parent | `(target.name1 = parent.name1 AND target.name2 = parent.name2)` OR `(target.name1 = parent.name2 AND target.name2 = parent.name1)` | Match target pairs to parent-child relationships |

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation. Inferred patterns:

- **Rule:** "Persons in same_gen table are from the same generation" → `WHERE (name1, name2) IN (SELECT name1, name2 FROM same_gen)`
- **Rule:** "Target classification applies to person pairs" → `WHERE name1 IN (SELECT name FROM person) AND name2 IN (SELECT name FROM person)`
- **Rule:** "Parent relationship is directional (name1 → name2)" → `WHERE name1 IS NOT NULL AND name2 IS NOT NULL`

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| parent-child pair | `parent.name1, parent.name2` |
| same generation pair | `same_gen.name1, same_gen.name2` |
| person identifier | `person.name` |
| classification label | `target.target` |
| positive class | `WHERE target.target = 1` |
| negative class | `WHERE target.target = 0` |
| all persons | `SELECT DISTINCT name FROM person` |
| all parent relationships | `SELECT * FROM parent` |
| all same-generation relationships | `SELECT * FROM same_gen` |
| all labeled pairs | `SELECT * FROM target` |