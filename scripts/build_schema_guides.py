#!/usr/bin/env python3
"""Build LLM-synthesized schema guides and embeddings for the SQL agent.

Reads the DuckDB schema, fuses structure with existing guide files (business rules),
calls an LLM to synthesize one guide per schema, then embeds all guides via
OpenRouter and saves embeddings.npz for fast cosine-similarity retrieval.

Usage:
    source .env && uv run python scripts/build_schema_guides.py
    uv run python scripts/build_schema_guides.py --skip-llm        # re-embed only
    uv run python scripts/build_schema_guides.py --schema world    # single schema

Cost: ~$1.05 per full 76-schema regeneration (anthropic/claude-haiku-4-5 synthesis +
openai/text-embedding-3-small embeddings via OpenRouter, measured 2026-05-10).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import duckdb
import httpx
import numpy as np
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------

_ROOT = Path(__file__).parent.parent
DATABASE_PATH = _ROOT / "hecks.duckdb"
GUIDES_DIR = _ROOT / "evaluation" / "data" / "guides"
OUTPUT_DIR = _ROOT / "evaluation" / "data" / "generated_guides"

API_BASE = "https://openrouter.ai/api/v1"
SYNTHESIS_MODEL = "anthropic/claude-haiku-4-5"
EMBEDDING_MODEL = "openai/text-embedding-3-small"

MAX_DISTINCT_VALUES = 20
SAMPLE_LIMIT = 5
LLM_DELAY = 0.4  # seconds between synthesis calls

# ---------------------------------------------------------------------------
# Guide-schema mapping
# ---------------------------------------------------------------------------

# Overrides for guides whose filenames don't map cleanly via H1 extraction.
# Value is the list of schema names this guide covers.
GUIDE_OVERRIDES: dict[str, list[str]] = {
    "movie_ratings.md":       ["imdb_MovieLens"],  # H1 says "IMDB / MovieLens"
    "hockey_analytics.md":    ["Hockey"],           # no parenthetical in H1
    "financial_operations.md": ["financial"],       # no parenthetical in H1
    "basketball_reporting.md": [],                  # ambiguous; skip
    "yelp_review_standards.md": [],                # no matching schema; skip
}


def _extract_schemas_from_h1(h1: str, known_schemas: set[str]) -> list[str]:
    """Extract schema name(s) from an H1 like 'Title (Schema / Other Database)'."""
    match = re.search(r"\(([^)]+)\)", h1)
    if not match:
        return []
    content = match.group(1)
    parts = [p.strip() for p in content.split(" / ")]
    lower_map = {s.lower(): s for s in known_schemas}
    result: list[str] = []
    for part in parts:
        name = re.sub(r"\s+Databases?$", "", part, flags=re.IGNORECASE).strip()
        canonical = lower_map.get(name.lower())
        if canonical and canonical not in result:
            result.append(canonical)
    return result


def build_guide_mapping(known_schemas: set[str]) -> dict[str, Path | None]:
    """Return schema_name → guide_path (or None if no guide exists)."""
    schema_to_guide: dict[str, Path | None] = {s: None for s in known_schemas}

    for guide_path in sorted(GUIDES_DIR.glob("*.md")):
        fname = guide_path.name
        if fname in GUIDE_OVERRIDES:
            schemas = GUIDE_OVERRIDES[fname]
        else:
            h1 = ""
            for line in guide_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("# "):
                    h1 = line[2:].strip()
                    break
            schemas = _extract_schemas_from_h1(h1, known_schemas)

        for schema in schemas:
            if schema in schema_to_guide:
                schema_to_guide[schema] = guide_path

    return schema_to_guide


# ---------------------------------------------------------------------------
# Schema textualization
# ---------------------------------------------------------------------------

def textualize_schema(conn: duckdb.DuckDBPyConnection, schema: str) -> str:
    """Build a structured text block describing all tables and columns in schema."""
    tables = conn.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema = ? AND table_type = 'BASE TABLE' ORDER BY table_name",
        [schema],
    ).fetchall()
    table_names = [row[0] for row in tables]

    if not table_names:
        return f"Schema: {schema}\n(no tables found)"

    lines: list[str] = [
        f"Schema: {schema}",
        f"Tables: {', '.join(table_names)}",
        "",
    ]

    for table in table_names:
        cols = conn.execute(
            "SELECT column_name, data_type FROM information_schema.columns "
            "WHERE table_schema = ? AND table_name = ? ORDER BY ordinal_position",
            [schema, table],
        ).fetchall()

        lines.append(f"Table: {schema}.{table} ({len(cols)} columns)")
        lines.append("Columns:")

        for col_name, col_type in cols:
            col_line = f"  {col_name}  {col_type}"
            is_char = any(kw in col_type.upper() for kw in ("CHAR", "TEXT", "VARCHAR"))
            if is_char:
                try:
                    count_row = conn.execute(
                        f'SELECT COUNT(DISTINCT "{col_name}") FROM "{schema}"."{table}"'
                    ).fetchone()
                    count = count_row[0] if count_row else 0
                    if 0 < count <= MAX_DISTINCT_VALUES:
                        vals = conn.execute(
                            f'SELECT DISTINCT "{col_name}" FROM "{schema}"."{table}" '
                            f'WHERE "{col_name}" IS NOT NULL ORDER BY 1 '
                            f"LIMIT {MAX_DISTINCT_VALUES}"
                        ).fetchall()
                        val_strs = [str(v[0]) for v in vals]
                        col_line += f"  — values: {', '.join(val_strs)}"
                except Exception:
                    pass
            lines.append(col_line)

        # Sample rows
        try:
            import pandas as pd  # noqa: PLC0415
            sample: pd.DataFrame = conn.execute(
                f'SELECT * FROM "{schema}"."{table}" LIMIT {SAMPLE_LIMIT}'
            ).fetchdf()
            if not sample.empty:
                # Truncate wide string columns so the table doesn't explode
                for c in sample.select_dtypes(include="str").columns:
                    sample[c] = sample[c].astype(str).str[:60]
                lines.append(f"\nSample rows ({table}):")
                lines.append(sample.to_string(index=False, max_colwidth=60))
        except Exception:
            pass

        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# LLM synthesis
# ---------------------------------------------------------------------------

_SYNTHESIS_SYSTEM = (
    "You are a database documentation expert writing reference guides for an AI SQL agent. "
    "Be precise. Use exact names. Never invent column names not present in the schema."
)

_SYNTHESIS_USER = """\
Here is the full schema structure for the `{schema}` schema:

