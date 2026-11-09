# Responsibility Relator

Candidate **0.3.2-case.1**; not the published current dictionary. Source SHA-256: `e98a63b286441c80fc10a9644804d64fc2b611e906b2d27cf3d72f3ebd72cfa8`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C052`; **source title:** `ResponsibilityRelator`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D07 · Risk Responsibility](Subdomains.md#d07)

## Authored source definition

A temporally qualified responsibility relationship connecting its participants, responsibility scope and grounding assignment.

## Identity and source typing

- OntoUML stereotype: `relator`; abstract: `false`.
- Identity supplier: [Responsibility Relator](RKM-C052.md)
- Identity basis: A grounded responsibility relationship with at least two distinct mediated individuals.
- Typing rationale: Relator proposal. Same actor at both named role ends is insufficient to establish two distinct participants; retain only assignment information until grounding is resolved.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-55 | incoming `documentsActualMandate` | [Responsibility Assignment Information](RKM-C051.md) | 0..* | 0..1 | FORMAL_CORE |
| R-56 | outgoing `mediatesBearer` | [Responsible Agent Role](RKM-C053.md) | 1..* | 1 | FORMAL_CORE |
| R-57 | outgoing `mediatesAuthority` | [Authorizing Agent Role](RKM-C054.md) | 1..* | 1 | FORMAL_CORE |
| R-58 | outgoing `mandateAbout` | [Risk Case](RKM-X01.md) | 0..* | 1..* | FORMAL_CORE |
| R-59 | outgoing `mandateRole` | [Responsibility Role Term](RKM-C059.md) | 0..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.  
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Rebuildable source recipe](../build_candidate.py) · [Export contract](../input-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
