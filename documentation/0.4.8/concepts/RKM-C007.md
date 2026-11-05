# Risk Source

**Source ID:** `RKM-C007` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `OPTIONAL_PHENOMENON_BOUNDARY`

## Current authored definition

A contextual source role that an entity may play in giving rise to risk, alone or with other contributors. The catalog boundary spans possible bearer categories and is not assigned a single OntoUML stereotype here.

## Identity and modeling

- OntoUML stereotype: `None`; abstract: `false`.
- Identity supplier: `None`.
- Identity basis: Bearer-specific; no uniform identity principle over objects, events, situations and aspects.
- Typing rationale: Broad domain notion retained in the catalog and optional external bridge; no uniform native OntoUML class asserted.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK3-002` | incoming `resolvesToSource` | [Risk Source Reference](RKM-X06.md) | 0..* → 0..1 |
| `RX-005` | incoming `hasSource` | [Risk Case](RKM-X01.md) | 0..* → 0..* |

Generalizes: none recorded.  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `ANALOGY` · reviewed 2026-11-05.

**Authored comparison:** Riskium permits heterogeneous contextual contributors and opportunities; the security threat-source definition is narrower in subject matter, without a proved class subsumption.

### Threat Source

**External source definition (paraphrase):** Intent/method or a situation/method potentially exploiting a vulnerability.

**Source:** Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1. September 2012; DOI 10.6028/NIST.SP.800-30r1. [Appendix B, printed B-13, PDF page 63; attributed there to CNSSI 4009](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=63). Accessed 2026-11-05.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
