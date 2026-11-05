# Risk Score Result

**Source ID:** `RKM-C037` · **Subdomain:** [D05 · Risk Assessment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A numeric assessment output produced under a declared scoring method; it is not the risk itself or a universal definition of risk level.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-17` | incoming `hasScoreResult` | [Assessment Information](RKM-C032.md) | 1 → 0..* |
| `R-18` | outgoing `derivedFrom` | [Dimension Assessment Result](RKM-C034.md) | 0..* → 0..* |
| `R-50` | outgoing `scoreMethod` | [Assessment Method Specification](RKM-C035.md) | 0..* → 1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `ANALOGY` · reviewed 2026-11-05.

**Authored comparison:** A metric-qualified output illustrates how to document a score; Riskium’s numeric risk output is not dataset quality or the risk itself.

### dqv:QualityMeasurement

**External source definition (paraphrase):** Evaluation of a dataset or distribution against a quality metric.

**Source:** Data on the Web Best Practices: Data Quality Vocabulary. W3C Working Group Note, 15 December 2016. [§4.1](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/#dqv:QualityMeasurement). Accessed 2026-11-05.

**Inspected scope:** Dataset-quality vocabulary used by analogy only. This Note is work in progress, not a W3C Recommendation.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
