"""ISE 2530 Course Project
Milestone 3 - Interactive Runner

INSTRUCTOR-PROVIDED FILE.
Students should not modify this file.

Behavior:
- Yes -> run/re-run the step
- No  -> skip the step and continue
- Existing outputs are reused when possible
"""

from __future__ import annotations

from pathlib import Path
import json
import sqlite3

import pandas as pd

from src.analysis import (
    describe_database_schema,
    load_analysis_data,
    calculate_metrics,
    validate_analysis_results,
)
from src.decision_support import (
    rank_candidates,
    generate_recommendations,
    validate_recommendations,
)
from src.sql_runner import (
    run_analysis_queries,
    display_sql_results,
)


BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = (
    BASE_DIR.parent
    / "milestone_2"
    / "outputs"
    / "project.db"
)

OUTPUT_DIR = BASE_DIR / "outputs"
ANALYSIS_OUTPUT_DIR = OUTPUT_DIR / "analysis"
DECISION_OUTPUT_DIR = OUTPUT_DIR / "decision"

ANALYSIS_QUERIES_PATH = (
    BASE_DIR
    / "sql"
    / "analysis_queries.sql"
)

SQL_RESULTS_PATH = (
    OUTPUT_DIR
    / "sql_results.json"
)

ENTITY_METRICS_PATH = (
    ANALYSIS_OUTPUT_DIR
    / "entity_metrics.csv"
)

GROUPED_COMPARISON_PATH = (
    ANALYSIS_OUTPUT_DIR
    / "grouped_comparison.csv"
)

TIME_ANALYSIS_PATH = (
    ANALYSIS_OUTPUT_DIR
    / "time_analysis.csv"
)

ANALYSIS_SUMMARY_PATH = (
    ANALYSIS_OUTPUT_DIR
    / "analysis_summary.json"
)

ANALYSIS_VALIDATION_PATH = (
    ANALYSIS_OUTPUT_DIR
    / "analysis_validation.json"
)

RANKED_CANDIDATES_PATH = (
    DECISION_OUTPUT_DIR
    / "ranked_candidates.csv"
)

RECOMMENDATIONS_PATH = (
    DECISION_OUTPUT_DIR
    / "recommendations.csv"
)

RECOMMENDATION_VALIDATION_PATH = (
    DECISION_OUTPUT_DIR
    / "recommendation_validation.json"
)


def ask_to_continue(message):
    """Ask yes/no. No means skip, not exit."""
    while True:
        answer = input(
            f"\n{message} [y/n]: "
        ).strip().lower()

        if answer in {"y", "yes"}:
            return True

        if answer in {"n", "no"}:
            return False

        print("Please enter 'y' or 'n'.")


