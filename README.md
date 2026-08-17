# ISE 2530 Course Project — Student Starter Package

This starter package contains the student-facing materials for:

- **Milestone 1: Problem Definition, Dataset Approval, and Feasibility**
- **Milestone 2: Data Cleaning and Database Formation**

## Project philosophy

You choose the dataset and decision-support context. The course defines the workflow, required deliverables, function interfaces, and output expectations.

You are expected to make and defend the dataset-specific choices. You are **not** expected to design a software project architecture from scratch.

## Folder structure

```text
ISE2530_Student_Project_M1_M2/
├── README.md
├── PROJECT_RULES.md
├── data/
│   ├── raw/
│   └── processed/
├── milestone_1/
│   ├── README.md
│   ├── project_proposal.md
│   ├── dataset_description.md
│   ├── data_dictionary.md
│   ├── decision_definition.md
│   ├── feasibility_preview.md
│   └── ai_use_log.md
└── milestone_2/
    ├── README.md
    ├── cleaning_report.md
    ├── validation_report.md
    ├── src/
    │   ├── __init__.py
    │   ├── data_loading.py
    │   ├── cleaning.py
    │   ├── database.py
    │   └── validation.py
    ├── sql/
    │   ├── schema.sql
    │   └── required_queries.sql
    ├── tests/
    │   └── test_public.py
    └── outputs/
```

## Important rule

Do not change required function names, parameter names, or return types unless the instructor explicitly approves the change.
