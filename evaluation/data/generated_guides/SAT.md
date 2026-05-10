# SAT Schema Reference Guide

## Schema Summary
This schema contains satellite telemetry data with time-indexed measurements, fault records, mission phase states, and binary classification labels (positive/negative) across multiple sensor and system channels.

---

## Table Reference

### SAT.class
**Meaning:** Classification taxonomy; defines the two possible class values used throughout the schema.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `cls` | VARCHAR | Classification category | `negative`, `positive` |

---

### SAT.time
**Meaning:** Master time index; defines all valid time points in the dataset.

| Column | Type | Meaning |
|--------|------|---------|
| `tm` | BIGINT | Time index (integer timestamp) |

---

### SAT.succ
**Meaning:** Successor relation; defines sequential time progression.

| Column | Type | Meaning |
|--------|------|---------|
| `tm1` | BIGINT | Current time index |
| `tm2` | BIGINT | Next time index |

**Join Path:** `SAT.succ.tm1 = SAT.time.tm` and `SAT.succ.tm2 = SAT.time.tm`

---

### SAT.fault
**Meaning:** Fault occurrence records; marks time points where faults are present.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `tf` | VARCHAR | Fault flag | `t` (true/fault present) |

**Join Path:** `SAT.fault.tm = SAT.time.tm`

---

### SAT.fault_test
**Meaning:** Fault test results; binary test outcomes at each time point.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `tf` | VARCHAR | Test result flag | `f` (false), `t` (true) |

**Join Path:** `SAT.fault_test.tm = SAT.time.tm`

---

### SAT.trfl
**Meaning:** Test result flag reference; enumeration of possible test outcomes.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tf` | VARCHAR | Test result flag | `f` (false), `t` (true) |

---

### SAT.gmt_mission_phase
**Meaning:** Mission phase state; defines the operational phase at each time point.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `state` | VARCHAR | Mission phase | `eclipse`, `presolstice`, `solstice`, `reconditioning` |

**Join Path:** `SAT.gmt_mission_phase.tm = SAT.time.tm`

---

### SAT.tm001_eod_relay
**Meaning:** End-of-Discharge relay status.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `positive` |

**Join Path:** `SAT.tm001_eod_relay.tm = SAT.time.tm`

---

### SAT.tm002_battov_temp
**Meaning:** Battery overvoltage temperature measurement.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm002_battov_temp.tm = SAT.time.tm`

---

### SAT.tm004_eoc_signaled
**Meaning:** End-of-Charge signaled status.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm004_eoc_signaled.tm = SAT.time.tm`

---

### SAT.tm007_switch
**Meaning:** Switch status (channel 7).

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm007_switch.tm = SAT.time.tm`

---

### SAT.tm009_switch
**Meaning:** Switch status (channel 9).

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm009_switch.tm = SAT.time.tm`

---

### SAT.tm011_eod_override
**Meaning:** End-of-Discharge override status.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `positive` |

**Join Path:** `SAT.tm011_eod_override.tm = SAT.time.tm`

---

### SAT.tm013_switch
**Meaning:** Switch status (channel 13).

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm013_switch.tm = SAT.time.tm`

---

### SAT.tm015_eod_signaled
**Meaning:** End-of-Discharge signaled status.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm015_eod_signaled.tm = SAT.time.tm`

---

### SAT.tm017_switch
**Meaning:** Switch status (channel 17).

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm017_switch.tm = SAT.time.tm`

---

### SAT.tm018_switch
**Meaning:** Switch status (channel 18).

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm018_switch.tm = SAT.time.tm`

---

### SAT.tm021_eoc_disabled
**Meaning:** End-of-Charge disabled status.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `positive` |

**Join Path:** `SAT.tm021_eoc_disabled.tm = SAT.time.tm`

---

### SAT.tm022_switch
**Meaning:** Switch status (channel 22).

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm022_switch.tm = SAT.time.tm`

---

### SAT.tm029_ovt_disabled
**Meaning:** Overvoltage threshold disabled status.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `positive` |

**Join Path:** `SAT.tm029_ovt_disabled.tm = SAT.time.tm`

---

