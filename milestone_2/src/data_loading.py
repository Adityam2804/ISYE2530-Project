"""Milestone 2: Raw-data loading and inspection.

Complete only the TODO sections. You may add helper functions.
"""

from pathlib import Path
import pandas as pd


def load_raw_data(path):
    """Load the approved raw dataset.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the approved source file.

    Returns
    -------
    pandas.DataFrame
        Raw dataset.

    Requirements
    ------------
    - Raise FileNotFoundError when the path does not exist.
    - Support the file type approved for your team.
    - Do not perform major cleaning in this function.
    """
    # TODO: implement
    raise NotImplementedError


def inspect_raw_data(df):
    """Summarize important raw-data characteristics.

    Returns
    -------
    dict
        Must contain at least:
        - row_count
        - column_count
        - columns
        - dtypes
        - missing_by_column
        - duplicate_rows
    """
    # TODO: implement
    raise NotImplementedError
