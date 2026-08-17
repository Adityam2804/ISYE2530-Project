"""ISE 2530 Course Project - Milestone 2 Interactive Runner.

Instructor-provided file. Students should not modify this file.
"""

from pathlib import Path
import json

from src.data_loading import load_raw_data, inspect_raw_data
from src.cleaning import clean_data, split_into_tables
from src.validation import validate_clean_data, validate_database
from src.database import create_database, load_clean_data

DATA_PATH = Path("../milestone_1/dataset.xlsx")
OUTPUT_DIR = Path("outputs")
RAW_INSPECTION_PATH = OUTPUT_DIR / "raw_data_inspection.json"
CLEANED_DATA_PATH = OUTPUT_DIR / "cleaned_data.csv"
CLEANING_SUMMARY_PATH = OUTPUT_DIR / "cleaning_summary.json"
TABLE_SUMMARY_PATH = OUTPUT_DIR / "table_summary.json"
CLEAN_DATA_VALIDATION_PATH = OUTPUT_DIR / "clean_data_validation.json"
SCHEMA_PATH = Path("sql/schema.sql")
DATABASE_PATH = OUTPUT_DIR / "project.db"
DATABASE_LOAD_SUMMARY_PATH = OUTPUT_DIR / "database_load_summary.json"
DATABASE_VALIDATION_PATH = OUTPUT_DIR / "database_validation.json"
REQUIRED_QUERIES_PATH = Path("sql/required_queries.sql")
SQL_RESULTS_PATH = OUTPUT_DIR / "sql_results.json"


def ask_to_continue(message):
    while True:
        answer = input(f"\n{message} [y/n]: ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")


def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, default=str)


def build_cleaning_summary(raw_df, clean_df):
    raw_rows = len(raw_df)
    clean_rows = len(clean_df)
    rows_removed = raw_rows - clean_rows
    percent_removed = rows_removed / raw_rows * 100 if raw_rows else 0
    return {
        "raw_rows": raw_rows,
        "clean_rows": clean_rows,
        "rows_removed": rows_removed,
        "percent_removed": round(percent_removed, 2),
        "remaining_missing_by_column": {
            c: int(v) for c, v in clean_df.isna().sum().items()
        },
        "remaining_duplicate_rows": int(clean_df.duplicated().sum()),
        "columns": clean_df.columns.tolist(),
        "dtypes": {c: str(t) for c, t in clean_df.dtypes.items()},
    }


def save_tables(tables):
    table_dir = OUTPUT_DIR / "tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    summary = {}
    for table_name, table_df in tables.items():
        output_path = table_dir / f"{table_name}.csv"
        table_df.to_csv(output_path, index=False)
        summary[table_name] = {
            "row_count": len(table_df),
            "column_count": len(table_df.columns),
            "columns": table_df.columns.tolist(),
            "output_file": str(output_path),
        }
    return summary


def run_required_sql_queries(connection, sql_path):
    sql_path = Path(sql_path)
    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    sql_text = sql_path.read_text(encoding="utf-8")
    queries = []
    current_name = None
    current_description = None
    current_sql_lines = []

    for line in sql_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("-- Q"):
            if current_name is not None and current_sql_lines:
                queries.append({
                    "name": current_name,
                    "description": current_description,
                    "sql": "\n".join(current_sql_lines).strip(),
                })
            current_sql_lines = []
            requirement_text = stripped[2:].strip()
            parts = requirement_text.split(".", 1)
            current_name = parts[0].strip()
            current_description = parts[1].strip() if len(parts) > 1 else ""
            continue
        if stripped.startswith("--"):
            continue
        if current_name is not None:
            current_sql_lines.append(line)

    if current_name is not None and current_sql_lines:
        queries.append({
            "name": current_name,
            "description": current_description,
            "sql": "\n".join(current_sql_lines).strip(),
        })

    results = {}
    cursor = connection.cursor()
    for query in queries:
        query_name = query["name"]
        statement = query["sql"].rstrip(";").strip()
        try:
            cursor.execute(statement)
            columns = [c[0] for c in cursor.description] if cursor.description else []
            rows = [list(row) for row in cursor.fetchall()] if cursor.description else []
            results[query_name] = {
                "description": query["description"],
                "status": "PASS",
                "columns": columns,
                "row_count": len(rows),
                "rows": rows,
            }
        except Exception as error:
            results[query_name] = {
                "description": query["description"],
                "status": "FAIL",
                "error": str(error),
            }
    return results


def display_sql_results(results):
    print("\n" + "=" * 60)
    print("REQUIRED SQL CHECKS")
    print("=" * 60)
    for query_name, result in results.items():
        print(f"\n{query_name}")
        print(f"  Requirement: {result.get('description', 'No description provided.')}")
        print(f"  Status: {result['status']}")
        if result["status"] == "FAIL":
            print(f"  Error: {result['error']}")
            continue
        print(f"  Rows returned: {result['row_count']:,}")
        columns = result.get("columns", [])
        if columns:
            print("  Columns: " + ", ".join(columns))
        preview = result.get("rows", [])[:5]
        if preview:
            print("  Preview:")
            for row in preview:
                print(f"    {row}")
        elif result["row_count"] == 0:
            print("  No rows returned.")


