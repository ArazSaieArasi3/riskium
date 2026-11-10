# Assessment Information

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C032`; **source title:** `AssessmentInformation`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D05 · Risk Assessment](Subdomains.md#d05)

## Authored source definition

A managed information artifact documenting an assessment and its scope, basis, methods, time context, participants and results. It is distinct from performing that assessment.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-11 | outgoing `assesses` | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-12 | outgoing `hasBasis` | [Assessment Basis](RKM-C033.md) | 0..* | 1 | FORMAL_CORE |
| R-13 | outgoing `hasDimensionResult` | [Dimension Assessment Result](RKM-C034.md) | 1 | 0..* | FORMAL_CORE |
| R-17 | outgoing `hasScoreResult` | [Risk Score Result](RKM-C037.md) | 1 | 0..* | FORMAL_CORE |
| R-26 | incoming `producesAssessmentInformation` | [Assessment Activity](RKM-C031.md) | 0..* | 0..* | FORMAL_CORE |
| R-28 | incoming `documentsAssessment` | [Entry Revision](RKM-C023.md) | 1..* | 0..* | FORMAL_CORE |
| R-45 | outgoing `assessmentContext` | [Risk Context Specification](RKM-C002.md) | 0..* | 0..1 | FORMAL_CORE |
| R-46 | outgoing `usesMethod` | [Assessment Method Specification](RKM-C035.md) | 0..* | 0..1 | FORMAL_CORE |
| R-47 | outgoing `epistemicStatus` | [Epistemic Status Term](RKM-C040.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-013 | outgoing `recordsUncertainty` | [Uncertainty Statement](RKM-X03.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-015 | incoming `recordsRemainingRiskAssessment` | [Treatment Decision Information](RKM-C041.md) | 0..* | 0..* | FORMAL_CORE |
| RX-012 | incoming `usesAssessment` | [Risk Evaluation Outcome](RKM-X04.md) | 0..* | 1..* | FORMAL_CORE |
| RX-014 | outgoing `usesContextVersion` | [Artifact Version](RKM-C015.md) | 0..* | 1 | FORMAL_CORE |
| RX-015 | outgoing `usesMethodVersion` | [Artifact Version](RKM-C015.md) | 0..* | 0..1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `ANALOGY` · reviewed 2026-11-10.

Retain the NIST security-report comparison as a documentary precedent. It describes an output of assessment, not the assessment activity or a universal enterprise/ecosystem report template.

R-11 targets the continuing RiskCase; R-12 records basis and R-13/R-17 allow dimensional and score outputs. RX-014 pins context version, while optional method links are completed under the selected analytical task. Revised RiskCase and ArtifactVersion neighbors were reviewed.

### Risk Assessment Report

**Selected source meaning (paraphrase):** The formal documented output of risk assessment.

**Source and locator:** [Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf), September 2012; DOI 10.6028/NIST.SP.800-30r1; [Appendix B, printed B-9, PDF page 59](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=59). Inspected 2026-11-10.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

**Review role:** Assistant-supported primary-passage comparison, current ancestry/neighbor/set-policy and selected assessment source-contract checks; not an instance or independent expert evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-04/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
