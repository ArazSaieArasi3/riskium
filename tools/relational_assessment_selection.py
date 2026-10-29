"""SQLite v9: explicit documentary selection of complete assessment bundles."""
from functools import lru_cache
import hashlib
import json

import relational_history as b
import relational_assessment as a
import relational_correction as c
import relational_evidence_lifecycle as previous
import relational_evidence as e

ROOT = previous.ROOT
OUT = ROOT / 'implementation/relational/0.8.0'
SQL = OUT / '009_assessment_selection.sql'
FIELDS = ('event_id', 'kind', 'assessment_id', 'decision_context_id', 'target_version',
          'actor', 'reason', 'source_record_id', 'source_locator', 'interpretation_origin', 'recorded_at')


def fail(code):
    raise ValueError('ASL-' + code)


def contract():
    value = json.loads((OUT / 'contract.json').read_text())
    for path, digest in value['source_sha256'].items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != digest:
            fail('SOURCE_BINDING: ' + path)
    if hashlib.sha256((OUT / 'fixtures.json').read_bytes()).hexdigest() != value['fixtures_sha256']:
        fail('FIXTURE_BINDING')
    if hashlib.sha256((OUT / 'execution-fixture.json').read_bytes()).hexdigest() != 'eab7528a46add5b37afc0048f42e0433d6cb01fde5e9cfc21b6cd3835f11ca3e':
        fail('EXECUTION_INPUT_BINDING')
    return value


def migration_text():
    contract()
    return SQL.read_text()


@lru_cache(maxsize=4)
def expected_schema(digest):
    db = a.connect()
    try:
        c.migrate(db)
        previous.k.migrate(db)
        previous.l.migrate(db)
        e.migrate(db)
        previous.migrate(db)
        b.execute_script(db, migration_text())
        return b.schema_snapshot(db)
    finally:
        db.close()


def audit_data(db):
    previous.prior_audit(db)
    for view in ('v_evidence_lifecycle_invalid', 'v_assessment_selection_invalid'):
        bad = db.execute('SELECT code FROM ' + view + ' LIMIT 1').fetchone()
        if bad:
            fail('DATA_' + bad[0])
    clocks = {}
    for table in ('evidence_lifecycle_event', 'assessment_selection_event'):
        count, maximum = db.execute('SELECT count(*),coalesce(max(ordinal),0) FROM ' + table).fetchone()
        if count != maximum:
            fail('SEQUENCE')
        if maximum:
            clocks[table] = maximum
        for (time,) in db.execute('SELECT recorded_at FROM ' + table):
            e.canonical_utc(time, 'ASL-INVALID_TIME')
    if dict(db.execute('SELECT name,seq FROM sqlite_sequence')) != clocks:
        fail('ALLOCATOR')


def health(db):
    b.require_configuration(db)
    contract()
    digest = hashlib.sha256(migration_text().encode()).hexdigest()
    expected = {1: hashlib.sha256((b.OUT / '001_tables.sql').read_bytes()).hexdigest(),
                2: hashlib.sha256((b.OUT / '002_guards.sql').read_bytes()).hexdigest(),
                3: a.migration_hash(), 4: c.digest(), 5: previous.k.digest(),
                6: previous.l.digest(), 7: e.digest(), 8: previous.digest(), 9: digest}
    if dict(db.execute('SELECT version,sha256 FROM schema_migration')) != expected or db.execute('PRAGMA user_version').fetchone()[0] != 9:
        fail('LEDGER')
    if b.schema_snapshot(db) != expected_schema(digest):
        fail('SCHEMA')
    if db.execute('PRAGMA foreign_key_check').fetchall() or db.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
        fail('INTEGRITY')
    audit_data(db)


def state(db):
    tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    return dict(rows={t: sorted([list(r) for r in db.execute('SELECT * FROM "' + t + '"')], key=lambda r: json.dumps(r)) for t in tables},
                schema=b.schema_snapshot(db), version=db.execute('PRAGMA user_version').fetchone()[0])


