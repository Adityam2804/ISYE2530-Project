"""Public Milestone 3 interface tests."""

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


def test_required_functions_are_callable():
    required = [
        load_analysis_data,
        calculate_metrics,
        validate_analysis_results,
        rank_candidates,
        generate_recommendations,
        validate_recommendations,
    ]
    assert all(callable(function) for function in required)
