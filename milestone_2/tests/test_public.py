"""Public Milestone 2 interface tests."""

from milestone_2.src.data_loading import load_raw_data, inspect_raw_data
from milestone_2.src.cleaning import clean_data, split_into_tables
from milestone_2.src.database import create_database, load_clean_data
from milestone_2.src.validation import validate_clean_data, validate_database


def test_required_functions_are_callable():
    required = [
        load_raw_data,
        inspect_raw_data,
        clean_data,
        split_into_tables,
        create_database,
        load_clean_data,
        validate_clean_data,
        validate_database,
    ]
    assert all(callable(function) for function in required)
