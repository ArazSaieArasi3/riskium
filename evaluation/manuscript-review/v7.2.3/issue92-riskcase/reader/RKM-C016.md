# Information Content

Candidate **0.3.2-case.1**; not the published current dictionary. Source SHA-256: `e98a63b286441c80fc10a9644804d64fc2b611e906b2d27cf3d72f3ebd72cfa8`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C016`; **source title:** `InformationContent`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D02 · Risk Information](Subdomains.md#d02)

## Authored source definition

The abstract informational meaning expressed by artifacts or versions. Content identity requires an explicit equivalence policy and is not inferred from equal strings or file hashes.

## Identity and source typing

- OntoUML stereotype: `abstract`; abstract: `false`.
- Identity supplier: No identity supplier is assigned in this source record.
- Identity basis: Abstract content identity requires a separately declared equivalence policy.
- Typing rationale: OntoUML 2 abstract-domain commitment, not a concrete managed-document kind. Native profile conformance is not established by this catalog.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RX-007 | incoming `expressesContent` | [Artifact Version](RKM-C015.md) | 0..* | 1..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.  
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Rebuildable source recipe](../build_candidate.py) · [Export contract](../input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
