"""Guide retrieval tools using BM25 search over chunked markdown guides."""

from __future__ import annotations

import math
import os
import re
from dataclasses import dataclass
from pathlib import Path

from framework.agent import Tool

_GUIDES_DIR = Path(os.environ.get(
    "GUIDES_DIR",
    str(Path(__file__).parent.parent / "evaluation" / "data" / "guides"),
))


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

@dataclass
class Chunk:
    file_path: str
    heading: str
    text: str
    tokens: list[str]


def _tokenize(text: str) -> list[str]:
    return re.findall(r'[a-z0-9_]+', text.lower())


def _chunk_file(path: Path) -> list[Chunk]:
    """Split a guide file into chunks on ## boundaries, keeping the H1 title."""
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines(keepends=True)

    # Extract H1 for context in every chunk
    h1 = ""
    for line in lines:
        if line.startswith("# "):
            h1 = line.strip()
            break

    chunks: list[Chunk] = []
    current_heading = h1 or path.stem
    current_lines: list[str] = [h1 + "\n"] if h1 else []

    for line in lines:
        if re.match(r'^#{2,3} ', line):
            if current_lines:
                text = "".join(current_lines).strip()
                if text:
                    chunks.append(Chunk(
                        file_path=str(path),
                        heading=current_heading,
                        text=text,
                        tokens=_tokenize(text),
                    ))
            current_heading = line.strip()
            current_lines = [h1 + "\n", line] if h1 else [line]
        else:
            current_lines.append(line)

    if current_lines:
        text = "".join(current_lines).strip()
        if text:
            chunks.append(Chunk(
                file_path=str(path),
                heading=current_heading,
                text=text,
                tokens=_tokenize(text),
            ))

    return chunks


# ---------------------------------------------------------------------------
# BM25
# ---------------------------------------------------------------------------

class _BM25Index:
    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75) -> None:
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        n = len(chunks)
        avg_dl = sum(len(c.tokens) for c in chunks) / max(n, 1)

        # Document frequency per term
        df: dict[str, int] = {}
        for chunk in chunks:
            for term in set(chunk.tokens):
                df[term] = df.get(term, 0) + 1

        self._idf: dict[str, float] = {
            term: math.log((n - freq + 0.5) / (freq + 0.5) + 1)
            for term, freq in df.items()
        }
        self._avg_dl = avg_dl

    def search(self, query: str, top_k: int = 5) -> list[tuple[Chunk, float]]:
        q_tokens = _tokenize(query)
        scored: list[tuple[Chunk, float]] = []
        for chunk in self.chunks:
            dl = len(chunk.tokens)
            tf: dict[str, int] = {}
            for t in chunk.tokens:
                tf[t] = tf.get(t, 0) + 1
            score = 0.0
            for term in q_tokens:
                if term not in self._idf:
                    continue
                f = tf.get(term, 0)
                score += self._idf[term] * (f * (self.k1 + 1)) / (
                    f + self.k1 * (1 - self.b + self.b * dl / self._avg_dl)
                )
            scored.append((chunk, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]


_index: _BM25Index | None = None


def _get_index() -> _BM25Index:
    global _index
    if _index is None:
        guides_dir = _GUIDES_DIR
        chunks: list[Chunk] = []
        if guides_dir.is_dir():
            for path in sorted(guides_dir.glob("*.md")):
                chunks.extend(_chunk_file(path))
        _index = _BM25Index(chunks)
    return _index


# ---------------------------------------------------------------------------
# Tool functions
# ---------------------------------------------------------------------------

def _search_guides_fn(query: str, top_k: int = 5) -> str:
    top_k = max(1, min(top_k, 10))
    idx = _get_index()
    if not idx.chunks:
        return "No guide files found. Check GUIDES_DIR."
    results = idx.search(query, top_k)
    if not results or results[0][1] == 0.0:
        return "No matching guide sections found."

    lines = [f"Top {len(results)} guide sections for: {query!r}\n"]
    for i, (chunk, score) in enumerate(results, 1):
        snippet = chunk.text[:300].replace("\n", " ")
        lines.append(
            f"{i}. [{chunk.heading}] (score={score:.2f})\n"
            f"   File: {chunk.file_path}\n"
            f"   Snippet: {snippet}..."
        )
    return "\n".join(lines)


def _read_guide_fn(path: str) -> str:
    p = Path(path)
    if not p.exists():
        # Try treating path as a filename stem or relative to guides dir
        alt = _GUIDES_DIR / p.name
        if alt.exists():
            p = alt
        else:
            return f"Guide file not found: {path}"
    return p.read_text(encoding="utf-8")


SEARCH_GUIDES = Tool(
    name="search_guides",
    description=(
        "Search the business-rule guide files using BM25 keyword search. "
        "Returns the most relevant guide sections for your query. "
        "Use domain terms, schema names, or concepts from the question. "
        "Always call this before writing SQL for questions that may involve business rules."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search terms — domain concepts, schema names, or keywords from the question.",
            },
            "top_k": {
                "type": "integer",
                "description": "Number of results to return (default 5, max 10).",
                "default": 5,
            },
        },
        "required": ["query"],
    },
    function=_search_guides_fn,
)

READ_GUIDE = Tool(
    name="read_guide",
    description=(
        "Read the full contents of a guide file returned by search_guides. "
        "Use this to get all business rules for a specific domain before writing SQL."
    ),
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Full file path as returned by search_guides.",
            },
        },
        "required": ["path"],
    },
    function=_read_guide_fn,
)
