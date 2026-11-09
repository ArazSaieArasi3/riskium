# Risk Control

Candidate **0.3.2-case.1**; not the published current dictionary. Source SHA-256: `e98a63b286441c80fc10a9644804d64fc2b611e906b2d27cf3d72f3ebd72cfa8`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C045`; **source title:** `RiskControl`; **layer:** `OPTIONAL_PHENOMENON_BOUNDARY`; **native representation:** `Note`.

**Subdomain:** [D06 · Risk Treatment](Subdomains.md#d06)

## Authored source definition

A contextual measure intended to maintain or modify risk. A policy, device, practice or activity may serve as its bearer. Implementation and observed effectiveness are separate claims; one cross-category stereotype is not asserted.

## Identity and source typing

- OntoUML stereotype: `not assigned`; abstract: `false`.
- Identity supplier: No identity supplier is assigned in this source record.
- Identity basis: Bearer-specific; no uniform identity principle over objects, events, situations and aspects.
- Typing rationale: Broad domain notion retained in the catalog and optional external bridge; no uniform native OntoUML class asserted.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-66 | incoming `implementsControl` | [Treatment Activity](RKM-C044.md) | 0..* | 0..* | OPTIONAL_EXTERNAL_BRIDGE |
| R-67 | outgoing `controlAddressing` | [Risk Case](RKM-X01.md) | 0..* | 0..* | OPTIONAL_EXTERNAL_BRIDGE |
| RX-020 | incoming `resolvesToControl` | [Control Reference](RKM-X05.md) | 0..* | 0..1 | OPTIONAL_EXTERNAL_BRIDGE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.  
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

This is an optional catalog boundary represented as a native Note; its displayed source stereotype does not make it an exported typed-core class.

[Rebuildable source recipe](../build_candidate.py) · [Export contract](../input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
