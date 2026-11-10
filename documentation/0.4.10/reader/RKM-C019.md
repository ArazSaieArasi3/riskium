# Classification Term

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C019`; **source title:** `ClassificationTerm`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D03 · Risk Classification](Subdomains.md#d03)

## Authored source definition

A managed vocabulary item expressing a controlled classification value within an identified scheme. Scheme membership and version context constrain its interpretation. This is a managed vocabulary resource with scheme-qualified identity, not a bare string.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-04 | incoming `selectsTerm` | [Classification Assertion](RKM-C020.md) | 0..* | 1 | FORMAL_CORE |
| R-05 | outgoing `belongsToScheme` | [Classification Scheme](RKM-C018.md) | 0..* | 1 | FORMAL_CORE |
| R-06 | incoming `hasBroaderTerm` | [Classification Term](RKM-C019.md) | 0..* | 0..* | FORMAL_CORE |
| R-06 | outgoing `hasBroaderTerm` | [Classification Term](RKM-C019.md) | 0..* | 0..* | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Vocabulary Concept](RKM-C017.md)<br>
Direct subtypes: [Nature Term](RKM-C006.md), [Intake Channel Term](RKM-C027.md), [Description Role Term](RKM-C028.md), [Consequence Slot Term](RKM-C029.md), [Epistemic Status Term](RKM-C040.md), [Treatment Strategy Term](RKM-C042.md), [Plan Role Term](RKM-C046.md), [Responsibility Role Term](RKM-C059.md), [Analysis State Term](RKM-C060.md), [Workflow State Term](RKM-C061.md)

## Current documentary comparisons

**Disposition:** `RELATED` · reviewed 2026-11-10.

Retain the controlled-resource/label distinction. The selected scheme and version context qualify a classification value; lexical equality is not a universal or resource identity rule.

G2-053/G2-052 preserve the inherited documentary identity. GS-RKM-C019 and GS-RKM-C017 remain explicitly non-disjoint and incomplete; no new covering, exclusivity or semantic-module claim is added.

### skos:Concept

**Selected source meaning (paraphrase):** A knowledge-organization notion; using it does not automatically identify an OWL class.

**Source and locator:** [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/2009/REC-skos-reference-20090818/), W3C Recommendation, 18 August 2009; [§3, especially §§3.1 and 3.5.1](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#concepts). Inspected 2026-11-10.

**Inspected scope:** Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.

### Lexical labels

**Selected source meaning (paraphrase):** A natural-language string associated with a resource, distinct from the resource.

**Source and locator:** [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/2009/REC-skos-reference-20090818/), W3C Recommendation, 18 August 2009; [§5.1](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#labels). Inspected 2026-11-10.

**Inspected scope:** Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.

**Review role:** Assistant-supported selected primary-passage comparison plus explicit source ancestry, changed-neighbor and set-policy review; no independent expert rating.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-01/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
