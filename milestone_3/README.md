# Milestone 3 — Database Analysis and Decision Support

## Main question

**What does your Milestone 2 database reveal, and how can that evidence support
the recurring decision approved in Milestone 1?**

Milestone 3 is intentionally guided. You are **not** being asked to build an
analysis system from scratch.

The instructor already provides:

- database connection code
- schema inspection code
- file paths
- output saving
- error handling
- validation functions
- percentile/ranking mechanics
- recommendation output structure
- SQL execution code
- public interface tests

Your job is to make the **dataset-specific analytical choices**.

---

## What you actually need to complete

### `src/analysis.py`

You complete small sections inside two functions.

#### `load_analysis_data()`

You provide:

1. one SQL query using your M2 tables
2. any date columns that should be converted

You do **not** write database-connection or query-execution infrastructure.

#### `calculate_metrics()`

You provide:

1. the decision-object identifier column
2. at least three entity-level measures
3. one grouped comparison
4. one time-based analysis or approved alternative
5. a decision indicator
6. a risk/exception indicator

The required output structure is already provided.

---

### `src/decision_support.py`

#### `rank_candidates()`

You provide only the ranking configuration:

- which measures contribute to the score
- relative weights
- whether higher or lower is preferable
- optional review/uncertainty flag

The provided code converts the measures to comparable percentile scores and
calculates the final ranking.

#### `generate_recommendations()`

You provide:

- High threshold
- Medium threshold
- short High/Medium/Low actions
- one general limitation

The standardized recommendation record is created for you.

---

### `sql/analysis_queries.sql`

Complete five guided analytical queries:

1. decision-object summary
2. grouped comparison
3. time analysis
4. meaningful JOIN
5. decision-relevant evidence

The provided `src/sql_runner.py` executes and displays them.

---

## Workflow

```text
Milestone 2 project.db
        ↓
inspect database schema
        ↓
load_analysis_data()
        ↓
calculate_metrics()
        ↓
validate_analysis_results()
        ↓
run Q1-Q5 analytical SQL
        ↓
rank_candidates()
        ↓
generate_recommendations()
        ↓
validate_recommendations()
```

Run:

```bash
python milestone_3/main.py
```

or from inside `milestone_3/`:

```bash
python main.py
```

Paths are based on the location of `main.py`, so either approach is supported.

---

## Important design rule

Your database tables will **not** necessarily have the same names as another
team's tables.

For example, one project might contain:

```text
patients
visits
facilities
```

while another might contain:

```text
orders
shipments
suppliers
```

Use the schema created by **your team in Milestone 2**.

Do not copy table/column names from an example project unless those names
actually exist in your database.

---

## Recommendation output contract

Every recommendation contains:

| Field | Meaning |
|---|---|
| `record_id` | entity being evaluated |
| `recommended_action` | suggested decision-support action |
| `priority` | High / Medium / Low / Review |
| `score_or_measure` | numeric prioritization evidence |
| `evidence` | why the record received this result |
| `expected_benefit` | potential usefulness |
| `limitation` | important caveat |
| `requires_review` | whether a human should review it |

---

## What is NOT expected

You are not expected to:

- build machine-learning models
- forecast future outcomes
- optimize an operational policy
- write database infrastructure
- design a scoring framework from scratch
- create a web application in M3

The emphasis is on **SQL, descriptive analysis, interpretation, transparent
ranking, and responsible decision support**.
