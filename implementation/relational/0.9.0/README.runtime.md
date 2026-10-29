# Execute the risk-nature history task

The development API retrieves an issued report with its original nature term, local vocabulary, context/objective versions, recording entry revisions and source qualifiers. A-v1 retains its original unfavorable report after two alternative corrections, A-v2 and A-v3. A later plain issue A-v4 stays outside their correction family. Competing B-v1 remains a separate source report.

The immutable [R1 declaration](README.md) at `805b1edecff254f1e21131aa6fd098344affb398` defines the acceptance. This implementation adds SQL 0.9.0/schema 10 under [#65](https://github.com/ArazSaieArasi3/riskium/issues/65). The published distribution remains v0.3.6; model and OWL remain 0.3.1. Integration, reader delivery and publication of proposed v0.3.7 are subsequent #66 work.

## Reproduce and inspect

Use Python 3.12 and the pinned dependencies in `tools/requirements-shacl.txt`:

```sh
python tools/build_risk_nature_schema.py --check
python -m unittest discover -s tests -p test_risk_nature.py -v
python tools/run_relational_risk_nature.py --output build/risk-nature-runtime.json
```

The replay executes the original 51 malformed requests and 59 locally executable controls against populated temporary SQLite databases. It compares complete literal rows and all triples in eight named graphs, exercises the upgrade, forbidden writes, branches, caller rollback, actual file reopen, trusted-digest restoration, two connections and measured synthetic workloads. Its successful pre-download summary is **59 PASS, zero FAIL/ERROR and one PENDING_EXTERNAL_READBACK**. It leaves control 60 pending until an actual hosted artifact is independently downloaded. This explicitly separates runtime execution from independent delivery verification.

The [hosted workflow](../../../.github/workflows/v036-versioned-suite.yml) stores three receipts in one ZIP: the source-qualified full suite, declaration verification and runtime results. After independently retrieving that ZIP and its trusted API digest:

```sh
python tools/complete_risk_nature_readback.py \
  --artifact build/hosted.zip --expected-zip-sha256 TRUSTED_API_DIGEST \
  --artifact-id ACTUAL_ARTIFACT_ID --run-id ACTUAL_RUN_ID \
  --output build/risk-nature-completed.json
```

Completion verifies the ZIP digest, inventory, clean exact source, source hashes, original declaration bytes, literal results and all malformed requests. Only then does it record control 60 and a **60 PASS** completion receipt. Actual source/run/artifact identities and independently checked outcome are recorded in #65. A digest received from the same untrusted file is insufficient to authenticate it.

## Integrate

For a verified populated schema-9 database:

```python
import sys
sys.path.insert(0, 'tools')
import relational_risk_nature as nature

db = nature.connect('research.sqlite')  # validates and upgrades 9 -> 10
answer = nature.get(db, exact_issued_nature_version_id)
row = answer['row']
# row: exact case/term/scheme/context/objective/recording-version pins,
# original narrative/provenance and explicit retrieval readiness
# answer['dependencies']: the pinned support/context/recording snapshots
# answer['sources']: verbatim original source JSON by documentary role
history = nature.family(db, explicit_root_version_id)
reports = nature.by_case(db, known_case_id)
```

Callers supply their own managed identifiers, sources and provenance. No runtime function seeds data, defaults timestamps or copies records from a fixture. `issue_support`, `issue_context`, `issue_bundle` and `declare_correction` are atomic public write operations. The `stage_*` functions are trusted transaction-internal preparation helpers; public readers require final semantic health. A bundle contains exactly `assertion`, `recording_revisions` and optional `correction` (explicit null when absent). Its fields follow the original concrete input shapes. A complete bundle issues the new recording revisions before the assertion within one transaction; any failure rolls everything back.

Known-empty cases return no reports. Unknown case/version IDs are explicit errors. Missing mandatory case/term/source cannot be issued; raw JSON can stay in the unchanged source staging store. Optional missing context yields `NOT_READY_CONTEXT_UNRECORDED`; a context without objective references yields `NOT_READY_OBJECTIVES_UNRECORDED`. Neither outcome fills in values or sources. Readiness is bounded to this documentary retrieval task.

Old schema-9 readers intentionally reject schema 10. Existing assessment, evidence and knowledge rows, guards, migration hashes, allocator values and named graphs remain protected. New base identities/entry versions add native base facts while preserving all earlier facts. No source truth, actual occurrence, independent corroboration, general classification/workflow, PostgreSQL/private migration, production SLO or organizational/independent semantic acceptance follows from these synthetic engineering results.
