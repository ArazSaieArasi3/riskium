# Evidence Reference

**Source ID:** `RKM-C065` · **Subdomain:** [D09 · Risk Evidence](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A qualified reference linking a claim or activity to an evidence item, with its intended evidential role and provenance.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-68` | outgoing `supportsRecordedArtifact` | [Information Artifact](RKM-C014.md) | 0..* → 1..* |
| `R-69` | outgoing `refersToOccurrence` | [Risk Occurrence](RKM-C004.md) | 0..* → 0..* |
| `R-70` | outgoing `refersToAgent` | [Agent](RKM-C047.md) | 0..* → 0..* |
| `R-71` | outgoing `refersToAssessmentActivity` | [Assessment Activity](RKM-C031.md) | 0..* → 0..* |
| `R-72` | outgoing `refersToTreatmentActivity` | [Treatment Activity](RKM-C044.md) | 0..* → 0..* |
| `RX-021` | outgoing `pointsToEvidence` | [Evidence Item](RKM-C066.md) | 1..* → 1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** Provenance links can support traceability; a derivation does not define an evidence role, entail claim truth or establish independent corroboration.

### prov:Derivation

**External source definition (paraphrase):** Entity-to-entity transformation, construction or updating represented as a qualified influence.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.3, Derivation](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Derivation). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
