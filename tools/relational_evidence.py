"""SQLite v7 qualified evidence with contextual item roles and exact issued pins."""
from datetime import datetime
from functools import lru_cache
import hashlib
import json

import relational_history as b
import relational_assessment as a
import relational_correction as c
import relational_source_scenario as k
import relational_source_scenario_lineage as l

ROOT = l.ROOT
OUT = ROOT / 'implementation/relational/0.6.0'
SQL = OUT / '007_qualified_evidence.sql'
FIELDS = ('version_id', 'artifact_id', 'item_id', 'item_version_id', 'statement', 'evidential_role',
          'source_record_id', 'source_locator', 'interpretation_origin', 'recorded_at')
NEW_TABLES = ('evidence_reference_type', 'evidence_snapshot', 'evidence_target')
TABLES = l.TABLES + NEW_TABLES
U = lambda name: 'urn:riskium:evidence:' + name



def contract():
    data = json.loads((OUT / 'contract.json').read_text())
    for path, digest in data['source_sha256'].items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != digest:
            raise ValueError('R-EVIDENCE-SOURCE-BINDING: ' + path)
    return data


def migration_text():
    contract()
    return SQL.read_text()


def digest():
    return hashlib.sha256(migration_text().encode()).hexdigest()


@lru_cache(maxsize=4)
def expected_schema(source_hash):
    db = a.connect()
    c.migrate(db)
    k.migrate(db)
    l.migrate(db)
    b.execute_script(db, migration_text())
    result = b.schema_snapshot(db)
    db.close()
    return result


def canonical_utc(value, code):
    try:
        parsed = datetime.fromisoformat(value.removesuffix('Z') + '+00:00')
        if len(value) != 20 or parsed.isoformat(timespec='seconds').replace('+00:00', 'Z') != value:
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise ValueError(code) from None


def audit_prior(db):
    """Retain all v6 data audits, with v7 exact-schema checks in this reader."""
    l.audit_prior(db)
    bad = db.execute('SELECT code FROM v_knowledge_lineage_invalid ORDER BY corrected_version_id,code LIMIT 1').fetchone()
    if bad:
        raise ValueError('R-LINEAGE-DATA-' + bad[0])
    for (value,) in db.execute('SELECT recorded_at FROM knowledge_correction'):
        canonical_utc(value, 'R-LINEAGE-TIME')


def health(db):
    b.require_configuration(db)
    contract()
    ledger = dict(db.execute('SELECT version,sha256 FROM schema_migration'))
    expected = {1: hashlib.sha256((b.OUT / '001_tables.sql').read_bytes()).hexdigest(),
                2: hashlib.sha256((b.OUT / '002_guards.sql').read_bytes()).hexdigest(),
                3: a.migration_hash(), 4: c.digest(), 5: k.digest(), 6: l.digest(), 7: digest()}
    if ledger != expected or db.execute('PRAGMA user_version').fetchone()[0] != 7:
        raise ValueError('R-EVIDENCE-LEDGER')
    if b.schema_snapshot(db) != expected_schema(ledger[7]):
        raise ValueError('R-EVIDENCE-SCHEMA')
    if db.execute('PRAGMA foreign_key_check').fetchall():
        raise ValueError('R-EVIDENCE-FK')
    if db.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
        raise ValueError('R-EVIDENCE-INTEGRITY')
    audit_prior(db)
    bad = db.execute("SELECT code FROM v_evidence_invalid ORDER BY version_id,CASE WHEN code='PAYLOAD' THEN 1 ELSE 0 END,code LIMIT 1").fetchone()
    if bad:
        raise ValueError('R-EVIDENCE-DATA-' + bad[0])
    for (value,) in db.execute('SELECT recorded_at FROM evidence_snapshot'):
        canonical_utc(value, 'R-EVIDENCE-TIME')


def legacy_snapshot(db):
    result = l.snapshot(db)
    result['schema_migration'] = [row for row in result['schema_migration'] if row[0] < 7]
    return result


def migrate(db):
    b.require_configuration(db)
    version = db.execute('PRAGMA user_version').fetchone()[0]
    if version == 6:
        with b.transaction(db):
            l.health(db)
            before = legacy_snapshot(db)
            text = migration_text()
            b.execute_script(db, text)
            db.execute('INSERT INTO schema_migration VALUES(7,?)', (hashlib.sha256(text.encode()).hexdigest(),))
            db.execute('PRAGMA user_version=7')
            if before != legacy_snapshot(db):
                raise ValueError('R-EVIDENCE-DATA-LOSS')
            health(db)
    elif version == 7:
        health(db)
    else:
        raise ValueError('R-EVIDENCE-REQUIRES-V6')


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


