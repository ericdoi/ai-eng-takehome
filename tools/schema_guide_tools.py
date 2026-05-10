"""Embedding-based schema guide retrieval for the SQL agent."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import numpy as np

from framework.agent import Tool

_GENERATED_GUIDES_DIR = Path(os.environ.get(
    "GENERATED_GUIDES_DIR",
    str(Path(__file__).parent.parent / "evaluation" / "data" / "generated_guides"),
))

_SCORE_GAP_THRESHOLD = 0.05  # return top-2 when gap between 1st and 2nd is < this


@lru_cache(maxsize=1)
def _load_index() -> tuple[list[str], np.ndarray] | None:
    """Load schema names and L2-normalized embeddings from disk. Returns None if not ready."""
    npz_path = _GENERATED_GUIDES_DIR / "embeddings.npz"
    if not npz_path.exists():
        return None
    data = np.load(str(npz_path), allow_pickle=False)
    schema_names: list[str] = data["schema_names"].tolist()
    embeddings: np.ndarray = data["embeddings"].astype(np.float32)
    return schema_names, embeddings


def _embed_query(query: str, api_key: str) -> np.ndarray | None:
    """Embed a query string via OpenRouter. Returns L2-normalized vector or None on error."""
    try:
        import httpx  # local import to avoid loading at module level when not needed
        resp = httpx.post(
            "https://openrouter.ai/api/v1/embeddings",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"model": "openai/text-embedding-3-small", "input": query},
            timeout=15.0,
        )
        resp.raise_for_status()
        vec = np.array(resp.json()["data"][0]["embedding"], dtype=np.float32)
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec
    except Exception:
        return None


def _find_schema_fn(query: str) -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        return "Error: OPENROUTER_API_KEY not set"

    index = _load_index()
    if index is None:
        return (
            "Generated schema guides not found. "
            "Run scripts/build_schema_guides.py first."
        )

    schema_names, embeddings = index

    q_vec = _embed_query(query, api_key)
    if q_vec is None:
        return "Error: could not embed query (check API key and connectivity)"

    scores: np.ndarray = embeddings @ q_vec  # cosine similarities (already normalized)
    top_indices = np.argsort(scores)[::-1]

    best_idx = int(top_indices[0])
    best_score = float(scores[best_idx])
    best_schema = schema_names[best_idx]

    guides_to_return: list[str] = [best_schema]

    # Return top-2 when scores are close
    if len(top_indices) > 1:
        second_idx = int(top_indices[1])
        second_score = float(scores[second_idx])
        if (best_score - second_score) < _SCORE_GAP_THRESHOLD:
            guides_to_return.append(schema_names[second_idx])

    results: list[str] = []
    for schema in guides_to_return:
        guide_path = _GENERATED_GUIDES_DIR / f"{schema}.md"
        if guide_path.exists():
            results.append(f"=== Schema: {schema} ===\n\n{guide_path.read_text(encoding='utf-8')}")
        else:
            results.append(f"=== Schema: {schema} ===\n\n(guide file missing)")

    header = f"Best match: {best_schema} (score={best_score:.3f})"
    if len(guides_to_return) > 1:
        header += f"\nAlso returning: {guides_to_return[1]} (scores are close)"
    header += "\n\n"

    return header + "\n\n---\n\n".join(results)


FIND_SCHEMA = Tool(
    name="find_schema",
    description=(
        "Find the schema guide most relevant to your question. "
        "Returns the full guide including exact table names, column names, join paths, "
        "business rules as SQL conditions, and a synonym glossary. "
        "Call this first — it gives you everything you need to write the SQL."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Your question or key domain terms from it (e.g. 'on-time flights', 'dominant language countries', 'credit card charge-off').",
            },
        },
        "required": ["query"],
    },
    function=_find_schema_fn,
)
