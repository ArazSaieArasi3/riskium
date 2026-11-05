# Risk Nature Assertion

**Source ID:** `RKM-C005` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A source-qualified information assertion that possible or reported effects are favorable, unfavorable or mixed relative to identified objectives and context.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-41` | outgoing `natureOf` | [Risk Case](RKM-X01.md) | 0..* → 1 |
| `R-42` | outgoing `declaresNature` | [Nature Term](RKM-C006.md) | 0..* → 1 |
| `R-43` | outgoing `natureInContext` | [Risk Context Specification](RKM-C002.md) | 0..* → 0..1 |
| `R-44` | incoming `recordsNature` | [Entry Revision](RKM-C023.md) | 1..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** Risk nature is an objective-relative source claim; a classification motivation alone supplies neither favorable/unfavorable meaning nor truth.

### oa:classifying

**External source definition (paraphrase):** A motivation for classifying a target.

**Source:** Web Annotation Data Model. W3C Recommendation, 23 February 2017. [§3.3.5, motivation classifying](https://www.w3.org/TR/2017/REC-annotation-model-20170223/#motivation-and-purpose). Accessed 2026-11-05.

**Inspected scope:** Selected motivations and annotation/body distinction only; no serialization conformance asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
