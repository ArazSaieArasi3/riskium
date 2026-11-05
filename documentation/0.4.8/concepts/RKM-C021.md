# Tag

**Source ID:** `RKM-C021` · **Subdomain:** [D03 · Risk Classification](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A managed annotation artifact carrying a lightweight label. Identical lexical labels do not by themselves identify one tag assignment or imply a formal taxonomy.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-24` | incoming `hasTag` | [Entry Revision](RKM-C023.md) | 0..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** The tagging motivation and its lexical content inform use; the Riskium tag artifact and any assignment still require explicit identities.

### oa:tagging

**External source definition (paraphrase):** A motivation for attaching a tag to a target.

**Source:** Web Annotation Data Model. W3C Recommendation, 23 February 2017. [§3.3.5, motivation tagging](https://www.w3.org/TR/2017/REC-annotation-model-20170223/#motivation-and-purpose). Accessed 2026-11-05.

**Inspected scope:** Selected motivations and annotation/body distinction only; no serialization conformance asserted.

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
