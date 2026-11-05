# Treatment Decision Information

**Source ID:** `RKM-C041` · **Subdomain:** [D06 · Risk Treatment](Subdomains.md) · **Layer:** `FORMAL_CORE`

## Current authored definition

A recorded decision about treating risk, including the selected option, rationale, responsible authority and relevant basis.

## Identity and modeling

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md).
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.

## Direct source relations

| ID | Source reading | Endpoint | Cardinalities |
| --- | --- | --- | --- |
| `R-19` | outgoing `decisionAbout` | [Risk Case](RKM-X01.md) | 0..* → 1 |
| `R-20` | outgoing `selectsStrategy` | [Treatment Strategy Term](RKM-C042.md) | 0..* → 1 |
| `R-60` | incoming `recordsDecision` | [Entry Revision](RKM-C023.md) | 1..* → 0..* |
| `R-63` | outgoing `isSpecifiedByPlan` | [Plan Specification](RKM-C043.md) | 0..* → 0..* |
| `RK2-014` | outgoing `basedOnEvaluation` | [Risk Evaluation Outcome](RKM-X04.md) | 0..* → 0..* |
| `RK2-015` | outgoing `recordsRemainingRiskAssessment` | [Assessment Information](RKM-C032.md) | 0..* → 0..* |

Generalizes: [Information Artifact](RKM-C014.md).  
Specialized by: none recorded.

## External definition and alignment status

**Documentary disposition:** `CONTRAST` · reviewed 2026-11-05.

**Authored comparison:** A recorded decision selecting a response differs from implementing that response; the security process term does not establish authority or success.

### Risk Response

**External source definition (paraphrase):** Accepting, avoiding, mitigating, sharing or transferring risk.

**Source:** Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1. September 2012; DOI 10.6028/NIST.SP.800-30r1. [Appendix B, printed B-10, PDF page 60; attributed there to SP 800-39](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=60). Accessed 2026-11-05.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

Formal equivalence and subsumption remain **unassessed**. This documentary comparison asserts no OWL or SKOS alignment axiom and records no independent semantic rating.

[Review method, source register and all 80 decisions](External-Definitions.md).

## Evidence and limits

Bounded review and finite tests; native OntoUML and independent semantic validation pending
The authored definition and link inventory are source facts; they do not constitute independent semantic validation. [Quality evidence](../../../evaluation/quality/README.md) keeps formal and application outcomes separate.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Model JSON](../../../ontology/riskium-model.json)
