"""ISE 2530 Course Project
Milestone 2 - Interactive Runner

INSTRUCTOR-PROVIDED FILE.
Students should not modify this file.

Behavior
--------
- Yes -> run/re-run that step
- No  -> skip that step and continue
- Existing outputs are reused when possible
"""

from __future__ import annotations

from pathlib import Path
import json
import sqlite3

import pandas as pd

from src.data_loading import (
    load_raw_data,
    inspect_raw_data,
)
from src.cleaning import (
    clean_data,
    split_into_tables,
)
from src.validation import (
    validate_clean_data,
    validate_database,
)
from src.database import (
    create_database,
    load_clean_data,
)


BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR.parent
    / "milestone_1"
    / "dataset.xlsx"
)

OUTPUT_DIR = BASE_DIR / "outputs"

RAW_INSPECTION_PATH = (
    OUTPUT_DIR
    / "raw_data_inspection.json"
)

CLEANED_DATA_PATH = (
    OUTPUT_DIR
    / "cleaned_data.csv"
)

CLEANING_SUMMARY_PATH = (
    OUTPUT_DIR
    / "cleaning_summary.json"
)

TABLE_SUMMARY_PATH = (
    OUTPUT_DIR
    / "table_summary.json"
)

TABLE_OUTPUT_DIR = (
    OUTPUT_DIR
    / "tables"
)

CLEAN_DATA_VALIDATION_PATH = (
    OUTPUT_DIR
    / "clean_data_validation.json"
)

SCHEMA_PATH = (
    BASE_DIR
    / "sql"
    / "schema.sql"
)

DATABASE_PATH = (
    OUTPUT_DIR
    / "project.db"
)

DATABASE_LOAD_SUMMARY_PATH = (
    OUTPUT_DIR
    / "database_load_summary.json"
)

DATABASE_VALIDATION_PATH = (
    OUTPUT_DIR
    / "database_validation.json"
)

REQUIRED_QUERIES_PATH = (
    BASE_DIR
    / "sql"
    / "required_queries.sql"
)

SQL_RESULTS_PATH = (
    OUTPUT_DIR
    / "sql_results.json"
)


def ask_to_continue(message):
    """Ask yes/no. No means skip, not exit."""
    while True:
        answer = input(
            f"\n{message} [y/n]: "
        ).strip().lower()

        if answer in {
            "y",
            "yes",
        }:
            return True

        if answer in {
            "n",
            "no",
        }:
            return False

        print(
            "Please enter 'y' or 'n'."
        )


