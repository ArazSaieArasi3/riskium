"""Configured migration 3 and version-owned assessment/result operations."""
from functools import lru_cache
from datetime import datetime
import hashlib
import json
import sqlite3

from build_relational_assessment import OUT, NEW_TABLES, RISK, ROOT, load_policy
import relational_history as base

MIGRATION_FILES=('003_assessment_tables.sql','003_assessment_guards.sql')
TIME='2026-10-24T00:00:00Z'
U=lambda value:'urn:riskium:assessment:'+value
BASE=lambda value:'urn:riskium:sql:'+value
SOURCE=U('source')


def migration_text():
    load_policy()
    return '\n'.join((OUT/name).read_text() for name in MIGRATION_FILES)


def migration_hash():
    return hashlib.sha256(migration_text().encode()).hexdigest()


@lru_cache(maxsize=4)
def expected_schema(source_hash):
    c=base.connect();base.migrate(c)
    base.execute_script(c,migration_text());result=base.schema_snapshot(c);c.close()
    return result


def health(c):
    base.require_configuration(c)
    rows=dict(c.execute('SELECT version,sha256 FROM schema_migration'))
    if set(rows)!={1,2,3} or c.execute('PRAGMA user_version').fetchone()[0]!=3:
        raise ValueError('R-ASSESSMENT-MIGRATION-LEDGER')
    paths={1:base.OUT/'001_tables.sql',2:base.OUT/'002_guards.sql'}
    if any(hashlib.sha256(path.read_bytes()).hexdigest()!=rows[v] for v,path in paths.items()) or rows[3]!=migration_hash():
        raise ValueError('R-ASSESSMENT-SOURCE-HASH')
    if base.schema_snapshot(c)!=expected_schema(rows[3]):
        raise ValueError('R-ASSESSMENT-SCHEMA-DRIFT')
    if c.execute('PRAGMA foreign_key_check').fetchall():
        raise ValueError('R-ASSESSMENT-FOREIGN-KEY')
    if c.execute('PRAGMA integrity_check').fetchall()!=[('ok',)]:
        raise ValueError('R-ASSESSMENT-INTEGRITY')
    base.audit_legacy(c)
    audit_data(c)


