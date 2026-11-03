# Trigger

**Source ID:** `RKM-C009` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An actual occurrence interpreted as initiating a risk-relevant development in a specified context. A hypothetical trigger description is represented as scenario content, not as an actual Trigger individual.

## Identity and modeling

- OntoUML stereotype: `event`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: An actual happening individuated by supported temporal extent, participants and occurrence boundaries.
- Typing rationale: Event interpretation; a description, plan or possibility is not an event instance.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-005` | incoming `initiatedBy` | [Risk Occurrence](RKM-C004.md) | 0..* → 0..* |

Generalizes: [Risk Occurrence](RKM-C004.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
