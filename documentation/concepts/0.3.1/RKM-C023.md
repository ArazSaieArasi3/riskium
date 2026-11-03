# Entry Revision

**Source ID:** `RKM-C023` · **Subdomain:** [D04 · Risk Registration](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An identifiable version of a register entry, preserving the content and qualified links effective at its issue.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Artifact Version](RKM-C015.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-02` | outgoing `hasDescription` | [Risk Description](RKM-C024.md) | 1 → 0..* |
| `R-23` | outgoing `hasStateAssertion` | [Record State Assertion](RKM-C062.md) | 1 → 0..* |
| `R-24` | outgoing `hasTag` | [Tag](RKM-C021.md) | 0..* → 0..* |
| `R-28` | outgoing `documentsAssessment` | [Assessment Information](RKM-C032.md) | 1..* → 0..* |
| `R-29` | outgoing `documentsClassification` | [Classification Assertion](RKM-C020.md) | 1..* → 0..* |
| `R-30` | outgoing `documentsAssignment` | [Responsibility Assignment Information](RKM-C051.md) | 1..* → 0..* |
| `R-33` | outgoing `revisionOf` | [Risk Register Entry](RKM-C022.md) | 0..* → 1 |
| `R-34` | outgoing `previousRevision` | [Entry Revision](RKM-C023.md) | 0..* → 0..1 |
| `R-34` | incoming `previousRevision` | [Entry Revision](RKM-C023.md) | 0..* → 0..1 |
| `R-38` | outgoing `recordsConsequence` | [Consequence Statement](RKM-C025.md) | 1 → 0..* |
| `R-44` | outgoing `recordsNature` | [Risk Nature Assertion](RKM-C005.md) | 1..* → 0..* |
| `R-52` | outgoing `recordsIdentification` | [Identification Information](RKM-C026.md) | 1..* → 0..* |
| `R-60` | outgoing `recordsDecision` | [Treatment Decision Information](RKM-C041.md) | 1..* → 0..* |
| `R-61` | outgoing `recordsPlan` | [Plan Specification](RKM-C043.md) | 1..* → 0..* |
| `RK2-016` | outgoing `recordsControlReference` | [Control Reference](RKM-X05.md) | 0..* → 0..* |
| `RK2-017` | outgoing `recordsObservation` | [Observation Result](RKM-C068.md) | 0..* → 0..* |
| `RX-031` | incoming `assignmentForRevision` | [Workflow Assignment](RKM-C064.md) | 0..* → 1 |

Generalizes: [Artifact Version](RKM-C015.md).  
Specialized by: none recorded.

## External definition and alignment status

No separately sourced external definition or term-level standards equivalence is recorded for this identifier in the model catalog. The [inspected source register](../../../references/README.md) is context, not proof of one-to-one alignment. A future alignment requires the exact source passage, edition, relation type, reviewer and rationale; absent that record, status is **unassessed**.

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
