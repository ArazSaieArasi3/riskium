# Observation Result

**Source ID:** `RKM-C068` · **Subdomain:** [D10 · Risk Monitoring](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An information result produced by an observation activity, qualified by subject, time, method and available units.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-017` | incoming `recordsObservation` | [Entry Revision](RKM-C023.md) | 0..* → 0..* |
| `RK2-026` | outgoing `observationContext` | [Risk Context Specification](RKM-C002.md) | 0..* → 0..1 |
| `RX-022` | incoming `producesObservation` | [Observation Activity](RKM-C067.md) | 1 → 0..* |
| `RX-023` | outgoing `reportsIndicator` | [Indicator](RKM-C069.md) | 0..* → 1 |
| `RX-024` | outgoing `observesCase` | [Risk Case](RKM-X01.md) | 0..* → 1 |
| `RX-026` | incoming `basedOnObservation` | [Signal](RKM-C071.md) | 0..* → 1..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
