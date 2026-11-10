# Risk Score Result

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C037`; **source title:** `RiskScoreResult`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D05 · Risk Assessment](Subdomains.md#d05)

## Authored source definition

A numeric assessment output produced under a declared scoring method; it is not the risk itself or a universal definition of risk level.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-17 | incoming `hasScoreResult` | [Assessment Information](RKM-C032.md) | 1 | 0..* | FORMAL_CORE |
| R-18 | outgoing `derivedFrom` | [Dimension Assessment Result](RKM-C034.md) | 0..* | 0..* | FORMAL_CORE |
| R-50 | outgoing `scoreMethod` | [Assessment Method Specification](RKM-C035.md) | 0..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `ANALOGY` · reviewed 2026-11-10.

Retain metric-qualified output as a DQV pattern analogy without equating dataset quality with risk. A recorded numeric output is neither the RiskCase nor an acceptability decision.

R-50 requires a score method; R-18 permits zero or many component links for reported scores. C-21 separately requires declared components, a pinned method and adequate inputs for a computed score. C-18 preserves missing data as missing and does not certify a reported number as reproducible.

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
