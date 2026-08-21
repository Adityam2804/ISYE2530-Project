"""ISE 2530 Milestone 4 Streamlit decision-support interface.

INSTRUCTOR-PROVIDED FILE
------------------------
Students normally do NOT modify this file.

Student customization belongs in:

    project_config.py

Run:

    streamlit run milestone_4/app.py

or, from inside milestone_4:

    streamlit run app.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from project_config import (
    PROJECT_TITLE,
    INTENDED_USER,
    RECURRING_DECISION,
    DECISION_OBJECT,
    VISUALIZATION_SOURCE,
    VISUALIZATION_TYPE,
    VISUALIZATION_X,
    VISUALIZATION_Y,
    VISUALIZATION_TITLE,
    LIMITATIONS,
    SCORE_FILTER_LABEL,
)

from src.app_helpers import (
    load_project_outputs,
    build_summary_metrics,
    filter_recommendations,
    build_visualization_data,
    build_recommendation_detail,
    evaluate_interface,
)


APP_DIR = Path(
    __file__
).resolve().parent

DEFAULT_ANALYSIS_DIR = (
    APP_DIR.parent
    / "milestone_3"
    / "outputs"
    / "analysis"
)

DEFAULT_DECISION_DIR = (
    APP_DIR.parent
    / "milestone_3"
    / "outputs"
    / "decision"
)


def _contains_student_todo(
    value,
) -> bool:
    """Return True when required config still contains TODO text."""
    return (
        "STUDENT TODO"
        in str(value)
    )


def validate_student_config():
    """Check required project_config.py values before rendering."""

    required_text = {
        "PROJECT_TITLE":
            PROJECT_TITLE,

        "INTENDED_USER":
            INTENDED_USER,

        "RECURRING_DECISION":
            RECURRING_DECISION,

        "DECISION_OBJECT":
            DECISION_OBJECT,

        "VISUALIZATION_SOURCE":
            VISUALIZATION_SOURCE,

        "VISUALIZATION_TYPE":
            VISUALIZATION_TYPE,

        "VISUALIZATION_X":
            VISUALIZATION_X,

        "VISUALIZATION_Y":
            VISUALIZATION_Y,

        "VISUALIZATION_TITLE":
            VISUALIZATION_TITLE,
    }

    incomplete = [
        name
        for name, value
        in required_text.items()
        if (
            not str(
                value
            ).strip()
            or _contains_student_todo(
                value
            )
        )
    ]

    if incomplete:
        raise ValueError(
            "Complete these values in project_config.py: "
            + ", ".join(
                incomplete
            )
        )

    if VISUALIZATION_TYPE not in {
        "bar",
        "line",
    }:
        raise ValueError(
            "VISUALIZATION_TYPE must be 'bar' or 'line'."
        )


st.set_page_config(
    page_title=(
        PROJECT_TITLE
        if not _contains_student_todo(
            PROJECT_TITLE
        )
        else "ISE 2530 Decision Support"
    ),
    page_icon="📊",
    layout="wide",
)


# ============================================================
# CONFIGURATION CHECK
# ============================================================

try:
    validate_student_config()

except Exception as error:
    st.error(
        f"Project configuration is incomplete: {error}"
    )

    st.info(
        "Open milestone_4/project_config.py "
        "and complete the STUDENT TODO values."
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title(
    PROJECT_TITLE
)

st.caption(
    f"Decision-support interface for {INTENDED_USER}"
)

st.info(
    "This interface supports human decision making. "
    "Recommendations should be reviewed before action."
)


# ============================================================
# LOAD MILESTONE 3 OUTPUTS
# ============================================================

with st.sidebar:
    st.header(
        "Data"
    )

    analysis_dir = Path(
        st.text_input(
            "Milestone 3 analysis directory",
            value=str(
                DEFAULT_ANALYSIS_DIR
            ),
        )
    )

    decision_dir = Path(
        st.text_input(
            "Milestone 3 decision directory",
            value=str(
                DEFAULT_DECISION_DIR
            ),
        )
    )


try:
    outputs = load_project_outputs(
        analysis_dir,
        decision_dir,
    )

except Exception as error:
    st.error(
        f"Unable to load Milestone 3 outputs: {error}"
    )

    st.stop()


# ============================================================
# 1. PROJECT OVERVIEW
# ============================================================

st.header(
    "1. Project overview"
)

st.write(
    f"**Intended user:** "
    f"{INTENDED_USER}"
)

st.write(
    f"**Recurring decision:** "
    f"{RECURRING_DECISION}"
)

st.write(
    f"**Decision object:** "
    f"{DECISION_OBJECT}"
)


# ============================================================
# 2. SUMMARY METRICS
# ============================================================

st.header(
    "2. Summary metrics"
)

try:
    summary_metrics = (
        build_summary_metrics(
            outputs
        )
    )

except Exception as error:
    st.error(
        f"Unable to build summary metrics: {error}"
    )
    st.stop()


metric_items = list(
    summary_metrics.items()
)

metric_columns = st.columns(
    len(
        metric_items
    )
)

for index, (
    label,
    value,
) in enumerate(
    metric_items
):
    metric_columns[
        index
    ].metric(
        label,
        value,
    )


# ============================================================
# 3. ANALYSIS VISUALIZATION
# ============================================================

st.header(
    "3. Analysis"
)

st.subheader(
    VISUALIZATION_TITLE
)

try:
    visualization_data = (
        build_visualization_data(
            outputs,
            VISUALIZATION_SOURCE,
            VISUALIZATION_X,
            VISUALIZATION_Y,
        )
    )

except Exception as error:
    st.error(
        f"Unable to build visualization: {error}"
    )

    st.info(
        "Check the selected source and column names "
        "in project_config.py."
    )

    st.stop()


chart_data = (
    visualization_data
    .set_index(
        VISUALIZATION_X
    )[
        VISUALIZATION_Y
    ]
)


if (
    VISUALIZATION_TYPE
    == "bar"
):
    st.bar_chart(
        chart_data
    )

elif (
    VISUALIZATION_TYPE
    == "line"
):
    st.line_chart(
        chart_data
    )


with st.expander(
    "Show chart data"
):
    st.dataframe(
        visualization_data,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# 4. RECOMMENDATIONS
# ============================================================

st.header(
    "4. Recommendations"
)

recommendations = outputs[
    "recommendations"
]

priority_options = (
    sorted(
        recommendations[
            "priority"
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    if "priority"
    in recommendations.columns
    else []
)


filter_col1, filter_col2 = (
    st.columns(
        2
    )
)


with filter_col1:
    selected_priorities = (
        st.multiselect(
            "Priority",
            options=priority_options,
            default=priority_options,
        )
    )

    review_only = (
        st.checkbox(
            "Show only records requiring human review"
        )
    )


with filter_col2:
    minimum_score = None

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

        max_score = (
            float(
                numeric_scores.max()
            )
            if numeric_scores.notna().any()
            else 0.0
        )

        minimum_score = (
            st.number_input(
                SCORE_FILTER_LABEL,
                min_value=0.0,
                max_value=max(
                    0.0,
                    max_score,
                ),
                value=0.0,
                step=1.0,
            )
        )


filtered = (
    filter_recommendations(
        recommendations,
        selected_priorities=(
            selected_priorities
        ),
        review_only=(
            review_only
        ),
        minimum_score=(
            minimum_score
        ),
    )
)


display_columns = [
    column
    for column in [
        "record_id",
        "priority",
        "recommended_action",
        "score_or_measure",
        "requires_review",
    ]
    if column
    in filtered.columns
]


st.dataframe(
    filtered[
        display_columns
    ],
    use_container_width=True,
    hide_index=True,
)


st.caption(
    f"{len(filtered):,} "
    "recommendation(s) displayed"
)


# ============================================================
# 5. RECOMMENDATION DETAIL
# ============================================================

st.header(
    "5. Recommendation detail"
)


if filtered.empty:
    st.warning(
        "No recommendation matches the current filters."
    )

else:
    record_ids = (
        filtered[
            "record_id"
        ]
        .astype(str)
        .tolist()
    )

    selected_record_id = (
        st.selectbox(
            "Select a record",
            options=record_ids,
        )
    )

    selected_record = (
        filtered[
            filtered[
                "record_id"
            ]
            .astype(str)
            == str(
                selected_record_id
            )
        ]
        .iloc[0]
    )

    detail = (
        build_recommendation_detail(
            selected_record
        )
    )

    left, right = (
        st.columns(
            2
        )
    )

    with left:
        st.write(
            f"**Record ID:** "
            f"{detail['record_id']}"
        )

        st.write(
            f"**Priority:** "
            f"{detail['priority']}"
        )

        st.write(
            f"**Score / measure:** "
            f"{detail['score_or_measure']}"
        )

        st.write(
            f"**Requires human review:** "
            f"{detail['requires_review']}"
        )

    with right:
        st.write(
            "**Recommended action**"
        )

        st.write(
            detail[
                "recommended_action"
            ]
        )

    st.write(
        "**Evidence**"
    )

    st.write(
        detail[
            "evidence"
        ]
    )

    st.write(
        "**Expected benefit**"
    )

    st.write(
        detail[
            "expected_benefit"
        ]
    )

    st.write(
        "**Limitation**"
    )

    st.write(
        detail[
            "limitation"
        ]
    )


# ============================================================
# 6. LIMITATIONS AND RESPONSIBLE USE
# ============================================================

st.header(
    "6. Limitations and responsible use"
)


for limitation in LIMITATIONS:
    st.warning(
        limitation
    )


st.caption(
    "The final decision remains with the intended human user."
)


# ============================================================
# 7. INTERFACE READINESS
# ============================================================

st.header(
    "7. Interface readiness"
)


evaluation = (
    evaluate_interface(
        outputs,
        visualization_data,
        LIMITATIONS,
    )
)


if evaluation.get(
    "validation_passed",
    False,
):
    st.success(
        "Milestone 4 interface data checks passed."
    )

else:
    st.warning(
        "Milestone 4 interface data checks require review."
    )


with st.expander(
    "Show interface evaluation details"
):
    st.json(
        evaluation
    )
