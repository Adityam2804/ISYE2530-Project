# Milestone 3 Decision Rules

<!--
Document the exact logic used by rank_candidates() and
generate_recommendations().

The instructor should be able to understand your recommendation without reading
your Python source code.
-->

## Decision object

What entity is being ranked or reviewed?

## Measures used

| Measure | Formula / logic | Why it matters |
|---|---|---|
|  |  |  |

## Ranking method

Explain how `score_or_measure` and `rank` are produced.

If you combine multiple measures:
- explain each component
- explain scaling/normalization, if any
- explain weights, if any
- justify why the method is reasonable

## Priority rules

| Priority | Rule | Interpretation |
|---|---|---|
| High |  |  |
| Medium |  |  |
| Low |  |  |

## Human-review rules

Explain when `requires_review = True`.

Examples might include:
- missing evidence
- insufficient history
- conflicting measures
- data-quality concerns

## Recommendation rules

Explain how observed evidence becomes a suggested action.

Use the pattern:

> observation → evidence → suggested action → expected benefit → limitation

## Important limitations

State what the rules cannot determine.
