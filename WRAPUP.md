# SQL Agent Wrapup

## The problem

The easy and hard splits test different capabilities. Easy questions can be answered purely
from schema structure — the right tables and the right join are enough. Hard questions
additionally require the business-rule markdown files: the agent must locate the relevant
rule, translate it into a SQL condition, and apply it correctly without over- or under-
filtering. Getting hard questions right means closing both the navigation gap (finding the
right schema and tables in a 76-schema warehouse) and the logic gap (applying domain rules
correctly). This writeup focuses on hard, since that's what separates the splits.

## Scores

| Split | Baseline (Run 1) | Final (Run 8) | Delta |
|-------|-----------------|---------------|-------|
| Easy | 40/64 (62.5%) | **51/64 (79.7%)** | +11 cases (+17 pp) |
| Hard | 25/64 (39.1%) | **38/64 (59.4%)** | +13 cases (+20 pp) |

Easy split navigation funnel (Run 8): schema 98%, tables 95%, logic 80%.
Hard split navigation funnel (Run 8): schema 97%, tables 88%, logic 68%.

All optimization targeted the hard split. The easy-split gains (+17 pp) are a free result of
the same general fixes — no easy-specific tuning was done.

---

## Approach

### Phase 1 — Baseline (Run 1)

Standard agentic loop: `list_schemas → list_tables → describe_table → run_sql → submit_answer`.
The agent had to discover schema structure from scratch on every question.

**Funnel analysis after Run 1:**
- Wrong schema: ~8 cases
- Wrong tables: ~12 cases
- Wrong logic: ~27–43 cases (highly variable across runs)

Navigation (schema + table selection) was a bottleneck but logic was already the larger problem.

### Phase 2 — LLM-synthesized schema guides + semantic search

**Core insight:** Having the agent rediscover the same schema structure on every run is wasteful
and inconsistent. Pre-synthesize a reference guide per schema, embed them, and let the agent
retrieve the right guide in one call.

**Pipeline (`scripts/build_schema_guides.py`):**
1. Textualize each schema: table names, columns with types, VARCHAR distinct values, sample rows
2. Fuse with existing hand-written business-rule guides (20/76 schemas have these)
3. Call an LLM (Haiku by default, Sonnet for complex schemas) to synthesize a guide
4. Embed all 76 guides with `text-embedding-3-small` → 76×1536 float32 matrix, L2-normalized

**Retrieval tool (`tools/schema_guide_tools.py`):**
`find_schema(query)` → cosine similarity over the embedding matrix → returns the top guide with
a prominent banner showing the exact schema name and SQL usage examples.

**System prompt** updated to enforce a fixed workflow:
`find_schema → run_sql → submit_answer`
with `list_tables` / `describe_table` available for gaps.

After Phase 2 (Run 6): schema identification 94%, table identification 84%, logic 61%.
AGENT_ERROR (navigation loops) fell from 11 to 2.

### Phase 2 iterations — targeted logic fixes

Eight targeted, general fixes (no schema-specific patches):

| Fix | What changed | Where |
|-----|-------------|-------|
| 1 | IDENTIFY / EXCLUDE rule framing; explicit rate denominators | synthesis prompt |
| 2 | DATE sentinel detection (far-future, epoch-zero, dominant value) | `textualize_schema()` |
| 3 | `[REQUIRED]` / `[OPTIONAL — display only]` join labels | synthesis prompt |
| 4 | `--model` flag; financial guide regenerated with Sonnet | `build_schema_guides.py` |
| 5 | LEFT JOIN for lookup/optional tables | agent system prompt |
| 6 | Extra columns are never penalized; include source cols alongside derived | agent system prompt |
| 7 | Apply EXCLUDE rules only when the question explicitly targets that metric | agent system prompt |
| 8 | Emit combined CASE WHEN SQL for multi-value classifications | synthesis prompt |

**All fixes are general mechanisms.** No hardcoded schema names, column values, or SQL snippets
anywhere in code or prompts.

---

## Run progression

Each case passes through three sequential gates: the agent must reach the correct schema,
use the correct tables, and then produce the right SQL. The funnel columns show what fraction
of all 64 cases cleared each gate; a case that fails at schema never reaches tables, and a
case that fails at tables never reaches logic. Logic% therefore equals the overall pass rate.

