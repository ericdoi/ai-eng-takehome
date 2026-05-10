#!/usr/bin/env python3
"""Run the agent on a handful of prompts and show tool calls + final answer.

Usage:
    source .env && uv run python scripts/spot_check.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from framework.agent import Agent, EventType
from framework.llm import OpenRouterConfig
from evaluation.evaluate import create_tools
from framework.database import execute_query

PROMPTS = [
    # Accidents — business-rule heavy (urban/rural, severity hierarchy)
    "Count accidents by administrative unit, only for units with more than 100 accidents for statistical significance.",
    # Airline — on-time performance definition
    "What is the on-time performance percentage for each unique airline carrier? Round the percentage to 2 decimal places.",
    # Chess — win-rate calculation with filtering
    "Calculate win rates for White players (with at least 5 games). Return the 30 players with the highest win rates, ordered by win rate descending.",
]

def run_case(agent: Agent, prompt: str) -> None:
    print("\n" + "=" * 70)
    print(f"PROMPT: {prompt}")
    print("=" * 70)

    agent.reset_conversation()
    submitted_query = None

    for event in agent.run(prompt):
        if event.type == EventType.TOOL_CALL_PARSED:
            name = event.data.get("name", "")
            args = event.data.get("arguments", {})
            if name == "find_schema":
                print(f"\n→ find_schema(query={args.get('query', '')!r})")
            elif name == "run_sql":
                sql = args.get("query", "").strip().replace("\n", " ")
                print(f"\n→ run_sql: {sql[:120]}{'...' if len(sql) > 120 else ''}")
            elif name == "submit_answer":
                sql = args.get("query", "").strip()
                print(f"\n→ submit_answer:\n{sql}")
                submitted_query = sql
            else:
                print(f"\n→ {name}({args})")

        elif event.type == EventType.TOOL_EXECUTION_END:
            name = event.data.get("name", "")
            result = event.data.get("result", "")
            if name == "find_schema":
                # Just show the first line (schema match line)
                first_line = result.split("\n")[0]
                print(f"  ← {first_line}")
            elif name == "run_sql":
                preview = result.strip().split("\n")
                print(f"  ← {len(preview)} lines returned")

        elif event.type == EventType.AGENT_ERROR:
            print(f"\n✗ AGENT_ERROR: {event.data.get('error')}")

    if submitted_query:
        result = execute_query(submitted_query)
        if result.is_success:
            df = result.dataframe
            print(f"\n✓ Query executed: {df.height} rows × {df.width} cols")
            print(df.head(5))
        else:
            print(f"\n✗ SQL error: {result.error_message}")
    else:
        print("\n✗ No answer submitted")

def main() -> None:
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set")
        sys.exit(1)

    config = OpenRouterConfig(api_key=api_key)
    tools = create_tools()
    agent = Agent(config=config, tools=tools)

    for prompt in PROMPTS:
        run_case(agent, prompt)

    print("\n" + "=" * 70)
    print("Spot-check complete.")

if __name__ == "__main__":
    main()
