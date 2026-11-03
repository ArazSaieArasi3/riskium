# Risk Evaluation Outcome

**Source ID:** `RKM-X04` · **Subdomain:** [D05 · Risk Assessment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A recorded judgment of risk significance or acceptability based on identified assessment information and criteria versions. It is distinct from a numeric score and from the evaluation activity.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-014` | incoming `basedOnEvaluation` | [Treatment Decision Information](RKM-C041.md) | 0..* → 0..* |
| `RX-011` | outgoing `evaluatesCase` | [Risk Case](RKM-X01.md) | 0..* → 1 |
| `RX-012` | outgoing `usesAssessment` | [Assessment Information](RKM-C032.md) | 0..* → 1..* |
| `RX-013` | outgoing `usesCriteriaVersion` | [Artifact Version](RKM-C015.md) | 0..* → 1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
