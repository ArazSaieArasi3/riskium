# Treatment Activity

Selected scientific source **0.3.2** for package **v0.3.9**; publication has not yet occurred. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C044`; **source title:** `TreatmentActivity`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D06 · Risk Treatment](Subdomains.md#d06)

## Authored source definition

An actual performance of actions intended to modify or otherwise respond to risk, distinct from the plan describing them.

## Identity and source typing

- OntoUML stereotype: `event`; abstract: `false`.
- Identity supplier: No identity supplier is assigned in this source record.
- Identity basis: An actual happening individuated by supported temporal extent, participants and occurrence boundaries.
- Typing rationale: Event interpretation; a description, plan or possibility is not an event instance.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-64 | outgoing `executesPlan` | [Plan Specification](RKM-C043.md) | 0..* | 0..* | FORMAL_CORE |
| R-65 | outgoing `treatmentPerformer` | [Agent](RKM-C047.md) | 0..* | 0..* | FORMAL_CORE |
| R-66 | outgoing `implementsControl` | [Risk Control](RKM-C045.md) | 0..* | 0..* | OPTIONAL_EXTERNAL_BRIDGE |
| R-72 | incoming `refersToTreatmentActivity` | [Evidence Reference](RKM-C065.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.<br>
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
