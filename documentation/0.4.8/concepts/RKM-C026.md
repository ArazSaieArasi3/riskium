# Identification Information

**Source ID:** `RKM-C026` · **Subdomain:** [D04 · Risk Registration](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

Recorded information about identifying a risk, including the stated source, channel, agent and available time information.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-07` | outgoing `identifiedRisk` | [Risk Case](RKM-X01.md) | 0..* → 1 |
| `R-08` | outgoing `hasParticipantReference` | [Actor Reference](RKM-C050.md) | 0..* → 0..* |
| `R-27` | outgoing `declaresIntakeChannel` | [Intake Channel Term](RKM-C027.md) | 0..* → 0..* |
| `R-52` | incoming `recordsIdentification` | [Entry Revision](RKM-C023.md) | 1..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** Entity-to-agent attribution can document one part of identification provenance; it is not the full recorded identification, channel or time information.

### prov:Attribution

**External source definition (paraphrase):** Ascription of an entity to an agent.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.3, Attribution](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Attribution). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
