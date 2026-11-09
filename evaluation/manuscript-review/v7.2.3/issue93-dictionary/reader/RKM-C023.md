# Entry Revision

Candidate **0.3.2-structural.2**; not the published current dictionary. Source SHA-256: `c1556811a468919b75521d1a93b8ef8f91c24bf2799deae274b1d211d5e4d5b7`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C023`; **source title:** `EntryRevision`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D04 · Risk Registration](Subdomains.md#d04)

## Authored source definition

An identifiable version of a register entry, preserving the content and qualified links effective at its issue.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Artifact Version](RKM-C015.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-02 | outgoing `hasDescription` | [Risk Description](RKM-C024.md) | 1 | 0..* | FORMAL_CORE |
| R-23 | outgoing `hasStateAssertion` | [Record State Assertion](RKM-C062.md) | 1 | 0..* | FORMAL_CORE |
| R-24 | outgoing `hasTag` | [Tag](RKM-C021.md) | 0..* | 0..* | FORMAL_CORE |
| R-28 | outgoing `documentsAssessment` | [Assessment Information](RKM-C032.md) | 1..* | 0..* | FORMAL_CORE |
| R-29 | outgoing `documentsClassification` | [Classification Assertion](RKM-C020.md) | 1..* | 0..* | FORMAL_CORE |
| R-30 | outgoing `documentsAssignment` | [Responsibility Assignment Information](RKM-C051.md) | 1..* | 0..* | FORMAL_CORE |
| R-33 | outgoing `revisionOf` | [Risk Register Entry](RKM-C022.md) | 0..* | 1 | FORMAL_CORE |
| R-34 | incoming `previousRevision` | [Entry Revision](RKM-C023.md) | 0..* | 0..1 | FORMAL_CORE |
| R-34 | outgoing `previousRevision` | [Entry Revision](RKM-C023.md) | 0..* | 0..1 | FORMAL_CORE |
| R-38 | outgoing `recordsConsequence` | [Consequence Statement](RKM-C025.md) | 1 | 0..* | FORMAL_CORE |
| R-44 | outgoing `recordsNature` | [Risk Nature Assertion](RKM-C005.md) | 1..* | 0..* | FORMAL_CORE |
| R-52 | outgoing `recordsIdentification` | [Identification Information](RKM-C026.md) | 1..* | 0..* | FORMAL_CORE |
| R-60 | outgoing `recordsDecision` | [Treatment Decision Information](RKM-C041.md) | 1..* | 0..* | FORMAL_CORE |
| R-61 | outgoing `recordsPlan` | [Plan Specification](RKM-C043.md) | 1..* | 0..* | FORMAL_CORE |
| RK2-016 | outgoing `recordsControlReference` | [Control Reference](RKM-X05.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-017 | outgoing `recordsObservation` | [Observation Result](RKM-C068.md) | 0..* | 0..* | FORMAL_CORE |
| RX-031 | incoming `assignmentForRevision` | [Workflow Assignment](RKM-C064.md) | 0..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Artifact Version](RKM-C015.md)  
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Rebuildable source recipe](../../issue93-generalization-sets/build_candidate.py) · [Export contract](../../issue93-export-contract/input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
