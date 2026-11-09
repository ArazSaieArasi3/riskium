# Agent

Selected scientific source **0.3.2** for package **v0.3.9**; publication has not yet occurred. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

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

Direct supertypes: None recorded.<br>
Direct subtypes: [Person](RKM-C048.md), [Organization](RKM-C049.md), [Responsible Agent Role](RKM-C053.md), [Authorizing Agent Role](RKM-C054.md)

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Selected integration interpretation](../../../evaluation/manuscript-review/v7.2.3/issue93-integration/definitions/RKM-C047.md) preserves the separate candidate design decision.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
