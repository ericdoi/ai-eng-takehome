# Plan: Improving Business Logic Application (Post Run 6)

Run 6 funnel: schema 94%, tables 84%, logic 33%. Navigation is solved.
33 of 54 right-table cases produce wrong SQL. Root causes identified in
`issues/business_logic_failures.md`. The fixes below target systemic causes,
not schema-specific overfit.

---

## Fix 1 — Synthesis prompt: clearer business rule expression

**Problem:** The LLM synthesizer (haiku) can express rules ambiguously or with
inverted labels. Example: financial guide labels the profitability exclusion filter
as "Non-performing loans" and gives `NOT IN ('C', 'D')` — which reads as defining
non-performing loans as status A and B. The glossary at the bottom has the correct
definition, giving the agent contradictory signals.

**General patterns to fix in the synthesis prompt:**
- Rules must use consistent framing: "TO IDENTIFY [X], filter: `WHERE ...`"
  vs "TO EXCLUDE [X] from a query, filter: `WHERE NOT ...`" — never mix
  the two framings in the same rule entry.
- Rate/ratio rules must explicitly state the denominator as SQL, not just prose
  ("exclude B from default rate calculations" → must become a concrete SQL example
  showing both numerator and denominator).
- Each rule should be independently parseable — no rule should require reading
  another rule to understand what it selects.

**Prompt change (in `_SYNTHESIS_USER`):** Add to the Business Rules section instructions:
> For each rule, use this exact format:
> - **IDENTIFY [label]:** `WHERE condition` — rows matching this condition ARE [label]
> - **EXCLUDE [label]:** `WHERE NOT condition` / `WHERE condition` in a subquery — to
>   filter [label] OUT of results
> For rates and ratios, always provide an example with explicit numerator and denominator.

---

## Fix 2 — Schema textualization: surface date sentinel values

**Problem:** The employee schema uses `to_date = '9999-01-01'` as a sentinel for
current salary rows. Our textualization only samples distinct values for VARCHAR
columns, leaving date sentinels invisible to the synthesizer.

**Fix in `textualize_schema()` (in `scripts/build_schema_guides.py`):**
- For DATE/TIMESTAMP columns, check if any rows contain sentinel-pattern values:
  years ≥ 9000 (far-future sentinels), year 1900/1970 (epoch zeros), or the single
  most-common value where one value accounts for > 80% of rows.
- Surface these in the textualization as: `to_date  DATE  — sentinel: '9999-01-01'
  means currently active`.
- This is cheap (one extra query per date column) and helps any schema using this
  pattern, not just employee.

---

## Fix 3 — Join paths section: distinguish required vs optional joins

**Problem:** Join paths are now first in the guide (correct for priority), but the
synthesizer lists all lookup table joins as peers of required fact joins. The agent
reads them as equally valid and uses lookup joins for simple aggregations where the
gold uses raw codes directly.

**Fix in `_SYNTHESIS_USER`:** Add to the Join Paths instructions:
> Label each join path as one of:
> - **[REQUIRED]** — always needed for this table combination
> - **[OPTIONAL — display only]** — only join when the question asks for
>   human-readable names or descriptions; for grouping/filtering use the raw
>   code column directly (e.g., `UniqueCarrier`, `Origin`, `Dest`)

This is general and applies to any schema with lookup/dimension tables.

---

## Fix 4 — Use Sonnet for top failing schemas (not all 76)

**Problem:** The financial guide has the most failures (7) and the most complex
business rules (4-way status classification, rate denominators, district aggregations).
Haiku may not reason carefully enough through multi-condition rules.

**Pricing (OpenRouter, confirmed 2026-05-10):**
| Model | Input | Output | Full 76-schema regen |
|-------|-------|--------|----------------------|
| Haiku 4.5 (`anthropic/claude-haiku-4-5`) | $1.00/1M | $5.00/1M | ~$1.05 |
| Sonnet 4.6 (`anthropic/claude-sonnet-4-6`) | $3.00/1M | $15.00/1M | ~$3.15 |
| Opus 4.7 (`anthropic/claude-opus-4-7`) | $5.00/1M | $25.00/1M | ~$5.25 |

**Budget constraint:** ~$12.68 remaining. Full Sonnet regen (~$3.15) plus multiple
eval runs (~$1.70 each) is feasible but leaves little room for iteration. Full Opus
regen (~$5.25) is too expensive given the eval budget we need.

**Strategy:** Use Sonnet for top failing schemas only — never Opus, never all 76.
- Add `--model` flag to `build_schema_guides.py`
- Regen financial (and optionally Credit, Airline) with Sonnet as part of the
  top-7 targeted regen; keep Haiku for the remaining schemas
- If top-7 Sonnet regen shows improvement, evaluate whether full Sonnet regen
  (all 76) is worth ~$3.15 before running a final eval

**Action:**
```bash
source .env && uv run python scripts/build_schema_guides.py --schema financial --model anthropic/claude-sonnet-4-6 --skip-embed
```

---

## Fix 5 — Agent prompt: LEFT JOIN for lookup/optional tables

**Problem:** When agents join optional tables (lookup tables, enrichment tables),
INNER JOIN can silently drop rows where the foreign key has no match. This manifests
in Chess (opening table may not cover all games) and would affect any schema with
incomplete lookup coverage.

**Fix in `framework/agent.py` system prompt:** Add one sentence:
> "When joining a lookup or optional table (for descriptions, names, or enrichment),
> use LEFT JOIN — not INNER JOIN — so unmatched rows are not silently dropped."

This is general, not schema-specific, and is standard SQL defensive practice.

Note: For Airline, this alone won't fix the root issue (agent shouldn't join lookup
tables for raw-code aggregations at all), but it prevents row-count reduction as a
safety net.

---

## Execution order

1. Fix 2 (textualization sentinel detection) — pure Python, no LLM cost, low risk
2. Fix 1 + Fix 3 (synthesis prompt improvements) — then regenerate all guides (~$1.05)
3. Fix 4 (Sonnet for financial) — can be done alongside Fix 2/3 or separately
4. Fix 5 (LEFT JOIN prompt) — one-line change, add before or after regen
5. Run eval (Run 7) — target ≥ 30/64 (≥47%)

---

## What we're NOT doing (to avoid overfitting)

- Schema-specific SQL patches in guide files
- Hardcoding loan status values or Airline column names anywhere in code
- Custom post-processing of synthesized guides
- Any change that only affects one schema's behaviour without a general mechanism
