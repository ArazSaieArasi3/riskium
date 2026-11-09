# Artifact Version

Candidate **0.3.2-structural.2**; not the published current dictionary. Source SHA-256: `c1556811a468919b75521d1a93b8ef8f91c24bf2799deae274b1d211d5e4d5b7`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C015`; **source title:** `ArtifactVersion`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D02 · Risk Information](Subdomains.md#d02)

## Authored source definition

An identifiable issued documentary version of a managed information artifact. Its issued semantic content and effective dependency versions are immutable; revisions receive distinct version identities.

## Identity and source typing

- OntoUML stereotype: `kind`; abstract: `false`.
- Identity supplier: [Artifact Version](RKM-C015.md)
- Identity basis: Provides an explicitly governed individuation principle within the declared profile; surrogate keys are identifiers of that policy, not independent ontological proof.
- Typing rationale: Proposed identity-supplying sortal; external Person/Organization and instituted case identities require their owning-domain commitments.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RX-006 | outgoing `versionOf` | [Information Artifact](RKM-C014.md) | 0..* | 1 | FORMAL_CORE |
| RX-007 | outgoing `expressesContent` | [Information Content](RKM-C016.md) | 0..* | 1..* | FORMAL_CORE |
| RX-013 | incoming `usesCriteriaVersion` | [Risk Evaluation Outcome](RKM-X04.md) | 0..* | 1 | FORMAL_CORE |
| RX-014 | incoming `usesContextVersion` | [Assessment Information](RKM-C032.md) | 0..* | 1 | FORMAL_CORE |
| RX-015 | incoming `usesMethodVersion` | [Assessment Information](RKM-C032.md) | 0..* | 0..1 | FORMAL_CORE |
| RX-016 | incoming `usesScaleVersion` | [Dimension Assessment Result](RKM-C034.md) | 0..* | 0..1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.  
Direct subtypes: [Entry Revision](RKM-C023.md), [Workflow Scheme Version](RKM-C063.md)

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Rebuildable source recipe](../../issue93-generalization-sets/build_candidate.py) · [Export contract](../../issue93-export-contract/input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
