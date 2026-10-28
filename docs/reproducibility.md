# Reproduce the current checks

Use [Latest published source release](https://github.com/ArazSaieArasi3/riskium/releases/latest) for live routing. **28 October 2026 checkpoint:** published **v0.3.3**, source `3380b6b31f4830417946105e17f023118c7be6ee`, has [28 final gates, 233 software regressions and six independently verified assets](../evaluation/releases/v0.3.3-publication.json). The newer SQL 0.4.0/0.5.0/0.6.0 development and maintained documentation 0.3.0 have their own inputs and receipts. v0.3.4 is planned under #45.

To reproduce historical source checks, use a clean checkout of the exact v0.3.3 tag and install its pinned requirements. Run its source-bound checks and compare archived manifests/receipts; do not attempt to reissue the published tag or demand that current live Wiki matches old bytes. `python tools/review_distribution.py` verifies published v0.3.2/v0.3.3 selections at their exact tagged sources. To inspect current development, use current main and the commands below. A future v0.3.4 freeze needs new final-source and actual channel evidence.

Use Python 3.12 or a compatible Python 3 installation. The conceptual-model and coverage builders use the standard library. The documentation portal uses pinned RDFLib, Markdown and Beautiful Soup packages. The OWL syntax and mapping regression tests require the pinned RDFLib package.

From the repository root:

```sh
python3 tools/validate_model.py
python3 tools/review_coverage.py
python3 tools/review_references.py --check
python3 tools/build_quality_report.py --check
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r tools/publication/requirements.txt
.venv-docs/bin/python tools/build_reference.py
.venv-docs/bin/python tools/build_reference.py --check
.venv-docs/bin/python tools/publication/audit_portal.py
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

Open `http://localhost:8000/docs/current/`. The generated reference links to the model and conceptual views. Local browsing does not establish a live Pages deployment.

The builder generates the maintained portal under `docs/current/`. `docs/index.html` opens that overview and `/site/` opens its conceptual reference. Curated guide hashes are recorded separately from the immutable model source in `publication-manifest.json`. The versioned-site builder assembles current pages and registered frozen snapshots without altering the latter.

The WIDOCO reference is checked in separately. Rebuild it with the pinned 1.4.25 JDK-17 jar whose SHA-256 is `be57a270fffb91e55810fa308717e704a44e2e7c027a3d68125a49da6c8b4e2b`:

```sh
.venv-docs/bin/python tools/publication/run_widoco.py --jar /path/to/widoco-1.4.25-jar-with-dependencies_JDK-17.jar
.venv-docs/bin/python tools/publication/audit_portal.py
```

See `tools/publication/README.md` for the upstream download, post-processing and verification boundaries. The original Turtle is copied byte for byte; RDF/XML, JSON-LD and N-Triples are checked for graph isomorphism. These are serialization checks. The local explorer reads asserted OWL neighborhoods, with no inference or upload service. The [public documentation](https://arazsaiearasi3.github.io/riskium/) must be read back after each deployment before reporting publication success.

The coverage review verifies source allocation, planned constraint routes and expected fixture contracts. It detects a stale or missing stored review; regeneration with `python3 tools/review_coverage.py --write` is appropriate only after reviewing an intentional contract change.

The [reference corpus check](../references/README.md) validates the dated editorial register and its model targets offline. It checks source/use identities, frozen model bytes and required limits, then compares generated documentation and its receipt. It does not repeat online reading or establish standards conformance. The corpus retains partial-access and unassessed comparisons explicitly.

The [quality synthesis check](../evaluation/quality/README.md) reads 22 evidence artifacts at the declared checkpoint and verifies live scientific receipt bytes, exact source hashes and row-level denominators. Historical documentation/release-policy snapshots are intentionally read at that checkpoint. It regenerates the report without rerunning engines or importing expert judgments. Six regression guards prevent lost blocked cases, hidden row relabeling, error-as-mutation success, fabricated semantic percentages and retroactive rewriting of source/trace evidence.

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

Run `python3 tools/build_release_claims.py` to regenerate the [candidate release claim inventory](../evaluation/release-claims.md). It checks the source, contract, OWL and C-14 input digests before listing all remaining HermiT/SHACL constraint rows. The inventory prepares the prerelease claims; a release still needs the clean freeze and publication gates.

## Requirement and CQ traceability

The post-prerelease CQ/traceability evidence is separate from the immutable release archive and earlier formal coverage plan. Install the pinned RDFLib dependency in `.venv-owl`, then run:

```sh
.venv-owl/bin/python tools/run_cq.py --check
.venv-owl/bin/python tools/build_traceability.py --check
.venv-owl/bin/python -m unittest discover -s tests -p test_cq.py -v
```

The [contracts and supplementary profile](../requirements/cq/README.md) explain the 32 synthetic answer graphs, eight query-mutant controls and exact expected bindings. Five original synthetic-task contracts have bounded execution; the independent evidence populations for CQ06–CQ08 remain pending in #13. These queries do not execute HermiT/SHACL, prove managed admission or establish semantic acceptance. The [ledger](../evaluation/traceability/README.md) records all 28 public requirement/scope/CQ traces and their unresolved routes. Original JSON/CSV planning statuses and formal denominators are preserved.

## Database assessment mapping and assurance after v0.3.1

The separate [SQLite assessment profile 0.2.0](../implementation/relational/0.2.0/README.md) applies additive migration 3 to the unchanged public 0.1.0 base. [DRSD 0.1.0](../requirements/relational-requirements.json), [method/checklist](relational-assurance.md), [source/requirement/case trace](../evaluation/relational/assessment/traceability.md), exact dictionary and named queries identify the scope.

```sh
python tools/build_relational_assessment.py --check
python tools/run_relational_assessment.py --check
python tools/check_database_assurance.py --check
python -m unittest discover -s tests -p test_relational_assessment.py -v
```

The replay executes 48 fixed cases, 100 frozen generated inputs, two actual SHACL comparison checks and four measured workload patterns on 1,000 generated assessment/result pairs. It checks SQL/RDF answers, current schema/dictionary, populated migration, immutability, backup/restore and bounded two-connection behavior. Two deliberately weakened-rule controls are sensitivity tests, not domain records. Timings and query-plan text are recorded observations and are not required identical across engines; exact logical answers and source hashes are. The current engineering gates do not execute PostgreSQL, full private migration, real user acceptance or independent scientific adjudication.

For a reproducible public synthetic database, the supported Python helper is `relational_assessment.baseline(path)` from `tools/`; use a fresh output path. Open existing v3 databases through `relational_assessment.connect` and its health check. The old v2-only reader intentionally rejects the newer schema. No private source database or binary is needed by these checks.

## Formal reading reference

Run `python tools/build_formal_reference.py --check` to verify the source-bound [method and 25-clause explanation](formal-method.md). After an intentional evidence change, review the underlying sources and regenerate with `python tools/build_formal_reference.py`, then rebuild Pages/Wiki with `python tools/build_reference.py`. This check creates no engine outcomes and cannot turn historical NOT_RUN or PARTIAL into PASS.

## Assessment correction overlay 0.3.0

After the earlier assessment checks, run `python tools/run_relational_correction.py --check`, `python tools/build_correction_inventory.py --check` and `python -m unittest discover -s tests -p test_relational_correction.py -v` in the pinned SHACL/RDF environment. The [separate receipt](../evaluation/relational/correction/README.md) retains exact fixed correction, populated migration, history, restoration and native-RDF outcomes. This adds no native predicate or historical engine PASS.

## Cross-document reconciliation

Run `python tools/audit_consistency.py --check` for the [423-row joined source/claim table](traceability.md), source inventory, exact model/claim IDs and preserved historical denominators. This generates no new scientific results. Actual author-file, Wiki and deployed Pages readbacks are recorded separately in `evaluation/consistency/`. Recheck affected rows and the final component/source selection under #45 before v0.3.4.

## Current source/scenario and evidence development

Install both pinned SHACL and publication requirements, then reproduce each separate bounded component:

```sh
python tools/run_relational_source_scenario.py --check
python tools/build_source_scenario_inventory.py --check
python tools/run_relational_source_scenario_lineage.py --check
python tools/build_source_scenario_lineage_inventory.py --check
python tools/run_relational_evidence.py --check
python tools/build_evidence_inventory.py --check
```

Their [54-control storage](../evaluation/relational/source-scenario/completion.json), [54-control correction](../evaluation/relational/source-scenario-lineage/completion.json) and [62-control evidence](../evaluation/relational/qualified-evidence/completion.json) receipts retain different populations. The evidence implementation source passed 280 full software tests and seven hosted workflows; that is a dated engineering result, not a count inherited by future code or the original scientific suite. The v7 reader requires a validated populated v6 database; older exact-schema readers intentionally reject newer profiles. No private database is required for synthetic replay.

For maintained documentation 0.3.0, regenerate/check the shared reference, verify its [component](../evaluation/documentation/current-0.3.0/component.json) with `python tools/publication/build_documentation_component.py --check`, assemble the site and run the documentation audit. Live Wiki/Pages publication and byte readback remain separate from local source parity. No new v0.3.4 snapshot or source release is created by these commands.
