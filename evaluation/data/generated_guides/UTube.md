# UTube Schema Reference Guide

## Schema Summary
This schema tracks U-tube states and their associated attributes, with classifications and directional value changes.

## Join Paths

**States to attributes:**
```sql
FROM UTube.utube_states s
JOIN UTube.utube_attributes a ON s.id = a.id_states
```

## Table Reference

### `UTube.utube_states`
State records with classification.

| Column | Semantics |
|--------|-----------|
| `id` | Primary key; referenced by `utube_attributes.id_states` |
| `class` | Classification type. Enum: `positive`, `negative` |

### `UTube.utube_attributes`
Attribute records linked to states, tracking value changes and directions.

| Column | Semantics |
|--------|-----------|
| `id_states` | Foreign key to `utube_states.id` |
| `name` | Attribute category. Enum: `fab`, `fba`, `la`, `lb` |
| `value1` | Initial or primary value. Enum: `0`, `f0`, `inf`, `la0`, `lb0`, `mf0`, `minf` |
| `value2` | Secondary or final value. Enum: `0`, `f0`, `inf`, `la0`, `lb0`, `mf0` (note: `minf` absent in samples) |
| `direction` | Change direction. Enum: `dec` (decreasing), `inc` (increasing), `std` (standard/no change) |