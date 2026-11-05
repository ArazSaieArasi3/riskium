# Risk Control

**Source ID:** `RKM-C045` · **Subdomain:** [D06 · Risk Treatment](Subdomains.md) · **Layer:** `OPTIONAL_PHENOMENON_BOUNDARY`

## Current authored definition

A contextual measure intended to maintain or modify risk. A policy, device, practice or activity may serve as its bearer. Implementation and observed effectiveness are separate claims; one cross-category stereotype is not asserted.

## Identity and modeling

- OntoUML stereotype: `None`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: Bearer-specific; no uniform identity principle over objects, events, situations and aspects.
- Typing rationale: Broad domain notion retained in the catalog and optional external bridge; no uniform native OntoUML class asserted.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-66` | incoming `implementsControl` | [Treatment Activity](RKM-C044.md) | 0..* → 0..* |
| `R-67` | outgoing `controlAddressing` | [Risk Case](RKM-X01.md) | 0..* → 0..* |
| `RX-020` | incoming `resolvesToControl` | [Control Reference](RKM-X05.md) | 0..* → 0..1 |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `ANALOGY` · reviewed 2026-11-05.

**Authored comparison:** Security safeguards cover one use of risk control; Riskium permits cross-category contextual measures and separates implementation from effectiveness.

### Security Controls

**External source definition (paraphrase):** Safeguards protecting information and systems against security risks.

**Source:** Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1. September 2012; DOI 10.6028/NIST.SP.800-30r1. [Appendix B, printed B-11, PDF page 61; attributed there to FIPS 199/CNSSI 4009](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=61). Accessed 2026-11-05.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
