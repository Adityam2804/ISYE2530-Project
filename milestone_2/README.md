# Milestone 2 — Data Cleaning and Relational Database

## Main question

**Can your approved Milestone 1 dataset be transformed into a trustworthy
relational SQLite database?**

Milestone 2 is heavily guided. You are **not** being asked to build a database
pipeline from scratch.

The instructor already provides:

- Excel loading
- raw-data profiling
- duplicate-removal mechanics
- text/date/numeric cleaning helpers
- database creation mechanics
- DataFrame-to-SQLite loading
- generic clean-data validation
- generic database integrity validation
- SQL execution/display
- output saving
- interactive `main.py`

Your responsibility is to make the important **dataset-specific cleaning and
relational-design choices**.

---

## Dataset

Milestone 2 always uses:

```text
milestone_1/dataset.xlsx
```

Do not create a second copy of the dataset for Milestone 2.

---

## What you actually complete

### 1. `src/cleaning.py`

#### `clean_data()`

You fill small configuration sections for:

- required non-missing fields
- text columns
- date columns
- known category replacements
- justified numeric validity rules
- optional small custom rule

The infrastructure that applies those rules is already provided.

#### `split_into_tables()`

This is the main Python task in M2.

You create the relational DataFrames proposed in M1.

You should normally write only a small amount of pandas code for each table,
for example:

```python
customers = (
    clean_df[
        ["CustomerID", "Country"]
    ]
    .dropna(subset=["CustomerID"])
    .drop_duplicates(subset=["CustomerID"])
    .reset_index(drop=True)
)
```

Your table names must match `schema.sql`.

---

### 2. `sql/schema.sql`

Define the relational tables.

You decide:

- table names
- columns
- primary keys
- foreign keys
- appropriate SQLite data types

The Python code that creates the database is already provided.

---

### 3. `sql/required_queries.sql`

Complete five guided SQL checks:

1. table row counts
2. duplicate-ID check
3. meaningful JOIN
4. GROUP BY + aggregate
5. project-specific integrity/data-quality check

The provided `main.py` runs these queries for you.

---

### 4. `cleaning_report.md`

Explain and justify your cleaning decisions.

A rule should not exist only because "the code worked."

---

## What you normally do NOT modify

```text
src/data_loading.py
src/database.py
src/validation.py
main.py
```

These files contain instructor-provided infrastructure.

---

## Workflow

```text
M1 dataset.xlsx
      ↓
load raw data                PROVIDED
      ↓
inspect raw data             PROVIDED
      ↓
clean_data()                 GUIDED STUDENT TASK
      ↓
split_into_tables()          GUIDED STUDENT TASK
      ↓
validate cleaned data        PROVIDED
      ↓
schema.sql                   STUDENT RELATIONAL DESIGN
      ↓
create SQLite database       PROVIDED
      ↓
load relational tables       PROVIDED
      ↓
validate database            PROVIDED
      ↓
required_queries.sql         GUIDED STUDENT SQL
      ↓
project.db + evidence
```

---

## Run Milestone 2

From the project root:

```bash
python milestone_2/main.py
```

or from inside `milestone_2/`:

```bash
python main.py
```

Paths are based on the location of `main.py`.

During execution:

- **Yes** = run/re-run the step
- **No** = skip the step and continue

When possible, existing outputs are reused.

---

## Important principles

### Missing values are not automatically errors

A missing value may be acceptable if the field is not required for your
approved decision.

### Negative numbers are not automatically invalid

A negative value may represent a return, correction, reversal, or another real
event. Check the dataset documentation.

### More tables are not automatically better

Create a small number of meaningful relational tables.

### Do not silently remove large amounts of data

If a cleaning rule removes many rows, explain why in `cleaning_report.md`.

### Table names must agree

These must match:

```text
split_into_tables() dictionary key
             =
CREATE TABLE name in schema.sql
```
