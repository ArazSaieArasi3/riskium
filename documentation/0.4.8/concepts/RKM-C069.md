# Indicator

**Source ID:** `RKM-C069` · **Subdomain:** [D10 · Risk Monitoring](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A versioned information specification of an observable or computed indicator, including its intended interpretation. A reported indicator value is an ObservationResult, not the specification.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RX-023` | incoming `reportsIndicator` | [Observation Result](RKM-C068.md) | 0..* → 1 |
| `RX-025` | incoming `thresholdForIndicator` | [Threshold](RKM-C070.md) | 0..* → 0..1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `ANALOGY` · reviewed 2026-11-05.

**Authored comparison:** The indicator is a versioned information specification; it is neither SOSA’s observable property nor a DQV dataset-quality metric as such.

### dqv:Metric

**External source definition (paraphrase):** A standard for measuring a quality dimension; a measurement provides its observed value.

**Source:** Data on the Web Best Practices: Data Quality Vocabulary. W3C Working Group Note, 15 December 2016. [§4.2](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/#dqv:Metric). Accessed 2026-11-05.

**Inspected scope:** Dataset-quality vocabulary used by analogy only. This Note is work in progress, not a W3C Recommendation.

### sosa:ObservableProperty

**External source definition (paraphrase):** An observable quality of a feature, rather than a specification describing that quality.

**Source:** Semantic Sensor Network Ontology. W3C Recommendation, 19 October 2017; SOSA/SSN. [§4.3.2.1](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/#SOSAObservableProperty). Accessed 2026-11-05.

**Inspected scope:** Selected core classes only; observed properties and their specifications remain distinct.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
