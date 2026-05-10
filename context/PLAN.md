# Hex AI Eng Takehome — Plan of Attack

> Pure plan. Facts about the repo and data live in `CONTEXT.md`.

## Guiding principles

- **Measure before changing.** Establish a baseline and per-case failure mode breakdown before adding capability. Optimize the loop, not your hunch.
- **Build the failure microscope alongside the agent.** Every change should be cheap to evaluate and easy to attribute.
- **Stay generic.** No hand-built schema maps, no edits to the guides — held-out test set will punish overfitting.
- **Default to the simple thing first.** Reach for embeddings / reasoning models / extra deps only if the simpler thing measurably plateaus.

## Phase 0 — Baseline & debug harness (do these first)

### 0.1 Run the evals untouched and record a baseline

- `uv run evaluate --api-key … --split easy --concurrency 16`
- `uv run evaluate --api-key … --split hard --concurrency 16`
- Save the printed summary + the `logs/run_<ts>/` directory. This is the floor; everything else is measured against it. Expect easy ≫ hard since the hard prompts strip the rules.

### 0.2 Build a trace inspector

The eval already writes one JSON trace per case to `logs/run_<ts>/<split>/<uuid>.json`. They contain every event including the submitted query and the failure type. Build a small analysis script (e.g. `scripts/analyze_run.py`) that, given a run dir:

- Buckets results by `failure_type` (`MISMATCH`, `NO_SUBMISSION`, `SQL_ERROR`, `AGENT_ERROR`, `INFRA_ERROR`, `EXCEPTION`).
- For each failed case, prints: prompt, gold query, submitted query, the diff between gold/submitted column counts and row counts, the first DuckDB error if any.
- Sorts cases by "cheapest to fix next" — e.g. group by guide-file the gold query implies (regex the schema name), so we can see "8 of 12 hard failures are in `Airline`".
- Dumps a CSV of `(case_idx, prompt, schema_used, failure_type, error)` so we can diff between runs.

This is the single most leveraged investment. Without it, every later change is guesswork.

### 0.3 Add a tiny per-case rerun helper

Reuse the existing `Agent` to rerun one specific eval case from the CLI (e.g. `scripts/rerun_case.py --split hard --idx 7`) and stream the events with `StreamPrinter`. Lets you iterate on prompt/tool changes without running all 64 cases.

## Phase 1 — Minimum viable agent (high confidence wins)

Target: agent can introspect the warehouse and consult guides. Most of the gap between current score and a respectable score is here.

### 1.1 Database introspection tools

Wrap the existing helpers in `framework/database.py` as `Tool` objects in `tools/`:

- `list_schemas()`
- `list_tables(schema)`
- `describe_table(schema, table)` — returns columns + types (already supported)
- `sample_rows(schema, table, limit≤20)` — small `LIMIT` query, gated to read-only
- `run_sql(query)` — read-only DuckDB exec, returns row count + first ~20 rows in markdown. Hard cap on output bytes so a runaway query can't bomb the context. Pass DuckDB error messages through verbatim — they're high-signal for the model.

Wire all of these into both `interactive.py::create_tools` and `evaluation/evaluate.py::create_tools`.

### 1.2 Guide retrieval tools (start with BM25)

Two tools:

- `search_guides(query, top_k=5)` — returns `(file, heading_path, score, snippet)` for top-k chunks across `evaluation/data/guides/*.md`. Chunk on `##` headers.
- `read_guide(path)` — fetch full file content for a path returned by `search_guides`.

Implementation: tokenize with `tiktoken` (already a dep), score with BM25 (rank_bm25 is the obvious dep, but a ~30-line pure-Python BM25 keeps deps unchanged). Build the index once at process start; it's read-only and thread-safe. Make the guides directory configurable via env var or constant — don't hardcode the takehome path, since the held-out set may swap it.

### 1.3 Prompt updates

Update `Agent._get_system_message` to teach the model:

- "DuckDB warehouse with many schemas. Always use `schema.table`. Names are case-sensitive."
- Workflow: (a) `search_guides` with key terms from the question, (b) `read_guide` on hits, (c) `list_schemas` / `list_tables` / `describe_table` to find columns, (d) optionally `run_sql` to preview, (e) `submit_answer`.
- Grader is loose: row count must match, extra columns OK, column names/order ignored. Don't waste turns matching the gold's column labels.

### 1.4 Config tweaks

- Drop `temperature` to 0.0–0.2.
- Enable `compress_context` (`keep_recent=3`, `max_chars≈400`) so schema dumps and SQL previews don't dominate the prompt.
- Leave `max_iterations` at 30 unless traces show exhaustion.

### 1.5 Re-run + analyze

Re-run both splits at `--concurrency 16`. Diff the per-case CSV against baseline. Expected: hard pass rate jumps significantly. If it doesn't, the trace inspector tells us why before we add more machinery.

## Phase 2 — Iterate on the long tail

Drive the next round of changes from the trace inspector, not from intuition. Likely categories and fixes:

- **Wrong guide retrieved** → tune chunking, raise `top_k`, add a re-rank step where the LLM picks among candidate guide headings before reading.
- **Right guide but rule ignored** → require an explicit "rules I'm applying" note in the assistant message before `submit_answer` (a small CoT scaffold). Or insert an automatic verification turn: rerun the SQL, ask the model "does this match every rule from the guide?".
- **Wrong table / column** → add a `search_columns(keyword)` tool that scans `information_schema.columns` for keyword matches across all schemas. This is still generic.
- **Empty result / row-count mismatch** → require a `run_sql` preview before `submit_answer`. Refuse `submit_answer` (in the tool itself) if the agent hasn't run a successful preview in this turn.
- **SQL parse errors** → optional `validate_sql` tool using sqlglot before submission.

