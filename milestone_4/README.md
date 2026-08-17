# Milestone 4 — Streamlit Decision-Support Interface and Evaluation

## Main question

Can the intended user understand and interact with the evidence and
recommendations produced in Milestone 3?

This milestone is intentionally heavily scaffolded. It is NOT a frontend
engineering assignment.

## Inputs

The app should use the standardized outputs from Milestone 3:

```text
../milestone_3/outputs/analysis/
../milestone_3/outputs/decision/
```

At minimum, Milestone 3 should have produced:

```text
ranked_candidates.csv
recommendations.csv
analysis_validation.json
recommendation_validation.json
```

plus the project-specific analysis tables produced by `calculate_metrics()`.

## Required interface

Your one-page Streamlit interface should contain:

1. Project / decision overview
2. 2–4 useful summary metrics
3. At least one meaningful visualization
4. Ranked recommendations table
5. At least one useful filter or scenario control
6. Selected recommendation detail
7. Evidence and limitation display
8. Responsible-use statement

## Student work

Complete the TODO functions in `src/app_helpers.py`.

Most Streamlit page structure is already provided in `app.py`.

## Run

From the `milestone_4` directory:

```bash
streamlit run app.py
```
