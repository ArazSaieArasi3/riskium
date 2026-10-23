"""Configured SQLite migrations and atomic issue operation for the bounded slice."""
from contextlib import contextmanager
import hashlib
import itertools
import json
import sqlite3
from build_relational_history import ROOT, OUT, RISK, SLOTS

COUNTER=itertools.count()
TABLES=('source_record','identity_registry','risk_case','information_artifact','register_entry',
        'working_draft','draft_dependency','version_snapshot','version_dependency')
LEDGER_SQL='CREATE TABLE IF NOT EXISTS schema_migration(version INTEGER PRIMARY KEY, sha256 TEXT NOT NULL) STRICT'


def connect(path=':memory:'):
    if sqlite3.sqlite_version_info<(3,38,0):raise ValueError('R-SQLITE-VERSION: requires SQLite >=3.38')
    c=sqlite3.connect(str(path),isolation_level=None)
    c.execute('PRAGMA foreign_keys=ON');c.execute('PRAGMA recursive_triggers=ON')
    require_configuration(c);return c


def require_configuration(c):
    if c.execute('PRAGMA foreign_keys').fetchone()[0]!=1 or c.execute('PRAGMA recursive_triggers').fetchone()[0]!=1:
        raise ValueError('R-CONNECTION-POLICY: foreign_keys and recursive_triggers must be ON')


@contextmanager
def transaction(c):
    nested=c.in_transaction;name='history_sp_'+str(next(COUNTER))
    c.execute('SAVEPOINT '+name if nested else 'BEGIN IMMEDIATE')
    try:yield
    except BaseException:
        if nested:c.execute('ROLLBACK TO '+name);c.execute('RELEASE '+name)
        else:c.execute('ROLLBACK')
        raise
    else:c.execute('RELEASE '+name if nested else 'COMMIT')


def statements(text):
    pending=''
    for line in text.splitlines(True):
        pending+=line
        if sqlite3.complete_statement(pending):yield pending;pending=''
    if pending.strip():raise ValueError('R-INCOMPLETE-SQL')


def execute_script(c,text):
    # executescript commits pending transactions; this parser deliberately does not.
    for statement in statements(text):c.execute(statement)


def logical_snapshot(c):
    return {t:sorted([list(r) for r in c.execute('SELECT * FROM '+t)],key=lambda r:json.dumps(r,ensure_ascii=False)) for t in TABLES}


def schema_snapshot(c):
    return [list(r) for r in c.execute("SELECT type,name,sql FROM sqlite_master WHERE sql IS NOT NULL ORDER BY type,name")]


def audit_legacy(c):
    if c.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('R-MIGRATION-FOREIGN-KEY')
    if c.execute("SELECT 1 FROM version_snapshot WHERE is_issued=1 AND (issued_at IS NULL OR NOT EXISTS(SELECT 1 FROM json_each(payload_json))) LIMIT 1").fetchone():
        raise ValueError('R-MIGRATION-ISSUED-CONTENT')
    if c.execute("""SELECT 1 FROM version_snapshot v JOIN information_artifact a ON a.artifact_id=v.artifact_id
      WHERE (a.kind='RKM-C022' AND (v.entry_id IS NULL OR v.entry_id<>a.artifact_id))
      OR (a.kind<>'RKM-C022' AND v.entry_id IS NOT NULL) LIMIT 1""").fetchone():raise ValueError('R-MIGRATION-REVISION-TARGET')
    if c.execute("""SELECT 1 FROM version_snapshot v LEFT JOIN version_snapshot p ON p.version_id=v.previous_version_id
      WHERE v.previous_version_id IS NOT NULL AND (p.version_id IS NULL OR p.entry_id IS NOT v.entry_id OR p.is_issued<>1) LIMIT 1""").fetchone():
        raise ValueError('R-MIGRATION-PREDECESSOR')
    if c.execute("""WITH RECURSIVE lineage(root,id) AS (
      SELECT version_id,previous_version_id FROM version_snapshot WHERE previous_version_id IS NOT NULL
      UNION SELECT l.root,v.previous_version_id FROM lineage l JOIN version_snapshot v ON v.version_id=l.id
      WHERE v.previous_version_id IS NOT NULL) SELECT 1 FROM lineage WHERE root=id LIMIT 1""").fetchone():raise ValueError('R-MIGRATION-CYCLE')
    expected="CASE d.slot "+' '.join("WHEN '"+s+"' THEN '"+cid+"'" for s,cid in SLOTS.items())+' END'
    if c.execute("""SELECT 1 FROM version_dependency d JOIN version_snapshot t ON t.version_id=d.target_version_id
      JOIN information_artifact a ON a.artifact_id=t.artifact_id WHERE t.is_issued<>1 OR a.kind<>"""+expected+"""
      OR (d.direct_artifact_id IS NOT NULL AND d.direct_artifact_id<>t.artifact_id) LIMIT 1""").fetchone():raise ValueError('R-MIGRATION-DEPENDENCY')


