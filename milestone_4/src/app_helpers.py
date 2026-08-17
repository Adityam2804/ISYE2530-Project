"""Milestone 4 helper functions.

Students complete these functions. The Streamlit page shell is provided.
"""

from pathlib import Path
import json

import pandas as pd


def load_project_outputs(analysis_dir, decision_dir):
    """Load standardized Milestone 3 outputs.

    Parameters
    ----------
    analysis_dir : str or pathlib.Path
    decision_dir : str or pathlib.Path

    Returns
    -------
    dict
        Must contain at least:
        - analysis_summary
        - recommendations
        - ranked_candidates

    You may include additional project-specific analysis tables.
    """
    # TODO: implement
    raise NotImplementedError


def build_summary_metrics(outputs):
    """Build 2–4 concise summary metrics for the dashboard.

    Returns
    -------
    dict[str, object]

    Example
    -------
    {
        "Records evaluated": 500,
        "High priority": 42,
        "Require review": 18,
    }

    Requirements
    ------------
    - Metrics must come from Milestone 3 outputs.
    - Do not invent values.
    - Keep metrics understandable to the intended user.
    """
    # TODO: implement
    raise NotImplementedError


def filter_recommendations(
    recommendations,
    selected_priorities=None,
    review_only=False,
    minimum_score=None,
):
    """Filter recommendation records using simple user controls.

    Returns
    -------
    pandas.DataFrame

    Requirements
    ------------
    - Do not mutate the input DataFrame.
    - Support priority filtering when selected_priorities is provided.
    - Support requires_review filtering.
    - Support minimum score filtering when possible.
    """
    # TODO: implement
    raise NotImplementedError


def build_visualization_data(outputs):
    """Return data appropriate for one meaningful visualization.

    Returns
    -------
    pandas.DataFrame

    The returned DataFrame should contain only the fields needed by the selected
    chart.

    The visualization must help explain the approved decision-support problem.
    """
    # TODO: implement
    raise NotImplementedError


def build_recommendation_detail(record):
    """Create structured detail for one recommendation.

    Parameters
    ----------
    record : pandas.Series or dict

    Returns
    -------
    dict
        Must contain at least:
        - record_id
        - recommended_action
        - priority
        - score_or_measure
        - evidence
        - expected_benefit
        - limitation
        - requires_review
    """
    # TODO: implement
    raise NotImplementedError


def evaluate_interface(outputs):
    """Evaluate whether required Milestone 4 content is available.

    Returns
    -------
    dict
        Must contain at least:
        - recommendations_available
        - summary_metrics_available
        - visualization_data_available
        - limitations_visible
        - validation_passed

    This function checks data/interface readiness. It does not measure whether
    the interface is aesthetically attractive.
    """
    # TODO: implement
    raise NotImplementedError
