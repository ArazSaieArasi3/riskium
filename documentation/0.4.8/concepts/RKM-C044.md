# Treatment Activity

**Source ID:** `RKM-C044` · **Subdomain:** [D06 · Risk Treatment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

An actual performance of actions intended to modify or otherwise respond to risk, distinct from the plan describing them.

## Identity and modeling

- OntoUML stereotype: `event`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: An actual happening individuated by supported temporal extent, participants and occurrence boundaries.
- Typing rationale: Event interpretation; a description, plan or possibility is not an event instance.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-64` | outgoing `executesPlan` | [Plan Specification](RKM-C043.md) | 0..* → 0..* |
| `R-65` | outgoing `treatmentPerformer` | [Agent](RKM-C047.md) | 0..* → 0..* |
| `R-66` | outgoing `implementsControl` | [Risk Control](RKM-C045.md) | 0..* → 0..* |
| `R-72` | incoming `refersToTreatmentActivity` | [Evidence Reference](RKM-C065.md) | 0..* → 0..* |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `ANALOGY` · reviewed 2026-11-05.

**Authored comparison:** Actual treatment performance relates to security response actions but is general in domain; a plan does not prove performance or effectiveness.

### Risk Response

**External source definition (paraphrase):** Accepting, avoiding, mitigating, sharing or transferring risk.

**Source:** Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1. September 2012; DOI 10.6028/NIST.SP.800-30r1. [Appendix B, printed B-10, PDF page 60; attributed there to SP 800-39](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=60). Accessed 2026-11-05.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

### prov:Activity

**External source definition (paraphrase):** An occurrence over time acting on or with entities.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.1, Activity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Activity). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
