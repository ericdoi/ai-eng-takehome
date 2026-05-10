# Hex AI Eng Takehome — Project Context

> Pure facts about the assignment, repo, and data. The action plan lives in `PLAN.md`.

## 1. The Assignment in One Paragraph

You are given a bare-bones SQL agent that uses OpenRouter (defaults to `openai/gpt-oss-120b:nitro` on Cerebras) and answers natural-language questions by submitting a single SQL query through a `submit_answer` tool. The agent is graded against two eval splits — `evals_easy.json` (64 cases, self-contained prompts) and `evals_hard.json` (64 cases, the **same questions stripped of the business rules** so the agent must consult `evaluation/data/guides/*.md` to get the right answer). The grader runs both queries (gold and submitted) against `hecks.duckdb` and uses **loose dataframe comparison**. Goal: improve the hard-set pass rate without overfitting to this database or these guides; a held-out test set will be used for final scoring. Time budget: ~4 hrs, cap 6.

## 2. What's in the Repo

| Path | Role |
|---|---|
| `framework/agent.py` | Generic tool-calling agent. Streams `AgentEvent`s, manages `Conversation`, has optional context compression. System prompt forces `submit_answer` usage. Max 30 iterations. |
| `framework/llm.py` | OpenRouter HTTP client with SSE streaming, retries on 429 / read timeouts, tool-call accumulation. Default config: `gpt-oss-120b:nitro`, temp 0.6, 100k max_tokens, 10s first-token timeout. |
| `framework/database.py` | DuckDB query helpers: `execute_query`, `validate_query` (sqlglot), `list_schemas`, `list_tables`, `describe_table`. **None of these are wired into the agent yet** — they're available for tools to use. |
| `framework/stream_printer.py` | Rich console renderer for events. |
| `tools/submit_answer.py` | The only tool registered today. Returns `ANSWER_SUBMITTED:<sql>` which signals agent termination. |
| `tools/your_cool_tool_here.py` | Empty stub — explicit invitation to add tools. |
| `interactive.py` | REPL via `uv run interactive --api-key …`. |
| `evaluation/evaluate.py` | Threaded evaluation runner (`uv run evaluate --concurrency 16`). Saves traces to `logs/run_<ts>/`. **`create_tools()` is the only place evaluation imports tools — wire new tools here.** |
| `evaluation/compare.py` | Loose dataframe equality — extra cols OK, column-name/order ignored, row order ignored, int/float tolerance ε=1e-4. |
| `evaluation/data/evals_easy.json` | 64 self-contained cases. |
| `evaluation/data/evals_hard.json` | 64 cases, business-rule-dependent. |
| `evaluation/data/guides/*.md` | 50 markdown business-rule files (~2,400 LOC total). |
| `hecks.duckdb` (635 MB, LFS zip) | Consolidated DuckDB; **76 schemas / 672 tables** drawn from CTU Relational. |

## 3. Data Surface

