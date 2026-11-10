# Artifact Version

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C015`; **source title:** `ArtifactVersion`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D02 · Risk Information](Subdomains.md#d02)

## Authored source definition

An identifiable issued documentary version of a managed information artifact. Its issued semantic content and effective dependency versions are immutable; revisions receive distinct version identities.

## Identity and source typing

- OntoUML stereotype: `kind`; abstract: `false`.
- Identity supplier: [Artifact Version](RKM-C015.md)
- Identity basis: Provides an explicitly governed individuation principle within the declared profile; surrogate keys are identifiers of that policy, not independent ontological proof.
- Typing rationale: Proposed identity-supplying kind for a distinct artifact version. Version identity and issuance are separate from RiskCase identity and operational admission.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RX-006 | outgoing `versionOf` | [Information Artifact](RKM-C014.md) | 0..* | 1 | FORMAL_CORE |
| RX-007 | outgoing `expressesContent` | [Information Content](RKM-C016.md) | 0..* | 1..* | FORMAL_CORE |
| RX-013 | incoming `usesCriteriaVersion` | [Risk Evaluation Outcome](RKM-X04.md) | 0..* | 1 | FORMAL_CORE |
| RX-014 | incoming `usesContextVersion` | [Assessment Information](RKM-C032.md) | 0..* | 1 | FORMAL_CORE |
| RX-015 | incoming `usesMethodVersion` | [Assessment Information](RKM-C032.md) | 0..* | 0..1 | FORMAL_CORE |
| RX-016 | incoming `usesScaleVersion` | [Dimension Assessment Result](RKM-C034.md) | 0..* | 0..1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: None recorded.<br>
Direct subtypes: [Entry Revision](RKM-C023.md), [Workflow Scheme Version](RKM-C063.md)

## Current documentary comparisons

**Disposition:** `CONTRAST` · reviewed 2026-11-10.

Retain the distinction: the issued version is the documentary object; Revision qualifies a derivation. First issue need not revise a predecessor. Issuance policy does not determine whether a RiskCase exists.

### prov:Entity

**Selected source meaning (paraphrase):** A thing considered through fixed aspects, including conceptual or imaginary things.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.1, Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity). Inspected 2026-11-10.

**Inspected scope:** Selected Entity, Person, Organization, Revision, Role, Usage and qualifiedUsage passages only; no import or PROV conformance asserted.

### prov:Revision

**Selected source meaning (paraphrase):** A qualified derivation whose result revises an original while retaining substantial content.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.3, Revision](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Revision). Inspected 2026-11-10.

**Inspected scope:** Selected Entity, Person, Organization, Revision, Role, Usage and qualifiedUsage passages only; no import or PROV conformance asserted.

**Authored illustration, not an executed test:** A correction is issued as a separately identified version with explicit predecessor lineage.

**Interpretation counterexample:** A revision relationship must not be substituted for the resulting version object.

**Review role:** Assistant-supported inspection of selected primary-source passages and the current authored model; no independent human rating.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-changed-review/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
