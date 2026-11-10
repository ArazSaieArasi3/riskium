# N3b-6 — structural-context documentary review

Date: 2026-11-10. Planning target v0.3.10; #85 remains open.

**This batch is complete: 5 concepts. Current-source documentary coverage is 82/82 (100.0%); 0 remain.** This fraction is not overall research completion, semantic correctness or independent acceptance.

## What was reviewed

The selected current concept definitions, direct associations/generalizations, complete ancestry, changed ancestor records, changed association-neighbor records, applicable explicit set policy and analytical-case application policy were compared with the historical source. Primary source editions, locators and selected passages were checked separately. An unchanged edge does not hide the change in its endpoint's meaning.

| Concept | Disposition | Current-context interpretation |
|---|---|---|
| [Evidence Reference](previews/RKM-C065.md) | RELATED | The reference keeps documentary identity and ordinary RX-021 linkage. Its local-edge difference is the added GE-001 specialization from EvidenceReferenceRole, not an altered direct association. RE-001/RE-002 and C-26 separately describe grounded use and distinct participants. R-68 is read with C-12 and its no-proof rationale, preserving support/challenge/context distinctions. |
| [Observation Result](previews/RKM-C068.md) | RELATED | RX-022 relates an ObservationActivity to its informational result; RX-023 identifies the indicator and RX-024 the continuing RiskCase. RK2-026 can retain context and RK2-017 connects revisions. The result is neither its activity nor a risk occurrence; a numeric value alone is insufficient for cross-context comparison. |
| [Indicator](previews/RKM-C069.md) | ANALOGY | RX-023 links reported results to their indicator specification; RX-025 can anchor a threshold. Specification versions and interpretation remain documentary. Neither external property classes nor DQV domain constraints are automatically imported into Riskium. |
| [Threshold](previews/RKM-C070.md) | CONTRAST | RX-025 and RK2-020 each permit an indicator or scale anchor. C-08 requires at least one supported anchor, with compatible interpretation if both exist; it does not require both. Qualitative boundaries retain scale semantics rather than invented numerical units. RX-027 records selected signal comparison. |
| [Signal](previews/RKM-C071.md) | RELATED | RX-026 requires supporting observation results in the managed signal profile; RX-027 can identify thresholds and RX-028 can prompt case review. Revised RiskCase meaning was reviewed. Source incomplete material is retained without fabricating observations; neither an alert nor a crossed threshold automatically proves a risk occurrence or cause. |

[Complete 82-concept disposition inventory](coverage.json): exact population and source/packet routes, including three explicit normative deferrals; not component qualification or publication.

## Findings and limits

All five authored definitions, concept records and inherited edges are unchanged. Four complete local-edge sets are unchanged; EvidenceReference adds GE-001 from EvidenceReferenceRole while its direct associations remain unchanged. The added role retains its authored candidate status; no new scientific or independent approval is inferred.

Three RELATED and one ANALOGY labels are retained. Threshold changes its scoped-absence label to CONTRAST with DQV Metric, clarifying the different intended roles without claiming no relevant threshold vocabulary exists.

EvidenceReference remains documentary. An actual grounded evidential-use relationship is separately represented through EvidenceUseRelator, EvidenceItem and EvidenceReferenceRole. C-26 supplies distinctness/grounding requirements; multiplicity alone does not establish distinct individuals or claim truth.

Observation activity, informational result, indicator specification, threshold and signal remain distinct. C-08 requires an indicator or scale anchor, with compatible interpretation if both exist; qualitative boundaries do not need fabricated numerical units. A signal can prompt review without proving an occurrence or cause.

Every current catalog concept now has one disjoint documentary disposition across N2/N3a/N3b-1..6. The inventory includes three NEEDS_LICENSED_SOURCE decisions (criteria/appetite/tolerance) carried in batch-05. Recording them is not normative-source inspection; #78 and independent semantic review #23 remain open. Full curation-component selection, generator qualification and actual publication/readback remain N4/N5.

## Primary sources

- [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/) — W3C Recommendation, 30 April 2013; accessed 2026-11-10. Terms listed below only; no PROV conformance or import asserted.
- [Semantic Sensor Network Ontology](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/) — W3C Recommendation, 19 October 2017; SOSA/SSN; accessed 2026-11-10. Selected core classes only; observed properties and their specifications remain distinct.
- [Data on the Web Best Practices: Data Quality Vocabulary](https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/) — W3C Working Group Note, 15 December 2016; accessed 2026-11-10. Dataset-quality vocabulary used by analogy only. This Note is work in progress, not a W3C Recommendation.

All three primary HTML responses were directly retrieved and match the historical hashes. Four selected term passages retain edition/locator/fingerprint bindings. DQV is a Working Group Note used only for bounded comparison; SOSA and PROV constraints are not automatically imported. Full source documents are not redistributed.

## Verification and reproduction

From the repository root:

```sh
python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-06/build.py --batch batch-06
python -B evaluation/releases/v0.3.9/followups/issue85-structural-review/batch-06/build.py --batch batch-06 --check
```

The validator binds raw source/prior/allocation/passage/context files; recomputes the structural context; checks the declared population and disjoint cumulative coverage; preserves authored definitions and separates comparison targets and policy conclusions. validation.json records local negative integrity controls; reproduction.json records separate-process byte equality. These are not CI, HermiT, SHACL or independent expert results.

## Next execution

N4 now assembles and qualifies the complete successor curation component for all 82 dispositions, including explicit normative deferrals; bind the generator/reader and preserve historical components. N5 then publishes and independently reads back the selected v0.3.10 package before closing #85. Main, public v0.3.9, source 0.3.2, reader 0.4.9 and article 7.2.21 remain unchanged.
