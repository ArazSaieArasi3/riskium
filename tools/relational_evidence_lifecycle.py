"""Audited SQLite v8 API for the bounded C065 documentary lifecycle."""
from functools import lru_cache
import hashlib
import json
import sqlite3

import relational_history as b
import relational_assessment as a
import relational_correction as c
import relational_source_scenario as k
import relational_source_scenario_lineage as l
import relational_evidence as e

ROOT = e.ROOT
OUT = ROOT / 'implementation/relational/0.7.0'
SQL = OUT / '008_evidence_lifecycle.sql'
FIELDS = ('event_id', 'kind', 'artifact_id', 'context_id', 'version_id', 'prior_version_id',
          'actor_id', 'reason', 'recorded_at', 'source_record_id', 'source_locator', 'interpretation_origin')
TABLES = e.TABLES + ('evidence_lifecycle_event', 'sqlite_sequence')


def fail(code):
    raise ValueError('ELC-' + code)


def contract():
    data = json.loads((OUT / 'contract.json').read_text())
    for path, digest in data['source_sha256'].items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != digest:
            fail('SOURCE_BINDING: ' + path)
    return data


def migration_text():
    contract()
    return SQL.read_text()


def digest():
    return hashlib.sha256(migration_text().encode()).hexdigest()


@lru_cache(maxsize=4)
def expected_schema(source_hash):
    db = a.connect()
    try:
        c.migrate(db)
        k.migrate(db)
        l.migrate(db)
        e.migrate(db)
        b.execute_script(db, migration_text())
        return b.schema_snapshot(db)
    finally:
        db.close()


def prior_audit(db):
    e.audit_prior(db)
    bad = db.execute("SELECT code FROM v_evidence_invalid ORDER BY version_id,CASE WHEN code='PAYLOAD' THEN 1 ELSE 0 END,code LIMIT 1").fetchone()
    if bad:
        raise ValueError('R-EVIDENCE-DATA-' + bad[0])
    for (value,) in db.execute('SELECT recorded_at FROM evidence_snapshot'):
        e.canonical_utc(value, 'R-EVIDENCE-TIME')


def health(db):
    b.require_configuration(db)
    contract()
    ledger = dict(db.execute('SELECT version,sha256 FROM schema_migration'))
    expected = {1: hashlib.sha256((b.OUT / '001_tables.sql').read_bytes()).hexdigest(),
                2: hashlib.sha256((b.OUT / '002_guards.sql').read_bytes()).hexdigest(),
                3: a.migration_hash(), 4: c.digest(), 5: k.digest(), 6: l.digest(), 7: e.digest(), 8: digest()}
    if ledger != expected or db.execute('PRAGMA user_version').fetchone()[0] != 8:
        fail('LEDGER')
    if b.schema_snapshot(db) != expected_schema(ledger[8]):
        fail('SCHEMA')
    if db.execute('PRAGMA foreign_key_check').fetchall():
        fail('FOREIGN_KEY')
    if db.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
        fail('INTEGRITY')
    prior_audit(db)
    bad = db.execute('SELECT code FROM v_evidence_lifecycle_invalid ORDER BY event_id,code LIMIT 1').fetchone()
    if bad:
        fail('DATA_' + bad[0])
    count, maximum = db.execute('SELECT count(*),coalesce(max(ordinal),0) FROM evidence_lifecycle_event').fetchone()
    clocks = db.execute('SELECT name,seq FROM sqlite_sequence ORDER BY name').fetchall()
    if count != maximum or clocks != ([('evidence_lifecycle_event', maximum)] if maximum else []):
        fail('SEQUENCE')
    for (value,) in db.execute('SELECT recorded_at FROM evidence_lifecycle_event'):
        e.canonical_utc(value, 'ELC-INVALID_RECORDED_TIME')


def legacy_snapshot(db):
    result = e.snapshot(db)
    result['schema_migration'] = [row for row in result['schema_migration'] if row[0] < 8]
    return result


