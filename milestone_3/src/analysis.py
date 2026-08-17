"""Milestone 3: analysis of the validated Milestone 2 database."""

import sqlite3
import pandas as pd


def load_analysis_data(connection):
    """Load the database information needed for Milestone 3 analysis.

    Parameters
    ----------
    connection : sqlite3.Connection
        Open connection to the Milestone 2 project database.

    Returns
    -------
    dict[str, pandas.DataFrame]
        Dataset-specific DataFrames needed by calculate_metrics().

    Requirements
    ------------
    - Read from the relational database created in Milestone 2.
    - Use SQL joins when information from multiple tables is needed.
    - Do not read the original raw Excel file in Milestone 3.
    - Return a dictionary of named DataFrames.
    """
    # TODO: implement
    raise NotImplementedError


def calculate_metrics(data):
    """Calculate meaningful project-specific analysis measures.

    Parameters
    ----------
    data : dict[str, pandas.DataFrame]
        Output from load_analysis_data().

    Returns
    -------
    dict[str, object]
        Must contain at least:
        - headline_metrics
        - entity_metrics
        - grouped_comparison
        - time_analysis
        - decision_indicator
        - risk_indicator

    Notes
    -----
    - entity_metrics should normally be a pandas.DataFrame with one row per
      decision object.
    - grouped_comparison should normally be a pandas.DataFrame.
    - time_analysis may be empty only when Milestone 1 approved an alternative.
    - All measures must be explainable from the data.
    """
    # TODO: implement dataset-specific measures
    raise NotImplementedError


def validate_analysis_results(metrics):
    """Validate Milestone 3 analysis outputs.

    Returns
    -------
    dict
        Must contain at least:
        - required_sections_present
        - entity_count
        - missing_values_in_key_outputs
        - validation_passed

    Add dataset-specific checks when appropriate.
    """
    # TODO: implement
    raise NotImplementedError
