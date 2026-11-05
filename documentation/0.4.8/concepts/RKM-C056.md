# Responsible Organization

**Source ID:** `RKM-C056` · **Subdomain:** [D07 · Risk Responsibility](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An organization bearing a responsible-agent role in a specified assignment context.

## Identity and modeling

- OntoUML stereotype: `role`; abstract: `false`.
- Identity supplier: [Organization](RKM-C049.md).
- Identity basis: Inherits bearer identity; role membership depends on an explicit responsibility or evidential context.
- Typing rationale: Anti-rigid contextual classification. Role mixins aggregate person and organization bearers without supplying identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| — | No direct catalog association | — | — |

Generalizes: [Organization](RKM-C049.md), [Responsible Agent Role](RKM-C053.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `ANALOGY` · reviewed 2026-11-05.

**Authored comparison:** Being an organization plus a provenance function does not establish the grounded responsible-organization role.

### prov:Organization

**External source definition (paraphrase):** A social or legal institution considered as an agent.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.2, Organization](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Organization). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

### prov:Role

**External source definition (paraphrase):** A function in an activity-qualified provenance context.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.3, Role](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Role). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
