"""Instructor-provided Milestone 3 SQL execution utilities.

Students do not normally modify this file.
"""

from __future__ import annotations

from pathlib import Path


def _parse_numbered_queries(sql_text: str) -> list[dict]:
    """Parse SQL statements grouped under -- Q1., -- Q2., etc."""
    queries = []
    current_name = None
    current_description = ""
    current_lines = []

    for line in sql_text.splitlines():
        stripped = line.strip()

        if stripped.startswith("-- Q"):
            if (
                current_name is not None
                and current_lines
            ):
                queries.append(
                    {
                        "name": current_name,
                        "description": (
                            current_description
                        ),
                        "sql": "\n".join(
                            current_lines
                        ).strip(),
                    }
                )

            current_lines = []

            requirement = stripped[2:].strip()
            parts = requirement.split(".", 1)

            current_name = parts[0].strip()
            current_description = (
                parts[1].strip()
                if len(parts) > 1
                else ""
            )

            continue

        if not stripped:
            continue

        if stripped.startswith("--"):
            continue

        if current_name is not None:
            current_lines.append(line)

    if (
        current_name is not None
        and current_lines
    ):
        queries.append(
            {
                "name": current_name,
                "description": current_description,
                "sql": "\n".join(
                    current_lines
                ).strip(),
            }
        )

    return queries


def run_analysis_queries(
    connection,
    sql_path,
):
    """Execute numbered Milestone 3 analytical SQL queries."""

    sql_path = Path(sql_path)

    if not sql_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {sql_path}"
        )

    queries = _parse_numbered_queries(
        sql_path.read_text(
            encoding="utf-8"
        )
    )

    results = {}
    cursor = connection.cursor()

    for query in queries:
        query_name = query["name"]
        statement = (
            query["sql"]
            .rstrip(";")
            .strip()
        )

        if not statement:
            results[query_name] = {
                "description": (
                    query["description"]
                ),
                "status": "FAIL",
                "error": "No SQL statement provided.",
            }
            continue

        try:
            cursor.execute(statement)

            columns = []
            rows = []

            if cursor.description:
                columns = [
                    column[0]
                    for column
                    in cursor.description
                ]
                rows = [
                    list(row)
                    for row
                    in cursor.fetchall()
                ]

            results[query_name] = {
                "description": (
                    query["description"]
                ),
                "status": "PASS",
                "columns": columns,
                "row_count": len(rows),
                "rows": rows,
            }

        except Exception as error:
            results[query_name] = {
                "description": (
                    query["description"]
                ),
                "status": "FAIL",
                "error": str(error),
            }

    return results


def display_sql_results(results):
    """Display a small terminal preview of SQL results."""

    print("\n" + "=" * 60)
    print("MILESTONE 3 ANALYTICAL SQL RESULTS")
    print("=" * 60)

    if not results:
        print("\nNo SQL results were produced.")
        print("=" * 60)
        return

    for query_name, result in results.items():
        print(f"\n{query_name}")
        print(
            "  Requirement: "
            f"{result.get('description', '')}"
        )
        print(
            "  Status: "
            f"{result.get('status', 'UNKNOWN')}"
        )

        if result.get("status") == "FAIL":
            print(
                "  Error: "
                f"{result.get('error', 'Unknown error')}"
            )
            continue

        row_count = int(
            result.get("row_count", 0)
        )

        print(
            f"  Rows returned: {row_count:,}"
        )

        columns = result.get(
            "columns",
            [],
        )

        if columns:
            print(
                "  Columns: "
                + ", ".join(columns)
            )

        preview = result.get(
            "rows",
            [],
        )[:5]

        if preview:
            print("  Preview:")

            for row in preview:
                print(f"    {row}")

            if row_count > 5:
                print(
                    f"    ... {row_count - 5:,} "
                    "more row(s)"
                )

        elif row_count == 0:
            print("  No rows returned.")

    print("\n" + "=" * 60)
