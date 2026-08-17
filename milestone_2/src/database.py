"""Milestone 2: SQLite database creation and loading."""

from pathlib import Path
import sqlite3
import pandas as pd


def create_database(db_path, schema_path):
    """Create a SQLite database using schema.sql.

    Parameters
    ----------
    db_path : str or pathlib.Path
    schema_path : str or pathlib.Path

    Returns
    -------
    sqlite3.Connection

    Requirements
    ------------
    - Read and execute the supplied/completed schema SQL.
    - Enable foreign-key checking.
    - Return an open sqlite3.Connection.
    """
    # TODO: implement
    raise NotImplementedError


def load_clean_data(connection, tables):
    """Load cleaned relational tables into SQLite.

    Parameters
    ----------
    connection : sqlite3.Connection
    tables : dict[str, pandas.DataFrame]

    Returns
    -------
    dict
        Must contain:
        - tables_loaded
        - rows_loaded

    Notes
    -----
    The returned rows_loaded value may itself be a dictionary keyed by table.
    """
    # TODO: implement
    raise NotImplementedError
