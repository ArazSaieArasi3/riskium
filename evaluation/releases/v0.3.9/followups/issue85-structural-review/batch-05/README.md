# N3b-5 — structural-context documentary review

Date: 2026-11-10. Planning target v0.3.10; #85 remains open.

**This batch is complete: 9 concepts. Current-source documentary coverage is 77/82 (93.9%); 5 remain.** This fraction is not overall research completion, semantic correctness or independent acceptance.

## What was reviewed

The selected current concept definitions, direct associations/generalizations, complete ancestry, changed ancestor records, changed association-neighbor records, applicable explicit set policy and analytical-case application policy were compared with the historical source. Primary source editions, locators and selected passages were checked separately. An unchanged edge does not hide the change in its endpoint's meaning.

| Concept | Disposition | Current-context interpretation |
|---|---|---|
| [Treatment Decision Information](previews/RKM-C041.md) | CONTRAST | R-19 relates the decision to the continuing RiskCase; R-20 selects a strategy. R-63 and RK2-014/RK2-015 may connect plans, evaluation and remaining-risk assessment. Those documentary links do not alone establish treatment execution or effectiveness. |
| [Treatment Strategy Term](previews/RKM-C042.md) | RELATED | R-20 selects this term in decision information. ClassificationTerm/VocabularyConcept ancestry preserves managed resource identity, while common labels and retained sibling groups do not create equivalence, exclusivity or realized response. |
| [Plan Specification](previews/RKM-C043.md) | RELATED | R-21 concerns one or more analytical risk cases; R-62 gives the plan role. R-64 relates an actual TreatmentActivity separately, and R-63 can connect decisions. A plan can be recorded before any execution is established; issued-content changes follow new-version lineage. |
| [Plan Role Term](previews/RKM-C046.md) | RELATED | R-62 assigns the chosen function to a plan specification. Scheme-qualified identity is inherited through ClassificationTerm/VocabularyConcept; the retained incomplete/non-disjoint groups are carried policy, not a new semantic-partition approval. |
| [Risk Criteria](previews/RKM-C072.md) | NEEDS_LICENSED_SOURCE | RX-017 qualifies the criteria specification by context. RX-018/RX-019 permit appetite/tolerance statements without making them universally mandatory or identical. The local C-25 version-target obligation remains separate from any uninspected normative definition. |
| [Risk Appetite Statement](previews/RKM-C073.md) | NEEDS_LICENSED_SOURCE | RK2-023 requires context under this managed profile, and RX-018 can connect criteria to the statement. Its objective, authority and framework qualifications preserve provenance; a statement is not universal permission for every case or evidence that an organization acted on it. |
| [Risk Tolerance Statement](previews/RKM-C074.md) | NEEDS_LICENSED_SOURCE | RK2-024 requires context under the managed profile and RX-019 optionally connects criteria. C-10 preserves framework/version/original meaning; common tolerance labels do not justify pooling values or applying a threshold to an unrelated context. |
| [Objective Reference](previews/RKM-X02.md) | CONTRAST | RX-003 connects analytical RiskCase to objective references; RK2-011 allows context-specific references. Revised RiskCase meaning was reviewed. The reference can identify source-context objectives without importing an entire organization ontology or asserting that the objective has been achieved. |
| [Control Reference](previews/RKM-X05.md) | CONTRAST | RX-020 keeps resolution to the heterogeneous control boundary optional. RK2-016/RK2-022 retain register and assessment-baseline references. C-14 excludes a uniform formal-core RiskControl class, so unresolved references remain information rather than fabricated realized controls. |

## Findings and limits

All nine definitions, concept records and direct/inherited edges are unchanged. All inherit InformationArtifact identity; three have the revised RiskCase as a direct association neighbor. The blanket artifact set remains excluded, while retained vocabulary groups are incomplete/non-disjoint without new semantic approval.

All nine disposition labels are retained: three RELATED, three CONTRAST and three NEEDS_LICENSED_SOURCE. Six primary-term comparisons and three explicit normative deferrals are current-source documentary decisions; the latter do not count as normative term inspection or exact crosswalk completion.

TreatmentDecisionInformation records a choice; PlanSpecification describes intended action; TreatmentActivity is a separately modeled event. A record, strategy or plan does not establish execution, authorization or effectiveness. Source security-response terminology is not generalized into a universal treatment workflow.

ControlReference may remain unresolved and does not create a formal-core RiskControl class. ObjectiveReference remains distinct from its objective. Those informational boundaries preserve incomplete knowledge without asserting physical controls or achieved objectives.

RiskCriteria, RiskAppetiteStatement and RiskToleranceStatement preserve context and authored meanings. The official ISO catalogue confirms edition identity only; exact normative wording and Risk IT/COBIT/ISO crosswalks remain #78. C-10 retains distinct source meanings rather than silently combining tolerance readings.

## Primary sources

- [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/) — W3C Recommendation, 30 April 2013; accessed 2026-11-10. Terms listed below only; no PROV conformance or import asserted.
- [Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf) — September 2012; DOI 10.6028/NIST.SP.800-30r1; accessed 2026-11-10. Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.
- [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/2009/REC-skos-reference-20090818/) — W3C Recommendation, 18 August 2009; accessed 2026-11-10. Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.
- [ISO 31073:2022, Risk management — Vocabulary](https://www.iso.org/standard/79637.html) — Edition 1, February 2022; accessed 2026-11-10. Official identity and abstract inspected; normative term text NOT inspected. No exact term or clause number claimed; #78 owns adoption.

PROV-O and SKOS were retrieved directly and match their historical hashes. NIST direct HTTP returned 403; current B-10/B-11 glossary text and page images were inspected via web, preserving original attributions and separate historical full-body hashes. ISO 31073:2022 catalogue title/edition/date/abstract were inspected as metadata only, not normative terms. Restricted texts and full source documents are not redistributed.

## Verification and reproduction

From the repository root:

```sh
python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-05/build.py --batch batch-05
python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-05/build.py --batch batch-05 --check
```

The validator binds raw source/prior/allocation/passage/context files; recomputes the structural context; checks the declared population and disjoint cumulative coverage; preserves authored definitions and separates comparison targets and policy conclusions. validation.json records local negative integrity controls; reproduction.json records separate-process byte equality. These are not CI, HermiT, SHACL or independent expert results.

## Next execution

N3b-6 reviews the final five D09/D10 evidence/monitoring concepts. Then qualify the complete successor curation and publish/read back the selected v0.3.10 package before closing #85. The three exact normative mappings remain separately deferred in #78; main, public v0.3.9, source 0.3.2, reader 0.4.9 and article 7.2.21 remain unchanged.
