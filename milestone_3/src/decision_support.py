"""Milestone 3: ranking and decision-support logic.

STUDENT FILE
------------
The instructor provides most mechanics.

You mainly define:
- which entity-level measures contribute to ranking
- whether high or low values are preferable
- weights
- priority thresholds
- short project-appropriate recommendation language

The goal is an EXPLAINABLE rule, not machine learning.
"""

from __future__ import annotations

import math

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


# ============================================================
# INSTRUCTOR-PROVIDED HELPERS
# ============================================================

def _percentile_score(
    series: pd.Series,
    higher_is_better: bool = True,
) -> pd.Series:
    """Convert a numeric measure to a 0-100 percentile score."""
    numeric = pd.to_numeric(series, errors="coerce")

    return (
        numeric.rank(
            method="average",
            pct=True,
            ascending=higher_is_better,
        )
        * 100
    )


def _validate_ranking_components(
    entity_metrics: pd.DataFrame,
    components: list[dict],
) -> None:
    """Validate student ranking configuration."""
    if not components:
        raise ValueError(
            "At least one ranking component is required."
        )

    total_weight = 0.0

    for component in components:
        column = component.get("column")
        weight = component.get("weight")
        higher_is_better = component.get(
            "higher_is_better"
        )

        if not column:
            raise ValueError(
                "Every ranking component needs a column."
            )

        if column not in entity_metrics.columns:
            raise ValueError(
                f"Ranking column '{column}' is not in entity_metrics. "
                f"Available columns: {list(entity_metrics.columns)}"
            )

        if not isinstance(weight, (int, float)) or weight <= 0:
            raise ValueError(
                f"Weight for '{column}' must be positive."
            )

        if not isinstance(higher_is_better, bool):
            raise ValueError(
                f"higher_is_better for '{column}' must be True or False."
            )

        total_weight += float(weight)

    if total_weight <= 0:
        raise ValueError(
            "Ranking component weights must sum to more than zero."
        )


def _priority_from_score(
    score: float,
    high_threshold: float,
    medium_threshold: float,
) -> str:
    """Convert a score to High / Medium / Low."""
    if score >= high_threshold:
        return "High"

    if score >= medium_threshold:
        return "Medium"

    return "Low"


# ============================================================
# STUDENT TASK 3
# ============================================================

def rank_candidates(metrics):
    """Rank/prioritize the approved decision objects.

    Student responsibility
    ----------------------
    Complete only:
    3A. RANKING_COMPONENTS
    3B. REVIEW_FLAG_COLUMN (optional)

    The instructor-provided code will:
    - percentile-scale each component
    - combine weighted components
    - create score_or_measure
    - create rank
    - preserve the original entity metrics

    This avoids requiring you to write scoring infrastructure
    from scratch.
    """

    entity_metrics = metrics.get("entity_metrics")

    if not isinstance(entity_metrics, pd.DataFrame):
        raise TypeError(
            "metrics['entity_metrics'] must be a pandas DataFrame."
        )

    if entity_metrics.empty:
        raise ValueError("entity_metrics is empty.")

    if "record_id" not in entity_metrics.columns:
        raise ValueError(
            "entity_metrics must contain record_id."
        )

    ranked = entity_metrics.copy()

    # --------------------------------------------------------
    # STUDENT TODO 3A — Ranking components
    #
    # Choose 1-4 numeric columns from entity_metrics.
    #
    # weight:
    #   Relative importance. Weights do NOT need to sum to 1.
    #
    # higher_is_better:
    #   True  -> larger value receives a higher priority score
    #   False -> smaller value receives a higher priority score
    #
    # Example SHAPE only:
    #
    # RANKING_COMPONENTS = [
    #     {
    #         "column": "activity_count",
    #         "weight": 2,
    #         "higher_is_better": True,
    #     },
    #     {
    #         "column": "days_since_event",
    #         "weight": 1,
    #         "higher_is_better": False,
    #     },
    # ]
    #
    # Explain your choices in decision_rules.md.
    # --------------------------------------------------------

    RANKING_COMPONENTS = []

    _validate_ranking_components(
        ranked,
        RANKING_COMPONENTS,
    )

    total_weight = sum(
        float(component["weight"])
        for component in RANKING_COMPONENTS
    )

    weighted_score = pd.Series(
        0.0,
        index=ranked.index,
        dtype="float64",
    )

    component_score_columns = []

    for component in RANKING_COMPONENTS:
        column = component["column"]
        weight = float(component["weight"])
        higher_is_better = component[
            "higher_is_better"
        ]

        score_column = f"{column}_score"
        component_score_columns.append(
            score_column
        )

        ranked[score_column] = _percentile_score(
            ranked[column],
            higher_is_better=higher_is_better,
        )

        weighted_score = (
            weighted_score
            + ranked[score_column].fillna(0) * weight
        )

    ranked["score_or_measure"] = (
        weighted_score / total_weight
    ).round(2)

    ranked["rank"] = (
        ranked["score_or_measure"]
        .rank(
            method="dense",
            ascending=False,
        )
        .astype(int)
    )

    # --------------------------------------------------------
    # STUDENT TODO 3B — Optional review flag
    #
    # If entity_metrics contains a Boolean column that marks
    # weak evidence / limited history / uncertain data, put
    # its name here.
    #
    # Example:
    # REVIEW_FLAG_COLUMN = "limited_history_flag"
    #
    # If you do not have one:
    # REVIEW_FLAG_COLUMN = None
    # --------------------------------------------------------

    REVIEW_FLAG_COLUMN = None

    if REVIEW_FLAG_COLUMN is not None:
        if REVIEW_FLAG_COLUMN not in ranked.columns:
            raise ValueError(
                f"Review flag '{REVIEW_FLAG_COLUMN}' "
                "is not in entity_metrics."
            )

        ranked["requires_review"] = (
            ranked[REVIEW_FLAG_COLUMN]
            .fillna(False)
            .astype(bool)
        )
    else:
        ranked["requires_review"] = False

    ranked = (
        ranked
        .sort_values(
            ["rank", "record_id"],
            ascending=[True, True],
        )
        .reset_index(drop=True)
    )

    ranked.attrs["ranking_components"] = (
        RANKING_COMPONENTS
    )
    ranked.attrs["component_score_columns"] = (
        component_score_columns
    )

    return ranked


