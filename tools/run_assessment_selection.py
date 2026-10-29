"""Replay the immutable 44 prospective controls on populated SQLite databases."""
import argparse, copy, hashlib, json, sqlite3, sys, tempfile
from pathlib import Path
from unittest.mock import patch
import relational_assessment_selection as x
import relational_assessment as a
import relational_history as b
import run_relational_evidence_lifecycle as old

U=lambda s:'urn:riskium:assessment-selection:'+s
OUT=x.ROOT/'evaluation/relational/assessment-selection'
M=json.loads((x.OUT/'execution-fixture.json').read_text())
F=json.loads((x.OUT/'fixtures.json').read_text())
TEMPLATE=None

def prior():
 global TEMPLATE
 if TEMPLATE is None:
  TEMPLATE=old.fresh();old.seed_decisions(TEMPLATE)
  for row in M['sources']:TEMPLATE.execute('INSERT INTO source_record VALUES(?,?)',row)
  for name,row in M['bundles'].items():
   if name!='A-v4':a.issue_bundle(TEMPLATE,row['assessment'],row['results'])
  for child,parent in M['corrections']:
   TEMPLATE.execute('INSERT INTO assessment_correction VALUES(?,?,?,?,?)',(U(child),U(parent),M['correction_reason'],M['correction_time'],U('S-decision')))
  x.previous.health(TEMPLATE)
 db=b.connect();TEMPLATE.backup(db);return db

def fresh():
 db=prior();x.migrate(db);return db

def event(kind='SELECT',target='A-v1',context='X',ident='test',assessment='A'):
 return dict(M['event_common'],event_id=ident,kind=kind,assessment_id=U(assessment),decision_context_id=context,target_version=U(target) if target else None)

def timeline(db,through=6):
 for row in F['timeline']:
  if row['sequence']<=through:
   ev=event(row['kind'],row['target_version'],row['decision_context'],'timeline-'+str(row['sequence']));ev['recorded_at']=row['recorded_at']
   assert x.append(db,ev)==row['sequence']

def rejected(db,action):
 before=x.state(db)
 try:action();ok=False;error='ACCEPTED'
 except (ValueError,sqlite3.DatabaseError) as e:ok=True;error=str(e)
 return dict(rejected=ok,all_preoperation_state_preserved=x.state(db)==before),error

def query(db,ctx='X',at=6,artifact='A'):
 raw=x.selection(db,U(artifact),ctx,at)
 if raw['state']!='SELECTED':return dict(state=raw['state'],assessment_version=raw['assessment_version'],results=raw['results'])
 version=raw['assessment_version'].removeprefix(U(''))
 expected=M['bundles'][version]
 owned=sorted([dict(r,assessment_version_id=raw['assessment_version']) for r in expected['results']],key=lambda r:r['result_version_id'])
 exact=raw['assessment']==expected['assessment'] and raw['results']==owned
 return dict(state=raw['state'],assessment_version=version,result_bundle=('exact owned bundle: '+version) if exact else 'BUNDLE_MISMATCH',automatic_comparability=raw['automatic_comparability'])

def sql_event(db,ev,extra=None):
 fields=list(x.FIELDS);values=[ev[k] for k in fields]
 if extra:fields+=list(extra);values+=list(extra.values())
 return db.execute('INSERT INTO assessment_selection_event('+','.join(fields)+') VALUES('+','.join('?' for _ in fields)+')',values)

