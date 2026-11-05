# Risk Occurrence

**Source ID:** `RKM-C004` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An actual occurrence or change relevant to a risk scenario; a scenario or report alone does not establish that it happened.

## Identity and modeling

- OntoUML stereotype: `event`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: An actual happening individuated by supported temporal extent, participants and occurrence boundaries.
- Typing rationale: Event interpretation; a description, plan or possibility is not an event instance.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-25` | incoming `mayBeRealizedBy` | [Risk Scenario Specification](RKM-C003.md) | 0..* → 0..* |
| `R-69` | incoming `refersToOccurrence` | [Evidence Reference](RKM-C065.md) | 0..* → 0..* |
| `RK2-005` | outgoing `initiatedBy` | [Trigger](RKM-C009.md) | 0..* → 0..* |
| `RK2-006` | outgoing `hasEstablishedConsequence` | [Consequence](RKM-C010.md) | 0..* → 0..* |

Generalizes: none recorded.  
Specialized by: [Trigger](RKM-C009.md).

## External definition and alignment status

**Documentary disposition:** `CONTRAST` · reviewed 2026-11-05.

**Authored comparison:** NIST permits a potential event or situation; Riskium Occurrence requires an actual occurrence, so the source term cannot establish realization.

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
