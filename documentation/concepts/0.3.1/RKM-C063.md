# Workflow Scheme Version

**Source ID:** `RKM-C063` · **Subdomain:** [D08 · Risk Workflow](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An issued version of a scheme defining workflow values and permitted transitions.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Artifact Version](RKM-C015.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-021` | incoming `availableInWorkflowScheme` | [Workflow State Term](RKM-C061.md) | 0..* → 1..* |
| `RX-030` | incoming `underSchemeVersion` | [Workflow Assignment](RKM-C064.md) | 0..* → 1 |

Generalizes: [Artifact Version](RKM-C015.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
