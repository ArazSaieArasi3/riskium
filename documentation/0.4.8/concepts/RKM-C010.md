# Consequence

**Source ID:** `RKM-C010` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `OPTIONAL_PHENOMENON_BOUNDARY`

## Current authored definition

An outcome relevant to objectives, considered as a referent distinct from a statement about it. Outcomes can have different ontological categories; no universal event or object stereotype is asserted.

## Identity and modeling

- OntoUML stereotype: `None`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: Bearer-specific; no uniform identity principle over objects, events, situations and aspects.
- Typing rationale: Broad domain notion retained in the catalog and optional external bridge; no uniform native OntoUML class asserted.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-006` | incoming `hasEstablishedConsequence` | [Risk Occurrence](RKM-C004.md) | 0..* → 0..* |
| `RX-010` | incoming `refersToActualOutcome` | [Consequence Statement](RKM-C025.md) | 0..* → 0..1 |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `NO_DIRECT_EQUIVALENT_REVIEWED` · reviewed 2026-11-05.

**Authored comparison:** A potentially harmful event is not its consequence. No direct definition for Riskium’s cross-category outcome boundary is adopted from this inspected entry.

### Threat Event

**External source definition (paraphrase):** An event or situation with potential adverse consequences.

**Source:** Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1. September 2012; DOI 10.6028/NIST.SP.800-30r1. [Appendix B, printed B-13, PDF page 63](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=63). Accessed 2026-11-05.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
