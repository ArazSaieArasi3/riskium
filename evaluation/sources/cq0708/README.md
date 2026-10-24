# CQ07 correction lineage and CQ08 withheld identity

Current status on 24 October 2026: the owner accepted the bounded source/case scope, and stable v0.3.1 is published. The later [publication/disclosure reconciliation](../publication-review.json) preserves four recorded source notices and the existing population/withheld-identity limits. Checkpoint-specific pending owner/final-release statements below are historical; broader independent case/meaning validation remains open in #13/#23.

Status: **published and verified** as [v0.3.1-rc.7](https://github.com/ArazSaieArasi3/riskium/releases/tag/v0.3.1-rc.7), completed child #26 under open parent #13, then final claim/route consolidation. Source/oracle freeze `920524ee05d4f7f7468ce7a9aa75a70cc7c08503` preceded query implementation/execution. [Readable report](report.md), [complete receipt](report.json.gz), [profile](profile.json), [CQ07 query](cq07.rq) and [CQ08 query](cq08.rq) retain current execution. [Publication receipt](../../releases/v0.3.1-rc.7-publication.json) verifies five assets, 340 source files, 16 passed gates, 137 software regressions and exact tag.

[Source/cell/identity cohort](cohort.json), [inspection receipt](inspection.json) and [fixed independent answer vector](expected.json) are stored separately. Two exact supplied PDF snapshots were inspected: the original online-first Wong/Siah/Lo article and its actual corrigendum. The latter's first page explicitly identifies the original DOI and affected tables. Both original table pages and reissued table pages were rendered and visually checked; ten selected old/new context anchors matched the stated normalization. No filename-based inference supplies correction lineage.

## Attribution, versions and rights

Chi Heem Wong, Kien Wei Siah and Andrew W. Lo, *Estimation of clinical trial success rates and related parameters*, DOI [10.1093/biostatistics/kxx069](https://doi.org/10.1093/biostatistics/kxx069), online 31 January 2018, Biostatistics 20(2):273-286 (2019). The supplied **14-page online-first original snapshot** contains the pre-correction entries. Original PDF pages 6 and 7 are their printed manuscript pages, not silently inferred final journal pages.

The same authors, *Corrigendum: Estimation of clinical trial success rates and related parameters*, DOI [10.1093/biostatistics/kxy072](https://doi.org/10.1093/biostatistics/kxy072), online 14 November 2018, final issue Biostatistics 20(2):366 (2019). The supplied **three-page online-first corrigendum** contains a notice on page 1 and corrected Tables 1/2 on pages 2/3; it is distinguished from the final one-page journal notice and its linked material. Exact PDF hashes and inspected page-text hashes bind these editions. Publisher indexed metadata was checked; direct Oxford opening redirected to an unavailable CDN and PMC returned a browser check. Actual cell evidence comes from supplied PDFs, not search snippets.

Both supplied PDFs explicitly declare **CC BY 4.0**. Authors/source/DOI/edition are credited; selected numerical cells were transcribed into a new original provenance envelope with changed representation. No full table, PDF or private database is tracked or included in public release assets. The original article and corrigendum are **distinct source works**, not two independently corroborating studies. Their respective citation and rights identities are retained. No complete later correction/retraction search is claimed.

## Finite meaning boundary

Five selected cell assertions retain old and reissued value, exact percent unit, indication/therapeutic/method/transition/time context, available denominator and standard error. Four selected values change; one oncology cell is reissued unchanged. Table 1 and Table 2 aggregate entries repeat an underlying estimate, not independent evidence. Missing Table 1 cell denominator/SE remains null. This is traceable published-assertion preservation, not recomputation of clinical trial success probabilities or a clinical/financial recommendation.

CQ08 reuses exactly the 11 already-approved WITHHELD documentary candidates from [the inspected rc.6 cohort](../cq06/README.md). Their case keys remain unassigned and occurrence assertions absent. No owner decision is reopened. An absent optional RDF binding means no link is asserted in the selected graph; it does not prove that a real case does not exist. Raw candidates are not admitted native RiskScenarioSpecifications.

The assistant prepared source selection, transcription, visual/text comparisons and separately fixed expected answers. There is no independent reviewer or new owner rating. The new source/identity population and deliberately synthetic controls will have separate counts. Native/OWL and all earlier scientific/query/SQL receipts remain unchanged; final owner review and claim/route matrix remain separate gates.

## Dictionary and task admission

| Field or relation | Meaning and boundary |
| --- | --- |
| Native RX-006 | Each of our selected curated assertion versions belongs to its assertion artifact. The original publication and corrigendum keep distinct DOI identities; they are not typed as these versions. |
| Native R-36 | ScenarioSpecification → RiskCase in the native model. It appears only as an OPTIONAL raw inspection pattern or deliberately false synthetic link; no such native scenario/case is admitted by the source cohort. |
| app:AssertionRecord, ap:candidate | Supplementary extraction envelope and exact curated version link; no new native class or axiom. |
| prov:wasRevisionOf | Explicit revision from our reissued assertion envelope to its original envelope; same versionOf artifact required by CQ07. |
| dct:source, app:correctsSource | Source DOI per envelope and notice-qualified correction-to-original DOI relation. Source correction does not add independent corroboration. |
| app:reportedValue, app:unit | Exact source-reported percent cell, not a RiskScore or recomputed trial estimate. |
| app:standardErrorPercent, app:totalPaths | Selected available SE/denominator. Missing Table 1 fields stay absent/null and cannot be silently filled with zero. |
| app:cellContext, app:sourceLocator | Exact frozen table/panel/therapeutic/method/transition/time/denominator context and supplied edition/page/row/column locator. |
| app:disposition | CORRECTED_VALUE or REISSUED_UNCHANGED; a real lineage need not change the number. |
| app:independentStudyLineages | One underlying study lineage for this pair; Table 1/Table 2 repeated aggregate estimates and correction do not add independent studies. |
| app:RawScenarioRecord, ap:candidate | CQ08 staging envelope and documentary InformationArtifact candidate inherited from rc.6; not native scenario admission. |
| app:caseAdmission, app:priorRecord | The existing WITHHELD decision and exact previously inspected record; owner decision is preserved. |
| app:occurrenceAsserted | False describes this pipeline's lack of occurrence assertion, not physical-world nonoccurrence. |
| dct:title | Display only; equal titles/numbers never merge distinct assertion/candidate identities. |

CQ07 raw SELECT requires explicit revision, shared native artifact, source correction link and equal cell context. CQ08 raw SELECT deliberately preserves OPTIONAL case links, including synthetic false/conflicting links. The separate caller-known cohort validator binds exact version/parent/target/type/source/context/value/unit/SE/denominator/locator/disposition and case-decision/provenance metadata. Raw answers alone never establish admission or source truth. Coherently forged source/context can be returned yet rejected by frozen checks. Deliberately deleting those checks exposes an admitted synthetic forgery; its test PASS is sensitivity, not domain acceptance. Conflicts are retained and rejected without data repair.

**59 actual SELECT executions** matched declared outcomes: 30 CQ07 and 29 CQ08; 18 source-query cases (two whole cohorts plus 16 individual assertion/candidate cases), 31 synthetic negatives, two equal-title identity controls, two deliberately weakened-guard controls, four successfully executed/detected query mutants and two graph serialization/reparse controls. Categories are disjoint, not 59 real cases. Exact RDF bindings, graph snapshots, query/input hashes, finding oracles and errors are retained in the complete receipt. Parser/engine errors are ERROR, never successful mutation detection.

Automated replay uses the frozen selected source data and inherited rc.6 source/adjudication binding. It does not re-read publisher PDFs, re-evaluate all historical data or infer complete native admission. An optional exact-PDF recheck was also executed with pypdf 6.10.0: both PDF hashes and all six inspected page-text hashes matched. Five pages were visually reviewed; original page 1 additionally supplies its license/text hash.

```sh
python tools/run_source_cq0708.py --check
python -m unittest discover -s tests -p test_source_cq0708.py -v
# Optional, with pypdf installed and exact privately held originals:
python tools/run_source_cq0708.py --verify-pdfs /path/to/private-pdfs
```

## Current CQ06-CQ08 reconciliation

| Obligation | Current method-specific evidence | Remaining boundary |
| --- | --- | --- |
| CQ06 source/origin trace | Rc.6: 13 inspected sourced statements, 35 matching SELECT/control outcomes | Finite source/locator trace, not source truth/full extraction accuracy or independent judgment |
| CQ07 correction lineage | This packet: five inspected old/reissued cell pairs, ten retained assertion versions; actual notice-qualified source link and exact query/control bindings | Not recomputed clinical probabilities, exhaustive correction search, full table validation, independent corroboration or general native correction axiom |
| CQ08 unresolved case identity | This packet: dedicated queries over all 11 already-WITHHELD candidates with exact unbound positive answers and false-promotion controls | Absent asserted case links are not proof that real cases do not exist; no organizational RiskCase or native managed scenario admission |

Historical 40 synthetic CQ results and their original source-population statuses remain unchanged; current source-backed supplements retain separate cohorts/denominators and are not relabeled historical executions. Native/OWL, manuscript and earlier HermiT/SHACL/SQLite receipts retain their exact bytes and engine-specific limits. Parent #13 still needs final accepted claim/source/case disposition and actual owner-led OR-09 review; independent review remains future nonblocking #23. After rc.7, consolidate one final claim/route matrix and final-freeze profile instead of starting unbounded feature packets. No owner judgment is generated by this technical completion.
