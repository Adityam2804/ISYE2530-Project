"""Milestone 3: analysis of the validated Milestone 2 database.

STUDENT FILE
------------
You will complete only the clearly marked STUDENT TODO sections.

The instructor has already provided:
- database-schema inspection helpers
- query execution helpers
- input/output validation
- output structure
- most error handling

Your main responsibility is to decide:
1. What information from YOUR Milestone 2 database is needed?
2. What is YOUR decision object?
3. What 3+ measures help describe that decision object?
4. What grouped and time-based comparisons are meaningful?

Do not copy table/column names from another team's project.
"""

from __future__ import annotations

import sqlite3
from typing import Any

import pandas as pd


# ============================================================
# INSTRUCTOR-PROVIDED HELPERS
# Do not modify unless instructed.
# ============================================================

def list_database_tables(connection: sqlite3.Connection) -> list[str]:
    """Return user-created SQLite table names."""
    rows = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    ).fetchall()

    return [str(row[0]) for row in rows]


def get_table_columns(
    connection: sqlite3.Connection,
    table_name: str,
) -> list[str]:
    """Return column names for one SQLite table."""
    safe_name = str(table_name).replace('"', '""')
    rows = connection.execute(
        f'PRAGMA table_info("{safe_name}")'
    ).fetchall()

    return [str(row[1]) for row in rows]


def describe_database_schema(
    connection: sqlite3.Connection,
) -> dict[str, list[str]]:
    """Return a simple {table: [columns]} schema dictionary."""
    return {
        table_name: get_table_columns(connection, table_name)
        for table_name in list_database_tables(connection)
    }


def read_sql(
    connection: sqlite3.Connection,
    query: str,
) -> pd.DataFrame:
    """Run one SELECT query and return a DataFrame."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("SQL query cannot be empty.")

    return pd.read_sql_query(query, connection)


def convert_date_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """Convert selected columns to pandas datetime when they exist."""
    result = df.copy()

    for column in columns:
        if column in result.columns:
            result[column] = pd.to_datetime(
                result[column],
                errors="coerce",
            )

    return result


# ============================================================
# STUDENT TASK 1
# ============================================================

def load_analysis_data(connection):
    """Load database information needed for Milestone 3 analysis.

    Parameters
    ----------
    connection : sqlite3.Connection
        Open connection to the Milestone 2 project database.

    Returns
    -------
    dict[str, pandas.DataFrame]
        Must contain:
        - analysis_data

        You may return additional named DataFrames if useful.

    What YOU need to do
    -------------------
    Complete only the STUDENT TODO sections below.

    Step A
        Look at the schema printed by main.py.

    Step B
        Identify the tables needed for your approved M1 decision.

    Step C
        Write ONE useful SQL query that creates an analysis-ready dataset.
        Usually this requires one or more JOINs.

    Step D
        List any date/time columns that should be converted to pandas datetime.

    Important
    ---------
    - Use project.db from Milestone 2.
    - Do NOT read dataset.xlsx.
    - Your table names depend on YOUR M2 schema.
    """

    schema = describe_database_schema(connection)

    if not schema:
        raise ValueError(
            "The Milestone 2 database contains no user-created tables."
        )

    # --------------------------------------------------------
    # STUDENT TODO 1A
    # Write an analysis query using YOUR M2 tables.
    #
    # Example SHAPE only — do not copy these names:
    #
    # ANALYSIS_QUERY = """
    # SELECT
    #     a.entity_id,
    #     a.category,
    #     b.event_date,
    #     b.numeric_value
    # FROM entity_table AS a
    # JOIN event_table AS b
    #     ON a.entity_id = b.entity_id
    # """
    #
    # Your query should normally include:
    # - the identifier for the decision object
    # - fields needed for at least 3 measures
    # - a grouping/category field when available
    # - a date/time field when available
    # --------------------------------------------------------

    ANALYSIS_QUERY = """
    -- STUDENT TODO:
    -- Replace this comment with your SELECT query.
    """

    if "STUDENT TODO" in ANALYSIS_QUERY:
        raise NotImplementedError(
            "Complete ANALYSIS_QUERY in load_analysis_data(). "
            "Use the schema printed by main.py to choose your tables and columns."
        )

    analysis_data = read_sql(
        connection,
        ANALYSIS_QUERY,
    )

    if analysis_data.empty:
        raise ValueError(
            "Your analysis query returned zero rows. "
            "Check the JOIN conditions and filters."
        )

    # --------------------------------------------------------
    # STUDENT TODO 1B
    # List date/time columns returned by ANALYSIS_QUERY.
    #
    # Example:
    # DATE_COLUMNS = ["event_date"]
    #
    # If your approved project has no time field:
    # DATE_COLUMNS = []
    # --------------------------------------------------------

    DATE_COLUMNS = []

    analysis_data = convert_date_columns(
        analysis_data,
        DATE_COLUMNS,
    )

    # Instructor-provided standardized return structure.
    return {
        "analysis_data": analysis_data,
    }


