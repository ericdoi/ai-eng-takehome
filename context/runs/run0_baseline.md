# Run 0 — Baseline

**Log:** `logs/run_20260510_053738/`
**Cost:** $0.04

## Configuration

- Tools: `submit_answer` only
- Model: `openai/gpt-oss-120b:nitro` (default)
- Temperature: 0.6
- Context compression: off

## Results

| Split | Pass | Fail | Pass Rate |
|-------|------|------|-----------|
| Easy  | 0/64 | 64   | 0.0%      |
| Hard  | 0/64 | 64   | 0.0%      |

## Failure breakdown

| Type | Easy | Hard |
|------|------|------|
| SQL_ERROR | 54 | 40 |
| MISMATCH  | 10 | 24 |

## What went wrong

The agent has no tools except `submit_answer`, so it has to guess schema/table names from the prompt alone.
With 76 schemas and 672 tables, it almost always writes unqualified table names (e.g. `FROM loans`) which
DuckDB rejects with a Catalog Error — hence 54/64 SQL_ERROR on easy.

The 10 easy MISMATCHes and 24 hard MISMATCHes are cases where the model happened to know the schema
(e.g. `financial`, `lahman_2014`) from training data but still got the business logic wrong (hard) or
the exact query wrong (easy).

## Key insight

Every failure traces back to one root cause: no introspection tools and no guide access.
