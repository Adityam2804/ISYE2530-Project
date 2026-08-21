"""Public Milestone 4 tests.

These tests check common interfaces and configuration structure.
Additional instructor tests may evaluate generated outputs.
"""

from milestone_4.src.app_helpers import (
    load_project_outputs,
    build_summary_metrics,
    filter_recommendations,
    build_visualization_data,
    build_recommendation_detail,
    evaluate_interface,
)

from milestone_4 import project_config


def test_required_helpers_are_callable():
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


def test_project_config_fields_exist():
    required = [
        "PROJECT_TITLE",
        "INTENDED_USER",
        "RECURRING_DECISION",
        "DECISION_OBJECT",
        "VISUALIZATION_SOURCE",
        "VISUALIZATION_TYPE",
        "VISUALIZATION_X",
        "VISUALIZATION_Y",
        "VISUALIZATION_TITLE",
        "LIMITATIONS",
    ]

    assert all(
        hasattr(
            project_config,
            name,
        )
        for name in required
    )
