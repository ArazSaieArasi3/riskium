# Plan Specification

**Source ID:** `RKM-C043` · **Subdomain:** [D06 · Risk Treatment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A versioned specification of intended actions, resources, responsibilities, timing and conditions for a stated purpose.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-21` | outgoing `planAbout` | [Risk Case](RKM-X01.md) | 0..* → 1..* |
| `R-61` | incoming `recordsPlan` | [Entry Revision](RKM-C023.md) | 1..* → 0..* |
| `R-62` | outgoing `planRole` | [Plan Role Term](RKM-C046.md) | 0..* → 1 |
| `R-63` | incoming `isSpecifiedByPlan` | [Treatment Decision Information](RKM-C041.md) | 0..* → 0..* |
| `R-64` | incoming `executesPlan` | [Treatment Activity](RKM-C044.md) | 0..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
