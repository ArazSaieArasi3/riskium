# Plan Specification

**Source ID:** `RKM-C043` · **Subdomain:** [D06 · Risk Treatment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A versioned specification of intended actions, resources, responsibilities, timing and conditions for a stated purpose.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-21` | outgoing `planAbout` | [Risk Case](RKM-X01.md) | 0..* → 1..* |
| `R-61` | incoming `recordsPlan` | [Entry Revision](RKM-C023.md) | 1..* → 0..* |
| `R-62` | outgoing `planRole` | [Plan Role Term](RKM-C046.md) | 0..* → 1 |
| `R-63` | incoming `isSpecifiedByPlan` | [Treatment Decision Information](RKM-C041.md) | 0..* → 0..* |
| `R-64` | incoming `executesPlan` | [Treatment Activity](RKM-C044.md) | 0..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `RELATED` · reviewed 2026-11-05.

**Authored comparison:** Intended actions toward a goal are relevant; Riskium adds versioned resources, responsibility, timing and conditions, without asserting full class equivalence.

### prov:Plan

**External source definition (paraphrase):** An entity representing intended steps toward agents’ goals.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.3, Plan](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Plan). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
