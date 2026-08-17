# Decision Definition

<!--
PURPOSE

Define the decision-support use case before coding begins.
The final system should support human decision making using evidence from the dataset. It should NOT claim to predict, optimize, diagnose, or prove causation unless the course explicitly requires and supports that method.

Keep every heading below.
-->

## Intended user

<!--
Identify the main user ROLE and explain in 1–3 sentences why that person would use the output.
Example: A customer/account manager who periodically reviews historical customer activity and decides which accounts deserve attention.
-->

## Decision statement

<!--
Write ONE clear sentence describing the recurring decision.
A useful pattern is:
"The [user] needs to decide which [decision objects] should be [reviewed/prioritized/compared] based on [available evidence]."
Avoid vague statements such as "make better decisions."
-->

## Decision object

<!--
Name the entity being evaluated, compared, ranked, prioritized, or reviewed.
Examples: customer, patient, supplier, shipment, product, facility, region, request, case.
Then explain how that entity appears in the dataset.
-->

## Evidence available in the dataset

<!--
List the actual columns/variables that can inform the decision and briefly explain how each could be useful.
A bullet list is recommended.
Example:
- InvoiceDate — supports recency/time analysis
- Quantity — measures purchase volume
- CustomerID — groups activity by customer
-->

## Candidate measures

<!--
Identify at least THREE measures.
"How it could be calculated" should describe the formula/logic in plain language. You do not need to write Python yet.

Example:
| Measure | How it could be calculated | Why it may matter |
|---|---|---|
| Purchase frequency | Count distinct invoices per customer | Distinguishes frequent from infrequent customers |

Add more rows if needed.
-->

| Measure | How it could be calculated | Why it may matter |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |

## Possible ranking or prioritization target

<!--
State:
1. WHAT entity could be ranked
2. WHAT evidence/measure might determine ordering
3. WHY that ranking would help the intended user
This is a proposal. The exact ranking method can be refined later.
-->

## Possible recommendation

<!--
Give one example of a recommendation the final system might produce.
Use careful language such as "Prioritize this record for review", "Monitor this item", or "Investigate this exception".
Avoid unsupported predictive/causal claims.
-->

## What the dataset cannot support

<!--
Identify important decisions/conclusions that would be inappropriate because required information is absent.
Every real dataset has limits.
Example: Historical transaction data alone cannot establish customer satisfaction or prove that outreach will increase future purchases.
-->

## Human review

<!--
Explain what should remain a human judgment even after the system generates a ranking/recommendation.
The final system is a decision-support tool, not an automatic decision maker.
-->
