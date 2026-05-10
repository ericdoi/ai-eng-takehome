"""Database introspection tools for the SQL agent."""

from __future__ import annotations

import re

import polars as pl

from framework.agent import Tool
from framework.database import describe_table as _describe_table
from framework.database import execute_query
from framework.database import list_schemas as _list_schemas
from framework.database import list_tables as _list_tables

_MAX_OUTPUT_CHARS = 3000
_MAX_ROWS = 20


def _df_to_text(df: pl.DataFrame, max_rows: int = _MAX_ROWS, max_chars: int = _MAX_OUTPUT_CHARS) -> str:
    """Format a DataFrame as a compact markdown table, capped at max_chars."""
    if df.is_empty():
        return "(empty result)"

    rows_shown = min(df.height, max_rows)
    header = "| " + " | ".join(str(c) for c in df.columns) + " |"
    sep = "| " + " | ".join(["---"] * df.width) + " |"
    lines = [header, sep]
    truncated = False
    for i in range(rows_shown):
        row = "| " + " | ".join(str(df[c][i]) for c in df.columns) + " |"
        lines.append(row)
        if sum(len(line) for line in lines) > max_chars:
            lines.append(f"| ... ({df.height - i - 1} more rows not shown) |")
            truncated = True
            break

    if not truncated and df.height > rows_shown:
        lines.append(f"| ... ({df.height - rows_shown} more rows not shown) |")

    return "\n".join(lines)


def _list_schemas_fn() -> str:
    schemas = _list_schemas()
    if not schemas:
        return "No schemas found."
    return f"{len(schemas)} schemas:\n" + "\n".join(schemas)


def _list_tables_fn(schema: str) -> str:
    tables = _list_tables(schema)
    if tables is None or len(tables) == 0:
        return f"No tables found in schema '{schema}'. Check spelling and case."
    return f"{len(tables)} tables in '{schema}':\n" + "\n".join(tables)


def _describe_table_fn(schema: str, table: str) -> str:
    cols = _describe_table(schema, table)
    if not cols:
        return f"Table '{schema}.{table}' not found or has no columns."
    return f"{len(cols)} columns in {schema}.{table}:\n" + "\n".join(f"  {c}" for c in cols)


def _sample_rows_fn(schema: str, table: str, limit: int = 5) -> str:
    limit = max(1, min(limit, _MAX_ROWS))
    query = f'SELECT * FROM "{schema}"."{table}" LIMIT {limit}'
    result = execute_query(query)
    if not result.is_success:
        return f"Error: {result.error_message}"
    df = result.dataframe
    assert df is not None
    header = f"Sample of {df.height} rows from {schema}.{table}:\n"
    return header + _df_to_text(df)


def _search_columns_fn(keyword: str) -> str:
    """Search information_schema.columns for tables containing a keyword in their column names."""
    safe = keyword.replace("'", "''")
    result = execute_query(f"""
        SELECT table_schema, table_name, column_name, data_type
        FROM information_schema.columns
        WHERE lower(column_name) LIKE lower('%{safe}%')
          AND table_schema NOT IN ('information_schema', 'pg_catalog')
        ORDER BY table_schema, table_name, ordinal_position
        LIMIT 60
    """)
    if not result.is_success:
        return f"SQL error: {result.error_message}"
    df = result.dataframe
    assert df is not None
    if df.is_empty():
        return f"No columns matching '{keyword}' found."
    return f"{df.height} columns matching '{keyword}':\n" + _df_to_text(df, max_rows=60)


def _run_sql_fn(query: str) -> str:
    # Reject obviously mutating statements early for a cleaner error
    first_word = re.match(r'\s*(\w+)', query)
    if first_word and first_word.group(1).upper() in {
        "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE",
    }:
        return "Error: only read-only (SELECT) queries are allowed."

    result = execute_query(query)
    if not result.is_success:
        return f"SQL error: {result.error_message}"
    df = result.dataframe
    assert df is not None
    summary = f"{df.height} rows × {df.width} columns\n\n"
    table_text = _df_to_text(df)
    combined = summary + table_text
    if len(combined) > _MAX_OUTPUT_CHARS:
        return combined[:_MAX_OUTPUT_CHARS] + "\n[output truncated]"
    return combined


LIST_SCHEMAS = Tool(
    name="list_schemas",
    description="List all available schemas (databases) in the warehouse.",
    parameters={"type": "object", "properties": {}, "required": []},
    function=_list_schemas_fn,
)

LIST_TABLES = Tool(
    name="list_tables",
    description="List all tables in a given schema.",
    parameters={
        "type": "object",
        "properties": {
            "schema": {
                "type": "string",
                "description": "Schema name (case-sensitive, e.g. 'Airline', 'financial').",
            },
        },
        "required": ["schema"],
    },
    function=_list_tables_fn,
)

DESCRIBE_TABLE = Tool(
    name="describe_table",
    description="Show column names and types for a table.",
    parameters={
        "type": "object",
        "properties": {
            "schema": {"type": "string", "description": "Schema name (case-sensitive)."},
            "table": {"type": "string", "description": "Table name (case-sensitive)."},
        },
        "required": ["schema", "table"],
    },
    function=_describe_table_fn,
)

SAMPLE_ROWS = Tool(
    name="sample_rows",
    description="Fetch a small sample of rows from a table to inspect values.",
    parameters={
        "type": "object",
        "properties": {
            "schema": {"type": "string", "description": "Schema name (case-sensitive)."},
            "table": {"type": "string", "description": "Table name (case-sensitive)."},
            "limit": {
                "type": "integer",
                "description": "Number of rows to return (max 20, default 5).",
                "default": 5,
            },
        },
        "required": ["schema", "table"],
    },
    function=_sample_rows_fn,
)

SEARCH_COLUMNS = Tool(
    name="search_columns",
    description=(
        "Search for tables that contain columns matching a keyword. "
        "Returns schema, table, column name, and type for all matches. "
        "Use this to quickly locate which schema and table holds a concept "
        "(e.g. 'language', 'salary', 'carrier') without iterating through all schemas manually."
    ),
    parameters={
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": "Partial column name to search for (case-insensitive substring match).",
            },
        },
        "required": ["keyword"],
    },
    function=_search_columns_fn,
)

RUN_SQL = Tool(
    name="run_sql",
    description=(
        "Execute a read-only SQL query and return the results. "
        "Use this to preview intermediate results or verify your query before submitting. "
        "Always use schema-qualified table names (schema.table). "
        "DuckDB errors are returned verbatim — read them carefully to fix your query."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "A read-only SQL SELECT query with schema-qualified table names.",
            },
        },
        "required": ["query"],
    },
    function=_run_sql_fn,
)
