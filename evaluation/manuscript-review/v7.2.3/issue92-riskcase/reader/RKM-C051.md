# Responsibility Assignment Information

Candidate **0.3.2-case.1**; not the published current dictionary. Source SHA-256: `e98a63b286441c80fc10a9644804d64fc2b611e906b2d27cf3d72f3ebd72cfa8`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C051`; **source title:** `ResponsibilityAssignmentInformation`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D07 · Risk Responsibility](Subdomains.md#d07)

## Authored source definition

A recorded statement about an assignment of responsibility or authority, distinct from the relationship it asserts.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-09 | outgoing `assignmentAbout` | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-10 | outgoing `hasBearerReference` | [Actor Reference](RKM-C050.md) | 0..* | 1 | FORMAL_CORE |
| R-30 | incoming `documentsAssignment` | [Entry Revision](RKM-C023.md) | 1..* | 0..* | FORMAL_CORE |
| R-54 | outgoing `assignmentRole` | [Responsibility Role Term](RKM-C059.md) | 0..* | 1 | FORMAL_CORE |
| R-55 | outgoing `documentsActualMandate` | [Responsibility Relator](RKM-C052.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-025 | outgoing `authorizerReference` | [Actor Reference](RKM-C050.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)  
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Rebuildable source recipe](../build_candidate.py) · [Export contract](../input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
