# Classification Term

**Source ID:** `RKM-C019` · **Subdomain:** [D03 · Risk Classification](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A managed vocabulary item expressing a controlled classification value within an identified scheme. Scheme membership and version context constrain its interpretation. This is a managed vocabulary resource with scheme-qualified identity, not a bare string.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-04` | incoming `selectsTerm` | [Classification Assertion](RKM-C020.md) | 0..* → 1 |
| `R-05` | outgoing `belongsToScheme` | [Classification Scheme](RKM-C018.md) | 0..* → 1 |
| `R-06` | outgoing `hasBroaderTerm` | [Classification Term](RKM-C019.md) | 0..* → 0..* |
| `R-06` | incoming `hasBroaderTerm` | [Classification Term](RKM-C019.md) | 0..* → 0..* |

Generalizes: [Vocabulary Concept](RKM-C017.md).  
Specialized by: [Nature Term](RKM-C006.md), [Intake Channel Term](RKM-C027.md), [Description Role Term](RKM-C028.md), [Consequence Slot Term](RKM-C029.md), [Epistemic Status Term](RKM-C040.md), [Treatment Strategy Term](RKM-C042.md), [Plan Role Term](RKM-C046.md), [Responsibility Role Term](RKM-C059.md), [Analysis State Term](RKM-C060.md), [Workflow State Term](RKM-C061.md).

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
