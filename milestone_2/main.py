"""
ISE 2530 Course Project
Milestone 2 - Interactive Runner

This file is provided by the instructor.

DO NOT MODIFY THIS FILE.
"""

from pathlib import Path
import json

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


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

DATA_PATH = Path("../milestone_1/dataset.xlsx")

OUTPUT_DIR = Path("outputs")

RAW_INSPECTION_PATH = (
    OUTPUT_DIR / "raw_data_inspection.json"
)

CLEANED_DATA_PATH = (
    OUTPUT_DIR / "cleaned_data.csv"
)

CLEANING_SUMMARY_PATH = (
    OUTPUT_DIR / "cleaning_summary.json"
)

TABLE_SUMMARY_PATH = (
    OUTPUT_DIR / "table_summary.json"
)

CLEAN_DATA_VALIDATION_PATH = (
    OUTPUT_DIR / "clean_data_validation.json"
)

SCHEMA_PATH = Path("sql/schema.sql")

DATABASE_PATH = (
    OUTPUT_DIR / "project.db"
)

DATABASE_LOAD_SUMMARY_PATH = (
    OUTPUT_DIR / "database_load_summary.json"
)
DATABASE_VALIDATION_PATH = (
    OUTPUT_DIR
    / "database_validation.json"
)
SQL_RESULTS_PATH = (
    OUTPUT_DIR / "sql_results.json"
)

REQUIRED_QUERIES_PATH = (
    Path("sql/required_queries.sql")
)

# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def ask_to_continue(message):
    """Ask whether to execute the next step."""

    while True:

        answer = input(
            f"\n{message} [y/n]: "
        ).strip().lower()

        if answer in {"y", "yes"}:
            return True

        if answer in {"n", "no"}:
            return False

        print("Please enter 'y' or 'n'.")