def execute():
 records=[]
 for case in F['cases']:
  n=int(case['id'][-2:]);db=prior() if n in (1,3) else fresh();details={}
  try:
   if n==1:
    before=x.previous.snapshot(db);old_schema=b.schema_snapshot(db);x.migrate(db);after=x.previous.snapshot(db);after['schema_migration']=[r for r in after['schema_migration'] if r[0]<9]
    observed=dict(user_version=db.execute('PRAGMA user_version').fetchone()[0],old_rows_schema_ledger_payloads_and_graphs_equal=before==after and all(r in b.schema_snapshot(db) for r in old_schema))
   elif n==2:
    before=x.state(db);x.migrate(db);observed=dict(exact_state_equal=before==x.state(db))
   elif n==3:
    sql=x.migration_text()
    with patch.object(x,'migration_text',return_value=sql+'\nINSERT INTO absent_table VALUES(1);\n'):observed,error=rejected(db,lambda:x.migrate(db))
    details['error']=error
   elif n==4:observed=query(db,at=0)
   elif n in (5,6,7,8,10,11,12,14,15,16):
    through,ctx,at={5:(1,'X',1),6:(2,'X',2),7:(6,'X',1),8:(2,'Y',2),10:(4,'X',4),11:(6,'X',3),12:(4,'Y',4),14:(5,'X',5),15:(6,'X',6),16:(6,'X',5)}[n]
    timeline(db,through);observed=query(db,ctx,at)
   elif n==9:
    timeline(db,3);observed={ctx:query(db,ctx,3) for ctx in ('X','Y')}
   elif n in (13,44):
    timeline(db,4 if n==13 else 6);observed,error=rejected(db,lambda:x.append(db,event(target='A-v2')));details['error']=error
   elif n==17:
    timeline(db,5);row=M['bundles']['A-v4'];x.issue(db,row['assessment'],row['results'],dict(prior_version=U('A-v1'),reason=M['correction_reason'],recorded_at=M['correction_time'],source_record_id=U('S-decision')));observed=query(db,at=5)
   elif n in (18,19,20,21,22,27):
    ev=event(target={18:'absent',19:'draft',21:'B-v1'}.get(n,'A-v1'))
    if n==19:
     ass=dict(M['bundles']['A-v1']['assessment'],assessment_version_id=U('draft'));a.stage_version(db,U('draft'),U('A'),payload=ass);a.insert_dict(db,'assessment_snapshot',ass)
    if n==20:ev['target_version']=db.execute('SELECT version_id FROM evidence_snapshot LIMIT 1').fetchone()[0]
    if n==22:ev['decision_context_id']=' '
    action=(lambda:x.selection(db,"'; DROP TABLE result_snapshot;--",'X',0)) if n==27 else lambda:x.append(db,ev)
    observed,error=rejected(db,action);details['error']=error
   elif n in (23,24,25):
    variants=[]
    if n==23:
     for field in ('actor','reason','source_record_id','source_locator','interpretation_origin'):
      for value in (None,'','\t'):
       ev=event();ev[field]=value;variants.append(rejected(db,lambda ev=ev:x.append(db,ev)))
    elif n==24:
     timeline(db)
     for at in (None,True,1.5,-1,7):variants.append(rejected(db,lambda at=at:x.selection(db,U('A'),'X',at)))
     try:x.selection(db,U('A'),'X');missing=False
     except TypeError:missing=True
     variants.append((dict(rejected=missing,all_preoperation_state_preserved=True),'missing argument'))
    else:
     for value in ('invalid','2026-02-30T12:00:00Z','2000-01-01T00:00:00Z'):
      ev=event();ev['recorded_at']=value;variants.append(rejected(db,lambda ev=ev:x.append(db,ev)))
    observed=dict(each_variant_rejected=all(r['rejected'] for r,e in variants),all_preoperation_state_preserved=all(r['all_preoperation_state_preserved'] for r,e in variants));details['errors']=[e for r,e in variants]
   elif n==26:
    timeline(db);before=x.state(db);attempts=[]
    for sql in ["UPDATE assessment_selection_event SET reason='changed'","DELETE FROM assessment_selection_event","INSERT OR REPLACE INTO assessment_selection_event SELECT * FROM assessment_selection_event"]:
     attempts.append(rejected(db,lambda sql=sql:db.execute(sql)))
    attempts.append(rejected(db,lambda:sql_event(db,event(),{'ordinal':7})))
    attempts.append(rejected(db,lambda:x.append(db,dict(event(),ordinal=7))))
    observed=dict(each_variant_rejected=all(r['rejected'] for r,e in attempts),exact_state_equal=before==x.state(db));details['errors']=[e for r,e in attempts]
   elif n==28:
    timeline(db);q=x.selection(db,U('A'),'Y',6);observed=dict(assessment_source=q['assessment']['source_record_id'].removeprefix(U('')),result_source=q['results'][0]['source_record_id'].removeprefix(U('')),decision_source=q['decisions'][0]['source_record_id'].removeprefix(U('')),roles_remain_distinct=len({q['assessment']['source_record_id'],q['results'][0]['source_record_id'],q['decisions'][0]['source_record_id']})==3)
   elif n==29:
    x.append(db,event(target='M-v1',assessment='M'));q=x.selection(db,U('M'),'X',1);observed=dict(result_versions=[r['result_version_id'].removeprefix(U('')) for r in q['results']],values=[r['reported_value'] for r in q['results']],scalar_selected='scalar' in q)
   elif n==30:
    x.append(db,event());x.append(db,event(target='N-v1',assessment='N',ident='other'));observed=x.compare(db,U('R-v1'),U('NR-v1'))
   elif n==31:
    timeline(db);q=x.selection(db,U('A'),'Y',6)['results'][0];observed={k:q[k] for k in ('score_kind','reported_value')}
   elif n==32:
    before=set(db.execute('SELECT graph_id,subject,predicate,object FROM v_assessment_quads'));timeline(db);row=M['bundles']['A-v4'];x.issue(db,row['assessment'],row['results'])
    graphs={name:sorted([list(t) for t in db.execute('SELECT subject,predicate,object FROM v_assessment_quads WHERE graph_id=?',(U(name),))]) for name in M['native_graphs']}
    observed=dict(graphs_equal=graphs==M['native_graphs'] and before<=set(db.execute('SELECT graph_id,subject,predicate,object FROM v_assessment_quads')),new_lifecycle_native_triples=sum('assessment_selection' in str(t) for g in graphs.values() for t in g),historical_union=False);details['actual_graphs']=graphs
   elif n==33:
    family=x.family(db,U('A-v1'));lineage=[list(r) for r in db.execute((x.c.OUT/'queries/descendants.sql').read_text(),dict(root=U('A-v1')))];observed=dict(lineage=[[v.removeprefix(U('')),d] for v,d in lineage],independent_corroboration=family['independent_corroboration'])
   elif n==34:
    db.execute('BEGIN');db.execute('INSERT INTO source_record VALUES(?,?)',(U('caller'),'{}'));before=x.state(db)
    def inner():
     with b.transaction(db):x.append(db,event());x.append(db,event(target='absent',ident='bad'))
    r,err=rejected(db,inner);marker=db.execute('SELECT count(*) FROM source_record WHERE record_id=?',(U('caller'),)).fetchone()[0]==1;db.rollback();observed=dict(caller_marker_retained=marker,no_partial_inner_writes=r['rejected'] and r['all_preoperation_state_preserved'],caller_can_rollback=not db.in_transaction and not db.execute('SELECT 1 FROM source_record WHERE record_id=?',(U('caller'),)).fetchone())
   elif n==35:
    ass=dict(M['bundles']['A-v1']['assessment'],assessment_version_id=U('draft'));a.stage_version(db,U('draft'),U('A'),payload=ass);a.insert_dict(db,'assessment_snapshot',ass)
    targets=[U('draft'),U('B-v1'),db.execute('SELECT version_id FROM evidence_snapshot LIMIT 1').fetchone()[0]];variants=[]
    for target in targets:
     ev=event();ev['target_version']=target;variants.append(rejected(db,lambda ev=ev:sql_event(db,ev)))
    observed=dict(each_variant_rejected=all(r['rejected'] for r,e in variants),exact_state_equal=all(r['all_preoperation_state_preserved'] for r,e in variants));details['errors']=[e for r,e in variants]
   elif n==36:
    results=[]
    for sql in ['DROP TRIGGER assessment_selection_update',"UPDATE schema_migration SET sha256='bad' WHERE version=9",'PRAGMA foreign_keys=OFF']:
     temp=fresh();temp.execute(sql)
     try:x.health(temp);results.append(False)
     except ValueError:results.append(True)
     temp.close()
    observed=dict(each_variant_rejected_by_health=all(results))
   elif n==37:
    try:x.previous.health(db);bad=False
    except ValueError:bad=True
    observed=dict(rejected=bad,original_reader_bytes_unchanged=hashlib.sha256((x.ROOT/'tools/relational_evidence_lifecycle.py').read_bytes()).hexdigest()==hashlib.sha256(__import__('subprocess').check_output(['git','show','753309d6a8e21d585b35a61968beb894027e4ff1:tools/relational_evidence_lifecycle.py'],cwd=x.ROOT)).hexdigest())
   elif n==38:
    timeline(db);before=x.state_sha256(db)
    with tempfile.TemporaryDirectory() as td:
     path=Path(td)/'backup.sqlite';other=b.connect(path);db.backup(other);other.close();other=x.connect(path);observed=dict(exact_logical_state_equal=before==x.state_sha256(other));other.close()
   elif n==39:
    timeline(db);dump='\n'.join(db.iterdump());digest=x.state_sha256(db);rest=b.connect();x.restore_dump(rest,dump,digest);valid=x.state_sha256(rest)==digest;rest.close();out=[]
    for oldval,newval in [(U('A-v2'),U('B-v1')),("'X'","'Z'"),("'WITHDRAW'","'SELECT'")]:
     altered=dump.replace(oldval,newval);assert altered!=dump
     rest=b.connect();result,err=rejected(rest,lambda:x.restore_dump(rest,altered,digest));out.append(result['rejected'] and result['all_preoperation_state_preserved']);rest.close()
    observed=dict(valid_restore_equal=valid,each_tampered_restore_rejected_atomically=all(out))
   elif n==40:
    timeline(db);normal=query(db,at=1)
    latest=db.execute('SELECT assessment_version_id FROM assessment_snapshot WHERE assessment_id=? ORDER BY assessment_version_id DESC LIMIT 1',(U('A'),)).fetchone()[0]
    no_context=db.execute("SELECT target_version FROM assessment_selection_event WHERE assessment_id=? AND kind='SELECT' AND ordinal<=3 ORDER BY ordinal DESC LIMIT 1",(U('A'),)).fetchone()[0]
    no_asof=db.execute("SELECT target_version FROM assessment_selection_event WHERE assessment_id=? AND decision_context_id='X' AND kind='SELECT' ORDER BY ordinal DESC LIMIT 1",(U('A'),)).fetchone()[0]
    mixed=list(db.execute('SELECT result_version_id FROM result_snapshot WHERE result_id=?',(U('R'),)))
    observed=dict(each_mutant_differs_from_its_fixed_oracle=latest!=U('A-v1') and no_context!=U('A-v2') and no_asof!=U('A-v1') and len(mixed)!=1,normal_query_matches=normal==F['cases'][4]['expected']);details['mutant_actual']=[latest,no_context,no_asof,mixed]
   elif n==41:
    before=x.state_sha256(db);mut=fresh();mut.execute('DROP TRIGGER assessment_selection_validate');sql_event(mut,event(target='B-v1'));count=mut.execute('SELECT count(*) FROM assessment_selection_event').fetchone()[0]
    try:x.audit_data(mut);bad=False
    except ValueError:bad=True
    observed=dict(forbidden_write_observed=count==1,audit_rejects=bad,normal_database_untouched=x.state_sha256(db)==before);mut.close()
   elif n==42:
    account=json.loads((x.ROOT/'evaluation/relational/evidence-lifecycle/mapping-accounting.json').read_text());sel=json.loads((x.ROOT/'releases/selection-v0.3.5.json').read_text());ratings=json.loads((x.ROOT/'evaluation/independent-review/responses.json').read_text());x.contract()
    # The immutable original admission packet is protected by selected source hashes.
    count=sum(hashlib.sha256((x.ROOT/p).read_bytes()).hexdigest()==h for p,h in sel['selected_files_sha256'].items())
    observed=dict(native_elements=len(account['rows']),deferred=sum(r['disposition']=='DEFERRED_NO_COMPLETE_SQL_MAPPING' for r in account['rows']),withheld_admissions=json.loads((x.ROOT/'evaluation/consistency/current-0.3.0/report.json').read_text())['summary']['organizational_admissions']['WITHHELD'],independent_ratings=len(ratings['initial_ratings']),published_selected_inputs_unchanged=count)
   elif n==43:
    x.append(db,event(context='Z'));x.append(db,event(kind='WITHDRAW',target='A-v2',context='Z',ident='w'));current=query(db,'Z',2);attempt,error=rejected(db,lambda:x.append(db,event(target='A-v2',context='Z',ident='bad')));observed=dict(current=current,attempt=attempt)
   else:raise AssertionError(n)
   records.append(dict(id=case['id'],requirements=case['requirements'],expected=case['expected'],observed=observed,status='PASS' if observed==case['expected'] else 'FAIL',evidence=details))
  except Exception as exc:
   records.append(dict(id=case['id'],expected=case['expected'],observed=None,status='ERROR',error=repr(exc)))
  finally:db.close()
 report=dict(schema='riskium-assessment-selection-execution-v1',declaration_commit='071b948dd46881f7456f0b501a55eafd963d2cce',input_commit='753309d6a8e21d585b35a61968beb894027e4ff1',runtime=dict(python=sys.version,sqlite=sqlite3.sqlite_version),summary={s:sum(r['status']==s for r in records) for s in ('PASS','FAIL','ERROR')},controls=records,independent_semantic_validation=False,reader_criteria='NOT_REVIEWED_ON_LIVE_CHANNELS',source_sha256={str(p.relative_to(x.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*x.OUT.rglob('*'),Path(__file__),x.ROOT/'tools/relational_assessment_selection.py'] if p.is_file() and p.name!='component.json'})
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(OUT/'report.json'));args=parser.parse_args();report=execute();target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['summary']))
 for row in report['controls']:
  if row['status']!='PASS':print(row['id'],json.dumps(row.get('observed')),row.get('error'), 'expected',json.dumps(row['expected']))
 sys.exit(0 if report['summary']['PASS']==44 else 1)
