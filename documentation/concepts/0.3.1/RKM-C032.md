# Assessment Information

**Source ID:** `RKM-C032` · **Subdomain:** [D05 · Risk Assessment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A managed information artifact documenting an assessment and its scope, basis, methods, time context, participants and results. It is distinct from performing that assessment.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-11` | outgoing `assesses` | [Risk Case](RKM-X01.md) | 0..* → 1 |
| `R-12` | outgoing `hasBasis` | [Assessment Basis](RKM-C033.md) | 0..* → 1 |
| `R-13` | outgoing `hasDimensionResult` | [Dimension Assessment Result](RKM-C034.md) | 1 → 0..* |
| `R-17` | outgoing `hasScoreResult` | [Risk Score Result](RKM-C037.md) | 1 → 0..* |
| `R-26` | incoming `producesAssessmentInformation` | [Assessment Activity](RKM-C031.md) | 0..* → 0..* |
| `R-28` | incoming `documentsAssessment` | [Entry Revision](RKM-C023.md) | 1..* → 0..* |
| `R-45` | outgoing `assessmentContext` | [Risk Context Specification](RKM-C002.md) | 0..* → 0..1 |
| `R-46` | outgoing `usesMethod` | [Assessment Method Specification](RKM-C035.md) | 0..* → 0..1 |
| `R-47` | outgoing `epistemicStatus` | [Epistemic Status Term](RKM-C040.md) | 0..* → 0..1 |
| `RK2-013` | outgoing `recordsUncertainty` | [Uncertainty Statement](RKM-X03.md) | 0..* → 0..* |
| `RK2-015` | incoming `recordsRemainingRiskAssessment` | [Treatment Decision Information](RKM-C041.md) | 0..* → 0..* |
| `RX-012` | incoming `usesAssessment` | [Risk Evaluation Outcome](RKM-X04.md) | 0..* → 1..* |
| `RX-014` | outgoing `usesContextVersion` | [Artifact Version](RKM-C015.md) | 0..* → 1 |
| `RX-015` | outgoing `usesMethodVersion` | [Artifact Version](RKM-C015.md) | 0..* → 0..1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
