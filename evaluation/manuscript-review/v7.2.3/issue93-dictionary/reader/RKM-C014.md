# Information Artifact

Candidate **0.3.2-structural.2**; not the published current dictionary. Source SHA-256: `c1556811a468919b75521d1a93b8ef8f91c24bf2799deae274b1d211d5e4d5b7`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C014`; **source title:** `InformationArtifact`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D02 · Risk Information](Subdomains.md#d02)

## Authored source definition

A managed documentary object with an instituted identity that persists across its descriptions and issued versions. Artifact identity is distinct from a file path, a storage row and semantic content.

## Identity and source typing

- OntoUML stereotype: `kind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Provides an explicitly governed individuation principle within the declared profile; surrogate keys are identifiers of that policy, not independent ontological proof.
- Typing rationale: Proposed identity-supplying sortal; external Person/Organization and instituted case identities require their owning-domain commitments.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-68 | incoming `supportsRecordedArtifact` | [Evidence Reference](RKM-C065.md) | 0..* | 1..* | FORMAL_CORE |
| RE-003 | incoming `groundedInUseRecord` | [Evidence Use Relator](RKM-C075.md) | 0..* | 1 | FORMAL_CORE |
| RX-006 | incoming `versionOf` | [Artifact Version](RKM-C015.md) | 0..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.  
Direct subtypes: [Risk Register Entry](RKM-C022.md), [Risk Description](RKM-C024.md), [Classification Assertion](RKM-C020.md), [Identification Information](RKM-C026.md), [Actor Reference](RKM-C050.md), [Responsibility Assignment Information](RKM-C051.md), [Risk Nature Assertion](RKM-C005.md), [Assessment Information](RKM-C032.md), [Assessment Basis](RKM-C033.md), [Dimension Assessment Result](RKM-C034.md), [Assessment Method Specification](RKM-C035.md), [Assessment Scale](RKM-C036.md), [Risk Score Result](RKM-C037.md), [Treatment Decision Information](RKM-C041.md), [Plan Specification](RKM-C043.md), [Consequence Statement](RKM-C025.md), [Record State Assertion](RKM-C062.md), [Evidence Reference](RKM-C065.md), [Risk Pattern Specification](RKM-C001.md), [Risk Context Specification](RKM-C002.md), [Risk Scenario Specification](RKM-C003.md), [Classification Scheme](RKM-C018.md), [Risk Register](RKM-C030.md), [Evidence Item](RKM-C066.md), [Observation Result](RKM-C068.md), [Indicator](RKM-C069.md), [Threshold](RKM-C070.md), [Signal](RKM-C071.md), [Risk Criteria](RKM-C072.md), [Risk Appetite Statement](RKM-C073.md), [Risk Tolerance Statement](RKM-C074.md), [Objective Reference](RKM-X02.md), [Uncertainty Statement](RKM-X03.md), [Risk Evaluation Outcome](RKM-X04.md), [Control Reference](RKM-X05.md), [Vocabulary Concept](RKM-C017.md), [Tag](RKM-C021.md), [Risk Source Reference](RKM-X06.md)

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Selected integration interpretation](../../issue93-integration/definitions/RKM-C014.md) preserves the separate candidate design decision.

[Rebuildable source recipe](../../issue93-generalization-sets/build_candidate.py) · [Export contract](../../issue93-export-contract/input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
