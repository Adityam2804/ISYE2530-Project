"""Public Milestone 4 interface tests."""

from milestone_4.src.app_helpers import (
    load_project_outputs,
    build_summary_metrics,
    filter_recommendations,
    build_visualization_data,
    build_recommendation_detail,
    evaluate_interface,
)


def test_required_functions_are_callable():
    required = [
        load_project_outputs,
        build_summary_metrics,
        filter_recommendations,
        build_visualization_data,
        build_recommendation_detail,
        evaluate_interface,
    ]

    assert all(
        callable(function)
        for function in required
    )
