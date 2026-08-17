# Milestone 3 — Database Analysis and Decision Support

## Main question

What does the cleaned relational database reveal, and what decision should the
intended user consider?

Milestone 3 uses the SQLite database created in Milestone 2.

Expected input:

```text
../milestone_2/outputs/project.db
```

Do not rebuild or manually edit the database for this milestone.

## What the instructor provides

- project structure
- function names and signatures
- execution workflow
- required output formats
- required SQL categories
- public tests
- standardized recommendation schema

## What your team completes

1. Analytical SQL appropriate to your approved dataset
2. Project-specific measures
3. A grouped comparison
4. Time-based analysis when appropriate
5. A transparent ranking/prioritization method
6. Evidence-based recommendation logic
7. Validation of the final analysis/recommendation outputs
8. Documentation of assumptions and limitations

## Required recommendation schema

Every recommendation must contain these fields:

| Field | Meaning |
|---|---|
| `record_id` | Identifier of the entity being evaluated |
| `recommended_action` | Suggested decision-support action |
| `priority` | High / Medium / Low or another documented small category set |
| `score_or_measure` | Numeric value supporting the ranking/recommendation |
| `evidence` | Short explanation of the observed evidence |
| `expected_benefit` | Reasonable potential usefulness |
| `limitation` | Important caveat |
| `requires_review` | Boolean indicating whether human review is required |

## Important

This is a decision-support project.

Do not make unsupported claims such as:
- causal conclusions
- medical diagnoses
- guaranteed future outcomes
- optimized decisions
- predictions that were not actually modeled

Prefer language such as:
- prioritize for review
- monitor
- investigate
- compare
- consider
