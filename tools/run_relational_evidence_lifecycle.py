"""Execute the 43 previously frozen lifecycle controls against actual SQLite."""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
from unittest.mock import patch

from rdflib import Graph, RDF, URIRef
from rdflib.compare import isomorphic
import relational_evidence_lifecycle as x
import relational_evidence as e
import relational_history as b
import relational_assessment as a
import relational_source_scenario as k
import run_relational_evidence as old

ROOT = x.ROOT
OUT = ROOT / 'evaluation/relational/evidence-lifecycle'
INPUTS = ['implementation/relational/0.7.0/' + p for p in
          ('contract.json', 'fixtures.json', 'execution-fixture.json', 'design.json',
           '008_evidence_lifecycle.sql', 'queries/selection.sql', 'queries/family.sql')]
INPUTS += ['tools/relational_evidence_lifecycle.py', 'tools/run_relational_evidence_lifecycle.py']


def fixture():
    return json.loads((x.OUT / 'fixtures.json').read_text())


def material():
    return json.loads((x.OUT / 'execution-fixture.json').read_text())


def alias(name):
    return material()['aliases'].get(name, name)


def logical(value):
    reverse = {v: k for k, v in material()['aliases'].items()}
    if isinstance(value, str):
        return reverse.get(value, value)
    if isinstance(value, list):
        return [logical(v) for v in value]
    if isinstance(value, dict):
        return {k: logical(v) for k, v in value.items()}
    return value


def event(kind='CORRECT', ident='event-test', version='ref-A@2', parent='ref-A@1',
          context=None, source=None, artifact='ref-A'):
    result = dict(material()['common_event'], event_id=ident, kind=kind, artifact_id=alias(artifact),
                  context_id=context, version_id=alias(version) if version is not None else None,
                  prior_version_id=alias(parent) if parent is not None else None)
    if source is not None:
        result['source_record_id'] = alias(source)
    return result


def prior(path=':memory:'):
    db = old.fresh(path)
    old.populate(db)
    m = material()
    extra_sources = {m['common_event']['source_record_id']} | {
        value for key, value in m['aliases'].items()
        if key.startswith('source-') or key.startswith('decision-source-') or key in ('notice-1', 'withdrawal-notice')}
    for source in sorted(extra_sources):
        if not db.execute('SELECT 1 FROM source_record WHERE record_id=?', (source,)).fetchone():
            db.execute('INSERT INTO source_record VALUES(?,?)', (source, json.dumps(dict(synthetic=True, identity=source), sort_keys=True)))
    for record in m['extra_reference_versions']:
        e.issue(db, record)
    draft = dict(old.fixture()['records'][0], version_id=alias('ref-A@draft'))
    e.stage(db, draft)
    e.health(db)
    return db


def fresh(path=':memory:'):
    db = prior(path)
    x.migrate(db)
    return db


def seed_decisions(db, through=40):
    for row in fixture()['base']['decision_ledger']:
        if row['sequence'] > through:
            continue
        result = x.append(db, event(row['kind'], 'decision-' + str(row['sequence']), row['version'], None,
                                   row['context'], row['source'], row['artifact']))
        if result['sequence'] != row['sequence']:
            raise ValueError('Materialized sequence differs from independently fixed input')


def seed_corrections(db):
    for row in fixture()['base']['correction_tree']:
        x.append(db, event(ident=row['id'], version=row['child'], parent=row['parent']))


