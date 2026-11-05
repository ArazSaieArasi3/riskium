# Risk Register Entry

**Source ID:** `RKM-C022` · **Subdomain:** [D04 · Risk Registration](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A managed register record about exactly one RiskCase in this profile. Distinct entries, source systems or registers can record the same case. A software record is an implementation record, not an additional risk subject.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-01` | outgoing `recordsAbout` | [Risk Case](RKM-X01.md) | 0..* → 1 |
| `R-33` | incoming `revisionOf` | [Entry Revision](RKM-C023.md) | 0..* → 1 |
| `RX-008` | outgoing `memberOfRegister` | [Risk Register](RKM-C030.md) | 0..* → 1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** The record is a documentary entity about one case in this profile; PROV Entity neither imposes that cardinality nor identifies the case with its entry.

### prov:Entity

**External source definition (paraphrase):** A thing considered through fixed aspects, including conceptual or imaginary things.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.1, Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
