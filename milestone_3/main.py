"""ISE 2530 Course Project
Milestone 3 - Interactive Runner

This file is provided by the instructor.

DO NOT MODIFY THIS FILE.
"""

from pathlib import Path
import json
import sqlite3

import pandas as pd

from src.analysis import (
    load_analysis_data,
    calculate_metrics,
    validate_analysis_results,
)
from src.decision_support import (
    rank_candidates,
    generate_recommendations,
    validate_recommendations,
)


DATABASE_PATH = Path("../milestone_2/outputs/project.db")
OUTPUT_DIR = Path("outputs")
ANALYSIS_OUTPUT_DIR = OUTPUT_DIR / "analysis"
DECISION_OUTPUT_DIR = OUTPUT_DIR / "decision"


def ask_to_continue(message):
    while True:
        answer = input(f"\n{message} [y/n]: ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")


def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, default=str)


def save_dataframe(value, path):
    if isinstance(value, pd.DataFrame):
        path.parent.mkdir(parents=True, exist_ok=True)
        value.to_csv(path, index=False)


def main():
    print("=" * 60)
    print("ISE 2530 - MILESTONE 3")
    print("Database Analysis and Decision Support")
    print("=" * 60)

    if not DATABASE_PATH.exists():
        print("\nERROR: Milestone 2 database not found.")
        print(f"Expected: {DATABASE_PATH}")
        return

    ANALYSIS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DECISION_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON;")

    if not ask_to_continue("Step 1: Load analysis data from the database?"):
        connection.close()
        return

    try:
        analysis_data = load_analysis_data(connection)
    except Exception as error:
        connection.close()
        print(f"\nERROR while loading analysis data:\n{error}")
        return

    print("\n[PASS] Analysis data loaded.")

    if not ask_to_continue("Step 2: Calculate project metrics?"):
        connection.close()
        return

    try:
        metrics = calculate_metrics(analysis_data)
    except Exception as error:
        connection.close()
        print(f"\nERROR while calculating metrics:\n{error}")
        return

    save_json(
        {
            key: value
            for key, value in metrics.items()
            if not isinstance(value, pd.DataFrame)
        },
        ANALYSIS_OUTPUT_DIR / "analysis_summary.json",
    )

    for key, value in metrics.items():
        if isinstance(value, pd.DataFrame):
            save_dataframe(value, ANALYSIS_OUTPUT_DIR / f"{key}.csv")

    print(f"\n[PASS] Analysis outputs saved to {ANALYSIS_OUTPUT_DIR}")

    if not ask_to_continue("Step 3: Validate analysis outputs?"):
        connection.close()
        return

    try:
        analysis_validation = validate_analysis_results(metrics)
    except Exception as error:
        connection.close()
        print(f"\nERROR while validating analysis:\n{error}")
        return

    save_json(
        analysis_validation,
        ANALYSIS_OUTPUT_DIR / "analysis_validation.json",
    )

    if not analysis_validation.get("validation_passed", False):
        connection.close()
        print("\nAnalysis validation failed. Correct the analysis before continuing.")
        return

    print("\n[PASS] Analysis validation passed.")

    if not ask_to_continue("Step 4: Rank decision candidates?"):
        connection.close()
        return

    try:
        ranked_candidates = rank_candidates(metrics)
    except Exception as error:
        connection.close()
        print(f"\nERROR while ranking candidates:\n{error}")
        return

    ranked_candidates.to_csv(
        DECISION_OUTPUT_DIR / "ranked_candidates.csv",
        index=False,
    )

    print("\n[PASS] Ranked candidates saved.")

    if not ask_to_continue("Step 5: Generate recommendations?"):
        connection.close()
        return

    try:
        recommendations = generate_recommendations(
            ranked_candidates,
            metrics,
        )
    except Exception as error:
        connection.close()
        print(f"\nERROR while generating recommendations:\n{error}")
        return

    recommendations.to_csv(
        DECISION_OUTPUT_DIR / "recommendations.csv",
        index=False,
    )

    print("\n[PASS] Recommendations saved.")

    if not ask_to_continue("Step 6: Validate recommendations?"):
        connection.close()
        return

    try:
        recommendation_validation = validate_recommendations(
            recommendations
        )
    except Exception as error:
        connection.close()
        print(f"\nERROR while validating recommendations:\n{error}")
        return

    save_json(
        recommendation_validation,
        DECISION_OUTPUT_DIR / "recommendation_validation.json",
    )

    connection.close()

    if not recommendation_validation.get("validation_passed", False):
        print("\nRecommendation validation failed.")
        return

    print("\n" + "=" * 60)
    print("MILESTONE 3 WORKFLOW COMPLETE")
    print("=" * 60)
    print(f"Analysis outputs: {ANALYSIS_OUTPUT_DIR}")
    print(f"Decision outputs: {DECISION_OUTPUT_DIR}")


if __name__ == "__main__":
    main()
