# Milestone 4 — Decision-Support Interface and Evaluation

## Main question

**Can the intended user understand and interact with the evidence and
recommendations produced in Milestone 3?**

Milestone 4 is intentionally **heavily scaffolded**.

This is **not** a frontend-programming assignment.

The instructor provides:

- the Streamlit page structure
- loading of Milestone 3 outputs
- summary-metric calculations
- recommendation filtering
- recommendation-detail display
- visualization-data loading
- interface validation
- error handling
- file paths

Students mainly make **design and communication choices**.

---

## What students actually complete

### 1. `project_config.py`

This is the main student code/configuration file.

You fill in:

- project title
- intended user
- recurring decision
- decision object
- chart source
- chart type
- chart X column
- chart Y column
- chart title
- 3–5 project-specific limitations

You do **not** write Streamlit infrastructure.

---

### 2. `evaluation.md`

Explain:

- why the interface elements are useful
- how you tested the interface
- how your recommendation system compares with a simple baseline
- important limitations
- what the intended user should understand before using the tool

---

## What students normally do NOT modify

```text
app.py
src/app_helpers.py
```

These are instructor-provided.

---

## Inputs from Milestone 3

Milestone 4 reads:

```text
milestone_3/
└── outputs/
    ├── analysis/
    │   ├── analysis_summary.json
    │   ├── entity_metrics.csv
    │   ├── grouped_comparison.csv
    │   ├── time_analysis.csv
    │   └── analysis_validation.json
    │
    └── decision/
        ├── ranked_candidates.csv
        ├── recommendations.csv
        └── recommendation_validation.json
```

You should not manually recreate these files in Milestone 4.

---

## Interface requirements

The provided app contains:

1. Project overview
2. Summary metrics
3. One meaningful visualization
4. Recommendation filters
5. Ranked recommendation table
6. Recommendation detail
7. Evidence and limitation display
8. Responsible-use section
9. Interface-readiness check

Your job is to configure these pieces for your project.

---

## Run

From the project root:

```bash
streamlit run milestone_4/app.py
```

or from inside `milestone_4/`:

```bash
streamlit run app.py
```

---

## Visualization guidance

Choose one analysis output created in Milestone 3:

```text
grouped_comparison
time_analysis
entity_metrics
```

### Good chart choices

Use `bar` when comparing categories.

Examples:

- volume by region
- average delay by facility
- records by priority group

Use `line` for an ordered time series.

Examples:

- monthly activity
- weekly service volume
- average delay over time

### Important

The column names in `project_config.py` must exist in the selected
Milestone 3 CSV file.

The app will show available columns if your configuration is incorrect.

---

## Summary metrics

The instructor-provided app automatically displays:

- Records evaluated
- High priority
- Require review
- Average score

You do not need to write code for these metrics.

---

## What is NOT expected

You are not expected to:

- design a complex website
- write HTML/CSS
- create custom JavaScript
- build authentication
- build an API
- deploy a production web service
- build another analysis pipeline

The focus is on **communicating decision-support evidence clearly and
responsibly to an intended user**.
