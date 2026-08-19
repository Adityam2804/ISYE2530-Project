"""Milestone 2: SQLite database creation and loading.

INSTRUCTOR-PROVIDED FILE
------------------------
Students normally do NOT modify this file.

Students define the relational design in:
- src/cleaning.py -> split_into_tables()
- sql/schema.sql

This file handles database mechanics.
"""

from __future__ import annotations

from pathlib import Path
import sqlite3

import pandas as pd


def create_database(
    db_path,
    schema_path,
):
    """Create a fresh SQLite database using schema.sql.

    Returns
    -------
    sqlite3.Connection
        Open connection with foreign-key checking enabled.
    """

    db_path = Path(db_path)
    schema_path = Path(schema_path)

    if not schema_path.exists():
        raise FileNotFoundError(
            f"Schema file not found: {schema_path}"
        )

    schema_sql = schema_path.read_text(
        encoding="utf-8"
    )

    if "CREATE TABLE" not in schema_sql.upper():
        raise ValueError(
            "schema.sql does not contain any CREATE TABLE statements."
        )

    db_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Re-running the milestone should rebuild the DB from the
    # current schema rather than silently reuse an older schema.
    if db_path.exists():
        db_path.unlink()

    connection = sqlite3.connect(
        db_path
    )

    connection.execute(
        "PRAGMA foreign_keys = ON;"
    )

    try:
        connection.executescript(
            schema_sql
        )
        connection.commit()

    except Exception:
        connection.close()
        raise

    return connection


def load_clean_data(
    connection,
    tables,
):
    """Load relational DataFrames into matching SQLite tables.

    The dictionary key must match the CREATE TABLE name in schema.sql.

    Returns
    -------
    dict
        Contains:
        - tables_loaded
        - rows_loaded
    """

    if not isinstance(tables, dict):
        raise TypeError(
            "tables must be a dictionary of DataFrames."
        )

    connection.execute(
        "PRAGMA foreign_keys = ON;"
    )

    existing_tables = {
        row[0]
        for row in connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            """
        ).fetchall()
    }

    missing_schema_tables = [
        table_name
        for table_name in tables
        if table_name not in existing_tables
    ]

    if missing_schema_tables:
        raise ValueError(
            "These DataFrame table names are not defined "
            f"in schema.sql: {missing_schema_tables}"
        )

    rows_loaded = {}
    tables_loaded = []

    try:
        # Disable FK checks temporarily during the physical load.
        # Integrity is checked immediately afterward.
        connection.execute(
            "PRAGMA foreign_keys = OFF;"
        )

        for table_name, dataframe in tables.items():
            if not isinstance(
                dataframe,
                pd.DataFrame,
            ):
                raise TypeError(
                    f"'{table_name}' is not a DataFrame."
                )

            dataframe.to_sql(
                table_name,
                connection,
                if_exists="append",
                index=False,
            )

            rows_loaded[table_name] = int(
                len(dataframe)
            )
            tables_loaded.append(
                table_name
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.execute(
            "PRAGMA foreign_keys = ON;"
        )

    violations = connection.execute(
        "PRAGMA foreign_key_check;"
    ).fetchall()

    if violations:
        raise ValueError(
            "Data loaded, but foreign-key violations were found: "
            f"{violations[:5]}"
        )

    return {
        "tables_loaded":
            tables_loaded,

        "rows_loaded":
            rows_loaded,
    }
