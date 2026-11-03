# Risk Occurrence

**Source ID:** `RKM-C004` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An actual occurrence or change relevant to a risk scenario; a scenario or report alone does not establish that it happened.

## Identity and modeling

- OntoUML stereotype: `event`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: An actual happening individuated by supported temporal extent, participants and occurrence boundaries.
- Typing rationale: Event interpretation; a description, plan or possibility is not an event instance.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-25` | incoming `mayBeRealizedBy` | [Risk Scenario Specification](RKM-C003.md) | 0..* → 0..* |
| `R-69` | incoming `refersToOccurrence` | [Evidence Reference](RKM-C065.md) | 0..* → 0..* |
| `RK2-005` | outgoing `initiatedBy` | [Trigger](RKM-C009.md) | 0..* → 0..* |
| `RK2-006` | outgoing `hasEstablishedConsequence` | [Consequence](RKM-C010.md) | 0..* → 0..* |

Generalizes: none recorded.  
Specialized by: [Trigger](RKM-C009.md).

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
