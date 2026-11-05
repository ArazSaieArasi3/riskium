# Exposure

**Source ID:** `RKM-C012` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A time-qualified situation relating an affected bearer to a risk source or relevant condition. An exposure score or its description is information about that situation.

## Identity and modeling

- OntoUML stereotype: `situation`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: A time-qualified configuration whose participants and context must be evidenced.
- Typing rationale: Situation interpretation; neither a workflow label nor an assessment score is the situation itself.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-003` | incoming `refersToExposure` | [Risk Context Specification](RKM-C002.md) | 0..* → 0..* |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `ANALOGY` · reviewed 2026-11-05.

**Authored comparison:** The source links exposure/susceptibility to conditions; Riskium’s timed bearer-to-source situation is a separate authored interpretation, not that note’s formal model.

### Susceptibility/exposure discussion

**External source definition (paraphrase):** Discusses susceptibility/exposure in relation to predisposing conditions.

**Source:** Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1. September 2012; DOI 10.6028/NIST.SP.800-30r1. [§2.3.1, footnote 27, printed page 10, PDF page 19](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=19). Accessed 2026-11-05.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
