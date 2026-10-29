# Assessment selection 0.8.0

This development component lets an application retrieve the complete assessment bundle explicitly selected in one decision context at a stated ledger boundary. It adds SQLite migration 9 and a local Python API under [#61](https://github.com/ArazSaieArasi3/riskium/issues/61). The published source distribution remains v0.3.5; v0.3.6 has not been released.

Suppose X selects A-v1 and later A-v2, while Y selects A-v3. Withdrawing A-v2 in X yields WITHDRAWN with an empty result bundle. X's earlier answer still identifies A-v2, and Y still identifies A-v3. An explicit later choice of A-v3 in X is allowed. CLEAR removes X's current pointer while retaining its history and withdrawal notices. A withdrawn version cannot be selected again in that context in this profile.

Selection returns every result owned by the chosen assessment version, with its original source and context, method, scale, dimension, basis and temporal pins. Competing values remain separate rows. UNKNOWN remains null. Decision context is supplementary application metadata, distinct from the native assessment context. A selection records a choice; direct comparability and task readiness require their existing checks.

## Use and reproduce

Use Python 3.12 and the pinned dependencies in `tools/requirements-shacl.txt`. SQLite must support the existing STRICT-table profile. The execution report records the actual local and hosted versions separately.

```sh
python -m pip install -r tools/requirements-shacl.txt
python tools/run_assessment_selection.py --output build/asl-report.json
python -m unittest discover -s tests -p test_assessment_selection.py -v
```

The replay creates disposable synthetic databases, upgrades populated schema 8, and compares actual answers with the 44 original expectations. Expected summary: 44 PASS, zero FAIL and zero ERROR. The additional suite covers 12 API, source, timestamp, transaction and restore boundaries. [Actual results and limits](../../../evaluation/relational/assessment-selection/README.md) distinguish those executions from the unchanged declaration.

For an existing validated schema-8 database:

```python
import sys
sys.path.insert(0, "tools")
import relational_assessment_selection as selection

db = selection.connect("research.sqlite")  # validates and upgrades to schema 9
answer = selection.selection(db, assessment_id, decision_context_id, as_of_sequence)
# answer: state, assessment_version, assessment, results, decisions and ledger bound
```

Callers supply real managed IDs and an explicit integer boundary from 0 to the current assessment-ledger head. Unknown assessment IDs, blank contexts and invalid boundaries are errors. A known assessment with no decision in that context returns NO_SELECTION. There is no automatic latest-version rule.

| Operation | Behavior |
| --- | --- |
| `append(db, event)` | Append SELECT, WITHDRAW or CLEAR with all declared provenance; return its assigned sequence. |
| `selection(db, assessment, context, as_of_sequence)` | Return the exact whole bundle or an empty NO_SELECTION/WITHDRAWN result, plus scoped decision history. |
| `issue(db, assessment, results, correction=None)` | Atomically issue a bundle at its supplied recorded timestamp and optionally reuse the existing same-assessment correction relation. |
| `family(db, root)` | Retain original and all declared correction branches with their source-qualified values. |
| `compare(db, left, right)` | Apply the existing exact-pin comparison policy to explicit result versions. |
| `health`, `migrate`, `connect` | Check schema, ledger, allocator, configuration and current/prior data before access. |
| `restore_dump(db, text, expected_state_sha256)` | Restore atomically and compare with a separately retained trusted logical-state digest. |

An event requires `event_id`, `kind`, `assessment_id`, `decision_context_id`, `target_version`, `actor`, `reason`, `source_record_id`, `source_locator`, `interpretation_origin` and `recorded_at`. Target is an exact issued assessment version for SELECT/WITHDRAW and null for CLEAR. IDs and decision provenance are never filled from the fixture by the runtime. Actor attribution does not enforce organizational authority.

## Sources and preservation

The [contract](contract.json) and [44 expectations](fixtures.json) were committed at `071b948dd46881f7456f0b501a55eafd963d2cce`. The [seven concrete bundles and literal graph oracles](execution-fixture.json) were committed before runtime code at `753309d6a8e21d585b35a61968beb894027e4ff1`. They remain unchanged; actual results are stored separately.

[Schema and transaction review](schema-dictionary.md) explains every new field, key, index and recovery boundary. Original model 0.3.1, source requirements, old migrations, 687 selected v0.3.5 inputs and native graph meanings remain intact. New decisions add no native predicate or class.

Schema-8 readers intentionally refuse schema 9. This API covers the declared assessment task; it does not advertise a general replacement for every earlier API. Exact release integration and current Wiki/Pages explanation remain subsequent #61/R3–R5 work. General assertion mapping, reinstatement, formulas, authorization, private/PostgreSQL migration and conference acceptance retain their separate criteria.
