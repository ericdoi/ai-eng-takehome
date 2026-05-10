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


def extract_schema(query: str) -> str:
    """Best-effort: return the first schema name found in a SQL query.

    Looks only in FROM/JOIN clauses and requires names ≥3 chars to skip aliases.
    """
    skip = {"information_schema", "pg_catalog", "main"}
    # Extract only FROM/JOIN clause portions to avoid alias.column false positives
    clause_text = " ".join(
        m.group(0) for m in re.finditer(
            r'(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\.\s*[A-Za-z_]',
            query, re.IGNORECASE,
        )
    )
    for m in re.finditer(
        r'(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\.',
        query, re.IGNORECASE,
    ):
        name = m.group(1)
        if name.lower() not in skip and len(name) >= 3:
            return name
    return "(unknown)"


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


def analyze(traces: list[dict], csv_path: Path | None) -> None:
    failures = [t for t in traces if not t["result"]["passed"]]
    passes = [t for t in traces if t["result"]["passed"]]

    total = len(traces)
    print(f"\n{'='*60}")
    print(f"Run analysis: {total} cases, {len(passes)} passed, {len(failures)} failed")
    print(f"{'='*60}\n")

    # --- Failure type breakdown ---
    by_type: Counter[str] = Counter(t["result"]["failure_type"] for t in failures)
    print("Failures by type:")
    for ftype, count in by_type.most_common():
        print(f"  {ftype:<20} {count:>3}")
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

    # --- Per-case detail ---
    print(f"{'='*60}")
    print("Failed cases detail:")
    print(f"{'='*60}\n")
    for i, t in enumerate(failures, 1):
        split = t.get("_split", "")
        ftype = t["result"]["failure_type"]
        prompt = t["case"]["prompt"]
        gold = t["case"]["gold_query"]
        submitted = t["result"]["submitted_query"] or "(none)"
        error = t["result"]["error"] or ""
        schema = extract_schema(gold)

        print(f"[{i}/{len(failures)}] {split} | {ftype} | schema={schema}")
        print(f"  PROMPT:    {prompt[:100]}")
        print(f"  GOLD:      {gold[:120]}")
        print(f"  SUBMITTED: {submitted[:120]}")
        if error:
            print(f"  ERROR:     {error[:120]}")
        print()

    # --- CSV dump ---
    if csv_path:
        rows = []
        for i, t in enumerate(traces):
            rows.append({
                "case_idx": i,
                "split": t.get("_split", ""),
                "passed": t["result"]["passed"],
                "failure_type": t["result"]["failure_type"],
                "schema_used": extract_schema(t["case"]["gold_query"]),
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
