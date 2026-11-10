# N3b-4 — structural-context documentary review

Date: 2026-11-10. Planning target v0.3.10; #85 remains open.

**This batch is complete: 11 concepts. Current-source documentary coverage is 68/82 (82.9%); 14 remain.** This fraction is not overall research completion, semantic correctness or independent acceptance.

## What was reviewed

The selected current concept definitions, direct associations/generalizations, complete ancestry, changed ancestor records, changed association-neighbor records, applicable explicit set policy and analytical-case application policy were compared with the historical source. Primary source editions, locators and selected passages were checked separately. An unchanged edge does not hide the change in its endpoint's meaning.

| Concept | Disposition | Current-context interpretation |
|---|---|---|
| [Assessment Information](previews/RKM-C032.md) | ANALOGY | R-11 targets the continuing RiskCase; R-12 records basis and R-13/R-17 allow dimensional and score outputs. RX-014 pins context version, while optional method links are completed under the selected analytical task. Revised RiskCase and ArtifactVersion neighbors were reviewed. |
| [Assessment Basis](previews/RKM-C033.md) | CONTRAST | R-12 makes the basis explicit for the assessment information; RK2-022 may identify the control baseline assumed. The documentary specification does not establish that the controls exist or are effective, and different bases cannot be silently pooled. |
| [Dimension Assessment Result](previews/RKM-C034.md) | ANALOGY | R-48 identifies one dimension; R-14/R-15 and RX-016 retain optional scale, selected level and scale-version information. C-13/C-18 require compatible interpretation for comparison. The revised ArtifactVersion neighbor does not turn the result itself into a version or a measured real-world quality. |
| [Assessment Method Specification](previews/RKM-C035.md) | ANALOGY | R-46/R-50 relate information and scores to a method; R-49 and RK2-018 describe permitted scales/dimensions. The specification retains documentary identity; a separately pinned ArtifactVersion identifies which issued content was used. A procedure description alone is not execution evidence. |
| [Assessment Scale](previews/RKM-C036.md) | ANALOGY | RK2-019 declares one dimension, R-16 relates level resources to their scale, and version references qualify interpretation. Equal codes or labels across scales do not license ranking or arithmetic; qualitative values remain possible. |
| [Risk Score Result](previews/RKM-C037.md) | ANALOGY | R-50 requires a score method; R-18 permits zero or many component links for reported scores. C-21 separately requires declared components, a pinned method and adequate inputs for a computed score. C-18 preserves missing data as missing and does not certify a reported number as reproducible. |
| [Assessment Scale Level](previews/RKM-C038.md) | RELATED | The VocabularyConcept ancestry preserves documentary identity; R-16 assigns one scale and R-15 selects a level for a result. C-13 also requires the selected level to match the scale version and dimension; a matching label alone is insufficient. |
| [Assessment Dimension](previews/RKM-C039.md) | ANALOGY | The path through ClassificationTerm/VocabularyConcept preserves scheme-qualified identity. R-48, RK2-018 and RK2-019 connect result, method and scale to the dimension. DQV metric requirements are not automatically added to the Riskium profile. |
| [Epistemic Status Term](previews/RKM-C040.md) | RELATED | R-47 can qualify assessment information with a controlled status. Missing designation remains missing; the status resource, its text and the evidence supporting that status are separate. Retained incomplete/non-disjoint term groups are not newly approved as semantic partitions. |
| [Uncertainty Statement](previews/RKM-X03.md) | RELATED | RX-004 concerns a continuing RiskCase; RK2-012/RK2-013 retain context and its use in assessment information. Revised RiskCase meaning was reviewed. Assumptions and evidential limitations may be qualitative; absence of a probability is not zero uncertainty. |
| [Risk Evaluation Outcome](previews/RKM-X04.md) | CONTRAST | RX-011 identifies the case, RX-012 requires assessment information and RX-013 pins a criteria ArtifactVersion. C-25 governs the versioned target. A numeric score alone does not establish acceptability or a treatment decision; revised case and version neighbors were reviewed. |