def save_json(data, path):
    """Save JSON evidence."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            data,
            indent=4,
            default=str,
        ),
        encoding="utf-8",
    )


def display_raw_summary(summary):
    """Display concise raw-data inspection."""

    print("\n" + "=" * 60)
    print("RAW DATA SUMMARY")
    print("=" * 60)

    print(
        f"\nRows: "
        f"{summary['row_count']:,}"
    )

    print(
        f"Columns: "
        f"{summary['column_count']}"
    )

    print(
        f"Duplicate rows: "
        f"{summary['duplicate_rows']:,}"
    )

    print("\nMissing values:")

    for column, count in (
        summary[
            "missing_by_column"
        ].items()
    ):
        print(
            f"  {column}: {count:,}"
        )

    print("\n" + "=" * 60)


def build_cleaning_summary(
    raw_df,
    clean_df,
):
    """Build a concise cleaning summary."""

    raw_rows = int(
        len(raw_df)
    )

    clean_rows = int(
        len(clean_df)
    )

    rows_removed = (
        raw_rows - clean_rows
    )

    percent_removed = (
        rows_removed / raw_rows * 100
        if raw_rows
        else 0
    )

    return {
        "raw_rows":
            raw_rows,

        "clean_rows":
            clean_rows,

        "rows_removed":
            rows_removed,

        "percent_removed":
            round(
                percent_removed,
                2,
            ),

        "remaining_missing_by_column": {
            str(column): int(count)
            for column, count
            in clean_df.isna().sum().items()
        },

        "remaining_duplicate_rows":
            int(
                clean_df
                .duplicated()
                .sum()
            ),

        "columns":
            [
                str(column)
                for column
                in clean_df.columns
            ],

        "dtypes": {
            str(column): str(dtype)
            for column, dtype
            in clean_df.dtypes.items()
        },
    }


def save_tables(tables):
    """Save relational DataFrames as CSV evidence."""

    TABLE_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary = {}

    for table_name, dataframe in (
        tables.items()
    ):
        output_path = (
            TABLE_OUTPUT_DIR
            / f"{table_name}.csv"
        )

        dataframe.to_csv(
            output_path,
            index=False,
        )

        summary[table_name] = {
            "row_count":
                int(
                    len(dataframe)
                ),

            "column_count":
                int(
                    len(
                        dataframe.columns
                    )
                ),

            "columns":
                [
                    str(column)
                    for column
                    in dataframe.columns
                ],

            "output_file":
                str(output_path),
        }

    return summary


def load_existing_tables():
    """Reload relational tables based on table_summary.json."""

    if not TABLE_SUMMARY_PATH.exists():
        return None

    try:
        summary = json.loads(
            TABLE_SUMMARY_PATH.read_text(
                encoding="utf-8"
            )
        )
    except Exception:
        return None

    tables = {}

    for table_name, information in (
        summary.items()
    ):
        output_file = Path(
            information[
                "output_file"
            ]
        )

        if not output_file.is_absolute():
            # Older runs may store a relative path.
            candidate = (
                BASE_DIR
                / output_file
            )

            if candidate.exists():
                output_file = candidate

        if not output_file.exists():
            fallback = (
                TABLE_OUTPUT_DIR
                / f"{table_name}.csv"
            )

            if fallback.exists():
                output_file = fallback
            else:
                return None

        tables[
            table_name
        ] = pd.read_csv(
            output_file
        )

    return tables


def _parse_numbered_sql(sql_path):
    """Parse SQL below -- Q1., -- Q2., etc."""

    sql_text = Path(
        sql_path
    ).read_text(
        encoding="utf-8"
    )

    queries = []
    current_name = None
    current_description = ""
    current_lines = []

    for line in (
        sql_text.splitlines()
    ):
        stripped = (
            line.strip()
        )

        if stripped.startswith(
            "-- Q"
        ):
            if (
                current_name
                and current_lines
            ):
                queries.append(
                    {
                        "name":
                            current_name,

                        "description":
                            current_description,

                        "sql":
                            "\n".join(
                                current_lines
                            ).strip(),
                    }
                )

            requirement = (
                stripped[2:]
                .strip()
            )

            parts = (
                requirement
                .split(
                    ".",
                    1,
                )
            )

            current_name = (
                parts[0]
                .strip()
            )

            current_description = (
                parts[1]
                .strip()
                if len(parts) > 1
                else ""
            )

            current_lines = []
            continue

        if (
            not stripped
            or stripped.startswith(
                "--"
            )
        ):
            continue

        if current_name:
            current_lines.append(
                line
            )

    if (
        current_name
        and current_lines
    ):
        queries.append(
            {
                "name":
                    current_name,

                "description":
                    current_description,

                "sql":
                    "\n".join(
                        current_lines
                    ).strip(),
            }
        )

    return queries


def run_required_sql_queries(
    connection,
    sql_path,
):
    """Execute Q1-Q5 from required_queries.sql."""

    sql_path = Path(
        sql_path
    )

    if not sql_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {sql_path}"
        )

    queries = _parse_numbered_sql(
        sql_path
    )

    results = {}
    cursor = connection.cursor()

    for query in queries:
        name = query["name"]
        statement = (
            query["sql"]
            .rstrip(";")
            .strip()
        )

        if not statement:
            results[name] = {
                "description":
                    query[
                        "description"
                    ],

                "status":
                    "FAIL",

                "error":
                    "No SQL statement provided.",
            }
            continue

        try:
            cursor.execute(
                statement
            )

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

            results[name] = {
                "description":
                    query[
                        "description"
                    ],

                "status":
                    "PASS",

                "columns":
                    columns,

                "row_count":
                    len(rows),

                "rows":
                    rows,
            }

        except Exception as error:
            results[name] = {
                "description":
                    query[
                        "description"
                    ],

                "status":
                    "FAIL",

                "error":
                    str(error),
            }

    return results


def display_sql_results(
    results,
):
    """Display first five rows of each SQL result."""

    print("\n" + "=" * 60)
    print("REQUIRED SQL CHECKS")
    print("=" * 60)

    if not results:
        print(
            "\nNo SQL results were produced."
        )
        return

    for query_name, result in (
        results.items()
    ):
        print(
            f"\n{query_name}"
        )

        print(
            "  Requirement: "
            f"{result.get('description', '')}"
        )

        print(
            "  Status: "
            f"{result.get('status', 'UNKNOWN')}"
        )

        if (
            result.get(
                "status"
            )
            == "FAIL"
        ):
            print(
                "  Error: "
                f"{result.get('error', '')}"
            )
            continue

        row_count = int(
            result.get(
                "row_count",
                0,
            )
        )

        print(
            f"  Rows returned: "
            f"{row_count:,}"
        )

        columns = result.get(
            "columns",
            [],
        )

        if columns:
            print(
                "  Columns: "
                + ", ".join(
                    columns
                )
            )

        preview = result.get(
            "rows",
            [],
        )[:5]

        if preview:
            print(
                "  Preview:"
            )

            for row in preview:
                print(
                    f"    {row}"
                )

            if row_count > 5:
                print(
                    f"    ... "
                    f"{row_count - 5:,} "
                    "more row(s)"
                )

        elif row_count == 0:
            print(
                "  No rows returned."
            )

    print("\n" + "=" * 60)


def open_existing_database():
    """Open existing project.db when available."""
    if not DATABASE_PATH.exists():
        return None

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.execute(
        "PRAGMA foreign_keys = ON;"
    )

    return connection


def main():
    print("=" * 60)
    print("ISE 2530 - MILESTONE 2")
    print("Data Cleaning and Database Formation")
    print("=" * 60)

    print(
        f"\nDataset:"
        f"\n  {DATA_PATH}"
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    raw_df = None
    clean_df = None
    tables = None
    connection = None

    # =====================================================
    # STEP 1 — LOAD RAW DATA
    # =====================================================

    if ask_to_continue(
        "Step 1: Load the raw dataset?"
    ):
        try:
            raw_df = load_raw_data(
                DATA_PATH
            )

            print(
                f"\n[PASS] Loaded "
                f"{len(raw_df):,} rows and "
                f"{len(raw_df.columns)} columns."
            )

        except Exception as error:
            print(
                "\n[FAIL] Step 1 - Load raw dataset"
            )
            print(error)

    else:
        print(
            "\n[SKIPPED] Step 1 - Load raw dataset"
        )

    # =====================================================
    # STEP 2 — INSPECT RAW DATA
    # =====================================================

    if ask_to_continue(
        "Step 2: Inspect the raw dataset?"
    ):
        if raw_df is None:
            try:
                raw_df = load_raw_data(
                    DATA_PATH
                )
            except Exception as error:
                print(
                    "\n[FAIL] Step 2 - "
                    "Raw dataset is unavailable."
                )
                print(error)

        if raw_df is not None:
            try:
                raw_summary = inspect_raw_data(
                    raw_df
                )

                save_json(
                    raw_summary,
                    RAW_INSPECTION_PATH,
                )

                display_raw_summary(
                    raw_summary
                )

                print(
                    f"\n[PASS] Saved:"
                    f"\n  {RAW_INSPECTION_PATH}"
                )

            except Exception as error:
                print(
                    "\n[FAIL] Step 2 - Inspect raw dataset"
                )
                print(error)

    else:
        print(
            "\n[SKIPPED] Step 2 - Inspect raw dataset"
        )

    # =====================================================
    # STEP 3 — CLEAN DATA
    # =====================================================

    if ask_to_continue(
        "Step 3: Clean the dataset?"
    ):
        if raw_df is None:
            try:
                raw_df = load_raw_data(
                    DATA_PATH
                )
            except Exception as error:
                print(
                    "\n[FAIL] Step 3 - "
                    "Raw dataset is unavailable."
                )
                print(error)

        if raw_df is not None:
            try:
                clean_df = clean_data(
                    raw_df
                )

                clean_df.to_csv(
                    CLEANED_DATA_PATH,
                    index=False,
                )

                cleaning_summary = (
                    build_cleaning_summary(
                        raw_df,
                        clean_df,
                    )
                )

                save_json(
                    cleaning_summary,
                    CLEANING_SUMMARY_PATH,
                )

                print(
                    "\n[PASS] Cleaned data saved:"
                )
                print(
                    f"  {CLEANED_DATA_PATH}"
                )

                print(
                    "[PASS] Cleaning summary saved:"
                )
                print(
                    f"  {CLEANING_SUMMARY_PATH}"
                )

            except Exception as error:
                print(
                    "\n[FAIL] Step 3 - Clean dataset"
                )
                print(error)

    else:
        print(
            "\n[SKIPPED] Step 3 - Clean dataset"
        )

        if CLEANED_DATA_PATH.exists():
            clean_df = pd.read_csv(
                CLEANED_DATA_PATH
            )

            print(
                "[INFO] Existing cleaned data "
                "will be reused."
            )

    # =====================================================
    # STEP 4 — CREATE RELATIONAL TABLES
    # =====================================================

    if ask_to_continue(
        "Step 4: Create relational tables?"
    ):
        if clean_df is None:
            if CLEANED_DATA_PATH.exists():
                clean_df = pd.read_csv(
                    CLEANED_DATA_PATH
                )

        if clean_df is None:
            print(
                "\n[SKIPPED] Step 4 - "
                "No cleaned data is available."
            )
        else:
            try:
                tables = split_into_tables(
                    clean_df
                )

                table_summary = save_tables(
                    tables
                )

                save_json(
                    table_summary,
                    TABLE_SUMMARY_PATH,
                )

                print(
                    "\n[PASS] Relational tables saved:"
                )

                for table_name, table_df in (
                    tables.items()
                ):
                    print(
                        f"  {table_name}: "
                        f"{len(table_df):,} rows"
                    )

            except Exception as error:
                print(
                    "\n[FAIL] Step 4 - "
                    "Create relational tables"
                )
                print(error)

    else:
        print(
            "\n[SKIPPED] Step 4 - "
            "Create relational tables"
        )

        tables = load_existing_tables()

        if tables is not None:
            print(
                "[INFO] Existing relational tables "
                "will be reused."
            )

    # =====================================================
    # STEP 5 — VALIDATE CLEANED DATA
    # =====================================================

    if ask_to_continue(
        "Step 5: Validate cleaned data?"
    ):
        if raw_df is None:
            try:
                raw_df = load_raw_data(
                    DATA_PATH
                )
            except Exception:
                pass

        if (
            clean_df is None
            and CLEANED_DATA_PATH.exists()
        ):
            clean_df = pd.read_csv(
                CLEANED_DATA_PATH
            )

        if (
            raw_df is None
            or clean_df is None
        ):
            print(
                "\n[SKIPPED] Step 5 - "
                "Raw or cleaned data is unavailable."
            )
        else:
            try:
                validation = validate_clean_data(
                    raw_df,
                    clean_df,
                )

                save_json(
                    validation,
                    CLEAN_DATA_VALIDATION_PATH,
                )

                print(
                    "\n[PASS] Clean-data validation completed."
                )
                print(
                    "  validation_passed: "
                    f"{validation.get('validation_passed')}"
                )

                for warning in validation.get(
                    "warnings",
                    [],
                ):
                    print(
                        f"  [WARNING] {warning}"
                    )

            except Exception as error:
                print(
                    "\n[FAIL] Step 5 - "
                    "Validate cleaned data"
                )
                print(error)

    else:
        print(
            "\n[SKIPPED] Step 5 - "
            "Validate cleaned data"
        )

    # =====================================================
    # STEP 6 — CREATE DATABASE
    # =====================================================

    if ask_to_continue(
        "Step 6: Create the SQLite database?"
    ):
        try:
            if connection is not None:
                connection.close()

            connection = create_database(
                DATABASE_PATH,
                SCHEMA_PATH,
            )

            print(
                "\n[PASS] SQLite database created:"
            )
            print(
                f"  {DATABASE_PATH}"
            )

        except Exception as error:
            print(
                "\n[FAIL] Step 6 - Create database"
            )
            print(error)

    else:
        print(
            "\n[SKIPPED] Step 6 - Create database"
        )

        connection = open_existing_database()

        if connection is not None:
            print(
                "[INFO] Existing database "
                "will be reused."
            )

    # =====================================================
    # STEP 7 — LOAD RELATIONAL TABLES
    # =====================================================

    if ask_to_continue(
        "Step 7: Load relational tables into the database?"
    ):
        if tables is None:
            tables = load_existing_tables()

        if connection is None:
            connection = open_existing_database()

        if (
            tables is None
            or connection is None
        ):
            print(
                "\n[SKIPPED] Step 7 - "
                "Database or relational tables are unavailable."
            )
        else:
            try:
                load_summary = load_clean_data(
                    connection,
                    tables,
                )

                save_json(
                    load_summary,
                    DATABASE_LOAD_SUMMARY_PATH,
                )

                print(
                    "\n[PASS] Relational tables loaded."
                )

                for table_name, count in (
                    load_summary[
                        "rows_loaded"
                    ].items()
                ):
                    print(
                        f"  {table_name}: "
                        f"{count:,} rows"
                    )

            except Exception as error:
                print(
                    "\n[FAIL] Step 7 - Load database"
                )
                print(error)

    else:
        print(
            "\n[SKIPPED] Step 7 - Load database"
        )

    # =====================================================
    # STEP 8 — VALIDATE DATABASE
    # =====================================================

    if ask_to_continue(
        "Step 8: Validate the SQLite database?"
    ):
        if connection is None:
            connection = open_existing_database()

        if connection is None:
            print(
                "\n[SKIPPED] Step 8 - "
                "Database is unavailable."
            )
        else:
            try:
                validation = validate_database(
                    connection
                )

                save_json(
                    validation,
                    DATABASE_VALIDATION_PATH,
                )

                print(
                    "\n[PASS] Database validation completed."
                )
                print(
                    "  validation_passed: "
                    f"{validation.get('validation_passed')}"
                )

                print(
                    "  tables: "
                    + ", ".join(
                        validation.get(
                            "tables",
                            [],
                        )
                    )
                )

            except Exception as error:
                print(
                    "\n[FAIL] Step 8 - Validate database"
                )
                print(error)

    else:
        print(
            "\n[SKIPPED] Step 8 - Validate database"
        )

    # =====================================================
    # STEP 9 — RUN REQUIRED SQL
    # =====================================================

    if ask_to_continue(
        "Step 9: Run the required SQL checks?"
    ):
        if connection is None:
            connection = open_existing_database()

        if connection is None:
            print(
                "\n[SKIPPED] Step 9 - "
                "Database is unavailable."
            )
        else:
            try:
                sql_results = run_required_sql_queries(
                    connection,
                    REQUIRED_QUERIES_PATH,
                )

                display_sql_results(
                    sql_results
                )

                save_json(
                    sql_results,
                    SQL_RESULTS_PATH,
                )

                print(
                    f"\n[PASS] SQL results saved:"
                    f"\n  {SQL_RESULTS_PATH}"
                )

            except Exception as error:
                print(
                    "\n[FAIL] Step 9 - Run SQL checks"
                )
                print(error)

    else:
        print(
            "\n[SKIPPED] Step 9 - "
            "Run required SQL checks"
        )

    if connection is not None:
        try:
            connection.close()
        except Exception:
            pass

    print("\n" + "=" * 60)
    print("MILESTONE 2 WORKFLOW FINISHED")
    print("=" * 60)

    print(
        "\nAll Milestone 2 tasks have been offered."
    )

    print(
        f"\nOutputs:"
        f"\n  {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()
