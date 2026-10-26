# Executed assessment-correction overlay 0.3.0

Bounded task #40 is a child of #35/#12. The [predeclared contract](../../../implementation/relational/0.3.0/contract.json) and [fixed values/lineage oracles](../../../implementation/relational/0.3.0/fixtures.json) preceded implementation at `753dccdce0865c6cbd3400aa245cea1b2e26d0d6`. A documented COR-04 source-ID citation amendment corrects RKRS-05 to RKRS-06 without changing the expected answers or task meaning.

The [receipt](report.json) records **36/36 matching scenarios**, including two deliberately weakened-rule controls and three exact native RDF graph comparisons. A passing negative case means the intended rejection and rollback occurred; mutation controls deliberately expose forbidden behavior and are not admitted domain records. Cases include populated migration 4, failed migration rollback, immutable old/new values, conflicting branches, separate source qualifiers, missing/unissued/cross-identity/self/cyclic parents, replacement/update/delete rejection, canonical calendar/time checks, partial bundle rollback, staged-data exclusion, schema/ledger/configuration drift, backup/file reopen and dump restoration. Native expected graphs come from the earlier hand-authored fixture oracle with only the explicitly selected version identifiers replaced.

Each row records expected and observed results. Large before/after storage states are represented by canonical SHA-256 fingerprints covering every selected row, schema definition, ledger and user_version; the source/fixtures permit reproduction. Native RDF comparison rows retain the full expected and observed N-Triples. The receipt records the execution checkout plus exact evaluated input digests; later commits and hosted replays bind implementation publication separately.

[All 306 native-element dispositions](mapping-accounting.json) retain the preceding profile's accounting categories and source hashes. There are **zero new native class/property mappings**: this relation is supplementary application history. The existing 250 incomplete core mappings and 11 external elements are not relabeled as implemented. [Five correction requirements and their cases](traceability.json) connect original ORSD clauses, implementation, fixtures and results. [The independent development component](../../../implementation/relational/0.3.0/component.json) pins all evaluated files and generated accounting. Earlier DRSD 0.1.0, components and release assets remain historical and unchanged.

## Reproduce

```sh
python tools/run_relational_correction.py --check
python tools/build_correction_inventory.py --check
python -m unittest discover -s tests -p test_relational_correction.py -v
```

Use the pinned `tools/requirements-shacl.txt` environment for native RDF comparisons. Bare `run_relational_correction.py` writes a fresh receipt; review changed inputs before regenerating metadata with `build_correction_inventory.py`. Hosted candidate and post-release workflows run both checks. The original history and assessment runners remain separate regression populations.

## Limits and next work

The overlay relates issued versions of one assessment identity and preserves all declared branches. It does not infer source truth, independent corroboration, actual occurrence, workflow permission, general assertion/scenario correction or an authoritative latest value. Source/scenario mapping remains #35; broad SQL coverage remains #12. All eleven organizational identities stay WITHHELD. Engine-specific NOT_RUN/PARTIAL and owner/independent-review statuses are unchanged.

Schema/ledger checks and data audits detect the declared drift and invalid restored relationships; they do not authenticate a plausible administrative rewrite of a reason. Administrative bypass, PostgreSQL/private migration, real workloads and user acceptance remain outside this packet. No new stable source distribution or manuscript acceptance is inferred. Cross-document reconciliation #39 is the next release gate before the next stable freeze.
