# Observation Result

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C068`; **source title:** `ObservationResult`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D10 · Risk Monitoring](Subdomains.md#d10)

## Authored source definition

An information result produced by an observation activity, qualified by subject, time, method and available units.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RK2-017 | incoming `recordsObservation` | [Entry Revision](RKM-C023.md) | 0..* | 0..* | FORMAL_CORE |
| RK2-026 | outgoing `observationContext` | [Risk Context Specification](RKM-C002.md) | 0..* | 0..1 | FORMAL_CORE |
| RX-022 | incoming `producesObservation` | [Observation Activity](RKM-C067.md) | 1 | 0..* | FORMAL_CORE |
| RX-023 | outgoing `reportsIndicator` | [Indicator](RKM-C069.md) | 0..* | 1 | FORMAL_CORE |
| RX-024 | outgoing `observesCase` | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| RX-026 | incoming `basedOnObservation` | [Signal](RKM-C071.md) | 0..* | 1..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `RELATED` · reviewed 2026-11-10.

Retain SOSA Result as related output context. SOSA also covers actuation and sampling results, while this Riskium concept selects observation information qualified by subject, method, time and available units; no class equivalence or imported restriction is asserted.

RX-022 relates an ObservationActivity to its informational result; RX-023 identifies the indicator and RX-024 the continuing RiskCase. RK2-026 can retain context and RK2-017 connects revisions. The result is neither its activity nor a risk occurrence; a numeric value alone is insufficient for cross-context comparison.

### sosa:Result

**Selected source meaning (paraphrase):** A result of observation, actuation or sampling; simple values have a separate property.

**Source and locator:** [Semantic Sensor Network Ontology](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/), W3C Recommendation, 19 October 2017; SOSA/SSN; [§4.7.2.1](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/#SOSAResult). Inspected 2026-11-10.

**Inspected scope:** Selected core classes only; observed properties and their specifications remain distinct.

**Review role:** Assistant-supported source comparison, current ancestry/neighbor/set-policy and selected evidence/monitoring contracts; not a new engine, instance or independent expert evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-06/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
