# Dimension Assessment Result

**Source ID:** `RKM-C034` · **Subdomain:** [D05 · Risk Assessment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A result for one assessment dimension, qualified by its method, scale, basis and relevant temporal context.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-13` | incoming `hasDimensionResult` | [Assessment Information](RKM-C032.md) | 1 → 0..* |
| `R-14` | outgoing `usesScale` | [Assessment Scale](RKM-C036.md) | 0..* → 0..1 |
| `R-15` | outgoing `selectsLevel` | [Assessment Scale Level](RKM-C038.md) | 0..* → 0..1 |
| `R-18` | incoming `derivedFrom` | [Risk Score Result](RKM-C037.md) | 0..* → 0..* |
| `R-48` | outgoing `dimension` | [Assessment Dimension](RKM-C039.md) | 0..* → 1 |
| `RX-016` | outgoing `usesScaleVersion` | [Artifact Version](RKM-C015.md) | 0..* → 0..1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
