"""Replay fixed qualified-evidence answers, contextual graphs, migration and recovery."""
import argparse
from collections import Counter
import copy
import hashlib
import json
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

from rdflib import Graph, RDF, URIRef
from rdflib.compare import isomorphic
import relational_history as b
import relational_assessment as a
import relational_source_scenario as k
import relational_source_scenario_lineage as l
import relational_evidence as e
import run_relational_source_scenario_lineage as previous
from run_relational_assessment import graph as assessment_graph

ROOT = e.ROOT
OUT = ROOT / 'evaluation/relational/qualified-evidence'
INPUTS = ['implementation/relational/0.6.0/' + n for n in ('contract.json', 'fixtures.json', '007_qualified_evidence.sql', 'queries/by_target.sql')]
INPUTS += ['tools/relational_evidence.py', 'tools/run_relational_evidence.py']


def fixture():
    return json.loads((e.OUT / 'fixtures.json').read_text())


def prior(path=':memory:'):
    db = previous.fresh(path)
    previous.populate(db)
    for row in fixture()['sources']:
        db.execute('INSERT INTO source_record VALUES(?,?)', row)
    for item in fixture()['items']:
        if not db.execute('SELECT 1 FROM information_artifact WHERE artifact_id=?', (item['artifact_id'],)).fetchone():
            b.add_identity(db, item['artifact_id'], 'artifact')
            db.execute('INSERT INTO information_artifact(artifact_id,kind,label,source_record_id) VALUES(?,?,?,?)', (item['artifact_id'], 'RKM-C014', item['label'], item['source_record_id']))
        a.stage_version(db, item['version_id'], item['artifact_id'], payload=item['payload'], source=item['source_record_id'])
        a.seal(db, item['version_id'], '2026-10-28T00:00:00Z')
    return db


def fresh(path=':memory:'):
    db = prior(path)
    e.migrate(db)
    return db


def populate(db):
    for record in fixture()['records']:
        e.issue(db, record)


def state(db):
    return dict(rows=e.snapshot(db), schema=b.schema_snapshot(db), version=db.execute('PRAGMA user_version').fetchone()[0])


