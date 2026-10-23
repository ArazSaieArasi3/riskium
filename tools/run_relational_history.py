"""Run the actual SQLite populated migration, negative operations and history round trips."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from datetime import datetime,timezone
from collections import Counter
from rdflib import Graph,URIRef
from rdflib.compare import isomorphic
import relational_history as h
from build_relational_history import ROOT,OUT as PROFILE,RISK,render,digest

OUT=ROOT/'evaluation/relational/history'
FIXTURE=PROFILE/'fixtures.json'
SOURCE='urn:riskium:sql:source'
U=lambda s:'urn:riskium:sql:'+s
INPUTS=['ontology/riskium-model.json','ontology/derived/riskium.owl.ttl','evaluation/coverage-review.json',
 'implementation/relational/0.1.0/001_tables.sql','implementation/relational/0.1.0/002_guards.sql',
 'implementation/relational/0.1.0/mapping.json','implementation/relational/0.1.0/fixtures.json',
 'tools/build_relational_history.py','tools/relational_history.py','tools/run_relational_history.py']


def baseline(target=2,path=':memory:'):
    c=h.connect(path);h.migrate(c,1);h.seed_v1(c,json.loads(FIXTURE.read_text()))
    if target==2:h.migrate(c)
    return c


def draft(c,name='draft',artifact='entry1',entry='entry1',prev='rev2',payload='{"text":"new","unknown":null}'):
    c.execute('INSERT INTO working_draft VALUES(?,?,?,?,?,?)',(U(name),U(artifact),U(entry) if entry else None,U(prev) if prev else None,payload,SOURCE))


def snapshot_record(c,name='new',artifact='entry1',entry='entry1',prev=None,payload='{"text":"new"}'):
    h.add_identity(c,U(name),'version')
    c.execute('INSERT INTO version_snapshot(version_id,artifact_id,entry_id,previous_version_id,payload_json,source_record_id) VALUES(?,?,?,?,?,?)',
        (U(name),U(artifact),U(entry) if entry else None,U(prev) if prev else None,payload,SOURCE))


def historical_rows(c):
    return [list(r) for r in c.execute('SELECT version_id,previous_version_id,payload_json,source_record_id,issued_at FROM v_issued_history WHERE entry_id=? ORDER BY version_id',(U('entry1'),))]


def native_edges(c):
    rdf_type='http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
    return sorted([[s,p.removeprefix(RISK),o] for s,p,o in c.execute('SELECT subject,predicate,object FROM v_native_facts WHERE predicate<>?',(rdf_type,))])


def specs():
    result=[]
    def add(cid,sql=None,params=(),expected=None,error=None,setup=None,action=None,kind='operation',target=2,unchanged=False):
        result.append(dict(id=cid,sql=sql,params=list(params),expected=expected,error=error,setup=setup,action=action,kind=kind,target=target,unchanged=unchanged))
    add('MIGRATE-POPULATED-V1',action='migrate-preserve',expected=True,target=1,kind='migration')
    add('MIGRATE-IDEMPOTENT',action='migrate-idempotent',expected=True,kind='migration')
    add('MIGRATE-INVALID-CYCLE-ATOMIC',action='migrate-invalid-cycle',error='R-MIGRATION-CYCLE',target=1,unchanged=True,kind='migration')
    add('MIGRATE-INVALID-DEPENDENCY-ATOMIC',action='migrate-invalid-dependency',error='R-MIGRATION-DEPENDENCY',target=1,unchanged=True,kind='migration')
    add('MIGRATE-INVALID-CONTENT-ATOMIC',action='migrate-invalid-content',error='R-MIGRATION-ISSUED-CONTENT',target=1,unchanged=True,kind='migration')
    add('MIGRATE-INVALID-REVISION-ATOMIC',action='migrate-invalid-revision',error='R-MIGRATION-REVISION-TARGET',target=1,unchanged=True,kind='migration')
    add('MIGRATE-FOREIGN-KEY-ATOMIC',action='migrate-invalid-fk',error='R-MIGRATION-FOREIGN-KEY',target=1,unchanged=True,kind='migration')
    add('MIGRATE-SOURCE-HASH-DRIFT',action='migrate-hash-drift',error='R-MIGRATION-SOURCE-HASH',target=1,unchanged=True,kind='migration')
    add('MIGRATE-SCHEMA-DRIFT',action='migrate-schema-drift',error='R-MIGRATION-SCHEMA-DRIFT',unchanged=True,kind='migration')
    add('CONFIGURATION-REQUIRED',action='configuration',error='R-CONNECTION-POLICY: foreign_keys and recursive_triggers must be ON',unchanged=True,kind='preflight')
    add('RECURSIVE-CONFIGURATION-REQUIRED',action='recursive-configuration',error='R-CONNECTION-POLICY: foreign_keys and recursive_triggers must be ON',unchanged=True,kind='preflight')
    add('RAW-UNKNOWN-IS-PRESERVED',"SELECT json_type(original_json,'$.score'),json_extract(original_json,'$.case') FROM source_record WHERE record_id=?",(U('raw'),),[['null',None]])
    add('DUPLICATE-LABELS-DISTINCT-CASES','SELECT case_id FROM risk_case WHERE label=? ORDER BY case_id',('Same label',),[[U('case1')],[U('case2')]])
    add('ONE-CASE-MULTIPLE-ENTRIES','SELECT entry_id,register_id FROM register_entry WHERE case_id=? ORDER BY entry_id',(U('case1'),),[[U('entry1'),U('register1')],[U('entry2'),U('register2')]])
    add('HISTORY-EXACT',action='history',expected=json.loads(FIXTURE.read_text())['expected_history'])
    add('DEPENDENCY-SNAPSHOTS-EXACT',"SELECT owner_version_id,slot,target_version_id,direct_artifact_id FROM version_dependency ORDER BY owner_version_id,slot",expected=json.loads(FIXTURE.read_text())['expected_pins'])
    add('NATIVE-EDGES-EXACT',action='native',expected=sorted(json.loads(FIXTURE.read_text())['expected_native_edges']))
    for field,value in [('payload_json','{"changed":true}'),('source_record_id',U('raw')),('artifact_id',U('method')),
        ('issued_at','2026-10-20T00:00:00Z'),('is_issued',0)]:
        add('ISSUED-NO-UPDATE-'+field.upper(),f'UPDATE version_snapshot SET {field}=? WHERE version_id=?',(value,U('artifact-v1')),error='R-ISSUED-IMMUTABLE',unchanged=True)
    add('ISSUED-NO-DELETE','DELETE FROM version_snapshot WHERE version_id=?',(U('artifact-v1'),),error='R-ISSUED-IMMUTABLE',unchanged=True)
    add('ISSUED-NO-REPLACE',"INSERT OR REPLACE INTO version_snapshot(version_id,artifact_id,payload_json,source_record_id) VALUES(?,?,?,?)",(U('artifact-v1'),U('artifact'),'{"changed":true}',SOURCE),error='R-VERSION-DUPLICATE',unchanged=True)
    add('ISSUED-NO-UPDATE-OR-REPLACE',action='update-or-replace',error='R-ISSUED-IMMUTABLE',unchanged=True)
    add('MANAGED-ENTRY-MISSING-CASE','INSERT INTO register_entry(entry_id,case_id,register_id) VALUES(?,?,?)',(U('new-entry'),U('missing'),U('register1')),setup='new-entry',error='FOREIGN KEY constraint failed',unchanged=True)
    add('MANAGED-ENTRY-WRONG-REGISTER-KIND','INSERT INTO register_entry(entry_id,case_id,register_id) VALUES(?,?,?)',(U('new-entry'),U('case1'),U('method')),setup='new-entry',error='FOREIGN KEY constraint failed',unchanged=True)
    add('MANAGED-ENTRY-UNKNOWN-CASE-NOT-ADMITTED','INSERT INTO register_entry(entry_id,case_id,register_id) VALUES(?,?,?)',(U('new-entry'),None,U('register1')),setup='new-entry',error='NOT NULL constraint failed: register_entry.case_id',unchanged=True)
    add('IDENTITY-CROSS-FAMILY-REFERENCE','INSERT INTO risk_case(case_id,label,source_record_id) VALUES(?,?,?)',(U('method'),'Not a case',SOURCE),error='FOREIGN KEY constraint failed',unchanged=True)
    for table,column,key in [('source_record','original_json',SOURCE),('risk_case','label',U('case1')),('information_artifact','label',U('entry1'))]:
        idcol={'source_record':'record_id','risk_case':'case_id','information_artifact':'artifact_id'}[table]
        add('CATALOG-NO-UPDATE-'+table.upper(),f'UPDATE {table} SET {column}=? WHERE {idcol}=?',('{"changed":true}' if table=='source_record' else 'changed',key),error='R-CATALOG-IMMUTABLE',unchanged=True)
    add('SOURCE-NO-REPLACE','INSERT OR REPLACE INTO source_record VALUES(?,?)',(SOURCE,'{"changed":true}'),error='R-CATALOG-DUPLICATE',unchanged=True)
    add('IDENTITY-NO-CROSS-FAMILY-REPLACE','INSERT OR REPLACE INTO identity_registry VALUES(?,?)',(U('case1'),'artifact'),error='R-CATALOG-DUPLICATE',unchanged=True)
    add('CATALOG-NO-DELETE-CASCADE','DELETE FROM information_artifact WHERE artifact_id=?',(U('entry1'),),error='R-CATALOG-IMMUTABLE',unchanged=True)
    add('DEPENDENCY-NO-LATE-APPEND','INSERT INTO version_dependency VALUES(?,?,?,?)',(U('rev1'),'Scale',U('scale-v1'),U('scale')),error='R-DEPENDENCY-FROZEN',unchanged=True)
    add('DEPENDENCY-NO-UPDATE','UPDATE version_dependency SET target_version_id=? WHERE owner_version_id=? AND slot=?',(U('method-v2'),U('rev1'),'Method'),error='R-DEPENDENCY-FROZEN',unchanged=True)
    add('DEPENDENCY-NO-DELETE','DELETE FROM version_dependency WHERE owner_version_id=? AND slot=?',(U('rev1'),'Method'),error='R-DEPENDENCY-FROZEN',unchanged=True)
    add('DEPENDENCY-NO-REPLACE','INSERT OR REPLACE INTO version_dependency VALUES(?,?,?,?)',(U('rev1'),'Method',U('method-v2'),U('method')),error='R-DEPENDENCY-DUPLICATE',unchanged=True)
    add('WORKING-DRAFT-EDITABLE',action='draft-edit',expected='{"text":"edited draft"}')
    add('ISSUE-NEW-REVISION-PRESERVES-OLD-PINS',action='issue-revision',expected=[[U('rev1'),'Method',U('method-v1')],[U('rev2'),'Method',U('method-v1')],[U('rev5'),'Method',U('method-v2')]])
    add('ISSUE-NEW-REVISION-SNAPSHOT-EXACT',action='issue-revision-details',expected={'new':[U('rev5'),U('entry1'),U('entry1'),U('rev2'),'{"text":"new","unknown":null}',SOURCE,'2026-10-03T00:00:00Z'],'prior_history_matches':True,'draft_count':0})
    add('ISSUE-GENERIC-ARTIFACT-VERSION',action='issue-generic',expected=[[U('artifact-v2'),None]])
    for label,setup,error in [('EMPTY-CONTENT','empty','R-ISSUE-CONTENT-REQUIRED'),('MISSING-TIME','time','R-ISSUE-TIME-REQUIRED'),
        ('WRONG-DEPENDENCY-KIND','kind','R-DEPENDENCY-TARGET-KIND'),('WRONG-DIRECT-ARTIFACT','direct','R-DEPENDENCY-DIRECT-TARGET'),
        ('UNISSUED-DEPENDENCY','unissued','R-DEPENDENCY-TARGET-NOT-ISSUED'),('ENTRY-WITHOUT-REVISION-TARGET','entry','R-REVISION-TARGET-KIND')]:
        add('ISSUE-ROLLBACK-'+label,action='issue-invalid',setup=setup,error=error,unchanged=True)
    add('REVISION-OF-EQUALS-VERSION-OF',action='mismatched-targets',error='CHECK constraint failed: revision_target',unchanged=True)
    add('PREDECESSOR-CROSS-ENTRY',action='bad-predecessor',setup='rev3',error='R-PREDECESSOR-SAME-ISSUED-ENTRY',unchanged=True)
    add('PREDECESSOR-MISSING',action='bad-predecessor',setup='missing',error='R-PREDECESSOR-SAME-ISSUED-ENTRY',unchanged=True)
    add('PREDECESSOR-SELF-CYCLE',action='bad-predecessor',setup='new',error='R-PREDECESSOR-CYCLE',unchanged=True)
    add('PREDECESSOR-BRANCH-ALLOWED',action='branch',expected=2)
    add('PREDECESSOR-SKIP-ALLOWED',action='skip',expected=U('rev1'))
    add('PREDECESSOR-17-CHAIN',action='long-chain',expected=17)
    add('CYCLE-DETECTED-WITHOUT-IMMUTABILITY',action='cycle-guard',error='R-PREDECESSOR-CYCLE',unchanged=True,kind='mutation-control')
    add('DELETED-IMMUTABILITY-EXPOSES-CHANGE',action='mutant-payload',expected='{"changed":true}',kind='mutation-control')
    add('DELETED-DEPENDENCY-GUARD-EXPOSES-APPEND',action='mutant-dependency',expected=1,kind='mutation-control')
    add('DELETED-CYCLE-GUARD-EXPOSES-CYCLE',action='mutant-cycle',expected=U('rev2'),kind='mutation-control')
    add('TRANSACTION-FAILURE-ROLLS-BACK-PRIOR-WRITES',action='transaction-rollback',error='R-ISSUED-IMMUTABLE',unchanged=True)
    add('FILE-CLOSE-REOPEN-MIGRATION',action='disk',expected=True,kind='roundtrip')
    add('SQL-DUMP-RESTORE-EXACT',action='dump',expected=True,kind='roundtrip')
    add('SQL-BACKUP-EXACT',action='backup',expected=True,kind='roundtrip')
    add('RDF-SELECTED-FACTS-ROUNDTRIP',action='rdf',expected=True,kind='roundtrip')
    add('FOREIGN-KEY-CHECK','PRAGMA foreign_key_check',expected=[])
    add('INTEGRITY-CHECK','PRAGMA integrity_check',expected=[['ok']])
    return result


def setup_case(c,s):
    action=s['action']
    if s['setup']=='new-entry':
        h.add_identity(c,U('new-entry'),'artifact');c.execute('INSERT INTO information_artifact(artifact_id,kind,label,source_record_id) VALUES(?,?,?,?)',(U('new-entry'),'RKM-C022','New entry',SOURCE))
    if action=='migrate-invalid-cycle':c.execute('UPDATE version_snapshot SET previous_version_id=? WHERE version_id=?',(U('rev2'),U('rev1')))
    elif action=='migrate-invalid-dependency':c.execute("UPDATE version_dependency SET target_version_id=? WHERE owner_version_id=? AND slot='Method'",(U('scale-v1'),U('rev1')))
    elif action=='migrate-invalid-content':c.execute("UPDATE version_snapshot SET payload_json='{}' WHERE version_id=?",(U('rev1'),))
    elif action=='migrate-invalid-revision':c.execute('UPDATE version_snapshot SET entry_id=NULL WHERE version_id=?',(U('rev1'),))
    elif action=='migrate-invalid-fk':
        c.execute('PRAGMA foreign_keys=OFF');c.execute('UPDATE register_entry SET case_id=? WHERE entry_id=?',(U('missing'),U('entry1')));c.execute('PRAGMA foreign_keys=ON')
    elif action=='migrate-hash-drift':c.execute("UPDATE schema_migration SET sha256='changed' WHERE version=1")
    elif action=='migrate-schema-drift':c.execute('DROP TRIGGER snapshot_immutable_update')
    elif action=='configuration':c.execute('PRAGMA foreign_keys=OFF')
    elif action=='recursive-configuration':c.execute('PRAGMA recursive_triggers=OFF')
    elif action=='update-or-replace':snapshot_record(c,'unissued','artifact',None)
    elif action=='issue-invalid':
        payload='{}' if s['setup']=='empty' else '{"text":"new"}'
        draft(c,entry=None if s['setup']=='entry' else 'entry1',prev=None if s['setup']=='entry' else 'rev2',payload=payload)
        if s['setup']=='kind':c.execute('INSERT INTO draft_dependency VALUES(?,?,?,?)',(U('draft'),'Context',U('method-v1'),None))
        if s['setup']=='direct':c.execute('INSERT INTO draft_dependency VALUES(?,?,?,?)',(U('draft'),'Method',U('method-v1'),U('scale')))
        if s['setup']=='unissued':
            snapshot_record(c,'unissued','method',None);c.execute('INSERT INTO draft_dependency VALUES(?,?,?,?)',(U('draft'),'Method',U('unissued'),None))
    elif action in ('cycle-guard','mutant-cycle'):
        c.execute('DROP TRIGGER snapshot_immutable_update')
        if action=='mutant-cycle':c.execute('DROP TRIGGER snapshot_cycle_update')
    elif action=='mutant-payload':c.execute('DROP TRIGGER snapshot_immutable_update')
    elif action=='mutant-dependency':c.execute('DROP TRIGGER dependency_frozen_insert')


def perform(c,s):
    a=s['action']
    if s['sql'] is not None:
        cur=c.execute(s['sql'],s['params']);return [list(r) for r in cur.fetchall()] if cur.description else cur.rowcount
    if a=='migrate-preserve':
        before=h.logical_snapshot(c);h.migrate(c);return h.logical_snapshot(c)==before and c.execute('PRAGMA user_version').fetchone()[0]==2
    if a=='migrate-idempotent':
        before=(h.logical_snapshot(c),h.schema_snapshot(c),list(c.execute('SELECT * FROM schema_migration')));h.migrate(c)
        return before==(h.logical_snapshot(c),h.schema_snapshot(c),list(c.execute('SELECT * FROM schema_migration')))
    if a.startswith('migrate-'):h.migrate(c);return None
    if a in ('configuration','recursive-configuration'):h.require_configuration(c)
    if a=='update-or-replace':c.execute('UPDATE OR REPLACE version_snapshot SET version_id=? WHERE version_id=?',(U('artifact-v1'),U('unissued')))
    if a=='history':return historical_rows(c)
    if a=='native':return native_edges(c)
    if a=='draft-edit':
        draft(c);c.execute('UPDATE working_draft SET payload_json=? WHERE draft_id=?',('{"text":"edited draft"}',U('draft')))
        return c.execute('SELECT payload_json FROM working_draft WHERE draft_id=?',(U('draft'),)).fetchone()[0]
    if a in ('issue-revision','issue-revision-details'):
        draft(c);c.execute('INSERT INTO draft_dependency VALUES(?,?,?,?)',(U('draft'),'Method',U('method-v2'),U('method')))
        h.issue_draft(c,U('draft'),U('rev5'),'2026-10-03T00:00:00Z')
        if a=='issue-revision-details':
            row=c.execute('SELECT version_id,artifact_id,entry_id,previous_version_id,payload_json,source_record_id,issued_at FROM v_issued_history WHERE version_id=?',(U('rev5'),)).fetchone()
            return {'new':list(row),'prior_history_matches':historical_rows(c)[:2]==json.loads(FIXTURE.read_text())['expected_history'],
                'draft_count':c.execute('SELECT count(*) FROM working_draft').fetchone()[0]}
        return [list(r) for r in c.execute("SELECT owner_version_id,slot,target_version_id FROM version_dependency WHERE slot='Method' ORDER BY owner_version_id")]
    if a=='issue-generic':
        draft(c,artifact='artifact',entry=None,prev=None);h.issue_draft(c,U('draft'),U('artifact-v2'),'2026-10-03T00:00:00Z')
        return [list(r) for r in c.execute('SELECT version_id,entry_id FROM v_issued_history WHERE version_id=?',(U('artifact-v2'),))]
    if a=='issue-invalid':h.issue_draft(c,U('draft'),U('rev5'),None if s['setup']=='time' else '2026-10-03T00:00:00Z')
    if a=='mismatched-targets':
        with h.transaction(c):snapshot_record(c,entry='entry2')
    if a=='bad-predecessor':
        with h.transaction(c):snapshot_record(c,prev=s['setup'])
    if a=='branch':
        draft(c,'draft-a',prev='rev1');h.issue_draft(c,U('draft-a'),U('rev-branch'),'2026-10-03T00:00:00Z')
        return c.execute('SELECT count(*) FROM version_snapshot WHERE previous_version_id=?',(U('rev1'),)).fetchone()[0]
    if a=='skip':
        draft(c,prev='rev1');h.issue_draft(c,U('draft'),U('rev-skip'),'2026-10-03T00:00:00Z')
        return c.execute('SELECT previous_version_id FROM version_snapshot WHERE version_id=?',(U('rev-skip'),)).fetchone()[0]
    if a=='long-chain':
        previous='rev1'
        for i in range(16):
            name='long-'+str(i);draft(c,'d-'+name,prev=previous);h.issue_draft(c,U('d-'+name),U(name),'2026-10-03T00:00:00Z');previous=name
        return c.execute("""WITH RECURSIVE lineage(id) AS (SELECT ? UNION SELECT v.previous_version_id FROM version_snapshot v JOIN lineage l ON v.version_id=l.id WHERE v.previous_version_id IS NOT NULL) SELECT count(*) FROM lineage""",(U(previous),)).fetchone()[0]
    if a in ('cycle-guard','mutant-cycle'):
        c.execute('UPDATE version_snapshot SET previous_version_id=? WHERE version_id=?',(U('rev2'),U('rev1')))
        return c.execute('SELECT previous_version_id FROM version_snapshot WHERE version_id=?',(U('rev1'),)).fetchone()[0]
    if a=='mutant-payload':
        c.execute('UPDATE version_snapshot SET payload_json=? WHERE version_id=?',('{"changed":true}',U('artifact-v1')))
        return c.execute('SELECT payload_json FROM version_snapshot WHERE version_id=?',(U('artifact-v1'),)).fetchone()[0]
    if a=='mutant-dependency':
        c.execute('INSERT INTO version_dependency VALUES(?,?,?,?)',(U('rev1'),'Scale',U('scale-v1'),U('scale')))
        return c.execute("SELECT count(*) FROM version_dependency WHERE owner_version_id=? AND slot='Scale'",(U('rev1'),)).fetchone()[0]
    if a=='transaction-rollback':
        with h.transaction(c):
            draft(c);c.execute('UPDATE version_snapshot SET payload_json=? WHERE version_id=?',('{"changed":true}',U('rev1')))
    if a=='disk':
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'migration.sqlite';d=baseline(1,path);before=h.logical_snapshot(d);d.close();d=h.connect(path);h.migrate(d);d.close()
            d=h.connect(path);h.migrate(d);same=h.logical_snapshot(d)==before and historical_rows(d)==json.loads(FIXTURE.read_text())['expected_history'];d.close();return same
    if a=='dump':
        text='\n'.join(c.iterdump());d=h.connect();h.restore_dump(d,text);same=h.logical_snapshot(d)==h.logical_snapshot(c) and historical_rows(d)==historical_rows(c);d.close();return same
    if a=='backup':
        d=h.connect();c.backup(d);h.migrate(d);same=h.logical_snapshot(d)==h.logical_snapshot(c);d.close();return same
    if a=='rdf':
        g=Graph()
        for row in c.execute('SELECT subject,predicate,object FROM v_native_facts'):g.add(tuple(URIRef(n) for n in row))
        return isomorphic(g,Graph().parse(data=g.serialize(format='nt'),format='nt')) and native_edges(c)==sorted(json.loads(FIXTURE.read_text())['expected_native_edges'])
    raise ValueError('Unknown action: '+str(a))


def record_state(c,states):
    state={'rows':h.logical_snapshot(c),'schema':h.schema_snapshot(c),'ledger':[list(r) for r in c.execute('SELECT * FROM schema_migration ORDER BY version')],
        'user_version':c.execute('PRAGMA user_version').fetchone()[0]}
    text=json.dumps(state,sort_keys=True,separators=(',',':'));key=hashlib.sha256(text.encode()).hexdigest();states.setdefault(key,{'json':text});return key


def execute(s,states):
    c=baseline(s['target']);setup_case(c,s);sql_trace=[];c.set_trace_callback(sql_trace.append)
    before=record_state(c,states);error=None;observed=None
    try:observed=perform(c,s)
    except (sqlite3.Error,ValueError) as e:error=str(e)
    after=record_state(c,states);c.close()
    matches=(error==s['error']) if s['error'] else error is None and observed==s['expected']
    if s['unchanged']:matches=matches and before==after
    return dict(id=s['id'],kind=s['kind'],action=s['action'],sql=s['sql'],params=s['params'],expected=s['expected'],expected_error=s['error'],
        observed=observed,error=error,unchanged_required=s['unchanged'],before_state=before,after_state=after,
        status='PASS' if matches else 'FAIL',sql_trace=sql_trace)


def run():
    sql,mapping=render()
    if (PROFILE/'002_guards.sql').read_text()!=sql or json.loads((PROFILE/'mapping.json').read_text())!=mapping:raise ValueError('Relational generated profile changed')
    states={};rows=[execute(s,states) for s in specs()]
    failed=[r for r in rows if r['status']!='PASS']
    for r in failed:print(json.dumps({k:r[k] for k in ('id','observed','expected','error','expected_error','before_state','after_state')}),flush=True)
    if failed:raise ValueError('Relational oracle failure')
    return dict(schema='riskium-relational-history-evidence-v1',source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        generated_at_utc=datetime.now(timezone.utc).isoformat(),inputs={p:digest(ROOT/p) for p in INPUTS},
        engine={'name':'SQLite','version':sqlite3.sqlite_version,'python':sys.version.split()[0],'foreign_keys':True,'recursive_triggers':True},
        provenance='Execution checkout plus exact input hashes; receipt may be committed subsequently. Public synthetic schema-v1 baseline, not a migration of the private database.',
        summary={'scenarios':len(rows),'statuses':dict(Counter(r['status'] for r in rows)),
            'by_kind':dict(Counter(r['kind'] for r in rows)),'native_relations_exported':5,'concepts_and_support_kinds':10},
        native_semantics_changed=False,postgresql_executed=False,owner_review_completed=False,independent_acceptance=False,
        outcome='SCOPED_SQLITE_IDENTITY_HISTORY_ROUTE_EXECUTED',states=states,cases=rows)


def verify_saved(saved,fresh):
    for key in ('inputs','summary','outcome','native_semantics_changed','postgresql_executed','owner_review_completed','independent_acceptance'):
        if saved[key]!=fresh[key]:raise ValueError('Relational receipt accounting/binding differs: '+key)
    for key,value in saved['states'].items():
        if hashlib.sha256(value['json'].encode()).hexdigest()!=key:raise ValueError('Stored SQL state hash differs')
    if len(saved['cases'])!=len(fresh['cases']):raise ValueError('Relational case population differs')
    for old,new in zip(saved['cases'],fresh['cases']):
        for key in ('id','kind','action','sql','params','expected','expected_error','observed','error','unchanged_required','before_state','after_state','status'):
            if old[key]!=new[key]:raise ValueError('Relational saved oracle/state differs: '+new['id']+' '+key)


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--database',type=Path);a=p.parse_args()
    if a.database:
        if a.database.exists():p.error('Database path must be new; existing databases are never overwritten')
        c=baseline(2,a.database);c.close();print(json.dumps({'public_synthetic_database':str(a.database),'sqlite':sqlite3.sqlite_version}));return
    report=run();path=OUT/'report.json.gz'
    if a.check:verify_saved(json.loads(gzip.decompress(path.read_bytes())),report)
    else:
        OUT.mkdir(parents=True,exist_ok=True);path.write_bytes(gzip.compress((json.dumps(report,indent=2)+'\n').encode(),mtime=0))
        lines=['# Executed SQLite identity and issued-history slice 0.1.0','',
            '**Scoped application/history evidence, not full relational or ontology acceptance.** Model/OWL unchanged; no PostgreSQL run or owner/independent judgment is claimed.','',
            'Execution checkout `'+report['source_commit']+'`; [full compressed receipt](report.json.gz), [mapping](../../../implementation/relational/0.1.0/mapping.json) and [scope/dictionary](README.md). Exact input hashes bind all executed files.','',
            'Engine: SQLite '+report['engine']['version']+'; foreign_keys=ON and recursive_triggers=ON. Schema 1 is populated from public synthetic fixtures, then upgraded transactionally to schema 2 without rebuilding its rows. The private historical companion is not copied or migrated by this suite.','',
            'Summary: '+json.dumps(report['summary'])+'. SQL traces, exact errors, before/after logical/schema/ledger snapshots, migration rollback and selected round trips are retained. A PASS means the expected acceptance, rejection or control outcome matched; mutants are not admitted domain cases.','',
            '| Case | Kind | Expected SQL error | Verdict |','| --- | --- | --- | --- |']
        for r in report['cases']:lines.append(f"| `{r['id']}` | {r['kind']} | {r['expected_error'] or '—'} | {r['status']} |")
        lines+=['','Replay with `python tools/run_relational_history.py --check`. Runtime versions are recorded per execution; the semantic/schema/state comparisons must match across supported SQLite >=3.38 environments. Byte-identical database files across SQLite versions are not claimed.']
        (OUT/'report.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(dict(report['summary'],engine=report['engine'])),flush=True)


if __name__=='__main__':main()
