# Risk Nature Assertion

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C005`; **source title:** `RiskNatureAssertion`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D01 · Risk Phenomena](Subdomains.md#d01)

## Authored source definition

A source-qualified information assertion that possible or reported effects are favorable, unfavorable or mixed relative to identified objectives and context.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-41 | outgoing `natureOf` | [Risk Case](RKM-X01.md) | 0..* | 1 | FORMAL_CORE |
| R-42 | outgoing `declaresNature` | [Nature Term](RKM-C006.md) | 0..* | 1 | FORMAL_CORE |
| R-43 | outgoing `natureInContext` | [Risk Context Specification](RKM-C002.md) | 0..* | 0..1 | FORMAL_CORE |
| R-44 | incoming `recordsNature` | [Entry Revision](RKM-C023.md) | 1..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Information Artifact](RKM-C014.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `RELATED` · reviewed 2026-11-10.

Retain contextual classification as a related use. The compared classifying term is a motivation instance, not the class of RiskNatureAssertion or proof of favorable/unfavorable meaning.

R-41/R-42/R-43 keep the claim about a case, selected nature value and context separate. The analytical case reading leaves nature objective-relative; the claim does not establish truth by classification.

### oa:classifying

**Selected source meaning (paraphrase):** A motivation for classifying a target.

**Source and locator:** [Web Annotation Data Model](https://www.w3.org/TR/2017/REC-annotation-model-20170223/), W3C Recommendation, 23 February 2017; [§3.3.5, motivation classifying](https://www.w3.org/TR/2017/REC-annotation-model-20170223/#motivation-and-purpose). Inspected 2026-11-10.

**Inspected scope:** Selected motivations and annotation/body distinction only; no serialization conformance asserted.

**Review role:** Assistant-supported selected primary-passage comparison plus explicit source ancestry, changed-neighbor and set-policy review; no independent expert rating.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-01/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
