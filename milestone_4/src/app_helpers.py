"""Milestone 4 helper functions.

INSTRUCTOR-PROVIDED FILE
------------------------
Students normally do NOT modify this file.

This file provides:
- Milestone 3 output loading
- standardized summary metrics
- recommendation filtering
- visualization-data selection
- recommendation-detail formatting
- interface validation
"""

from __future__ import annotations

from pathlib import Path
import json

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


def _read_json(path: Path) -> dict:
    """Read one JSON file."""
    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def _read_csv(path: Path) -> pd.DataFrame:
    """Read one CSV file."""
    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}"
        )

    return pd.read_csv(
        path,
        low_memory=False,
    )


def _normalize_boolean(
    series: pd.Series,
) -> pd.Series:
    """Normalize common CSV Boolean representations."""
    if pd.api.types.is_bool_dtype(
        series
    ):
        return (
            series
            .fillna(False)
            .astype(bool)
        )

    return (
        series
        .astype("string")
        .str.strip()
        .str.lower()
        .isin(
            [
                "true",
                "1",
                "yes",
                "y",
            ]
        )
    )


def load_project_outputs(
    analysis_dir,
    decision_dir,
):
    """Load standardized Milestone 3 outputs.

    Returns
    -------
    dict
        Contains:
        - analysis_summary
        - entity_metrics
        - grouped_comparison
        - time_analysis
        - recommendations
        - ranked_candidates
        - analysis_validation, when available
        - recommendation_validation, when available
    """

    analysis_dir = Path(
        analysis_dir
    )

    decision_dir = Path(
        decision_dir
    )

    outputs = {
        "analysis_summary":
            _read_json(
                analysis_dir
                / "analysis_summary.json"
            ),

        "entity_metrics":
            _read_csv(
                analysis_dir
                / "entity_metrics.csv"
            ),

        "grouped_comparison":
            _read_csv(
                analysis_dir
                / "grouped_comparison.csv"
            ),

        "time_analysis":
            _read_csv(
                analysis_dir
                / "time_analysis.csv"
            ),

        "ranked_candidates":
            _read_csv(
                decision_dir
                / "ranked_candidates.csv"
            ),

        "recommendations":
            _read_csv(
                decision_dir
                / "recommendations.csv"
            ),
    }

    analysis_validation_path = (
        analysis_dir
        / "analysis_validation.json"
    )

    if analysis_validation_path.exists():
        outputs[
            "analysis_validation"
        ] = _read_json(
            analysis_validation_path
        )

    recommendation_validation_path = (
        decision_dir
        / "recommendation_validation.json"
    )

    if (
        recommendation_validation_path
        .exists()
    ):
        outputs[
            "recommendation_validation"
        ] = _read_json(
            recommendation_validation_path
        )

    recommendations = outputs[
        "recommendations"
    ]

    if (
        "requires_review"
        in recommendations.columns
    ):
        recommendations[
            "requires_review"
        ] = _normalize_boolean(
            recommendations[
                "requires_review"
            ]
        )

    return outputs


def build_summary_metrics(
    outputs,
):
    """Build four standardized dashboard metrics.

    Students do not need to implement these calculations.
    """

    recommendations = outputs.get(
        "recommendations"
    )

    if not isinstance(
        recommendations,
        pd.DataFrame,
    ):
        raise TypeError(
            "recommendations output is missing."
        )

    total_records = int(
        len(recommendations)
    )

    high_priority = (
        int(
            (
                recommendations[
                    "priority"
                ]
                .astype(str)
                == "High"
            ).sum()
        )
        if "priority"
        in recommendations.columns
        else 0
    )

    require_review = (
        int(
            recommendations[
                "requires_review"
            ].sum()
        )
        if "requires_review"
        in recommendations.columns
        else 0
    )

    average_score = None

    if (
        "score_or_measure"
        in recommendations.columns
        and not recommendations.empty
    ):
        numeric_scores = pd.to_numeric(
            recommendations[
                "score_or_measure"
            ],
            errors="coerce",
        )

        if numeric_scores.notna().any():
            average_score = round(
                float(
                    numeric_scores.mean()
                ),
                2,
            )

    return {
        "Records evaluated":
            total_records,

        "High priority":
            high_priority,

        "Require review":
            require_review,

        "Average score":
            (
                average_score
                if average_score
                is not None
                else "N/A"
            ),
    }


