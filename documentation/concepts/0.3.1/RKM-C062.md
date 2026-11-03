# Record State Assertion

**Source ID:** `RKM-C062` · **Subdomain:** [D08 · Risk Workflow](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A qualified statement about a record's state, preserving the source and available temporal precision.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-23` | incoming `hasStateAssertion` | [Entry Revision](RKM-C023.md) | 1 → 0..* |
| `R-31` | outgoing `declaresAnalysisState` | [Analysis State Term](RKM-C060.md) | 0..* → 0..1 |
| `R-32` | outgoing `declaresWorkflowState` | [Workflow State Term](RKM-C061.md) | 0..* → 0..1 |
| `RX-032` | outgoing `documentsWorkflowAssignment` | [Workflow Assignment](RKM-C064.md) | 0..* → 0..1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