def state_hash(db):
    return hashlib.sha256(json.dumps(state(db), sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def expected_graph(version):
    graph = Graph()
    data = fixture()['graphs'][version]
    for subject, kind in data['types']:
        graph.add((URIRef(subject), RDF.type, URIRef(k.RISK + kind)))
    for subject, predicate, obj in data['edges']:
        graph.add((URIRef(subject), URIRef(k.RISK + predicate), URIRef(obj)))
    return graph


def knowledge_graph(db, version):
    graph = Graph()
    for s, p, o in db.execute('SELECT subject,predicate,object FROM v_knowledge_quads WHERE graph_id=?', (version,)):
        graph.add((URIRef(s), URIRef(p), URIRef(o)))
    return graph


def query_rows(db, sql, target):
    rows = [list(row) for row in db.execute(sql, {'target': target})]
    for row in rows:
        row[13] = json.loads(row[13])
    return rows


def execute():
    f = fixture()
    rows = []

    def add(ident, expected, observed, kind='positive', detail=None):
        rows.append(dict(id=ident, kind=kind, expected=expected, observed=observed,
                         status='PASS' if expected == observed else 'FAIL', detail=detail))

    db = prior()
    before = e.legacy_snapshot(db)
    knowledge = {name: knowledge_graph(db, k.U(name)) for name in previous.fixture()['graphs']}
    assessments = [assessment_graph(db, a.U('a1-v' + str(i))) for i in (1, 2, 3)]
    lineage = l.family(db, k.U('scenario-a-v1'))['rows']
    e.migrate(db)
    add('POPULATED_UPGRADE', True, before == e.legacy_snapshot(db))
    add('LEGACY_GRAPHS_PRESERVED', True, all(isomorphic(g, knowledge_graph(db, k.U(name))) for name, g in knowledge.items())
        and all(isomorphic(g, assessment_graph(db, a.U('a1-v' + str(i + 1)))) for i, g in enumerate(assessments)))
    # Read the unchanged v6 query directly after v7 health; an older exact-schema reader rejects v7.
    e.health(db)
    old_rows = [list(row) for row in db.execute((l.OUT / 'queries/family.sql').read_text(), {'root': k.U('scenario-a-v1')})]
    for row in old_rows:
        row[9], row[10] = json.loads(row[9]), json.loads(row[10])
    add('LINEAGE_PRESERVED', lineage, old_rows)
    before = state_hash(db)
    e.migrate(db)
    add('IDEMPOTENT_UPGRADE', before, state_hash(db))
    db.close()
    db = prior()
    before = dict(rows=l.snapshot(db), schema=b.schema_snapshot(db), version=6)
    with patch.object(e, 'migration_text', return_value=e.migration_text() + '\nINSERT INTO missing_evidence_table VALUES(1);\n'):
        try:
            e.migrate(db)
            rejected = False
        except sqlite3.OperationalError:
            rejected = True
    add('FAILED_UPGRADE', True, rejected and before == dict(rows=l.snapshot(db), schema=b.schema_snapshot(db),
        version=db.execute('PRAGMA user_version').fetchone()[0]), 'negative')
    db.close()
    db = fresh()
    populate(db)
    for ident, target in [('TARGET_OLD', 'scenario-a-v1'), ('TARGET_NEW', 'scenario-a-v2'), ('MULTIPLE_TARGETS', 'scenario-b-v1')]:
        add(ident, f['answers'][target], e.by_target(db, k.U(target))['rows'])
    add('PROVENANCE_EXACT', f['answers']['scenario-a-v1'][1], e.by_target(db, k.U('scenario-a-v1'))['rows'][1])
    add('ITEM_OLD_PIN', e.U('item-a-v1'), e.by_target(db, k.U('scenario-a-v1'))['rows'][0][4])
    item_role = (URIRef(e.U('item-a')), RDF.type, URIRef(k.RISK + 'RKM-C066'))
    add('ROLE_CONTEXTUAL', True, item_role in e.native_graph(db, e.U('ref-a-v1'))
        and not len(e.native_graph(db, e.U('item-a-v1')))
        and db.execute('SELECT kind FROM information_artifact WHERE artifact_id=?', (e.U('item-a'),)).fetchone()[0] == 'RKM-C014'
        and not db.execute("SELECT 1 FROM artifact_typing WHERE native_class='RKM-C066'").fetchone())
    combined = Graph()
    for record, ident in zip(f['records'], ['NATIVE_REFERENCE_A1', 'NATIVE_REFERENCE_A2', 'NATIVE_REFERENCE_B1', 'NATIVE_REFERENCE_C1']):
        expected = expected_graph(record['version_id'])
        actual = e.native_graph(db, record['version_id'])
        add(ident, True, isomorphic(expected, actual), detail=dict(expected_nt=sorted(expected.serialize(format='nt').splitlines()), observed_nt=sorted(actual.serialize(format='nt').splitlines())))
        for triple in actual:
            combined.add(triple)
    forbidden = {k.RISK + x for x in ('RKM-C004', 'RKM-C007', 'R-69', 'R-70', 'R-71', 'R-72')}
    add('NO_IMPLICIT_ENDORSEMENT', True, not any(str(p) in forbidden or str(o) in forbidden for _, p, o in combined)
        and e.by_target(db, k.U('scenario-a-v1'))['endorsement'] == 'NOT_INFERRED'
        and {r[2] for target in ('scenario-a-v1', 'scenario-a-v2') for r in e.by_target(db, k.U(target))['rows']} == {'support', 'challenge', 'context'})
    add('RAW_EXCLUSION', True, not db.execute('SELECT 1 FROM identity_registry WHERE resource_id=?', (e.U('raw-document'),)).fetchone()
        and not len(e.native_graph(db, e.U('raw-document'))))
    add('DUPLICATE_LABEL_IDENTITIES', 3, db.execute('SELECT count(DISTINCT artifact_id) FROM evidence_reference_type').fetchone()[0])
    add('BOUND_PARAMETER', [], e.by_target(db, "'; DROP TABLE evidence_snapshot; --")['rows'])
    before = state_hash(db)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'backup.sqlite'
        target = b.connect(path)
        db.backup(target)
        target.close()
        target = e.connect(path)
        add('BACKUP_REOPEN', before, state_hash(target))
        target.close()
        path = Path(directory) / 'live.sqlite'
        target = fresh(path)
        populate(target)
        target.close()
        target = e.connect(path)
        add('FILE_REOPEN', before, state_hash(target))
        target.close()
    dump = '\n'.join(db.iterdump())
    target = b.connect()
    e.restore_dump(target, dump)
    add('DUMP_RESTORE', before, state_hash(target))
    target.close()
    sql = (e.OUT / 'queries/by_target.sql').read_text()
    changed = sql.replace('items.record_id=iv.source_record_id', 'items.record_id=e.source_record_id')
    add('MUTANT_SOURCE_JOIN_EXPOSED', False, f['answers']['scenario-a-v1'] == query_rows(db, changed, k.U('scenario-a-v1')), 'mutation')
    actual = e.native_graph(db, e.U('ref-a-v1'))
    triple = (URIRef(e.U('ref-a')), URIRef(k.RISK + 'RX-021'), URIRef(e.U('item-a')))
    actual.remove(triple)
    actual.add((triple[2], triple[1], triple[0]))
    add('MUTANT_DIRECTION_EXPOSED', False, isomorphic(expected_graph(e.U('ref-a-v1')), actual), 'mutation')
    db.execute('DROP TRIGGER evidence_target_delete')
    db.execute('DELETE FROM evidence_target WHERE version_id=?', (e.U('ref-a-v1'),))
    add('MUTANT_IMMUTABILITY_EXPOSED', False, f['answers']['scenario-a-v1'] == query_rows(db, sql, k.U('scenario-a-v1')), 'mutation')
    db.close()
    db = fresh()
    record = dict(f['records'][0], target_version_ids=[])
    trigger = db.execute("SELECT sql FROM sqlite_master WHERE name='evidence_seal'").fetchone()[0]
    start = trigger.index(" SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_invalid WHERE version_id=NEW.version_id AND code='CARDINALITY')")
    end = trigger.index(" SELECT CASE WHEN EXISTS(SELECT 1 FROM v_evidence_invalid WHERE version_id=NEW.version_id AND code='PAYLOAD')", start)
    changed = (trigger[:start] + trigger[end:]).replace('SELECT 1 FROM v_evidence_invalid WHERE version_id=NEW.version_id)', "SELECT 1 FROM v_evidence_invalid WHERE version_id=NEW.version_id AND code<>'CARDINALITY')")
    db.execute('DROP TRIGGER evidence_seal')
    db.execute(changed)
    e.stage(db, record)
    a.seal(db, record['version_id'], record['recorded_at'])
    add('MUTANT_CARDINALITY_EXPOSED', 1, db.execute('SELECT is_issued FROM version_snapshot WHERE version_id=?', (record['version_id'],)).fetchone()[0], 'mutation')
    db.close()
    db = fresh()
    e.stage(db, f['records'][0])
    e.health(db)
    add('UNISSUED_EXCLUDED', [], list(e.native_graph(db, f['records'][0]['version_id'])))
    db.close()
    for ident, diagnostic in f['rejection_diagnostics'].items():
        db = fresh()
        record = copy.deepcopy(f['records'][0])
        if ident in ('DUPLICATE_VERSION', 'UPDATE_SNAPSHOT', 'DELETE_SNAPSHOT', 'REPLACE_SNAPSHOT', 'UPDATE_TARGET', 'DELETE_TARGET', 'REPLACE_TARGET', 'LATE_TARGET'):
            e.issue(db, record)
        if ident == 'CONFIGURATION_OFF':
            db.execute('PRAGMA foreign_keys=OFF')
        if ident in ('UNISSUED_ITEM', 'UNISSUED_TARGET'):
            a.stage_version(db, e.U('unissued-version'), e.U('item-a'))
        before = state(db)
        target_rollback = True
        try:
            with b.transaction(db):
                if ident == 'NO_TARGET':
                    record['target_version_ids'] = []
                elif ident in ('MISSING_TARGET', 'ATOMIC_BUNDLE_FAILURE'):
                    record['target_version_ids'].append(e.U('absent'))
                elif ident == 'UNISSUED_TARGET':
                    record['target_version_ids'] = [e.U('unissued-version')]
                elif ident == 'DUPLICATE_TARGET':
                    record['target_version_ids'] *= 2
                elif ident == 'TWO_VERSIONS_ONE_TARGET':
                    record['target_version_ids'].append(k.U('scenario-a-v2'))
                elif ident == 'MISSING_ITEM':
                    record['item_version_id'] = e.U('absent')
                elif ident == 'UNISSUED_ITEM':
                    record['item_version_id'] = e.U('unissued-version')
                elif ident == 'WRONG_REF_KIND':
                    record['artifact_id'] = a.BASE('context')
                elif ident == 'CONFLICTING_TYPING':
                    record['artifact_id'] = k.U('scenario-a')
                elif ident == 'MISSING_SOURCE':
                    record['source_record_id'] = e.U('absent')
                elif ident == 'EMPTY_PROVENANCE':
                    record['source_locator'] = ' '
                elif ident == 'BAD_CALENDAR':
                    record['recorded_at'] = '2026-02-30T00:00:00Z'
                elif ident == 'INVALID_ROLE':
                    record['evidential_role'] = 'proven'
                elif ident == 'NONTEXT_INPUT':
                    record['statement'] = 0
                if ident == 'TARGET_OWNER_MISMATCH':
                    e.stage(db, record)
                    db.execute('INSERT INTO evidence_target VALUES(?,?,?)', (record['version_id'], k.U('scenario-b'), k.U('scenario-a-v2')))
                elif ident in ('ITEM_OWNER_MISMATCH', 'SOURCE_MISMATCH', 'OWNER_MISMATCH'):
                    e.stage(db, record)
                    forged = dict(record, version_id=e.U('forged-v1'))
                    a.stage_version(db, forged['version_id'], e.U('item-a') if ident == 'OWNER_MISMATCH' else forged['artifact_id'], payload=e.payload(forged), source=forged['source_record_id'])
                    forged['item_id'] = e.U('item-b') if ident == 'ITEM_OWNER_MISMATCH' else e.U('item-a')
                    if ident == 'SOURCE_MISMATCH':
                        forged['source_record_id'] = e.U('document-b')
                    db.execute('INSERT INTO evidence_snapshot VALUES(?,?,?,?,?,?,?,?,?,?)', tuple(forged[key] for key in e.FIELDS))
                elif ident in ('PAYLOAD_DRIFT', 'SEAL_SMUGGLE'):
                    e.stage(db, record)
                    if ident == 'PAYLOAD_DRIFT':
                        db.execute("UPDATE version_snapshot SET payload_json=json_set(payload_json,'$.statement','forged') WHERE version_id=?", (record['version_id'],))
                        a.seal(db, record['version_id'], record['recorded_at'])
                    else:
                        db.execute("UPDATE version_snapshot SET payload_json=json_set(payload_json,'$.statement','forged'),issued_at=?,is_issued=1 WHERE version_id=?", (record['recorded_at'], record['version_id']))
                elif ident in ('UPDATE_SNAPSHOT', 'DELETE_SNAPSHOT', 'UPDATE_TARGET', 'DELETE_TARGET'):
                    table = 'evidence_snapshot' if ident.endswith('SNAPSHOT') else 'evidence_target'
                    db.execute(('UPDATE ' + table + ' SET version_id=version_id') if ident.startswith('UPDATE') else 'DELETE FROM ' + table)
                elif ident in ('REPLACE_SNAPSHOT', 'REPLACE_TARGET'):
                    table = 'evidence_snapshot' if ident.endswith('SNAPSHOT') else 'evidence_target'
                    db.execute('INSERT OR REPLACE INTO ' + table + ' SELECT * FROM ' + table)
                elif ident == 'LATE_TARGET':
                    db.execute('INSERT INTO evidence_target VALUES(?,?,?)', (record['version_id'], k.U('scenario-b'), k.U('scenario-b-v1')))
                elif ident == 'LEDGER_DRIFT':
                    db.execute("UPDATE schema_migration SET sha256='forged' WHERE version=7")
                    e.health(db)
                elif ident == 'SCHEMA_DRIFT':
                    db.execute('DROP INDEX evidence_by_target')
                    e.health(db)
                elif ident == 'CONFIGURATION_OFF':
                    e.health(db)
                elif ident.startswith('RESTORE_'):
                    lines = []
                    for line in dump.splitlines():
                        if line.startswith('INSERT INTO "evidence_snapshot"') and e.U('ref-a-v1') in line:
                            if ident == 'RESTORE_PAYLOAD_TAMPER':
                                line = line.replace('Source presented as support', 'tampered statement')
                            elif ident == 'RESTORE_ITEM_TAMPER':
                                line = line.replace("'" + e.U('item-a') + "'", "'" + e.U('item-b') + "'")
                            elif ident == 'RESTORE_ROLE_TAMPER':
                                line = line.replace("'support'", "'proven'")
                        lines.append(line)
                    target = b.connect()
                    target.execute('PRAGMA ignore_check_constraints=ON')
                    try:
                        e.restore_dump(target, '\n'.join(lines))
                    finally:
                        target_rollback = b.schema_snapshot(target) == [] and target.execute('PRAGMA user_version').fetchone()[0] == 0
                        target.close()
                else:
                    e.issue(db, record)
            observed = 'ACCEPTED'
        except (ValueError, sqlite3.DatabaseError) as exc:
            observed = diagnostic if diagnostic in str(exc) else 'WRONG_DIAGNOSTIC: ' + str(exc)
        unchanged = before == state(db) and target_rollback
        add(ident, diagnostic, observed, 'negative', dict(rollback_preserved=unchanged))
        if not unchanged:
            rows[-1]['status'] = 'FAIL'
        db.close()
    if len(rows) != len(set(f['case_ids'])) or {row['id'] for row in rows} != set(f['case_ids']):
        raise ValueError('Lost/duplicate predeclared qualified-evidence case IDs')
    rows.sort(key=lambda row: row['id'])
    return dict(schema='riskium-qualified-evidence-execution-v1', profile='0.6.0', schema_version=7,
                runtime=dict(sqlite=sqlite3.sqlite_version, scope='Actual local engine; hosted replay reports its own runtime.'),
                inputs_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in INPUTS},
                summary=dict(cases=len(rows), outcomes=dict(Counter(row['status'] for row in rows)), kinds=dict(Counter(row['kind'] for row in rows)), native_graph_oracles=4),
                cases=rows, independent_semantic_validation=False, stable_distribution_changed=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    report = execute()
    if report['summary']['outcomes'] != {'PASS': len(fixture()['case_ids'])}:
        print(json.dumps([row for row in report['cases'] if row['status'] != 'PASS'], indent=2))
        raise SystemExit('Qualified-evidence oracle mismatch')
    target = OUT / 'report.json'
    if args.check:
        expected = json.loads(target.read_text())
        for key in ('inputs_sha256', 'summary', 'cases'):
            if report[key] != expected[key]:
                raise ValueError('Stale qualified-evidence execution: ' + key)
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status='QUALIFIED_EVIDENCE_EXECUTION_PASS', sqlite=sqlite3.sqlite_version, **report['summary'])))


if __name__ == '__main__':
    main()