# ============================================================
# STUDENT TASK 2
# ============================================================

def calculate_metrics(data):
    """Calculate meaningful project-specific measures.

    Returns
    -------
    dict[str, object]
        Must contain:
        - headline_metrics
        - entity_metrics
        - grouped_comparison
        - time_analysis
        - decision_indicator
        - risk_indicator

    Student responsibility
    ----------------------
    You are NOT building this entire function from scratch.

    Complete the five marked tasks:
    2A. identify the decision-object ID
    2B. create at least 3 entity-level measures
    2C. create one grouped comparison
    2D. create one time-based analysis (or approved alternative)
    2E. identify one decision indicator and one risk/exception indicator
    """

    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary.")

    analysis_data = data.get("analysis_data")

    if not isinstance(analysis_data, pd.DataFrame):
        raise TypeError(
            "data['analysis_data'] must be a pandas DataFrame."
        )

    if analysis_data.empty:
        raise ValueError("analysis_data is empty.")

    df = analysis_data.copy()

    # --------------------------------------------------------
    # STUDENT TODO 2A — Decision object
    #
    # Enter the column that identifies the entity you are
    # ranking/reviewing.
    #
    # Examples of decision objects:
    # customer, product, supplier, shipment, facility, region
    #
    # Example:
    # ENTITY_ID_COLUMN = "customer_id"
    # --------------------------------------------------------

    ENTITY_ID_COLUMN = ""

    if not ENTITY_ID_COLUMN:
        raise NotImplementedError(
            "Set ENTITY_ID_COLUMN in calculate_metrics()."
        )

    if ENTITY_ID_COLUMN not in df.columns:
        raise ValueError(
            f"ENTITY_ID_COLUMN '{ENTITY_ID_COLUMN}' is not present "
            f"in analysis_data. Available columns: {list(df.columns)}"
        )

    # --------------------------------------------------------
    # INSTRUCTOR-PROVIDED headline measures
    #
    # These are intentionally generic and give every project
    # a consistent starting point.
    # --------------------------------------------------------

    headline_metrics = {
        "analysis_rows": int(len(df)),
        "decision_object_count": int(
            df[ENTITY_ID_COLUMN].dropna().nunique()
        ),
        "analysis_columns": int(len(df.columns)),
    }

    # --------------------------------------------------------
    # STUDENT TODO 2B — Entity-level measures
    #
    # Goal:
    # Create ONE ROW PER decision object and calculate at least
    # THREE useful measures.
    #
    # You only need to replace the example aggregation block.
    #
    # Example pattern:
    #
    # entity_metrics = (
    #     df.dropna(subset=[ENTITY_ID_COLUMN])
    #       .groupby(ENTITY_ID_COLUMN)
    #       .agg(
    #           event_count=("event_id", "nunique"),
    #           total_value=("numeric_value", "sum"),
    #           average_value=("numeric_value", "mean"),
    #       )
    #       .reset_index()
    # )
    #
    # Choose measures that make sense for YOUR decision.
    # --------------------------------------------------------

    entity_metrics = None  # STUDENT TODO: replace with groupby/agg result

    if not isinstance(entity_metrics, pd.DataFrame):
        raise NotImplementedError(
            "Create entity_metrics in calculate_metrics(). "
            "It should contain one row per decision object."
        )

    if entity_metrics.empty:
        raise ValueError("entity_metrics contains zero rows.")

    # Standardize the identifier for later functions.
    if "record_id" not in entity_metrics.columns:
        entity_metrics["record_id"] = (
            entity_metrics[ENTITY_ID_COLUMN]
            .astype(str)
        )

    # --------------------------------------------------------
    # STUDENT TODO 2C — Grouped comparison
    #
    # Compare a meaningful category/group.
    #
    # Examples:
    # - activity by region
    # - average delay by facility
    # - volume by supplier type
    #
    # Example pattern:
    #
    # grouped_comparison = (
    #     df.groupby("category")
    #       .agg(
    #           record_count=(ENTITY_ID_COLUMN, "nunique"),
    #           average_value=("numeric_value", "mean"),
    #       )
    #       .reset_index()
    # )
    # --------------------------------------------------------

    grouped_comparison = None  # STUDENT TODO

    if not isinstance(grouped_comparison, pd.DataFrame):
        raise NotImplementedError(
            "Create grouped_comparison in calculate_metrics()."
        )

    # --------------------------------------------------------
    # STUDENT TODO 2D — Time-based analysis
    #
    # If a useful time field was approved in M1, summarize one
    # meaningful measure over time.
    #
    # Example pattern:
    #
    # temp = df.dropna(subset=["event_date"]).copy()
    # temp["period"] = temp["event_date"].dt.to_period("M").astype(str)
    #
    # time_analysis = (
    #     temp.groupby("period")
    #         .agg(
    #             event_count=("event_id", "nunique"),
    #             total_value=("numeric_value", "sum"),
    #         )
    #         .reset_index()
    # )
    #
    # If the instructor approved a non-time alternative:
    # time_analysis = pd.DataFrame({
    #     "alternative_analysis": [...],
    #     "value": [...]
    # })
    # --------------------------------------------------------

    time_analysis = None  # STUDENT TODO

    if not isinstance(time_analysis, pd.DataFrame):
        raise NotImplementedError(
            "Create time_analysis (or the approved alternative)."
        )

    # --------------------------------------------------------
    # STUDENT TODO 2E — Decision and risk indicators
    #
    # These are short labels/names, not essays.
    #
    # decision_indicator:
    #   the measure most directly related to the recurring
    #   decision.
    #
    # risk_indicator:
    #   a measure/flag that suggests uncertainty, exception,
    #   missing evidence, unusual behavior, or need for review.
    #
    # Examples:
    # decision_indicator = "total_activity"
    # risk_indicator = "limited_history_flag"
    # --------------------------------------------------------

    decision_indicator = ""
    risk_indicator = ""

    if not decision_indicator:
        raise NotImplementedError(
            "Set decision_indicator in calculate_metrics()."
        )

    if not risk_indicator:
        raise NotImplementedError(
            "Set risk_indicator in calculate_metrics()."
        )

    # Instructor-provided standardized output contract.
    return {
        "headline_metrics": headline_metrics,
        "entity_metrics": entity_metrics,
        "grouped_comparison": grouped_comparison,
        "time_analysis": time_analysis,
        "decision_indicator": decision_indicator,
        "risk_indicator": risk_indicator,
        "entity_id_column": ENTITY_ID_COLUMN,
    }


