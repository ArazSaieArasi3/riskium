# Classification Term

Candidate **0.3.2-structural.2**; not the published current dictionary. Source SHA-256: `c1556811a468919b75521d1a93b8ef8f91c24bf2799deae274b1d211d5e4d5b7`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C019`; **source title:** `ClassificationTerm`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D03 · Risk Classification](Subdomains.md#d03)

## Authored source definition

A managed vocabulary item expressing a controlled classification value within an identified scheme. Scheme membership and version context constrain its interpretation. This is a managed vocabulary resource with scheme-qualified identity, not a bare string.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-04 | incoming `selectsTerm` | [Classification Assertion](RKM-C020.md) | 0..* | 1 | FORMAL_CORE |
| R-05 | outgoing `belongsToScheme` | [Classification Scheme](RKM-C018.md) | 0..* | 1 | FORMAL_CORE |
| R-06 | incoming `hasBroaderTerm` | [Classification Term](RKM-C019.md) | 0..* | 0..* | FORMAL_CORE |
| R-06 | outgoing `hasBroaderTerm` | [Classification Term](RKM-C019.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Vocabulary Concept](RKM-C017.md)  
Direct subtypes: [Nature Term](RKM-C006.md), [Intake Channel Term](RKM-C027.md), [Description Role Term](RKM-C028.md), [Consequence Slot Term](RKM-C029.md), [Epistemic Status Term](RKM-C040.md), [Treatment Strategy Term](RKM-C042.md), [Plan Role Term](RKM-C046.md), [Responsibility Role Term](RKM-C059.md), [Analysis State Term](RKM-C060.md), [Workflow State Term](RKM-C061.md)

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Rebuildable source recipe](../../issue93-generalization-sets/build_candidate.py) · [Export contract](../../issue93-export-contract/input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