def audit_data(c):
    """Also check stored semantics after dump/restore, where inserts precede guards."""
    checks={
      'TYPE':"""SELECT 1 FROM artifact_typing t JOIN information_artifact a USING(artifact_id) WHERE a.kind<>'RKM-C014'""",
      'NATIVE-KIND':"""SELECT 1 FROM assessment_snapshot a WHERE NOT EXISTS(SELECT 1 FROM artifact_typing t WHERE t.artifact_id=a.assessment_id AND t.native_class='RKM-C032')
        OR NOT EXISTS(SELECT 1 FROM artifact_typing t WHERE t.artifact_id=a.basis_id AND t.native_class='RKM-C033')
        UNION SELECT 1 FROM result_snapshot r WHERE NOT EXISTS(SELECT 1 FROM artifact_typing t WHERE t.artifact_id=r.result_id AND t.native_class='RKM-C034')
        OR NOT EXISTS(SELECT 1 FROM artifact_typing t WHERE t.artifact_id=r.dimension_id AND t.native_class='RKM-C039')
        UNION SELECT 1 FROM scale_snapshot s JOIN version_snapshot v ON v.version_id=s.scale_version_id WHERE s.scale_id<>v.artifact_id
        OR NOT EXISTS(SELECT 1 FROM information_artifact t WHERE t.artifact_id=s.scale_id AND t.kind='RKM-C036')
        OR NOT EXISTS(SELECT 1 FROM artifact_typing t WHERE t.artifact_id=s.dimension_id AND t.native_class='RKM-C039')
        UNION SELECT 1 FROM scale_level l WHERE NOT EXISTS(SELECT 1 FROM artifact_typing t WHERE t.artifact_id=l.level_id AND t.native_class='RKM-C038')
        UNION SELECT 1 FROM method_scope m JOIN version_snapshot v ON v.version_id=m.method_version_id
        WHERE NOT EXISTS(SELECT 1 FROM information_artifact t WHERE t.artifact_id=v.artifact_id AND t.kind='RKM-C035')
        OR NOT EXISTS(SELECT 1 FROM information_artifact t WHERE t.artifact_id=m.scale_id AND t.kind='RKM-C036')
        OR NOT EXISTS(SELECT 1 FROM artifact_typing t WHERE t.artifact_id=m.dimension_id AND t.native_class='RKM-C039')""",
      'CONTEXT':"""SELECT 1 FROM assessment_snapshot a JOIN version_snapshot v ON v.version_id=a.context_version_id
        JOIN information_artifact t ON t.artifact_id=v.artifact_id WHERE v.is_issued<>1 OR t.kind<>'RKM-C002'
        OR (a.context_id IS NOT NULL AND a.context_id<>v.artifact_id)""",
      'METHOD':"""SELECT 1 FROM assessment_snapshot a LEFT JOIN version_snapshot v ON v.version_id=a.method_version_id
        LEFT JOIN information_artifact t ON t.artifact_id=v.artifact_id WHERE a.method_version_id IS NOT NULL AND
        (v.is_issued<>1 OR t.kind<>'RKM-C035' OR (a.method_id IS NOT NULL AND a.method_id<>v.artifact_id))""",
      'BASIS':"""SELECT 1 FROM assessment_snapshot a LEFT JOIN version_snapshot v ON v.version_id=a.basis_version_id
        WHERE a.basis_version_id IS NOT NULL AND (v.is_issued<>1 OR v.artifact_id<>a.basis_id)""",
      'SCALE':"""SELECT 1 FROM result_snapshot r LEFT JOIN scale_snapshot s USING(scale_version_id)
        LEFT JOIN version_snapshot v ON v.version_id=r.scale_version_id WHERE r.scale_version_id IS NOT NULL
        AND (v.is_issued<>1 OR s.scale_id IS NOT v.artifact_id OR s.dimension_id IS NOT r.dimension_id
          OR (r.scale_id IS NOT NULL AND r.scale_id<>s.scale_id))""",
      'LEVEL':"""SELECT 1 FROM result_snapshot r LEFT JOIN scale_level l USING(level_id)
        WHERE r.level_id IS NOT NULL AND l.scale_version_id IS NOT r.scale_version_id""",
      'VALUE':"""SELECT 1 FROM result_snapshot WHERE score_kind NOT IN ('REPORTED','UNKNOWN') OR
        (score_kind='REPORTED' AND (reported_value IS NULL OR length(trim(reported_value))=0)) OR
        (score_kind='UNKNOWN' AND reported_value IS NOT NULL) OR length(trim(source_locator))=0 OR length(trim(interpretation_origin))=0""",
      'OWNER':"""SELECT 1 FROM assessment_snapshot a JOIN version_snapshot v ON v.version_id=a.assessment_version_id WHERE a.assessment_id<>v.artifact_id
        UNION SELECT 1 FROM result_snapshot r JOIN version_snapshot v ON v.version_id=r.result_version_id WHERE r.result_id<>v.artifact_id""",
      'PARENT':"""SELECT 1 FROM result_snapshot r JOIN result_snapshot p ON p.result_id=r.result_id
        JOIN assessment_snapshot a ON a.assessment_version_id=r.assessment_version_id
        JOIN assessment_snapshot b ON b.assessment_version_id=p.assessment_version_id WHERE a.assessment_id<>b.assessment_id"""}
    for code,query in checks.items():
        if c.execute(query+' LIMIT 1').fetchone():raise ValueError('R-ASSESSMENT-DATA-'+code)
    for row in c.execute('SELECT recorded_at,reference_at,valid_from,valid_to FROM assessment_snapshot'):
        for value in row:
            if value is None:continue
            try:
                parsed=datetime.fromisoformat(value.removesuffix('Z')+'+00:00')
                if len(value)!=20 or parsed.isoformat(timespec='seconds').replace('+00:00','Z')!=value:raise ValueError()
            except (ValueError,TypeError):raise ValueError('R-ASSESSMENT-DATA-TIME') from None
        if row[2] is not None and row[3] is not None and row[3]<row[2]:raise ValueError('R-ASSESSMENT-DATA-TIME-ORDER')
    for table,key in (('assessment_snapshot','assessment_version_id'),('result_snapshot','result_version_id')):
        columns=[r[1] for r in c.execute('PRAGMA table_info('+table+')')]
        differences=' OR '.join(f"json_type(v.payload_json,'$.{col}') IS NULL OR json_extract(v.payload_json,'$.{col}') IS NOT m.{col}" for col in columns)
        if c.execute(f'SELECT 1 FROM {table} m JOIN version_snapshot v ON v.version_id=m.{key} WHERE v.is_issued=1 AND ({differences}) LIMIT 1').fetchone():
            raise ValueError('R-ASSESSMENT-DATA-PAYLOAD')