| Run | Hard (pass rate) | Schema% | Tables% | Logic% | Key change |
|-----|-----------------|---------|---------|--------|------------|
| 1 | 25/64 (39%) | ~88% | ~72% | ~39% | Baseline |
| 6 | 21/64 (33%) | 94% | 84% | 33% | Phase 2 launch |
| 7 | 32/64 (50%) | 94% | 91% | 50% | Fixes 1–5 (guide quality + agent prompt) |
| 8 | 38/64 (59%) | 97% | 88% | 59% | Fixes 6–8 (output columns, conditional EXCLUDE, CASE WHEN) |

Schema% and Tables% measure navigation quality independent of logic. The gap between
Tables% and Logic% (pass rate) shows how many cases reached the right tables but still
produced wrong SQL — the pure logic failure rate. In Run 8 that gap is 88% − 59% = 29 pp
(19 cases with right tables but wrong query).

Run 6 scored *lower* than Run 1 despite better navigation. Phase 2 fixed navigation so
thoroughly that cases previously failing at schema (and counted as navigation losses) now
reached the correct schema and failed on logic instead — revealing logic errors that were
previously hidden behind navigation failures. The logic failure count was always high;
Run 6 just made it visible.

---

## What worked

**Semantic schema retrieval.** Embedding 76 schema guides and doing cosine similarity on the
query achieves 94–97% schema identification. The prior approach (agent calls `list_schemas`,
reads a list of 76 names, guesses) was inconsistent and slow. Pre-computation is the right
architecture here.

**LLM-synthesized guides.** Having the synthesizer read raw schema structure + business rules
and produce a query-optimized reference document is significantly better than giving the agent
raw schema dumps. The synthesizer naturally surfaces join paths, enum semantics, and business
rules as SQL conditions in a scannable format.

**IDENTIFY / EXCLUDE framing.** Replacing ambiguous prose rules ("non-performing loans exclude
statuses C and D") with explicit `IDENTIFY` / `EXCLUDE` labels and SQL conditions eliminated
the most common class of inverted-logic errors seen in Run 6.

**Conditional EXCLUDE in agent prompt.** The single sentence "Apply EXCLUDE rules ONLY when
the question explicitly targets that metric" reduced several false exclusions. The agent was
treating guide filters as always-on constraints rather than conditional business rules.

**Extra-columns rule.** The grader ignores column name aliases and tolerates extra columns,
but compares values. Telling the agent to include source columns alongside any derived ones
fixed cases where the agent returned only a concatenated `firstName || ' ' || lastName` value
when the gold expected the raw `firstName` and `lastName` values in separate columns — a value
mismatch regardless of aliases.

**CASE WHEN classification SQL.** Adding instruction to emit a single combined CASE WHEN for
multi-value mappings (e.g., `status → 'Performing'/'Watch List'/'Non-Performing'`) fixed
financial and Credit classification queries that previously returned raw status codes.

---

## What didn't work

**`search_columns` tool (Run 2).** Added a keyword-search tool so the agent could look up
columns by name across all schemas. It improved schema accuracy but caused regressions: the
agent started using `search_columns` to reconstruct join paths incrementally rather than
reading a table description holistically, producing poorly-reasoned multi-step navigation
that was slower and less reliable. Reverted after one run; code kept but disabled.

**Prompt engineering alone.** Before building guides, several rounds of system-prompt
iteration tried to reduce wrong-logic cases: emphasizing the business-rule files, adding
examples, tweaking workflow instructions. Each iteration moved 1–3 cases but never addressed
the root cause — the agent had to re-derive the same schema structure from scratch on every
question, with no persistent representation of what the rules actually said as SQL. Prompt
changes are a multiplier on a solid foundation; they can't substitute for one.

**`search_guides` / `read_guide` tools.** Implemented a BM25-style guide search and a guide
reader tool so the agent could retrieve the relevant markdown file on demand. These were
superseded by the LLM-synthesis approach before being wired up: reading a raw markdown
business-rules file is harder for an agent than reading a pre-synthesized guide that already
translates those rules into SQL conditions.

---

## Remaining failures (26 cases, Run 8)

### Navigation failures (7 cases)

| Pattern | Count | Root cause |
|---------|-------|------------|
| Wrong schema (world→nations, Credit→ccs) | 2 | Short generic queries don't disambiguate similar-sounding schemas |
| Wrong tables (missed join target) | 5 | Guide describes join path but agent queries partial table set |

The wrong-schema cases ("small populations", "average transaction value") are queries generic
enough that the embedding retrieval picks a plausible but wrong schema. These would require
either better guide content to widen the semantic distance between schemas, or a fallback
validation step (run a test query; if 0 rows, re-query with `find_schema`).

The wrong-table cases (employee missing `employees`, ErgastF1 using `constructorResults` instead
of `results`) indicate the agent found the right schema but chose an adjacent table. These guides
may need stronger "use THIS table for points/scores, not that one" language.

### Logic failures (19 cases)

**Integer vs float division — lahman_2014 (4 cases)**

Gold queries use `pi.IPouts / 3` (integer division in DuckDB), producing truncated
`innings_pitched` values. The agent consistently uses `pi.IPouts / 3.0` (float), producing
fractional values. Because `innings_pitched` appears in results, the values differ even when
the formula is logically correct. Additionally, the agent sometimes incorrectly aggregates
`SUM(pi.IPouts)` across seasons for queries that ask for single-season statistics — a
per-row vs aggregate confusion the guide doesn't fully resolve.

**ErgastF1 wrong-value column selection (3 cases)**

The agent selects `constructorRef` (a machine slug like `"mercedes"`) instead of `name`
(a display string like `"Mercedes"`). The grader ignores column name aliases but compares
values — so even though both columns could be aliased identically, the underlying values
differ and the comparison fails. The guide's synonym glossary says "constructor name →
`constructors.name`" but the agent doesn't consistently follow it when writing its first
query.

**CraftBeer LEFT JOIN vs INNER JOIN (2 cases)**

Fix 5 instructs the agent to use LEFT JOIN for lookup/optional tables. The brewery join in
CraftBeer is a lookup join (for brewery name), so the agent uses LEFT JOIN. The gold uses
INNER JOIN. If any beer has no matching brewery, LEFT JOIN produces extra rows the gold
doesn't include. This is a tension between the general safety rule (LEFT JOIN to avoid
silent drops) and the specific gold behaviour. The fix would require distinguishing
"enrichment joins where missing is meaningful" from "lookup joins where all FKs are present."

