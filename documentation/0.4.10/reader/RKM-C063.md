# Workflow Scheme Version

Scientific source **0.3.2** · documentary review **0.2.0** · reader **0.4.10**. Prepared for package **v0.3.10**; not published. Source SHA-256: `060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb`.

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

**Source ID:** `RKM-C063`; **source title:** `WorkflowSchemeVersion`; **layer:** `FORMAL_CORE`; **native representation:** `Class`.

**Subdomain:** [D08 · Risk Workflow](Subdomains.md#d08)

## Authored source definition

An issued version of a scheme defining workflow values and permitted transitions.

## Identity and source typing

- OntoUML stereotype: `subkind`; abstract: `false`.
- Identity supplier: [Artifact Version](RKM-C015.md)
- Identity basis: Inherits documentary identity from InformationArtifact, or version identity from ArtifactVersion through an explicit generalization path.
- Typing rationale: Essential documentary specialization in the bounded risk-knowledge profile; label equality does not establish identity.
- Source aliases: None recorded.

## Direct catalog associations

| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |
|---|---|---|---|---|---|
| RK2-021 | incoming `availableInWorkflowScheme` | [Workflow State Term](RKM-C061.md) | 0..* | 1..* | FORMAL_CORE |
| RX-030 | incoming `underSchemeVersion` | [Workflow Assignment](RKM-C064.md) | 0..* | 1 | FORMAL_CORE |

The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.

## Direct inheritance

Direct supertypes: [Artifact Version](RKM-C015.md)<br>
Direct subtypes: None recorded.

## Current documentary comparisons

**Disposition:** `CONTRAST` · reviewed 2026-11-10.

Retain the comparison boundary. Riskium WorkflowSchemeVersion is an issued transition specification; concept-scheme aggregation or a revision qualification does not define its transitions or authorization rules.

Do not infer executable workflow rules from a concept aggregation or version lineage.

### skos:ConceptScheme

**Selected source meaning (paraphrase):** An organization of concepts; a scheme need not be an OWL ontology.

**Source and locator:** [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/2009/REC-skos-reference-20090818/), W3C Recommendation, 18 August 2009; [§4, especially §§4.1 and 4.6.2](https://www.w3.org/TR/2009/REC-skos-reference-20090818/#schemes). Inspected 2026-11-10.

**Inspected scope:** Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.

### prov:Revision

**Selected source meaning (paraphrase):** A qualified derivation whose result revises an original while retaining substantial content.

**Source and locator:** [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/), W3C Recommendation, 30 April 2013; [§4.3, Revision](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Revision). Inspected 2026-11-10.

**Inspected scope:** Terms listed below only; no PROV conformance or import asserted.

**Review role:** Assistant-supported reinspection of selected primary passages and unchanged authored/local structural context; not an independent expert judgment.

[Original decision and evidence route](../../../evaluation/releases/v0.3.9/followups/issue85-reuse-review/review.json) · [Current review component](../../../references/concept-definitions/0.2.0/review.json) · [All 82 dispositions](External-Definitions.md).

Formal alignment remains **unassessed**; no OWL/SKOS equivalence, imported source restriction or independent semantic rating is generated.

## Evidence and alignment boundary

**Authored source status:** Bounded review and finite tests; native OntoUML and independent semantic validation pending

The source status is preserved verbatim. The [qualification and publication plan](../../../plans/v0.3.9.md) separately report the current bounded structural and engine checks. The source status and documentary comparisons do not supply independent semantic acceptance or formal standards equivalence. Domain comparisons and modeling foundations are distinguished below.

[Rebuildable source recipe](../../../tools/releases/v039/source.py) · [Export contract](../../../ontology/0.3.2/source-contract.json) · [Structural binding](structural-binding.json)

[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)

[Current documentary review](External-Definitions.md) · [Curation and version status](Curation-Status.md)
