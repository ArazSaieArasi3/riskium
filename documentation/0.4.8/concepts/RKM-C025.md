# Consequence Statement

**Source ID:** `RKM-C025` · **Subdomain:** [D04 · Risk Registration](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An information item expressing a possible or reported consequence; it is not the consequence itself.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-22` | outgoing `statementAbout` | [Risk Case](RKM-X01.md) | 0..* → 1 |
| `R-38` | incoming `recordsConsequence` | [Entry Revision](RKM-C023.md) | 1 → 0..* |
| `R-40` | outgoing `sourceSlot` | [Consequence Slot Term](RKM-C029.md) | 0..* → 1 |
| `RX-009` | incoming `hasPossibleConsequenceStatement` | [Risk Scenario Specification](RKM-C003.md) | 0..* → 0..* |
| `RX-010` | outgoing `refersToActualOutcome` | [Consequence](RKM-C010.md) | 0..* → 0..1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** Descriptive content about an outcome does not create that outcome; the source motivation does not supply consequence semantics.

### oa:describing

**External source definition (paraphrase):** A motivation for describing a target.

**Source:** Web Annotation Data Model. W3C Recommendation, 23 February 2017. [§3.3.5, motivation describing](https://www.w3.org/TR/2017/REC-annotation-model-20170223/#motivation-and-purpose). Accessed 2026-11-05.

**Inspected scope:** Selected motivations and annotation/body distinction only; no serialization conformance asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