# ============================================================
# INSTRUCTOR-PROVIDED VALIDATION
# Students normally do not need to modify this function.
# ============================================================

def validate_analysis_results(metrics):
    """Validate the standardized Milestone 3 analysis outputs."""

    required_sections = [
        "headline_metrics",
        "entity_metrics",
        "grouped_comparison",
        "time_analysis",
        "decision_indicator",
        "risk_indicator",
    ]

    required_sections_present = {
        section: section in metrics
        for section in required_sections
    }

    entity_metrics = metrics.get("entity_metrics")
    grouped_comparison = metrics.get("grouped_comparison")
    time_analysis = metrics.get("time_analysis")

    entity_count = (
        int(len(entity_metrics))
        if isinstance(entity_metrics, pd.DataFrame)
        else 0
    )

    missing_values_in_key_outputs = {}

    if isinstance(entity_metrics, pd.DataFrame):
        for column in entity_metrics.columns:
            missing_values_in_key_outputs[column] = int(
                entity_metrics[column].isna().sum()
            )

    record_id_present = (
        isinstance(entity_metrics, pd.DataFrame)
        and "record_id" in entity_metrics.columns
    )

    duplicate_record_ids = (
        int(entity_metrics["record_id"].duplicated().sum())
        if record_id_present
        else None
    )

    checks = {
        "all_required_sections_present": all(
            required_sections_present.values()
        ),
        "entity_metrics_is_dataframe": isinstance(
            entity_metrics, pd.DataFrame
        ),
        "entity_metrics_not_empty": entity_count > 0,
        "record_id_present": record_id_present,
        "unique_record_ids": (
            duplicate_record_ids == 0
            if duplicate_record_ids is not None
            else False
        ),
        "grouped_comparison_is_dataframe": isinstance(
            grouped_comparison, pd.DataFrame
        ),
        "grouped_comparison_not_empty": (
            isinstance(grouped_comparison, pd.DataFrame)
            and not grouped_comparison.empty
        ),
        "time_analysis_is_dataframe": isinstance(
            time_analysis, pd.DataFrame
        ),
        "time_analysis_not_empty": (
            isinstance(time_analysis, pd.DataFrame)
            and not time_analysis.empty
        ),
        "decision_indicator_defined": bool(
            metrics.get("decision_indicator")
        ),
        "risk_indicator_defined": bool(
            metrics.get("risk_indicator")
        ),
    }

    return {
        "required_sections_present": required_sections_present,
        "entity_count": entity_count,
        "missing_values_in_key_outputs": missing_values_in_key_outputs,
        "duplicate_record_ids": duplicate_record_ids,
        "checks": checks,
        "validation_passed": bool(all(checks.values())),
    }