def migrate(db):
    b.require_configuration(db)
    version = db.execute('PRAGMA user_version').fetchone()[0]
    if version == 7:
        with b.transaction(db):
            e.health(db)
            before = legacy_snapshot(db)
            text = migration_text()
            b.execute_script(db, text)
            db.execute('INSERT INTO schema_migration VALUES(8,?)', (hashlib.sha256(text.encode()).hexdigest(),))
            db.execute('PRAGMA user_version=8')
            if legacy_snapshot(db) != before:
                fail('DATA_LOSS')
            health(db)
        return 'UPGRADED'
    if version == 8:
        health(db)
        return 'ALREADY_CURRENT'
    fail('REQUIRES_V7')


def connect(path):
    db = b.connect(path)
    try:
        migrate(db)
    except BaseException:
        db.close()
        raise
    return db


def snapshot(db):
    return {table: sorted([list(row) for row in db.execute('SELECT * FROM ' + table)],
                          key=lambda row: json.dumps(row, ensure_ascii=False)) for table in TABLES}


def validate_event(db, event):
    if not isinstance(event, dict) or set(event) != set(FIELDS):
        fail('INVALID_INPUT')
    provenance = ('event_id', 'actor_id', 'reason', 'source_record_id', 'source_locator', 'interpretation_origin')
    if any(not isinstance(event[x], str) or not event[x].strip() for x in provenance):
        fail('MISSING_PROVENANCE')
    if not db.execute('SELECT 1 FROM source_record WHERE record_id=?', (event['source_record_id'],)).fetchone():
        fail('MISSING_PROVENANCE')
    e.canonical_utc(event['recorded_at'], 'ELC-INVALID_RECORDED_TIME')
    kind = event['kind']
    if kind not in ('CORRECT', 'SELECT', 'WITHDRAW', 'CLEAR'):
        fail('INVALID_EVENT')
    if kind == 'CORRECT':
        if event['context_id'] is not None or not all(isinstance(event[x], str) and event[x].strip() for x in ('version_id', 'prior_version_id')):
            fail('INVALID_EVENT')
    else:
        if not isinstance(event['context_id'], str) or not event['context_id'].strip():
            fail('INVALID_CONTEXT')
        if event['prior_version_id'] is not None or (kind == 'CLEAR' and event['version_id'] is not None):
            fail('INVALID_EVENT')
        if kind != 'CLEAR' and (not isinstance(event['version_id'], str) or not event['version_id'].strip()):
            fail('INVALID_EVENT')
    if not isinstance(event['artifact_id'], str) or not event['artifact_id'].strip():
        fail('UNKNOWN_ENDPOINT')
    for version in (event['version_id'], event['prior_version_id']):
        if version is None:
            continue
        row = db.execute('SELECT artifact_id,is_issued FROM version_snapshot WHERE version_id=?', (version,)).fetchone()
        if row is None:
            fail('UNKNOWN_ENDPOINT')
        if row[1] != 1:
            fail('UNISSUED_ENDPOINT')
        if not db.execute('SELECT 1 FROM evidence_snapshot WHERE version_id=?', (version,)).fetchone():
            fail('UNSUPPORTED_ENDPOINT_FAMILY')
    if not db.execute('SELECT 1 FROM information_artifact WHERE artifact_id=?', (event['artifact_id'],)).fetchone():
        fail('UNKNOWN_ENDPOINT')
    if not db.execute('SELECT 1 FROM evidence_reference_type WHERE artifact_id=?', (event['artifact_id'],)).fetchone():
        fail('UNSUPPORTED_ENDPOINT_FAMILY')
    if any(db.execute('SELECT artifact_id FROM version_snapshot WHERE version_id=?', (v,)).fetchone()[0] != event['artifact_id']
           for v in (event['version_id'], event['prior_version_id']) if v is not None):
        fail('CROSS_ARTIFACT')


def insert_event(db, event):
    """Internal helper; the public append/issue_corrected transaction owns rollback."""
    validate_event(db, event)
    db.execute('INSERT INTO evidence_lifecycle_event(' + ','.join(FIELDS) + ') VALUES(' + ','.join('?' for _ in FIELDS) + ')',
               tuple(event[x] for x in FIELDS))
    return db.execute('SELECT sequence FROM v_evidence_lifecycle_ledger WHERE event_id=?', (event['event_id'],)).fetchone()[0]


def append(db, event):
    health(db)
    with b.transaction(db):
        sequence = insert_event(db, event)
        health(db)
    return dict(status='ACCEPTED', sequence=sequence)


