# Agent

Candidate **0.3.2-case.1**; not the published current dictionary. Source SHA-256: `e98a63b286441c80fc10a9644804d64fc2b611e906b2d27cf3d72f3ebd72cfa8`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C047`; **source title:** `Agent`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D07 · Risk Responsibility](Subdomains.md#d07)

## Authored source definition

An entity capable of performing or being accountable for relevant actions, including persons and organizations within the declared profile.

## Identity and source typing

- OntoUML stereotype: `category`; abstract: `true`.
- Identity supplier: No identity supplier is assigned in this source record.
- Identity basis: No new identity principle; Person and Organization supply different identities.
- Typing rationale: Rigid abstract non-sortal over the external actor kinds.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-51 | incoming `assessmentPerformer` | [Assessment Activity](RKM-C031.md) | 0..* | 0..* | FORMAL_CORE |
| R-53 | incoming `resolvesToAgent` | [Actor Reference](RKM-C050.md) | 0..* | 0..1 | FORMAL_CORE |
| R-65 | incoming `treatmentPerformer` | [Treatment Activity](RKM-C044.md) | 0..* | 0..* | FORMAL_CORE |
| R-70 | incoming `refersToAgent` | [Evidence Reference](RKM-C065.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.  
Direct subtypes: [Person](RKM-C048.md), [Organization](RKM-C049.md), [Responsible Agent Role](RKM-C053.md), [Authorizing Agent Role](RKM-C054.md)

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Selected integration interpretation](../../issue93-integration/definitions/RKM-C047.md) preserves the separate candidate design decision.

[Rebuildable source recipe](../build_candidate.py) · [Export contract](../input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
