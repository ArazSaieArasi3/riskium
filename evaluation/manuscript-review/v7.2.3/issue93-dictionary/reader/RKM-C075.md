# Evidence Use Relator

Candidate **0.3.2-structural.2**; not the published current dictionary. Source SHA-256: `c1556811a468919b75521d1a93b8ef8f91c24bf2799deae274b1d211d5e4d5b7`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C075`; **source title:** `EvidenceUseRelator`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D09 · Risk Evidence](Subdomains.md#d09)

## Authored source definition

A context-qualified evidential-use relationship connecting a qualified reference and a distinct information artifact used as support, challenge or context in an analysis. Its grounding concerns that use, not the truth of the referenced claim.

## Identity and source typing

- OntoUML stereotype: `relator`; abstract: `false`.
- Identity supplier: [Evidence Use Relator](RKM-C075.md)
- Identity basis: One grounded use episode qualified by its reference, evidence artifact, analysis context and evidential purpose; different descriptions of that same use do not supply new identities.
- Typing rationale: Relator candidate: a grounded evidential-use relationship, with two distinct mediated documentary participants. The information describing a proposed use is not automatically an instance of this relator.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RE-001 | outgoing `mediatesEvidenceItem` | [Evidence Item](RKM-C066.md) | 1..* | 1 | FORMAL_CORE |
| RE-002 | outgoing `mediatesEvidenceReference` | [Evidence Reference Role](RKM-C076.md) | 1..* | 1 | FORMAL_CORE |
| RE-003 | outgoing `groundedInUseRecord` | [Information Artifact](RKM-C014.md) | 0..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.  
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** ISOLATED_CANDIDATE; scoped source, OWL and explicit-data tests recorded separately

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Selected integration interpretation](../../issue93-integration/definitions/RKM-C075.md) preserves the separate candidate design decision.

[Rebuildable source recipe](../../issue93-generalization-sets/build_candidate.py) · [Export contract](../../issue93-export-contract/input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
