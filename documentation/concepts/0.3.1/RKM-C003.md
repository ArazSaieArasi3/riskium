# Risk Scenario Specification

**Source ID:** `RKM-C003` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A managed information specification of a possible development of conditions, events and effects concerning one or more RiskCases. Several scenarios may concern one case; a scenario is not the case or an actual occurrence.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-25` | outgoing `mayBeRealizedBy` | [Risk Occurrence](RKM-C004.md) | 0..* → 0..* |
| `R-36` | outgoing `scenarioAbout` | [Risk Case](RKM-X01.md) | 0..* → 1..* |
| `R-37` | incoming `expressesScenario` | [Risk Description](RKM-C024.md) | 0..* → 0..* |
| `RK2-010` | outgoing `scenarioContext` | [Risk Context Specification](RKM-C002.md) | 0..* → 0..* |
| `RX-009` | outgoing `hasPossibleConsequenceStatement` | [Consequence Statement](RKM-C025.md) | 0..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
