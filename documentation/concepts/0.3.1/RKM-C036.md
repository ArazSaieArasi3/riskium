# Assessment Scale

**Source ID:** `RKM-C036` · **Subdomain:** [D05 · Risk Assessment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A governed scale specification defining permissible values or ordered levels for a specified assessment dimension.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-14` | incoming `usesScale` | [Dimension Assessment Result](RKM-C034.md) | 0..* → 0..1 |
| `R-16` | incoming `levelOf` | [Assessment Scale Level](RKM-C038.md) | 0..* → 1 |
| `R-49` | incoming `permitsScale` | [Assessment Method Specification](RKM-C035.md) | 0..* → 0..* |
| `RK2-019` | outgoing `scaleForDimension` | [Assessment Dimension](RKM-C039.md) | 0..* → 1 |
| `RK2-020` | incoming `thresholdOnScale` | [Threshold](RKM-C070.md) | 0..* → 0..1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
