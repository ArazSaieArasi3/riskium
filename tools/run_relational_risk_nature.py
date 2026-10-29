"""Execute fixed risk-nature controls; observations never replace declarations."""
import argparse
import copy
import hashlib
import json
import platform
import re
import sqlite3
import statistics
import subprocess
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

from rdflib import Dataset,Graph,URIRef,RDF
import relational_risk_nature as x
import run_assessment_selection as old

U=lambda s:'urn:riskium:nature37:'+s
I=json.loads((x.OUT/'execution-fixture.json').read_text())
F=json.loads((x.OUT/'fixtures.json').read_text())
O=json.loads((x.OUT/'query-oracles.json').read_text())
NEG=json.loads((x.OUT/'negative-inputs.json').read_text())
EXPECTED=Dataset();EXPECTED.parse(x.OUT/'native-oracles.trig',format='trig')
TEMPLATE=None
PRIOR=None


def prior():
    global PRIOR
    if PRIOR is None:PRIOR=old.fresh();old.timeline(PRIOR)
    db=x.b.connect();PRIOR.backup(db);return db


def seed(db):
    for s in I['sources']:db.execute('INSERT INTO source_record VALUES(?,?)',(s['record_id'],s['original_json']))
    for r in I['raw_records']:db.execute('INSERT INTO source_record VALUES(?,?)',(r['record_id'],r['original_json']))
    for c in I['cases']:
        x.b.add_identity(db,c['case_id'],'case');db.execute('INSERT INTO risk_case(case_id,label,source_record_id) VALUES(?,?,?)',(c['case_id'],c['label'],c['source_record_id']))
    r=I['register'];x.a.add_artifact(db,r['artifact_id'],'RKM-C030',r['label'],r['source_record_id'])
    for e in I['entries']:
        x.a.add_artifact(db,e['entry_id'],'RKM-C022',e['label'],e['source_record_id'])
        db.execute('INSERT INTO register_entry(entry_id,case_id,register_id) VALUES(?,?,?)',(e['entry_id'],e['case_id'],e['register_id']))
    for r in I['support_versions']:x.issue_support(db,r)
    for r in I['context_versions']:x.issue_context(db,r)
    for r in I['assertions']:
        x.issue_bundle(db,dict(assertion=r,recording_revisions=[e for e in I['recording_revisions'] if r['version_id'] in e['nature_version_ids']],correction=None))


def fresh(corrections=True):
    global TEMPLATE
    if TEMPLATE is None:
        TEMPLATE=prior();x.migrate(TEMPLATE);seed(TEMPLATE)
    db=x.b.connect();TEMPLATE.backup(db)
    if corrections:
        for c in I['corrections']:x.declare_correction(db,c)
    return db


def later(db):x.issue_bundle(db,copy.deepcopy(I['later_unlinked_bundle']))
def graph_rows(g):return sorted([[str(s),str(p),str(o)] for s,p,o in g])
def rejection(db,action):
    before=x.state(db)
    try:action();error='ACCEPTED'
    except (ValueError,sqlite3.DatabaseError,TypeError) as exc:error=str(exc)
    match=re.search(r'NRA-[A-Z_]+',error)
    return dict(rejected=error!='ACCEPTED',diagnostic_family=match.group() if match else error,
                all_preoperation_state_preserved=x.state(db)==before),error


def resolve_path(obj,path):
    for key in re.findall(r'[^.\[\]]+',path):obj=obj[int(key) if key.isdigit() else key]
    return copy.deepcopy(obj)


def changes(obj,values):
    for path,value in values.items():
        parts=re.findall(r'[^.\[\]]+',path);target=obj
        for key in parts[:-1]:target=target[int(key) if key.isdigit() else key]
        key=parts[-1];target[int(key) if key.isdigit() else key]=copy.deepcopy(value)
    return obj


def negative(row):
    no_corrections=any(p['operation']=='load_initial_without_corrections' for p in row['preparation'])
    db=fresh(not no_corrections)
    try:
        for prep in row['preparation']:
            if not prep.get('base'):continue
            obj=changes(resolve_path(I,prep['base']),prep.get('set',{}))
            {'stage_support_without_sealing':x.stage_support,'stage_context_without_sealing':x.stage_context,
             'stage_bundle_without_sealing':x.stage_bundle}[prep['operation']](db,obj)
        obj=changes(resolve_path(I,row['base']),row['set']) if row['base'] else row['set']
        funcs={'issue_bundle':x.issue_bundle,'issue_support':x.issue_support,'issue_context':x.issue_context,'declare_correction':x.declare_correction}
        if row['operation'] in funcs:action=lambda:funcs[row['operation']](db,obj)
        else:action=lambda:getattr(x,row['operation'])(db,obj.get('version_id',obj.get('case_id')))
        observed,error=rejection(db,action)
        return dict(id=row['id'],control=row['control'],expected=row['expected'],observed=observed,error=error,
                    status='PASS' if observed==row['expected'] else 'FAIL')
    finally:db.close()


