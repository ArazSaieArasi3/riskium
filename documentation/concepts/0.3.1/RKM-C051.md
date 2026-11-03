# Responsibility Assignment Information

**Source ID:** `RKM-C051` · **Subdomain:** [D07 · Risk Responsibility](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A recorded statement about an assignment of responsibility or authority, distinct from the relationship it asserts.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-09` | outgoing `assignmentAbout` | [Risk Case](RKM-X01.md) | 0..* → 1 |
| `R-10` | outgoing `hasBearerReference` | [Actor Reference](RKM-C050.md) | 0..* → 1 |
| `R-30` | incoming `documentsAssignment` | [Entry Revision](RKM-C023.md) | 1..* → 0..* |
| `R-54` | outgoing `assignmentRole` | [Responsibility Role Term](RKM-C059.md) | 0..* → 1 |
| `R-55` | outgoing `documentsActualMandate` | [Responsibility Relator](RKM-C052.md) | 0..* → 0..1 |
| `RK2-025` | outgoing `authorizerReference` | [Actor Reference](RKM-C050.md) | 0..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
