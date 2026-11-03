# Risk Context Specification

**Source ID:** `RKM-C002` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A versioned information specification of analysis boundaries, circumstances, time horizon and objective references under which risk statements and results are interpreted.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-35` | incoming `analyzedInContext` | [Risk Case](RKM-X01.md) | 0..* → 0..* |
| `R-43` | incoming `natureInContext` | [Risk Nature Assertion](RKM-C005.md) | 0..* → 0..1 |
| `R-45` | incoming `assessmentContext` | [Assessment Information](RKM-C032.md) | 0..* → 0..1 |
| `RK2-001` | outgoing `refersToCondition` | [Predisposing Condition](RKM-C008.md) | 0..* → 0..* |
| `RK2-002` | outgoing `refersToVulnerability` | [Vulnerability](RKM-C011.md) | 0..* → 0..* |
| `RK2-003` | outgoing `refersToExposure` | [Exposure](RKM-C012.md) | 0..* → 0..* |
| `RK2-009` | incoming `descriptionContext` | [Risk Description](RKM-C024.md) | 0..* → 0..1 |
| `RK2-010` | incoming `scenarioContext` | [Risk Scenario Specification](RKM-C003.md) | 0..* → 0..* |
| `RK2-011` | outgoing `referencesObjective` | [Objective Reference](RKM-X02.md) | 0..* → 0..* |
| `RK2-012` | incoming `uncertaintyContext` | [Uncertainty Statement](RKM-X03.md) | 0..* → 0..1 |
| `RK2-023` | incoming `appetiteContext` | [Risk Appetite Statement](RKM-C073.md) | 0..* → 1..* |
| `RK2-024` | incoming `toleranceContext` | [Risk Tolerance Statement](RKM-C074.md) | 0..* → 1..* |
| `RK2-026` | incoming `observationContext` | [Observation Result](RKM-C068.md) | 0..* → 0..1 |
| `RK3-003` | incoming `sourceReferenceContext` | [Risk Source Reference](RKM-X06.md) | 0..* → 0..1 |
| `RX-001` | incoming `hasContext` | [Risk Case](RKM-X01.md) | 0..* → 1..* |
| `RX-017` | incoming `criteriaForContext` | [Risk Criteria](RKM-C072.md) | 0..* → 1..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
