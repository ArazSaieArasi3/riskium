# Risk Scenario Specification

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C003`; **source title:** `RiskScenarioSpecification`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D01 · Risk Phenomena](Subdomains.md#d01)

## Authored source definition

A managed information specification of a possible development of conditions, events and effects concerning one or more RiskCases. Several scenarios may concern one case; a scenario is not the case or an actual occurrence.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-25 | outgoing `mayBeRealizedBy` | [Risk Occurrence](RKM-C004.md) | 0..* | 0..* | FORMAL_CORE |
| R-36 | outgoing `scenarioAbout` | [Risk Case](RKM-X01.md) | 0..* | 1..* | FORMAL_CORE |
| R-37 | incoming `expressesScenario` | [Risk Description](RKM-C024.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-010 | outgoing `scenarioContext` | [Risk Context Specification](RKM-C002.md) | 0..* | 0..* | FORMAL_CORE |
| RX-009 | outgoing `hasPossibleConsequenceStatement` | [Consequence Statement](RKM-C025.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `ANALOGY` · reviewed 2026-11-10.

Retain a bounded analogy to the security scenario entry. Riskium describes possible developments about continuing cases, with a broader stated risk scope.

R-36 separates a scenario from its analytical case and R-25 does not turn a specification into an actual occurrence. Inherited artifact identity remains documentary, without blanket sibling exclusion.

### Threat Scenario

**Selected source meaning (paraphrase):** A time-partially-ordered grouping of threat events associated with threat sources.

**Source and locator:** [Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf), September 2012; DOI 10.6028/NIST.SP.800-30r1; [Appendix B, printed B-13, PDF page 63](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf#page=63). Inspected 2026-11-10.

**Inspected scope:** Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.

**Review role:** Assistant-supported selected primary-passage comparison plus explicit source ancestry, changed-neighbor and set-policy review; no independent expert rating.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-01/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
