"""Milestone 2: Dataset-specific cleaning.

The instructor provides the interface. Your team defines and justifies
the cleaning rules.
"""

import pandas as pd


def clean_data(df):
    """Return a cleaned copy of the approved dataset.

    Requirements
    ------------
    Your implementation should address, when applicable:
    - missing values
    - duplicate observations
    - invalid or impossible values
    - inconsistent category labels
    - inconsistent data types
    - date/time parsing
    - identifier problems

    Important
    ---------
    Do not silently drop large amounts of data.
    Every important cleaning rule must be described in cleaning_report.md.

    Returns
    -------
    pandas.DataFrame
    """
    # TODO: implement dataset-specific cleaning
    raise NotImplementedError


def split_into_tables(clean_df):
    """Convert cleaned data into the relational tables approved for your project.

    Parameters
    ----------
    clean_df : pandas.DataFrame

    Returns
    -------
    dict[str, pandas.DataFrame]
        Dictionary where each key is a table name and each value is the
        DataFrame to load into that table.

    Example
    -------
    {
        "customers": customers_df,
        "transactions": transactions_df
    }

    Requirements
    ------------
    - Return at least two meaningful tables unless the instructor approved
      an alternative structure.
    - Table names must match schema.sql.
    - Primary/foreign-key fields should be retained where appropriate.
    """
    # TODO: implement
    raise NotImplementedError