Each of these is a 10–30 minute change. The trace inspector decides which one is worth doing next.

## Phase 3 — Stretch ideas (only if Phases 1–2 plateau)

### 3.1 Embeddings for guide retrieval (your suggestion — keep as a fallback)

If BM25 misses on paraphrased prompts ("severe delays" → "delays over 3 hours") show up as a meaningful failure bucket, swap in embeddings.

**API to use** (details in `CONTEXT.md § Embeddings`):

- `POST https://openrouter.ai/api/v1/embeddings` — same Bearer auth and `httpx`/`tenacity` retry plumbing as the chat client. Reuse `OpenRouterConfig.api_key`.
- Default model: `openai/text-embedding-3-small` (1536-d, 8,191-token context, ~$0.02 / 1M tokens). A full re-index of all 50 guides costs well under a cent.
- Upgrade path: `openai/text-embedding-3-large` if recall is still short. `qwen/qwen3-embedding-0.6b` if we ever want to self-host.
- Batch many texts per POST (array `input`); cache the result matrix to `.cache/guide_embeddings.npz`. No vector DB — one NumPy cosine matmul.

**Loop**:

- One-time: chunk guides on `##`, embed each chunk + its heading path, persist as `(chunk_text, heading, schema_hint, vector)`.
- Query: embed the user question, cosine-rank, return top-k.
- Hybrid: combine with BM25 via Reciprocal Rank Fusion (RRF) — hybrid almost always beats either alone in retrieval benchmarks.
- Schema embeddings: same idea over per-table summary strings (`{schema} {table} columns: {col1, col2, …}`) for cases where the question doesn't share tokens with any identifier.

**Why fallback rather than default**

- Adds a network round-trip per question and a cache-invalidation surface.
- Prior art for this exact data shape ([arXiv 2510.02394](https://arxiv.org/html/2510.02394v1)) found **sub-string n-gram matching beats both BM25 and dense embeddings** when the corpus is short structured rule statements (n=2–4). That's a stronger argument for adding sub-string matching as the *first* upgrade past BM25, with embeddings as the *second*.
- BM25-vs-embeddings benchmarks on technical / acronym-heavy corpora consistently show BM25 winning the common case ([ai.rs](https://ai.rs/ai-developer/bm25-vs-embeddings-keyword-search)). Our guides are full of identifiers like `charge_amt`, `IBU`, `WHIP`, `inducted = 'Y'` — BM25's natural strength.
- The trace inspector from Phase 0 tells us *exactly* which prompts BM25 misses on; we add embeddings only if the misses are paraphrase-shaped.

**Decision criteria**: ship embeddings if, after Phase 1, the inspector shows ≥5 hard-split failures attributable to retrieval miss on paraphrased queries. Otherwise stay on BM25 (+ optional sub-string match) and spend the iteration budget elsewhere.

### 3.2 Stronger model on the long tail

Default `gpt-oss-120b` is already a strong tool-using reasoning model (close to o4-mini on τ-bench), so the lift from a model swap is probably modest — but cheap to test. Try a reasoning model (`openai/gpt-5`, `anthropic/claude-sonnet-4.5`, `deepseek/deepseek-r1`) only on cases that failed at default settings. Framework already supports `reasoning` and per-config models.

Alternative: try cranking `reasoning.effort = "high"` on the default model first — same model, more thinking budget. Often a better $/accuracy trade than swapping models entirely.

### 3.3 Tool ergonomics polish

- Combine `describe_table` + `sample_rows` into one tool to halve round-trips.
- Truncate `run_sql` output more aggressively (e.g. summarize column dtypes + 5 rows) once compression kicks in.

### 3.4 Schema dump over schema linking (per ["Death of Schema Linking?"](https://arxiv.org/html/2408.07702v2))

Once a guide hit identifies the relevant schema, **dump the full schema** for that one schema into the model's context rather than relying on the agent to incrementally `describe_table` its way to the right columns. The BIRD-leading approach found that schema linking introduces false negatives that hurt more than the irrelevant-column noise it removes. Single-schema dumps for our warehouse fit comfortably in `gpt-oss-120b`'s context.

## Phase 4 — Writeup

The README requires a prose writeup alongside the forked repo. Suggested structure:

1. **Baseline numbers** (Phase 0).
2. **What I changed and why**, in the order I changed them, with the per-phase score delta.
3. **Tradeoffs**: BM25 vs embeddings, prompt scaffolding vs more tools, reasoning model cost.
4. **What I'd do next** with another day (probably the embedding fallback + a real verification loop).
5. **Generalization notes**: how the design avoids overfitting to this warehouse + these guides.

## Risk register

- **Schema case sensitivity** in DuckDB will silently break queries. System prompt must call this out.
- **`L_*` lookup tables** in `Airline` are tempting distractions; gold queries usually hit the fact table. Guide retrieval anchors the agent.
- **Token budget** — a flat `list_schemas` is fine; never dump all 76 × N tables at once.
- **Thread safety** at `--concurrency 16`: BM25 index must be read-only after build; DuckDB connection-per-call (current pattern) is already safe.
- **Held-out test set** — anything tuned to the visible 64 hard cases that doesn't generalize hurts you. Treat splits as dev sets.
- **Empty-gold cases** — `compare.py` raises on empty gold, so some cases may be unwinnable through no fault of the agent. Note in writeup if observed.

## Deliverables checklist

- [ ] Phase 0 baseline numbers + trace inspector script committed.
- [ ] Phase 1 tools + prompt + config committed; re-run numbers recorded.
- [ ] Phase 2 iterations driven by trace inspector, each with before/after.
- [ ] Writeup (PDF or doc): choices, tradeoffs, ablations, score progression, what's next.
- [ ] Fork link emailed to recruiter.
