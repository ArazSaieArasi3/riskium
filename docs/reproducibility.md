# Reproduce the current checks

Use Python 3.12 or a compatible Python 3 installation. The conceptual-model, coverage and reference builders use the standard library. The OWL syntax and mapping regression tests require the pinned RDFLib package.

From the repository root:

```sh
python3 tools/validate_model.py
python3 tools/review_coverage.py
python3 tools/build_reference.py
```

To reproduce the OWL export and the complete regression suite in an isolated environment:

```sh
python3 -m venv .venv-owl
.venv-owl/bin/pip install -r tools/requirements-owl.txt
python3 tools/build_owl.py --check
.venv-owl/bin/python -m unittest discover -s tests -v
```

The [OWL review](../evaluation/owl-mapping-review.md) describes the mapping and its limits. Parsing the RDF and checking source allocation do not execute HermiT or SHACL.

To browse the generated reference locally:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/docs/site/`. The generated reference links to the model and conceptual views. Local browsing does not establish a live Pages deployment.

The coverage review verifies source allocation, planned constraint routes and expected fixture contracts. It detects a stale or missing stored review; regeneration with `python3 tools/review_coverage.py --write` is appropriate only after reviewing an intentional contract change.

The optional [native-exchange checks](../evaluation/native-model-review.md) use a pinned schema, Python validation environment and official SDK versions. Their dependency installation and reproduction commands are documented separately; the standard-library checks above remain available without those dependencies.

The [HermiT execution report](../evaluation/hermit/report.md) and exact [premise](../evaluation/hermit/premise.rdf) record the scoped reasoner run. To rerun the mapped ontology and regenerate the JSON and Markdown evidence:

```sh
python3 -m venv .venv-hermit
.venv-hermit/bin/pip install -r tools/requirements-hermit.txt
.venv-hermit/bin/python tools/run_hermit.py
```

The installed Owlready2 package supplies the pinned HermiT jar; the jar itself is not copied into this repository. The script verifies its version and records its SHA-256 digest. Its baseline percentage uses the 295 predeclared HermiT-related obligations; supplemental inference and mutation cases have their own counts. SHACL profiles and explicit-data fixtures remain open in issue #5.

## Scoped SHACL profiles

The first [SHACL report](../evaluation/shacl/report.md) retains every raw graph, effective data graph, shapes graph, publication focus list and exact source-shape/component oracle in JSON. Use a separate pinned environment:

```sh
python3 -m venv .venv-shacl
.venv-shacl/bin/pip install -r tools/requirements-shacl.txt
.venv-shacl/bin/python tools/build_shacl.py
.venv-shacl/bin/python tools/run_shacl.py
.venv-shacl/bin/python -m unittest discover -s tests -v
```

The source signatures and profile SHA-256 digests are checked. Graphs use inference `none`; only source subclass triples and the documented identity normalization are supplied explicitly. No imports or OWL existential fillers are materialized. The task-ready dual-anchor C-08 case is BLOCKED, not a pass. Regenerated Turtle bytes can vary in blank-node/list serialization; the exact per-case snapshots in JSON pin the executed graphs.

`python3 tools/build_semantic_register.py` creates an **unadjudicated planning inventory** for independent semantic review. Do not rerun it over completed reviewer annotations without a migration/reconciliation step: it never imports engineering passes or independent ratings. The [assurance plan](../evaluation/semantic-assurance-plan.md) distinguishes this review from engine testing.

## Ordered endpoint module

The [endpoint receipt](../evaluation/shacl/endpoints/report.md) tests all 254 cardinality obligations in module 0.2.0. The earlier 0.1.0 conditional profiles retain their own source-bound receipt.

```sh
.venv-shacl/bin/python tools/build_endpoint_shapes.py
.venv-shacl/bin/python tools/run_endpoint_shacl.py
.venv-shacl/bin/python tools/build_admission_shapes.py
.venv-shacl/bin/python tools/run_admission_shacl.py
.venv-shacl/bin/python tools/package_admission_receipt.py
.venv-shacl/bin/python tools/build_coherence_shapes.py
.venv-shacl/bin/python tools/run_coherence_shacl.py
.venv-shacl/bin/python tools/build_qualification_shapes.py
.venv-shacl/bin/python tools/run_qualification_shacl.py
.venv-shacl/bin/python tools/verify_qualification_receipt.py
python3 tools/summarize_shacl.py
```

The endpoint JSON stores content-addressed canonical N-Triples snapshots. Reconstruct each validation data graph from its normalized snapshot plus the shared source taxonomy; the exact effective shapes and result graphs are retained. Unit tests replace targetClass with an explicit targetNode to isolate one endpoint, while all 127 paired-end tests retain original targetClass populations. Supplementary hasValue sentinels expose path reversals even for 0..*; they are not domain axioms. Non-applicable below-zero or above-unbounded negative fixtures retain reasons. This module does not yet certify full managed-record admission.

## Catalog metadata admission module

Module 0.3.0 executes the 80 catalog rows under an explicit [application record policy](../evaluation/shacl/admission/profile-review.md), with 77 typed class profiles and three boundary exclusions. The sole supported task is CatalogInspection; risk assessment remains outside this module. The input model and the 359-row coverage contract are unchanged. Run the catalog builder, runner and lossless packager before merging the module receipts with `tools/summarize_shacl.py` as shown above.

The full `report.json.gz` archive preserves raw/effective data, shapes, external record/class requests and result graphs byte for byte; `report-index.json` keeps all obligations and compact case outcomes readable. The index pins compressed/uncompressed hashes and verifies a lossless round trip. Regenerated uncompressed `report.json` is ignored by git. Its N-Triples snapshots preserve blank labels within the receipt rather than canonicalizing each graph independently. Use `run_admission_shacl.reconstruct_pair(report, case)` to parse data and shapes with one shared blank-node context. Caller-added blank-record focus selectors are retained in effective data. No arbitrary instance input may supply schema/import axioms or reserved vocabulary identity aliases.

A relocated environment may retain packages while its interpreter symlink is missing. Recreate it with `python3 -m venv .venv-shacl`, then install/verify the pinned requirements before running. Configuration/identity rejections are exercised by regressions and are not successful SHACL engine runs. Historical frozen receipts retain their source commits; current regression results and input hashes are recorded separately.

## Context and revision coherence module

Module 0.4.0 adds C-23 and C-24 graph conformance under inference none, without context materialization or implicit entry equality. Its [profile](../evaluation/shacl/coherence/profile-review.md) specifies target populations and static/history limits. Run its builder/runner before merging SHACL receipts. The JSON stores full input/shapes/results and exact source-shape/component/focus oracles; replay via `run_admission_shacl.reconstruct_pair()`. Cycle and lineage rules have distinct source shapes. No C-03 history test or complete cross-profile acceptance is implied.

## Vocabulary and evidence qualification module

Module 0.5.0 checks C-11/C-12 under a separately declared [application metadata policy](../evaluation/shacl/qualification/profile-review.md). The lossless `report.json.gz` stores all 47 engine executions, graph snapshots, exact oracles, source/input digests and versions; `verification.json` checks hashes and six saved graph replays. Run its builder, runner and verifier before the coverage summarizer. The vocabulary key is operational within the supplied graph; evidence roles and locators are not claim-truth judgments. Neither the HermiT denominator nor full managed-profile acceptance changes.

## C-14 release boundary review

Run `.venv-shacl/bin/python tools/review_c14_boundary.py` to reconcile the three optional catalog boundaries, their documentary representations and seven excluded bridges against the native, typed and OWL outputs. The [review](../evaluation/c14-boundary-review.md) pins all input digests and checks 12 cases from the earlier admission receipt. This is a structural readback of prior evidence, not a new SHACL or HermiT run.
