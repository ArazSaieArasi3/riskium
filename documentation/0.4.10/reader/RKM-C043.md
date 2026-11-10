# Plan Specification

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C043`; **source title:** `PlanSpecification`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D06 · Risk Treatment](Subdomains.md#d06)

## Authored source definition

A versioned specification of intended actions, resources, responsibilities, timing and conditions for a stated purpose.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-21 | outgoing `planAbout` | [Risk Case](RKM-X01.md) | 0..* | 1..* | FORMAL_CORE |
| R-61 | incoming `recordsPlan` | [Entry Revision](RKM-C023.md) | 1..* | 0..* | FORMAL_CORE |
| R-62 | outgoing `planRole` | [Plan Role Term](RKM-C046.md) | 0..* | 1 | FORMAL_CORE |
| R-63 | incoming `isSpecifiedByPlan` | [Treatment Decision Information](RKM-C041.md) | 0..* | 0..* | FORMAL_CORE |
| R-64 | incoming `executesPlan` | [Treatment Activity](RKM-C044.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `RELATED` · reviewed 2026-11-10.

Retain PROV Plan as related intended-action content. Riskium records its own resources, responsibility, timing, purpose and versions without adopting a full PROV representation or treating the plan as its execution.

R-21 concerns one or more analytical risk cases; R-62 gives the plan role. R-64 relates an actual TreatmentActivity separately, and R-63 can connect decisions. A plan can be recorded before any execution is established; issued-content changes follow new-version lineage.

### prov:Plan

**Selected source meaning (paraphrase):** An entity representing intended steps toward agents’ goals.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.3, Plan](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Plan). Inspected 2026-11-10.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

**Review role:** Assistant-supported source comparison, current ancestry/neighbor/set-policy and selected treatment/policy contracts; normative deferrals explicit; not independent expert or operational evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-05/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
