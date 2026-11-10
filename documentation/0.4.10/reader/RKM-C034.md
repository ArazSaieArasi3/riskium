# Dimension Assessment Result

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C034`; **source title:** `DimensionAssessmentResult`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D05 · Risk Assessment](Subdomains.md#d05)

## Authored source definition

A result for one assessment dimension, qualified by its method, scale, basis and relevant temporal context.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-13 | incoming `hasDimensionResult` | [Assessment Information](RKM-C032.md) | 1 | 0..* | FORMAL_CORE |
| R-14 | outgoing `usesScale` | [Assessment Scale](RKM-C036.md) | 0..* | 0..1 | FORMAL_CORE |
| R-15 | outgoing `selectsLevel` | [Assessment Scale Level](RKM-C038.md) | 0..* | 0..1 | FORMAL_CORE |
| R-18 | incoming `derivedFrom` | [Risk Score Result](RKM-C037.md) | 0..* | 0..* | FORMAL_CORE |
| R-48 | outgoing `dimension` | [Assessment Dimension](RKM-C039.md) | 0..* | 1 | FORMAL_CORE |
| RX-016 | outgoing `usesScaleVersion` | [Artifact Version](RKM-C015.md) | 0..* | 0..1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `ANALOGY` · reviewed 2026-11-10.

Retain DQV measurement as a pattern analogy. DQV concerns dataset quality; Riskium records a risk-dimension result with its own interpretation dependencies. DQV types and domain restrictions are not imported.

R-48 identifies one dimension; R-14/R-15 and RX-016 retain optional scale, selected level and scale-version information. C-13/C-18 require compatible interpretation for comparison. The revised ArtifactVersion neighbor does not turn the result itself into a version or a measured real-world quality.

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
