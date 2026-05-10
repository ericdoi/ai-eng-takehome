# Seznam Schema Reference Guide

## Schema Summary
This schema tracks advertising services, billing, and campaign performance for clients across Czech regions, with transaction-level detail on charged services, executed campaigns, and out-of-network advertising activity.

---

## Join Paths

**Client to billing and performance:**
```sql
SELECT c.client_id, c.kraj, c.obor, d.kc_dobito, p.kc_proklikano
FROM Seznam.client c
LEFT JOIN Seznam.dobito d ON c.client_id = d.client_id
LEFT JOIN Seznam.probehnuto p ON c.client_id = p.client_id 
  AND d.month_year_datum_transakce = p.month_year_datum_transakce
  AND d.sluzba = p.sluzba
```

**Client to out-of-network advertising:**
```sql
SELECT c.client_id, pmp.Month_Year, pmp.probehla_inzerce_mimo_penezenku
FROM Seznam.client c
LEFT JOIN Seznam.probehnuto_mimo_penezenku pmp ON c.client_id = pmp.client_id
```

---

## Synonym Glossary

| Term | Schema Reference |
|------|------------------|
| charged amount, billed CZK | `Seznam.dobito.kc_dobito` |
| executed amount, clicked CZK, performance CZK | `Seznam.probehnuto.kc_proklikano` |
| service type, ad type | `Seznam.dobito.sluzba` or `Seznam.probehnuto.sluzba` |
| region, territory | `Seznam.client.kraj` |
| business category, industry | `Seznam.client.obor` |
| transaction date, month | `Seznam.dobito.month_year_datum_transakce` or `Seznam.probehnuto.month_year_datum_transakce` |
| out-of-network campaign, external advertising | `Seznam.probehnuto_mimo_penezenku` |

---

## Table Reference

### `Seznam.client`
Client master data with regional and business classification.

| Column | Notes |
|--------|-------|
| `kraj` | Czech region. Values: Jihomoravský kraj, Jihočeský kraj, Karlovarský kraj, Královéhradecký kraj, Liberecký kraj, Moravskoslezský kraj, Olomoucký kraj, Pardubický kraj, Plzeňský kraj, Praha, Středočeský kraj, Vysočina, Zlínský kraj, Ústecký kraj |
| `obor` | Business category/industry classification |

---

### `Seznam.dobito`
Billed/charged transactions for advertising services.

| Column | Notes |
|--------|-------|
| `month_year_datum_transakce` | Transaction date (first day of month) |
| `sluzba` | Service type. Values: a, b, c, d, e, f, g, h |
| `kc_dobito` | Amount charged in CZK (Czech koruna) |

---

### `Seznam.probehnuto`
Executed campaign performance with click-through or engagement metrics.

| Column | Notes |
|--------|-------|
| `month_year_datum_transakce` | Transaction date (first day of month) |
| `sluzba` | Service type. Values: a, b, c, d, e, f, g, h |
| `kc_proklikano` | Amount executed/clicked in CZK; can be negative |

---

### `Seznam.probehnuto_mimo_penezenku`
Flag indicating out-of-network or external advertising campaigns.

| Column | Notes |
|--------|-------|
| `Month/Year` | Campaign month (first day of month) |
| `probehla_inzerce_mimo_penezenku` | Out-of-network advertising indicator. Value: ANO (yes) |