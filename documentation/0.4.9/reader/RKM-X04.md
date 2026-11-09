# Risk Evaluation Outcome

Selected scientific source **0.3.2** for package **v0.3.9**; publication has not yet occurred. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-X04`; **source title:** `RiskEvaluationOutcome`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D05 · Risk Assessment](Subdomains.md#d05)

## Authored source definition

A recorded judgment of risk significance or acceptability based on identified assessment information and criteria versions. It is distinct from a numeric score and from the evaluation activity.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RK2-014 | incoming `basedOnEvaluation` | [Treatment Decision Information](RKM-C041.md) | 0..* | 0..* | FORMAL_CORE |
| RX-011 | outgoing `evaluatesCase` | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| RX-012 | outgoing `usesAssessment` | [Assessment Information](RKM-C032.md) | 0..* | 1..* | FORMAL_CORE |
| RX-013 | outgoing `usesCriteriaVersion` | [Artifact Version](RKM-C015.md) | 0..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)
