"""ISE 2530 Milestone 4 Streamlit starter application.

Most page structure is provided. Students complete helper functions in
src/app_helpers.py and customize only the clearly marked project-specific areas.

Run:
    streamlit run app.py
"""

from pathlib import Path

import streamlit as st

from src.app_helpers import (
    load_project_outputs,
    build_summary_metrics,
    filter_recommendations,
    build_visualization_data,
    build_recommendation_detail,
    evaluate_interface,
)


APP_DIR = Path(__file__).resolve().parent

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


st.set_page_config(
    page_title="ISE 2530 Decision Support",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("Decision-Support Dashboard")

# STUDENT TODO:
# Replace the text below with your approved M1 project title,
# intended user, and recurring decision.
st.caption(
    "Replace this caption with a concise description of your project."
)

st.info(
    "This tool supports human decision making. "
    "Recommendations should be reviewed before action."
)


# ============================================================
# LOAD MILESTONE 3 OUTPUTS
# ============================================================

with st.sidebar:
    st.header("Data")

    analysis_dir = Path(
        st.text_input(
            "Milestone 3 analysis directory",
            value=str(DEFAULT_ANALYSIS_DIR),
        )
    )

    decision_dir = Path(
        st.text_input(
            "Milestone 3 decision directory",
            value=str(DEFAULT_DECISION_DIR),
        )
    )


try:
    outputs = load_project_outputs(
        analysis_dir,
        decision_dir,
    )
except Exception as error:
    st.error(f"Unable to load Milestone 3 outputs: {error}")
    st.stop()


# ============================================================
# 1. PROJECT OVERVIEW
# ============================================================

st.header("1. Project overview")

# STUDENT TODO:
# Replace these three lines with your approved M1 information.
st.write("**Intended user:** [replace]")
st.write("**Recurring decision:** [replace]")
st.write("**Decision object:** [replace]")


# ============================================================
# 2. SUMMARY METRICS
# ============================================================

st.header("2. Summary metrics")

try:
    summary_metrics = build_summary_metrics(outputs)
except Exception as error:
    st.error(f"Unable to build summary metrics: {error}")
    st.stop()

metric_items = list(summary_metrics.items())

if not metric_items:
    st.warning("No summary metrics were produced.")
else:
    metric_columns = st.columns(min(4, len(metric_items)))

    for index, (label, value) in enumerate(metric_items[:4]):
        metric_columns[index].metric(
            label,
            value,
        )


# ============================================================
# 3. ANALYSIS VISUALIZATION
# ============================================================

st.header("3. Analysis")

try:
    visualization_data = build_visualization_data(outputs)
except Exception as error:
    st.error(f"Unable to build visualization data: {error}")
    st.stop()

if visualization_data is None or visualization_data.empty:
    st.warning("No visualization data is available.")
else:
    # STUDENT TODO:
    # Choose ONE chart that is meaningful for your project.
    #
    # Examples:
    # st.bar_chart(visualization_data.set_index("group")["value"])
    # st.line_chart(visualization_data.set_index("date")["value"])
    #
    # Replace the generic table below with your selected visualization.
    st.dataframe(
        visualization_data,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# 4. RECOMMENDATION FILTERS
# ============================================================

st.header("4. Recommendations")

recommendations = outputs["recommendations"]

priority_options = sorted(
    recommendations["priority"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
) if "priority" in recommendations.columns else []

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    selected_priorities = st.multiselect(
        "Priority",
        options=priority_options,
        default=priority_options,
    )

    review_only = st.checkbox(
        "Show only recommendations requiring human review"
    )

with filter_col2:
    if (
        "score_or_measure" in recommendations.columns
        and not recommendations.empty
    ):
        max_score = float(
            recommendations["score_or_measure"]
            .fillna(0)
            .max()
        )

        minimum_score = st.number_input(
            "Minimum score",
            min_value=0.0,
            max_value=max(0.0, max_score),
            value=0.0,
        )
    else:
        minimum_score = None


try:
    filtered = filter_recommendations(
        recommendations,
        selected_priorities=selected_priorities,
        review_only=review_only,
        minimum_score=minimum_score,
    )
except Exception as error:
    st.error(f"Unable to filter recommendations: {error}")
    st.stop()


display_columns = [
    column
    for column in [
        "record_id",
        "priority",
        "recommended_action",
        "score_or_measure",
        "requires_review",
    ]
    if column in filtered.columns
]

st.dataframe(
    filtered[display_columns],
    use_container_width=True,
    hide_index=True,
)

st.caption(
    f"{len(filtered):,} recommendation(s) displayed"
)


# ============================================================
# 5. RECOMMENDATION DETAIL
# ============================================================

st.header("5. Recommendation detail")

if filtered.empty:
    st.warning(
        "No recommendation matches the current filters."
    )
else:
    record_options = (
        filtered["record_id"]
        .astype(str)
        .tolist()
    )

    selected_record_id = st.selectbox(
        "Select a record",
        record_options,
    )

    selected_record = filtered[
        filtered["record_id"].astype(str)
        == str(selected_record_id)
    ].iloc[0]

    try:
        detail = build_recommendation_detail(
            selected_record
        )
    except Exception as error:
        st.error(
            f"Unable to build recommendation detail: {error}"
        )
        st.stop()

    left, right = st.columns(2)

    with left:
        st.write(
            f"**Record ID:** "
            f"{detail.get('record_id')}"
        )

        st.write(
            f"**Priority:** "
            f"{detail.get('priority')}"
        )

        st.write(
            f"**Score / measure:** "
            f"{detail.get('score_or_measure')}"
        )

        st.write(
            f"**Requires human review:** "
            f"{detail.get('requires_review')}"
        )

    with right:
        st.write("**Recommended action**")
        st.write(
            detail.get(
                "recommended_action"
            )
        )

    st.write("**Evidence**")
    st.write(
        detail.get(
            "evidence"
        )
    )

    st.write("**Expected benefit**")
    st.write(
        detail.get(
            "expected_benefit"
        )
    )

    st.write("**Limitation**")
    st.write(
        detail.get(
            "limitation"
        )
    )


# ============================================================
# 6. LIMITATIONS / RESPONSIBLE USE
# ============================================================

st.header("6. Limitations and responsible use")

# STUDENT TODO:
# Replace this generic text with 3–5 limitations from your own project.
st.warning(
    """
    - Recommendations are based on the available historical data.
    - Missing or incomplete information may affect interpretation.
    - Ranking is a decision-support aid, not an automatic final decision.
    - A human user should review the supporting evidence before action.
    """
)


# ============================================================
# 7. INTERFACE READINESS CHECK
# ============================================================

st.header("7. Interface readiness")

try:
    interface_evaluation = evaluate_interface(
        outputs
    )
except Exception as error:
    st.error(
        f"Unable to evaluate interface readiness: {error}"
    )
    st.stop()

if interface_evaluation.get(
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
    st.json(interface_evaluation)
