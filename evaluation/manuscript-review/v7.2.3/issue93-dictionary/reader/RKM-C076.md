# Evidence Reference Role

Candidate **0.3.2-structural.2**; not the published current dictionary. Source SHA-256: `c1556811a468919b75521d1a93b8ef8f91c24bf2799deae274b1d211d5e4d5b7`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C076`; **source title:** `EvidenceReferenceRole`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D09 · Risk Evidence](Subdomains.md#d09)

## Authored source definition

A qualified EvidenceReference participating in an actual grounded evidential-use relationship. The reference retains documentary identity when it is only a record of a proposed use.

## Identity and source typing

- OntoUML stereotype: `role`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits InformationArtifact identity through EvidenceReference; role membership depends on grounded evidential use.
- Typing rationale: Anti-rigid participation of a documentary reference, distinct from merely recording a proposed use.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RE-002 | incoming `mediatesEvidenceReference` | [Evidence Use Relator](RKM-C075.md) | 1..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Evidence Reference](RKM-C065.md)  
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** ISOLATED_CANDIDATE; scoped tests recorded separately

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Selected integration interpretation](../../issue93-integration/definitions/RKM-C076.md) preserves the separate candidate design decision.

[Rebuildable source recipe](../../issue93-generalization-sets/build_candidate.py) · [Export contract](../../issue93-export-contract/input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