def state(db):
    tables = [row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    return dict(rows={name: sorted([list(r) for r in db.execute('SELECT * FROM "' + name + '"')],
                                  key=lambda row: json.dumps(row, ensure_ascii=False)) for name in tables},
                schema=b.schema_snapshot(db), version=db.execute('PRAGMA user_version').fetchone()[0])


def state_hash(db):
    return hashlib.sha256(json.dumps(state(db), sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def diagnostic(error):
    text = str(error)
    return text.split('ELC-', 1)[1] if 'ELC-' in text else text


def reject(db, action):
    before = state(db)
    try:
        action()
        code = 'ACCEPTED'
    except (ValueError, sqlite3.DatabaseError) as exc:
        code = diagnostic(exc)
    return dict(diagnostic=code, writes=0 if state(db) == before else 1)


def select_case(db, case):
    q = case['operation']['selection']
    return logical(x.selection(db, alias(q['artifact']), q['context'], q['as_of_sequence']))


def graph(db, version):
    return x.native_graph(db, alias(version))


def native_set(db):
    return set(db.execute('SELECT graph_id,subject,predicate,object FROM v_evidence_quads'))


def execute():
    f = fixture()
    records = []

    def add(case, observed, evidence=None):
        records.append(dict(id=case['id'], category=case['category'], expected=case['expected'],
                            observed=observed, status='PASS' if observed == case['expected'] else 'FAIL',
                            evidence=evidence or {}))

    for case in f['cases']:
        number = int(case['id'].split('F')[1])
        if number == 36:
            continue
        db = prior() if number in (1, 2) else fresh()
        evidence = {}
        try:
            if number == 1:
                before = e.snapshot(db)
                graphs = native_set(db)
                result = x.migrate(db)
                same = before == x.legacy_snapshot(db)
                old_ledger = before['schema_migration']
                observed = dict(status=result, prior_rows='byte-equivalent logical values' if same else 'CHANGED',
                                migration_1_to_7_hashes='UNCHANGED' if old_ledger == x.legacy_snapshot(db)['schema_migration'] else 'CHANGED',
                                all_prior_named_graphs='UNCHANGED' if graphs == native_set(db) else 'CHANGED')
                evidence = dict(old_tables=len(before), prior_logical_rows=sum(map(len, before.values())),
                                prior_quad_count=len(graphs), literal_graph_oracles_match=all(isomorphic(
                                    old.expected_graph(v), x.native_graph(db, v)) for v in old.fixture()['graphs']))
                if not evidence['literal_graph_oracles_match']:
                    observed['all_prior_named_graphs'] = 'ORACLE_MISMATCH'
            elif number == 2:
                before = state(db)
                text = x.migration_text()
                try:
                    with patch.object(x, 'migration_text', return_value=text + '\nINVALID LIFECYCLE MIGRATION;\n'):
                        x.migrate(db)
                    rolled_back = False
                except sqlite3.DatabaseError:
                    rolled_back = state(db) == before
                observed = dict(status='ROLLED_BACK' if rolled_back else 'FAILED_ATOMICITY',
                                source_schema_version=db.execute('PRAGMA user_version').fetchone()[0],
                                new_schema_objects=db.execute("SELECT count(*) FROM sqlite_master WHERE name LIKE '%lifecycle%'").fetchone()[0],
                                all_source_rows='UNCHANGED' if state(db) == before else 'CHANGED')
            elif number == 3:
                before = state(db)
                observed = dict(status=x.migrate(db), new_rows=0 if state(db) == before else 1,
                                prior_rows='UNCHANGED' if state(db) == before else 'CHANGED')
            elif number == 4:
                before = native_set(db)
                result = x.append(db, event(source='notice-1'))
                observed = dict(status=result['status'], family=logical(x.family(db, alias('ref-A@1'))['version_ids']),
                                native_new_triples=len(native_set(db) - before))
            elif number in (5, 6, 7, 8, 9, 18, 24, 38, 39, 40, 41, 42):
                if number in (8, 9):
                    seed_corrections(db)
                if number == 18:
                    seed_decisions(db, 20)
                item = event()
                if number == 5:
                    item['version_id'] = alias('ref-B@1')
                elif number == 6:
                    item['version_id'] = alias('ref-A@draft')
                elif number == 7:
                    item['version_id'] = alias('ref-A@1')
                elif number == 8:
                    item.update(version_id=alias('ref-A@1'), prior_version_id=alias('ref-A@4'))
                elif number == 9:
                    item['prior_version_id'] = alias('ref-A@3')
                elif number == 18:
                    item = event('SELECT', 'selected-again', 'ref-A@2', None, 'review-X')
                elif number == 24:
                    item = event('SELECT', 'unknown-selection', 'unknown-ref@1', None, 'review-X', artifact='unknown-ref')
                elif number == 38:
                    original = event('SELECT', 'event-original', 'ref-A@2', None, 'review-X')
                    x.append(db, original)
                    item = dict(original, version_id=alias('ref-A@3'))
                elif number == 39:
                    item = event('SELECT', version='ref-B@1', parent=None, context='review-X')
                elif number == 40:
                    item['recorded_at'] = '2026-02-30T12:00:00Z'
                elif number == 41:
                    item['version_id'] = alias('scenario-A@1')
                elif number == 42:
                    item['source_locator'] = None
                observed = reject(db, lambda: x.append(db, item))
                if number == 24:
                    raw = db.execute('SELECT original_json FROM source_record WHERE record_id=?', (e.U('raw-document'),)).fetchone()[0]
                    observed = dict(diagnostic=observed['diagnostic'], managed_writes=observed['writes'],
                                    raw_source='UNCHANGED' if raw == old.fixture()['sources'][2][1] else 'CHANGED')
                if number == 38:
                    observed['original'] = 'UNCHANGED' if observed['writes'] == 0 else 'CHANGED'
                if number == 41:
                    observed['note'] = 'Family check precedes same-artifact check for this control.'
                evidence = dict(full_input=item)
            elif number == 10:
                seed_corrections(db)
                answer = x.family(db, alias('ref-A@1'))
                observed = dict(version_ids=logical(answer['version_ids']), parent_edges=logical(answer['parent_edges']),
                                independent_source_count_inferred=answer['independent_corroboration'] != 'NOT_ASSESSED')
                evidence = dict(rows=answer['rows'])
            elif number == 11:
                answer = x.family(db, alias('ref-A@1'))
                selected = x.selection(db, alias('ref-A'), 'review-X', 999)
                observed = dict(version_ids=logical(answer['version_ids']), implicit_edges=len(answer['parent_edges']),
                                selected_version=selected['selected_version'])
            elif number in (12, 13, 14, 15, 16, 17, 19, 20, 21):
                if number != 12:
                    seed_decisions(db)
                observed = select_case(db, case)
                if number == 17:
                    observed['fallback_allowed'] = observed['selected_version'] is not None
                evidence = dict(ledger=x.ledger(db))
            elif number == 22:
                seed_decisions(db, 20)
                rows = x.ledger(db)
                outcome = reject(db, lambda: db.execute('UPDATE evidence_lifecycle_event SET ordinal=ordinal+1'))
                observed = dict(order=[r['sequence'] for r in rows],
                                real_world_authority_inferred=bool(db.execute('SELECT 1 FROM identity_registry WHERE resource_id=?',
                                                                            (rows[0]['actor_id'],)).fetchone()),
                                rewritable_sequences=outcome['diagnostic'] == 'ACCEPTED')
                evidence = dict(recorded_times=[r['recorded_at'] for r in rows], same_time=len({r['recorded_at'] for r in rows}) == 1)
                if not evidence['same_time']:
                    observed['order'] = []
            elif number == 23:
                result = x.by_target(db, k.U('scenario-a-v1'))
                observed = dict(additional_independent_studies_inferred=0 if result['independent_corroboration'] == 'NOT_ASSESSED' else 1,
                                endorsement_inferred=result['endorsement'] != 'NOT_INFERRED')
                evidence = dict(reference_versions=[r[0] for r in result['rows']], item_versions=[r[4] for r in result['rows']])
            elif number in (25, 26, 27):
                before = native_set(db)
                seed_decisions(db)
                if number == 25:
                    seed_corrections(db)
                if number == 25:
                    same = isomorphic(graph(db, 'ref-A@1'), old.expected_graph(alias('ref-A@1')))
                    source = db.execute('SELECT source_record_id FROM evidence_snapshot WHERE version_id=?', (alias('ref-A@1'),)).fetchone()[0]
                    observed = dict(exact_inherited_graph=alias('ref-A@1') if same else 'GRAPH_MISMATCH',
                                    new_native_predicates=sorted({r[2] for r in native_set(db) - before}), issued_source=logical(source))
                elif number == 26:
                    same = isomorphic(graph(db, 'ref-A@2'), old.expected_graph(alias('ref-A@2')))
                    global_role = db.execute("SELECT count(*) FROM artifact_typing WHERE native_class='RKM-C066'").fetchone()[0]
                    observed = dict(exact_inherited_graph=alias('ref-A@2') if same else 'GRAPH_MISMATCH',
                                    global_C066_membership=bool(global_role),
                                    historical_graph_union=not same)
                else:
                    added = sorted(native_set(db) - before)
                    observed = dict(added_triples=added, new_correction_authority_or_occurrence_predicates=sorted({r[2] for r in added}))
            elif number == 28:
                seed_decisions(db)
                seed_corrections(db)
                before = state(db)
                actions = ["UPDATE evidence_lifecycle_event SET reason='rewritten'",
                           'DELETE FROM evidence_lifecycle_event',
                           'INSERT OR REPLACE INTO evidence_lifecycle_event SELECT * FROM evidence_lifecycle_event']
                results = [reject(db, lambda sql=sql: db.execute(sql)) for sql in actions]
                observed = dict(each_rejected=all(r['diagnostic'] == 'IMMUTABLE' or r['diagnostic'] == 'DUPLICATE_EVENT_ID' for r in results),
                                all_rows='UNCHANGED' if state(db) == before else 'CHANGED')
                evidence = dict(actual_errors=results)
            elif number == 29:
                x.append(db, event(source='decision-source-1'))
                row = x.family(db, alias('ref-A@1'))['rows'][1]
                parent_source = db.execute('SELECT source_record_id FROM evidence_snapshot WHERE version_id=?', (alias('ref-A@1'),)).fetchone()[0]
                observed = dict(parent_source=logical(parent_source), child_source=logical(row['version_source']),
                                decision_source=logical(row['declaration_source']), merged_source=len({parent_source, row['version_source'], row['declaration_source']}) != 3)
                evidence = dict(actual_child_and_declaration=row)
            elif number == 30:
                record = dict(old.fixture()['records'][1], version_id=alias('ref-A@5'))
                invalid = event(version='ref-A@5', parent='absent-parent')
                with b.transaction(db):
                    db.execute('INSERT INTO source_record VALUES(?,?)', ('urn:fixture:outer', '{}'))
                    result = reject(db, lambda: x.issue_corrected(db, record, invalid))
                    version_exists = bool(db.execute('SELECT 1 FROM identity_registry WHERE resource_id=?', (record['version_id'],)).fetchone())
                    declared = bool(db.execute('SELECT 1 FROM evidence_lifecycle_event WHERE version_id=?', (record['version_id'],)).fetchone())
                    outer = bool(db.execute("SELECT 1 FROM source_record WHERE record_id='urn:fixture:outer'").fetchone())
                observed = dict(status='ROLLED_BACK' if result['diagnostic'] == 'UNKNOWN_ENDPOINT' and result['writes'] == 0 else 'FAILED',
                                new_version_exists=version_exists, new_declaration_exists=declared,
                                outer_prior_writes='PRESERVED' if outer else 'LOST')
                evidence = dict(actual_error=result['diagnostic'])
            elif number == 31:
                before = state(db)
                try:
                    e.health(db)
                    code = 'ACCEPTED'
                except ValueError as exc:
                    code = 'UNSUPPORTED_SCHEMA_VERSION' if str(exc) == 'R-EVIDENCE-LEDGER' and db.execute('PRAGMA user_version').fetchone()[0] == 8 else str(exc)
                    evidence['legacy_error'] = str(exc)
                observed = dict(diagnostic=code, database_writes=0 if state(db) == before else 1)
            elif number == 32:
                wrong = db.execute('SELECT version_id FROM evidence_snapshot WHERE artifact_id=? ORDER BY version_id DESC LIMIT 1', (alias('ref-A'),)).fetchone()[0]
                oracle = next(r for r in f['cases'] if r['id'] == 'ELC-F12')['expected']['selected_version']
                observed = dict(incorrect_selected_version=logical(wrong), oracle_selected_version=oracle,
                                must_detect_difference=logical(wrong) != oracle)
                evidence = dict(mutant='Actual newest-version SQL query with no selection event')
            elif number == 33:
                seed_decisions(db)
                rejected = reject(db, lambda: x.selection(db, alias('ref-A'), None, 10))
                wrong = db.execute((x.OUT / 'queries/selection.sql').read_text(),
                                   dict(artifact=alias('ref-A'), context='review-X', as_of_sequence=10)).fetchone()
                observed = dict(diagnostic=rejected['diagnostic'], must_detect_difference=wrong[0] == 'SELECTED' and rejected['diagnostic'] == 'INVALID_CONTEXT')
                evidence = dict(mutant_default_context_result=list(wrong))
            elif number == 34:
                cohort = json.loads((ROOT / 'evaluation/sources/cq0708/cohort.json').read_text())
                statuses = [r['case_admission'] for r in cohort['identity_candidates']]
                responses = json.loads((ROOT / 'evaluation/independent-review/responses.json').read_text())
                mapping = json.loads((ROOT / 'evaluation/relational/qualified-evidence/mapping-accounting.json').read_text())
                observed = dict(all_organizational_admissions='WITHHELD' if len(statuses) == 11 and set(statuses) == {'WITHHELD'} else 'CHANGED',
                                independent_ratings=len(responses['initial_ratings']), source_elements=len(mapping['rows']),
                                full_mapping_completed=mapping['full_mapping_completed'])
            elif number == 35:
                seed_decisions(db)
                seed_corrections(db)
                before = state(db)
                valid = True
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / 'backup.sqlite'
                    target = b.connect(path)
                    db.backup(target)
                    target.close()
                    target = x.connect(path)
                    valid = valid and before == state(target)
                    target.close()
                dump = '\n'.join(db.iterdump())
                target = b.connect()
                try:
                    x.restore_dump(target, dump)
                    valid = valid and before == state(target)
                finally:
                    target.close()
                changed = dump.replace("'fixed synthetic declaration'", "'tampered declaration'", 1)
                # A content-preserving administrative rewrite is not authentication.
                # The exercised tamper deliberately breaks a declared source/pin invariant.
                changed = '\n'.join(line.replace('Source presented as support', 'tampered statement')
                                    if line.startswith('INSERT INTO "evidence_snapshot"') else line for line in changed.splitlines())
                target = b.connect()
                tamper = 'ACCEPTED'
                rollback = False
                try:
                    x.restore_dump(target, changed)
                except (ValueError, sqlite3.DatabaseError) as exc:
                    tamper = 'REJECTED'
                    rollback = b.schema_snapshot(target) == [] and target.execute('PRAGMA user_version').fetchone()[0] == 0
                    evidence['tamper_error'] = str(exc)
                finally:
                    target.close()
                observed = dict(valid_roundtrips='exact row/query/graph equivalence' if valid else 'MISMATCH',
                                tampered_restore=tamper, all_previous_audits='RETAINED' if rollback and before == state(db) else 'LOST')
            elif number == 37:
                actual = Graph()
                params = dict(version=alias('ref-A@1'), old_item=e.U('item-a-v1'), new_item=e.U('item-a-v2'),
                              old_target=k.U('scenario-a-v1'), new_target=k.U('scenario-a-v2'))
                wrong = """SELECT CASE subject WHEN :old_item THEN :new_item WHEN :old_target THEN :new_target ELSE subject END,
                                  predicate,
                                  CASE object WHEN :old_item THEN :new_item WHEN :old_target THEN :new_target ELSE object END
                           FROM v_evidence_quads WHERE graph_id=:version"""
                for s, p, o in db.execute(wrong, params):
                    actual.add((URIRef(s), URIRef(p), URIRef(o)))
                observed = dict(must_detect_difference=not isomorphic(actual, old.expected_graph(alias('ref-A@1'))),
                                expected_graph=alias('ref-A@1'), forbidden_graph=alias('ref-A@2'))
                evidence = dict(mutant_triples=sorted([list(map(str, t)) for t in actual]))
            elif number == 43:
                rejected = reject(db, lambda: x.selection(db, alias('ref-A'), 'review-X', None))
                observed = dict(diagnostic=rejected['diagnostic'], selected_version=None if rejected['diagnostic'] != 'ACCEPTED' else 'UNEXPECTED_POINTER')
            else:
                raise ValueError('Unimplemented fixed control ' + case['id'])
            add(case, observed, evidence)
        finally:
            db.close()
    case = next(r for r in f['cases'] if r['id'] == 'ELC-F36')
    contract = x.contract()
    cases_by_id = {r['id']: r for r in records}
    mapping = json.loads((ROOT / 'evaluation/relational/qualified-evidence/mapping-accounting.json').read_text())
    model = json.loads((ROOT / 'ontology/riskium-model.json').read_text())
    native_ids = {row['id'] for key in ('concepts', 'imported_types', 'associations', 'generalizations', 'constraints') for row in model[key]}
    historical = hashlib.sha256((ROOT / 'evaluation/consistency/traceability.json').read_bytes()).hexdigest()
    unexplained = [r['id'] for r in contract['requirements'] if not r['cases'] or
                   any(c != 'ELC-F36' and cases_by_id.get(c, {}).get('status') != 'PASS' for c in r['cases'])]
    observed = dict(requirements_without_fixed_cases=sum(not r['cases'] for r in contract['requirements']),
                    unaccounted_native_ids=len(native_ids ^ {r['id'] for r in mapping['rows']}),
                    historical_row_semantics='UNCHANGED' if historical == contract['source_sha256']['evaluation/consistency/traceability.json'] else 'CHANGED',
                    unexplained_retained_claims=len(unexplained))
    add(case, observed, dict(scope='ELC-01..09 engineering claims only; this is not release R3/current whole-manuscript reconciliation.'))
    records.sort(key=lambda r: r['id'])
    if {r['id'] for r in records} != {r['id'] for r in f['cases']} or len(records) != 43:
        raise ValueError('Lost or duplicated frozen lifecycle control')
    db = fresh()
    try:
        seed_decisions(db, 20)
        db.execute('DROP TRIGGER evidence_lifecycle_validate')
        item = event('SELECT', 'weakened-withdrawal', 'ref-A@2', None, 'review-X')
        x.insert_event(db, item)
        violation = db.execute("SELECT code FROM v_evidence_lifecycle_invalid WHERE event_id='weakened-withdrawal'").fetchall()
        rejected = reject(db, lambda: x.health(db))
        supplementary = [dict(id='ELC-MUT-WITHDRAW-GUARD', kind='actual_weakened_rule_control',
                              forbidden_row_inserted=True, data_violation_detected=('WITHDRAWN_IN_CONTEXT',) in violation,
                              exact_schema_reader_rejects=rejected['diagnostic'] == 'SCHEMA')]
        supplementary[0]['status'] = 'PASS' if supplementary[0]['data_violation_detected'] and supplementary[0]['exact_schema_reader_rejects'] else 'FAIL'
    finally:
        db.close()
    return dict(schema='riskium-evidence-lifecycle-execution-v1', profile='0.7.0', schema_version=8,
                execution_issue=53, declaration_commit='cb996241553fc8ae858acb38622009ed3a08f450',
                runtime=dict(sqlite=sqlite3.sqlite_version, scope='Actual engine; hosted replay records its own version.'),
                inputs_sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in INPUTS},
                summary=dict(cases=len(records), outcomes=dict(Counter(r['status'] for r in records)),
                             categories=dict(Counter(r['category'] for r in records)), inherited_native_oracles=4,
                             fixed_query_mutations=3, supplementary_weakened_rule_controls=len(supplementary)),
                cases=records, supplementary_controls=supplementary,
                independent_semantic_validation=False, publication_executed=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    report = execute()
    failed = [r for r in report['cases'] + report['supplementary_controls'] if r['status'] != 'PASS']
    if failed:
        print(json.dumps(failed, indent=2))
        raise SystemExit('Lifecycle control mismatch')
    target = OUT / 'report.json'
    if args.check:
        expected = json.loads(target.read_text())
        for key in ('inputs_sha256', 'summary', 'cases', 'supplementary_controls'):
            if report[key] != expected[key]:
                raise ValueError('Stale lifecycle evidence: ' + key)
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status='EVIDENCE_LIFECYCLE_EXECUTION_PASS', sqlite=sqlite3.sqlite_version, **report['summary'])))


if __name__ == '__main__':
    main()
