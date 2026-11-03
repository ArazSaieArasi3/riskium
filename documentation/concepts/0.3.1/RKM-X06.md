# Risk Source Reference

**Source ID:** `RKM-X06` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A managed information artifact identifying or describing a claimed contributor to risk in a declared context. The referenced contributor may be unresolved, hypothetical or heterogeneous. The reference does not establish actual causation or an actual occurrence.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Governed documentary identity, inherited from InformationArtifact; source-reference identity is distinct from source-bearer identity.
- Typing rationale: A documentary reference can be uniformly typed without forcing its heterogeneous referents into one category.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK3-001` | incoming `hasSourceReference` | [Risk Case](RKM-X01.md) | 0..* → 0..* |
| `RK3-002` | outgoing `resolvesToSource` | [Risk Source](RKM-C007.md) | 0..* → 0..1 |
| `RK3-003` | outgoing `sourceReferenceContext` | [Risk Context Specification](RKM-C002.md) | 0..* → 0..1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
