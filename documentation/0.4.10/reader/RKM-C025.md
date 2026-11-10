# Consequence Statement

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C025`; **source title:** `ConsequenceStatement`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D04 · Risk Registration](Subdomains.md#d04)

## Authored source definition

An information item expressing a possible or reported consequence; it is not the consequence itself.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-22 | outgoing `statementAbout` | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-38 | incoming `recordsConsequence` | [Entry Revision](RKM-C023.md) | 1 | 0..* | FORMAL_CORE |
| R-40 | outgoing `sourceSlot` | [Consequence Slot Term](RKM-C029.md) | 0..* | 1 | FORMAL_CORE |
| RX-009 | incoming `hasPossibleConsequenceStatement` | [Risk Scenario Specification](RKM-C003.md) | 0..* | 0..* | FORMAL_CORE |
| RX-010 | outgoing `refersToActualOutcome` | [Consequence](RKM-C010.md) | 0..* | 0..1 | OPTIONAL_EXTERNAL_BRIDGE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `RELATED` · reviewed 2026-11-10.

Retain descriptive-function context while separating a possible/reported consequence statement from an outcome. The motivation does not supply consequence semantics or establish realization.

R-22 concerns the analytical RiskCase; R-40 retains a source slot and RX-010 permits no actual-outcome referent (0..1). A recorded possible consequence must not be promoted into an observed outcome merely to populate a field.

### oa:describing

**Selected source meaning (paraphrase):** A motivation for describing a target.

**Source and locator:** [Web Annotation Data Model](https://www.w3.org/TR/2017/REC-annotation-model-20170223/), W3C Recommendation, 23 February 2017; [§3.3.5, motivation describing](https://www.w3.org/TR/2017/REC-annotation-model-20170223/#motivation-and-purpose). Inspected 2026-11-10.

**Inspected scope:** Selected motivations and annotation/body distinction only; no serialization conformance asserted.

**Review role:** Assistant-supported primary-passage comparison and current ancestry/neighbor/set-policy plus selected registration/workflow source-contract checks; not an instance or independent expert evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-03/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
