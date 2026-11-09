# Treatment Decision Information

Selected scientific source **0.3.2** for package **v0.3.9**; publication has not yet occurred. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C041`; **source title:** `TreatmentDecisionInformation`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D06 · Risk Treatment](Subdomains.md#d06)

## Authored source definition

A recorded decision about treating risk, including the selected option, rationale, responsible authority and relevant basis.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-19 | outgoing `decisionAbout` | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-20 | outgoing `selectsStrategy` | [Treatment Strategy Term](RKM-C042.md) | 0..* | 1 | FORMAL_CORE |
| R-60 | incoming `recordsDecision` | [Entry Revision](RKM-C023.md) | 1..* | 0..* | FORMAL_CORE |
| R-63 | outgoing `isSpecifiedByPlan` | [Plan Specification](RKM-C043.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-014 | outgoing `basedOnEvaluation` | [Risk Evaluation Outcome](RKM-X04.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-015 | outgoing `recordsRemainingRiskAssessment` | [Assessment Information](RKM-C032.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
