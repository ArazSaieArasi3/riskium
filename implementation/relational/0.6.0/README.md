# Qualified evidence profile 0.6.0

Bounded child #44 under #35/#12 follows source/scenario correction 0.5.0. The contract and literal expected SQL/native answers are declared before implementation. C065 is a documentary subkind; C066 is a contextual role on an existing artifact, projected only within the selected reference-version graph. R-68 and RX-021 retain their native directions. The role qualifier support/challenge/context is supplementary and does not establish truth or endorsement.

One explicit issued item-version pin and one or more issued artifact target-version pins are required; raw unknown targets stay raw. No global C066 membership, new bearer identity, automatic occurrence/independent-corroboration inference or current/authoritative selection is introduced. Original source JSON, old context/version pins and correction branches are preserved.

This is a development component proposed for **planned source distribution v0.3.4**, not a public v0.6.0 model/release. Stable v0.3.3, model 0.3.1, ORSD 0.4.3, original DRSD 0.1.0, article 7.0.8 and prior component bytes remain unchanged. All eleven original organizational admissions stay WITHHELD.

## Implemented storage and projection

[Declaration checkpoint ed458f9](https://github.com/ArazSaieArasi3/riskium/commit/ed458f9b4961eefcb4330b01965964f5a8c6405c) precedes the SQL/API implementation. Migration 7 adds three STRICT tables, four indexes, insertion/immutability/seal guards, an invalid-data audit and a named evidence graph view. [The dictionary](schema-dictionary.md) reviews all columns, dependencies, key/role ownership and index rationale. Earlier tables/views/triggers and all frozen component bytes remain unchanged.

`issue` stages a qualified reference, its item pin, all target pins and its exact serialized payload in one audited transaction/savepoint, then seals them together. Inputs use explicit existing issued information-artifact versions. A later reference version can choose a different item version/source or qualification without rewriting earlier evidence. Missing target identity remains raw; duplicate target pins and multiple versions of a target artifact in one reference are rejected by this selected policy. Targets and items may be existing knowledge artifacts without replacing their identities/types or historical graphs.

[The exact-target query](queries/by_target.sql) returns all explicitly linked issued reference versions, ordered by version ID, with reference and item-version source JSON kept separate. An artifact's original source does not replace a later item version's source. Selecting an old target does not select a reference linked only to its newer version. Multiple references to the same item are not independent corroboration. The native `supportsRecordedArtifact` name is retained even for challenge/context qualification; C-12 explicitly prevents a proof/endorsement inference. R-69..R-72 are outside this projection.

The v7 reader validates all seven migration hashes, exact schema, configuration, FKs/integrity and prior v6 plus new evidence semantics. It requires a validated populated v6 database; older exact-schema readers deliberately reject v7. Controlled backup/reopen/dump recovery and rejected tampered restores execute. These checks validate engineering consistency, not documentary truth or cryptographic authenticity against administrative rewriting.

## Reproduce and follow the evidence

```bash
python tools/run_relational_evidence.py --check
python tools/build_evidence_inventory.py --check
python -m unittest discover -s tests -p test_qualified_evidence.py -v
```

[Execution](../../../evaluation/relational/qualified-evidence/report.json) contains 62 fixed controls and four independent native graph oracles; [trace](../../../evaluation/relational/qualified-evidence/traceability.json) links all six derived EQR requirements, original IDs/CQs and exact inputs; [306-row accounting](../../../evaluation/relational/qualified-evidence/mapping-accounting.json) retains historical dispositions. The six new partial routes supplement the prior eight, leaving 236 deferred source elements. This is not complete semantic/class/native acceptance. Current public docs/Wiki reconciliation, component selection and new source-distribution freeze remain the planned v0.3.4 task #45; no new release is published here.