def main():
    print("=" * 60)
    print("ISE 2530 - MILESTONE 2")
    print("Data Cleaning and Database Formation")
    print("=" * 60)
    print(f"\nDataset: {DATA_PATH}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not ask_to_continue("Step 1: Load the raw dataset?"):
        return
    try:
        raw_df = load_raw_data(DATA_PATH)
    except Exception as error:
        print(f"\nERROR while loading dataset:\n{error}")
        return
    print(f"\n[PASS] Loaded {len(raw_df):,} rows and {len(raw_df.columns)} columns.")

    if not ask_to_continue("Step 2: Inspect the raw dataset?"):
        return
    try:
        raw_summary = inspect_raw_data(raw_df)
    except Exception as error:
        print(f"\nERROR while inspecting dataset:\n{error}")
        return
    save_json(raw_summary, RAW_INSPECTION_PATH)
    print(f"\n[PASS] Saved: {RAW_INSPECTION_PATH}")

    if not ask_to_continue("Step 3: Clean the dataset?"):
        return
    try:
        clean_df = clean_data(raw_df)
    except Exception as error:
        print(f"\nERROR while cleaning dataset:\n{error}")
        return
    clean_df.to_csv(CLEANED_DATA_PATH, index=False)
    cleaning_summary = build_cleaning_summary(raw_df, clean_df)
    save_json(cleaning_summary, CLEANING_SUMMARY_PATH)
    print(f"\n[PASS] Saved: {CLEANED_DATA_PATH}")
    print(f"[PASS] Saved: {CLEANING_SUMMARY_PATH}")

    if not ask_to_continue("Step 4: Create relational tables?"):
        return
    try:
        tables = split_into_tables(clean_df)
    except Exception as error:
        print(f"\nERROR while creating relational tables:\n{error}")
        return
    table_summary = save_tables(tables)
    save_json(table_summary, TABLE_SUMMARY_PATH)
    print(f"\n[PASS] Saved: {TABLE_SUMMARY_PATH}")

    if not ask_to_continue("Step 5: Validate cleaned data?"):
        return
    try:
        clean_validation = validate_clean_data(raw_df, clean_df)
    except Exception as error:
        print(f"\nERROR while validating cleaned data:\n{error}")
        return
    save_json(clean_validation, CLEAN_DATA_VALIDATION_PATH)
    print(f"\n[PASS] Saved: {CLEAN_DATA_VALIDATION_PATH}")
    if not clean_validation.get("validation_passed", False):
        print("\nClean-data validation failed. Correct the cleaning before continuing.")
        return

    if not ask_to_continue("Step 6: Create the SQLite database?"):
        return
    try:
        connection = create_database(DATABASE_PATH, SCHEMA_PATH)
    except Exception as error:
        print(f"\nERROR while creating database:\n{error}")
        return
    print(f"\n[PASS] SQLite database created: {DATABASE_PATH}")

    if not ask_to_continue("Step 7: Load cleaned tables into the database?"):
        connection.close(); return
    try:
        database_load_summary = load_clean_data(connection, tables)
    except Exception as error:
        connection.close()
        print(f"\nERROR while loading database:\n{error}")
        return
    save_json(database_load_summary, DATABASE_LOAD_SUMMARY_PATH)
    print(f"\n[PASS] Saved: {DATABASE_LOAD_SUMMARY_PATH}")

    if not ask_to_continue("Step 8: Validate the SQLite database?"):
        connection.close(); return
    try:
        database_validation = validate_database(connection)
    except Exception as error:
        connection.close()
        print(f"\nERROR while validating database:\n{error}")
        return
    save_json(database_validation, DATABASE_VALIDATION_PATH)
    print(f"\n[PASS] Saved: {DATABASE_VALIDATION_PATH}")
    if not database_validation.get("validation_passed", False):
        connection.close()
        print("\nDatabase validation failed. Correct the database before continuing.")
        return

    if not ask_to_continue("Step 9: Run the required SQL checks?"):
        connection.close(); return
    try:
        sql_results = run_required_sql_queries(connection, REQUIRED_QUERIES_PATH)
    except Exception as error:
        connection.close()
        print(f"\nERROR while running SQL checks:\n{error}")
        return
    display_sql_results(sql_results)
    save_json(sql_results, SQL_RESULTS_PATH)
    connection.close()

    print("\n" + "=" * 60)
    print("MILESTONE 2 TECHNICAL WORKFLOW COMPLETE")
    print("=" * 60)
    print(f"\nOutputs: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
