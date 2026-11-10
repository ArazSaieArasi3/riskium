# Entry Revision

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C023`; **source title:** `EntryRevision`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D04 · Risk Registration](Subdomains.md#d04)

## Authored source definition

An identifiable version of a register entry, preserving the content and qualified links effective at its issue.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Artifact Version](RKM-C015.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-02 | outgoing `hasDescription` | [Risk Description](RKM-C024.md) | 1 | 0..* | FORMAL_CORE |
| R-23 | outgoing `hasStateAssertion` | [Record State Assertion](RKM-C062.md) | 1 | 0..* | FORMAL_CORE |
| R-24 | outgoing `hasTag` | [Tag](RKM-C021.md) | 0..* | 0..* | FORMAL_CORE |
| R-28 | outgoing `documentsAssessment` | [Assessment Information](RKM-C032.md) | 1..* | 0..* | FORMAL_CORE |
| R-29 | outgoing `documentsClassification` | [Classification Assertion](RKM-C020.md) | 1..* | 0..* | FORMAL_CORE |
| R-30 | outgoing `documentsAssignment` | [Responsibility Assignment Information](RKM-C051.md) | 1..* | 0..* | FORMAL_CORE |
| R-33 | outgoing `revisionOf` | [Risk Register Entry](RKM-C022.md) | 0..* | 1 | FORMAL_CORE |
| R-34 | incoming `previousRevision` | [Entry Revision](RKM-C023.md) | 0..* | 0..1 | FORMAL_CORE |
| R-34 | outgoing `previousRevision` | [Entry Revision](RKM-C023.md) | 0..* | 0..1 | FORMAL_CORE |
| R-38 | outgoing `recordsConsequence` | [Consequence Statement](RKM-C025.md) | 1 | 0..* | FORMAL_CORE |
| R-44 | outgoing `recordsNature` | [Risk Nature Assertion](RKM-C005.md) | 1..* | 0..* | FORMAL_CORE |
| R-52 | outgoing `recordsIdentification` | [Identification Information](RKM-C026.md) | 1..* | 0..* | FORMAL_CORE |
| R-60 | outgoing `recordsDecision` | [Treatment Decision Information](RKM-C041.md) | 1..* | 0..* | FORMAL_CORE |
| R-61 | outgoing `recordsPlan` | [Plan Specification](RKM-C043.md) | 1..* | 0..* | FORMAL_CORE |
| RK2-016 | outgoing `recordsControlReference` | [Control Reference](RKM-X05.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-017 | outgoing `recordsObservation` | [Observation Result](RKM-C068.md) | 0..* | 0..* | FORMAL_CORE |
| RX-031 | incoming `assignmentForRevision` | [Workflow Assignment](RKM-C064.md) | 0..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Artifact Version](RKM-C015.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `CONTRAST` · reviewed 2026-11-10.

Retain the object/derivation distinction. Riskium EntryRevision is a version object with effective links; a qualified revision describes derivation rather than being that version or its creation activity.

Do not substitute a derivation qualification for an entry-version individual.

### prov:Entity

**Selected source meaning (paraphrase):** A thing considered through fixed aspects, including conceptual or imaginary things.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.1, Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity). Inspected 2026-11-10.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

### prov:Revision

**Selected source meaning (paraphrase):** A qualified derivation whose result revises an original while retaining substantial content.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.3, Revision](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Revision). Inspected 2026-11-10.

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