<schema>
{textualized}
</schema>

{rules_section}

Write a reference guide for an AI SQL agent querying this schema. Be concise — \
omit obvious columns (id, name, description) unless they have non-obvious semantics or \
important enumerated values.

CRITICAL: Every table reference in SQL snippets MUST use the fully-qualified form \
`{schema}.TableName`. Never use bare table names in SQL. For example:
  ✓ FROM {schema}.results r JOIN {schema}.drivers d ON r.driverId = d.driverId
  ✗ FROM results r JOIN drivers d ON r.driverId = d.driverId

Write the sections in this order (most important first):

1. **Schema summary**: one sentence describing what this schema contains.

2. **Join paths**: exact SQL JOIN snippets (fully-qualified) for common table combinations.

3. **Business rules as SQL** (if rules provided): each rule as the exact SQL condition \
or filter. Format:
   - Rule: "language percentage exceeds 90%" → `WHERE cl.Percentage > 90`
   - Rule: "on-time flight" → `WHERE ArrDelayMinutes <= 15`

4. **Synonym glossary**: map common question terms to exact schema identifiers.
   Format: "career hits" → `SUM({schema}.batting.H)`, "dominant language" → `WHERE Percentage > 90`

5. **Table reference** (for each table):
   - Qualified name `{schema}.TableName`, plain-English meaning, synonym names
   - Only columns with non-obvious semantics, important enum values, or tricky joins
   - Notable enumerated values (exact strings from sample data)

