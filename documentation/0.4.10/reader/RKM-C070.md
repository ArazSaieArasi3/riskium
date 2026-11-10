# Threshold

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C070`; **source title:** `Threshold`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D10 · Risk Monitoring](Subdomains.md#d10)

## Authored source definition

A versioned information specification of a context-qualified decision boundary for an indicator or assessment scale, with a comparator, permissible value interpretation and applicability context.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RK2-020 | outgoing `thresholdOnScale` | [Assessment Scale](RKM-C036.md) | 0..* | 0..1 | FORMAL_CORE |
| RX-025 | outgoing `thresholdForIndicator` | [Indicator](RKM-C069.md) | 0..* | 0..1 | FORMAL_CORE |
| RX-027 | incoming `evaluatedAgainstThreshold` | [Signal](RKM-C071.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `CONTRAST` · reviewed 2026-11-10.

Clarify the former scoped-absence label as a contrast in intended role: a DQV measuring standard does not itself specify a comparator-qualified decision boundary. No global absence, class disjointness or exact threshold equivalence is asserted.

RX-025 and RK2-020 each permit an indicator or scale anchor. C-08 requires at least one supported anchor, with compatible interpretation if both exist; it does not require both. Qualitative boundaries retain scale semantics rather than invented numerical units. RX-027 records selected signal comparison.

### dqv:Metric

**Selected source meaning (paraphrase):** A standard for measuring a quality dimension; a measurement provides its observed value.

**Source and locator:** [Data on the Web Best Practices: Data Quality Vocabulary](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/), W3C Working Group Note, 15 December 2016; [§4.2](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/#dqv:Metric). Inspected 2026-11-10.

**Inspected scope:** Dataset-quality vocabulary used by analogy only. This Note is work in progress, not a W3C Recommendation.

**Review role:** Assistant-supported source comparison, current ancestry/neighbor/set-policy and selected evidence/monitoring contracts; not a new engine, instance or independent expert evaluation.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-06/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
