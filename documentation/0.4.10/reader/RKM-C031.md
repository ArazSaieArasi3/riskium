# Assessment Activity

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C031`; **source title:** `AssessmentActivity`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D05 · Risk Assessment](Subdomains.md#d05)

## Authored source definition

An actual activity contributing to risk identification, analysis or evaluation. It may cover only part of a risk assessment; the complete standardized assessment process is outside the current process-modeling scope.

## Identity and source typing

- OntoUML stereotype: `event`; abstract: `false`.
- Identity supplier: No identity supplier is assigned in this source record.
- Identity basis: An actual happening individuated by supported temporal extent, participants and occurrence boundaries.
- Typing rationale: Event interpretation; a description, plan or possibility is not an event instance.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-26 | outgoing `producesAssessmentInformation` | [Assessment Information](RKM-C032.md) | 0..* | 0..* | FORMAL_CORE |
| R-51 | outgoing `assessmentPerformer` | [Agent](RKM-C047.md) | 0..* | 0..* | FORMAL_CORE |
| R-71 | incoming `refersToAssessmentActivity` | [Evidence Reference](RKM-C065.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `CONTRAST` · reviewed 2026-11-10.

Retain the activity/process scope distinction. A Riskium AssessmentActivity may contribute only one actual part of identification, analysis or evaluation; it is not automatically the complete security assessment process.

A planned assessment is not an actual assessment activity.

### Risk Assessment

**Selected source meaning (paraphrase):** An information-system risk assessment process.

**Source and locator:** [Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf), September 2012; DOI 10.6028/NIST.SP.800-30r1; [Appendix B, printed B-9, PDF page 59; attributed there to SP 800-39](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=59). Inspected 2026-11-10.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

### prov:Activity

**Selected source meaning (paraphrase):** An occurrence over time acting on or with entities.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.1, Activity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Activity). Inspected 2026-11-10.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

**Review role:** Assistant-supported reinspection of selected primary passages and unchanged authored/local structural context; not an independent expert judgment.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-reuse-review/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
