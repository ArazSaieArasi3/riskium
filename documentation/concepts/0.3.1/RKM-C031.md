# Assessment Activity

**Source ID:** `RKM-C031` · **Subdomain:** [D05 · Risk Assessment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An actual activity contributing to risk identification, analysis or evaluation. It may cover only part of a risk assessment; the complete standardized assessment process is outside the current process-modeling scope.

## Identity and modeling

- OntoUML stereotype: `event`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: An actual happening individuated by supported temporal extent, participants and occurrence boundaries.
- Typing rationale: Event interpretation; a description, plan or possibility is not an event instance.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-26` | outgoing `producesAssessmentInformation` | [Assessment Information](RKM-C032.md) | 0..* → 0..* |
| `R-51` | outgoing `assessmentPerformer` | [Agent](RKM-C047.md) | 0..* → 0..* |
| `R-71` | incoming `refersToAssessmentActivity` | [Evidence Reference](RKM-C065.md) | 0..* → 0..* |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
