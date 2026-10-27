"""SQLite v5: version-owned scenario/source references; no raw-data admission."""
from functools import lru_cache
from datetime import datetime
import hashlib
import json
from pathlib import Path

import relational_history as b
import relational_assessment as a
import relational_correction as c

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'implementation/relational/0.4.0'
SQL=OUT/'005_source_scenario.sql'
NEW_TABLES=('knowledge_type','knowledge_snapshot','knowledge_case','knowledge_context')
TABLES=c.TABLES+NEW_TABLES
RISK='https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'
FIELDS=('version_id','artifact_id','narrative','source_record_id','source_locator','interpretation_origin','recorded_at')
U=lambda x:'urn:riskium:knowledge:'+x


def contract():
    data=json.loads((OUT/'contract.json').read_text())
    for p,h in data['source_sha256'].items():
        if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h:raise ValueError('R-KNOWLEDGE-SOURCE: '+p)
    return data


def migration_text():contract();return SQL.read_text()
def digest():return hashlib.sha256(migration_text().encode()).hexdigest()


@lru_cache(maxsize=4)
def expected_schema(source_hash):
    db=a.connect();c.migrate(db);b.execute_script(db,migration_text());x=b.schema_snapshot(db);db.close();return x


def legacy_snapshot(db):
    result=c.snapshot(db)
    result['schema_migration']=[r for r in result['schema_migration'] if r[0]<5]
    return result


def audit_prior(db):
    """Retain all v4 semantic checks without pretending its exact-schema reader accepts v5."""
    b.audit_legacy(db);a.audit_data(db)
    if db.execute('SELECT 1 FROM v_correction_invalid LIMIT 1').fetchone():raise ValueError('R-CORRECTION-DATA')
    if db.execute('''WITH RECURSIVE walk(root,id) AS (
    SELECT corrected_version_id,prior_version_id FROM assessment_correction UNION
    SELECT w.root,c.prior_version_id FROM walk w JOIN assessment_correction c ON c.corrected_version_id=w.id)
    SELECT 1 FROM walk WHERE root=id LIMIT 1''').fetchone():raise ValueError('R-CORRECTION-CYCLE')
    for (value,) in db.execute('SELECT recorded_at FROM assessment_correction'):
        parsed=datetime.fromisoformat(value.removesuffix('Z')+'+00:00')
        if len(value)!=20 or parsed.isoformat(timespec='seconds').replace('+00:00','Z')!=value:raise ValueError('R-CORRECTION-TIME')


def health(db):
    b.require_configuration(db);contract()
    ledger=dict(db.execute('SELECT version,sha256 FROM schema_migration'))
    expected={1:hashlib.sha256((b.OUT/'001_tables.sql').read_bytes()).hexdigest(),2:hashlib.sha256((b.OUT/'002_guards.sql').read_bytes()).hexdigest(),3:a.migration_hash(),4:c.digest(),5:digest()}
    if ledger!=expected or db.execute('PRAGMA user_version').fetchone()[0]!=5:raise ValueError('R-KNOWLEDGE-LEDGER')
    if b.schema_snapshot(db)!=expected_schema(ledger[5]):raise ValueError('R-KNOWLEDGE-SCHEMA')
    if db.execute('PRAGMA foreign_key_check').fetchall():raise ValueError('R-KNOWLEDGE-FK')
    if db.execute('PRAGMA integrity_check').fetchall()!=[('ok',)]:raise ValueError('R-KNOWLEDGE-INTEGRITY')
    audit_prior(db)
    bad=db.execute('SELECT version_id,code FROM v_knowledge_invalid ORDER BY version_id,code LIMIT 1').fetchone()
    if bad:raise ValueError('R-KNOWLEDGE-DATA-'+bad[1])
    for (value,) in db.execute('SELECT recorded_at FROM knowledge_snapshot'):
        try:
            d=datetime.fromisoformat(value.removesuffix('Z')+'+00:00')
            if len(value)!=20 or d.isoformat(timespec='seconds').replace('+00:00','Z')!=value:raise ValueError()
        except (ValueError,TypeError):raise ValueError('R-KNOWLEDGE-TIME') from None


def migrate(db):
    b.require_configuration(db)
    v=db.execute('PRAGMA user_version').fetchone()[0]
    if v==4:
        with b.transaction(db):
            c.health(db);before=legacy_snapshot(db)
            text=migration_text();b.execute_script(db,text)
            db.execute('INSERT INTO schema_migration VALUES(5,?)',(hashlib.sha256(text.encode()).hexdigest(),))
            db.execute('PRAGMA user_version=5')
            if legacy_snapshot(db)!=before:raise ValueError('R-KNOWLEDGE-DATA-LOSS')
            health(db)
    elif v==5:health(db)
    else:raise ValueError('R-KNOWLEDGE-REQUIRES-V4')


