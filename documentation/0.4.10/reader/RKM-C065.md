# Evidence Reference

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C065`; **source title:** `EvidenceReference`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D09 · Risk Evidence](Subdomains.md#d09)

## Authored source definition

A qualified reference linking a claim or activity to an evidence item, with its intended evidential role and provenance.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-68 | outgoing `supportsRecordedArtifact` | [Information Artifact](RKM-C014.md) | 0..* | 1..* | FORMAL_CORE |
| R-69 | outgoing `refersToOccurrence` | [Risk Occurrence](RKM-C004.md) | 0..* | 0..* | FORMAL_CORE |
| R-70 | outgoing `refersToAgent` | [Agent](RKM-C047.md) | 0..* | 0..* | FORMAL_CORE |
| R-71 | outgoing `refersToAssessmentActivity` | [Assessment Activity](RKM-C031.md) | 0..* | 0..* | FORMAL_CORE |
| R-72 | outgoing `refersToTreatmentActivity` | [Treatment Activity](RKM-C044.md) | 0..* | 0..* | FORMAL_CORE |
| RX-021 | outgoing `pointsToEvidence` | [Evidence Item](RKM-C066.md) | 1..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: [Evidence Reference Role](RKM-C076.md)

## Current documentary comparisons

**Disposition:** `RELATED` · reviewed 2026-11-10.

Retain derivation as one related provenance pattern, not as a definition of evidential use. Evidence may be used without deriving a new entity or endorsing a claim; a citation does not establish independent corroboration.

The reference keeps documentary identity and ordinary RX-021 linkage. Its local-edge difference is the added GE-001 specialization from EvidenceReferenceRole, not an altered direct association. RE-001/RE-002 and C-26 separately describe grounded use and distinct participants. R-68 is read with C-12 and its no-proof rationale, preserving support/challenge/context distinctions.

### prov:Derivation

**Selected source meaning (paraphrase):** Entity-to-entity transformation, construction or updating represented as a qualified influence.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.3, Derivation](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Derivation). Inspected 2026-11-10.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

**Review role:** Assistant-supported source comparison, current ancestry/neighbor/set-policy and selected evidence/monitoring contracts; not a new engine, instance or independent expert evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-06/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Selected integration interpretation](../../../evaluation/manuscript-review/v7.2.3/issue93-integration/definitions/RKM-C065.md) preserves the separate candidate design decision.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