def save_json(data, path):
    """Write JSON using string conversion for uncommon objects."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            default=str,
        )


def save_metric_outputs(metrics):
    """Save standardized metric outputs."""
    ANALYSIS_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary = {}

    for key, value in metrics.items():
        if isinstance(value, pd.DataFrame):
            value.to_csv(
                ANALYSIS_OUTPUT_DIR
                / f"{key}.csv",
                index=False,
            )
        else:
            summary[key] = value

    save_json(
        summary,
        ANALYSIS_SUMMARY_PATH,
    )


def load_existing_metrics():
    """Reload standardized metric outputs when available."""
    required = [
        ENTITY_METRICS_PATH,
        GROUPED_COMPARISON_PATH,
        TIME_ANALYSIS_PATH,
        ANALYSIS_SUMMARY_PATH,
    ]

    if not all(
        path.exists()
        for path in required
    ):
        return None

    entity_metrics = pd.read_csv(
        ENTITY_METRICS_PATH
    )
    grouped_comparison = pd.read_csv(
        GROUPED_COMPARISON_PATH
    )
    time_analysis = pd.read_csv(
        TIME_ANALYSIS_PATH
    )

    summary = json.loads(
        ANALYSIS_SUMMARY_PATH.read_text(
            encoding="utf-8"
        )
    )

    return {
        **summary,
        "entity_metrics": entity_metrics,
        "grouped_comparison": (
            grouped_comparison
        ),
        "time_analysis": time_analysis,
    }


def main():
    print("=" * 60)
    print("ISE 2530 - MILESTONE 3")
    print("Database Analysis and Decision Support")
    print("=" * 60)

    print(
        f"\nDatabase:"
        f"\n  {DATABASE_PATH}"
    )

    if not DATABASE_PATH.exists():
        print(
            "\nERROR: Milestone 2 database "
            "was not found."
        )
        return

    ANALYSIS_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )
    DECISION_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.execute(
        "PRAGMA foreign_keys = ON;"
    )

    analysis_data = None
    metrics = None
    ranked_candidates = None
    recommendations = None

    # =====================================================
    # STEP 0 - SHOW DATABASE SCHEMA
    # =====================================================

    print("\n" + "=" * 60)
    print("MILESTONE 2 DATABASE SCHEMA")
    print("=" * 60)

    schema = describe_database_schema(
        connection
    )

    for table_name, columns in schema.items():
        print(
            f"\nTABLE: {table_name}"
        )

        for column in columns:
            print(
                f"  - {column}"
            )

    # =====================================================
    # STEP 1 - LOAD ANALYSIS DATA
    # =====================================================

    if ask_to_continue(
        "Step 1: Load analysis data from the database?"
    ):
        try:
            analysis_data = load_analysis_data(
                connection
            )

            print(
                "\n[PASS] Analysis data loaded."
            )

            for name, dataframe in (
                analysis_data.items()
            ):
                if isinstance(
                    dataframe,
                    pd.DataFrame,
                ):
                    print(
                        f"  {name}: "
                        f"{len(dataframe):,} rows, "
                        f"{len(dataframe.columns)} columns"
                    )

        except Exception as error:
            print(
                "\n[FAIL] Step 1 - "
                "Load analysis data"
            )
            print(error)

    else:
        print(
            "\n[SKIPPED] Step 1 - "
            "Load analysis data"
        )

    # =====================================================
    # STEP 2 - CALCULATE METRICS
    # =====================================================

    if ask_to_continue(
        "Step 2: Calculate project metrics?"
    ):
        if analysis_data is None:
            try:
                analysis_data = (
                    load_analysis_data(
                        connection
                    )
                )
            except Exception as error:
                print(
                    "\n[FAIL] Step 2 - "
                    "Analysis data is unavailable."
                )
                print(error)

        if analysis_data is not None:
            try:
                metrics = calculate_metrics(
                    analysis_data
                )

                save_metric_outputs(
                    metrics
                )

                print(
                    "\n[PASS] Analysis outputs saved:"
                )
                print(
                    f"  {ANALYSIS_OUTPUT_DIR}"
                )

            except Exception as error:
                print(
                    "\n[FAIL] Step 2 - "
                    "Calculate metrics"
                )
                print(error)

    else:
        print(
            "\n[SKIPPED] Step 2 - "
            "Calculate project metrics"
        )

        metrics = load_existing_metrics()

        if metrics is not None:
            print(
                "[INFO] Existing analysis outputs "
                "will be reused."
            )

    # =====================================================
    # STEP 3 - VALIDATE ANALYSIS
    # =====================================================

    if ask_to_continue(
        "Step 3: Validate analysis outputs?"
    ):
        if metrics is None:
            metrics = load_existing_metrics()

        if metrics is None:
            print(
                "\n[SKIPPED] Step 3 - "
                "No analysis outputs are available."
            )
        else:
            try:
                validation = (
                    validate_analysis_results(
                        metrics
                    )
                )

                save_json(
                    validation,
                    ANALYSIS_VALIDATION_PATH,
                )

                print(
                    "\n[PASS] Analysis validation "
                    "completed."
                )
                print(
                    "  validation_passed: "
                    f"{validation.get('validation_passed')}"
                )

            except Exception as error:
                print(
                    "\n[FAIL] Step 3 - "
                    "Validate analysis"
                )
                print(error)

    else:
        print(
            "\n[SKIPPED] Step 3 - "
            "Validate analysis"
        )

    # =====================================================
    # STEP 4 - RUN ANALYTICAL SQL
    # =====================================================

    if ask_to_continue(
        "Step 4: Run required analytical SQL?"
    ):
        try:
            sql_results = run_analysis_queries(
                connection,
                ANALYSIS_QUERIES_PATH,
            )

            display_sql_results(
                sql_results
            )

            save_json(
                sql_results,
                SQL_RESULTS_PATH,
            )

            print(
                f"\n[PASS] SQL results saved:"
                f"\n  {SQL_RESULTS_PATH}"
            )

        except Exception as error:
            print(
                "\n[FAIL] Step 4 - "
                "Run analytical SQL"
            )
            print(error)

    else:
        print(
            "\n[SKIPPED] Step 4 - "
            "Run analytical SQL"
        )

    # =====================================================
    # STEP 5 - RANK CANDIDATES
    # =====================================================

    if ask_to_continue(
        "Step 5: Rank decision candidates?"
    ):
        if metrics is None:
            metrics = load_existing_metrics()

        if metrics is None:
            print(
                "\n[SKIPPED] Step 5 - "
                "No metric outputs are available."
            )
        else:
            try:
                ranked_candidates = (
                    rank_candidates(
                        metrics
                    )
                )

                ranked_candidates.to_csv(
                    RANKED_CANDIDATES_PATH,
                    index=False,
                )

                print(
                    "\n[PASS] Ranked candidates saved:"
                )
                print(
                    f"  {RANKED_CANDIDATES_PATH}"
                )

            except Exception as error:
                print(
                    "\n[FAIL] Step 5 - "
                    "Rank candidates"
                )
                print(error)

    else:
        print(
            "\n[SKIPPED] Step 5 - "
            "Rank candidates"
        )

        if RANKED_CANDIDATES_PATH.exists():
            ranked_candidates = pd.read_csv(
                RANKED_CANDIDATES_PATH
            )

            print(
                "[INFO] Existing ranked candidates "
                "will be reused."
            )

    # =====================================================
    # STEP 6 - GENERATE RECOMMENDATIONS
    # =====================================================

    if ask_to_continue(
        "Step 6: Generate recommendations?"
    ):
        if ranked_candidates is None:
            if RANKED_CANDIDATES_PATH.exists():
                ranked_candidates = pd.read_csv(
                    RANKED_CANDIDATES_PATH
                )

        if metrics is None:
            metrics = load_existing_metrics()

        if (
            ranked_candidates is None
            or metrics is None
        ):
            print(
                "\n[SKIPPED] Step 6 - "
                "Required ranking/metrics are unavailable."
            )
        else:
            try:
                recommendations = (
                    generate_recommendations(
                        ranked_candidates,
                        metrics,
                    )
                )

                recommendations.to_csv(
                    RECOMMENDATIONS_PATH,
                    index=False,
                )

                print(
                    "\n[PASS] Recommendations saved:"
                )
                print(
                    f"  {RECOMMENDATIONS_PATH}"
                )

            except Exception as error:
                print(
                    "\n[FAIL] Step 6 - "
                    "Generate recommendations"
                )
                print(error)

    else:
        print(
            "\n[SKIPPED] Step 6 - "
            "Generate recommendations"
        )

        if RECOMMENDATIONS_PATH.exists():
            recommendations = pd.read_csv(
                RECOMMENDATIONS_PATH
            )

            print(
                "[INFO] Existing recommendations "
                "will be reused."
            )

    # =====================================================
    # STEP 7 - VALIDATE RECOMMENDATIONS
    # =====================================================

    if ask_to_continue(
        "Step 7: Validate recommendations?"
    ):
        if recommendations is None:
            if RECOMMENDATIONS_PATH.exists():
                recommendations = pd.read_csv(
                    RECOMMENDATIONS_PATH
                )

        if recommendations is None:
            print(
                "\n[SKIPPED] Step 7 - "
                "No recommendation output is available."
            )
        else:
            try:
                recommendation_validation = (
                    validate_recommendations(
                        recommendations
                    )
                )

                save_json(
                    recommendation_validation,
                    RECOMMENDATION_VALIDATION_PATH,
                )

                print(
                    "\n[PASS] Recommendation "
                    "validation completed."
                )
                print(
                    "  validation_passed: "
                    f"{recommendation_validation.get('validation_passed')}"
                )

            except Exception as error:
                print(
                    "\n[FAIL] Step 7 - "
                    "Validate recommendations"
                )
                print(error)

    else:
        print(
            "\n[SKIPPED] Step 7 - "
            "Validate recommendations"
        )

    connection.close()

    print("\n" + "=" * 60)
    print("MILESTONE 3 WORKFLOW FINISHED")
    print("=" * 60)
    print(
        "\nAll Milestone 3 tasks have been offered."
    )
    print(
        f"\nOutputs:"
        f"\n  {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()
