# Source/scenario correction lineage 0.5.0

Issue #43 is a bounded child of #35/#12, following profile 0.4.0. Requirements, policy and fixed synthetic SQL/native graph expectations were committed **before implementation**. The expected family rows are literal endpoint inputs plus a manually specified five-edge correction tree; no implementation output generated an expected answer. Graphs use unchanged native 0.4.0 directions and explicitly named versions.

The selected application policy requires issued endpoints of the same artifact, one parent per child, any number of branches and no cycles/self links. Declaration provenance is distinct from endpoint provenance. Exact root plus declared descendants is the query scope; no current/authority/corroboration selection is inferred. Plain new versions remain unlinked. Retraction, branch endorsement and general EvidenceReference/assertion correction stay deferred. The native model and mapping counts do not change.

Stable v0.3.3, model 0.3.1, ORSD 0.4.3, original DRSD 0.1.0, manuscript 7.0.8 and previous component bytes remain unchanged. All eleven original organizational admissions stay WITHHELD. Passing engineering controls is not independent semantic or operational acceptance.

## Implemented reader and declaration ownership

The [contract](contract.json) and [literal oracles](fixtures.json) were committed at [5cdd9a2](https://github.com/ArazSaieArasi3/riskium/commit/5cdd9a26fa4fd003f5b2f2d4dc3fcea478b8f5a2) before the SQL/API implementation. Migration 6 adds only `knowledge_correction`, two indexes, guards and a semantic invalid-data view. The [dictionary](schema-dictionary.md) reviews all seven columns, keys, functional dependency, index rationale and ownership diagram.

`declare` records an explicit retrospective assertion between already issued exact versions. `issue_corrected` atomically stages/seals a new knowledge version and its declaration; failure removes the new version and its identity, including inside a caller's outer transaction. `issue` adds a plain unlinked version. The old v5 native views remain unchanged; use the v6 reader for v6 databases. The reader does not silently bootstrap an empty database: upgrade a populated, validated v5 database.

Declarations cannot be updated, deleted or replaced. A mistaken declaration needs a separately reviewed future retraction/selection policy; this bounded profile does not silently erase it. A declaration may use a different documentary source from either endpoint. All three attributions remain separate. The original narrative, exact context versions, original JSON, source locators and interpretation origins are preserved. The declaration time must not precede either endpoint timestamp; recording order of the endpoints itself does not establish authority.

[The bound family query](queries/family.sql) returns the exact root and all declared descendants once, sorted by version ID. Selecting a child returns its subtree, not siblings or ancestors; that row's parent metadata remains visible. Same-label artifacts remain distinct. New versions have no implicit correction edge, and no branch is selected as current or endorsed. Multiple related versions are not counted as independent sources.

## Reproduce

Install the repository's pinned SHACL/publication requirements, then run:

```bash
python tools/run_relational_source_scenario_lineage.py --check
python tools/build_source_scenario_lineage_inventory.py --check
python -m unittest discover -s tests -p test_source_scenario_lineage.py -v
```

[Execution evidence](../../../evaluation/relational/source-scenario-lineage/report.json) covers 54 fixed controls: 20 positive, 31 rejection/rollback controls (including failed migration), and three actual weakened-rule/wrong-join mutations. Ten independently fixed native graph oracles compare old and new issued versions. Focused regressions add nested transaction, atomic-child mismatch, alternate-parent, raw SQL calendar, endpoint timestamp, three-node cycle, old-audit and explicit-reader-version boundaries. [Trace](../../../evaluation/relational/source-scenario-lineage/traceability.json) binds six derived SCL requirements to original IDs, CQs, exact cases and implementation; [306-element accounting](../../../evaluation/relational/source-scenario-lineage/mapping-accounting.json) retains all prior dispositions. The historical 423-row release trace is unchanged.

This application correction component adds **zero** native classes, predicates or mapping routes. The previous eight partial source/scenario routes and 242 deferred core mappings retain their scope. General EvidenceReference/assertion correction, retraction/branch selection, remaining native/formal semantics and real deployment acceptance are still open. No stable asset, article, organizational admission or independent rating is changed by this engineering packet.
