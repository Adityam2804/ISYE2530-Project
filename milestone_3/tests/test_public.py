"""Public Milestone 3 tests.

These tests check the common interface only.
Instructor tests may perform additional checks.
"""

from milestone_3.src.analysis import (
    load_analysis_data,
    calculate_metrics,
    validate_analysis_results,
)
from milestone_3.src.decision_support import (
    rank_candidates,
    generate_recommendations,
    validate_recommendations,
)
from milestone_3.src.sql_runner import (
    run_analysis_queries,
    display_sql_results,
)


def test_required_functions_are_callable():
    required = [
        load_analysis_data,
        calculate_metrics,
        validate_analysis_results,
        rank_candidates,
        generate_recommendations,
        validate_recommendations,
        run_analysis_queries,
        display_sql_results,
    ]

    assert all(
        callable(function)
        for function in required
    )
