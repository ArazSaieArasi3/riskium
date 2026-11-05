# Risk State

**Source ID:** `RKM-C013` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A temporally qualified state of a risk-relevant situation, distinct from the workflow status of its record.

## Identity and modeling

- OntoUML stereotype: `situation`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: A time-qualified configuration whose participants and context must be evidenced.
- Typing rationale: Situation interpretation; neither a workflow label nor an assessment score is the situation itself.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-004` | incoming `hasEstablishedState` | [Risk Case](RKM-X01.md) | 0..* → 0..* |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `NO_DIRECT_EQUIVALENT_REVIEWED` · reviewed 2026-11-05.

**Authored comparison:** Considering fixed aspects of an entity does not define the temporal state of a risk situation; the risk-state/workflow distinction remains authored.

### prov:Entity

**External source definition (paraphrase):** A thing considered through fixed aspects, including conceptual or imaginary things.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.1, Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
