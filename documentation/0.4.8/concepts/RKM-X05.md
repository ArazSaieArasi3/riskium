# Control Reference

**Source ID:** `RKM-X05` · **Subdomain:** [D06 · Risk Treatment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A managed identifier or description of a claimed control whose real-world bearer may remain unresolved.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `RK2-016` | incoming `recordsControlReference` | [Entry Revision](RKM-C023.md) | 0..* → 0..* |
| `RK2-022` | incoming `referencesControlBaseline` | [Assessment Basis](RKM-C033.md) | 0..* → 0..* |
| `RX-020` | outgoing `resolvesToControl` | [Risk Control](RKM-C045.md) | 0..* → 0..1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `CONTRAST` · reviewed 2026-11-05.

**Authored comparison:** A documentary identifier may describe a safeguard without proving that its bearer exists, is implemented or is effective.

### prov:Entity

**External source definition (paraphrase):** A thing considered through fixed aspects, including conceptual or imaginary things.

**Source:** PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [§4.1, Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity). Accessed 2026-11-05.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

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
