# SAT Schema Reference Guide

## Schema Summary
This schema contains satellite telemetry data with time-indexed measurements, fault records, mission phase states, and binary class labels (positive/negative) across 40+ telemetry channels.

---

## Join Paths

**Timeline with mission phase:**
```sql
SELECT t.tm, gmp.state
FROM SAT.time t
LEFT JOIN SAT.gmt_mission_phase gmp ON t.tm = gmp.tm
```

**Successive time points:**
```sql
SELECT s.tm1, s.tm2
FROM SAT.succ s
WHERE s.tm1 = <value>
```

**Fault records with test classification:**
```sql
SELECT f.tm, f.tf, ft.tf AS test_classification
FROM SAT.fault f
LEFT JOIN SAT.fault_test ft ON f.tm = ft.tm
```

**Any telemetry channel with class label:**
```sql
SELECT t.tm, t.class
FROM SAT.<telemetry_table> t
WHERE t.tm = <value>
```

---

## Business Rules as SQL

**Fault condition (production fault):**
```sql
WHERE tf = 't'
```

**Test fault condition:**
```sql
WHERE tf = 'f'
```

**Positive class (nominal/healthy state):**
```sql
WHERE class = 'positive'
```

**Negative class (anomalous/fault state):**
```sql
WHERE class = 'negative'
```

**Mission phase filters:**
```sql
WHERE state IN ('eclipse', 'presolstice', 'solstice', 'reconditioning')
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| timestamp, time index | `SAT.time.tm` |
| fault flag | `SAT.fault.tf` |
| test fault flag | `SAT.fault_test.tf` |
| mission state, phase | `SAT.gmt_mission_phase.state` |
| anomaly, fault state | `class = 'negative'` |
| nominal, healthy state | `class = 'positive'` |
| next time point | `SAT.succ.tm2` WHERE `tm1 = <current>` |
| previous time point | `SAT.succ.tm1` WHERE `tm2 = <current>` |

---

## Table Reference

### SAT.time
**Meaning:** Master timeline index.  
**Columns:**
- `tm` (BIGINT): Time index, primary key for all telemetry tables.

---

### SAT.class
**Meaning:** Classification domain reference.  
**Columns:**
- `cls` (VARCHAR): Enumerated values: `negative`, `positive`

---

### SAT.fault
**Meaning:** Production fault records.  
**Columns:**
- `tm` (BIGINT): Time index of fault occurrence.
- `tf` (VARCHAR): Fault flag; value: `t` (true/fault present).

---

### SAT.fault_test
**Meaning:** Test/validation fault classifications.  
**Columns:**
- `tm` (BIGINT): Time index.
- `tf` (VARCHAR): Test fault flag; values: `f` (false), `t` (true).

---

### SAT.gmt_mission_phase
**Meaning:** Satellite mission operational phase at each time point.  
**Columns:**
- `tm` (BIGINT): Time index.
- `state` (VARCHAR): Mission phase; values: `eclipse`, `presolstice`, `solstice`, `reconditioning`.

---

### SAT.succ
**Meaning:** Successor relationship; maps consecutive time points.  
**Columns:**
- `tm1` (BIGINT): Current time index.
- `tm2` (BIGINT): Next time index.

---

### SAT.trfl
**Meaning:** Test fault label reference domain.  
**Columns:**
- `tf` (VARCHAR): Values: `f`, `t`.

---

## Telemetry Tables (40 channels)

All telemetry tables share structure: `tm` (BIGINT, time index) + `class` (VARCHAR, classification).

**Always-positive (nominal-only) channels:**
- `SAT.tm001_eod_relay` — End-of-discharge relay state.
- `SAT.tm011_eod_override` — EOD override enable.
- `SAT.tm021_eoc_disabled` — End-of-charge disabled flag.
- `SAT.tm029_ovt_disabled` — Overvoltage threshold disabled.
- `SAT.tm039_eod_disabled` — EOD disabled flag.
- `SAT.tm071_asr_or_switch_20` — ASR OR switch 20.

**Binary (positive/negative) channels:**
- `SAT.tm002_battov_temp` — Battery overvoltage/temperature.
- `SAT.tm004_eoc_signaled` — End-of-charge signaled.
- `SAT.tm007_switch`, `SAT.tm009_switch`, `SAT.tm013_switch`, `SAT.tm017_switch`, `SAT.tm018_switch`, `SAT.tm022_switch`, `SAT.tm031_switch`, `SAT.tm038_switch`, `SAT.tm040_switch`, `SAT.tm042_switch`, `SAT.tm043_switch` — Switch states.
- `SAT.tm015_eod_signaled` — EOD signaled.
- `SAT.tm054_supply_1a`, `SAT.tm055_supply_1b`, `SAT.tm070_supply_3c`, `SAT.tm220_supply_1c` — Supply rail voltages.
- `SAT.tm058_asr_or_switch_10` — ASR OR switch 10.
- `SAT.tm211_bus_voltage` — Bus voltage.
- `SAT.tm222_charging` — Charging state.
- `SAT.tm257_battery_voltage` — Battery voltage.

**Negative-only channel:**
- `SAT.tm057_supply_2c` — Supply 2C rail (anomaly-only observations).