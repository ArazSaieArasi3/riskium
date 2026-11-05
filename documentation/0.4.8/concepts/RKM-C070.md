# Threshold

**Source ID:** `RKM-C070` · **Subdomain:** [D10 · Risk Monitoring](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A versioned information specification of a context-qualified decision boundary for an indicator or assessment scale, with a comparator, permissible value interpretation and applicability context.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-020` | outgoing `thresholdOnScale` | [Assessment Scale](RKM-C036.md) | 0..* → 0..1 |
| `RX-025` | outgoing `thresholdForIndicator` | [Indicator](RKM-C069.md) | 0..* → 0..1 |
| `RX-027` | incoming `evaluatedAgainstThreshold` | [Signal](RKM-C071.md) | 0..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `NO_DIRECT_EQUIVALENT_REVIEWED` · reviewed 2026-11-05.

**Authored comparison:** A measuring standard is not a comparator-qualified decision boundary. No direct threshold equivalent is adopted from the inspected DQV entry.

### dqv:Metric

**External source definition (paraphrase):** A standard for measuring a quality dimension; a measurement provides its observed value.

**Source:** Data on the Web Best Practices: Data Quality Vocabulary. W3C Working Group Note, 15 December 2016. [§4.2](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/#dqv:Metric). Accessed 2026-11-05.

**Inspected scope:** Dataset-quality vocabulary used by analogy only. This Note is work in progress, not a W3C Recommendation.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
