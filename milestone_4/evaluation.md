# Milestone 4 Evaluation and Reflection

<!--
STUDENT DOCUMENT

Keep this concise. The goal is to explain WHY your interface supports the
Milestone 1 recurring decision.
-->

## Intended user

<!--
Copy the intended user from your approved project and briefly explain what this
person needs from the interface.
-->

## Recurring decision

<!--
State the recurring decision the dashboard supports.
-->

## Interface choices

<!--
Complete the table in plain language.
-->

| Interface element | What you chose | Why it helps the intended user |
|---|---|---|
| Summary metrics | Records evaluated, High priority, Require review, Average score | |
| Visualization | | |
| Recommendation filters | Priority / review / minimum score | |
| Recommendation table | | |
| Recommendation detail | | |
| Limitations section | | |

## Visualization

<!--
Answer:
1. Which Milestone 3 output did you visualize?
2. What are the X and Y columns?
3. Why is bar or line appropriate?
4. What should the user notice from the chart?
-->

## Required test cases

### Case 1 — Normal recommendation

<!--
Select a normal recommendation.
What priority/action/evidence appeared?
Did it match the Milestone 3 CSV?
-->

### Case 2 — Record requiring human review

<!--
If your project produces requires_review=True records, test one.

If none exist, explain how you verified that behavior another way.
-->

### Case 3 — Filter with no matching records

<!--
Apply filters that return no records.
Does the interface show an understandable message instead of crashing?
-->

### Case 4 — Recommendation detail

<!--
Select one record and compare the displayed evidence, expected benefit, and
limitation with recommendations.csv.
-->

## Baseline comparison

<!--
Compare your ranking/recommendation method with ONE simple baseline.

Possible baselines:
- alphabetical/random ordering
- ranking by one raw measure only
- no prioritization
- first-come/first-served

Explain in 3–6 sentences why the M3 method is more useful, or where the baseline
performs similarly.
-->

## Limitations

<!--
List the 3–5 limitations visible in project_config.py and explain which one is
most important for the intended user.
-->

## Final reflection

<!--
In 3–5 sentences:
What should the intended user understand before acting on this dashboard?
-->
