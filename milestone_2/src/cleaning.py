"""Milestone 2: dataset-specific cleaning."""

import pandas as pd


def clean_data(df):
    """Return a cleaned copy of the approved dataset.

    Address when applicable: missing values, duplicates, invalid values,
    inconsistent labels/types, dates, and identifiers.
    Do not silently drop large amounts of data. Document important rules in
    cleaning_report.md.
    """
    # TODO: implement dataset-specific cleaning
    raise NotImplementedError


def split_into_tables(clean_df):
    """Return dict[str, pandas.DataFrame] for relational tables.

    Requirements:
    - At least two meaningful tables unless approved otherwise.
    - Names must match schema.sql.
    - Retain appropriate primary/foreign-key fields.
    """
    # TODO: implement
    raise NotImplementedError
