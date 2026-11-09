# Evidence Item

Candidate **0.3.2-case.1**; not the published current dictionary. Source SHA-256: `e98a63b286441c80fc10a9644804d64fc2b611e906b2d27cf3d72f3ebd72cfa8`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C066`; **source title:** `EvidenceItem`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D09 · Risk Evidence](Subdomains.md#d09)

## Authored source definition

An information artifact playing an evidential role for a specified claim or analytical activity. The same artifact may be used as evidence in one context and not another.

## Identity and source typing

- OntoUML stereotype: `role`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits bearer identity; role membership depends on an explicit responsibility or evidential context.
- Typing rationale: Anti-rigid documentary role founded through mandatory mediation by EvidenceUseRelator. The artifact retains InformationArtifact identity when not used as evidence.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RE-001 | incoming `mediatesEvidenceItem` | [Evidence Use Relator](RKM-C075.md) | 1..* | 1 | FORMAL_CORE |
| RX-021 | incoming `pointsToEvidence` | [Evidence Reference](RKM-C065.md) | 1..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)  
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Selected integration interpretation](../../issue93-integration/definitions/RKM-C066.md) preserves the separate candidate design decision.

[Rebuildable source recipe](../build_candidate.py) · [Export contract](../input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
