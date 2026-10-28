"""SQLite v6 correction declarations for issued knowledge versions; native model unchanged."""
from datetime import datetime
from functools import lru_cache
import hashlib
import json

import relational_history as b
import relational_assessment as a
import relational_correction as c
import relational_source_scenario as k

ROOT = k.ROOT
OUT = ROOT / 'implementation/relational/0.5.0'
SQL = OUT / '006_source_scenario_lineage.sql'
FIELDS = ('corrected_version_id', 'prior_version_id', 'reason', 'recorded_at',
          'source_record_id', 'source_locator', 'interpretation_origin')
TABLES = k.TABLES + ('knowledge_correction',)


def contract():
    data = json.loads((OUT / 'contract.json').read_text())
    for path, digest in data['source_sha256'].items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != digest:
            raise ValueError('R-LINEAGE-SOURCE-BINDING: ' + path)
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
    """Keep v5 data audits; exact-schema/version checks belong to this v6 reader."""
    k.audit_prior(db)
    bad = db.execute('SELECT code FROM v_knowledge_invalid ORDER BY version_id,code LIMIT 1').fetchone()
    if bad:
        raise ValueError('R-KNOWLEDGE-DATA-' + bad[0])
    for (value,) in db.execute('SELECT recorded_at FROM knowledge_snapshot'):
        canonical_utc(value, 'R-KNOWLEDGE-TIME')


def health(db):
    b.require_configuration(db)
    contract()
    ledger = dict(db.execute('SELECT version,sha256 FROM schema_migration'))
    expected = {1: hashlib.sha256((b.OUT / '001_tables.sql').read_bytes()).hexdigest(),
                2: hashlib.sha256((b.OUT / '002_guards.sql').read_bytes()).hexdigest(),
                3: a.migration_hash(), 4: c.digest(), 5: k.digest(), 6: digest()}
    if ledger != expected or db.execute('PRAGMA user_version').fetchone()[0] != 6:
        raise ValueError('R-LINEAGE-LEDGER')
    if b.schema_snapshot(db) != expected_schema(ledger[6]):
        raise ValueError('R-LINEAGE-SCHEMA')
    if db.execute('PRAGMA foreign_key_check').fetchall():
        raise ValueError('R-LINEAGE-FK')
    if db.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
        raise ValueError('R-LINEAGE-INTEGRITY')
    audit_prior(db)
    bad = db.execute('SELECT code FROM v_knowledge_lineage_invalid ORDER BY corrected_version_id,code LIMIT 1').fetchone()
    if bad:
        raise ValueError('R-LINEAGE-DATA-' + bad[0])
    for (value,) in db.execute('SELECT recorded_at FROM knowledge_correction'):
        canonical_utc(value, 'R-LINEAGE-TIME')


def legacy_snapshot(db):
    result = k.snapshot(db)
    result['schema_migration'] = [row for row in result['schema_migration'] if row[0] < 6]
    return result


def migrate(db):
    b.require_configuration(db)
    version = db.execute('PRAGMA user_version').fetchone()[0]
    if version == 5:
        with b.transaction(db):
            k.health(db)
            before = legacy_snapshot(db)
            text = migration_text()
            b.execute_script(db, text)
            db.execute('INSERT INTO schema_migration VALUES(6,?)', (hashlib.sha256(text.encode()).hexdigest(),))
            db.execute('PRAGMA user_version=6')
            if before != legacy_snapshot(db):
                raise ValueError('R-LINEAGE-DATA-LOSS')
            health(db)
    elif version == 6:
        health(db)
    else:
        raise ValueError('R-LINEAGE-REQUIRES-V5')


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


def insert_declaration(db, declaration):
    """Internal insertion; public callers wrap it in an audited transaction."""
    if not isinstance(declaration, dict) or set(declaration) != set(FIELDS) or any(
            not isinstance(declaration[key], str) for key in FIELDS):
        raise ValueError('R-LINEAGE-INPUT')
    canonical_utc(declaration['recorded_at'], 'R-LINEAGE-TIME')
    db.execute('INSERT INTO knowledge_correction VALUES(?,?,?,?,?,?,?)',
               tuple(declaration[key] for key in FIELDS))


def declare(db, declaration):
    """Explicit retrospective metadata between already-issued exact versions."""
    health(db)
    with b.transaction(db):
        insert_declaration(db, declaration)
        health(db)


def issue(db, record):
    """Plain issuance deliberately creates no implicit correction declaration."""
    health(db)
    with b.transaction(db):
        k.stage(db, record)
        a.seal(db, record['version_id'], record['recorded_at'])
        health(db)


def issue_corrected(db, record, declaration):
    health(db)
    if not isinstance(record, dict) or not isinstance(declaration, dict) or declaration.get('corrected_version_id') != record.get('version_id'):
        raise ValueError('R-LINEAGE-INPUT')
    with b.transaction(db):
        k.stage(db, record)
        a.seal(db, record['version_id'], record['recorded_at'])
        insert_declaration(db, declaration)
        health(db)


def family(db, root):
    health(db)
    rows = []
    for raw in db.execute((OUT / 'queries/family.sql').read_text(), {'root': root}):
        row = list(raw)
        row[9] = json.loads(row[9])
        row[10] = json.loads(row[10])
        rows.append(row)
    return dict(rows=rows, selection='EXACT_ROOT_AND_ALL_DECLARED_DESCENDANTS',
                independent_corroboration='NOT_ASSESSED', authority='NOT_SELECTED', occurrence='NOT_INFERRED')


def native_graph(db, version):
    health(db)
    from rdflib import Graph, URIRef
    graph = Graph()
    for s, p, o in db.execute('SELECT subject,predicate,object FROM v_knowledge_quads WHERE graph_id=?', (version,)):
        graph.add((URIRef(s), URIRef(p), URIRef(o)))
    return graph


def by_case(db, case_id):
    health(db)
    return dict(rows=[list(row) for row in db.execute((k.OUT / 'queries/by_case.sql').read_text(), {'case_id': case_id})],
                selection='ALL_EXPLICIT_ISSUED_VERSIONS', independent_corroboration='NOT_ASSESSED', occurrence='NOT_INFERRED')


def restore_dump(db, text):
    """Controlled SQLite export recovery, with schema/data audit inside the transaction."""
    b.require_configuration(db)
    items = [s for s in b.statements(text) if s.strip().upper() not in ('BEGIN TRANSACTION;', 'COMMIT;')]
    tables = [s for s in items if s.lstrip().upper().startswith('CREATE TABLE')]
    inserts = [s for s in items if s.lstrip().upper().startswith('INSERT INTO')]
    other = [s for s in items if s not in tables and s not in inserts]
    with b.transaction(db):
        db.execute('PRAGMA defer_foreign_keys=ON')
        for statement in tables + inserts + other:
            db.execute(statement)
        db.execute('PRAGMA user_version=6')
        health(db)
