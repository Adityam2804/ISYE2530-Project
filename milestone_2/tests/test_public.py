"""Public structural tests for Milestone 2.

These tests check the common project contract. They do not determine whether
your dataset-specific cleaning choices are correct.
"""

import inspect
import sqlite3
import pandas as pd

from milestone_2.src.data_loading import load_raw_data, inspect_raw_data
from milestone_2.src.cleaning import clean_data, split_into_tables
from milestone_2.src.database import create_database, load_clean_data
from milestone_2.src.validation import validate_clean_data, validate_database


def test_required_functions_exist():
    funcs = [
        load_raw_data,
        inspect_raw_data,
        clean_data,
        split_into_tables,
        create_database,
        load_clean_data,
        validate_clean_data,
        validate_database,
    ]
    assert all(callable(f) for f in funcs)


def test_signatures():
    assert list(inspect.signature(load_raw_data).parameters) == ["path"]
    assert list(inspect.signature(inspect_raw_data).parameters) == ["df"]
    assert list(inspect.signature(clean_data).parameters) == ["df"]
    assert list(inspect.signature(split_into_tables).parameters) == ["clean_df"]
    assert list(inspect.signature(create_database).parameters) == ["db_path", "schema_path"]
    assert list(inspect.signature(load_clean_data).parameters) == ["connection", "tables"]
    assert list(inspect.signature(validate_clean_data).parameters) == ["raw_df", "clean_df"]
    assert list(inspect.signature(validate_database).parameters) == ["connection"]


def test_split_contract_example(monkeypatch):
    # This test only demonstrates the required return structure.
    # It does not call student code because TODOs are initially incomplete.
    example = {
        "table_a": pd.DataFrame({"id": [1, 2]}),
        "table_b": pd.DataFrame({"id": [10, 11], "table_a_id": [1, 2]}),
    }
    assert isinstance(example, dict)
    assert len(example) >= 2
    assert all(isinstance(v, pd.DataFrame) for v in example.values())


def test_validation_contract_example():
    example = {
        "raw_rows": 100,
        "clean_rows": 95,
        "rows_removed": 5,
        "remaining_missing": {"column_a": 0},
        "remaining_duplicates": 0,
        "validation_passed": True,
    }
    required = {
        "raw_rows",
        "clean_rows",
        "rows_removed",
        "remaining_missing",
        "remaining_duplicates",
        "validation_passed",
    }
    assert required.issubset(example)