def issue(db, record):
    health(db)
    with b.transaction(db):
        e.stage(db, record)
        a.seal(db, record['version_id'], record['recorded_at'])
        health(db)


def issue_corrected(db, record, event):
    health(db)
    if not isinstance(record, dict) or not isinstance(event, dict) or event.get('kind') != 'CORRECT' or event.get('version_id') != record.get('version_id'):
        fail('INVALID_INPUT')
    with b.transaction(db):
        e.stage(db, record)
        a.seal(db, record['version_id'], record['recorded_at'])
        sequence = insert_event(db, event)
        health(db)
    return dict(status='ACCEPTED', sequence=sequence)


def selection(db, artifact, context, as_of_sequence):
    health(db)
    if not isinstance(context, str) or not context.strip():
        fail('INVALID_CONTEXT')
    if type(as_of_sequence) is not int or as_of_sequence < 0 or as_of_sequence > 9223372036854775807:
        fail('INVALID_AS_OF_SEQUENCE')
    if not isinstance(artifact, str) or not artifact.strip():
        fail('UNKNOWN_ENDPOINT')
    row = db.execute((OUT / 'queries/selection.sql').read_text(),
                     dict(artifact=artifact, context=context, as_of_sequence=as_of_sequence)).fetchone()
    return dict(zip(('status', 'selected_version', 'last_selected_version'), row))


def family(db, root):
    health(db)
    fields = ('version_id', 'artifact_id', 'statement', 'version_source', 'version_source_json', 'item_version_id',
              'prior_version_id', 'event_id', 'declaration_source', 'declaration_source_json', 'actor_id', 'reason',
              'recorded_at', 'source_locator', 'interpretation_origin')
    rows = [dict(zip(fields, row)) for row in db.execute((OUT / 'queries/family.sql').read_text(), dict(root=root))]
    for row in rows:
        for key in ('version_source_json', 'declaration_source_json'):
            if row[key] is not None:
                row[key] = json.loads(row[key])
    return dict(rows=rows, version_ids=[r['version_id'] for r in rows],
                parent_edges=[[r['version_id'], r['prior_version_id']] for r in rows if r['prior_version_id']],
                authority='NOT_INFERRED', independent_corroboration='NOT_ASSESSED')


def ledger(db):
    health(db)
    names = ('sequence',) + FIELDS
    return [dict(zip(names, row)) for row in db.execute('SELECT * FROM v_evidence_lifecycle_ledger ORDER BY sequence')]


def native_graph(db, version):
    health(db)
    from rdflib import Graph, URIRef
    graph = Graph()
    for s, p, o in db.execute('SELECT subject,predicate,object FROM v_evidence_quads WHERE graph_id=?', (version,)):
        graph.add((URIRef(s), URIRef(p), URIRef(o)))
    return graph


def by_target(db, target):
    health(db)
    rows = []
    for raw in db.execute((e.OUT / 'queries/by_target.sql').read_text(), dict(target=target)):
        row = list(raw)
        row[13] = json.loads(row[13])
        rows.append(row)
    return dict(rows=rows, independent_corroboration='NOT_ASSESSED', endorsement='NOT_INFERRED')


def restore_dump(db, text):
    b.require_configuration(db)
    items = [s for s in b.statements(text) if s.strip().upper() not in ('BEGIN TRANSACTION;', 'COMMIT;')]
    clocks = [s for s in items if s.lstrip().upper().startswith(
        ('INSERT INTO "SQLITE_SEQUENCE"', 'INSERT INTO SQLITE_SEQUENCE', 'DELETE FROM "SQLITE_SEQUENCE"', 'DELETE FROM SQLITE_SEQUENCE'))]
    items = [s for s in items if s not in clocks]
    tables = [s for s in items if s.lstrip().upper().startswith('CREATE TABLE')]
    inserts = [s for s in items if s.lstrip().upper().startswith('INSERT INTO')]
    other = [s for s in items if s not in tables and s not in inserts]
    with b.transaction(db):
        db.execute('PRAGMA defer_foreign_keys=ON')
        for statement in tables + inserts + other + clocks:
            db.execute(statement)
        db.execute('PRAGMA user_version=8')
        health(db)
