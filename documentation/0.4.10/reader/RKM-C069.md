# Indicator

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C069`; **source title:** `Indicator`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D10 · Risk Monitoring](Subdomains.md#d10)

## Authored source definition

A versioned information specification of an observable or computed indicator, including its intended interpretation. A reported indicator value is an ObservationResult, not the specification.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RX-023 | incoming `reportsIndicator` | [Observation Result](RKM-C068.md) | 0..* | 1 | FORMAL_CORE |
| RX-025 | incoming `thresholdForIndicator` | [Threshold](RKM-C070.md) | 0..* | 0..1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `ANALOGY` · reviewed 2026-11-10.

Retain DQV Metric and SOSA ObservableProperty as bounded pattern comparisons. DQV concerns dataset quality; SOSA describes an observable feature quality. Riskium Indicator is an information specification, distinct from the property and its measured value.

RX-023 links reported results to their indicator specification; RX-025 can anchor a threshold. Specification versions and interpretation remain documentary. Neither external property classes nor DQV domain constraints are automatically imported into Riskium.

### dqv:Metric

**Selected source meaning (paraphrase):** A standard for measuring a quality dimension; a measurement provides its observed value.

**Source and locator:** [Data on the Web Best Practices: Data Quality Vocabulary](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/), W3C Working Group Note, 15 December 2016; [§4.2](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/#dqv:Metric). Inspected 2026-11-10.

**Inspected scope:** Dataset-quality vocabulary used by analogy only. This Note is work in progress, not a W3C Recommendation.

### sosa:ObservableProperty

**Selected source meaning (paraphrase):** An observable quality of a feature, rather than a specification describing that quality.

**Source and locator:** [Semantic Sensor Network Ontology](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/), W3C Recommendation, 19 October 2017; SOSA/SSN; [§4.3.2.1](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/#SOSAObservableProperty). Inspected 2026-11-10.

**Inspected scope:** Selected core classes only; observed properties and their specifications remain distinct.

**Review role:** Assistant-supported source comparison, current ancestry/neighbor/set-policy and selected evidence/monitoring contracts; not a new engine, instance or independent expert evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-06/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
