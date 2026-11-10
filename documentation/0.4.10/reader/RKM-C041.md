# Treatment Decision Information

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C041`; **source title:** `TreatmentDecisionInformation`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D06 · Risk Treatment](Subdomains.md#d06)

## Authored source definition

A recorded decision about treating risk, including the selected option, rationale, responsible authority and relevant basis.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-19 | outgoing `decisionAbout` | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-20 | outgoing `selectsStrategy` | [Treatment Strategy Term](RKM-C042.md) | 0..* | 1 | FORMAL_CORE |
| R-60 | incoming `recordsDecision` | [Entry Revision](RKM-C023.md) | 1..* | 0..* | FORMAL_CORE |
| R-63 | outgoing `isSpecifiedByPlan` | [Plan Specification](RKM-C043.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-014 | outgoing `basedOnEvaluation` | [Risk Evaluation Outcome](RKM-X04.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-015 | outgoing `recordsRemainingRiskAssessment` | [Assessment Information](RKM-C032.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `CONTRAST` · reviewed 2026-11-10.

Retain the contrast between a recorded choice and a response process. The NIST glossary entry is security-specific and attributed there to SP 800-39; it does not establish that a Riskium decision was authorized, executed or successful.

R-19 relates the decision to the continuing RiskCase; R-20 selects a strategy. R-63 and RK2-014/RK2-015 may connect plans, evaluation and remaining-risk assessment. Those documentary links do not alone establish treatment execution or effectiveness.

### Risk Response

**Selected source meaning (paraphrase):** Accepting, avoiding, mitigating, sharing or transferring risk.

**Source and locator:** [Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf), September 2012; DOI 10.6028/NIST.SP.800-30r1; [Appendix B, printed B-10, PDF page 60; attributed there to SP 800-39](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=60). Inspected 2026-11-10.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

**Review role:** Assistant-supported source comparison, current ancestry/neighbor/set-policy and selected treatment/policy contracts; normative deferrals explicit; not independent expert or operational evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-05/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
