# Vulnerability

Candidate **0.3.2-case.1**; not the published current dictionary. Source SHA-256: `e98a63b286441c80fc10a9644804d64fc2b611e906b2d27cf3d72f3ebd72cfa8`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C011`; **source title:** `Vulnerability`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D01 · Risk Phenomena](Subdomains.md#d01)

## Authored source definition

An intrinsic susceptibility of a bearer to specified risk-relevant conditions or effects. The proposed mode interpretation requires a supported bearer; security-specific exploitation meanings remain source-qualified.

## Identity and source typing

- OntoUML stereotype: `mode`; abstract: `false`.
- Identity supplier: No identity supplier is assigned in this source record.
- Identity basis: Intrinsic susceptibility with exactly one substantial-endurant bearer. Bearer identity is supplied externally. Mere reported susceptibility is recorded as information, not automatically asserted as an actual intrinsic mode.
- Typing rationale: The approved intrinsic interpretation is proposed as «mode» and is connected to an imported Object category through characterization. Broader relational vulnerability meanings are not silently equated with this interpretation.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RK2-002 | incoming `refersToVulnerability` | [Risk Context Specification](RKM-C002.md) | 0..* | 0..* | FORMAL_CORE |
| RK3-004 | incoming `bearsVulnerability` | [External Object](EXT-OBJECT.md) | 1 | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.  
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Rebuildable source recipe](../build_candidate.py) · [Export contract](../input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
