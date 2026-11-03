# Consequence Statement

**Source ID:** `RKM-C025` · **Subdomain:** [D04 · Risk Registration](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An information item expressing a possible or reported consequence; it is not the consequence itself.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-22` | outgoing `statementAbout` | [Risk Case](RKM-X01.md) | 0..* → 1 |
| `R-38` | incoming `recordsConsequence` | [Entry Revision](RKM-C023.md) | 1 → 0..* |
| `R-40` | outgoing `sourceSlot` | [Consequence Slot Term](RKM-C029.md) | 0..* → 1 |
| `RX-009` | incoming `hasPossibleConsequenceStatement` | [Risk Scenario Specification](RKM-C003.md) | 0..* → 0..* |
| `RX-010` | outgoing `refersToActualOutcome` | [Consequence](RKM-C010.md) | 0..* → 0..1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
