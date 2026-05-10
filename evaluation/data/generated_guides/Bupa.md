# Bupa Schema Reference Guide

## Schema Summary
The Bupa schema contains medical test results and patient attributes, with liver function tests (alkphos, gammagt, sgot, sgpt), blood cell measurements (mcv), alcohol consumption (drinks), and a binary health indicator (bupa).

## Join Paths

All records are keyed by patient identifier in `arg1`. Standard join pattern:

```sql
FROM Bupa.bupa b
JOIN Bupa.alkphos a ON b.arg1 = a.arg1
JOIN Bupa.drinks d ON b.arg1 = d.arg1
JOIN Bupa.gammagt g ON b.arg1 = g.arg1
JOIN Bupa.mcv m ON b.arg1 = m.arg1
JOIN Bupa.sgot s ON b.arg1 = s.arg1
JOIN Bupa.sgpt sp ON b.arg1 = sp.arg1
```

To filter by patient type:
```sql
JOIN Bupa.bupa_type bt ON b.arg2 = bt.arg1
```

## Table Reference

### `Bupa.bupa`
Binary health indicator per patient.
- **arg1**: Patient identifier (VARCHAR)
- **arg2**: Health status flag; values: `F`, `T`

### `Bupa.bupa_type`
Enumeration of valid health status values.
- **arg1**: Status type; values: `F`, `T`

### `Bupa.bupa_name`
Patient identifier registry.
- **arg1**: Patient identifier (VARCHAR)

### `Bupa.alkphos`
Alkaline phosphatase test result (BIGINT, units not specified).
- **arg1**: Patient identifier
- **arg2**: Test value

### `Bupa.gammagt`
Gamma-glutamyl transferase test result (BIGINT, units not specified).
- **arg1**: Patient identifier
- **arg2**: Test value

### `Bupa.sgot`
Serum glutamic-oxaloacetic transaminase test result (BIGINT, units not specified).
- **arg1**: Patient identifier
- **arg2**: Test value

### `Bupa.sgpt`
Serum glutamic-pyruvic transaminase test result (BIGINT, units not specified).
- **arg1**: Patient identifier
- **arg2**: Test value

### `Bupa.mcv`
Mean corpuscular volume test result (BIGINT, units not specified).
- **arg1**: Patient identifier
- **arg2**: Test value

### `Bupa.drinks`
Alcohol consumption measurement (DOUBLE, units not specified).
- **arg1**: Patient identifier
- **arg2**: Consumption value