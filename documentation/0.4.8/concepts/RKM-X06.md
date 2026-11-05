# Risk Source Reference

**Source ID:** `RKM-X06` · **Subdomain:** [D01 · Risk Phenomena](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A managed information artifact identifying or describing a claimed contributor to risk in a declared context. The referenced contributor may be unresolved, hypothetical or heterogeneous. The reference does not establish actual causation or an actual occurrence.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Governed documentary identity, inherited from InformationArtifact; source-reference identity is distinct from source-bearer identity.
- Typing rationale: A documentary reference can be uniformly typed without forcing its heterogeneous referents into one category.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK3-001` | incoming `hasSourceReference` | [Risk Case](RKM-X01.md) | 0..* → 0..* |
| `RK3-002` | outgoing `resolvesToSource` | [Risk Source](RKM-C007.md) | 0..* → 0..1 |
| `RK3-003` | outgoing `sourceReferenceContext` | [Risk Context Specification](RKM-C002.md) | 0..* → 0..1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `CONTRAST` · reviewed 2026-11-05.

**Authored comparison:** A recorded contributor reference may remain hypothetical or unresolved; it cannot be identified with NIST’s threat source or establish actual causation.

### prov:Entity

**External source definition (paraphrase):** A thing considered through fixed aspects, including conceptual or imaginary things.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.1, Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

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
