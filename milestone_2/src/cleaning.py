"""Milestone 2: dataset-specific cleaning and relational splitting.

STUDENT FILE
------------
You will complete only the clearly marked STUDENT TODO sections.

The instructor already provides:
- copying the raw DataFrame safely
- duplicate removal
- common text cleanup
- date conversion helpers
- numeric-rule helpers
- checks on the returned relational-table dictionary

Your job is to make DATASET-SPECIFIC choices based on:
- your Milestone 1 data description
- your Milestone 1 feasibility preview
- the actual problems visible in dataset.xlsx

Do not copy another team's column names.
"""

from __future__ import annotations

import pandas as pd


# ============================================================
# INSTRUCTOR-PROVIDED HELPERS
# ============================================================

def _clean_text_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Trim whitespace and normalize empty strings to missing values."""
    result = df.copy()

    for column in columns:
        if column not in result.columns:
            raise ValueError(
                f"Text-cleaning column '{column}' does not exist. "
                f"Available columns: {list(result.columns)}"
            )

        series = result[column].astype("string")

        series = (
            series
            .str.strip()
            .replace(
                {
                    "": pd.NA,
                    "nan": pd.NA,
                    "None": pd.NA,
                }
            )
        )

        result[column] = series

    return result


def _convert_date_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Convert selected columns to pandas datetime."""
    result = df.copy()

    for column in columns:
        if column not in result.columns:
            raise ValueError(
                f"Date column '{column}' does not exist."
            )

        result[column] = pd.to_datetime(
            result[column],
            errors="coerce",
        )

    return result


def _apply_category_replacements(
    df: pd.DataFrame,
    replacements: dict[str, dict],
) -> pd.DataFrame:
    """Apply explicit category-label replacements.

    Example configuration
    ---------------------
    {
        "Status": {
            "complete ": "Complete",
            "COMPLETE": "Complete"
        }
    }
    """
    result = df.copy()

    for column, mapping in replacements.items():
        if column not in result.columns:
            raise ValueError(
                f"Category column '{column}' does not exist."
            )

        result[column] = result[column].replace(
            mapping
        )

    return result


def _apply_numeric_rules(
    df: pd.DataFrame,
    rules: list[dict],
) -> pd.DataFrame:
    """Apply simple, explicit numeric validity rules.

    Supported rule format
    ---------------------
    {
        "column": "numeric_column",
        "minimum": 0,          # optional
        "maximum": 100,        # optional
        "action": "remove"     # currently supported action
    }

    Use only rules that you can justify in cleaning_report.md.
    """
    result = df.copy()

    for rule in rules:
        column = rule.get("column")
        minimum = rule.get("minimum")
        maximum = rule.get("maximum")
        action = rule.get("action", "remove")

        if column not in result.columns:
            raise ValueError(
                f"Numeric-rule column '{column}' does not exist."
            )

        numeric = pd.to_numeric(
            result[column],
            errors="coerce",
        )

        invalid = pd.Series(
            False,
            index=result.index,
        )

        if minimum is not None:
            invalid = invalid | (
                numeric < minimum
            )

        if maximum is not None:
            invalid = invalid | (
                numeric > maximum
            )

        # Missing values are handled separately.
        invalid = invalid.fillna(False)

        if action == "remove":
            result = result.loc[
                ~invalid
            ].copy()
        else:
            raise ValueError(
                f"Unsupported numeric-rule action: {action}"
            )

    return result


def _validate_table_dictionary(
    tables: dict[str, pd.DataFrame],
) -> None:
    """Perform basic checks on split_into_tables() output."""
    if not isinstance(tables, dict):
        raise TypeError(
            "split_into_tables() must return a dictionary."
        )

    if len(tables) < 2:
        raise ValueError(
            "Return at least two meaningful relational tables "
            "unless the instructor approved another design."
        )

    for table_name, dataframe in tables.items():
        if not isinstance(table_name, str):
            raise TypeError(
                "Every table name must be a string."
            )

        if not table_name.strip():
            raise ValueError(
                "Table names cannot be empty."
            )

        if not isinstance(
            dataframe,
            pd.DataFrame,
        ):
            raise TypeError(
                f"Table '{table_name}' must be a pandas DataFrame."
            )

        if dataframe.empty:
            raise ValueError(
                f"Table '{table_name}' contains zero rows."
            )


