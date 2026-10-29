"""SQLite schema 10: source-qualified risk-nature history with exact version pins."""
from functools import lru_cache
import hashlib
import json
import sqlite3

import relational_assessment_selection as previous
import relational_history as b
import relational_assessment as a
from relational_evidence import canonical_utc

ROOT = previous.ROOT
OUT = ROOT / 'implementation/relational/0.9.0'
SQL = OUT / '010_risk_nature.sql'
COMMON = ('narrative','source_record_id','source_locator','interpretation_origin','recorded_at')
SUPPORT = ('version_id','artifact_id','native_class') + COMMON
CONTEXT = ('version_id','artifact_id') + COMMON + ('objective_version_ids',)
ASSERTION = ('version_id','artifact_id','case_id','term_version_id','context_version_id') + COMMON
ENTRY = ('version_id','entry_id','previous_version_id') + COMMON + ('nature_version_ids',)
CORRECTION = ('corrected_version_id','prior_version_id','actor','reason','source_record_id','source_locator','interpretation_origin','recorded_at')
ENVELOPE = dict(selection='ALL_EXPLICIT_ISSUED_VERSIONS', independent_corroboration='NOT_ASSESSED',
                factual_correctness='NOT_ASSESSED', occurrence='NOT_INFERRED')
RISK = 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'


def fail(code):
    raise ValueError('NRA-'+code)


