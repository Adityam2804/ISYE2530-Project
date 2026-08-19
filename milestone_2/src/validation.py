"""Milestone 2: clean-data and database validation.

INSTRUCTOR-PROVIDED CORE
------------------------
Students normally do not rewrite the validation infrastructure.

Students may optionally add ONE project-specific database check in the clearly
marked section if useful.
"""

from __future__ import annotations

import sqlite3

import pandas as pd


def validate_clean_data(
    raw_df,
    clean_df,
):
    """Compare raw and cleaned data using generic quality checks."""

    if not isinstance(
        raw_df,
        pd.DataFrame,
    ):
        raise TypeError(
            "raw_df must be a pandas DataFrame."
        )

    if not isinstance(
        clean_df,
        pd.DataFrame,
    ):
        raise TypeError(
            "clean_df must be a pandas DataFrame."
        )

    raw_rows = int(
        len(raw_df)
    )

    clean_rows = int(
        len(clean_df)
    )

    rows_removed = int(
        raw_rows - clean_rows
    )

    percent_removed = (
        round(
            rows_removed / raw_rows * 100,
            2,
        )
        if raw_rows
        else 0.0
    )

    remaining_missing = {
        str(column): int(count)
        for column, count
        in clean_df.isna().sum().items()
    }

    remaining_duplicates = int(
        clean_df.duplicated().sum()
    )

    checks = {
        "clean_data_not_empty":
            clean_rows > 0,

        "no_exact_duplicate_rows":
            remaining_duplicates == 0,

        "row_count_not_increased_unexpectedly":
            clean_rows <= raw_rows,
    }

    # Important:
    # Missing values are NOT automatically a failure.
    # Some projects may legitimately retain missing values.
    #
    # Large row removal is reported for instructor review rather
    # than automatically treated as failure.

    warnings = []

    if percent_removed > 25:
        warnings.append(
            "More than 25% of raw rows were removed. "
            "Explain and justify this in cleaning_report.md."
        )

    if any(
        count > 0
        for count in remaining_missing.values()
    ):
        warnings.append(
            "Missing values remain. This is acceptable only when "
            "your project rules explain why those values can remain."
        )

    return {
        "raw_rows":
            raw_rows,

        "clean_rows":
            clean_rows,

        "rows_removed":
            rows_removed,

        "percent_removed":
            percent_removed,

        "remaining_missing":
            remaining_missing,

        "remaining_duplicates":
            remaining_duplicates,

        "checks":
            checks,

        "warnings":
            warnings,

        "validation_passed":
            bool(
                all(checks.values())
            ),
    }


def validate_database(connection):
    """Validate relational database structure and integrity."""

    if not isinstance(
        connection,
        sqlite3.Connection,
    ):
        raise TypeError(
            "connection must be sqlite3.Connection."
        )

    connection.execute(
        "PRAGMA foreign_keys = ON;"
    )

    tables = [
        str(row[0])
        for row in connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()
    ]

    row_counts = {}

    for table_name in tables:
        safe_name = (
            table_name.replace(
                '"',
                '""',
            )
        )

        row_count = connection.execute(
            f'SELECT COUNT(*) FROM "{safe_name}"'
        ).fetchone()[0]

        row_counts[
            table_name
        ] = int(
            row_count
        )

    foreign_key_violations = [
        list(row)
        for row in connection.execute(
            "PRAGMA foreign_key_check;"
        ).fetchall()
    ]

    empty_tables = [
        table_name
        for table_name, count
        in row_counts.items()
        if count == 0
    ]

    checks = {
        "at_least_two_tables":
            len(tables) >= 2,

        "no_empty_tables":
            len(empty_tables) == 0,

        "no_foreign_key_violations":
            len(
                foreign_key_violations
            ) == 0,
    }

    # --------------------------------------------------------
    # OPTIONAL STUDENT EXTENSION
    #
    # You normally do not need to modify this function.
    #
    # If your project has ONE especially important integrity
    # condition that cannot be captured by PK/FK constraints,
    # discuss it with the instructor and add the result below.
    #
    # Example:
    #
    # result = connection.execute(
    #     "SELECT COUNT(*) FROM events WHERE end_time < start_time"
    # ).fetchone()[0]
    #
    # checks["no_negative_duration"] = (result == 0)
    # --------------------------------------------------------

    return {
        "tables":
            tables,

        "row_counts":
            row_counts,

        "empty_tables":
            empty_tables,

        "foreign_key_violations":
            foreign_key_violations,

        "checks":
            checks,

        "validation_passed":
            bool(
                all(checks.values())
            ),
    }
