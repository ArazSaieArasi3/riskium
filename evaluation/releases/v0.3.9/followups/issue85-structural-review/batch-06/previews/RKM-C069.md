# Indicator — N3b-6 documentary preview

**Planning preview; not deployed or independently validated.**

## Authored definition, unchanged

A versioned information specification of an observable or computed indicator, including its intended interpretation. A reported indicator value is an ObservationResult, not the specification.

[Source model 0.3.2](https://github.com/ArazSaieArasi3/riskium/blob/36ff7a55becfe206b821fe969fecd5efbcd22149/ontology/0.3.2/riskium-model.json); subdomain D10; stereotype subkind; identity supplier RKM-C014.

Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.

Authored verification status, preserved verbatim: Bounded review and finite tests; native OntoUML and independent semantic validation pending

Later bounded qualification/publication evidence is in the [v0.3.9 receipt](https://github.com/ArazSaieArasi3/riskium/blob/36ff7a55becfe206b821fe969fecd5efbcd22149/evaluation/releases/v0.3.9/R2b-outcome.md). Source labels and documentary comparisons are not independent semantic ratings.

## Documentary comparison

**ANALOGY → ANALOGY**.

Retain DQV Metric and SOSA ObservableProperty as bounded pattern comparisons. DQV concerns dataset quality; SOSA describes an observable feature quality. Riskium Indicator is an information specification, distinct from the property and its measured value.

| Selected term | Source kind and locator |
|---|---|
| [dqv:Metric](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/#dqv:Metric) | DATASET_QUALITY_PATTERN_CLASS; §4.2 |
| [sosa:ObservableProperty](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/#SOSAObservableProperty) | OBSERVABLE_PROPERTY_CLASS; §4.3.2.1 |

## Current structural context

RX-023 links reported results to their indicator specification; RX-025 can anchor a threshold. Specification versions and interpretation remain documentary. Neither external property classes nor DQV domain constraints are automatically imported into Riskium.

Source continuity: concept record unchanged=True; local association/generalization records unchanged=True; inherited edges unchanged=True. Ancestor and neighbor changes are reported separately.

| Observation | Source-bound result |
|---|---|
| Inheritance path | GX-055: RKM-C069 → RKM-C014 |
| Source constraint route | C-03, C-04, C-11, C-18 — [selected source statements](../evidence-monitoring-checks.json) |
| Changed ancestor | RKM-C014: typing_rationale |
| Changed relation neighbor | None in this selected context |
| Excluded blanket sets | GS-RKM-C014 |

Reference, role participation and evidence-use relationship remain distinct; a citation or provenance link is not proof of claim truth. Observation information and indicator specifications do not create actual risk events. Thresholds use supported indicator/scale semantics, and signals preserve context and uncertainty without inventing missing values.

Complete source observations are in [contexts.json](../contexts.json). Context SHA-256: `6a685d05fb4f2bd34259ed9be93e2df2c0451e08fa53271640828eaf752cf5b3`.

Authored definition SHA-256: `ec765e03e516ea9a295473eaf70893bfac0ab473f0602459a31acc03de53e589`.

No formal alignment axiom, new ontology-engine execution or independent expert rating is supplied. Documentary batch accounting is complete; full component qualification and actual publication/readback retain their separate gates. #23 and #78 remain separate.
