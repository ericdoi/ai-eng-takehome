# Trains Schema Reference Guide

## Schema Summary
This schema contains train compositions and their physical characteristics, tracking individual cars within trains and their directional movement.

## Join Paths

**Trains to their cars:**
```sql
FROM trains.trains t
JOIN trains.cars c ON t.id = c.train_id
```

## Table Reference

### `trains.trains`
Represents individual trains with directional metadata.

| Column | Notes |
|--------|-------|
| `direction` | Enum: `east`, `west` |

### `trains.cars`
Represents individual cars within a train, ordered by position.

| Column | Notes |
|--------|-------|
| `train_id` | Foreign key to `trains.trains.id` |
| `position` | Sequential order of car within train (1-indexed) |
| `shape` | Enum: `bucket`, `ellipse`, `hexagon`, `rectangle`, `u_shaped` |
| `len` | Enum: `long`, `short` |
| `sides` | Enum: `double`, `not_double` |
| `roof` | Enum: `arc`, `flat`, `jagged`, `none`, `peaked` |
| `wheels` | Count of wheels on car |
| `load_shape` | Enum: `circle`, `diamond`, `hexagon`, `rectangle`, `triangle` |
| `load_num` | Quantity of loads carried |