**Airline — wrong join or extra join (2 cases)**

Despite `[OPTIONAL — display only]` labels, the agent still joins the UniqueCarrier lookup
table in some on-time performance queries, adding a CarrierName column that shifts the result
set. The gold uses only raw `UniqueCarrier` codes.

**Credit — RF refund exclusion over-applied (2 cases)**

The guide's business rule `SUM(CASE WHEN charge_code = 'RF' THEN -charge_amt ELSE charge_amt END)`
for net charges is being applied to simple `SUM(charge_amt)` lifetime charge queries. Fix 7
reduced this significantly but didn't fully eliminate it — likely because the guide prominently
shows the RF formula as a "business rule" and the agent anchors to it.

**Credit — category label casing (1 case)**

The source guide says "Essential spending" and "Discretionary spending" (title case). The
synthesizer outputs lowercase labels ('essential', 'discretionary'). The gold query uses
'Essential', 'Discretionary', 'Premium'. The third label ('Premium') does not appear in the
source guide at all, making it genuinely unrecoverable from available information.

**Airline — thin route count query structure (1 case)**

The question asks "how many thin-route pairs are there?" (answer: a single integer). The gold
wraps the pair enumeration in `SELECT COUNT(*) FROM (...)`. The agent enumerates the pairs
with a `COUNT(*) OVER ()` window function, returning one row per pair with the total count —
correct value, wrong shape. This is a question-comprehension issue.

**Credit — "quarters" interpreted as DATE_TRUNC (1 case)**

The question asks for "top member-quarters by charge count." The gold treats a `statement_no`
as a quarter proxy (the schema has monthly statements). The agent interprets "quarter" as a
calendar quarter and uses `DATE_TRUNC('quarter', statement_dt)`, producing different groupings.
This is an implicit domain mapping that requires business context the guide doesn't provide.

**Over-engineered queries (3 cases across financial, CraftBeer)**

The agent produces more complex SQL than required: adds classification CASE WHEN for a simple
aggregation, or adds style-group categorization when the question asks for a raw average. Fix 7
reduced this pattern but didn't eliminate it — the agent interprets guide content as a
prescription for what to compute rather than a reference for what's available.

**AGENT_ERROR — max iterations (1 case)**

One financial "performing loans by district" case exhausts the iteration budget while trying
various join approaches.

---

## What I'd do next

**Highest-impact: source-column selection guidance in synthesis prompt**
The grader compares values, not column name aliases. The failure in ErgastF1 cases is that
the agent selects `constructorRef` (value: `"mercedes"`) instead of `name` (value:
`"Mercedes"`) — two different values that happen to answer the same question. Add to the
synthesis prompt: "For any table with both a human-readable column (e.g., `name`,
`forename`+`surname`) and a code/slug column (e.g., `constructorRef`, `driverRef`), note in
the synonym glossary which column holds the display-quality value, and mark the other as
join-only." This would steer the agent toward selecting the right source column.

