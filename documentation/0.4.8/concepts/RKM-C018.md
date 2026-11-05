# Classification Scheme

**Source ID:** `RKM-C018` · **Subdomain:** [D03 · Risk Classification](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A governed organization of classification concepts with an identified scope and version policy.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-05` | incoming `belongsToScheme` | [Classification Term](RKM-C019.md) | 0..* → 1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** ConceptScheme informs vocabulary organization; Riskium adds scope and governance/version policies without asserting identical extension.

### skos:ConceptScheme

**External source definition (paraphrase):** An organization of concepts; a scheme need not be an OWL ontology.

**Source:** SKOS Simple Knowledge Organization System Reference. W3C Recommendation, 18 August 2009. [§4, especially §§4.1 and 4.6.2](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#schemes). Accessed 2026-11-05.

**Inspected scope:** Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
