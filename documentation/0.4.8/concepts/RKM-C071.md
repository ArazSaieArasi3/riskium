# Signal

**Source ID:** `RKM-C071` · **Subdomain:** [D10 · Risk Monitoring](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An information item indicating a potentially relevant change or condition and potentially prompting review; it does not by itself establish a risk event.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RX-026` | outgoing `basedOnObservation` | [Observation Result](RKM-C068.md) | 0..* → 1..* |
| `RX-027` | outgoing `evaluatedAgainstThreshold` | [Threshold](RKM-C070.md) | 0..* → 0..* |
| `RX-028` | outgoing `promptsReviewOf` | [Risk Case](RKM-X01.md) | 0..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** An informative signal may arise from results, but is not automatically an observation result or proof of a risk event.

### sosa:Result

**External source definition (paraphrase):** A result of observation, actuation or sampling; simple values have a separate property.

**Source:** Semantic Sensor Network Ontology. W3C Recommendation, 19 October 2017; SOSA/SSN. [§4.7.2.1](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/#SOSAResult). Accessed 2026-11-05.

**Inspected scope:** Selected core classes only; observed properties and their specifications remain distinct.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
