# Inspect and use the model

## Risk-nature history

A source reports an **unfavorable** effect on a delivery objective. It later declares two alternative corrections: one **favorable**, one **mixed**. A second source retains its own unfavorable report. Riskium keeps each report, source and recorded context separately. It does not choose which report is true.

| Exact version | Recorded nature and pins | Relationship |
| --- | --- | --- |
| A-v1 | Unfavorable; context-v1, objective-v1 | Original report; two recording revisions |
| A-v2 | Favorable; context-v2, objective-v2 | Explicit correction of A-v1 |
| A-v3 | Mixed; context-v1, objective-v1 | Alternative correction of A-v1 |
| B-v1 | Unfavorable in another local scheme; context-v1, objective-v1 | Independent documentary report; corroboration unassessed |
| A-v4 | Favorable with later term/scheme versions | Later issue without a correction declaration; outside A-v1's correction family |

Retrieving A-v1 keeps its original values after A-v2 or A-v4 exists. The correction family rooted at A-v1 contains **A-v1, A-v2 and A-v3**. An entry's revision chain alone does not establish a correction. These records are an authored synthetic example.

## Missing information and readiness

A record without a mandatory case, nature term or source stays **raw**. It does not acquire an invented case identity or become an issued assertion. An **issued documentary version** is sealed content that passed its declared storage contract. That status does not establish that its report is true.

Context is optional in the native relation. An issued version without context is **NOT_READY_CONTEXT_UNRECORDED** for this retrieval task. A context without objective pins yields **NOT_READY_OBJECTIVES_UNRECORDED**. Both retain their actual missing values. A complete pinned context with explicit objective versions is **READY_FOR_DECLARED_RETRIEVAL**. This is task readiness, not factual correctness, decision approval or a risk score.

Use an exact issued version identifier to ask what it recorded. Use a case query to inspect all issued reports for that case. Use an explicit root version to inspect declared correction branches. [Reproduce](Reproduce.md#risk-nature-example) shows exact IDs and expected answers.

Begin with the [scope](Scope.md), then choose a question: identify a case, interpret an assessment, follow a documentary version or inspect supporting evidence. The [term search](https://arazsaiearasi3.github.io/riskium/current/reference/search.html) leads to definitions and the views that actually contain each term.

## Keep the entities distinct

If case identity has been established, two register entries may document the same RiskCase. A scenario specification describes a possibility; neither that description nor its revision establishes that an occurrence happened. An issued payload stays historical when a correction is recorded.

Similarly, equal reported scores do not authorize comparison across incompatible scales, dimensions, contexts or versions. Check the method and basis before interpreting the values. These are illustrative inspection tasks, not empirical case results. [Modeling decisions](Decisions.md) explains the underlying commitments.

## Choose the appropriate view

| Question | View |
| --- | --- |
| What does a term mean in the conceptual design? | [Conceptual reference](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html) and [selected diagram](https://arazsaiearasi3.github.io/riskium/current/reference/diagrams/index.html) |
| What is asserted in the bounded OWL export? | [WIDOCO reference](https://arazsaiearasi3.github.io/riskium/current/widoco/index-en.html) and [formal-method guide](Formalization.md) |
| Which named terms are connected? | [Text explorer](https://arazsaiearasi3.github.io/riskium/current/explore/index.html) or [WebVOWL](https://arazsaiearasi3.github.io/riskium/current/webvowl/index.html) |
| What database behavior has been implemented? | [Database assurance](Database-Assurance.md) and its exact mapping/schema/query evidence |

The conceptual catalog has 80 concepts, 134 associations/bridges, 66 generalizations and 25 interpretation constraints; the imported anchor is separate. The bounded OWL export contains 77 local named classes, one anchor proxy and 127 object properties. Three optional boundaries and seven bridges are outside that export. [Visualization](Visualization.md) explains the projection limits.

## Before implementing a change

SQLite profiles through lifecycle 0.7.0 implement selected, version-owned slices with explicit unknown/zero, issued-payload and history rules. They are not a complete automatic translation of OWL into relational constraints, a migrated private database, a PostgreSQL implementation or a production-accepted application.

Follow [reproduction](Reproduce.md), declare the task and expected counterexamples, then inspect the affected source and [traceability](Traceability.md). A change in model, profile, schema, query or fixture requires the affected evidence to be checked again before acceptance.
