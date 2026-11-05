# Responsibility Assignment Information

**Source ID:** `RKM-C051` · **Subdomain:** [D07 · Risk Responsibility](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A recorded statement about an assignment of responsibility or authority, distinct from the relationship it asserts.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-09` | outgoing `assignmentAbout` | [Risk Case](RKM-X01.md) | 0..* → 1 |
| `R-10` | outgoing `hasBearerReference` | [Actor Reference](RKM-C050.md) | 0..* → 1 |
| `R-30` | incoming `documentsAssignment` | [Entry Revision](RKM-C023.md) | 1..* → 0..* |
| `R-54` | outgoing `assignmentRole` | [Responsibility Role Term](RKM-C059.md) | 0..* → 1 |
| `R-55` | outgoing `documentsActualMandate` | [Responsibility Relator](RKM-C052.md) | 0..* → 0..1 |
| `RK2-025` | outgoing `authorizerReference` | [Actor Reference](RKM-C050.md) | 0..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `CONTRAST` · reviewed 2026-11-05.

**Authored comparison:** PROV Association attributes responsibility within an activity; Riskium Assignment Information records a claim whose grounding may remain unsupported.

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
