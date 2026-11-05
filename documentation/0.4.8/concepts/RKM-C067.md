# Observation Activity

**Source ID:** `RKM-C067` · **Subdomain:** [D10 · Risk Monitoring](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An activity that observes a stated feature of a subject using a declared procedure and temporal context.

## Identity and modeling

- OntoUML stereotype: `event`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: An actual happening individuated by supported temporal extent, participants and occurrence boundaries.
- Typing rationale: Event interpretation; a description, plan or possibility is not an event instance.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RX-022` | outgoing `producesObservation` | [Observation Result](RKM-C068.md) | 1 → 0..* |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** The procedure/feature/value separation informs observations; Riskium’s subject, time and procedure qualification remains its own profile.

### sosa:Observation

**External source definition (paraphrase):** An act following a procedure to estimate or calculate a feature property’s value.

**Source:** Semantic Sensor Network Ontology. W3C Recommendation, 19 October 2017; SOSA/SSN. [§4.3.2.2](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/#SOSAObservation). Accessed 2026-11-05.

**Inspected scope:** Selected core classes only; observed properties and their specifications remain distinct.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