**Integer division annotation in synthesis**
Add to synthesis prompt: "When documenting formula columns derived from integer division
(e.g., innings pitched from IPouts), note that the division is integer (`IPouts / 3`,
not `IPouts / 3.0`)." The distinction affects sort order in DuckDB and needs to be explicit
in the guide.

**Regen all 76 guides with accumulated prompt improvements**
Eight rounds of prompt improvements have been applied incrementally. A single full-76 regen
with the final synthesis prompt (~$1.05 at Haiku rates) would propagate all improvements to
schemas not yet regenerated. This is straightforward and worth doing before a final eval.

**Validation fallback for navigation errors**
When the agent's first `run_sql` after `find_schema` returns 0 rows, inject a prompt:
"Your query returned 0 rows — you may have the wrong schema. Call find_schema again with
different terms." This would recover the 2 wrong-schema navigation failures automatically
without changing the core architecture.

**LEFT JOIN / INNER JOIN distinction**
The current "use LEFT JOIN for optional tables" rule causes CraftBeer failures where the gold
uses INNER JOIN for a complete-FK lookup. A more precise rule: "Use LEFT JOIN when the foreign
key is known to be nullable or when missing rows should be included; use INNER JOIN for
required lookups where every FK has a match." The synthesizer could annotate join paths with
this information.

---

## Conclusions

The key finding is that navigation (finding the right schema and tables) and logic
(writing correct SQL given those tables) are separate problems that require separate fixes.
Navigation is largely solved — embedding-based retrieval gets the agent to the right schema
97% of the time. Logic is the remaining bottleneck, accounting for all but 7 of the 26
remaining failures in Run 8.

The most effective single intervention was the LLM-synthesized guide: converting raw schema
dumps and prose business rules into a query-optimized reference document that expresses
rules as explicit SQL conditions. This alone unlocked the ability to fix downstream logic
errors with targeted prompt instructions, because the agent now had a reliable, consistent
representation of the rules to work from.

The most persistent remaining failure mode is rule over-application: the agent reads a
business rule in the guide and applies it to every query touching that schema, even when the
question doesn't ask for that filtered metric. This is a general problem in RAG-based agents
and requires either better rule-scoping in the guide or a reasoning step that explicitly asks
"does this question require this filter?"

For a production system, the right architecture is the one built here — offline synthesis,
embedding-based retrieval, agent with a small focused tool set — but with tighter iteration
loops on guide quality and a validation fallback (retry `find_schema` on 0-row results).

---

## Design decisions and tradeoffs

**Embeddings vs BM25 for guide retrieval.** Dense embeddings with `text-embedding-3-small`
work well (94–97% schema accuracy) and are fast at inference time (numpy dot product over 76
vectors). BM25 over guide text would likely improve recall for queries with exact schema-name
keywords but underperform for semantic synonyms ("batting average" → lahman). A hybrid
Reciprocal Rank Fusion approach would be the natural next step if embedding recall plateaued.

**Haiku vs Sonnet for synthesis.** Full Haiku regen (~$1.05) is affordable for iteration.
Sonnet produces noticeably better business-rule guides for complex schemas (financial has 4-way
status classification and rate formulas) but at 3× the cost. The selective Sonnet strategy
(Sonnet for top-failing schemas, Haiku for the rest) delivered the right tradeoff.

**Guide truncation.** With `max_tokens=8192`, 55/76 guides are still truncated. The section
ordering (join paths and business rules first) ensures the most critical content is preserved.
Long table reference sections for schemas with many columns get clipped. Increasing max_tokens
or splitting large guides would help for schemas like ErgastF1 and lahman.

**Context compression.** The agent truncates older tool results to 400 chars to stay within
the model's context window. This occasionally causes the agent to lose early schema information
on long reasoning chains. A smarter compression policy (never truncate the find_schema result)
would help.

**Generalization.** No fix names a specific schema, table, column, or threshold value. Every
change is a general mechanism: prompt framing, output instructions, synthesis rules, or
textualization logic. The guide synthesis pipeline works from the live database schema
and the customer's own markdown files — it doesn't require manual curation per schema and
would produce equivalent guides for an entirely different warehouse. The 64 visible hard
cases are a small fraction of the held-out test set; deliberate generality is the only
defence against overfitting. Wherever a candidate fix felt schema-specific (e.g., documenting
`forename`/`surname` vs `driverRef` as a one-off), it was reformulated as a general synthesis
prompt instruction or not implemented.
