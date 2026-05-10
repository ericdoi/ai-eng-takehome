#!/usr/bin/env python3
"""Analyze an evaluation run directory.

Usage:
    uv run python scripts/analyze_run.py logs/run_<ts>/
    uv run python scripts/analyze_run.py logs/run_<ts>/ --split hard
    uv run python scripts/analyze_run.py logs/run_<ts>/ --csv out.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


# ---------------------------------------------------------------------------
# SQL extraction helpers
# ---------------------------------------------------------------------------

def extract_schema(query: str) -> str:
    """Best-effort: return the first schema name found in a SQL query.

    Looks only in FROM/JOIN clauses and requires names ≥3 chars to skip aliases.
    """
    skip = {"information_schema", "pg_catalog", "main"}
    for m in re.finditer(
        r'(?:FROM|JOIN)\s+["`]?([A-Za-z_][A-Za-z0-9_]*)["`]?\s*\.',
        query, re.IGNORECASE,
    ):
        name = m.group(1)
        if name.lower() not in skip and len(name) >= 3:
            return name
    return "(unknown)"


def extract_schema_table_pairs(query: str) -> set[tuple[str, str]]:
    """Extract all (schema, table) pairs from FROM/JOIN clauses of a SQL query."""
    skip = {"information_schema", "pg_catalog", "main"}
    pairs: set[tuple[str, str]] = set()
    for m in re.finditer(
        r'(?:FROM|JOIN)\s+["`]?([A-Za-z_][A-Za-z0-9_]*)["`]?\s*\.\s*["`]?([A-Za-z_][A-Za-z0-9_]*)["`]?',
        query, re.IGNORECASE,
    ):
        schema, table = m.group(1), m.group(2)
        if schema.lower() not in skip:
            pairs.add((schema, table))
    return pairs


# ---------------------------------------------------------------------------
# Trace analysis helpers
# ---------------------------------------------------------------------------

def get_tool_calls(events: list[dict]) -> list[dict]:
    """Return list of {name, args} for every TOOL_CALL_PARSED event."""
    return [
        {"name": e["data"]["name"], "args": e["data"].get("arguments", {})}
        for e in events
        if e["type"] == "TOOL_CALL_PARSED"
    ]


def schemas_explored(tool_calls: list[dict]) -> set[str]:
    """Schemas the agent actually queried (via list_tables / describe_table / sample_rows)."""
    schemas: set[str] = set()
    for tc in tool_calls:
        if tc["name"] in ("list_tables", "describe_table", "sample_rows"):
            s = tc["args"].get("schema")
            if s:
                schemas.add(s)
    return schemas


def tables_explored(tool_calls: list[dict]) -> set[tuple[str, str]]:
    """(schema, table) pairs the agent described or sampled."""
    tables: set[tuple[str, str]] = set()
    for tc in tool_calls:
        if tc["name"] in ("describe_table", "sample_rows"):
            s = tc["args"].get("schema")
            t = tc["args"].get("table")
            if s and t:
                tables.add((s, t))
    return tables


def guides_read(tool_calls: list[dict]) -> list[str]:
    """Filenames of guides read via read_guide (de-duplicated, order preserved)."""
    seen: set[str] = set()
    result: list[str] = []
    for tc in tool_calls:
        if tc["name"] == "read_guide":
            name = Path(tc["args"].get("path", "")).stem
            if name not in seen:
                seen.add(name)
                result.append(name)
    return result


def tool_sequence_str(tool_calls: list[dict]) -> str:
    """Compact human-readable summary of the tool call sequence."""
    parts: list[str] = []
    for tc in tool_calls:
        name = tc["name"]
        args = tc["args"]
        if name == "list_schemas":
            parts.append("list_schemas")
        elif name == "list_tables":
            parts.append(f"list_tables({args.get('schema', '?')})")
        elif name == "describe_table":
            parts.append(f"describe({args.get('schema', '?')}.{args.get('table', '?')})")
        elif name == "sample_rows":
            parts.append(f"sample({args.get('schema', '?')}.{args.get('table', '?')})")
        elif name == "search_guides":
            parts.append("search_guides")
        elif name == "read_guide":
            parts.append(f"read_guide({Path(args.get('path', '')).stem})")
        elif name == "run_sql":
            parts.append("run_sql")
        elif name == "submit_answer":
            parts.append("submit")
        elif name == "find_schema":
            parts.append(f"find_schema")
        else:
            parts.append(name)
    return " → ".join(parts)


def diagnose(trace: dict) -> dict:
    """Compute per-case navigation diagnostics.

    Returns:
        gold_schema:      schema name from gold query
        gold_tables:      set of (schema, table) from gold query
        explored_schemas: schemas the agent explored via tool calls
        explored_tables:  (schema, table) pairs the agent described/sampled
        submitted_tables: (schema, table) pairs in the submitted query (if any)
        schema_correct:   agent reached the right schema
        tables_correct:   agent described/submitted all gold tables
        tool_calls:       list of {name, args}
        guides_read:      list of guide stems read
    """
    events = trace.get("events", [])
    tool_calls = get_tool_calls(events)
    gold_query = trace["case"]["gold_query"]
    submitted_query = trace["result"].get("submitted_query") or ""

    gold_schema = extract_schema(gold_query)
    gold_tables = extract_schema_table_pairs(gold_query)
    exp_schemas = schemas_explored(tool_calls)
    exp_tables = tables_explored(tool_calls)
    sub_tables = extract_schema_table_pairs(submitted_query)

    # Schema correct: agent explored it OR used it in the submitted query
    schema_correct = (
        gold_schema in exp_schemas
        or any(gold_schema == s for s, _ in sub_tables)
    )

    # Tables correct: every gold (schema, table) was either described/sampled
    # OR appears directly in the submitted query (agent may write correct JOIN
    # without having explicitly described every table first)
    tables_correct = schema_correct and bool(gold_tables) and all(
        (gs, gt) in exp_tables or (gs, gt) in sub_tables
        for gs, gt in gold_tables
    )

    return {
        "gold_schema": gold_schema,
        "gold_tables": gold_tables,
        "explored_schemas": exp_schemas,
        "explored_tables": exp_tables,
        "submitted_tables": sub_tables,
        "schema_correct": schema_correct,
        "tables_correct": tables_correct,
        "tool_calls": tool_calls,
        "guides_read": guides_read(tool_calls),
    }


# ---------------------------------------------------------------------------
# Load traces
# ---------------------------------------------------------------------------

def load_traces(run_dir: Path, split: str | None) -> list[dict]:
    """Load all trace JSON files from a run directory."""
    traces = []
    subdirs = sorted(run_dir.iterdir()) if run_dir.is_dir() else []
    for subdir in subdirs:
        if not subdir.is_dir():
            continue
        if split and subdir.name != f"evals_{split}":
            continue
        for f in sorted(subdir.glob("*.json")):
            try:
                data = json.loads(f.read_text())
                data["_split"] = subdir.name
                traces.append(data)
            except Exception as e:
                print(f"Warning: could not read {f}: {e}", file=sys.stderr)
    return traces


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def analyze(traces: list[dict], csv_path: Path | None) -> None:
    failures = [t for t in traces if not t["result"]["passed"]]
    passes = [t for t in traces if t["result"]["passed"]]
    total = len(traces)

    # Pre-compute diagnostics for all traces
    diags = [diagnose(t) for t in traces]
    fail_diags = [d for t, d in zip(traces, diags) if not t["result"]["passed"]]

    print(f"\n{'='*60}")
    print(f"Run analysis: {total} cases, {len(passes)} passed, {len(failures)} failed")
    print(f"{'='*60}\n")

    # --- Failure type breakdown ---
    by_type: Counter[str] = Counter(t["result"]["failure_type"] for t in failures)
    print("Failures by type:")
    for ftype, count in by_type.most_common():
        print(f"  {ftype:<20} {count:>3}")
    print()

    # --- Navigation funnel ---
    n = len(traces)
    n_schema = sum(1 for d in diags if d["schema_correct"])
    n_tables = sum(1 for d in diags if d["tables_correct"])
    n_pass = len(passes)
    print("Navigation funnel (all cases):")
    print(f"  Right schema:  {n_schema:>3}/{n}  ({100*n_schema/n:.0f}%)")
    print(f"  Right tables:  {n_tables:>3}/{n}  ({100*n_tables/n:.0f}%)  "
          f"[of schema-correct: {n_tables}/{n_schema}]" if n_schema else "")
    print(f"  Right logic:   {n_pass:>3}/{n}  ({100*n_pass/n:.0f}%)  "
          f"[of table-correct: {n_pass}/{n_tables}]" if n_tables else "")
    print()

    # --- Failures by schema ---
    by_schema: defaultdict[str, list[str]] = defaultdict(list)
    for t in failures:
        schema = extract_schema(t["case"]["gold_query"])
        by_schema[schema].append(t["result"]["failure_type"])

    print("Failures by schema (gold query):")
    for schema, ftypes in sorted(by_schema.items(), key=lambda x: -len(x[1])):
        breakdown = ", ".join(f"{k}×{v}" for k, v in Counter(ftypes).most_common())
        print(f"  {schema:<35} {len(ftypes):>3} failures  [{breakdown}]")
    print()

    # --- Failure breakdown by navigation stage ---
    wrong_schema = sum(1 for d in fail_diags if not d["schema_correct"])
    wrong_tables = sum(1 for d in fail_diags if d["schema_correct"] and not d["tables_correct"])
    wrong_logic  = sum(1 for d in fail_diags if d["tables_correct"])
    print("Failures by navigation stage:")
    print(f"  Wrong schema:  {wrong_schema:>3}  (never reached gold schema)")
    print(f"  Wrong tables:  {wrong_tables:>3}  (schema ok, missed a gold table)")
    print(f"  Wrong logic:   {wrong_logic:>3}  (right tables, wrong query)")
    print()

    # --- Per-case detail ---
    print(f"{'='*60}")
    print("Failed cases detail:")
    print(f"{'='*60}\n")

    for i, (t, d) in enumerate(zip(failures, fail_diags), 1):
        split = t.get("_split", "")
        ftype = t["result"]["failure_type"]
        prompt = t["case"]["prompt"]
        gold = t["case"]["gold_query"]
        submitted = t["result"]["submitted_query"] or "(none)"
        error = t["result"]["error"] or ""

        schema_mark = "✓" if d["schema_correct"] else "✗"
        tables_mark = "✓" if d["tables_correct"] else ("~" if d["schema_correct"] else "✗")

        gold_tables_str = ", ".join(f"{s}.{tb}" for s, tb in sorted(d["gold_tables"]))
        explored_schemas_str = ", ".join(sorted(d["explored_schemas"])) or "(none)"
        missed_tables = [
            f"{s}.{tb}" for s, tb in sorted(d["gold_tables"])
            if (s, tb) not in d["explored_tables"] and (s, tb) not in d["submitted_tables"]
        ]

        print(f"[{i}/{len(failures)}] {split} | {ftype} | schema={d['gold_schema']}")
        print(f"  Schema: {schema_mark}  explored={explored_schemas_str}")
        if d["schema_correct"]:
            if missed_tables:
                print(f"  Tables: {tables_mark}  missed={', '.join(missed_tables)}")
            else:
                print(f"  Tables: {tables_mark}  gold=({gold_tables_str})")
        else:
            print(f"  Tables: {tables_mark}  gold=({gold_tables_str})")
        if d["guides_read"]:
            print(f"  Guides: {', '.join(d['guides_read'])}")
        seq = tool_sequence_str(d["tool_calls"])
        if seq:
            print(f"  Seq:    {seq[:160]}")
        print(f"  PROMPT:    {prompt[:100]}")
        print(f"  GOLD:      {gold[:120]}")
        print(f"  SUBMITTED: {submitted[:120]}")
        if error:
            print(f"  ERROR:     {error[:120]}")
        print()

    # --- CSV dump ---
    if csv_path:
        rows = []
        for i, (t, d) in enumerate(zip(traces, diags)):
            rows.append({
                "case_idx": i,
                "split": t.get("_split", ""),
                "passed": t["result"]["passed"],
                "failure_type": t["result"]["failure_type"],
                "gold_schema": d["gold_schema"],
                "gold_tables": "|".join(f"{s}.{tb}" for s, tb in sorted(d["gold_tables"])),
                "schema_correct": d["schema_correct"],
                "tables_correct": d["tables_correct"],
                "guides_read": "|".join(d["guides_read"]),
                "tool_sequence": tool_sequence_str(d["tool_calls"]),
                "prompt": t["case"]["prompt"],
                "gold_query": t["case"]["gold_query"],
                "submitted_query": t["result"]["submitted_query"] or "",
                "error": t["result"]["error"] or "",
                "duration_seconds": t.get("duration_seconds", ""),
            })
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"CSV written to: {csv_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze an evaluation run directory.")
    parser.add_argument("run_dir", type=Path, help="Path to logs/run_<ts>/ directory.")
    parser.add_argument("--split", choices=["easy", "hard"], help="Analyze only one split.")
    parser.add_argument("--csv", type=Path, help="Write per-case CSV to this path.")
    args = parser.parse_args()

    if not args.run_dir.is_dir():
        print(f"Error: {args.run_dir} is not a directory.", file=sys.stderr)
        sys.exit(1)

    traces = load_traces(args.run_dir, args.split)
    if not traces:
        print("No traces found.", file=sys.stderr)
        sys.exit(1)

    analyze(traces, args.csv)


if __name__ == "__main__":
    main()
