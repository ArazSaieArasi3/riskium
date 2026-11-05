# Assessment Dimension

**Source ID:** `RKM-C039` · **Subdomain:** [D05 · Risk Assessment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A managed vocabulary resource specifying an assessment aspect, such as likelihood or consequence severity. The vocabulary item, the aspect denoted and its measured or judged value remain distinct.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-48` | incoming `dimension` | [Dimension Assessment Result](RKM-C034.md) | 0..* → 1 |
| `RK2-018` | incoming `specifiesDimension` | [Assessment Method Specification](RKM-C035.md) | 0..* → 0..* |
| `RK2-019` | incoming `scaleForDimension` | [Assessment Scale](RKM-C036.md) | 0..* → 1 |

Generalizes: [Vocabulary Concept](RKM-C017.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `ANALOGY` · reviewed 2026-11-05.

**Authored comparison:** DQV’s criterion is modeled as a SKOS concept; Riskium’s vocabulary aspect and its judged result remain distinct from dataset-quality criteria.

### dqv:Dimension

**External source definition (paraphrase):** A dataset-quality assessment criterion associated with one or more metrics.

**Source:** Data on the Web Best Practices: Data Quality Vocabulary. W3C Working Group Note, 15 December 2016. [§4.3](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/#dqv:Dimension). Accessed 2026-11-05.

**Inspected scope:** Dataset-quality vocabulary used by analogy only. This Note is work in progress, not a W3C Recommendation.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
