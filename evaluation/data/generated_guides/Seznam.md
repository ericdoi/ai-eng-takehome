# Seznam Schema Reference Guide

## 1. Schema Summary

The Seznam schema contains client advertising transaction data across Czech regions, tracking billed services, executed campaigns, and out-of-pocket advertising activity.

---

## 2. Table Reference

### Table: `Seznam.client`
**Meaning:** Client master data; registry of advertising clients by region and business category.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `client_id` | BIGINT | Unique client identifier | client number, account ID |
| `kraj` | VARCHAR | Czech administrative region | region, district, province |
| `obor` | VARCHAR | Business category or industry classification | industry, business type, sector |

**Notable Values:**
- `kraj`: Jihomoravský kraj, Jihočeský kraj, Karlovarský kraj, Královéhradecký kraj, Liberecký kraj, Moravskoslezský kraj, Olomoucký kraj, Pardubický kraj, Plzeňský kraj, Praha, Středočeský kraj, Vysočina, Zlínský kraj, Ústecký kraj

---

### Table: `Seznam.dobito`
**Meaning:** Billed services; amounts charged to clients for advertising services rendered.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `client_id` | BIGINT | Foreign key to client | account ID |
| `month_year_datum_transakce` | DATE | Transaction date (first day of month) | billing month, transaction month, period |
| `sluzba` | VARCHAR | Service code | service type, service category |
| `kc_dobito` | DOUBLE | Amount billed in Czech crowns | billed amount, charged amount, invoice total |

**Notable Values:**
- `sluzba`: a, b, c, d, e, f, g, h

---

### Table: `Seznam.probehnuto`
**Meaning:** Executed campaigns; actual campaign performance and click-through revenue by service.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `client_id` | BIGINT | Foreign key to client | account ID |
| `month_year_datum_transakce` | DATE | Transaction date (first day of month) | campaign month, execution month, period |
| `sluzba` | VARCHAR | Service code | service type, service category |
| `kc_proklikano` | DOUBLE | Revenue from clicks in Czech crowns | click revenue, executed amount, performance revenue |

**Notable Values:**
- `sluzba`: a, b, c, d, e, f, g, h

---

### Table: `Seznam.probehnuto_mimo_penezenku`
**Meaning:** Out-of-pocket advertising; campaigns executed outside the standard billing system.

| Column | Type | Meaning | Synonyms |
|--------|------|---------|----------|
| `client_id` | BIGINT | Foreign key to client | account ID |
| `Month/Year` | DATE | Period date (first day of month) | month, period, transaction month |
| `probehla_inzerce_mimo_penezenku` | VARCHAR | Indicator of out-of-pocket advertising activity | off-budget flag, external advertising |

**Notable Values:**
- `probehla_inzerce_mimo_penezenku`: ANO (yes)

---

## 3. Join Paths

**Client to Billed Services:**
```sql
Seznam.client c
JOIN Seznam.dobito d ON c.client_id = d.client_id
```

**Client to Executed Campaigns:**
```sql
Seznam.client c
JOIN Seznam.probehnuto p ON c.client_id = p.client_id
```

**Client to Out-of-Pocket Advertising:**
```sql
Seznam.client c
JOIN Seznam.probehnuto_mimo_penezenku pm ON c.client_id = pm.client_id
```

**Billed Services to Executed Campaigns (same period and service):**
```sql
Seznam.dobito d
JOIN Seznam.probehnuto p 
  ON d.client_id = p.client_id 
  AND d.month_year_datum_transakce = p.month_year_datum_transakce
  AND d.sluzba = p.sluzba
```

---

## 4. Business Rules as SQL

No explicit business rules provided in schema documentation. Rules should be inferred from query context.

---

## 5. Synonym Glossary

| Common Term | Exact Schema Reference |
|-------------|------------------------|
| billed amount | `dobito.kc_dobito` |
| click revenue | `probehnuto.kc_proklikano` |
| campaign execution | `probehnuto` table |
| service type | `dobito.sluzba` or `probehnuto.sluzba` |
| region | `client.kraj` |
| industry | `client.obor` |
| billing period | `dobito.month_year_datum_transakce` |
| campaign period | `probehnuto.month_year_datum_transakce` |
| off-budget advertising | `probehnuto_mimo_penezenku` table WHERE `probehla_inzerce_mimo_penezenku = 'ANO'` |
| client account | `client.client_id` |