"""Milestone 3: ranking and decision-support logic."""

import pandas as pd


REQUIRED_RECOMMENDATION_COLUMNS = [
    "record_id",
    "recommended_action",
    "priority",
    "score_or_measure",
    "evidence",
    "expected_benefit",
    "limitation",
    "requires_review",
]


def rank_candidates(metrics):
    """Rank or prioritize the approved decision objects.

    Parameters
    ----------
    metrics : dict
        Output from calculate_metrics().

    Returns
    -------
    pandas.DataFrame
        One row per decision object.

    Requirements
    ------------
    The returned DataFrame must contain at least:
    - record_id
    - score_or_measure
    - rank

    Your ranking method must:
    - be transparent
    - use measures actually available in the dataset
    - be reproducible
    - be documented in decision_rules.md
    - avoid unsupported predictive/causal claims
    """
    # TODO: implement
    raise NotImplementedError


def generate_recommendations(ranked_candidates, metrics):
    """Generate standardized decision-support recommendation records.

    Parameters
    ----------
    ranked_candidates : pandas.DataFrame
        Output from rank_candidates().

    metrics : dict
        Analysis evidence returned by calculate_metrics().

    Returns
    -------
    pandas.DataFrame
        Must contain EXACTLY these required columns at minimum:

        - record_id
        - recommended_action
        - priority
        - score_or_measure
        - evidence
        - expected_benefit
        - limitation
        - requires_review

    Requirements
    ------------
    - Recommendations must be evidence-based.
    - Rules must be explicit and documented.
    - Do not claim guaranteed outcomes.
    - Records with weak/uncertain evidence should require human review.
    """
    # TODO: implement
    raise NotImplementedError


def validate_recommendations(recommendations):
    """Validate standardized recommendation outputs.

    Returns
    -------
    dict
        Must contain at least:
        - recommendation_count
        - required_columns_present
        - duplicate_record_ids
        - invalid_priorities
        - invalid_requires_review
        - validation_passed
    """
    # TODO: implement
    raise NotImplementedError