def expected(value):
    if isinstance(value,str) and value.startswith('query-oracles.json#/'):
        result=O
        for key in value.split('#/')[1].split('/'):result=result[key]
        return result
    if isinstance(value,str) and value.startswith('native-oracles.trig#'):
        return graph_rows(EXPECTED.graph(URIRef(value.split('#',1)[1])))
    if isinstance(value,list):return [expected(v) for v in value]
    if isinstance(value,dict):return {(k[:-4] if k.endswith('_ref') else k):expected(v) for k,v in value.items()}
    return value


def raw_mutations(db,queries):
    outputs=[]
    for query in queries:
        result,error=rejection(db,lambda q=query:db.execute(q));outputs.append(dict(sql=query,result=result,error=error))
    return outputs


def all_rejected(items):return all(r['result']['rejected'] and r['result']['all_preoperation_state_preserved'] for r in items)
def native_match(db,versions):return all(set(x.native_graph(db,v))==set(EXPECTED.graph(URIRef(v))) for v in versions)
def pins(db,version):
    r=x.get(db,U(version))['row'];return [r['context_version_id'],*r['objective_version_ids'],r['term_version_id'],r['scheme_version_id']]


def execute_control(number,negatives,hosted=None):
    db=prior() if number in (1,3) else fresh();details={}
    try:
        subset=[r for r in negatives if r['control']=='NRA-F%02d'%number]
        if number in (7,8,14,15,19,22,29,30,31,32,33):
            details['variants']=subset
            if not subset:raise ValueError('Missing concrete variants')
            o=subset[0]['observed'];assert all(r['status']=='PASS' for r in subset)
        elif number==1:
            before=x.state(db);views={v:list(db.execute('SELECT * FROM '+v)) for v in ('v_native_facts','v_assessment_quads','v_evidence_quads','v_knowledge_quads')}
            x.migrate(db);after=x.state(db)
            o=dict(schema_version=db.execute('PRAGMA user_version').fetchone()[0],old_rows_payloads_ledgers_and_named_graphs_equal=all(rows==[r for r in after['rows'][t] if t!='schema_migration' or r[0]<10] for t,rows in before['rows'].items()) and all(rows==list(db.execute('SELECT * FROM '+v)) for v,rows in views.items()),old_schema_objects_unchanged=all(r in after['schema'] for r in before['schema']),invented_native_or_backfilled_rows=sum(len(r) for t,r in after['rows'].items() if t.startswith('nature_')))
        elif number==2:
            before=x.state(db);out=x.migrate(db);o=dict(outcome=out,exact_state_equal=before==x.state(db))
        elif number==3:
            before=x.state(db);sql=x.migration_text()
            with patch.object(x,'migration_text',return_value=sql+'\nINSERT INTO absent_nature_table VALUES(1);\n'):r,err=rejection(db,lambda:x.migrate(db))
            details['error']=err;o=dict(rejected=r['rejected'],exact_state_equal=before==x.state(db),schema_version=db.execute('PRAGMA user_version').fetchone()[0])
        elif number==4:
            trials=[]
            for ident in (U('case-1'),U('A'),U('A-v1')):
                r,e=rejection(db,lambda ident=ident:x.identity(db,dict(I['later_unlinked_bundle']['assertion'],artifact_id=ident),'RKM-X02'));trials.append((r,e))
            details['variants']=trials+subset
            o=dict(rejected=all(r['rejected'] for r,e in trials),diagnostic_family='NRA-IDENTITY' if all(r['diagnostic_family']=='NRA-IDENTITY' for r,e in trials) else 'WRONG_DIAGNOSTIC',all_preoperation_state_preserved=all(r['all_preoperation_state_preserved'] for r,e in trials))
        elif number==5:
            ids=[r['version_id'] for r in x.by_case(db,U('case-2'))['rows']];o=dict(version_ids=ids,other_equal_label_case_included=U('A-v1') in ids)
        elif number==6:
            r=[x.get(db,U(v))['row'] for v in ('A-v1','B-v1')];meta=[db.execute('SELECT code,label FROM nature_membership JOIN information_artifact USING(artifact_id) WHERE artifact_id=?',(v['term_id'],)).fetchone() for v in r]
            o=dict(terms=[v['term_id'] for v in r],schemes=[v['scheme_id'] for v in r],code=meta[0][0] if meta[0][0]==meta[1][0] else None,label=meta[0][1] if meta[0][1]==meta[1][1] else None,merged=r[0]['term_id']==r[1]['term_id'])
        elif number==9:
            queries=['INSERT OR '+op+' INTO '+t+' SELECT * FROM '+t+' LIMIT 1' for t in ('nature_membership','nature_support','nature_snapshot','nature_entry_link','nature_correction') for op in ('IGNORE','REPLACE')]
            details['sql']=raw_mutations(db,queries);r,e=rejection(db,lambda:x.issue_bundle(db,dict(assertion=I['assertions'][0],recording_revisions=I['recording_revisions'][:2],correction=None)))
            o=dict(each_variant_rejected=all_rejected(details['sql']) and r['rejected'],exact_state_equal=all_rejected(details['sql']) and r['all_preoperation_state_preserved'])
        elif number in (10,11,12,25,26):
            name={10:'A-v1',11:'A-v2',12:'A-v3',25:'U-v1',26:'Z-v1'}[number];o=dict(exact_row=x.get(db,U(name))['row'])
        elif number==13:
            later(db);family=x.family(db,U('A-v1'))['lineage'];o=dict(family=family,get=x.get(db,U('A-v1'))['row'],A_v4_in_family=any(r[0]==U('A-v4') for r in family))
        elif number==16:
            later(db);r=[x.get(db,U(v))['row'] for v in ('A-v2','A-v4')];o=dict(A_v2=[r[0]['term_version_id'],r[0]['scheme_version_id']],A_v4=[r[1]['term_version_id'],r[1]['scheme_version_id']],earlier_row=r[0])
        elif number in (17,20,21):
            tables=('nature_objective',) if number==17 else ('source_record',) if number==21 else ('nature_support','nature_context','nature_snapshot','nature_entry','nature_entry_link','nature_correction','nature_objective','version_snapshot','source_record')
            queries=[]
            for t in tables:
                col=db.execute('PRAGMA table_info('+t+')').fetchone()[1]
                queries+=['UPDATE '+t+' SET '+col+'='+col,'DELETE FROM '+t,'INSERT OR REPLACE INTO '+t+' SELECT * FROM '+t+' LIMIT 1','INSERT OR IGNORE INTO '+t+' SELECT * FROM '+t+' LIMIT 1']
            if number==17:queries.append("UPDATE version_snapshot SET payload_json='{}' WHERE version_id='"+U('context-v1')+"'")
            details['sql']=raw_mutations(db,queries);o=dict(each_variant_rejected=all_rejected(details['sql']),exact_state_equal=all_rejected(details['sql']))
        elif number==18:
            s=x.get(db,U('A-v2'))['sources'];original={r['record_id']:r['original_json'] for r in I['sources']}
            o={role+'_source':s[role][0]['record_id'] for role in ('assertion','term','context','objective','correction')}
            o['exact_original_json_equal']=all(r['original_json']==original[r['record_id']] for v in s.values() for r in v)
        elif number in (23,24):
            details['variants']=subset;r=subset[0]['observed'];raw=db.execute('SELECT original_json FROM source_record WHERE record_id=?',(U('raw-incomplete'),)).fetchone()
            o=dict(rejected=r['rejected'],diagnostic_family=r['diagnostic_family'],raw_source_retained=raw is not None,partial_managed_rows=0 if r['all_preoperation_state_preserved'] else -1)
            o['fabricated_cases' if number==23 else 'synthesized_terms']=0 if r['all_preoperation_state_preserved'] else -1
        elif number==27:
            rs=[x.get(db,U(v))['row'] for v in ('U-v1','Z-v1')]
            o=dict(raw_text=json.loads(db.execute('SELECT original_json FROM source_record WHERE record_id=?',(U('raw-incomplete'),)).fetchone()[0])['text'],native_unknown_terms=db.execute("SELECT count(*) FROM nature_membership WHERE code='UNKNOWN'").fetchone()[0],fabricated_objectives=sum(len(r['objective_version_ids']) for r in rs),numeric_defaults=sum(isinstance(r['context_version_id'],(int,float)) for r in rs),ready_rows=[r['readiness']=='READY_FOR_DECLARED_RETRIEVAL' for r in rs])
        elif number in (28,36):
            r=x.family(db,U('A-v1' if number==28 else 'A-v2'));o=dict(exact_rows=r['lineage'])
            if number==28:o['independent_corroboration']=r['independent_corroboration']
        elif number==34:
            later(db);graphs=[x.native_graph(db,U(v)) for v in ('A-v1','A-v2','A-v3','A-v4','B-v1','C-v1','U-v1','Z-v1')];env=x.family(db,U('A-v1'))
            o=dict(native_correction_triples=sum('correction' in str(p).lower() for g in graphs for s,p,t in g),automatic_selection='selected_version' in env,independent_corroboration=env['independent_corroboration'],factual_correctness=env['factual_correctness'])
        elif number==35:
            r=subset[0]['observed'];details['variants']=subset;o=dict(rejected=r['rejected'],all_preoperation_state_preserved=r['all_preoperation_state_preserved'],partial_identities_versions_entry_links_or_edges=0 if r['all_preoperation_state_preserved'] else -1)
        elif number==37:
            g=x.native_graph(db,U('A-v1'));ds=Dataset();ds.graph(URIRef(U('A-v1'))).__iadd__(g)
            rr=[[str(v) if v is not None else None for v in row] for row in ds.query((x.OUT/'native-query.rq').read_text(),initBindings={'graph':URIRef(U('A-v1'))})]
            o=dict(graph=graph_rows(g),rdf_rows=rr,exact_triples_equal=set(g)==set(EXPECTED.graph(URIRef(U('A-v1')))))
        elif number in (38,39):
            ids=[U(v) for v in (('A-v2','A-v3') if number==38 else ('B-v1','C-v1','U-v1','Z-v1'))]
            o=dict(graph_ids=ids,exact_triples_equal=native_match(db,ids),expected_dataset='native-oracles.trig')
        elif number==40:
            later(db);ds=Dataset();actual={};normalized={}
            for v in O['get']:
                ds.graph(URIRef(v)).__iadd__(x.native_graph(db,v))
                actual[v]=[[str(i) if i is not None else None for i in row] for row in ds.query((x.OUT/'native-query.rq').read_text(),initBindings={'graph':URIRef(v)})]
                r=x.get(db,v)['row'];normalized[v]=[]
                for entry in r['recording_entry_version_ids']:
                    for obj in r['objective_version_ids'] or [None]:
                        aid=db.execute('SELECT artifact_id FROM nature_support WHERE version_id=?',(obj,)).fetchone() if obj else None
                        normalized[v].append([v,r['artifact_id'],r['case_id'],r['term_id'],r['term_version_id'],r['scheme_id'],r['scheme_version_id'],r['context_id'],r['context_version_id'],aid[0] if aid else None,obj,entry])
            o=dict(expected_rows=actual,graphs=len(actual),historical_union=False,comparison_passes=actual==normalized);details['SQL_normalized_rows']=normalized
        elif number==41:
            later(db);graphs=[x.native_graph(db,v) for v in O['get']];preds={str(p) for g in graphs for s,p,t in g};native=json.loads((x.ROOT/'ontology/riskium-model.json').read_text());known={x.RISK+a['id'] for a in native['associations']}
            o=dict(new_native_ids=len(preds-known-{str(RDF.type)}),C005_typed_versions=sum((URIRef(v),RDF.type,URIRef(x.RISK+'RKM-C005')) in g for v in O['get'] for g in graphs),direct_assertion_objective_or_usesContextVersion=sum(str(p).endswith('RX-014') or (str(s) in {r['artifact_id'] for r in O['get'].values()} and str(p).endswith('RK2-011')) for g in graphs for s,p,t in g),occurrences=sum(str(t)==x.RISK+'RKM-C004' for g in graphs for s,p,t in g),owl_sameAs=sum(str(p).endswith('sameAs') for g in graphs for s,p,t in g),source_records_as_RiskSource=sum(str(s).startswith(U('source-')) and str(t)==x.RISK+'RKM-C007' for g in graphs for s,p,t in g))
        elif number==42:
            views=('v_assessment_quads','v_evidence_quads','v_knowledge_quads');before={v:list(db.execute('SELECT * FROM '+v)) for v in views};base=set(db.execute('SELECT * FROM v_native_facts'));gs={v:set(x.native_graph(db,v)) for v in O['get'] if v!=U('A-v4')};later(db)
            o=dict(old_named_graphs_equal=all(before[v]==list(db.execute('SELECT * FROM '+v)) for v in views),prior_nature_graphs_equal=all(g==set(x.native_graph(db,v)) for v,g in gs.items()),earlier_base_native_facts_retained=base<=set(db.execute('SELECT * FROM v_native_facts')),new_graph=graph_rows(x.native_graph(db,U('A-v4'))))
        elif number==43:
            details['variants']=subset;queries=["INSERT INTO nature_entry_link VALUES('"+U('entry-1-r1')+"','"+U('A-v2')+"')"]
            details['sql']=raw_mutations(db,queries);o=dict(each_variant_rejected=all(r['status']=='PASS' for r in subset) and all_rejected(details['sql']),exact_state_equal=all(r['observed']['all_preoperation_state_preserved'] for r in subset) and all_rejected(details['sql']))
        elif number==44:
            r,e=rejection(db,lambda:x.previous.health(db));details['error']=e
            trusted=subprocess.check_output(['git','show','805b1edecff254f1e21131aa6fd098344affb398:tools/relational_assessment_selection.py'],cwd=x.ROOT)
            o=dict(rejected=r['rejected'],reader_source_unchanged=trusted==(x.ROOT/'tools/relational_assessment_selection.py').read_bytes(),schema_version=db.execute('PRAGMA user_version').fetchone()[0])
        elif number==45:
            mutations=['DROP TRIGGER nature_snapshot_update',"UPDATE schema_migration SET sha256='bad' WHERE version=10",'PRAGMA foreign_keys=OFF','PRAGMA recursive_triggers=OFF','PRAGMA user_version=11',"DROP TRIGGER a_result_snapshot_update; UPDATE result_snapshot SET reported_value='tampered' WHERE result_version_id=(SELECT result_version_id FROM result_snapshot LIMIT 1)"]
            outcomes=[]
            for sql in mutations:
                q=fresh()
                original=q.execute("SELECT sql FROM sqlite_master WHERE name='a_result_snapshot_update'").fetchone()[0] if sql.startswith('DROP TRIGGER a_result_snapshot_update') else None
                q.executescript(sql)
                if original:q.execute(original)
                r,e=rejection(q,lambda:x.health(q));outcomes.append((r,e));q.close()
            details['variants']=outcomes;o=dict(each_variant_rejected=all(r['rejected'] for r,e in outcomes),honest_schema_state_preserved=x.health(db) is None)
        elif number==46:
            query="UPDATE nature_snapshot SET context_version_id='"+U('context-v2')+"' WHERE version_id='"+U('A-v1')+"'"
            r,e=rejection(db,lambda:db.execute(query));q=fresh();q.execute('DROP TRIGGER nature_snapshot_update');q.execute(query)
            observed=q.execute('SELECT context_version_id FROM nature_snapshot WHERE version_id=?',(U('A-v1'),)).fetchone()[0]==U('context-v2');rr,ee=rejection(q,lambda:x.audit_data(q));details['errors']=[e,ee];q.close()
            o=dict(normal_write_rejected=r['rejected'],mutant_forbidden_write_observed=observed,semantic_audit_rejects_mutant=rr['rejected'],normal_state_unchanged=r['all_preoperation_state_preserved'])
        elif number==47:
            db.execute('BEGIN');db.execute('INSERT INTO source_record VALUES(?,?)',(U('caller'),'{}'))
            def inner():
                with x.b.transaction(db):later(db);bad=copy.deepcopy(I['later_unlinked_bundle']);bad['assertion']['case_id']=None;x.issue_bundle(db,bad)
            r,e=rejection(db,inner);marker=db.execute('SELECT 1 FROM source_record WHERE record_id=?',(U('caller'),)).fetchone() is not None;db.rollback()
            o=dict(caller_marker_retained_after_inner_failure=marker,no_partial_inner_writes=r['all_preoperation_state_preserved'] and r['rejected'],caller_can_rollback=not db.in_transaction and not db.execute('SELECT 1 FROM source_record WHERE record_id=?',(U('caller'),)).fetchone())
        elif number==48:
            later(db);digest=x.state_sha256(db)
            with tempfile.TemporaryDirectory() as td:
                path=Path(td)/'backup.sqlite';q=x.b.connect(path);db.backup(q);q.close();db.close();db=None;q=x.connect(path)
                o=dict(exact_logical_state_equal=x.state_sha256(q)==digest,all_literal_query_and_graph_answers_equal=all(x.get(q,v)['row']==r for v,r in O['get'].items()) and native_match(q,O['get']));q.close()
        elif number==49:
            later(db);dump='\n'.join(db.iterdump());digest=x.state_sha256(db);q=x.b.connect();x.restore_dump(q,dump,digest)
            valid=x.state_sha256(q)==digest;answers=all(x.get(q,v)['row']==r for v,r in O['get'].items()) and native_match(q,O['get']);q.close();outs=[]
            for a,b in [('Reported unfavorable effect.','Edited report.'),(U('context-v1'),U('context-v2')),("'"+U('A-v1')+"', 'synthetic-curator'","'"+U('B-v1')+"', 'synthetic-curator'")]:
                changed=dump.replace(a,b)
                if changed==dump:
                    # SQL's dump spacing is not part of a lexical claim.
                    changed=dump.replace("'"+U('A-v2')+"','"+U('A-v1')+"'","'"+U('A-v2')+"','"+U('B-v1')+"'")
                assert changed!=dump
                q=x.b.connect();r,e=rejection(q,lambda:x.restore_dump(q,changed,digest));outs.append((r,e));q.close()
            q=x.b.connect();r,e=rejection(q,lambda:x.restore_dump(q,"ATTACH DATABASE ':memory:' AS other;\n",digest));q.close();details['restore_attempts']=outs
            o=dict(valid_restore_equal=valid,each_tampered_restore_rejected_atomically=all(r['rejected'] and r['all_preoperation_state_preserved'] for r,e in outs),external_database_statements_rejected=r['rejected'],exact_literal_answers_equal=answers)
        elif number==50:o,details=concurrency(db)
        elif number==51:o,details=workload()
        elif number==52:
            out={}
            for key,fn,arg in [('unknown_version',x.get,U('absent')),('unknown_family',x.family,U('absent')),('unknown_case',x.by_case,U('case-absent'))]:out[key]=rejection(db,lambda fn=fn,arg=arg:fn(db,arg))[0]['diagnostic_family']
            out['known_empty']=x.by_case(db,U('case-empty'))['rows'];o=out
        elif number==53:
            outs=[rejection(db,lambda fn=fn:fn(db,"'; DROP TABLE nature_snapshot;--"))[0] for fn in (x.get,x.by_case)];o=dict(rejected_as_unknown=all(r['diagnostic_family'] in ('NRA-UNKNOWN_VERSION','NRA-UNKNOWN_CASE') for r in outs),SQL_executed_from_input=not all(r['all_preoperation_state_preserved'] for r in outs),exact_state_equal=all(r['all_preoperation_state_preserved'] for r in outs))
        elif number==54:
            later(db);r,e=rejection(db,lambda:x.get(db));rr,ee=rejection(db,lambda:x.get(db,U('A')));o=dict(missing_argument_rejected=r['rejected'],artifact_as_version=rr['diagnostic_family'],automatic_latest_selected=not rr['rejected'])
        elif number==55:
            answer=x.by_case(db,U('case-1'));o=dict(exact_version_ids=[r['version_id'] for r in answer['rows']],rows_use_literal_get_oracles=all(r==O['get'][r['version_id']] for r in answer['rows']),envelope={k:answer[k] for k in x.ENVELOPE})
        elif number==56:
            later(db);r1=x.get(db,U('A-v1'))['row'];r2=x.get(db,U('A-v2'))['row']
            latestctx=db.execute('SELECT version_id FROM nature_context WHERE artifact_id=? ORDER BY version_id DESC LIMIT 1',(r1['context_id'],)).fetchone()[0]
            latestobj=db.execute('SELECT version_id FROM nature_support WHERE artifact_id=? ORDER BY version_id DESC LIMIT 1',(U('objective'),)).fetchone()[0]
            latestterm=db.execute('SELECT version_id FROM nature_support WHERE artifact_id=? ORDER BY version_id DESC LIMIT 1',(r2['term_id'],)).fetchone()[0]
            latestscheme=db.execute('SELECT version_id FROM nature_support WHERE artifact_id=? ORDER BY version_id DESC LIMIT 1',(r2['scheme_id'],)).fetchone()[0]
            o=dict(each_mutant_differs_from_fixed_oracle=latestctx!=r1['context_version_id'] and latestobj not in r1['objective_version_ids'] and latestterm!=r2['term_version_id'] and latestscheme!=r2['scheme_version_id'],A_v1_expected_pins=pins(db,'A-v1'),A_v2_expected_term_scheme=[r2['term_version_id'],r2['scheme_version_id']]);details['mutants']=[latestctx,latestobj,latestterm,latestscheme]
        elif number==57:
            later(db);correct=[r[0] for r in x.family(db,U('A-v1'))['lineage']];case2=[r['version_id'] for r in x.by_case(db,U('case-2'))['rows']]
            allversions=[r[0] for r in db.execute('SELECT version_id FROM nature_snapshot ORDER BY version_id')];allA=[r[0] for r in db.execute('SELECT version_id FROM nature_snapshot WHERE artifact_id=? ORDER BY version_id',(U('A'),))]
            inferred=[r[0] for r in db.execute('SELECT l.nature_version_id FROM nature_entry e JOIN nature_entry_link l ON l.entry_version_id=e.version_id WHERE e.previous_version_id IS NOT NULL ORDER BY l.nature_version_id')]
            o=dict(each_mutant_differs_from_fixed_oracle=case2!=allversions and correct!=allA and sorted(inferred)!=correct,correct_case2_ids=case2,correct_A_root_family_ids=correct);details['mutants']=[allversions,allA,inferred]
        elif number==58:
            gs=[x.native_graph(db,U(v)) for v in ('A-v1','A-v2','A-v3')];union=Graph()
            for g in gs:union+=g
            pred=URIRef(x.RISK+'R-42');subject=URIRef(U('A'))
            o=dict(correct_graph_term_counts=[len(list(g.objects(subject,pred))) for g in gs],union_distinct_terms=len(list(union.objects(subject,pred))),union_matches_single_version_oracle=set(union)==set(EXPECTED.graph(URIRef(U('A-v1')))))
        elif number==59:
            import check_risk_nature_declaration as check
            result=check.check();account=json.loads((x.ROOT/'evaluation/relational/evidence-lifecycle/mapping-accounting.json').read_text());native=json.loads((x.ROOT/'ontology/riskium-model.json').read_text())
            o=dict(native_elements=len(account['rows']),historical_deferred=sum(r['disposition']=='DEFERRED_NO_COMPLETE_SQL_MAPPING' for r in account['rows']),withheld_admissions=json.loads((x.ROOT/'evaluation/consistency/current-0.3.0/report.json').read_text())['summary']['organizational_admissions']['WITHHELD'],independent_ratings=len(json.loads((x.ROOT/'evaluation/independent-review/responses.json').read_text())['initial_ratings']),preserved_v036_inputs_except_live_README=result['protected_v036_files_except_live_README'],preserved_v035_selected_inputs=result['protected_v035_files'],native_model_changed=x.sha((x.ROOT/'ontology/riskium-model.json').read_bytes())!=json.loads((x.OUT/'contract.json').read_text())['source_sha256']['ontology/riskium-model.json'])
        elif number==60:
            if hosted is None:return None,dict(phase='AWAITING_INDEPENDENT_HOSTED_ARTIFACT_DOWNLOAD',no_runtime_pass_in_declaration=all(r['status']=='NOT_RUN' and r['observed'] is None for r in F['cases']))
            o=hosted
        else:raise ValueError('Unimplemented control '+str(number))
        return o,details
    finally:
        if db is not None:db.close()


