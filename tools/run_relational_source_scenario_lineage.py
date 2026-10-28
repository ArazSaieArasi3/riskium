"""Execute predeclared source/scenario correction, history, native and recovery oracles."""
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
import run_relational_source_scenario as previous
from run_relational_assessment import graph as assessment_graph

ROOT = l.ROOT
OUT = ROOT / 'evaluation/relational/source-scenario-lineage'
INPUTS = ['implementation/relational/0.5.0/' + name for name in (
    'contract.json', 'fixtures.json', '006_source_scenario_lineage.sql', 'queries/family.sql')]
INPUTS += ['tools/relational_source_scenario_lineage.py', 'tools/run_relational_source_scenario_lineage.py']


def fixture():
    return json.loads((l.OUT / 'fixtures.json').read_text())


def prior(path=':memory:'):
    db = previous.fresh(path)
    previous.populate(db)
    return db


def fresh(path=':memory:'):
    db = prior(path)
    l.migrate(db)
    db.execute('INSERT INTO source_record VALUES(?,?)', fixture()['declaration_source'])
    return db


def populate(db):
    f = fixture()
    edges = {e['corrected_version_id']: e for e in f['declared_edges']}
    for e in f['declared_edges']:
        if e['corrected_version_id'] in {k.U('scenario-a-v2'), k.U('reference-a-v2')}:
            l.declare(db, e)
    for record in f['new_records']:
        if record['version_id'] in edges:
            l.issue_corrected(db, record, edges[record['version_id']])
        else:
            l.issue(db, record)


def state(db):
    return dict(rows=l.snapshot(db), schema=b.schema_snapshot(db), version=db.execute('PRAGMA user_version').fetchone()[0])


