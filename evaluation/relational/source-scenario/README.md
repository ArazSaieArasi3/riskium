# Executed source/scenario engineering evidence — 0.4.0

The predeclared [contract](../../../implementation/relational/0.4.0/contract.json) and [fixed answers](../../../implementation/relational/0.4.0/fixtures.json) bind this controlled synthetic task. Declaration preceded implementation in the issue #42 checkpoint. The original ORSD/DRSD, article and scientific engine receipts remain unchanged.

[Report](report.json) records **54 fixed checks**: 23 positive, 28 rejection/rollback and three mutation controls. Six native graph answers are hand-authored independently of the SQL view and compared by RDF isomorphism, including old/new versions and the direction of hasSourceReference. Queries preserve six explicit histories for case1 and two for case2, with exact documentary JSON, locator and interpretation. Equal labels do not become identity keys. Unknown context is unasserted; raw/withheld candidates create no case, scenario, occurrence or causal contributor.

Actual populated v4→v5 migration preserves old assessment/version graphs and correction branches. Idempotence and failed-upgrade rollback run. Recovery includes SQLite backup, file reopen and controlled dump restore; tampered restored semantics, ledger/schema drift and disabled FK configuration are rejected. Negative cases match their declared diagnostic and check that all failed writes roll back. Two deliberately weakened SQL guards admit an invalid case/link state, exposing the protection they remove; an additional reversed native edge fails its graph oracle. Software regressions add a wrong documentary join and same-update payload/source tampering controls.

The [306-element inventory](mapping-accounting.json) keeps original hashes and historical dispositions, adding bounded routes for **two classes, four relations and two inherited typing routes**. There are 242 still-deferred routes plus eight new partial routes; the earlier historical 250-incomplete denominator is not relabeled as complete mapping. Eleven external elements remain external. The [six-requirement trace](traceability.json) connects SSC-01..06 to original requirements, CQ02/CQ06/CQ08, schema/query files and executed case IDs. The separately hashed [component](../../../implementation/relational/0.4.0/component.json) does not alter the immutable stable v0.3.3 selection or historical 423-row release trace.

The report records its actual SQLite engine version; --check re-executes the cases and verifies source bindings/observed results while printing the CI engine separately. No real organizational case admission, independent judgment, whole-ontology semantic validity, full FOL/native rule execution, production workload or PostgreSQL/private migration is established.

```bash
python tools/run_relational_source_scenario.py --check
python tools/build_source_scenario_inventory.py --check
python -m unittest discover -s tests -p test_source_scenario.py -v
```

Completion/hosted CI bindings are recorded separately after the final implementation source is pushed. #35/#12 remain open for general assertion correction, broader mappings and their acceptance criteria. The next finite packet should address versioned source-qualified assertion correction without treating corrections as independent corroboration.