def concurrency(db):
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'shared.sqlite';q=x.b.connect(p);db.backup(q);q.close();writer=x.connect(p);reader=x.connect(p)
        try:
            for c in (writer,reader):c.execute('PRAGMA busy_timeout=0')
            writer.execute('BEGIN IMMEDIATE');later(writer)
            visible=reader.execute('SELECT count(*) FROM nature_snapshot WHERE version_id=?',(U('A-v4'),)).fetchone()[0]
            half=reader.execute('SELECT count(*) FROM nature_entry WHERE version_id=?',(U('entry-1-r4'),)).fetchone()[0]
            try:reader.execute('BEGIN IMMEDIATE');conflict=False
            except sqlite3.OperationalError:conflict=True
            writer.commit();reader.execute('BEGIN IMMEDIATE');reader.commit()
            answer=x.get(reader,U('A-v4'))['row']
            return dict(uncommitted_rows_visible=visible>0,half_bundle_visible=half>0,writer_conflict_observed=conflict,explicit_retry_succeeds_once=reader.execute('SELECT count(*) FROM nature_snapshot WHERE version_id=?',(U('A-v4'),)).fetchone()[0]==1,postcommit_literal_answer_equal=answer==O['get'][U('A-v4')]),dict(journal_mode=writer.execute('PRAGMA journal_mode').fetchone()[0],busy_timeout_ms=0)
        finally:writer.close();reader.close()


