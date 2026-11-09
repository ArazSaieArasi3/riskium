# Evidence Reference

Candidate **0.3.2-case.1**; not the published current dictionary. Source SHA-256: `e98a63b286441c80fc10a9644804d64fc2b611e906b2d27cf3d72f3ebd72cfa8`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C065`; **source title:** `EvidenceReference`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D09 · Risk Evidence](Subdomains.md#d09)

## Authored source definition

A qualified reference linking a claim or activity to an evidence item, with its intended evidential role and provenance.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-68 | outgoing `supportsRecordedArtifact` | [Information Artifact](RKM-C014.md) | 0..* | 1..* | FORMAL_CORE |
| R-69 | outgoing `refersToOccurrence` | [Risk Occurrence](RKM-C004.md) | 0..* | 0..* | FORMAL_CORE |
| R-70 | outgoing `refersToAgent` | [Agent](RKM-C047.md) | 0..* | 0..* | FORMAL_CORE |
| R-71 | outgoing `refersToAssessmentActivity` | [Assessment Activity](RKM-C031.md) | 0..* | 0..* | FORMAL_CORE |
| R-72 | outgoing `refersToTreatmentActivity` | [Treatment Activity](RKM-C044.md) | 0..* | 0..* | FORMAL_CORE |
| RX-021 | outgoing `pointsToEvidence` | [Evidence Item](RKM-C066.md) | 1..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)  
Direct subtypes: [Evidence Reference Role](RKM-C076.md)

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Selected integration interpretation](../../issue93-integration/definitions/RKM-C065.md) preserves the separate candidate design decision.

[Rebuildable source recipe](../build_candidate.py) · [Export contract](../input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
