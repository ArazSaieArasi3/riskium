# Authorizing Agent Role

**Source ID:** `RKM-C054` · **Subdomain:** [D07 · Risk Responsibility](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A context-dependent role borne by an agent authorized to approve or issue a specified decision or assignment.

## Identity and modeling

- OntoUML stereotype: `roleMixin`; abstract: `true`.
- Identity supplier: `None`.
- Identity basis: Inherits bearer identity; role membership depends on an explicit responsibility or evidential context.
- Typing rationale: Anti-rigid contextual classification. Role mixins aggregate person and organization bearers without supplying identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-57` | incoming `mediatesAuthority` | [Responsibility Relator](RKM-C052.md) | 1..* → 1 |

Generalizes: [Agent](RKM-C047.md).  
Specialized by: [Authorizing Person](RKM-C057.md), [Authorizing Organization](RKM-C058.md).

## External definition and alignment status

**Documentary disposition:** `ANALOGY` · reviewed 2026-11-05.

**Authored comparison:** Approval/issue authority is Riskium-specific; a provenance role or participation does not by itself establish authorization.

### prov:Role

**External source definition (paraphrase):** A function in an activity-qualified provenance context.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.3, Role](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Role). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

### prov:Association

**External source definition (paraphrase):** An agent’s responsibility and role in an activity, optionally qualified by a plan.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.3, Association](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Association). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
