# Risk Source Reference

Candidate **0.3.2-structural.2**; not the published current dictionary. Source SHA-256: `c1556811a468919b75521d1a93b8ef8f91c24bf2799deae274b1d211d5e4d5b7`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-X06`; **source title:** `RiskSourceReference`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D01 · Risk Phenomena](Subdomains.md#d01)

## Authored source definition

A managed information artifact identifying or describing a claimed contributor to risk in a declared context. The referenced contributor may be unresolved, hypothetical or heterogeneous. The reference does not establish actual causation or an actual occurrence.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Governed documentary identity, inherited from InformationArtifact; source-reference identity is distinct from source-bearer identity.
- Typing rationale: A documentary reference can be uniformly typed without forcing its heterogeneous referents into one category.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RK3-001 | incoming `hasSourceReference` | [Risk Case](RKM-X01.md) | 0..* | 0..* | FORMAL_CORE |
| RK3-002 | outgoing `resolvesToSource` | [Risk Source](RKM-C007.md) | 0..* | 0..1 | OPTIONAL_EXTERNAL_BRIDGE |
| RK3-003 | outgoing `sourceReferenceContext` | [Risk Context Specification](RKM-C002.md) | 0..* | 0..1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)  
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Rebuildable source recipe](../../issue93-generalization-sets/build_candidate.py) · [Export contract](../../issue93-export-contract/input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
