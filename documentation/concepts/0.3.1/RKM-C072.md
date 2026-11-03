# Risk Criteria

**Source ID:** `RKM-C072` · **Subdomain:** [D11 · Risk Policy](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A versioned information specification of reference conditions used to judge the significance or acceptability of risk in an identified context.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RX-017` | outgoing `criteriaForContext` | [Risk Context Specification](RKM-C002.md) | 0..* → 1..* |
| `RX-018` | outgoing `considersAppetiteStatement` | [Risk Appetite Statement](RKM-C073.md) | 0..* → 0..* |
| `RX-019` | outgoing `considersToleranceStatement` | [Risk Tolerance Statement](RKM-C074.md) | 0..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