def save_json(data, path):
    """Save a dictionary as formatted JSON."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            default=str
        )


def display_raw_summary(summary):
    """Display raw-data inspection results."""

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

    print("\nColumns:")

    for column in summary["columns"]:
        print(f"  - {column}")

    print("\nData Types:")

    for column, dtype in summary["dtypes"].items():
        print(
            f"  {column}: {dtype}"
        )

    print("\nMissing Values:")

    for column, count in (
        summary["missing_by_column"].items()
    ):
        print(
            f"  {column}: {count:,}"
        )

    print(
        f"\nDuplicate Rows: "
        f"{summary['duplicate_rows']:,}"
    )

    print("\n" + "=" * 60)


def build_cleaning_summary(
    raw_df,
    clean_df
):
    """Create a basic cleaning summary."""

    raw_rows = len(raw_df)
    clean_rows = len(clean_df)

    rows_removed = (
        raw_rows - clean_rows
    )

    percent_removed = (
        rows_removed / raw_rows * 100
        if raw_rows > 0
        else 0
    )

    return {
        "raw_rows": raw_rows,
        "clean_rows": clean_rows,
        "rows_removed": rows_removed,

        "percent_removed": round(
            percent_removed,
            2
        ),

        "remaining_missing_by_column": {
            column: int(count)
            for column, count
            in clean_df.isna().sum().items()
        },

        "remaining_duplicate_rows": int(
            clean_df.duplicated().sum()
        ),

        "columns":
            clean_df.columns.tolist(),

        "dtypes": {
            column: str(dtype)
            for column, dtype
            in clean_df.dtypes.items()
        }
    }


def display_cleaning_summary(summary):
    """Display cleaning results."""

    print("\n" + "=" * 60)
    print("CLEANING SUMMARY")
    print("=" * 60)

    print(
        f"\nRaw rows: "
        f"{summary['raw_rows']:,}"
    )

    print(
        f"Clean rows: "
        f"{summary['clean_rows']:,}"
    )

    print(
        f"Rows removed: "
        f"{summary['rows_removed']:,}"
    )

    print(
        f"Percent removed: "
        f"{summary['percent_removed']:.2f}%"
    )

    print(
        f"\nRemaining duplicate rows: "
        f"{summary['remaining_duplicate_rows']:,}"
    )

    print("\nRemaining missing values:")

    for column, count in (
        summary[
            "remaining_missing_by_column"
        ].items()
    ):
        print(
            f"  {column}: {count:,}"
        )

    print("\n" + "=" * 60)


def save_tables(tables):
    """Save relational tables as CSV files."""

    table_dir = (
        OUTPUT_DIR
        / "tables"
    )

    table_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    summary = {}

    for table_name, table_df in tables.items():

        output_path = (
            table_dir
            / f"{table_name}.csv"
        )

        table_df.to_csv(
            output_path,
            index=False
        )

        summary[table_name] = {
            "row_count":
                len(table_df),

            "column_count":
                len(table_df.columns),

            "columns":
                table_df.columns.tolist(),

            "output_file":
                str(output_path),
        }

    return summary


def display_table_summary(summary):
    """Display relational-table results."""

    print("\n" + "=" * 60)
    print("RELATIONAL TABLE SUMMARY")
    print("=" * 60)

    for table_name, details in (
        summary.items()
    ):

        print(
            f"\nTable: {table_name}"
        )

        print(
            f"  Rows: "
            f"{details['row_count']:,}"
        )

        print(
            f"  Columns: "
            f"{details['column_count']}"
        )

        print(
            "  Fields: "
            + ", ".join(
                details["columns"]
            )
        )

        print(
            f"  Saved to: "
            f"{details['output_file']}"
        )

    print("\n" + "=" * 60)


def display_clean_validation(result):
    """Display clean-data validation."""

    print("\n" + "=" * 60)
    print("CLEAN DATA VALIDATION")
    print("=" * 60)

    print(
        f"\nRaw rows: "
        f"{result['raw_rows']:,}"
    )

    print(
        f"Clean rows: "
        f"{result['clean_rows']:,}"
    )

    print(
        f"Rows removed: "
        f"{result['rows_removed']:,}"
    )

    print(
        f"Percent removed: "
        f"{result['percent_removed']:.2f}%"
    )

    print(
        f"\nRemaining duplicates: "
        f"{result['remaining_duplicates']:,}"
    )

    print("\nValidation checks:")

    for check_name, passed in (
        result["checks"].items()
    ):

        status = (
            "PASS"
            if passed
            else "FAIL"
        )

        print(
            f"  {status}: {check_name}"
        )

    print("\nOverall validation:")

    if result["validation_passed"]:
        print("  ✓ PASSED")
    else:
        print("  ✗ FAILED")

    print("\n" + "=" * 60)


def display_database_load_summary(result):
    """Display database loading results."""

    print("\n" + "=" * 60)
    print("DATABASE LOAD SUMMARY")
    print("=" * 60)

    print("\nTables loaded:")

    for table_name in (
        result["tables_loaded"]
    ):
        print(
            f"  ✓ {table_name}"
        )

    print("\nRows loaded:")

    for table_name, count in (
        result["rows_loaded"].items()
    ):
        print(
            f"  {table_name}: "
            f"{count:,}"
        )

    print(
        f"\nTotal rows loaded: "
        f"{result['total_rows_loaded']:,}"
    )

    print("\n" + "=" * 60)




def run_required_sql_queries(
    connection,
    sql_path
):
    """Execute SQL statements from required_queries.sql.

    Parameters
    ----------
    connection : sqlite3.Connection
        Open SQLite database connection.

    sql_path : str or pathlib.Path
        Path to required_queries.sql.

    Returns
    -------
    dict
        Results for each SQL query, including the requirement description.
    """

    sql_path = Path(sql_path)

    if not sql_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {sql_path}"
        )

    sql_text = sql_path.read_text(
        encoding="utf-8"
    )

    # -----------------------------------------------------
    # Parse Q1, Q2, ... requirement comments and SQL
    # -----------------------------------------------------

    queries = []

    current_name = None
    current_description = None
    current_sql_lines = []

    for line in sql_text.splitlines():

        stripped = line.strip()

        # Ignore empty lines
        if not stripped:
            continue

        # Detect requirement comments such as:
        # -- Q1. Show the row count for each major table.
        if stripped.startswith("-- Q"):

            # Save the previous query before starting a new one
            if (
                current_name is not None
                and current_sql_lines
            ):

                queries.append({
                    "name": current_name,
                    "description":
                        current_description,
                    "sql":
                        "\n".join(
                            current_sql_lines
                        ).strip()
                })

            # Reset SQL lines
            current_sql_lines = []

            # Remove leading "--"
            requirement_text = (
                stripped[2:].strip()
            )

            # Split:
            # Q1. Description...
            parts = requirement_text.split(
                ".",
                1
            )

            current_name = (
                parts[0].strip()
            )

            current_description = (
                parts[1].strip()
                if len(parts) > 1
                else ""
            )

            continue

        # Ignore other comments
        if stripped.startswith("--"):
            continue

        # SQL belonging to current requirement
        if current_name is not None:
            current_sql_lines.append(
                line
            )

    # Save final query
    if (
        current_name is not None
        and current_sql_lines
    ):

        queries.append({
            "name": current_name,
            "description":
                current_description,
            "sql":
                "\n".join(
                    current_sql_lines
                ).strip()
        })

    # -----------------------------------------------------
    # Execute parsed queries
    # -----------------------------------------------------

    results = {}

    cursor = connection.cursor()

    for query in queries:

        query_name = query["name"]

        description = (
            query["description"]
        )

        statement = (
            query["sql"]
            .rstrip(";")
            .strip()
        )

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

            results[query_name] = {
                "description":
                    description,

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

            results[query_name] = {
                "description":
                    description,

                "status":
                    "FAIL",

                "error":
                    str(error),
            }

    return results

def display_sql_results(results):
    """Display results from required SQL checks."""

    print("\n" + "=" * 60)
    print("REQUIRED SQL CHECKS")
    print("=" * 60)

    for query_name, result in results.items():

        print(f"\n{query_name}")

        # Display the SQL requirement
        description = result.get(
            "description",
            "No description provided."
        )

        print(
            f"  Requirement: {description}"
        )

        print(
            f"  Status: {result['status']}"
        )

        if result["status"] == "FAIL":

            print(
                f"  Error: {result['error']}"
            )

            continue

        print(
            f"  Rows returned: "
            f"{result['row_count']:,}"
        )

        columns = result.get(
            "columns",
            []
        )

        if columns:

            print(
                "  Columns: "
                + ", ".join(columns)
            )

        # Show only first five rows in terminal.
        preview_rows = result.get(
            "rows",
            []
        )[:5]

        if preview_rows:

            print("  Preview:")

            for row in preview_rows:

                print(
                    f"    {row}"
                )

        elif result["row_count"] == 0:

            print(
                "  No rows returned."
            )

    print("\n" + "=" * 60)

# ---------------------------------------------------------
# Main execution
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("ISE 2530 - MILESTONE 2")
    print("Data Cleaning and Database Formation")
    print("=" * 60)

    print("\nDataset:")
    print(DATA_PATH)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # =====================================================
    # STEP 1
    # Load raw data
    # =====================================================

    if not ask_to_continue(
        "Step 1: Load the raw dataset?"
    ):
        print("\nExecution stopped.")
        return

    try:

        raw_df = load_raw_data(
            DATA_PATH
        )

    except Exception as error:

        print(
            "\nERROR while loading dataset:"
        )

        print(error)

        return

    print(
        "\n✓ Dataset loaded successfully."
    )

    # =====================================================
    # STEP 2
    # Inspect raw data
    # =====================================================

    if not ask_to_continue(
        "Step 2: Inspect the raw dataset?"
    ):
        return

    try:

        raw_summary = (
            inspect_raw_data(
                raw_df
            )
        )

    except Exception as error:

        print(
            "\nERROR while inspecting dataset:"
        )

        print(error)

        return

    display_raw_summary(
        raw_summary
    )

    save_json(
        raw_summary,
        RAW_INSPECTION_PATH
    )

    print(
        f"\n✓ Saved: "
        f"{RAW_INSPECTION_PATH}"
    )

    # =====================================================
    # STEP 3
    # Clean data
    # =====================================================

    if not ask_to_continue(
        "Step 3: Clean the dataset?"
    ):
        return

    try:

        clean_df = clean_data(
            raw_df
        )

    except Exception as error:

        print(
            "\nERROR while cleaning dataset:"
        )

        print(error)

        return

    clean_df.to_csv(
        CLEANED_DATA_PATH,
        index=False
    )

    cleaning_summary = (
        build_cleaning_summary(
            raw_df,
            clean_df
        )
    )

    display_cleaning_summary(
        cleaning_summary
    )

    save_json(
        cleaning_summary,
        CLEANING_SUMMARY_PATH
    )

    print(
        f"\n✓ Saved: "
        f"{CLEANED_DATA_PATH}"
    )

    print(
        f"✓ Saved: "
        f"{CLEANING_SUMMARY_PATH}"
    )

    # =====================================================
    # STEP 4
    # Create relational tables
    # =====================================================

    if not ask_to_continue(
        "Step 4: Create relational tables?"
    ):
        return

    try:

        tables = split_into_tables(
            clean_df
        )

    except Exception as error:

        print(
            "\nERROR while creating "
            "relational tables:"
        )

        print(error)

        return

    table_summary = save_tables(
        tables
    )

    display_table_summary(
        table_summary
    )

    save_json(
        table_summary,
        TABLE_SUMMARY_PATH
    )

    print(
        f"\n✓ Saved: "
        f"{TABLE_SUMMARY_PATH}"
    )

    # =====================================================
    # STEP 5
    # Validate clean data
    # =====================================================

    if not ask_to_continue(
        "Step 5: Validate cleaned data?"
    ):
        return

    try:

        clean_validation = (
            validate_clean_data(
                raw_df,
                clean_df
            )
        )

    except Exception as error:

        print(
            "\nERROR while validating "
            "cleaned data:"
        )

        print(error)

        return

    display_clean_validation(
        clean_validation
    )

    save_json(
        clean_validation,
        CLEAN_DATA_VALIDATION_PATH
    )

    print(
        f"\n✓ Saved: "
        f"{CLEAN_DATA_VALIDATION_PATH}"
    )

    if not clean_validation[
        "validation_passed"
    ]:

        print(
            "\nClean-data validation failed."
        )

        print(
            "Correct the cleaning implementation "
            "before database creation."
        )

        return

    # =====================================================
    # STEP 6
    # Create SQLite database
    # =====================================================

    if not ask_to_continue(
        "Step 6: Create the SQLite database?"
    ):
        return

    try:

        connection = create_database(
            DATABASE_PATH,
            SCHEMA_PATH
        )

    except Exception as error:

        print(
            "\nERROR while creating database:"
        )

        print(error)

        print(
            "\nCheck schema.sql and "
            "create_database()."
        )

        return

    print(
        "\n✓ SQLite database created."
    )

    print(
        f"  {DATABASE_PATH}"
    )

    # =====================================================
    # STEP 7
    # Load relational tables
    # =====================================================

    if not ask_to_continue(
        "Step 7: Load cleaned tables "
        "into the database?"
    ):

        connection.close()
        return

    try:

        database_load_summary = (
            load_clean_data(
                connection,
                tables
            )
        )

    except Exception as error:

        connection.close()

        print(
            "\nERROR while loading tables "
            "into database:"
        )

        print(error)

        print(
            "\nCheck schema.sql and "
            "load_clean_data()."
        )

        return

    display_database_load_summary(
        database_load_summary
    )

    save_json(
        database_load_summary,
        DATABASE_LOAD_SUMMARY_PATH
    )

    print(
        f"\n✓ Saved: "
        f"{DATABASE_LOAD_SUMMARY_PATH}"
    )

    # =====================================================
    # STEP 8
    # Validate SQLite database
    # =====================================================

    if not ask_to_continue(
        "Step 8: Validate the SQLite database?"
    ):

        connection.close()
        return

    try:

        database_validation = (
            validate_database(
                connection
            )
        )

    except Exception as error:

        connection.close()

        print(
            "\nERROR while validating database:"
        )

        print(error)

        print(
            "\nCheck your implementation of "
            "validate_database() and schema.sql."
        )

        return

    print(
        "\n✓ Database validation completed."
    )

    # -----------------------------------------------------
    # Display database validation results
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("DATABASE VALIDATION")
    print("=" * 60)

    print("\nTables:")

    for table in database_validation["tables"]:
        print(f"  - {table}")

    print("\nRow counts:")

    for table, count in (
        database_validation[
            "row_counts"
        ].items()
    ):

        print(
            f"  {table}: {count:,}"
        )

    print("\nValidation checks:")

    for check_name, passed in (
        database_validation[
            "checks"
        ].items()
    ):

        status = (
            "PASS"
            if passed
            else "FAIL"
        )

        print(
            f"  {status}: {check_name}"
        )

    print("\nForeign-key violations:")

    fk_violations = (
        database_validation[
            "foreign_key_violations"
        ]
    )

    if fk_violations:

        for violation in fk_violations:
            print(
                f"  {violation}"
            )

    else:

        print("  None")

    print("\nOverall validation:")

    if database_validation[
        "validation_passed"
    ]:

        print("  ✓ PASSED")

    else:

        print("  ✗ FAILED")

    print("\n" + "=" * 60)

    # -----------------------------------------------------
    # Save database validation output
    # -----------------------------------------------------

    DATABASE_VALIDATION_PATH = (
        OUTPUT_DIR
        / "database_validation.json"
    )

    save_json(
        database_validation,
        DATABASE_VALIDATION_PATH
    )

    print(
        "\n✓ Database validation saved:"
    )

    print(
        f"  {DATABASE_VALIDATION_PATH}"
    )

    # -----------------------------------------------------
    # Stop if validation failed
    # -----------------------------------------------------

    if not database_validation[
        "validation_passed"
    ]:

        print(
            "\nDatabase validation failed."
        )

        print(
            "Review schema.sql, relational tables, "
            "and database-loading logic."
        )

        connection.close()
        return

    if not ask_to_continue(
        "Step 9: Run the required SQL checks?"
    ):

        connection.close()
        return


    try:

        sql_results = (
            run_required_sql_queries(
                connection,
                REQUIRED_QUERIES_PATH
            )
        )

    except Exception as error:

        connection.close()

        print(
            "\nERROR while running "
            "required SQL queries:"
        )

        print(error)

        print(
            "\nCheck required_queries.sql."
        )

        return


    print(
        "\n✓ Required SQL checks completed."
    )


    display_sql_results(
        sql_results
    )


    save_json(
        sql_results,
        SQL_RESULTS_PATH
    )


    print(
        "\n✓ SQL results saved:"
    )

    print(
        f"  {SQL_RESULTS_PATH}"
    )


    # -----------------------------------------------------
    # Determine whether every query executed
    # -----------------------------------------------------

    sql_execution_passed = all(
        result["status"] == "PASS"
        for result
        in sql_results.values()
    )


    if not sql_execution_passed:

        print(
            "\nOne or more SQL queries failed."
        )

        print(
            "Review required_queries.sql "
            "before completing Milestone 2."
        )

        connection.close()

        return


    connection.close()

    # =====================================================
    # Progress
    # =====================================================

    print("\n" + "=" * 60)
    print("MILESTONE 2 PROGRESS")
    print("=" * 60)

    print("✓ Step 1 - Raw data loaded")
    print("✓ Step 2 - Raw data inspected")
    print("✓ Step 3 - Data cleaned")
    print("✓ Step 4 - Relational tables created")
    print("✓ Step 5 - Clean data validated")
    print("✓ Step 6 - SQLite database created")
    print("✓ Step 7 - Tables loaded into database")
    print("✓ Step 8 - Database validated")
    print("✓ Step 9 - Required SQL checks executed")


if __name__ == "__main__":
    main()