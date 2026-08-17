# Feasibility Preview for Milestones 2–4

<!--
PURPOSE

This file helps the instructor decide whether dataset.xlsx and your proposed decision can support the remaining course project.
Answer using what you know NOW. Your design may be refined after instructor feedback.

TABLE INSTRUCTIONS
Keep all table headers and separator rows. Replace blank cells with your content. Add rows by copying the same Markdown row format.
-->

## 1. Likely entities

<!--
List the main real-world entities represented in the data as bullets.
Examples: Customer, Invoice, Product, Shipment, Facility.
Do not list every column as an entity.
-->

## 2. Initial relational structure

<!--
Propose at least TWO meaningful relational tables.
A table should represent an entity or relationship, not merely split columns arbitrarily.
Possible primary key = field that could uniquely identify one row in that table.

Example:
| Proposed table | What it represents | Possible primary key |
|---|---|---|
| customers | One row per known customer | customer_id |
| invoices | One row per invoice | invoice_no |
-->

| Proposed table | What it represents | Possible primary key |
|---|---|---|
|  |  |  |
|  |  |  |

## 3. Expected relationship or join

<!--
Describe at least ONE meaningful relationship between proposed tables.
Use plain language first. If you know the keys, include them.
Example: Each invoice belongs to a customer, so invoices.customer_id can reference customers.customer_id.
-->

## 4. Expected cleaning work

<!--
Identify at least THREE likely data-quality checks/cleaning operations based on actual observations from dataset.xlsx.
Examples:
1. Investigate/remove exact duplicate rows.
2. Decide how missing customer identifiers should be handled.
3. Investigate negative quantities before deciding whether they represent returns.
-->

1.
2.
3.

## 5. Candidate analysis measures

<!--
List at least THREE measures that could later be calculated from the cleaned database.
Examples: number of transactions per customer, total historical value, days since most recent activity.
-->

1.
2.
3.

## 6. Grouped comparison

<!--
Give ONE example comparing meaningful groups.
Examples: average service delay by facility, shipment volume by region, sales activity by country.
Explain what the comparison might help the user understand.
-->

## 7. Time-based analysis

<!--
If a date/time field exists, describe one meaningful trend/measure.
Examples: monthly transaction activity, average delay by month, days since last event.
If no meaningful time field exists, explicitly explain why an alternative analysis should be approved.
-->

## 8. Ranking or prioritization

<!--
Answer BOTH questions:
1. What records/entities could be ranked?
2. What transparent measure or rule could drive that ranking?
This does not need to be your final scoring rule.
-->

What records/entities could be ranked?

What measure or logic might drive the ranking?

## 9. Example final recommendation

<!--
Complete ONE hypothetical example showing what a final recommendation record may look like.
This is only a format preview; do not invent a claim that your data cannot support.

Field guidance:
- record_id: identifier of the entity being reviewed
- recommended_action: human-readable suggested action
- priority: e.g., High / Medium / Low
- score_or_measure: numeric evidence supporting ranking
- evidence: short explanation of the observed data
- expected_benefit: reasonable potential usefulness, not a guaranteed outcome
- limitation: important caveat
- requires_review: True if a human should review before action

Example:
| record_id | C102 |
| recommended_action | Review recent activity |
| priority | High |
| score_or_measure | 8.4 |
| evidence | High transaction frequency and recent activity |
| expected_benefit | Helps manager focus limited review time |
| limitation | Historical activity does not predict future behavior |
| requires_review | True |
-->

| Field | Example |
|---|---|
| record_id | |
| recommended_action | |
| priority | |
| score_or_measure | |
| evidence | |
| expected_benefit | |
| limitation | |
| requires_review | True/False |

## 10. Milestone 4 feasibility

<!--
Describe what would be useful in a simple ONE-PAGE decision-support interface.
Consider 2–4 summary metrics, one visualization, a ranked recommendation table, one useful filter/control, selected-record details, and a limitations/responsible-use note.
Do not design a complex website.
-->

## 11. Team feasibility judgment

<!--
Change exactly ONE checkbox from [ ] to [x].
Then explain your choice in 2–5 sentences.
Example:
- [x] We believe this dataset can support Milestones 2–4
-->

- [ ] We believe this dataset can support Milestones 2–4
- [ ] We are unsure and need instructor feedback
- [ ] We believe the dataset or decision should be changed

Explain:
