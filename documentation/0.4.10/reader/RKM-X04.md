# Risk Evaluation Outcome

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

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

## Current documentary comparisons

**Disposition:** `CONTRAST` · reviewed 2026-11-10.

Retain the distinction between a criteria-based significance/acceptability judgment and a DQV metric result. This is a difference of intended role, not a global disjointness claim between external and local classes.

RX-011 identifies the case, RX-012 requires assessment information and RX-013 pins a criteria ArtifactVersion. C-25 governs the versioned target. A numeric score alone does not establish acceptability or a treatment decision; revised case and version neighbors were reviewed.

### dqv:QualityMeasurement

**Selected source meaning (paraphrase):** Evaluation of a dataset or distribution against a quality metric.

**Source and locator:** [Data on the Web Best Practices: Data Quality Vocabulary](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/), W3C Working Group Note, 15 December 2016; [§4.1](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/#dqv:QualityMeasurement). Inspected 2026-11-10.

**Inspected scope:** Dataset-quality vocabulary used by analogy only. This Note is work in progress, not a W3C Recommendation.

**Review role:** Assistant-supported primary-passage comparison, current ancestry/neighbor/set-policy and selected assessment source-contract checks; not an instance or independent expert evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-04/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