def workload():
    observations={};details={}
    for seed,count in ((17,200),(29,400)):
        db=fresh();bundles=[]
        try:
            for idx in range(4):
                case=U(f'bench-{seed}-case-{idx}');entry=U(f'bench-{seed}-entry-{idx}');x.b.add_identity(db,case,'case');db.execute('INSERT INTO risk_case(case_id,label,source_record_id) VALUES(?,?,?)',(case,'Synthetic workload',U('source-catalog')));x.a.add_artifact(db,entry,'RKM-C022','Workload entry',U('source-catalog'));db.execute('INSERT INTO register_entry(entry_id,case_id,register_id) VALUES(?,?,?)',(entry,case,U('register')))
            with x.b.transaction(db):
                for idx in range(count):
                    name=f'bench-{seed}-{idx:04d}';version=U(name+'-v1');r=dict(I['assertions'][0],artifact_id=U(name),version_id=version,case_id=U(f'bench-{seed}-case-{idx%4}'))
                    e=dict(I['recording_revisions'][0],version_id=U(name+'-entry-v1'),entry_id=U(f'bench-{seed}-entry-{idx%4}'),nature_version_ids=[version]);bundle=dict(assertion=r,recording_revisions=[e],correction=None);bundles.append(bundle);x.stage_bundle(db,bundle);x.a.seal(db,e['version_id'],e['recorded_at']);x.a.seal(db,version,r['recorded_at'])
                x.health(db)
            counts=[len(x.by_case(db,U(f'bench-{seed}-case-{idx}'))['rows']) for idx in range(4)];observations[seed]=counts
            queries={'by_case':((x.OUT/'queries/by_case.sql').read_text(),{'case':U(f'bench-{seed}-case-0')}),'exact_version':((x.OUT/'queries/exact_version.sql').read_text(),{'version':U(f'bench-{seed}-0000-v1')}),'family':((x.OUT/'queries/family.sql').read_text(),{'root':U(f'bench-{seed}-0000-v1')})}
            measured={}
            for name,(sql,args) in queries.items():
                for _ in range(5):db.execute(sql,args).fetchall()
                times=[]
                for _ in range(31):
                    start=time.perf_counter_ns();actual=db.execute(sql,args).fetchall();times.append((time.perf_counter_ns()-start)/1e6)
                measured[name]=dict(rows=len(actual),median_ms=statistics.median(times),p95_ms=sorted(times)[29],query_plan=[list(r) for r in db.execute('EXPLAIN QUERY PLAN '+sql,args)])
            details[str(seed)]=dict(reports=count,construction_sha256=x.sha(x.encode(bundles).encode()),warmups=5,repetitions=31,measurements=measured)
        finally:db.close()
    return dict(case_row_counts_seed17=observations[17],case_row_counts_seed29=observations[29],duplicates_or_cross_case_leaks=sum(abs(v-count//4) for seed,count in ((17,200),(29,400)) for v in observations[seed]),query_and_index_rationale_recorded=all(details[str(s)]['measurements'][q]['query_plan'] for s in (17,29) for q in ('by_case','exact_version','family')),production_SLO_claimed=False),details


def execute(hosted=None):
    negatives=[negative(r) for r in NEG['variants']]
    records=[]
    for case in F['cases']:
        number=int(case['id'][-2:])
        try:
            observed,details=execute_control(number,negatives,hosted)
            status='PENDING_EXTERNAL_READBACK' if observed is None and number==60 else 'PASS' if observed==expected(case['expected']) else 'FAIL'
            records.append(dict(id=case['id'],requirements=case['requirements'],expected=expected(case['expected']),observed=observed,details=details,status=status))
        except Exception as exc:
            records.append(dict(id=case['id'],requirements=case['requirements'],observed=None,status='ERROR',error=repr(exc)))
        print(case['id'],records[-1]['status'],flush=True)
    component=json.loads((x.OUT/'component.json').read_text())
    source_paths=list(component['files_sha256'])+['implementation/relational/0.9.0/component.json']
    return dict(schema='riskium-risk-nature-execution-v1',declaration_commit='805b1edecff254f1e21131aa6fd098344affb398',source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=x.ROOT,text=True).strip(),working_tree_clean=not subprocess.check_output(['git','status','--porcelain'],cwd=x.ROOT).strip(),runtime_source_sha256={p:x.sha((x.ROOT/p).read_bytes()) for p in source_paths},runtime=dict(python=platform.python_version(),sqlite=sqlite3.sqlite_version,foreign_keys=True,recursive_triggers=True),input_sha256={p.name:x.sha(p.read_bytes()) for p in x.OUT.iterdir() if p.is_file()},negative_variants=negatives,controls=records,summary={s:sum(r['status']==s for r in records) for s in ('PASS','FAIL','ERROR','PENDING_EXTERNAL_READBACK')},native_semantic_acceptance=False,independent_ratings=0)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();report=execute();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['summary']))
    if report['summary']['FAIL'] or report['summary']['ERROR'] or any(r['status']!='PASS' for r in report['negative_variants']):raise SystemExit(1)