# ============================================================
# STUDENT TASK 1 — CLEAN THE DATA
# ============================================================

def clean_data(df):
    """Return a cleaned copy of the approved dataset.

    What YOU complete
    -----------------
    1A. Columns where missing values make a row unusable
    1B. Text columns needing whitespace cleanup
    1C. Date/time columns
    1D. Category-label replacements, if needed
    1E. Simple numeric validity rules, if justified
    1F. A small OPTIONAL custom-cleaning section

    What is already provided
    ------------------------
    - copying the data
    - exact duplicate removal
    - generic cleanup mechanics
    - configuration validation

    Important
    ---------
    Do NOT remove data simply because it "looks unusual."
    Every important rule must be justified in cleaning_report.md.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "df must be a pandas DataFrame."
        )

    if df.empty:
        raise ValueError(
            "Raw dataset contains zero rows."
        )

    clean_df = df.copy()

    # --------------------------------------------------------
    # INSTRUCTOR-PROVIDED:
    # Remove exact duplicate rows.
    #
    # This is a common baseline cleaning operation.
    # If duplicates have special meaning in your project,
    # discuss that with the instructor before changing this.
    # --------------------------------------------------------

    clean_df = (
        clean_df
        .drop_duplicates()
        .copy()
    )

    # --------------------------------------------------------
    # STUDENT TODO 1A — Required non-missing columns
    #
    # Put ONLY columns here when a missing value makes the row
    # unusable for the approved project.
    #
    # Example:
    # REQUIRED_NON_NULL_COLUMNS = [
    #     "TransactionID",
    # ]
    #
    # Do NOT automatically put every column here.
    # --------------------------------------------------------

    REQUIRED_NON_NULL_COLUMNS = []

    for column in REQUIRED_NON_NULL_COLUMNS:
        if column not in clean_df.columns:
            raise ValueError(
                f"Required column '{column}' does not exist."
            )

    if REQUIRED_NON_NULL_COLUMNS:
        clean_df = clean_df.dropna(
            subset=REQUIRED_NON_NULL_COLUMNS
        ).copy()

    # --------------------------------------------------------
    # STUDENT TODO 1B — Text columns
    #
    # Add columns where leading/trailing spaces or empty text
    # values should be standardized.
    #
    # Example:
    # TEXT_COLUMNS = [
    #     "Category",
    #     "Country",
    # ]
    # --------------------------------------------------------

    TEXT_COLUMNS = []

    clean_df = _clean_text_columns(
        clean_df,
        TEXT_COLUMNS,
    )

    # --------------------------------------------------------
    # STUDENT TODO 1C — Date/time columns
    #
    # Example:
    # DATE_COLUMNS = ["EventDate"]
    #
    # If there are no meaningful date columns:
    # DATE_COLUMNS = []
    # --------------------------------------------------------

    DATE_COLUMNS = []

    clean_df = _convert_date_columns(
        clean_df,
        DATE_COLUMNS,
    )

    # --------------------------------------------------------
    # STUDENT TODO 1D — Category replacements
    #
    # Use this ONLY for labels you know represent the same
    # category.
    #
    # Example:
    #
    # CATEGORY_REPLACEMENTS = {
    #     "Region": {
    #         "north ": "North",
    #         "NORTH": "North",
    #     }
    # }
    #
    # If no replacements are needed:
    # CATEGORY_REPLACEMENTS = {}
    # --------------------------------------------------------

    CATEGORY_REPLACEMENTS = {}

    clean_df = _apply_category_replacements(
        clean_df,
        CATEGORY_REPLACEMENTS,
    )

    # --------------------------------------------------------
    # STUDENT TODO 1E — Numeric validity rules
    #
    # Add ONLY rules supported by the meaning of the column.
    #
    # Example:
    # NUMERIC_RULES = [
    #     {
    #         "column": "WaitTimeMinutes",
    #         "minimum": 0,
    #         "maximum": None,
    #         "action": "remove",
    #     }
    # ]
    #
    # Important:
    # A negative value is NOT automatically invalid.
    # For example, negative quantities may represent returns.
    # Investigate the data definition first.
    # --------------------------------------------------------

    NUMERIC_RULES = []

    clean_df = _apply_numeric_rules(
        clean_df,
        NUMERIC_RULES,
    )

    # --------------------------------------------------------
    # STUDENT TODO 1F — Optional custom cleaning
    #
    # Use this small section only if your project needs a rule
    # that cannot be expressed above.
    #
    # Keep it simple and explain it in cleaning_report.md.
    #
    # Example:
    #
    # clean_df["SomeID"] = (
    #     clean_df["SomeID"]
    #     .astype("string")
    #     .str.strip()
    # )
    #
    # If no additional rule is needed, leave this section
    # unchanged.
    # --------------------------------------------------------

    # STUDENT OPTIONAL CUSTOM CLEANING HERE

    clean_df = clean_df.reset_index(
        drop=True
    )

    return clean_df


# ============================================================
# STUDENT TASK 2 — SPLIT INTO RELATIONAL TABLES
# ============================================================

def split_into_tables(clean_df):
    """Convert cleaned data into meaningful relational tables.

    What YOU complete
    -----------------
    Define the tables approved for your project in Milestone 1.

    You are NOT expected to build database-loading infrastructure.
    This function only creates pandas DataFrames.

    Requirements
    ------------
    - Return at least two meaningful tables unless approved otherwise.
    - Table names must exactly match schema.sql.
    - Keep primary-key and foreign-key fields needed for relationships.
    - One entity table should normally contain one row per entity.

    Helpful patterns
    ----------------
    ENTITY TABLE:

        entities = (
            clean_df[
                ["EntityID", "Category"]
            ]
            .dropna(subset=["EntityID"])
            .drop_duplicates(subset=["EntityID"])
            .reset_index(drop=True)
        )

    EVENT / TRANSACTION TABLE:

        events = (
            clean_df[
                ["EventID", "EntityID", "EventDate", "Value"]
            ]
            .copy()
            .reset_index(drop=True)
        )

    LINK / DETAIL TABLE:
        Sometimes one row in the original dataset represents a detail line.
        If no natural unique identifier exists, you may create a simple
        surrogate integer ID using:

        details = clean_df[["EventID", "ItemID", "Value"]].copy()
        details.insert(
            0,
            "detail_id",
            range(1, len(details) + 1),
        )
    """

    if not isinstance(
        clean_df,
        pd.DataFrame,
    ):
        raise TypeError(
            "clean_df must be a pandas DataFrame."
        )

    if clean_df.empty:
        raise ValueError(
            "clean_df contains zero rows."
        )

    # --------------------------------------------------------
    # STUDENT TODO 2A — Create table 1
    #
    # Replace the placeholder with the first meaningful table
    # from your approved relational design.
    # --------------------------------------------------------

    table_1 = None

    # --------------------------------------------------------
    # STUDENT TODO 2B — Create table 2
    #
    # Replace the placeholder with the second meaningful table.
    # --------------------------------------------------------

    table_2 = None

    if not isinstance(table_1, pd.DataFrame):
        raise NotImplementedError(
            "Create your first relational DataFrame in "
            "split_into_tables()."
        )

    if not isinstance(table_2, pd.DataFrame):
        raise NotImplementedError(
            "Create your second relational DataFrame in "
            "split_into_tables()."
        )

    # --------------------------------------------------------
    # STUDENT TODO 2C — Name the tables
    #
    # These names MUST match CREATE TABLE names in schema.sql.
    #
    # Example:
    #
    # tables = {
    #     "entities": table_1,
    #     "events": table_2,
    # }
    #
    # If your approved schema contains more than two tables,
    # create them above and add them to this dictionary.
    # --------------------------------------------------------

    tables = {
        "STUDENT_TABLE_1": table_1,
        "STUDENT_TABLE_2": table_2,
    }

    if any(
        name.startswith("STUDENT_")
        for name in tables
    ):
        raise NotImplementedError(
            "Replace STUDENT_TABLE_1/STUDENT_TABLE_2 with "
            "the actual table names from schema.sql."
        )

    _validate_table_dictionary(
        tables
    )

    return tables