def state_hash(db):
    return hashlib.sha256(json.dumps(state(db), sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def expected_graph(name):
    def uri(value):
        return URIRef(a.BASE(value[1:]) if value.startswith('@') else k.U(value))
    data = fixture()['graphs'][name]
    graph = Graph()
    for subject, kind in data['types']:
        graph.add((uri(subject), RDF.type, URIRef(k.RISK + kind)))
    for subject, predicate, obj in data['edges']:
        graph.add((uri(subject), URIRef(k.RISK + predicate), uri(obj)))
    return graph


def execute():
    f = fixture()
    rows = []

    def add(ident, expected, observed, kind='positive', detail=None):
        rows.append(dict(id=ident, kind=kind, expected=expected, observed=observed,
                         status='PASS' if expected == observed else 'FAIL', detail=detail))

    db = prior()
    old = l.legacy_snapshot(db)
    native = {name: k.native_graph(db, k.U(name)) for name in previous.fixture()['graphs']}
    assessments = [assessment_graph(db, a.U('a1-v' + str(i))) for i in (1, 2, 3)]
    l.migrate(db)
    add('POPULATED_UPGRADE', True, old == l.legacy_snapshot(db))
    add('LEGACY_NATIVE_PRESERVED', True,
        all(isomorphic(graph, l.native_graph(db, k.U(name))) for name, graph in native.items())
        and all(isomorphic(graph, assessment_graph(db, a.U('a1-v' + str(i + 1)))) for i, graph in enumerate(assessments)))
    before = state_hash(db)
    l.migrate(db)
    add('IDEMPOTENT_UPGRADE', before, state_hash(db))
    db.close()
    db = prior()
    before = dict(rows=k.snapshot(db), schema=b.schema_snapshot(db), version=5)
    with patch.object(l, 'migration_text', return_value=l.migration_text() + '\nINSERT INTO missing_lineage_table VALUES(1);\n'):
        try:
            l.migrate(db)
            rejected = False
        except sqlite3.OperationalError:
            rejected = True
    add('FAILED_UPGRADE', True, rejected and before == dict(rows=k.snapshot(db), schema=b.schema_snapshot(db),
        version=db.execute('PRAGMA user_version').fetchone()[0]), 'negative')
    db.close()
    db = fresh()
    before = {name: l.native_graph(db, k.U(name)) for name in previous.fixture()['graphs']}
    populate(db)
    for ident, root in [('SCENARIO_BRANCHES', 'scenario-a-v1'), ('REFERENCE_BRANCHES', 'reference-a-v1'),
                        ('DESCENDANT_ROOT', 'scenario-a-v2'), ('EQUAL_LABEL_SINGLETON', 'scenario-b-v1'),
                        ('UNKNOWN_ROOT', 'missing')]:
        add(ident, f['families'][root], l.family(db, k.U(root))['rows'])
    add('PLAIN_VERSION_UNLINKED', [f['families'][x] for x in ('reference-b-v1', 'reference-b-v2')],
        [l.family(db, k.U(x))['rows'] for x in ('reference-b-v1', 'reference-b-v2')])
    add('PROVENANCE_SEPARATE', f['families']['scenario-a-v1'][1],
        l.family(db, k.U('scenario-a-v1'))['rows'][1])
    add('ORIGINAL_CONTEXT_PIN', [a.BASE('context-v1')], l.family(db, k.U('scenario-a-v1'))['rows'][0][10])
    add('UNKNOWN_CONTEXT_RETAINED', [], l.family(db, k.U('scenario-a-v1'))['rows'][1][10])
    graph_results = []
    for name in f['graphs']:
        expected = expected_graph(name)
        actual = l.native_graph(db, k.U(name))
        graph_results.append(dict(version_id=k.U(name), matches=isomorphic(expected, actual),
            expected_nt=sorted(expected.serialize(format='nt').splitlines()),
            observed_nt=sorted(actual.serialize(format='nt').splitlines())))
    add('ALL_NATIVE_ORACLES', True, all(x['matches'] for x in graph_results), detail=graph_results)
    add('OLD_GRAPHS_UNCHANGED', True, all(isomorphic(g, l.native_graph(db, k.U(name))) for name, g in before.items()))
    combined = Graph()
    for name in f['graphs']:
        for triple in l.native_graph(db, k.U(name)):
            combined.add(triple)
    add('NO_NATIVE_CORRECTION', True, all('correct' not in str(p).lower() for _, p, _ in combined))
    forbidden = {k.RISK + x for x in ('RKM-C004', 'RKM-C007', 'RKM-C065', 'RKM-C066')}
    add('NO_ADMISSION_OR_OCCURRENCE', True, not any(str(o) in forbidden for _, _, o in combined)
        and not db.execute('SELECT 1 FROM risk_case WHERE case_id=?', (k.U('withheld'),)).fetchone())
    add('BOUND_PARAMETER', [], l.family(db, "'; DROP TABLE knowledge_correction; --")['rows'])
    before = state_hash(db)
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / 'backup.sqlite'
        target = b.connect(path)
        db.backup(target)
        target.close()
        target = l.connect(path)
        add('BACKUP_REOPEN', before, state_hash(target))
        target.close()
        path = Path(folder) / 'live.sqlite'
        target = fresh(path)
        populate(target)
        target.close()
        target = l.connect(path)
        add('FILE_REOPEN', before, state_hash(target))
        target.close()
    dump = '\n'.join(db.iterdump())
    target = b.connect()
    l.restore_dump(target, dump)
    add('DUMP_RESTORE', before, state_hash(target))
    target.close()
    # Mutate a real source join in the executable query and compare fixed rows.
    sql = (l.OUT / 'queries/family.sql').read_text()
    mutant = sql.replace('s.record_id=k.source_record_id', 's.record_id=c.source_record_id')
    actual = [list(row) for row in db.execute(mutant, {'root': k.U('scenario-a-v1')})]
    for row in actual:
        row[9], row[10] = json.loads(row[9]), json.loads(row[10])
    add('MUTANT_SOURCE_JOIN_EXPOSED', False, actual == f['families']['scenario-a-v1'], 'mutation')
    # Weaken the actual delete guard, then expose the missing branch against its oracle.
    db.execute('DROP TRIGGER knowledge_correction_delete')
    db.execute('DELETE FROM knowledge_correction WHERE corrected_version_id=?', (k.U('scenario-a-v2'),))
    actual = [row[0] for row in db.execute(sql, {'root': k.U('scenario-a-v1')})]
    add('MUTANT_IMMUTABILITY_EXPOSED', False, actual == [row[0] for row in f['families']['scenario-a-v1']], 'mutation')
    db.close()
    db = fresh()
    trigger = db.execute("SELECT sql FROM sqlite_master WHERE name='knowledge_correction_insert'").fetchone()[0]
    start = trigger.index(' SELECT CASE WHEN EXISTS(\n SELECT 1 FROM knowledge_snapshot n JOIN knowledge_snapshot p\n JOIN knowledge_type nt')
    end = trigger.index(' SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM source_record', start)
    db.execute('DROP TRIGGER knowledge_correction_insert')
    db.execute(trigger[:start] + trigger[end:])
    edge = dict(f['declared_edges'][0], prior_version_id=k.U('scenario-b-v1'))
    l.insert_declaration(db, edge)
    add('MUTANT_OWNER_GUARD_EXPOSED', [['OWNER']], [list(row) for row in db.execute('SELECT code FROM v_knowledge_lineage_invalid')], 'mutation')
    db.close()
    # Every failed action is isolated, must name the intended diagnostic, and preserve state.
    for ident, diagnostic in f['rejection_diagnostics'].items():
        db = fresh()
        edge = copy.deepcopy(f['declared_edges'][0])
        record = copy.deepcopy(f['new_records'][0])
        if ident in ('DUPLICATE_PARENT', 'REPLACE_PARENT', 'UPDATE_DECLARATION', 'DELETE_DECLARATION', 'CYCLE'):
            l.declare(db, edge)
        if ident == 'UNISSUED_CHILD':
            k.stage(db, record)
            edge = copy.deepcopy(f['declared_edges'][1])
        if ident == 'UNISSUED_PARENT':
            k.stage(db, record)
            edge['prior_version_id'] = record['version_id']
        if ident == 'CONFIGURATION_OFF':
            db.execute('PRAGMA foreign_keys=OFF')
        before = state(db)
        restore_rollback = True
        try:
            with b.transaction(db):
                if ident == 'REPLACE_PARENT':
                    db.execute('INSERT OR REPLACE INTO knowledge_correction VALUES(?,?,?,?,?,?,?)', tuple(edge[key] for key in l.FIELDS))
                elif ident == 'UPDATE_DECLARATION':
                    db.execute("UPDATE knowledge_correction SET reason='rewritten'")
                elif ident == 'DELETE_DECLARATION':
                    db.execute('DELETE FROM knowledge_correction')
                elif ident == 'LEDGER_DRIFT':
                    db.execute("UPDATE schema_migration SET sha256='forged' WHERE version=6")
                    l.health(db)
                elif ident == 'SCHEMA_DRIFT':
                    db.execute('DROP INDEX knowledge_correction_parent')
                    l.health(db)
                elif ident == 'CONFIGURATION_OFF':
                    l.health(db)
                elif ident.startswith('RESTORE_'):
                    lines = []
                    for line in dump.splitlines():
                        if line.startswith('INSERT INTO "knowledge_correction"') and "'" + k.U('scenario-a-v2') + "'" in line:
                            if ident == 'RESTORE_OWNER_TAMPER':
                                line = line.replace(k.U('scenario-a-v1'), k.U('scenario-b-v1'))
                            elif ident == 'RESTORE_TIME_TAMPER':
                                line = line.replace('2026-10-28T00:00:00Z', '2026-02-30T00:00:00Z')
                            elif ident == 'RESTORE_CYCLE_TAMPER':
                                line = line.replace(k.U('scenario-a-v1'), k.U('scenario-a-v4')).replace('2026-10-28T00:00:00Z', '2026-10-28T03:00:00Z')
                            elif ident == 'RESTORE_PROVENANCE_TAMPER':
                                line = line.replace('Revise scenario interpretation', '')
                        lines.append(line)
                    target = b.connect()
                    target.execute('PRAGMA ignore_check_constraints=ON')
                    try:
                        l.restore_dump(target, '\n'.join(lines))
                    finally:
                        restore_rollback = b.schema_snapshot(target) == [] and target.execute('PRAGMA user_version').fetchone()[0] == 0
                        target.close()
                elif ident == 'ATOMIC_ISSUE_FAILURE':
                    edge = dict(f['declared_edges'][1], prior_version_id=k.U('scenario-b-v1'))
                    l.issue_corrected(db, record, edge)
                else:
                    if ident == 'SELF_PARENT':
                        edge['prior_version_id'] = edge['corrected_version_id']
                    elif ident == 'CYCLE':
                        edge['corrected_version_id'], edge['prior_version_id'] = edge['prior_version_id'], edge['corrected_version_id']
                    elif ident == 'CROSS_ARTIFACT':
                        edge['prior_version_id'] = k.U('scenario-b-v1')
                    elif ident == 'CROSS_CLASS':
                        edge['prior_version_id'] = k.U('reference-a-v1')
                    elif ident == 'MISSING_CHILD':
                        edge['corrected_version_id'] = k.U('absent')
                    elif ident == 'MISSING_PARENT':
                        edge['prior_version_id'] = k.U('absent')
                    elif ident == 'NONKNOWLEDGE_PARENT':
                        edge['prior_version_id'] = a.BASE('context-v1')
                    elif ident == 'RAW_PARENT':
                        edge['prior_version_id'] = k.U('raw-document')
                    elif ident == 'MISSING_DECLARATION_SOURCE':
                        edge['source_record_id'] = k.U('absent')
                    elif ident == 'EMPTY_REASON':
                        edge['reason'] = ' '
                    elif ident == 'EMPTY_LOCATOR':
                        edge['source_locator'] = ' '
                    elif ident == 'EMPTY_INTERPRETATION':
                        edge['interpretation_origin'] = ' '
                    elif ident == 'BAD_CALENDAR':
                        edge['recorded_at'] = '2026-02-30T00:00:00Z'
                    elif ident == 'NONCANONICAL_TIME':
                        edge['recorded_at'] = '2026-10-28T00:00:00+00:00'
                    elif ident == 'EARLY_DECLARATION':
                        edge['recorded_at'] = '2026-10-26T00:00:00Z'
                    elif ident == 'NONTEXT_INPUT':
                        edge['reason'] = 3
                    l.declare(db, edge)
            observed = 'ACCEPTED'
        except (ValueError, sqlite3.DatabaseError) as exc:
            observed = diagnostic if diagnostic in str(exc) else 'WRONG_DIAGNOSTIC: ' + str(exc)
        unchanged = before == state(db) and restore_rollback
        add(ident, diagnostic, observed, 'negative', dict(rollback_preserved=unchanged))
        if not unchanged:
            rows[-1]['status'] = 'FAIL'
        db.close()
    declared = set(f['case_ids'])
    if len(rows) != len(declared) or {row['id'] for row in rows} != declared:
        raise ValueError('Lost/duplicate predeclared lineage case IDs')
    rows.sort(key=lambda row: row['id'])
    return dict(schema='riskium-source-scenario-lineage-execution-v1', profile='0.5.0', schema_version=6,
                runtime=dict(sqlite=sqlite3.sqlite_version, scope='Actual local engine; hosted replay reports its own runtime.'),
                inputs_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in INPUTS},
                summary=dict(cases=len(rows), outcomes=dict(Counter(row['status'] for row in rows)),
                             kinds=dict(Counter(row['kind'] for row in rows)), native_graph_oracles=len(f['graphs'])),
                cases=rows, independent_semantic_validation=False, stable_distribution_changed=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    report = execute()
    if report['summary']['outcomes'] != {'PASS': len(fixture()['case_ids'])}:
        print(json.dumps([r for r in report['cases'] if r['status'] != 'PASS'], indent=2))
        raise SystemExit('Lineage oracle mismatch')
    target = OUT / 'report.json'
    if args.check:
        expected = json.loads(target.read_text())
        for key in ('inputs_sha256', 'summary', 'cases'):
            if report[key] != expected[key]:
                raise ValueError('Stale lineage execution: ' + key)
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status='SOURCE_SCENARIO_LINEAGE_EXECUTION_PASS', sqlite=sqlite3.sqlite_version, **report['summary'])))


if __name__ == '__main__':
    main()
