"""Milestone 2: raw-data loading and inspection.

INSTRUCTOR-PROVIDED FILE
------------------------
Students normally do NOT modify this file.

Why?
Milestone 2 is about cleaning and relational thinking, not about rebuilding
basic file-loading/profiling utilities.

The approved Milestone 1 dataset is always:

    milestone_1/dataset.xlsx
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_raw_data(path):
    """Load the approved raw Excel dataset without cleaning it.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to milestone_1/dataset.xlsx.

    Returns
    -------
    pandas.DataFrame
        Raw dataset exactly as read from the workbook.

    Notes
    -----
    - This function does NOT remove missing values.
    - This function does NOT remove duplicates.
    - This function does NOT change identifiers.
    - Major cleaning belongs in clean_data().
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    if path.suffix.lower() != ".xlsx":
        raise ValueError(
            "Milestone 2 expects the approved dataset "
            "to be named dataset.xlsx."
        )

    try:
        df = pd.read_excel(
            path,
            engine="openpyxl",
        )
    except Exception as error:
        raise RuntimeError(
            f"Unable to read Excel dataset: {path}"
        ) from error

    if df.empty:
        raise ValueError(
            "The approved dataset contains zero rows."
        )

    return df


def inspect_raw_data(df):
    """Summarize important raw-data characteristics.

    Returns
    -------
    dict
        Contains:
        - row_count
        - column_count
        - columns
        - dtypes
        - missing_by_column
        - duplicate_rows

    Students do not need to implement this profiling infrastructure.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "df must be a pandas DataFrame."
        )

    return {
        "row_count":
            int(len(df)),

        "column_count":
            int(len(df.columns)),

        "columns":
            [str(column) for column in df.columns],

        "dtypes": {
            str(column): str(dtype)
            for column, dtype
            in df.dtypes.items()
        },

        "missing_by_column": {
            str(column): int(count)
            for column, count
            in df.isna().sum().items()
        },

        "duplicate_rows":
            int(df.duplicated().sum()),
    }
