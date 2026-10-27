"""Replay fixed source/scenario SQL/RDF oracles and migration/recovery controls."""
import argparse
from collections import Counter
import copy
import hashlib
import json
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch

from rdflib import Graph,RDF,URIRef
from rdflib.compare import isomorphic
import relational_source_scenario as k
import relational_history as b
import relational_assessment as a
import relational_correction as c
from run_relational_assessment import graph as prior_graph
from run_relational_correction import complete_family

ROOT=k.ROOT
OUT=ROOT/'evaluation/relational/source-scenario'
FIXTURE=k.OUT/'fixtures.json'
INPUTS=['implementation/relational/0.4.0/contract.json','implementation/relational/0.4.0/fixtures.json','implementation/relational/0.4.0/005_source_scenario.sql','implementation/relational/0.4.0/queries/by_case.sql','implementation/relational/0.4.0/queries/provenance.sql','tools/relational_source_scenario.py','tools/run_relational_source_scenario.py']

def fixture():return json.loads(FIXTURE.read_text())
def prior(path=':memory:'):
    db=a.baseline(path);c.migrate(db);complete_family(db);return db

def fresh(path=':memory:',seed=False):
    db=prior(path);k.migrate(db)
    if seed:
        for row in fixture()['sources']:db.execute('INSERT INTO source_record VALUES(?,?)',row)
    return db

def populate(db):
    for row in fixture()['sources']:db.execute('INSERT INTO source_record VALUES(?,?)',row)
    for row in fixture()['records']:k.issue(db,row)

def state(db):
    return dict(rows=k.snapshot(db),schema=b.schema_snapshot(db),version=db.execute('PRAGMA user_version').fetchone()[0])

def state_hash(db):return hashlib.sha256(json.dumps(state(db),sort_keys=True,separators=(',',':')).encode()).hexdigest()

def uri(value):return URIRef(a.BASE(value[1:]) if value.startswith('@') else k.U(value))

def expected_graph(name):
    data=fixture()['graphs'][name];g=Graph()
    for s,t in data['types']:g.add((uri(s),RDF.type,URIRef(k.RISK+t)))
    for s,p,o in data['edges']:g.add((uri(s),URIRef(k.RISK+p),uri(o)))
    return g