def migrate(c):
    base.require_configuration(c)
    version=c.execute('PRAGMA user_version').fetchone()[0]
    if version<3:
        # Base reader verifies exact accepted schema/ledger before extension.
        # An outer transaction also rolls back an intermediate 1->2 upgrade
        # if extension installation fails.
        with base.transaction(c):
            base.migrate(c)
            before=base.logical_snapshot(c)
            text=migration_text();base.execute_script(c,text)
            c.execute('INSERT INTO schema_migration VALUES(3,?)',(hashlib.sha256(text.encode()).hexdigest(),))
            c.execute('PRAGMA user_version=3')
            if base.logical_snapshot(c)!=before:
                raise ValueError('R-ASSESSMENT-MIGRATION-DATA-LOSS')
            health(c)
    else:health(c)


def connect(path=':memory:'):
    c=base.connect(path);migrate(c);return c


def snapshot(c):
    tables=base.TABLES+NEW_TABLES
    return {table:sorted([list(r) for r in c.execute('SELECT * FROM '+table)],key=lambda r:json.dumps(r,ensure_ascii=False)) for table in tables}


def add_artifact(c,iri,cid,label,source=SOURCE,code=None):
    # New classes share the accepted artifact identity table. Exact subtype
    # membership is separate and cannot reinterpret an already issued artifact.
    base.add_identity(c,iri,'artifact')
    kind='RKM-C014' if cid in ('RKM-C032','RKM-C033','RKM-C034','RKM-C038','RKM-C039') else cid
    c.execute('INSERT INTO information_artifact(artifact_id,kind,label,source_record_id) VALUES(?,?,?,?)',(iri,kind,label,source))
    if kind!=cid:
        vocabulary=cid in ('RKM-C038','RKM-C039')
        c.execute('INSERT INTO artifact_typing VALUES(?,?,?,?,?,?)',(iri,cid,U('scheme') if vocabulary else None,U('scheme-edition') if vocabulary else None,code if vocabulary else None,source))


def stage_version(c,version,artifact,payload=None,source=SOURCE):
    base.add_identity(c,version,'version')
    c.execute('INSERT INTO version_snapshot(version_id,artifact_id,payload_json,source_record_id) VALUES(?,?,?,?)',
        (version,artifact,json.dumps({'synthetic':'versioned assertion'} if payload is None else payload,ensure_ascii=False,separators=(',',':')),source))


def seal(c,version,time=TIME):
    c.execute('UPDATE version_snapshot SET issued_at=?,is_issued=1 WHERE version_id=?',(time,version))


def default_assessment(name='new'):
    return dict(assessment_version_id=U(name+'-v1'),assessment_id=U(name),basis_id=U('basis'),basis_version_id=U('basis-v1'),
        context_id=BASE('context'),context_version_id=BASE('context-v1'),method_id=BASE('method'),method_version_id=U('method-v3'),
        temporal_context_id=U('time-context'),recorded_at=TIME,reference_at=None,valid_from=None,valid_to=None,source_record_id=SOURCE)


def default_result(name='new-result'):
    return dict(result_version_id=U(name+'-v1'),result_id=U(name),dimension_id=U('dimension'),scale_id=BASE('scale'),
        scale_version_id=U('scale-v3'),level_id=U('level-v3'),score_kind='REPORTED',reported_value='0',
        source_record_id=SOURCE,source_locator='synthetic/declared-fixture',interpretation_origin='deterministic synthetic generator; not source evidence')


def insert_dict(c,table,values):
    # Table/column choices come from this trusted API, never a supplied SQL string.
    allowed={'assessment_snapshot':('assessment_version_id','assessment_id','basis_id','basis_version_id','context_id','context_version_id','method_id','method_version_id','temporal_context_id','recorded_at','reference_at','valid_from','valid_to','source_record_id'),
        'result_snapshot':('result_version_id','result_id','assessment_version_id','dimension_id','scale_id','scale_version_id','level_id','score_kind','reported_value','source_record_id','source_locator','interpretation_origin')}
    cols=allowed[table]
    if set(values)!=set(cols):raise ValueError('R-API-FIELDS')
    c.execute('INSERT INTO '+table+'('+','.join(cols)+') VALUES('+','.join('?' for _ in cols)+')',[values[k] for k in cols])