### SAT.tm031_switch
**Meaning:** Switch status (channel 31).

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm031_switch.tm = SAT.time.tm`

---

### SAT.tm038_switch
**Meaning:** Switch status (channel 38).

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm038_switch.tm = SAT.time.tm`

---

### SAT.tm039_eod_disabled
**Meaning:** End-of-Discharge disabled status.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `positive` |

**Join Path:** `SAT.tm039_eod_disabled.tm = SAT.time.tm`

---

### SAT.tm040_switch
**Meaning:** Switch status (channel 40).

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm040_switch.tm = SAT.time.tm`

---

### SAT.tm042_switch
**Meaning:** Switch status (channel 42).

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm042_switch.tm = SAT.time.tm`

---

### SAT.tm043_switch
**Meaning:** Switch status (channel 43).

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm043_switch.tm = SAT.time.tm`

---

### SAT.tm054_supply_1a
**Meaning:** Supply 1A voltage/status measurement.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm054_supply_1a.tm = SAT.time.tm`

---

### SAT.tm055_supply_1b
**Meaning:** Supply 1B voltage/status measurement.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm055_supply_1b.tm = SAT.time.tm`

---

### SAT.tm057_supply_2c
**Meaning:** Supply 2C voltage/status measurement.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative` |

**Join Path:** `SAT.tm057_supply_2c.tm = SAT.time.tm`

---

### SAT.tm058_asr_or_switch_10
**Meaning:** Autonomous Switch Reconfiguration OR switch (channel 10) status.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm058_asr_or_switch_10.tm = SAT.time.tm`

---

### SAT.tm070_supply_3c
**Meaning:** Supply 3C voltage/status measurement.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm070_supply_3c.tm = SAT.time.tm`

---

### SAT.tm071_asr_or_switch_20
**Meaning:** Autonomous Switch Reconfiguration OR switch (channel 20) status.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `positive` |

**Join Path:** `SAT.tm071_asr_or_switch_20.tm = SAT.time.tm`

---

### SAT.tm211_bus_voltage
**Meaning:** Bus voltage measurement.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm211_bus_voltage.tm = SAT.time.tm`

---

### SAT.tm220_supply_1c
**Meaning:** Supply 1C voltage/status measurement.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm220_supply_1c.tm = SAT.time.tm`

---

### SAT.tm222_charging
**Meaning:** Battery charging status.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm222_charging.tm = SAT.time.tm`

---

### SAT.tm257_battery_voltage
**Meaning:** Battery voltage measurement.

| Column | Type | Meaning | Values |
|--------|------|---------|--------|
| `tm` | BIGINT | Time index | |
| `class` | VARCHAR | Classification | `negative`, `positive` |

**Join Path:** `SAT.tm257_battery_voltage.tm = SAT.time.tm`

---

## Join Paths

All telemetry and state tables join to the master time index:
```sql
INNER JOIN SAT.time t ON [telemetry_table].tm = t.tm
```

Sequential time progression:
```sql
INNER JOIN SAT.succ s ON t1.tm = s.tm1 AND t2.tm = s.tm2
```

Fault correlation:
```sql
LEFT JOIN SAT.fault f ON t.tm = f.tm
LEFT JOIN SAT.fault_test ft ON t.tm = ft.tm
```

Mission phase context:
```sql
LEFT JOIN SAT.gmt_mission_phase gmp ON t.tm = gmp.tm
```

---

## Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| time point, timestamp | `SAT.time.tm` |
| next time, successor | `SAT.succ.tm2` WHERE `SAT.succ.tm1 = [current_tm]` |
| fault present | `SAT.fault.tm` (existence indicates fault) |
| test passed | `SAT.fault_test.tf = 't'` |
| test failed | `SAT.fault_test.tf = 'f'` |
| positive state, nominal | `[table].class = 'positive'` |
| negative state, anomalous | `[table].class = 'negative'` |
| eclipse phase | `SAT.gmt_mission_phase.state = 'eclipse'` |
| solstice phase | `SAT.gmt_mission_phase.state = 'solstice'` |
| presolstice phase | `SAT.gmt_mission_phase.state = 'presolstice