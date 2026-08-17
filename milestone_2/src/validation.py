"""Milestone 2: Clean-data and database validation."""

import pandas as pd
import sqlite3


def validate_clean_data(raw_df, clean_df):
    """Compare raw and cleaned data and report quality checks.

    Returns
    -------
    dict
        Must contain at least:
        - raw_rows
        - clean_rows
        - rows_removed
        - remaining_missing
        - remaining_duplicates
        - validation_passed

    validation_passed should reflect your documented project rules, not simply
    whether every missing value has disappeared.
    """
    # TODO: implement
    raise NotImplementedError


def validate_database(connection):
    """Validate the final SQLite database.

    Returns
    -------
    dict
        Must contain at least:
        - tables
        - row_counts
        - foreign_key_violations
        - validation_passed

    Add dataset-specific integrity checks when appropriate.
    """
    # TODO: implement
    raise NotImplementedError