def issue_bundle(c,assessment,results):
    base.require_configuration(c)
    if any(item.get('reported_value') is not None and not isinstance(item['reported_value'],str) for item in results):
        raise ValueError('R-REPORTED-LEXEME-TYPE')
    with base.transaction(c):
        aid=assessment['assessment_id']
        if not c.execute('SELECT 1 FROM information_artifact WHERE artifact_id=?',(aid,)).fetchone():
            add_artifact(c,aid,'RKM-C032','Synthetic assessment',assessment['source_record_id'])
        stage_version(c,assessment['assessment_version_id'],aid,payload=assessment,source=assessment['source_record_id'])
        insert_dict(c,'assessment_snapshot',assessment)
        for item in results:
            row=dict(item,assessment_version_id=assessment['assessment_version_id'])
            if not c.execute('SELECT 1 FROM information_artifact WHERE artifact_id=?',(row['result_id'],)).fetchone():
                add_artifact(c,row['result_id'],'RKM-C034','Same result label',row['source_record_id'])
            stage_version(c,row['result_version_id'],row['result_id'],payload=row,source=row['source_record_id'])
            insert_dict(c,'result_snapshot',row)
            seal(c,row['result_version_id'])
        seal(c,assessment['assessment_version_id'])


def prepare_catalog(c):
    with base.transaction(c):
        c.execute('INSERT INTO source_record VALUES(?,?)',(SOURCE,'{"score":null,"case":null,"synthetic":true}'))
        for label,cid,code in [('dimension','RKM-C039','DIM'),('other-dimension','RKM-C039','DIM-OTHER'),('basis','RKM-C033',None),('level-v3','RKM-C038','LEVEL-3'),('level-v4','RKM-C038','LEVEL-4'),('late-level','RKM-C038','LATE-LEVEL')]:
            add_artifact(c,U(label),cid,label,code=code)
        stage_version(c,U('basis-v1'),U('basis'));seal(c,U('basis-v1'))
        for v in ('scale-v3','scale-v4'):
            stage_version(c,U(v),BASE('scale'))
            c.execute('INSERT INTO scale_snapshot VALUES(?,?,?,?)',(U(v),BASE('scale'),U('dimension'),SOURCE))
            c.execute('INSERT INTO scale_level VALUES(?,?,?)',(U('level-v'+v[-1]),U(v),SOURCE))
            seal(c,U(v))
        stage_version(c,U('method-v3'),BASE('method'))
        c.execute('INSERT INTO method_scope VALUES(?,?,?,?)',(U('method-v3'),BASE('scale'),U('dimension'),SOURCE))
        seal(c,U('method-v3'))
        stage_version(c,U('unissued-method'),BASE('method'))


def baseline(path=':memory:',populated=True):
    c=base.connect(path);base.migrate(c,1)
    base.seed_v1(c,json.loads((base.OUT/'fixtures.json').read_text()))
    base.migrate(c);migrate(c)
    if populated:
        prepare_catalog(c)
        for name,value in [('a1','0'),('a2','0'),('a-unknown',None)]:
            result=default_result('r1' if name=='a1' else 'r2' if name=='a2' else 'unknown-result')
            result.update(reported_value=value,score_kind='UNKNOWN' if value is None else 'REPORTED')
            issue_bundle(c,default_assessment(name),[result])
    return c


def lookup(c,result_version):
    return c.execute((OUT/'queries/comparison_inputs.sql').read_text(),{'result_version':result_version}).fetchone()


def compare(c,left,right):
    health(c)
    old=c.row_factory;c.row_factory=sqlite3.Row
    try:rows=[lookup(c,value) for value in (left,right)]
    finally:c.row_factory=old
    fields=('context_id','context_version_id','method_id','method_version_id','basis_id','basis_version_id','temporal_context_id','dimension_id','scale_id','scale_version_id','level_id')
    if any(row is None or any(row[key] is None for key in fields) for row in rows):return 'NOT_READY'
    for row in rows:
        if not c.execute('SELECT 1 FROM method_scope WHERE method_version_id=? AND scale_id=? AND dimension_id=?',(row['method_version_id'],row['scale_id'],row['dimension_id'])).fetchone():return 'NOT_READY'
    same=fields[:-1]  # Different permissible levels may be compared, never numerically ordered here.
    return 'SCOPED_DIRECT_COMPARISON_ADMISSIBLE' if all(rows[0][key]==rows[1][key] for key in same) else 'NOT_ADMISSIBLE_BY_EXACT_PIN_POLICY'


def restore_dump(c,text):
    base.require_configuration(c)
    items=[s for s in base.statements(text) if s.strip().upper() not in ('BEGIN TRANSACTION;','COMMIT;')]
    tables=[s for s in items if s.lstrip().upper().startswith('CREATE TABLE')]
    inserts=[s for s in items if s.lstrip().upper().startswith('INSERT INTO')]
    other=[s for s in items if s not in tables and s not in inserts]
    with base.transaction(c):
        c.execute('PRAGMA defer_foreign_keys=ON')
        for statement in tables+inserts+other:c.execute(statement)
        c.execute('PRAGMA user_version=3')
        health(c)
