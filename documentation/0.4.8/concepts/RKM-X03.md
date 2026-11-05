# Uncertainty Statement

**Source ID:** `RKM-X03` · **Subdomain:** [D05 · Risk Assessment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A managed statement of what is uncertain about a risk case, including assumptions and evidential limitations; it does not imply a numerical probability.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-012` | outgoing `uncertaintyContext` | [Risk Context Specification](RKM-C002.md) | 0..* → 0..1 |
| `RK2-013` | incoming `recordsUncertainty` | [Assessment Information](RKM-C032.md) | 0..* → 0..* |
| `RX-004` | outgoing `uncertaintyAbout` | [Risk Case](RKM-X01.md) | 0..* → 1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** An annotation can express uncertainty context, but supplies no probability or evidence-strength semantics; Riskium preserves the authored statement and its limitations.

### oa:Annotation

**External source definition (paraphrase):** An association involving body and target resources.

**Source:** Web Annotation Data Model. W3C Recommendation, 23 February 2017. [§3.1](https://www.w3.org/TR/2017/REC-annotation-model-20170223/#annotations). Accessed 2026-11-05.

**Inspected scope:** Selected motivations and annotation/body distinction only; no serialization conformance asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
