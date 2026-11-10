# Risk Context Specification

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C002`; **source title:** `RiskContextSpecification`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D01 · Risk Phenomena](Subdomains.md#d01)

## Authored source definition

A versioned information specification of analysis boundaries, circumstances, time horizon and objective references under which risk statements and results are interpreted.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-35 | incoming `analyzedInContext` | [Risk Case](RKM-X01.md) | 0..* | 0..* | FORMAL_CORE |
| R-43 | incoming `natureInContext` | [Risk Nature Assertion](RKM-C005.md) | 0..* | 0..1 | FORMAL_CORE |
| R-45 | incoming `assessmentContext` | [Assessment Information](RKM-C032.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-001 | outgoing `refersToCondition` | [Predisposing Condition](RKM-C008.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-002 | outgoing `refersToVulnerability` | [Vulnerability](RKM-C011.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-003 | outgoing `refersToExposure` | [Exposure](RKM-C012.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-009 | incoming `descriptionContext` | [Risk Description](RKM-C024.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-010 | incoming `scenarioContext` | [Risk Scenario Specification](RKM-C003.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-011 | outgoing `referencesObjective` | [Objective Reference](RKM-X02.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-012 | incoming `uncertaintyContext` | [Uncertainty Statement](RKM-X03.md) | 0..* | 0..1 | FORMAL_CORE |
| RK2-023 | incoming `appetiteContext` | [Risk Appetite Statement](RKM-C073.md) | 0..* | 1..* | FORMAL_CORE |
| RK2-024 | incoming `toleranceContext` | [Risk Tolerance Statement](RKM-C074.md) | 0..* | 1..* | FORMAL_CORE |
| RK2-026 | incoming `observationContext` | [Observation Result](RKM-C068.md) | 0..* | 0..1 | FORMAL_CORE |
| RK3-003 | incoming `sourceReferenceContext` | [Risk Source Reference](RKM-X06.md) | 0..* | 0..1 | FORMAL_CORE |
| RX-001 | incoming `hasContext` | [Risk Case](RKM-X01.md) | 0..* | 1..* | FORMAL_CORE |
| RX-017 | incoming `criteriaForContext` | [Risk Criteria](RKM-C072.md) | 0..* | 1..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `RELATED` · reviewed 2026-11-10.

The context specification retains boundaries, horizon and objective references. Generic entity context does not supply that schema or its version policy.

R-35/RX-001 now refer to the explicitly analytical RiskCase. Missing task inputs concern readiness under a declared profile, not nonexistence or formal admission of that case.

### prov:Entity

**Selected source meaning (paraphrase):** A thing considered through fixed aspects, including conceptual or imaginary things.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.1, Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity). Inspected 2026-11-10.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

**Review role:** Assistant-supported selected primary-passage comparison plus explicit source ancestry, changed-neighbor and set-policy review; no independent expert rating.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-01/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