Keep the guide focused and scannable. Do not add caveats or padding."""


def synthesize_guide(
    client: httpx.Client,
    schema: str,
    textualized: str,
    guide_content: str | None,
) -> str:
    """Call the LLM to produce a comprehensive schema guide."""
    rules_section = ""
    if guide_content:
        rules_section = (
            "Here are the business rules for this schema:\n\n"
            f"<rules>\n{guide_content}\n</rules>"
        )

    user_msg = _SYNTHESIS_USER.format(
        schema=schema,
        textualized=textualized,
        rules_section=rules_section,
    )

    for attempt in range(3):
        try:
            resp = client.post(
                f"{API_BASE}/chat/completions",
                json={
                    "model": SYNTHESIS_MODEL,
                    "messages": [
                        {"role": "system", "content": _SYNTHESIS_SYSTEM},
                        {"role": "user", "content": user_msg},
                    ],
                    "max_tokens": 8192,
                    "temperature": 0.0,
                },
                timeout=90.0,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                wait = 5 * (2**attempt)
                tqdm.write(f"    Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
        except Exception as e:
            if attempt < 2:
                tqdm.write(f"    Retry {attempt + 1}/3 for {schema}: {e}")
                time.sleep(3)
            else:
                raise RuntimeError(f"Synthesis failed for {schema}: {e}") from e

    raise RuntimeError(f"Synthesis failed after 3 attempts for {schema}")


# ---------------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------------

def embed_texts(
    client: httpx.Client,
    texts: list[str],
    batch_size: int = 20,
) -> np.ndarray:
    """Embed texts and return L2-normalized (N, D) float32 array."""
    all_embeddings: list[list[float]] = []

    for i in tqdm(range(0, len(texts), batch_size), desc="Embedding batches"):
        batch = texts[i : i + batch_size]
        resp = client.post(
            f"{API_BASE}/embeddings",
            json={"model": EMBEDDING_MODEL, "input": batch},
            timeout=60.0,
        )
        resp.raise_for_status()
        items = resp.json()["data"]
        for item in sorted(items, key=lambda x: x["index"]):
            all_embeddings.append(item["embedding"])

    arr = np.array(all_embeddings, dtype=np.float32)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    return arr / np.where(norms > 0, norms, 1.0)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Build schema guides and embeddings")
    parser.add_argument(
        "--skip-llm",
        action="store_true",
        help="Skip LLM synthesis — re-embed existing .md files only",
    )
    parser.add_argument(
        "--skip-embed",
        action="store_true",
        help="Skip embedding generation",
    )
    parser.add_argument(
        "--schema",
        help="Generate for a single schema only (useful for spot-checks)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=8,
        help="Number of parallel LLM synthesis calls (default: 8)",
    )
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Connecting to database...")
    conn = duckdb.connect(str(DATABASE_PATH), read_only=True)

    all_schemas: list[str] = [
        row[0]
        for row in conn.execute(
            "SELECT DISTINCT table_schema FROM information_schema.tables "
            "WHERE table_schema NOT IN ('information_schema', 'pg_catalog') "
            "ORDER BY table_schema"
        ).fetchall()
    ]

    if args.schema:
        if args.schema not in all_schemas:
            print(f"ERROR: Schema '{args.schema}' not found", file=sys.stderr)
            sys.exit(1)
        all_schemas = [args.schema]

    print(f"Found {len(all_schemas)} schemas")

    known_set = set(all_schemas)
    guide_mapping = build_guide_mapping(known_set)
    matched = sum(1 for v in guide_mapping.values() if v is not None)
    print(f"Guide matches: {matched}/{len(all_schemas)} schemas have a business-rule guide")

    # Print the mapping for transparency
    for schema, path in sorted(guide_mapping.items()):
        if path:
            print(f"  {schema:30s} ← {path.name}")

    if not args.skip_llm:
        http_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/hex-inc/takehome",
        }

        schemas_to_run = [
            s for s in all_schemas
            if args.schema or not (OUTPUT_DIR / f"{s}.md").exists()
        ]
        skipped = len(all_schemas) - len(schemas_to_run)
        if skipped:
            print(f"Skipping {skipped} already-generated schemas")

        def _worker(schema: str) -> tuple[str, str | None]:
            """Textualize + synthesize one schema. Returns (schema, error_or_None)."""
            out_path = OUTPUT_DIR / f"{schema}.md"
            guide_path = guide_mapping.get(schema)
            guide_content = (
                guide_path.read_text(encoding="utf-8") if guide_path else None
            )
            # Each thread gets its own DB connection (DuckDB read-only is safe)
            thread_conn = duckdb.connect(str(DATABASE_PATH), read_only=True)
            try:
                textualized = textualize_schema(thread_conn, schema)
            finally:
                thread_conn.close()

            with httpx.Client(headers=http_headers, timeout=120.0) as thread_client:
                guide_text = synthesize_guide(thread_client, schema, textualized, guide_content)

            out_path.write_text(guide_text, encoding="utf-8")
            return schema, None

        with tqdm(total=len(schemas_to_run), desc="Synthesizing guides") as bar:
            with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
                futures = {pool.submit(_worker, s): s for s in schemas_to_run}
                for fut in as_completed(futures):
                    schema = futures[fut]
                    try:
                        _, err = fut.result()
                        if err:
                            tqdm.write(f"  ERROR {schema}: {err}")
                        else:
                            tqdm.write(f"  Done: {schema}")
                    except Exception as exc:
                        tqdm.write(f"  EXCEPTION {schema}: {exc}")
                    bar.update(1)

    conn.close()
    print(f"\nGuides written to: {OUTPUT_DIR}")
    guide_count = len(list(OUTPUT_DIR.glob("*.md")))
    print(f"Total guide files: {guide_count}")

    if args.skip_embed:
        return

    print("\nGenerating embeddings...")
    guide_files = sorted(OUTPUT_DIR.glob("*.md"))
    if not guide_files:
        print("No guide files found — skipping embeddings")
        return

    schema_names = [f.stem for f in guide_files]
    texts = [f.read_text(encoding="utf-8") for f in guide_files]

    http_headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/hex-inc/takehome",
    }
    with httpx.Client(headers=http_headers, timeout=120.0) as client:
        embeddings = embed_texts(client, texts)

    npz_path = OUTPUT_DIR / "embeddings.npz"
    np.savez(
        str(npz_path),
        schema_names=np.array(schema_names),
        embeddings=embeddings,
    )
    print(f"Embeddings saved: {npz_path}")
    print(f"Matrix shape: {embeddings.shape}")


if __name__ == "__main__":
    main()
