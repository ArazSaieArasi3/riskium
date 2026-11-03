# Signal

**Source ID:** `RKM-C071` · **Subdomain:** [D10 · Risk Monitoring](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An information item indicating a potentially relevant change or condition and potentially prompting review; it does not by itself establish a risk event.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RX-026` | outgoing `basedOnObservation` | [Observation Result](RKM-C068.md) | 0..* → 1..* |
| `RX-027` | outgoing `evaluatedAgainstThreshold` | [Threshold](RKM-C070.md) | 0..* → 0..* |
| `RX-028` | outgoing `promptsReviewOf` | [Risk Case](RKM-X01.md) | 0..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