def filter_recommendations(
    recommendations,
    selected_priorities=None,
    review_only=False,
    minimum_score=None,
):
    """Apply the standard Milestone 4 recommendation filters."""

    if not isinstance(
        recommendations,
        pd.DataFrame,
    ):
        raise TypeError(
            "recommendations must be a pandas DataFrame."
        )

    filtered = (
        recommendations.copy()
    )

    if (
        selected_priorities
        is not None
    ):
        selected_priorities = [
            str(value)
            for value
            in selected_priorities
        ]

        if (
            selected_priorities
            and "priority"
            in filtered.columns
        ):
            filtered = filtered[
                filtered[
                    "priority"
                ]
                .astype(str)
                .isin(
                    selected_priorities
                )
            ]

    if (
        review_only
        and "requires_review"
        in filtered.columns
    ):
        filtered = filtered[
            _normalize_boolean(
                filtered[
                    "requires_review"
                ]
            )
        ]

    if (
        minimum_score
        is not None
        and "score_or_measure"
        in filtered.columns
    ):
        numeric_scores = pd.to_numeric(
            filtered[
                "score_or_measure"
            ],
            errors="coerce",
        )

        filtered = filtered[
            numeric_scores
            >= float(
                minimum_score
            )
        ]

    return (
        filtered
        .reset_index(
            drop=True
        )
    )


def build_visualization_data(
    outputs,
    source_name,
    x_column,
    y_column,
):
    """Select two columns from one M3 analysis output.

    Parameters are supplied through project_config.py.
    """

    allowed_sources = {
        "grouped_comparison",
        "time_analysis",
        "entity_metrics",
    }

    if source_name not in (
        allowed_sources
    ):
        raise ValueError(
            "VISUALIZATION_SOURCE must be one of: "
            + ", ".join(
                sorted(
                    allowed_sources
                )
            )
        )

    dataframe = outputs.get(
        source_name
    )

    if not isinstance(
        dataframe,
        pd.DataFrame,
    ):
        raise TypeError(
            f"{source_name} is unavailable."
        )

    missing = [
        column
        for column in [
            x_column,
            y_column,
        ]
        if column
        not in dataframe.columns
    ]

    if missing:
        raise ValueError(
            f"Visualization column(s) not found: {missing}. "
            f"Available columns in {source_name}: "
            f"{list(dataframe.columns)}"
        )

    result = dataframe[
        [
            x_column,
            y_column,
        ]
    ].copy()

    result[
        y_column
    ] = pd.to_numeric(
        result[
            y_column
        ],
        errors="coerce",
    )

    result = result.dropna(
        subset=[
            x_column,
            y_column,
        ]
    )

    if result.empty:
        raise ValueError(
            "Visualization data contains no usable rows."
        )

    return result


def build_recommendation_detail(
    record,
):
    """Return standardized fields for one recommendation."""

    if isinstance(
        record,
        pd.Series,
    ):
        record = record.to_dict()

    if not isinstance(
        record,
        dict,
    ):
        raise TypeError(
            "record must be a pandas Series or dictionary."
        )

    detail = {
        column: record.get(
            column
        )
        for column
        in REQUIRED_RECOMMENDATION_COLUMNS
    }

    missing = [
        column
        for column, value
        in detail.items()
        if value is None
    ]

    if missing:
        raise ValueError(
            "Recommendation is missing required fields: "
            f"{missing}"
        )

    return detail


def evaluate_interface(
    outputs,
    visualization_data,
    limitations,
):
    """Evaluate whether required M4 content is available."""

    recommendations = outputs.get(
        "recommendations"
    )

    summary_metrics = (
        build_summary_metrics(
            outputs
        )
    )

    recommendations_available = (
        isinstance(
            recommendations,
            pd.DataFrame,
        )
        and not recommendations.empty
    )

    recommendation_columns_present = (
        recommendations_available
        and all(
            column
            in recommendations.columns
            for column
            in REQUIRED_RECOMMENDATION_COLUMNS
        )
    )

    summary_metrics_available = (
        isinstance(
            summary_metrics,
            dict,
        )
        and len(
            summary_metrics
        ) >= 2
    )

    visualization_data_available = (
        isinstance(
            visualization_data,
            pd.DataFrame,
        )
        and not visualization_data.empty
    )

    limitations_visible = (
        isinstance(
            limitations,
            list,
        )
        and len(
            [
                value
                for value
                in limitations
                if str(value).strip()
                and "STUDENT TODO"
                not in str(value)
            ]
        ) >= 3
    )

    checks = {
        "recommendations_available":
            recommendations_available,

        "recommendation_columns_present":
            recommendation_columns_present,

        "summary_metrics_available":
            summary_metrics_available,

        "visualization_data_available":
            visualization_data_available,

        "limitations_visible":
            limitations_visible,
    }

    return {
        **checks,
        "validation_passed":
            bool(
                all(
                    checks.values()
                )
            ),
    }
