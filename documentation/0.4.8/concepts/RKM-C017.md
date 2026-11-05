# Vocabulary Concept

**Source ID:** `RKM-C017` · **Subdomain:** [D03 · Risk Classification](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A managed terminological information artifact that identifies a vocabulary meaning independently of its labels. It is a vocabulary resource, not automatically a domain universal or the real-world entity denoted.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| — | No direct catalog association | — | — |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: [Classification Term](RKM-C019.md), [Assessment Scale Level](RKM-C038.md), [Assessment Dimension](RKM-C039.md).

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** SKOS separates vocabulary notions from their labels and from OWL classes; Riskium additionally manages the documentary resource’s identity.

### skos:Concept

**External source definition (paraphrase):** A knowledge-organization notion; using it does not automatically identify an OWL class.

**Source:** SKOS Simple Knowledge Organization System Reference. W3C Recommendation, 18 August 2009. [§3, especially §§3.1 and 3.5.1](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#concepts). Accessed 2026-11-05.

**Inspected scope:** Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.

### Lexical labels

**External source definition (paraphrase):** A natural-language string associated with a resource, distinct from the resource.

**Source:** SKOS Simple Knowledge Organization System Reference. W3C Recommendation, 18 August 2009. [§5.1](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#labels). Accessed 2026-11-05.

**Inspected scope:** Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
