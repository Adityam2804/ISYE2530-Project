# Milestone 2 — Data Cleaning and Database Formation

## Purpose

Transform the approved raw dataset into a trustworthy relational database.

Milestone 2 introduces the student coding scaffold. You will complete specified TODO functions rather than build the project architecture from scratch.

## Learning goals

By the end of this milestone, you should be able to:

- identify and implement defensible data-cleaning rules
- explain what data was changed, removed, or preserved
- convert source data into a relational representation
- define primary and foreign keys where appropriate
- load cleaned data into SQLite
- validate data quality and database integrity
- write basic required SQL checks

## Required workflow

1. Place the approved source dataset in `data/raw/`.
2. Complete the TODOs in `src/data_loading.py`.
3. Complete the TODOs in `src/cleaning.py`.
4. Define the relational schema in `sql/schema.sql`.
5. Complete database TODOs in `src/database.py`.
6. Complete validation TODOs in `src/validation.py`.
7. Complete `sql/required_queries.sql`.
8. Run the public tests.
9. Generate the required outputs.
10. Complete `cleaning_report.md` and `validation_report.md`.

## Required student deliverables

- completed Python TODO functions
- `schema.sql`
- `required_queries.sql`
- cleaned data output(s)
- `project.db`
- `cleaning_report.md`
- `validation_report.md`

## Fixed function interfaces

Do not rename or remove these functions:

```python
load_raw_data(path)
inspect_raw_data(df)
clean_data(df)
split_into_tables(clean_df)
create_database(db_path, schema_path)
load_clean_data(connection, tables)
validate_clean_data(raw_df, clean_df)
validate_database(connection)
```

You may create additional helper functions.

## Expected return contracts

- `load_raw_data(path)` -> `pandas.DataFrame`
- `inspect_raw_data(df)` -> `dict`
- `clean_data(df)` -> `pandas.DataFrame`
- `split_into_tables(clean_df)` -> `dict[str, pandas.DataFrame]`
- `create_database(...)` -> `sqlite3.Connection`
- `load_clean_data(...)` -> `dict`
- `validate_clean_data(...)` -> `dict`
- `validate_database(...)` -> `dict`

The instructor may adapt small details after reviewing Milestone 1 dataset diversity.