- **Database origin**: the schemas are drawn from the **CTU Prague Relational Learning Repository** ([relational.fel.cvut.cz](https://relational.fel.cvut.cz), [arXiv 1511.03086](https://arxiv.org/abs/1511.03086)) — a public collection of 148 multi-relational MySQL databases used for relational ML research. The takehome ships 76 of them in a single DuckDB file under per-database schemas. Useful because: original schema docs (table descriptions, FK graphs, dataset summaries) are public per dataset on that site, in case we need ground truth for sanity-checking. **Do not** rely on those external docs at runtime — the held-out test set may swap in arbitrary new databases.
- **Schemas**: 76, including `Airline`, `Credit`, `financial`, `lahman_2014`, `imdb_ijs`, `Chess`, `ErgastF1`, `CraftBeer`, `Hockey`, `Mondial`, `employee`, `Accidents`, `world`, `northwind`, `sakila`, `tpcc`, etc. Schemas are **case-sensitive** in DuckDB queries (e.g., `Airline.On_Time_On_Time_Performance_2016_1`). Use schema-qualified names in every query.
- **Guides**: 50 files (~2,400 LOC total). Each is keyed to a specific schema (e.g., `airline_operations.md` → `Airline`, `credit_card_operations.md` → `Credit`, `baseball_sabermetrics.md` → `lahman_2014`). They encode definitions like "on-time = ≤15 min late", "exclude `charge_amt = 0.01`", "`halloffame` table requires `inducted = 'Y'`", "thin routes <50 flights/yr". **The hard split removes those rules from the prompt** — the agent must find the right guide. Guides have consistent structure: a `# <Name> (<Schema> Database)` H1, then `##` sections with bulleted rules. Useful for chunking on `##` boundaries.
- **Eval data**: `easy[i]` and `hard[i]` typically share a gold query; the prompt is just terser in `hard`. There are 64 cases per split.
- **Schema/guide coverage**: only ~50 of the 76 schemas are exercised by the eval cases. The remaining ~26 schemas are noise the retriever has to filter past.

## 4. What "Loose Comparison" Lets You Get Away With

Reading `evaluation/compare.py` carefully (it's the actual oracle):

- Submitted DF must have **the same row count** and **at least as many columns** as gold.
- Each gold column must match some submitted column **as a multiset of normalized values** (sorted, after rounding floats to ~3-4 decimals). Column names and order don't matter.
- Extra submitted columns are free; you can defensively `SELECT col, col` or include extras.
- Empty gold dataframes raise — you cannot win an "expected 0 rows" case unless gold also returns rows.
- ε = 1e-4 tolerance; `int 1 == float 1.0`.

Implication: getting the right **set of values** is what counts; you don't have to mimic the gold query's column order or labels. This is friendly to LLM agents.

## 5. Failure Modes the Current Setup Has

1. **No exploration tools**. The only tool is `submit_answer`. The agent sees system prompt + user question; it has to guess schema/table/column names blind. Easy failure on 76 schemas / 672 tables.
2. **No access to the guides**. The hard split is unwinnable without them, yet nothing exposes the markdown files to the agent.
3. **No schema awareness in the system prompt** — model doesn't know what databases exist, doesn't know to use `schema.table`, doesn't know about case sensitivity.
4. **No SQL pre-flight**. The agent could submit a syntactically broken or empty-result query and lose silently.
5. **Default model `gpt-oss-120b`** is fast/cheap but not the strongest at long-horizon SQL planning.
6. **`temperature=0.6`** is high for deterministic SQL.
7. **Context compression off by default** — long exploration sessions will balloon prompt tokens.

## 6. Constraints from the README

- Don't edit `evaluation/evaluate.py` beyond adding tools to `create_tools()`.
- Don't edit the bundled guide files.
- Don't hand-maintain a schema map tailored only to this warehouse.
- The system must be **generally capable** — works for arbitrary warehouses + arbitrary guidance. A held-out test set will be used.
- Time budget: target ~4 hrs, cap 6.

## 7. APIs / Libraries Already Available

`pyproject.toml` already pulls in everything you'd plausibly need:

- `duckdb`, `polars`, `pyarrow`, `connectorx` (DB)
- `sqlglot[rs]` (parsing/validation/dialect)
- `httpx`, `tenacity` (HTTP/retry)
- `tiktoken` (token counting; useful for compression and token-based BM25)
- `tqdm`, `rich` (UX)

### OpenRouter

Docs: <https://openrouter.ai/docs>. Useful knobs:

- `:nitro` suffix = fastest provider routing.
- `provider` field in `OpenRouterConfig` lets you pin Cerebras / Groq / etc.
- Reasoning models need the `reasoning` field; the framework already passes it through.

### Default model: `gpt-oss-120b`

From the [model card](https://cdn.openai.com/pdf/419b6906-9da6-406c-a19d-1bb078ac7637/oai_gpt-oss_model_card.pdf) and arXiv 2508.10925: open-weight reasoning model, supports adjustable reasoning effort, full chain-of-thought, structured outputs, and is benchmarked specifically on tool-use (τ-bench retail) and coding (SWE-Bench Verified). Notably **strong at tool calling and coding** — close to o4-mini at high reasoning effort. This is good news for an introspect-then-SQL agent. Means the lift from a stronger model is probably smaller than the lift from better tools/prompting.

### Embeddings (for the Phase 3 fallback)

OpenRouter exposes a unified embeddings endpoint compatible with the OpenAI shape:

- **Endpoint**: `POST https://openrouter.ai/api/v1/embeddings` ([reference](https://openrouter.ai/docs/api/api-reference/embeddings/create-embeddings)).
- **Auth**: same `Authorization: Bearer $OPENROUTER_API_KEY` we already use; `Content-Type: application/json`. Reuse the existing `httpx` client and key plumbed through `OpenRouterConfig`.
- **Request body**: `{ model, input, encoding_format?, dimensions?, provider?, input_type? }`. `input` accepts a string, list of strings, or multimodal `content` arrays. Batch many texts in one POST (an array of strings; no documented hard cap, but plan ~100 per request). `dimensions` lets you truncate output vectors (handy for storage) on models that support Matryoshka representations.
- **Response shape**: OpenAI-style — `{ data: [{ embedding: number[], index, object }], model, usage }`.
- **Rate limits**: 429 on overload — implement exponential backoff. The framework's `tenacity` retry helpers in `framework/llm.py` already handle this pattern; copy the retryer.
- **Models worth knowing** (via [embedding-models collection](https://openrouter.ai/collections/embedding-models)):
  - `openai/text-embedding-3-small` — **1536-d, 8,191-token context, ~$0.02 per 1M input tokens** ([pricing](https://developers.openai.com/api/docs/models/text-embedding-3-small)). Strong default for English retrieval; cheapest. ~50 guides × small chunks ≪ 1M tokens, so a full re-index is well under a cent.
  - `openai/text-embedding-3-large` — 3072-d, ~$0.13 / 1M. Higher recall when small misses.
  - `qwen/qwen3-embedding-0.6b` — strong multilingual open-weight option; useful if we ever wanted to self-host.
  - `pplx-embed-v1-0.6B` / `pplx-embed-v1` — Perplexity's embedding family, tuned for web-scale retrieval.
  - `google/gemini-embedding-2-preview` — multimodal (text + image) with flexible output dims (128–3,072). Overkill here.
- **Local fallback**: if we want zero new network dependency, `sentence-transformers` `all-mpnet-base-v2` is the academic default cited in [Retrieval and Augmentation of Domain Knowledge for Text-to-SQL (arXiv 2510.02394)](https://arxiv.org/html/2510.02394v1). Adds a heavy dep though — only worth it if avoiding the API is a hard constraint.

### Vector store

For 50 guide files × tens of `##` chunks each, **don't add a vector DB**. A single NumPy matrix in memory (or a `.npz` cache file alongside the guides) does the job. Cosine ranking is one matmul.

## 8. Prior art relevant to the strategy

- **"The Death of Schema Linking?" — Maamari et al., NeurIPS 2024** ([paper](https://arxiv.org/html/2408.07702v2), [poster](https://neurips.cc/virtual/2024/103140)). Currently #1 on BIRD at 71.83% EX. Headline: with a strong enough LLM and a schema that fits in context, **explicit schema linking hurts more than it helps** (false negatives drop required columns). Our 76-schema warehouse is way too big to dump whole — but the per-schema picture (after we narrow to the right schema via a guide hit) usually fits. Implication: once we identify the right schema, prefer **giving the model the full schema dump** rather than a filtered subset.
- **"Retrieval and Augmentation of Domain Knowledge for Text-to-SQL" — arXiv 2510.02394 (Sept 2025)**. Studies retrieval of structured "domain statements" — a near-perfect mirror of our guide-file setup. Finding: **sub-string match retrieval beat both BM25 and dense embeddings** on BIRD-Dev when the corpus is short structured rule statements. Their best embedding model was `all-mpnet-base-v2`; n-gram thresholds 2–4 worked best. Direct implication: **for a Phase-3 fallback, hybrid (BM25 + sub-string n-gram match) may beat embeddings** on this exact data shape. Worth considering before paying for embeddings.
- **BIRD benchmark** ([bird-bench.github.io](https://bird-bench.github.io)). Closest public analog to our task: 12,751 NL/SQL pairs, 95 large DBs across 37 domains, evaluation by execution accuracy with **external knowledge hints** (their term for what we call "guides"). Patterns to borrow: knowledge hint → SQL pipelines, error-driven query repair, value retrieval (sampling concrete cell values to ground filters).
- **Spider 2.0** ([spider2-sql.github.io](https://spider2-sql.github.io), ICLR 2025 oral). Real enterprise text-to-SQL with cloud DBs (3,000+ cols). Best model (o1) only solves 23% on the agent setting. Sobering: the more agentic the task, the more LLMs struggle with nested schema and external docs. Reinforces "narrow scope first, retrieve docs, then SQL" over "throw everything at the model."
- **BM25 vs embeddings** ([ai.rs benchmark](https://ai.rs/ai-developer/bm25-vs-embeddings-keyword-search), [Reddit thread](https://www.reddit.com/r/Rag/comments/1rf7xf6/whats_your_experience_with_hybrid_retrieval/)). Consistent finding across product / technical / acronym-heavy corpora: **BM25 wins on exact / technical queries, embeddings win on vague/intent queries, hybrid wins overall**. Our guides are technical and acronym-heavy (`charge_amt`, `IBU`, `WHIP`). Strong prior that BM25 will be hard to beat for the *common* case, with embeddings only earning their keep on paraphrased queries ("severe delays" → "delays over 3 hours").
