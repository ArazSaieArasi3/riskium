# Observation Result

**Source ID:** `RKM-C068` · **Subdomain:** [D10 · Risk Monitoring](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An information result produced by an observation activity, qualified by subject, time, method and available units.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-017` | incoming `recordsObservation` | [Entry Revision](RKM-C023.md) | 0..* → 0..* |
| `RK2-026` | outgoing `observationContext` | [Risk Context Specification](RKM-C002.md) | 0..* → 0..1 |
| `RX-022` | incoming `producesObservation` | [Observation Activity](RKM-C067.md) | 1 → 0..* |
| `RX-023` | outgoing `reportsIndicator` | [Indicator](RKM-C069.md) | 0..* → 1 |
| `RX-024` | outgoing `observesCase` | [Risk Case](RKM-X01.md) | 0..* → 1 |
| `RX-026` | incoming `basedOnObservation` | [Signal](RKM-C071.md) | 0..* → 1..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** SOSA Result includes actuation and sampling outputs too; Riskium selects observation information and adds explicit interpretation context.

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