def execute():
    f=fixture();rows=[]
    def add(ident,expected,observed,kind='positive',detail=None):
        rows.append(dict(id=ident,kind=kind,expected=expected,observed=observed,status='PASS' if expected==observed else 'FAIL',detail=detail))
    db=prior();old=k.legacy_snapshot(db);graphs=[prior_graph(db,a.U('a1-v'+v)) for v in ('1','2','3')];k.migrate(db)
    add('POPULATED_UPGRADE',True,old==k.legacy_snapshot(db))
    add('LEGACY_GRAPH_PRESERVED',True,all(isomorphic(g,prior_graph(db,a.U('a1-v'+str(i+1)))) for i,g in enumerate(graphs)))
    old=state_hash(db);k.migrate(db);add('IDEMPOTENT_UPGRADE',old,state_hash(db));db.close()
    db=prior();old=dict(rows=c.snapshot(db),schema=b.schema_snapshot(db),version=4)
    with patch.object(k,'migration_text',return_value=k.migration_text()+'\nINSERT INTO missing_table VALUES(1);\n'):
        try:k.migrate(db);rejected=False
        except sqlite3.OperationalError:rejected=True
    add('FAILED_UPGRADE',True,rejected and old==dict(rows=c.snapshot(db),schema=b.schema_snapshot(db),version=db.execute('PRAGMA user_version').fetchone()[0]),'negative');db.close()
    db=fresh();populate(db)
    add('CASE1_HISTORY',f['case1_rows'],k.by_case(db,a.BASE('case1'))['rows'])
    add('CASE2_HISTORY',f['case2_rows'],k.by_case(db,a.BASE('case2'))['rows'])
    original=f['records'][0]
    expected=[original['version_id'],original['source_record_id'],f['sources'][0][1],original['source_locator'],original['interpretation_origin'],original['narrative']]
    add('PROVENANCE_EXACT',expected,list(db.execute((k.OUT/'queries/provenance.sql').read_text(),{'version_id':original['version_id']}).fetchone()))
    add('OLD_VERSION_CONTEXT',[[a.BASE('context'),a.BASE('context-v1')]], [list(r) for r in db.execute('SELECT context_id,context_version_id FROM knowledge_context WHERE version_id=?',(k.U('scenario-a-v1'),))])
    add('UNKNOWN_CONTEXT',[],[list(r) for r in db.execute('SELECT context_id FROM knowledge_context WHERE version_id=?',(k.U('scenario-a-v2'),))])
    add('EQUAL_LABEL_IDENTITIES',4,db.execute("SELECT count(DISTINCT artifact_id) FROM knowledge_type t JOIN information_artifact a USING(artifact_id) WHERE a.label='Same label'").fetchone()[0])
    add('RAW_EXCLUSION',True,not db.execute('SELECT 1 FROM risk_case WHERE case_id=?',(k.U('withheld'),)).fetchone() and not len(k.native_graph(db,k.U('raw-document'))))
    combined=Graph()
    for name in f['graphs']:
        for t in k.native_graph(db,k.U(name)):combined.add(t)
    add('NO_OCCURRENCE_CAUSATION',True,not any(str(o) in {k.RISK+'RKM-C004',k.RISK+'RKM-C007',k.RISK+'RKM-C065',k.RISK+'RKM-C066'} for _,_,o in combined) and not any(str(p) in {k.RISK+'R-25',k.RISK+'RK3-002'} for _,p,_ in combined))
    add('NO_GENERAL_CORRECTION',True,not any('revision' in str(p).lower() or 'correct' in str(p).lower() for _,p,_ in combined))
    add('BOUND_PARAMETER',[],k.by_case(db,"'; DROP TABLE risk_case; --")['rows'])
    for name,ident in [('scenario-a-v1','NATIVE_SCENARIO_A1'),('scenario-a-v2','NATIVE_SCENARIO_A2'),('scenario-b-v1','NATIVE_SCENARIO_B1'),('reference-a-v1','NATIVE_REFERENCE_A1'),('reference-a-v2','NATIVE_REFERENCE_A2'),('reference-b-v1','NATIVE_REFERENCE_B1')]:
        expected=expected_graph(name);actual=k.native_graph(db,k.U(name))
        add(ident,True,isomorphic(expected,actual),detail=dict(expected_nt=sorted(expected.serialize(format='nt').splitlines()),observed_nt=sorted(actual.serialize(format='nt').splitlines())))
    # Three different storage recovery paths, with exact logical/graph comparison.
    old=state_hash(db)
    with tempfile.TemporaryDirectory() as folder:
        path=Path(folder)/'backup.sqlite';target=b.connect(path);db.backup(target);target.close()
        reopened=k.connect(path);add('BACKUP_REOPEN',old,state_hash(reopened));reopened.close()
        live=Path(folder)/'live.sqlite';filedb=fresh(live);populate(filedb);filedb.close()
        reopened=k.connect(live);add('FILE_REOPEN',old,state_hash(reopened));reopened.close()
    dump='\n'.join(db.iterdump());restored=b.connect();k.restore_dump(restored,dump);add('DUMP_RESTORE',old,state_hash(restored));restored.close()
    # Real deleted-clause mutation: the weakened seal admits a scenario with no case.
    mutant=fresh(seed=True);r=copy.deepcopy(f['records'][0]);r['case_ids']=[]
    text=mutant.execute("SELECT sql FROM sqlite_master WHERE type='trigger' AND name='knowledge_seal'").fetchone()[0]
    start=text.index(" SELECT CASE WHEN EXISTS(SELECT 1 FROM v_knowledge_invalid WHERE version_id=NEW.version_id AND code='CARDINALITY')")
    end=text.index(" SELECT CASE WHEN EXISTS(SELECT 1 FROM v_knowledge_invalid WHERE version_id=NEW.version_id AND code='PAYLOAD')",start)
    changed=text[:start]+text[end:]
    changed=changed.replace("SELECT 1 FROM v_knowledge_invalid WHERE version_id=NEW.version_id)","SELECT 1 FROM v_knowledge_invalid WHERE version_id=NEW.version_id AND code<>'CARDINALITY')")
    mutant.execute('DROP TRIGGER knowledge_seal');mutant.execute(changed)
    k.stage(mutant,r);a.seal(mutant,r['version_id'],r['recorded_at'])
    add('MUTANT_CARDINALITY_EXPOSED',True,mutant.execute('SELECT is_issued FROM version_snapshot WHERE version_id=?',(r['version_id'],)).fetchone()[0]==1,'mutation');mutant.close()
    mutant=fresh();populate(mutant);mutant.execute('DROP TRIGGER knowledge_case_delete')
    mutant.execute('DELETE FROM knowledge_case WHERE version_id=? AND case_id=?',(k.U('scenario-a-v1'),a.BASE('case1')))
    add('MUTANT_FROZEN_LINK_EXPOSED',0,mutant.execute('SELECT count(*) FROM knowledge_case WHERE version_id=?',(k.U('scenario-a-v1'),)).fetchone()[0],'mutation');mutant.close()
    expected=expected_graph('reference-a-v1');actual=k.native_graph(db,k.U('reference-a-v1'))
    triple=(uri('@case1'),URIRef(k.RISK+'RK3-001'),uri('reference-a'));actual.remove(triple);actual.add((triple[2],triple[1],triple[0]))
    add('MUTANT_DIRECTION_EXPOSED',False,isomorphic(expected,actual),'mutation');db.close()
    # Each rejection is isolated, matches its predeclared diagnostic and must roll back.
    for ident,diagnostic in f['rejection_diagnostics'].items():
        db=fresh(seed=True);r=copy.deepcopy(f['records'][0])
        try:
            if ident=='CONFIGURATION_OFF':db.execute('PRAGMA foreign_keys=OFF')
            if ident=='NO_CASE':r['case_ids']=[]
            elif ident=='MISSING_CASE' or ident=='ATOMIC_BUNDLE_FAILURE':r['case_ids']=[a.BASE('case1'),k.U('missing-case')]
            elif ident=='WRONG_CONTEXT_KIND':r['context_version_ids']=[a.BASE('scale-v1')]
            elif ident=='UNISSUED_CONTEXT':r['context_version_ids']=[k.U('unissued-context')]
            elif ident=='MISSING_SOURCE':r['source_record_id']=k.U('missing-source')
            elif ident=='EMPTY_PROVENANCE':r['source_locator']=' '
            elif ident=='BAD_CALENDAR':r['recorded_at']='2026-02-30T00:00:00Z'
            elif ident=='DUPLICATE_CASE':r['case_ids']*=2
            elif ident=='DUPLICATE_CONTEXT':r['context_version_ids']*=2
            if ident=='UNISSUED_CONTEXT':a.stage_version(db,k.U('unissued-context'),a.BASE('context'))
            if ident=='REFERENCE_MULTI_CONTEXT':
                a.add_artifact(db,k.U('second-context'),'RKM-C002','Other context');a.stage_version(db,k.U('second-context-v1'),k.U('second-context'));a.seal(db,k.U('second-context-v1'))
                r=copy.deepcopy(f['records'][3]);r['context_version_ids']=[a.BASE('context-v1'),k.U('second-context-v1')]
            if ident in ('DUPLICATE_VERSION','MIXED_CLASS','IMMUTABLE_SNAPSHOT','IMMUTABLE_CASE','IMMUTABLE_CONTEXT','REPLACE_SNAPSHOT','REPLACE_CASE','REPLACE_CONTEXT'):
                k.issue(db,r)
                if ident=='MIXED_CLASS':r['version_id']=k.U('mixed-v1');r['native_class']='RKM-X06'
            before=state(db)
            with b.transaction(db):
                if ident=='CONTEXT_OWNER_MISMATCH':
                    r['context_version_ids']=[]
                    k.stage(db,r);db.execute('INSERT INTO knowledge_context VALUES(?,?,?)',(r['version_id'],a.BASE('method'),a.BASE('context-v1')))
                elif ident in ('FORGED_SOURCE','OWNER_DRIFT'):
                    # Staged version is owned/source-qualified independently of the attempted row.
                    k.stage(db,r)
                    other=copy.deepcopy(r);other['version_id']=k.U('forged-v1')
                    a.stage_version(db,other['version_id'],r['artifact_id'],payload=k.payload(other),source=other['source_record_id'])
                    if ident=='FORGED_SOURCE':other['source_record_id']=k.U('document-b')
                    else:other['artifact_id']=a.BASE('method')
                    db.execute('INSERT INTO knowledge_snapshot VALUES(?,?,?,?,?,?,?)',tuple(other[key] for key in k.FIELDS))
                elif ident=='PAYLOAD_DRIFT':
                    k.stage(db,r);db.execute("UPDATE version_snapshot SET payload_json=json_set(payload_json,'$.narrative','tampered') WHERE version_id=?",(r['version_id'],));a.seal(db,r['version_id'],r['recorded_at'])
                elif ident.startswith('IMMUTABLE_'):
                    table={'IMMUTABLE_SNAPSHOT':'knowledge_snapshot','IMMUTABLE_CASE':'knowledge_case','IMMUTABLE_CONTEXT':'knowledge_context'}[ident]
                    db.execute('DELETE FROM '+table+' WHERE version_id=?',(r['version_id'],))
                elif ident.startswith('REPLACE_'):
                    table={'REPLACE_SNAPSHOT':'knowledge_snapshot','REPLACE_CASE':'knowledge_case','REPLACE_CONTEXT':'knowledge_context'}[ident]
                    db.execute('INSERT OR REPLACE INTO '+table+' SELECT * FROM '+table+' WHERE version_id=?',(r['version_id'],))
                elif ident=='LEDGER_DRIFT':db.execute("UPDATE schema_migration SET sha256='wrong' WHERE version=5");k.health(db)
                elif ident=='SCHEMA_DRIFT':db.execute('DROP INDEX knowledge_case_lookup');k.health(db)
                elif ident=='CONFIGURATION_OFF':k.health(db)
                elif ident=='RESTORE_TAMPER':
                    original=fresh();populate(original)
                    lines=[line for line in original.iterdump() if not (line.startswith('INSERT INTO "knowledge_case"') and k.U('scenario-a-v1') in line)]
                    original.close();empty=b.connect()
                    try:k.restore_dump(empty,'\n'.join(lines))
                    finally:empty.close()
                else:k.issue(db,r)
            observed='ACCEPTED'
        except (ValueError,sqlite3.DatabaseError) as exc:
            observed=diagnostic if diagnostic in str(exc) else 'WRONG_DIAGNOSTIC: '+str(exc)
        add(ident,diagnostic,observed,'negative',detail=dict(rollback_preserved=state(db)==before))
        if state(db)!=before:rows[-1]['status']='FAIL'
        db.close()
    # A valid staged but unissued bundle is not a managed native graph.
    db=fresh(seed=True);r=copy.deepcopy(f['records'][0]);k.stage(db,r);k.health(db)
    add('UNISSUED_EXCLUDED',[],list(k.native_graph(db,r['version_id'])));db.close()
    declared=set(f['case_ids']);actual=[r['id'] for r in rows]
    if set(actual)!=declared or len(actual)!=len(declared):raise ValueError('Lost/duplicate predeclared source/scenario case IDs')
    rows.sort(key=lambda r:r['id'])
    return dict(schema='riskium-source-scenario-execution-v1',profile='0.4.0',schema_version=5,runtime=dict(sqlite=sqlite3.sqlite_version,scope='Actual local engine; CI replays print their actual runtime separately.'),inputs_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in INPUTS},summary=dict(cases=len(rows),outcomes=dict(Counter(r['status'] for r in rows)),kinds=dict(Counter(r['kind'] for r in rows))),cases=rows,independent_semantic_validation=False,stable_distribution_changed=False)


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    report=execute()
    if report['summary']['outcomes']!={'PASS':54}:
        print(json.dumps([r for r in report['cases'] if r['status']!='PASS'],indent=2));raise SystemExit('Source/scenario oracle mismatch')
    target=OUT/'report.json'
    if args.check:
        expected=json.loads(target.read_text())
        for key in ('inputs_sha256','summary','cases'):
            if report[key]!=expected[key]:raise ValueError('Stale source/scenario execution: '+key)
    else:OUT.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='SOURCE_SCENARIO_EXECUTION_PASS',sqlite=sqlite3.sqlite_version,**report['summary'])))

if __name__=='__main__':main()