def expected_schema():
    c=connect();c.execute(LEDGER_SQL)
    execute_script(c,(OUT/'001_tables.sql').read_text());execute_script(c,(OUT/'002_guards.sql').read_text())
    result=schema_snapshot(c);c.close();return result


def migrate(c,target=2):
    require_configuration(c)
    if target not in (1,2):raise ValueError('R-MIGRATION-TARGET')
    c.execute(LEDGER_SQL)
    rows=dict(c.execute('SELECT version,sha256 FROM schema_migration'))
    if set(rows)-{1,2} or (2 in rows and 1 not in rows):raise ValueError('R-MIGRATION-LEDGER')
    if c.execute('PRAGMA user_version').fetchone()[0]!=max(rows,default=0):raise ValueError('R-MIGRATION-USER-VERSION')
    paths={1:OUT/'001_tables.sql',2:OUT/'002_guards.sql'}
    for v,sha in rows.items():
        if hashlib.sha256(paths[v].read_bytes()).hexdigest()!=sha:raise ValueError('R-MIGRATION-SOURCE-HASH')
    for v in range(1,target+1):
        if v in rows:continue
        text=paths[v].read_text()
        with transaction(c):
            if v==2:audit_legacy(c)
            execute_script(c,text)
            c.execute('INSERT INTO schema_migration VALUES(?,?)',(v,hashlib.sha256(text.encode()).hexdigest()))
            c.execute('PRAGMA user_version='+str(v))
    if target==2:
        if schema_snapshot(c)!=expected_schema():raise ValueError('R-MIGRATION-SCHEMA-DRIFT')
        audit_legacy(c)


def add_identity(c,iri,family):c.execute('INSERT INTO identity_registry VALUES(?,?)',(iri,family))


def seed_v1(c,fixture):
    if c.execute('PRAGMA user_version').fetchone()[0]!=1:raise ValueError('Synthetic baseline seeding requires schema 1')
    with transaction(c):
        for row in fixture['sources']:c.execute('INSERT INTO source_record VALUES(?,?)',row)
        for row in fixture['cases']:
            add_identity(c,row[0],'case');c.execute('INSERT INTO risk_case(case_id,label,source_record_id) VALUES(?,?,?)',row)
        for row in fixture['artifacts']:
            add_identity(c,row[0],'artifact');c.execute('INSERT INTO information_artifact(artifact_id,kind,label,source_record_id) VALUES(?,?,?,?)',row)
        for row in fixture['entries']:c.execute('INSERT INTO register_entry(entry_id,case_id,register_id) VALUES(?,?,?)',row)
        for row in fixture['versions']:
            add_identity(c,row[0],'version')
            c.execute('INSERT INTO version_snapshot(version_id,artifact_id,entry_id,previous_version_id,payload_json,source_record_id,issued_at,is_issued) VALUES(?,?,?,?,?,?,?,?)',row)
        for row in fixture['dependencies']:c.execute('INSERT INTO version_dependency VALUES(?,?,?,?)',row)


def issue_draft(c,draft_id,version_id,issued_at):
    require_configuration(c)
    with transaction(c):
        row=c.execute('SELECT artifact_id,entry_id,previous_version_id,payload_json,source_record_id FROM working_draft WHERE draft_id=?',(draft_id,)).fetchone()
        if row is None:raise ValueError('R-DRAFT-NOT-FOUND')
        add_identity(c,version_id,'version')
        c.execute('INSERT INTO version_snapshot(version_id,artifact_id,entry_id,previous_version_id,payload_json,source_record_id) VALUES(?,?,?,?,?,?)',(version_id,*row))
        for slot,target,direct in c.execute('SELECT slot,target_version_id,direct_artifact_id FROM draft_dependency WHERE draft_id=? ORDER BY slot',(draft_id,)).fetchall():
            c.execute('INSERT INTO version_dependency VALUES(?,?,?,?)',(version_id,slot,target,direct))
        c.execute('UPDATE version_snapshot SET issued_at=?,is_issued=1 WHERE version_id=?',(issued_at,version_id))
        c.execute('DELETE FROM working_draft WHERE draft_id=?',(draft_id,))


def restore_dump(c,text):
    require_configuration(c)
    items=[stmt for stmt in statements(text) if stmt.strip().upper() not in ('BEGIN TRANSACTION;','COMMIT;')]
    # Deferred row checks still require referenced tables to exist at prepare time.
    # Create all tables first, load their rows, then restore indexes/views/triggers.
    tables=[s for s in items if s.lstrip().upper().startswith('CREATE TABLE')]
    inserts=[s for s in items if s.lstrip().upper().startswith('INSERT INTO')]
    other=[s for s in items if s not in tables and s not in inserts]
    with transaction(c):
        c.execute('PRAGMA defer_foreign_keys=ON')
        for stmt in tables+inserts+other:c.execute(stmt)
        if c.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('R-RESTORE-FOREIGN-KEY')
    # iterdump excludes PRAGMA user_version; derive it only from the restored ledger.
    current=c.execute('SELECT max(version) FROM schema_migration').fetchone()[0] or 0
    c.execute('PRAGMA user_version='+str(current));migrate(c)
