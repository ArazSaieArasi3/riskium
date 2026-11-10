# N3b-3 — structural-context documentary review

Date: 2026-11-10. Planning target v0.3.10; #85 remains open.

**This batch is complete: 11 concepts. Current-source documentary coverage is 57/82 (69.5%); 25 remain.** This fraction is not overall research completion, semantic correctness or independent acceptance.

## What was reviewed

The selected current concept definitions, direct associations/generalizations, complete ancestry, changed ancestor records, changed association-neighbor records, applicable explicit set policy and analytical-case application policy were compared with the historical source. Primary source editions, locators and selected passages were checked separately. An unchanged edge does not hide the change in its endpoint's meaning.

| Concept | Disposition | Current-context interpretation |
|---|---|---|
| [Risk Register Entry](previews/RKM-C022.md) | RELATED | R-01 targets one RiskCase in this profile and permits zero or many entries per case. R-33 relates distinct entry revisions to their entry; RX-008 assigns register membership. Neither an entry identifier nor organizational admission is the case's universal existence condition. |
| [Risk Description](previews/RKM-C024.md) | RELATED | RK2-007/RK2-008/R-37 preserve case, pattern and scenario targets; R-39 qualifies description function. C-09 requires a published description target under its profile. Source/description context does not establish an actual occurrence or turn the description into its case. |
| [Consequence Statement](previews/RKM-C025.md) | RELATED | R-22 concerns the analytical RiskCase; R-40 retains a source slot and RX-010 permits no actual-outcome referent (0..1). A recorded possible consequence must not be promoted into an observed outcome merely to populate a field. |
| [Identification Information](previews/RKM-C026.md) | RELATED | R-07 identifies the analytical risk item, R-08 records actor references and R-27 records intake channels. R-52 connects the information to revisions. Documentary attribution is kept separate from actual risk causation, operational admission and available temporal precision. |
| [Intake Channel Term](previews/RKM-C027.md) | RELATED | The path through ClassificationTerm and VocabularyConcept preserves InformationArtifact identity. R-27 records a source-qualified channel; common text neither identifies the vocabulary resource nor resolves a risk source. |
| [Description Role Term](previews/RKM-C028.md) | RELATED | R-39 supplies the selected function of a RiskDescription. Scheme-qualified term identity is inherited through ClassificationTerm/VocabularyConcept; retained groups remain incomplete and non-disjoint without a new semantic approval. |
| [Consequence Slot Term](previews/RKM-C029.md) | RELATED | R-40 preserves the original statement's source slot. The inherited documentary identity does not equate identical strings across schemes or force a scalar selection when multiple assertions apply. |
| [Risk Register](previews/RKM-C030.md) | RELATED | RX-008 organizes entry records, while entries and their revisions keep separate identities. Register membership does not establish one-to-one case identity or require every analytical RiskCase to be operationally admitted. |
| [Analysis State Term](previews/RKM-C060.md) | RELATED | R-31 optionally records analysis state in a RecordStateAssertion. Scheme/version and temporal qualification matter; incomplete or absent state information is not silently replaced by a workflow value or an invented completion result. |
| [Workflow State Term](previews/RKM-C061.md) | RELATED | R-32 records an optional workflow value; RX-029 and RX-030 link a workflow assignment to its value and scheme version. C-19 preserves unknown rules/authority as unknown. The term resource is not the assignment situation. |
| [Record State Assertion](previews/RKM-C062.md) | RELATED | R-23 attaches the statement to an EntryRevision, R-31/R-32 can retain separate analysis/workflow values, and RX-032 optionally documents a WorkflowAssignment. The statement remains documentary; the assignment remains a situation. Corrections and lineage follow C-03/C-24 without overwriting issued content. |

## Findings and limits

All eleven authored definitions, direct edge records and inherited edges are unchanged. Every selected concept still inherits InformationArtifact identity; four have the revised RiskCase as a direct association neighbor. Excluding the blanket artifact set preserves subtype edges without inventing sibling exclusivity or complete coverage.

The selected source contracts keep register entries, continuing risk items, entry revisions and register membership separate. An entry concerns one case in this profile, but a case can have zero or many entries. EntryRevision retains ArtifactVersion identity; correction/lineage obligations remain source statements rather than a new overwrite or migration implementation.

Description, consequence and record-state statements remain information about referents. A possible outcome link and the statement-to-workflow-assignment link remain optional. WorkflowAssignment remains a situation under a scheme version and revision; the statement documenting it is not that situation.

Analysis/workflow values are scheme-qualified vocabulary resources, not real-world risk states. Closure does not establish cessation or effectiveness; missing rule/authority remains unknown. These commitments are documented without claiming actual workflow execution, complete task data or independent semantic approval.

## Primary sources

- [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/) — W3C Recommendation, 30 April 2013; accessed 2026-11-10. Terms listed below only; no PROV conformance or import asserted.
- [Web Annotation Data Model](https://www.w3.org/TR/2017/REC-annotation-model-20170223/) — W3C Recommendation, 23 February 2017; accessed 2026-11-10. Selected motivations and annotation/body distinction only; no serialization conformance asserted.
- [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/2009/REC-skos-reference-20090818/) — W3C Recommendation, 18 August 2009; accessed 2026-11-10. Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.

All three primary responses were directly retrieved and match the historical response hashes. Selected anchor fingerprints, versions and locators are retained without redistributing documents. Web Annotation describing is a motivation instance, not a class equivalent to RiskDescription or ConsequenceStatement. No PROV/SKOS/Annotation conformance, imported axiom or complete semantic preservation is asserted.

## Verification and reproduction

From the repository root:

```sh
python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-03/build.py --batch batch-03
python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-03/build.py --batch batch-03 --check
```

The validator binds raw source/prior/allocation/passage/context files; recomputes the structural context; checks the declared population and disjoint cumulative coverage; preserves authored definitions and separates comparison targets and policy conclusions. validation.json records local negative integrity controls; reproduction.json records separate-process byte equality. These are not CI, HermiT, SHACL or independent expert results.

## Next execution

N3b-4 reviews eleven D05 assessment concepts, followed by D06/D11 (9) and D09/D10 (5). After all 82 dispositions, qualify the complete successor curation and publish/read back the selected v0.3.10 package before closing #85. Main, public v0.3.9, scientific source 0.3.2, reader 0.4.9 and article 7.2.21 are unchanged.
