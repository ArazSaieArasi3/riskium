# Workflow Scheme Version

**Source ID:** `RKM-C063` · **Subdomain:** [D08 · Risk Workflow](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An issued version of a scheme defining workflow values and permitted transitions.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Artifact Version](RKM-C015.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-021` | incoming `availableInWorkflowScheme` | [Workflow State Term](RKM-C061.md) | 0..* → 1..* |
| `RX-030` | incoming `underSchemeVersion` | [Workflow Assignment](RKM-C064.md) | 0..* → 1 |

Generalizes: [Artifact Version](RKM-C015.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `CONTRAST` · reviewed 2026-11-05.

**Authored comparison:** A version of a workflow scheme defines transitions; SKOS scheme aggregation and a PROV revision derivation supply neither those transitions nor authorization rules.

### skos:ConceptScheme

**External source definition (paraphrase):** An organization of concepts; a scheme need not be an OWL ontology.

**Source:** SKOS Simple Knowledge Organization System Reference. W3C Recommendation, 18 August 2009. [§4, especially §§4.1 and 4.6.2](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#schemes). Accessed 2026-11-05.

**Inspected scope:** Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.

### prov:Revision

**External source definition (paraphrase):** A qualified derivation whose result revises an original while retaining substantial content.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.3, Revision](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Revision). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