def payload(record):
    return {key: record[key] for key in ('version_id', 'artifact_id', 'statement', 'item_version_id',
            'evidential_role', 'source_record_id', 'source_locator', 'interpretation_origin', 'recorded_at', 'target_version_ids')}


def stage(db, record):
    """Trusted internal staging; issue() adds transaction, seal and audits."""
    required = set(FIELDS) - {'item_id'} | {'label', 'target_version_ids'}
    if not isinstance(record, dict) or set(record) != required or any(
            not isinstance(record[key], str) for key in required - {'target_version_ids'}):
        raise ValueError('R-EVIDENCE-INPUT')
    if not isinstance(record['target_version_ids'], list) or any(not isinstance(x, str) for x in record['target_version_ids']):
        raise ValueError('R-EVIDENCE-INPUT')
    record = dict(record, target_version_ids=sorted(record['target_version_ids']))
    if db.execute('SELECT 1 FROM version_snapshot WHERE version_id=?', (record['version_id'],)).fetchone():
        raise ValueError('R-VERSION-DUPLICATE')
    if not db.execute('SELECT 1 FROM source_record WHERE record_id=?', (record['source_record_id'],)).fetchone():
        raise ValueError('R-EVIDENCE-SOURCE')
    item = db.execute('SELECT artifact_id FROM version_snapshot WHERE version_id=? AND is_issued=1', (record['item_version_id'],)).fetchone()
    if item is None:
        raise ValueError('R-EVIDENCE-ITEM')
    aid = record['artifact_id']
    if not db.execute('SELECT 1 FROM evidence_reference_type WHERE artifact_id=?', (aid,)).fetchone():
        if not db.execute('SELECT 1 FROM information_artifact WHERE artifact_id=?', (aid,)).fetchone():
            b.add_identity(db, aid, 'artifact')
            db.execute('INSERT INTO information_artifact(artifact_id,kind,label,source_record_id) VALUES(?,?,?,?)', (aid, 'RKM-C014', record['label'], record['source_record_id']))
        db.execute('INSERT INTO evidence_reference_type VALUES(?)', (aid,))
    a.stage_version(db, record['version_id'], aid, payload=payload(record), source=record['source_record_id'])
    row = dict(record, item_id=item[0])
    db.execute('INSERT INTO evidence_snapshot VALUES(?,?,?,?,?,?,?,?,?,?)', tuple(row[key] for key in FIELDS))
    for target in record['target_version_ids']:
        owner = db.execute('SELECT artifact_id FROM version_snapshot WHERE version_id=? AND is_issued=1', (target,)).fetchone()
        if owner is None:
            raise ValueError('R-EVIDENCE-TARGET')
        db.execute('INSERT INTO evidence_target VALUES(?,?,?)', (record['version_id'], owner[0], target))


def issue(db, record):
    health(db)
    with b.transaction(db):
        stage(db, record)
        a.seal(db, record['version_id'], record['recorded_at'])
        health(db)


def by_target(db, target):
    health(db)
    rows = []
    for raw in db.execute((OUT / 'queries/by_target.sql').read_text(), {'target': target}):
        row = list(raw)
        row[13] = json.loads(row[13])
        rows.append(row)
    return dict(rows=rows, selection='EXACT_TARGET_VERSION_ALL_EXPLICIT_REFERENCES',
                endorsement='NOT_INFERRED', independent_corroboration='NOT_ASSESSED', authority='NOT_SELECTED')


def native_graph(db, version):
    health(db)
    from rdflib import Graph, URIRef
    graph = Graph()
    for s, p, o in db.execute('SELECT subject,predicate,object FROM v_evidence_quads WHERE graph_id=?', (version,)):
        graph.add((URIRef(s), URIRef(p), URIRef(o)))
    return graph


def restore_dump(db, text):
    """Controlled export recovery with all seven schema and data audits before commit."""
    b.require_configuration(db)
    items = [s for s in b.statements(text) if s.strip().upper() not in ('BEGIN TRANSACTION;', 'COMMIT;')]
    tables = [s for s in items if s.lstrip().upper().startswith('CREATE TABLE')]
    inserts = [s for s in items if s.lstrip().upper().startswith('INSERT INTO')]
    other = [s for s in items if s not in tables and s not in inserts]
    with b.transaction(db):
        db.execute('PRAGMA defer_foreign_keys=ON')
        for statement in tables + inserts + other:
            db.execute(statement)
        db.execute('PRAGMA user_version=7')
        health(db)
