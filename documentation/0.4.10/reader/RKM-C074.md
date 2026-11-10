# Risk Tolerance Statement

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C074`; **source title:** `RiskToleranceStatement`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D11 · Risk Policy](Subdomains.md#d11)

## Authored source definition

A managed, versioned statement recording an organization's stated risk tolerance under an explicitly identified source vocabulary or framework and context. Permissible deviation and readiness to bear remaining risk are retained as distinct source meanings, not silently merged.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RK2-024 | outgoing `toleranceContext` | [Risk Context Specification](RKM-C002.md) | 0..* | 1..* | FORMAL_CORE |
| RX-019 | incoming `considersToleranceStatement` | [Risk Criteria](RKM-C072.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `NEEDS_LICENSED_SOURCE` · reviewed 2026-11-10.

Retain the explicit normative deferral and source-specific tolerance meanings. Permissible-deviation and remaining-risk readings are not silently equated or attributed to an unseen ISO clause; exact edition-qualified interpretation remains #78.

RK2-024 requires context under the managed profile and RX-019 optionally connects criteria. C-10 preserves framework/version/original meaning; common tolerance labels do not justify pooling values or applying a threshold to an unrelated context.

**Normative mapping deferred:** [ISO 31073:2022, Risk management — Vocabulary](https://www.iso.org/standard/79637.html), Edition 1, February 2022. Only catalogue identity/abstract were inspected; no exact normative term wording or clause is asserted. [#78](https://github.com/ArazSaieArasi3/riskium/issues/78) retains legitimate full-source access, edition-specific interpretation and adoption.

**Review role:** Assistant-supported source comparison, current ancestry/neighbor/set-policy and selected treatment/policy contracts; normative deferrals explicit; not independent expert or operational evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-05/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