def state_sha256(db):
    return hashlib.sha256(json.dumps(state(db), sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def migrate(db):
    b.require_configuration(db)
    version = db.execute('PRAGMA user_version').fetchone()[0]
    if version == 9:
        health(db)
        return 'ALREADY_CURRENT'
    if version != 8:
        fail('REQUIRES_V8')
    with b.transaction(db):
        previous.health(db)
        before = previous.snapshot(db)
        text = migration_text()
        b.execute_script(db, text)
        db.execute('INSERT INTO schema_migration VALUES(9,?)', (hashlib.sha256(text.encode()).hexdigest(),))
        db.execute('PRAGMA user_version=9')
        after = previous.snapshot(db)
        after['schema_migration'] = [r for r in after['schema_migration'] if r[0] < 9]
        if after != before:
            fail('DATA_LOSS')
        health(db)
    return 'UPGRADED'


def connect(path):
    db = b.connect(path)
    try:
        migrate(db)
    except BaseException:
        db.close()
        raise
    return db


def append(db, event):
    health(db)
    if not isinstance(event, dict) or set(event) != set(FIELDS):
        fail('EVENT_FIELDS')
    for field in FIELDS:
        if field == 'target_version' and event['kind'] == 'CLEAR':
            continue
        if not isinstance(event[field], str) or not event[field].strip():
            fail('MISSING_' + field.upper())
    e.canonical_utc(event['recorded_at'], 'ASL-INVALID_TIME')
    with b.transaction(db):
        cursor = db.execute('INSERT INTO assessment_selection_event(' + ','.join(FIELDS) + ') VALUES(' + ','.join('?' for _ in FIELDS) + ')', tuple(event[f] for f in FIELDS))
        sequence = cursor.lastrowid
        health(db)
    return sequence


def rows(db, sql, parameters=()):
    cursor = db.execute(sql, parameters)
    names = [col[0] for col in cursor.description]
    return [dict(zip(names, r)) for r in cursor]


def selection(db, assessment, context, as_of_sequence):
    health(db)
    if not isinstance(context, str) or not context.strip():
        fail('CONTEXT')
    if not isinstance(assessment, str) or not db.execute("SELECT 1 FROM artifact_typing WHERE artifact_id=? AND native_class='RKM-C032'", (assessment,)).fetchone():
        fail('ASSESSMENT')
    head = db.execute('SELECT coalesce(max(ordinal),0) FROM assessment_selection_event').fetchone()[0]
    if type(as_of_sequence) is not int or not 0 <= as_of_sequence <= head:
        fail('AS_OF')
    answer = rows(db, (OUT / 'queries/selection.sql').read_text(), dict(assessment=assessment, context=context, as_of=as_of_sequence))[0]
    answer.update(as_of_sequence=as_of_sequence, decision_context=context, automatic_comparability=False,
                  assessment=None, results=[], decisions=rows(db, 'SELECT * FROM assessment_selection_event WHERE assessment_id=? AND decision_context_id=? AND ordinal<=? ORDER BY ordinal', (assessment, context, as_of_sequence)))
    if answer['assessment_version'] is not None:
        version = answer['assessment_version']
        answer['assessment'] = rows(db, 'SELECT * FROM assessment_snapshot WHERE assessment_version_id=?', (version,))[0]
        answer['results'] = rows(db, 'SELECT * FROM result_snapshot WHERE assessment_version_id=? ORDER BY result_version_id', (version,))
    return answer


def issue(db, assessment, results, correction=None):
    """Seal an assessment bundle and optional existing correction relation atomically."""
    health(db)
    if not results:
        fail('EMPTY_BUNDLE')
    with b.transaction(db):
        aid = assessment['assessment_id']
        if not db.execute('SELECT 1 FROM information_artifact WHERE artifact_id=?', (aid,)).fetchone():
            a.add_artifact(db, aid, 'RKM-C032', 'Assessment', assessment['source_record_id'])
        a.stage_version(db, assessment['assessment_version_id'], aid, payload=assessment, source=assessment['source_record_id'])
        a.insert_dict(db, 'assessment_snapshot', assessment)
        for item in results:
            row = dict(item, assessment_version_id=assessment['assessment_version_id'])
            if row.get('reported_value') is not None and not isinstance(row['reported_value'], str):
                fail('REPORTED_LEXEME_TYPE')
            if not db.execute('SELECT 1 FROM information_artifact WHERE artifact_id=?', (row['result_id'],)).fetchone():
                a.add_artifact(db, row['result_id'], 'RKM-C034', 'Result', row['source_record_id'])
            a.stage_version(db, row['result_version_id'], row['result_id'], payload=row, source=row['source_record_id'])
            a.insert_dict(db, 'result_snapshot', row)
            a.seal(db, row['result_version_id'], assessment['recorded_at'])
        a.seal(db, assessment['assessment_version_id'], assessment['recorded_at'])
        if correction is not None:
            if set(correction) != {'prior_version', 'reason', 'recorded_at', 'source_record_id'}:
                fail('CORRECTION_FIELDS')
            e.canonical_utc(correction['recorded_at'], 'ASL-INVALID_TIME')
            db.execute('INSERT INTO assessment_correction VALUES(?,?,?,?,?)',
                       (assessment['assessment_version_id'], correction['prior_version'], correction['reason'], correction['recorded_at'], correction['source_record_id']))
        health(db)


def family(db, root):
    health(db)
    return dict(rows=[list(r) for r in db.execute((c.OUT / 'queries/family.sql').read_text(),dict(root=root))],
                independent_corroboration='NOT_ASSESSED')


def compare(db, left, right):
    health(db)
    fields = ('context_id','context_version_id','method_id','method_version_id','basis_id','basis_version_id','temporal_context_id','dimension_id','scale_id','scale_version_id','level_id')
    query = (a.OUT / 'queries/comparison_inputs.sql').read_text()
    values = [rows(db, query, dict(result_version=v)) for v in (left,right)]
    if any(not r or any(r[0][f] is None for f in fields) for r in values):
        return 'NOT_READY'
    for r in values:
        r=r[0]
        if not db.execute('SELECT 1 FROM method_scope WHERE method_version_id=? AND scale_id=? AND dimension_id=?',(r['method_version_id'],r['scale_id'],r['dimension_id'])).fetchone():
            return 'NOT_READY'
    return 'SCOPED_DIRECT_COMPARISON_ADMISSIBLE' if all(values[0][0][f]==values[1][0][f] for f in fields[:-1]) else 'NOT_ADMISSIBLE_BY_EXACT_PIN_POLICY'


def restore_dump(db, text, expected_state_sha256):
    """Require a separately retained trusted digest; edited history can be valid SQL."""
    b.require_configuration(db)
    if not isinstance(expected_state_sha256,str) or len(expected_state_sha256)!=64:
        fail('EXPECTED_RESTORE_DIGEST')
    items=[s for s in b.statements(text) if s.strip().upper() not in ('BEGIN TRANSACTION;','COMMIT;')]
    permitted = ('CREATE TABLE ', 'CREATE INDEX ', 'CREATE UNIQUE INDEX ', 'CREATE VIEW ', 'CREATE TRIGGER ',
                 'INSERT INTO ', 'DELETE FROM SQLITE_SEQUENCE', 'DELETE FROM "SQLITE_SEQUENCE"')
    if any(not s.lstrip().upper().startswith(permitted) for s in items):
        fail('RESTORE_STATEMENT')
    clocks=[s for s in items if s.lstrip().upper().startswith(('INSERT INTO "SQLITE_SEQUENCE"','INSERT INTO SQLITE_SEQUENCE','DELETE FROM "SQLITE_SEQUENCE"','DELETE FROM SQLITE_SEQUENCE'))]
    items=[s for s in items if s not in clocks]
    tables=[s for s in items if s.lstrip().upper().startswith('CREATE TABLE')]
    inserts=[s for s in items if s.lstrip().upper().startswith('INSERT INTO')]
    rest=[s for s in items if s not in tables and s not in inserts]
    with b.transaction(db):
        db.execute('PRAGMA defer_foreign_keys=ON')
        for statement in tables+inserts+rest+clocks:
            db.execute(statement)
        db.execute('PRAGMA user_version=9')
        health(db)
        if state_sha256(db)!=expected_state_sha256:
            fail('RESTORE_DIGEST')