def sha(data):return hashlib.sha256(data).hexdigest()
def encode(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def migration_text():return SQL.read_text()
def digest():return sha(migration_text().encode())
state = previous.state
state_sha256 = previous.state_sha256


def bindings():
    manifest=json.loads((OUT/'declaration-manifest.json').read_text())
    for path,h in manifest['files_sha256'].items():
        if sha((ROOT/path).read_bytes())!=h:fail('DECLARATION_BINDING: '+path)
    if sha((OUT/'declaration-manifest.json').read_bytes())!='29f274634feffcce8f3fd5852917b32ee085bdb6f3ccbfe81f02d2025a06d1b4':fail('DECLARATION_MANIFEST')
    contract=json.loads((OUT/'contract.json').read_text())
    for path,h in contract['source_sha256'].items():
        if sha((ROOT/path).read_bytes())!=h:fail('SOURCE_BINDING: '+path)
    component=json.loads((OUT/'component.json').read_text())
    for path,h in component['files_sha256'].items():
        if sha((ROOT/path).read_bytes())!=h:fail('RUNTIME_BINDING: '+path)


@lru_cache(maxsize=4)
def expected_schema(sql_digest):
    db=a.connect()
    try:
        previous.c.migrate(db); previous.previous.k.migrate(db); previous.previous.l.migrate(db)
        previous.e.migrate(db); previous.previous.migrate(db); previous.migrate(db)
        b.execute_script(db,migration_text())
        return b.schema_snapshot(db)
    finally:db.close()


def audit_data(db):
    previous.audit_data(db)
    bad=db.execute('SELECT version_id,code FROM v_nature_invalid LIMIT 1').fetchone()
    if bad:fail('DATA_'+bad[1]+': '+bad[0])
    # Exact payload and owner audits above include unsealed staged rows. A sealed
    # typed identity cannot bypass its required explicit semantic snapshot.
    if db.execute('''SELECT 1 FROM nature_membership m JOIN version_snapshot v USING(artifact_id)
      WHERE v.is_issued=1 AND NOT EXISTS(SELECT 1 FROM v_nature_expected_payload p WHERE p.version_id=v.version_id) LIMIT 1''').fetchone():fail('DATA_METADATA')
    if db.execute('''WITH RECURSIVE w(root,id) AS (
      SELECT corrected_version_id,prior_version_id FROM nature_correction UNION
      SELECT w.root,c.prior_version_id FROM w JOIN nature_correction c ON c.corrected_version_id=w.id)
      SELECT 1 FROM w WHERE root=id LIMIT 1''').fetchone():fail('DATA_CORRECTION_CYCLE')
    for table in ('nature_support','nature_context','nature_snapshot','nature_entry','nature_correction'):
        for (value,) in db.execute('SELECT recorded_at FROM '+table):canonical_utc(value,'NRA-TIME')


def health(db):
    b.require_configuration(db);bindings()
    ledger=dict(db.execute('SELECT version,sha256 FROM schema_migration'))
    expected_schema_rows=expected_schema(digest())
    # Independently reconstruct the trusted old migration ledger, not a prefix
    # copied from the database being checked.
    old={1:sha((b.OUT/'001_tables.sql').read_bytes()),2:sha((b.OUT/'002_guards.sql').read_bytes()),
         3:a.migration_hash(),4:previous.c.digest(),5:previous.previous.k.digest(),6:previous.previous.l.digest(),
         7:previous.e.digest(),8:previous.previous.digest(),9:sha(previous.migration_text().encode()),10:digest()}
    if ledger!=old or db.execute('PRAGMA user_version').fetchone()[0]!=10:fail('LEDGER')
    if b.schema_snapshot(db)!=expected_schema_rows:fail('SCHEMA')
    if db.execute('PRAGMA foreign_key_check').fetchall() or db.execute('PRAGMA integrity_check').fetchall()!=[('ok',)]:fail('INTEGRITY')
    audit_data(db)


def migrate(db):
    b.require_configuration(db)
    version=db.execute('PRAGMA user_version').fetchone()[0]
    if version==10:health(db);return 'ALREADY_CURRENT'
    if version!=9:fail('REQUIRES_V9')
    with b.transaction(db):
        bindings();previous.health(db);before=state(db)
        b.execute_script(db,migration_text())
        db.execute('INSERT INTO schema_migration VALUES(10,?)',(digest(),));db.execute('PRAGMA user_version=10')
        after=state(db)
        for table,rows in before['rows'].items():
            retained=[r for r in after['rows'][table] if table!='schema_migration' or r[0]!=10]
            if rows!=retained:fail('MIGRATION_DATA_LOSS')
        if not all(r in after['schema'] for r in before['schema']):fail('MIGRATION_SCHEMA_LOSS')
        health(db)
    return 'UPGRADED'


def connect(path):
    db=b.connect(path)
    try:migrate(db)
    except BaseException:db.close();raise
    return db


def rows(db,query,args=()):return previous.rows(db,query,args)


def text(value,code):
    if not isinstance(value,str) or not value.strip():fail(code)


def provenance(db,record):
    for k in ('source_record_id','source_locator','interpretation_origin'):
        text(record.get(k),'PROVENANCE')
    if 'narrative' in record:text(record['narrative'],'PROVENANCE')
    if not db.execute('SELECT 1 FROM source_record WHERE record_id=?',(record['source_record_id'],)).fetchone():fail('PROVENANCE')
    canonical_utc(record.get('recorded_at'),'NRA-TIME')


def fields(record,required,label=False):
    if not isinstance(record,dict) or set(record)!=set(required)|({'label'} if label else set()):fail('INPUT_FIELDS')
    if label:text(record['label'],'IDENTITY')


def target(db,version,table,kind,code):
    text(version,code)
    # Table is an internal constant chosen by this module, never caller input.
    query='SELECT t.*,v.is_issued FROM '+table+' t JOIN version_snapshot v USING(version_id) WHERE t.version_id=?'
    found=rows(db,query,(version,))
    if not found or found[0]['is_issued']!=1 or (kind and found[0].get('native_class')!=kind):fail(code)
    return found[0]


def no_later(child,owner):
    if child['recorded_at']>owner['recorded_at']:fail('TIME')


def identity(db,record,kind,scheme=None,code=None):
    ident=record['artifact_id'];text(ident,'IDENTITY')
    existing=db.execute('SELECT kind FROM information_artifact WHERE artifact_id=?',(ident,)).fetchone()
    if existing is None:
        try:
            b.add_identity(db,ident,'artifact')
            db.execute('INSERT INTO information_artifact(artifact_id,kind,label,source_record_id) VALUES(?,?,?,?)',
                       (ident,kind if kind=='RKM-C002' else 'RKM-C014',record['label'],record['source_record_id']))
        except sqlite3.IntegrityError:fail('IDENTITY')
    if kind=='RKM-C002':
        if existing and existing[0]!=kind:fail('CONTEXT_VERSION')
        return
    member=db.execute('SELECT native_class,scheme_id,code FROM nature_membership WHERE artifact_id=?',(ident,)).fetchone()
    if member is not None:
        if member!=(kind,scheme,code):fail('IDENTITY')
    else:
        try:db.execute('INSERT INTO nature_membership VALUES(?,?,?,?)',(ident,kind,scheme,code))
        except sqlite3.IntegrityError:fail('IDENTITY')


def stage_version(db,record,entry=False):
    version=record['version_id'];text(version,'IDENTITY')
    try:b.add_identity(db,version,'version')
    except sqlite3.IntegrityError:fail('IDENTITY')
    payload={k:v for k,v in record.items() if k!='label'}
    db.execute('''INSERT INTO version_snapshot(version_id,artifact_id,entry_id,previous_version_id,payload_json,source_record_id)
      VALUES(?,?,?,?,?,?)''',(version,record['entry_id'] if entry else record['artifact_id'],record['entry_id'] if entry else None,
                            record['previous_version_id'] if entry else None,encode(payload),record['source_record_id']))


def insert(db,table,record):
    keys=list(record)
    db.execute('INSERT INTO '+table+'('+','.join(keys)+') VALUES('+','.join('?' for _ in keys)+')',[record[k] for k in keys])


def stage_support(db,record):
    kind=record.get('native_class')
    fields(record,SUPPORT+(('code','scheme_version_id') if kind=='RKM-C006' else ()),True);provenance(db,record)
    if kind not in ('RKM-C006','RKM-C018','RKM-X02'):fail('IDENTITY')
    scheme=None
    if kind=='RKM-C006':
        dep=target(db,record['scheme_version_id'],'nature_support','RKM-C018','TERM_VERSION');no_later(dep,record)
        scheme=dep['artifact_id'];text(record['code'],'IDENTITY')
    identity(db,record,kind,scheme,record.get('code'));stage_version(db,record)
    insert(db,'nature_support',{k:v for k,v in record.items() if k!='label'})


def stage_context(db,record):
    fields(record,CONTEXT,True);provenance(db,record)
    pins=record['objective_version_ids']
    if not isinstance(pins,list) or any(not isinstance(p,str) for p in pins) or len(pins)!=len(set(pins)):fail('OBJECTIVE_VERSION')
    deps=[target(db,p,'nature_support','RKM-X02','OBJECTIVE_VERSION') for p in pins]
    if len({d['artifact_id'] for d in deps})!=len(deps):fail('OBJECTIVE_VERSION')
    for dep in deps:no_later(dep,record)
    record=dict(record,objective_version_ids=sorted(pins));identity(db,record,'RKM-C002');stage_version(db,record)
    insert(db,'nature_context',{k:v for k,v in record.items() if k not in ('label','objective_version_ids')})
    for dep in deps:db.execute('INSERT INTO nature_objective VALUES(?,?,?)',(record['version_id'],dep['version_id'],dep['artifact_id']))


def stage_bundle(db,bundle):
    fields(bundle,('assertion','recording_revisions','correction'))
    record=bundle['assertion'];fields(record,ASSERTION,True);provenance(db,record)
    if not db.execute('SELECT 1 FROM risk_case WHERE case_id=?',(record['case_id'],)).fetchone():fail('CASE')
    dep=target(db,record['term_version_id'],'nature_support','RKM-C006','TERM_VERSION');no_later(dep,record)
    if record['context_version_id'] is not None:
        dep=target(db,record['context_version_id'],'nature_context',None,'CONTEXT_VERSION');no_later(dep,record)
    recorders=bundle['recording_revisions']
    if not isinstance(recorders,list) or not recorders:fail('RECORDING')
    for entry in recorders:
        fields(entry,ENTRY);provenance(db,entry)
        case=db.execute('SELECT case_id FROM register_entry WHERE entry_id=?',(entry['entry_id'],)).fetchone()
        if case!=(record['case_id'],) or entry['nature_version_ids']!=[record['version_id']]:fail('RECORDING')
        if db.execute('SELECT 1 FROM version_snapshot WHERE version_id=?',(entry['version_id'],)).fetchone():fail('RECORDING')
        if entry['previous_version_id'] is not None:
            prior=db.execute('SELECT entry_id,is_issued,issued_at FROM version_snapshot WHERE version_id=?',(entry['previous_version_id'],)).fetchone()
            if not prior or prior[:2]!=(entry['entry_id'],1):fail('RECORDING')
            if prior[2]>entry['recorded_at']:fail('TIME')
        if entry['recorded_at']!=record['recorded_at']:fail('TIME')
    if db.execute('SELECT 1 FROM nature_snapshot WHERE artifact_id=? AND case_id<>?',(record['artifact_id'],record['case_id'])).fetchone():fail('IDENTITY')
    identity(db,record,'RKM-C005');stage_version(db,record)
    insert(db,'nature_snapshot',{k:v for k,v in record.items() if k!='label'})
    for entry in recorders:
        stage_version(db,entry,True)
        insert(db,'nature_entry',{k:v for k,v in entry.items() if k!='nature_version_ids'})
        db.execute('INSERT INTO nature_entry_link VALUES(?,?)',(entry['version_id'],record['version_id']))


def issue_support(db,record):
    health(db)
    with b.transaction(db):stage_support(db,record);a.seal(db,record['version_id'],record['recorded_at']);health(db)


def issue_context(db,record):
    health(db)
    with b.transaction(db):stage_context(db,record);a.seal(db,record['version_id'],record['recorded_at']);health(db)


def correction(db,record):
    fields(record,CORRECTION);provenance(db,record)
    for k in ('actor','reason'):text(record[k],'PROVENANCE')
    ends=[target(db,record[k],'nature_snapshot',None,'CORRECTION') for k in ('corrected_version_id','prior_version_id')]
    if ends[0]['artifact_id']!=ends[1]['artifact_id'] or ends[0]['case_id']!=ends[1]['case_id'] or ends[0]['version_id']==ends[1]['version_id']:fail('CORRECTION')
    for end in ends:no_later(end,record)
    insert(db,'nature_correction',record)


def declare_correction(db,record):
    health(db)
    with b.transaction(db):correction(db,record);health(db)


def issue_bundle(db,bundle):
    health(db)
    with b.transaction(db):
        stage_bundle(db,bundle)
        for entry in bundle['recording_revisions']:a.seal(db,entry['version_id'],entry['recorded_at'])
        r=bundle['assertion'];a.seal(db,r['version_id'],r['recorded_at'])
        if bundle['correction'] is not None:correction(db,bundle['correction'])
        health(db)


def _get(db,version):
    if not isinstance(version,str):fail('UNKNOWN_VERSION')
    found=rows(db,(OUT/'queries/exact_version.sql').read_text(),{'version':version})
    if not found:fail('UNKNOWN_VERSION')
    answer=found[0]
    for k in ('objective_version_ids','recording_entry_version_ids'):answer[k]=json.loads(answer[k])
    return answer


def _sources(db,answer):
    references={'assertion':[answer['version_id']], 'term':[answer['term_version_id']], 'scheme':[answer['scheme_version_id']],
                'context':[answer['context_version_id']] if answer['context_version_id'] else [], 'objective':answer['objective_version_ids'],
                'recording':answer['recording_entry_version_ids']}
    result={}
    for role,versions in references.items():
        result[role]=[dict(record_id=r[0],original_json=r[1]) for v in versions for r in db.execute('SELECT s.record_id,s.original_json FROM version_snapshot v JOIN source_record s ON s.record_id=v.source_record_id WHERE v.version_id=?',(v,))]
    result['correction']=[dict(record_id=r[0],original_json=r[1]) for r in db.execute('SELECT s.record_id,s.original_json FROM nature_correction c JOIN source_record s ON s.record_id=c.source_record_id WHERE c.corrected_version_id=?',(answer['version_id'],))]
    return result


def get(db,version):
    health(db);answer=_get(db,version)
    return dict(row=answer,sources=_sources(db,answer),dependencies=_dependencies(db,answer),**ENVELOPE)


def _dependencies(db,answer):
    result={}
    for role,table,versions in (
        ('term','nature_support',[answer['term_version_id']]),('scheme','nature_support',[answer['scheme_version_id']]),
        ('context','nature_context',[answer['context_version_id']] if answer['context_version_id'] else []),
        ('objectives','nature_support',answer['objective_version_ids']),('recording','nature_entry',answer['recording_entry_version_ids'])):
        result[role]=[rows(db,'SELECT * FROM '+table+' WHERE version_id=?',(v,))[0] for v in versions]
    return result


def by_case(db,case):
    health(db)
    if not isinstance(case,str):fail('UNKNOWN_CASE')
    if not db.execute('SELECT 1 FROM risk_case WHERE case_id=?',(case,)).fetchone():fail('UNKNOWN_CASE')
    versions=[v[0] for v in db.execute((OUT/'queries/by_case.sql').read_text(),{'case':case})]
    return dict(rows=[_get(db,v) for v in versions],sources={v:_sources(db,_get(db,v)) for v in versions},**ENVELOPE)


def family(db,version):
    health(db);_get(db,version)
    lineage=[list(r) for r in db.execute((OUT/'queries/family.sql').read_text(),{'root':version})]
    return dict(lineage=lineage,rows=[_get(db,r[0]) for r in lineage],
                corrections=rows(db,'SELECT * FROM nature_correction WHERE corrected_version_id IN (SELECT value FROM json_each(?)) ORDER BY corrected_version_id',(json.dumps([r[0] for r in lineage]),)),
                sources={r[0]:_sources(db,_get(db,r[0])) for r in lineage},**ENVELOPE)


def native_graph(db,version):
    """Project actual pinned SQL values; no declaration fixture/oracle is read."""
    from rdflib import Graph,RDF,URIRef
    health(db);r=_get(db,version);g=Graph()
    def triple(s,p,o):g.add((URIRef(s),URIRef(p),URIRef(o)))
    def types(s,*classes):
        for cls in classes:triple(s,str(RDF.type),RISK+cls)
    def artifact(s,*classes):types(s,*classes,'RKM-C014')
    def ver(v,owner):types(v,'RKM-C015');triple(v,RISK+'RX-006',owner)
    artifact(r['artifact_id'],'RKM-C005');ver(version,r['artifact_id']);types(r['case_id'],'RKM-X01')
    artifact(r['term_id'],'RKM-C006','RKM-C019','RKM-C017');ver(r['term_version_id'],r['term_id'])
    artifact(r['scheme_id'],'RKM-C018');ver(r['scheme_version_id'],r['scheme_id']);triple(r['term_id'],RISK+'R-05',r['scheme_id'])
    triple(r['artifact_id'],RISK+'R-41',r['case_id']);triple(r['artifact_id'],RISK+'R-42',r['term_id'])
    if r['context_id']:
        artifact(r['context_id'],'RKM-C002');ver(r['context_version_id'],r['context_id']);triple(r['artifact_id'],RISK+'R-43',r['context_id'])
        for v in r['objective_version_ids']:
            owner=db.execute('SELECT artifact_id FROM nature_support WHERE version_id=?',(v,)).fetchone()[0]
            artifact(owner,'RKM-X02');ver(v,owner);triple(r['context_id'],RISK+'RK2-011',owner)
    for v in r['recording_entry_version_ids']:
        e=rows(db,'SELECT e.entry_id,r.register_id FROM nature_entry e JOIN register_entry r USING(entry_id) WHERE e.version_id=?',(v,))[0]
        ver(v,e['entry_id']);types(v,'RKM-C023');artifact(e['entry_id'],'RKM-C022');artifact(e['register_id'],'RKM-C030')
        triple(v,RISK+'R-44',r['artifact_id']);triple(v,RISK+'R-33',e['entry_id']);triple(e['entry_id'],RISK+'R-01',r['case_id']);triple(e['entry_id'],RISK+'RX-008',e['register_id'])
    return g


def restore_dump(db,dump,expected_state_sha256):
    b.require_configuration(db)
    if not isinstance(expected_state_sha256,str) or len(expected_state_sha256)!=64:fail('RESTORE_DIGEST')
    statements=[s for s in b.statements(dump) if s.strip().upper() not in ('BEGIN TRANSACTION;','COMMIT;')]
    allowed=('CREATE TABLE ','CREATE INDEX ','CREATE UNIQUE INDEX ','CREATE VIEW ','CREATE TRIGGER ','INSERT INTO ','DELETE FROM SQLITE_SEQUENCE','DELETE FROM "SQLITE_SEQUENCE"')
    if any(not s.lstrip().upper().startswith(allowed) for s in statements):fail('RESTORE_STATEMENT')
    clocks=[s for s in statements if 'SQLITE_SEQUENCE' in s.lstrip().upper()[:40] and s.lstrip().upper().startswith(('INSERT INTO','DELETE FROM'))]
    statements=[s for s in statements if s not in clocks]
    tables=[s for s in statements if s.lstrip().upper().startswith('CREATE TABLE')]
    inserts=[s for s in statements if s.lstrip().upper().startswith('INSERT INTO')]
    rest=[s for s in statements if s not in tables+inserts]
    with b.transaction(db):
        db.execute('PRAGMA defer_foreign_keys=ON')
        for statement in tables+inserts+rest+clocks:db.execute(statement)
        db.execute('PRAGMA user_version=10');health(db)
        if state_sha256(db)!=expected_state_sha256:fail('RESTORE_DIGEST')
