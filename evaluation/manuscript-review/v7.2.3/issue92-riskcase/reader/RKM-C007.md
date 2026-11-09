# Risk Source

Candidate **0.3.2-case.1**; not the published current dictionary. Source SHA-256: `e98a63b286441c80fc10a9644804d64fc2b611e906b2d27cf3d72f3ebd72cfa8`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C007`; **source title:** `RiskSource`; **layer:** `OPTIONAL_PHENOMENON_BOUNDARY`; **native representation:** `Note`.

**Subdomain:** [D01 · Risk Phenomena](Subdomains.md#d01)

## Authored source definition

A contextual source role that an entity may play in giving rise to risk, alone or with other contributors. The catalog boundary spans possible bearer categories and is not assigned a single OntoUML stereotype here.

## Identity and source typing

- OntoUML stereotype: `not assigned`; abstract: `false`.
- Identity supplier: No identity supplier is assigned in this source record.
- Identity basis: Bearer-specific; no uniform identity principle over objects, events, situations and aspects.
- Typing rationale: Broad domain notion retained in the catalog and optional external bridge; no uniform native OntoUML class asserted.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RK3-002 | incoming `resolvesToSource` | [Risk Source Reference](RKM-X06.md) | 0..* | 0..1 | OPTIONAL_EXTERNAL_BRIDGE |
| RX-005 | incoming `hasSource` | [Risk Case](RKM-X01.md) | 0..* | 0..* | OPTIONAL_EXTERNAL_BRIDGE |

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