# ============================================================
# STUDENT TASK 4
# ============================================================

def generate_recommendations(
    ranked_candidates,
    metrics,
):
    """Generate standardized decision-support recommendations.

    Student responsibility
    ----------------------
    Complete:
    4A. two priority thresholds
    4B. short recommendation language
    4C. one general limitation

    The instructor-provided code builds the final standardized
    recommendation table.
    """

    if not isinstance(
        ranked_candidates,
        pd.DataFrame,
    ):
        raise TypeError(
            "ranked_candidates must be a pandas DataFrame."
        )

    if ranked_candidates.empty:
        raise ValueError(
            "ranked_candidates is empty."
        )

    required = {
        "record_id",
        "score_or_measure",
        "rank",
        "requires_review",
    }

    missing = required - set(
        ranked_candidates.columns
    )

    if missing:
        raise ValueError(
            "ranked_candidates is missing: "
            f"{sorted(missing)}"
        )

    # --------------------------------------------------------
    # STUDENT TODO 4A — Priority thresholds
    #
    # Scores are on a 0-100 scale.
    #
    # Example:
    # HIGH_THRESHOLD = 75
    # MEDIUM_THRESHOLD = 50
    #
    # Choose values that you can explain in decision_rules.md.
    # --------------------------------------------------------

    HIGH_THRESHOLD = None
    MEDIUM_THRESHOLD = None

    if HIGH_THRESHOLD is None or MEDIUM_THRESHOLD is None:
        raise NotImplementedError(
            "Set HIGH_THRESHOLD and MEDIUM_THRESHOLD."
        )

    if not (
        0 <= float(MEDIUM_THRESHOLD)
        < float(HIGH_THRESHOLD)
        <= 100
    ):
        raise ValueError(
            "Priority thresholds must satisfy "
            "0 <= MEDIUM < HIGH <= 100."
        )

    # --------------------------------------------------------
    # STUDENT TODO 4B — Recommendation language
    #
    # Keep actions cautious and decision-support oriented.
    #
    # Good:
    # "Prioritize this record for review."
    # "Include this record in routine monitoring."
    #
    # Avoid:
    # "This customer will churn."
    # "This patient has disease X."
    # "This supplier will fail."
    # --------------------------------------------------------

    ACTIONS = {
        "High": "STUDENT TODO: write a high-priority action.",
        "Medium": "STUDENT TODO: write a medium-priority action.",
        "Low": "STUDENT TODO: write a low-priority action.",
        "Review": "Review this record before assigning a priority.",
    }

    if any(
        "STUDENT TODO" in action
        for action in ACTIONS.values()
    ):
        raise NotImplementedError(
            "Complete the High/Medium/Low ACTIONS."
        )

    # --------------------------------------------------------
    # STUDENT TODO 4C — General limitation
    #
    # Write ONE limitation that applies to all recommendations.
    #
    # Example:
    # "The recommendation is based on historical records and
    # does not guarantee future outcomes."
    # --------------------------------------------------------

    GENERAL_LIMITATION = ""

    if not GENERAL_LIMITATION.strip():
        raise NotImplementedError(
            "Set GENERAL_LIMITATION."
        )

    # Instructor-provided recommendation construction.
    records = []

    for _, row in ranked_candidates.iterrows():
        score = float(row["score_or_measure"])
        requires_review = bool(
            row["requires_review"]
        )

        if requires_review:
            priority = "Review"
        else:
            priority = _priority_from_score(
                score,
                high_threshold=float(
                    HIGH_THRESHOLD
                ),
                medium_threshold=float(
                    MEDIUM_THRESHOLD
                ),
            )

        # Generic evidence is intentionally based on visible,
        # reproducible values. Students may enrich this sentence
        # after the minimum implementation works.
        evidence = (
            f"Rank {int(row['rank'])} with a "
            f"combined score of {score:.2f}."
        )

        if requires_review:
            evidence += (
                " Available evidence was flagged "
                "for human review."
            )

        expected_benefit = (
            "Helps the intended user organize limited "
            "review attention using a consistent rule."
        )

        records.append(
            {
                "record_id": str(
                    row["record_id"]
                ),
                "recommended_action": ACTIONS[
                    priority
                ],
                "priority": priority,
                "score_or_measure": round(
                    score,
                    2,
                ),
                "evidence": evidence,
                "expected_benefit": expected_benefit,
                "limitation": GENERAL_LIMITATION,
                "requires_review": requires_review,
            }
        )

    recommendations = pd.DataFrame(
        records,
        columns=REQUIRED_RECOMMENDATION_COLUMNS,
    )

    priority_order = {
        "High": 1,
        "Review": 2,
        "Medium": 3,
        "Low": 4,
    }

    recommendations["_priority_order"] = (
        recommendations["priority"]
        .map(priority_order)
        .fillna(99)
    )

    recommendations = (
        recommendations
        .sort_values(
            [
                "_priority_order",
                "score_or_measure",
                "record_id",
            ],
            ascending=[
                True,
                False,
                True,
            ],
        )
        .drop(
            columns=["_priority_order"]
        )
        .reset_index(drop=True)
    )

    return recommendations