## Findings and limits

All eleven authored definitions, direct edge records and inherited edges are unchanged. All inherit InformationArtifact identity; four concepts have changed association neighbors involving RiskCase and/or ArtifactVersion. Excluding the blanket artifact set preserves subtype edges without inventing exclusive or complete sibling partitions.

Ten labels are retained. AssessmentBasis changes its scoped-absence label to CONTRAST with generic PROV Entity, clarifying a difference in definitional scope rather than claiming no comparable work exists. The batch contains six ANALOGY, three RELATED and two CONTRAST decisions.

Assessment information, activity, dimensional result, method specification, scale/level, numeric score and criteria-based evaluation remain distinct. Optional received information is not declared task-ready merely because it has been recorded. Version targets follow the selected C-25 source statement; this packet does not newly execute dependency validation on real data.

C-18/C-21 preserve comparison dependencies, missingness and the reported/computed score distinction. A reported score may lack component links; a computed score has additional input/method obligations. A value alone establishes neither reproducibility nor acceptability. Full formula adequacy, all scale/unit compatibility and independent interpretation remain separate evaluation work.

The DQV comparisons are dataset-quality pattern analogies to a Working Group Note, not risk-specific standards conformance. NIST supplies security-specific documentary and scale examples. Neither DQV domain constraints nor NIST example codes are imported as universal risk rules.

## Primary sources

- [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/) — W3C Recommendation, 30 April 2013; accessed 2026-11-10. Terms listed below only; no PROV conformance or import asserted.
- [Guide for Conducting Risk Assessments, NIST SP 800-30 Revision 1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf) — September 2012; DOI 10.6028/NIST.SP.800-30r1; accessed 2026-11-10. Security-specific terms, selected glossary entries and tables only; not a universal enterprise-risk vocabulary. Glossary entries retain their original attributions.
- [Data on the Web Best Practices: Data Quality Vocabulary](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/) — W3C Working Group Note, 15 December 2016; accessed 2026-11-10. Dataset-quality vocabulary used by analogy only. This Note is work in progress, not a W3C Recommendation.
- [Semantic Sensor Network Ontology](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/) — W3C Recommendation, 19 October 2017; SOSA/SSN; accessed 2026-11-10. Selected core classes only; observed properties and their specifications remain distinct.
- [SKOS Simple Knowledge Organization System Reference](https://www.w3.org/TR/2009/REC-skos-reference-20090818/) — W3C Recommendation, 18 August 2009; accessed 2026-11-10. Concept, scheme and lexical-label distinctions; no SKOS mapping triples asserted.
- [Web Annotation Data Model](https://www.w3.org/TR/2017/REC-annotation-model-20170223/) — W3C Recommendation, 23 February 2017; accessed 2026-11-10. Selected motivations and annotation/body distinction only; no serialization conformance asserted.

Five primary HTML responses were directly retrieved and match their historical hashes. NIST direct HTTP attempts failed; the current B-9 glossary and F-2 scale were inspected through web PDF text and page images. Their selected passage fingerprints and exact locators are recorded; the historical full-PDF hash is retained separately and was not reverified. No source text is redistributed.

## Verification and reproduction

From the repository root:

```sh
python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-04/build.py --batch batch-04
python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-04/build.py --batch batch-04 --check
```

The validator binds raw source/prior/allocation/passage/context files; recomputes the structural context; checks the declared population and disjoint cumulative coverage; preserves authored definitions and separates comparison targets and policy conclusions. validation.json records local negative integrity controls; reproduction.json records separate-process byte equality. These are not CI, HermiT, SHACL or independent expert results.

## Next execution

N3b-5 reviews nine D06/D11 treatment/policy concepts, then N3b-6 five D09/D10 evidence/monitoring concepts. After all 82 dispositions, qualify the complete successor curation and publish/read back the selected v0.3.10 package before closing #85. Main, public v0.3.9, source 0.3.2, reader 0.4.9 and article 7.2.21 remain unchanged.
