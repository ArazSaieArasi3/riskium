# Assessment Scale

**Source ID:** `RKM-C036` · **Subdomain:** [D05 · Risk Assessment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A governed scale specification defining permissible values or ordered levels for a specified assessment dimension.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-14` | incoming `usesScale` | [Dimension Assessment Result](RKM-C034.md) | 0..* → 0..1 |
| `R-16` | incoming `levelOf` | [Assessment Scale Level](RKM-C038.md) | 0..* → 1 |
| `R-49` | incoming `permitsScale` | [Assessment Method Specification](RKM-C035.md) | 0..* → 0..* |
| `RK2-019` | outgoing `scaleForDimension` | [Assessment Dimension](RKM-C039.md) | 0..* → 1 |
| `RK2-020` | incoming `thresholdOnScale` | [Threshold](RKM-C070.md) | 0..* → 0..1 |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `ANALOGY` · reviewed 2026-11-05.

**Authored comparison:** NIST’s example vulnerability-severity levels illustrate a scale, without defining all permissible Riskium dimensions, units or version-compatibility policies.

### Assessment scale: vulnerability severity

**External source definition (paraphrase):** Example levels for vulnerability severity.

**Source:** Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1. September 2012; DOI 10.6028/NIST.SP.800-30r1. [Appendix F, Table F-2, printed F-2, PDF page 78](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=78). Accessed 2026-11-05.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
