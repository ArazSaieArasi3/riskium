# Responsibility Assignment Information

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C051`; **source title:** `ResponsibilityAssignmentInformation`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D07 · Risk Responsibility](Subdomains.md#d07)

## Authored source definition

A recorded statement about an assignment of responsibility or authority, distinct from the relationship it asserts.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-09 | outgoing `assignmentAbout` | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-10 | outgoing `hasBearerReference` | [Actor Reference](RKM-C050.md) | 0..* | 1 | FORMAL_CORE |
| R-30 | incoming `documentsAssignment` | [Entry Revision](RKM-C023.md) | 1..* | 0..* | FORMAL_CORE |
| R-54 | outgoing `assignmentRole` | [Responsibility Role Term](RKM-C059.md) | 0..* | 1 | FORMAL_CORE |
| R-55 | outgoing `documentsActualMandate` | [Responsibility Relator](RKM-C052.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-025 | outgoing `authorizerReference` | [Actor Reference](RKM-C050.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `CONTRAST` · reviewed 2026-11-10.

Retain the claim/relationship contrast. A recorded responsibility assignment can describe an unsupported claim; a provenance association does not supply the full Riskium mandate-grounding contract.

R-55 links the statement to at most one actual mandate and allows none. R-09 concerns an analytical RiskCase; neither this statement nor missing approval determines that case's existence. A named owner alone does not establish responsibility, accountability and approval authority together.

### prov:Association

**Selected source meaning (paraphrase):** An agent’s responsibility and role in an activity, optionally qualified by a plan.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.3, Association](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Association). Inspected 2026-11-10.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

**Review role:** Assistant-supported selected-source comparison, ancestry/neighbor/set-policy review and bounded static identity/dependency checks; no instance-level or independent expert evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-02/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