# ============================================================
# INSTRUCTOR-PROVIDED VALIDATION
# Students normally do not modify this function.
# ============================================================

def validate_recommendations(recommendations):
    """Validate standardized recommendation outputs."""

    if not isinstance(
        recommendations,
        pd.DataFrame,
    ):
        raise TypeError(
            "recommendations must be a pandas DataFrame."
        )

    required_columns_present = {
        column: column in recommendations.columns
        for column in REQUIRED_RECOMMENDATION_COLUMNS
    }

    recommendation_count = int(
        len(recommendations)
    )

    duplicate_record_ids = (
        int(
            recommendations[
                "record_id"
            ].duplicated().sum()
        )
        if "record_id" in recommendations.columns
        else None
    )

    allowed_priorities = {
        "High",
        "Medium",
        "Low",
        "Review",
    }

    invalid_priorities = []

    if "priority" in recommendations.columns:
        invalid_priorities = sorted(
            {
                str(value)
                for value in recommendations[
                    "priority"
                ].dropna()
                if str(value) not in allowed_priorities
            }
        )

    invalid_requires_review = 0

    if "requires_review" in recommendations.columns:
        for value in recommendations[
            "requires_review"
        ]:
            if not isinstance(value, bool):
                # numpy.bool_ is also accepted.
                if type(value).__name__ != "bool_":
                    invalid_requires_review += 1

    missing_values = {}

    for column in REQUIRED_RECOMMENDATION_COLUMNS:
        if column in recommendations.columns:
            missing_values[column] = int(
                recommendations[
                    column
                ].isna().sum()
            )
        else:
            missing_values[column] = None

    empty_text_values = {}

    for column in [
        "record_id",
        "recommended_action",
        "priority",
        "evidence",
        "expected_benefit",
        "limitation",
    ]:
        if column in recommendations.columns:
            empty_text_values[column] = int(
                (
                    recommendations[column]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    == ""
                ).sum()
            )
        else:
            empty_text_values[column] = None

    invalid_scores = 0

    if "score_or_measure" in recommendations.columns:
        numeric_scores = pd.to_numeric(
            recommendations[
                "score_or_measure"
            ],
            errors="coerce",
        )

        invalid_scores = int(
            numeric_scores.isna().sum()
        )

    checks = {
        "has_recommendations": (
            recommendation_count > 0
        ),
        "all_required_columns_present": all(
            required_columns_present.values()
        ),
        "unique_record_ids": (
            duplicate_record_ids == 0
            if duplicate_record_ids is not None
            else False
        ),
        "priorities_valid": (
            len(invalid_priorities) == 0
        ),
        "requires_review_valid": (
            invalid_requires_review == 0
        ),
        "scores_numeric": (
            invalid_scores == 0
        ),
        "required_values_present": all(
            value == 0
            for value in missing_values.values()
            if value is not None
        ),
        "required_text_not_empty": all(
            value == 0
            for value in empty_text_values.values()
            if value is not None
        ),
    }

    return {
        "recommendation_count": recommendation_count,
        "required_columns_present": (
            required_columns_present
        ),
        "duplicate_record_ids": (
            duplicate_record_ids
        ),
        "invalid_priorities": invalid_priorities,
        "invalid_requires_review": (
            invalid_requires_review
        ),
        "invalid_scores": invalid_scores,
        "missing_values": missing_values,
        "empty_text_values": empty_text_values,
        "checks": checks,
        "validation_passed": bool(
            all(checks.values())
        ),
    }
