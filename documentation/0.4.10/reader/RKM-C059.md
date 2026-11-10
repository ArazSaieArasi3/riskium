# Responsibility Role Term

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C059`; **source title:** `ResponsibilityRoleTerm`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D07 · Risk Responsibility](Subdomains.md#d07)

## Authored source definition

A controlled value identifying the kind of responsibility or authority assigned. This is a managed vocabulary resource with scheme-qualified identity, not a bare string.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Information Artifact](RKM-C014.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| R-54 | incoming `assignmentRole` | [Responsibility Assignment Information](RKM-C051.md) | 0..* | 1 | FORMAL_CORE |
| R-59 | incoming `mandateRole` | [Responsibility Relator](RKM-C052.md) | 0..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Classification Term](RKM-C019.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `RELATED` · reviewed 2026-11-10.

Retain vocabulary-concept/function context. The controlled term denotes a responsibility or authority kind; selecting the term does not instantiate the actual role or the mandate grounding it.

The path through ClassificationTerm and VocabularyConcept preserves InformationArtifact identity. R-54 records an assignment's selected term and R-59 a mandate's term; lexical equality alone establishes neither mandate identity nor actual authorization.

### skos:Concept

**Selected source meaning (paraphrase):** A knowledge-organization notion; using it does not automatically identify an OWL class.

**Source and locator:** [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/2009/REC-skos-reference-20090818/), W3C Recommendation, 18 August 2009; [§3, especially §§3.1 and 3.5.1](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#concepts). Inspected 2026-11-10.

**Inspected scope:** Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.

### prov:Role

**Selected source meaning (paraphrase):** A function in an activity-qualified provenance context.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.3, Role](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Role). Inspected 2026-11-10.

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