def connect(path):
    db=b.connect(path)
    try:migrate(db)
    except BaseException:db.close();raise
    return db


def snapshot(db):
    return {t:sorted([list(r) for r in db.execute('SELECT * FROM '+t)],key=lambda r:json.dumps(r,ensure_ascii=False)) for t in TABLES}


def payload(record):
    return {k:record[k] for k in ('version_id','artifact_id','native_class','narrative','source_record_id','source_locator','interpretation_origin','recorded_at','case_ids','context_version_ids')}


def stage(db,record):
    """Trusted transaction-internal staging; public issue() is atomic and audited."""
    required=set(FIELDS)|{'native_class','label','case_ids','context_version_ids'}
    if set(record)!=required or any(not isinstance(record[k],str) for k in required-{'case_ids','context_version_ids'}):raise ValueError('R-KNOWLEDGE-INPUT')
    for key in ('case_ids','context_version_ids'):
        if not isinstance(record[key],list) or any(not isinstance(x,str) for x in record[key]):raise ValueError('R-KNOWLEDGE-INPUT')
    record=dict(record,case_ids=sorted(record['case_ids']),context_version_ids=sorted(record['context_version_ids']))
    if db.execute('SELECT 1 FROM version_snapshot WHERE version_id=?',(record['version_id'],)).fetchone():raise ValueError('R-VERSION-DUPLICATE')
    aid=record['artifact_id'];kind=record['native_class']
    if kind not in ('RKM-C003','RKM-X06'):raise ValueError('R-KNOWLEDGE-TYPE')
    typing=db.execute('SELECT native_class FROM knowledge_type WHERE artifact_id=?',(aid,)).fetchone()
    if typing is None:
        existing=db.execute('SELECT kind FROM information_artifact WHERE artifact_id=?',(aid,)).fetchone()
        if existing is None:
            b.add_identity(db,aid,'artifact')
            db.execute('INSERT INTO information_artifact(artifact_id,kind,label,source_record_id) VALUES(?,?,?,?)',(aid,'RKM-C014',record['label'],record['source_record_id']))
        db.execute('INSERT INTO knowledge_type VALUES(?,?)',(aid,kind))
    elif typing[0]!=kind:raise ValueError('R-KNOWLEDGE-TYPE')
    a.stage_version(db,record['version_id'],aid,payload=payload(record),source=record['source_record_id'])
    db.execute('INSERT INTO knowledge_snapshot VALUES(?,?,?,?,?,?,?)',tuple(record[k] for k in FIELDS))
    for case in record['case_ids']:db.execute('INSERT INTO knowledge_case VALUES(?,?)',(record['version_id'],case))
    for version in record['context_version_ids']:
        target=db.execute('SELECT artifact_id FROM version_snapshot WHERE version_id=?',(version,)).fetchone()
        if target is None:raise ValueError('R-KNOWLEDGE-CONTEXT')
        db.execute('INSERT INTO knowledge_context VALUES(?,?,?)',(record['version_id'],target[0],version))


def issue(db,record):
    health(db)
    with b.transaction(db):
        stage(db,record);a.seal(db,record['version_id'],record['recorded_at']);health(db)


def by_case(db,case_id):
    health(db)
    return dict(rows=[list(r) for r in db.execute((OUT/'queries/by_case.sql').read_text(),dict(case_id=case_id))],selection='ALL_EXPLICIT_ISSUED_VERSIONS',independent_corroboration='NOT_ASSESSED',occurrence='NOT_INFERRED')


def native_graph(db,version):
    health(db)
    from rdflib import Graph,URIRef
    g=Graph()
    for s,p,o in db.execute('SELECT subject,predicate,object FROM v_knowledge_quads WHERE graph_id=?',(version,)):g.add((URIRef(s),URIRef(p),URIRef(o)))
    return g


def restore_dump(db,text):
    b.require_configuration(db)
    items=[s for s in b.statements(text) if s.strip().upper() not in ('BEGIN TRANSACTION;','COMMIT;')]
    tables=[s for s in items if s.lstrip().upper().startswith('CREATE TABLE')]
    inserts=[s for s in items if s.lstrip().upper().startswith('INSERT INTO')]
    other=[s for s in items if s not in tables and s not in inserts]
    with b.transaction(db):
        db.execute('PRAGMA defer_foreign_keys=ON')
        for statement in tables+inserts+other:db.execute(statement)
        db.execute('PRAGMA user_version=5');health(db)
