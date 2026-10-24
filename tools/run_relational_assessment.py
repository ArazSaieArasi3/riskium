"""Execute fixed and seeded SQLite assessment assurance; never certify production."""
import argparse
from collections import Counter
from datetime import datetime,timezone
import gzip
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import sqlite3
import statistics
import subprocess
import sys
import tempfile
import time

from rdflib import Dataset,Graph,Literal,RDF,RDFS,URIRef
from rdflib.compare import isomorphic
import relational_assessment as a
import relational_history as b
from build_relational_assessment import ROOT,OUT as PROFILE,RISK,RDF_TYPE,SP,render as build,sha,load_policy
from audit_relational_design import inspect as design_audit,render as render_design

OUT=ROOT/'evaluation/relational/assessment'
FIXTURE=PROFILE/'fixtures.json'
INPUTS=['requirements/relational-requirements.json','implementation/relational/0.2.0/policy.json',
 'implementation/relational/0.2.0/fixtures.json','implementation/relational/0.2.0/003_assessment_tables.sql',
 'implementation/relational/0.2.0/003_assessment_guards.sql','implementation/relational/0.2.0/mapping.json',
 'implementation/relational/0.2.0/mapping.ttl','tools/build_relational_assessment.py','tools/relational_assessment.py',
 'tools/run_relational_assessment.py','tools/audit_relational_design.py','ontology/shacl/0.7.0/comparison.ttl',
 'ontology/shacl/0.7.0/receipt.json','tools/build_comparison_shapes.py','tools/run_comparison_shacl.py',
 'tools/requirements-shacl.txt']


def state(c):
    obj=dict(rows=a.snapshot(c),schema=b.schema_snapshot(c),ledger=list(c.execute('SELECT * FROM schema_migration ORDER BY version')),user_version=c.execute('PRAGMA user_version').fetchone()[0])
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()


def row_bundle(c,patch=None,name='new'):
    assessment=a.default_assessment(name);result=a.default_result(name+'-result')
    for key,value in (patch or {}).items():
        if key in assessment:assessment[key]=value
        if key in result:result[key]=value
    a.issue_bundle(c,assessment,[result])
    return assessment,result


def graph(c,version):
    g=Graph()
    for s,p,o in c.execute('SELECT subject,predicate,object FROM v_assessment_quads WHERE graph_id=?',(version,)):
        g.add((URIRef(s),URIRef(p),URIRef(o)))
    return g


def expected_graph():
    # Hand-authored from the fixed source record and declared native meanings,
    # not by reading the SQL view, mapping builder or observed engine output.
    u=a.U;old=a.BASE
    edges=[(u('a1'),'R-12',u('basis')),(u('a1'),'R-13',u('r1')),(u('a1'),'R-45',old('context')),
      (u('a1'),'R-46',old('method')),(u('a1'),'RX-014',old('context-v1')),(u('a1'),'RX-015',u('method-v3')),
      (u('r1'),'R-14',old('scale')),(u('r1'),'R-15',u('level-v3')),(u('r1'),'R-48',u('dimension')),
      (u('r1'),'RX-016',u('scale-v3')),(u('level-v3'),'R-16',old('scale')),(old('scale'),'RK2-019',u('dimension')),
      (old('method'),'R-49',old('scale')),(old('method'),'RK2-018',u('dimension'))]
    versions=[(u('a1-v1'),u('a1')),(u('r1-v1'),u('r1')),(u('basis-v1'),u('basis')),
      (u('method-v3'),old('method')),(u('scale-v3'),old('scale')),(old('context-v1'),old('context'))]
    g=Graph()
    for s,p,o in edges:g.add((URIRef(s),URIRef(RISK+p),URIRef(o)))
    for version,artifact in versions:
        g.add((URIRef(version),RDF.type,URIRef(RISK+'RKM-C015')))
        g.add((URIRef(version),URIRef(RISK+'RX-006'),URIRef(artifact)))
    for subject,cid in [(u('a1'),'RKM-C032'),(u('r1'),'RKM-C034'),(u('basis'),'RKM-C033'),(u('dimension'),'RKM-C039'),
        (u('level-v3'),'RKM-C038'),(old('context'),'RKM-C002'),(old('method'),'RKM-C035'),(old('scale'),'RKM-C036')]:
        for kind in (cid,'RKM-C014'):g.add((URIRef(subject),RDF.type,URIRef(RISK+kind)))
    for subject,predicate,obj in [(u('a1'),'basisVersion',u('basis-v1')),(u('a1'),'temporalContext',u('time-context')),
      (u('a1'),'source',a.SOURCE),(u('level-v3'),'levelScaleVersion',u('scale-v3'))]:
        g.add((URIRef(subject),URIRef(SP+predicate),URIRef(obj)))
    return g


def compare_shacl(c):
    import run_comparison_shacl as h
    import build_comparison_shapes as shapes
    module,receipt=shapes.render();taxonomy=Graph()
    for gen in json.loads((ROOT/'ontology/riskium-model.json').read_text())['generalizations']:
        taxonomy.add((URIRef(RISK+gen['specific']),RDFS.subClassOf,URIRef(RISK+gen['general'])))
    data=graph(c,a.U('a1-v1'))
    for t in graph(c,a.U('a2-v1')):data.add(t)
    request=[URIRef(a.U('comparison-request')),URIRef(a.U('a1')),URIRef(a.U('r1')),URIRef(a.U('a2')),URIRef(a.U('r2'))]
    spec=dict(id='SQL-PROJECTION-COMPARE',raw=data,profile='direct-comparison',request=request,participants=[],mutation=None,integration=False,
        expected_findings=[],expected_decision='DIRECT_COMPARISON_ADMISSIBLE')
    positive=h.execute(spec,module,receipt,taxonomy,{})
    # A missing-time assessment is persisted without fabricating readiness.
    row_bundle(c,{'temporal_context_id':None},'no-time')
    data=graph(c,a.U('a1-v1'))
    for t in graph(c,a.U('no-time-v1')):data.add(t)
    request[3:]=[URIRef(a.U('no-time')),URIRef(a.U('no-time-result'))]
    negative=h.execute(dict(spec,id='SQL-PROJECTION-NOT-READY',raw=data,request=request,
        expected_decision='NOT_READY',expected_findings=[(str(shapes.C.RightTemporal),str(shapes.SH.MinCountConstraintComponent),str(request[0]))]),module,receipt,taxonomy,{})
    return dict(matched=positive['status']==negative['status']=='PASS' and a.compare(c,a.U('r1-v1'),a.U('no-time-result-v1'))=='NOT_READY',
        cases=[{k:row[k] for k in ('id','observed','violations','expected_findings','engine_executed','status')} for row in (positive,negative)])


def action(c,case):
    task=case['action'];u=a.U;old=a.BASE
    if task=='migration':
        before=b.logical_snapshot(c);ledger=list(c.execute('SELECT * FROM schema_migration'));a.migrate(c)
        return b.logical_snapshot(c)==before and list(c.execute('SELECT * FROM schema_migration WHERE version<3'))==ledger
    if task=='idempotent':
        before=state(c);a.migrate(c);return state(c)==before
    if task=='ledger-drift':c.execute("UPDATE schema_migration SET sha256='drift' WHERE version=1");a.migrate(c)
    if task=='schema-drift':c.execute('DROP TRIGGER snapshot_immutable_update');a.migrate(c)
    if task=='fk-off':c.execute('PRAGMA foreign_keys=OFF');a.migrate(c)
    if task=='triggers-off':c.execute('PRAGMA recursive_triggers=OFF');a.migrate(c)
    if task=='lookup':return [list(r) for r in c.execute((PROFILE/'queries/result_by_version.sql').read_text(),{'result_version':u('r1-v1')})]
    if task=='unknown':return [list(r) for r in c.execute('SELECT score_kind,reported_value FROM v_assessment_frame WHERE result_version_id=?',(u('unknown-result-v1'),))]
    if task=='labels':return c.execute("SELECT count(*) FROM v_assessment_frame f JOIN information_artifact a ON a.artifact_id=f.result_id WHERE a.label='Same result label' AND f.result_id IN (?,?)",(u('r1'),u('r2'))).fetchone()[0]
    if task=='zero':return c.execute('SELECT reported_value FROM v_assessment_frame WHERE result_version_id=?',(u('r1-v1'),)).fetchone()[0]
    if task=='raw':return c.execute('SELECT original_json FROM source_record WHERE record_id=?',(a.SOURCE,)).fetchone()[0]
    if task=='compare':return a.compare(c,u('r1-v1'),u('r2-v1'))
    if task=='compare-missing':
        row_bundle(c,{'temporal_context_id':None},'missing');return a.compare(c,u('r1-v1'),u('missing-result-v1'))
    if task=='compare-version':
        row_bundle(c,{'scale_version_id':u('scale-v4'),'level_id':u('level-v4')},'different');return a.compare(c,u('r1-v1'),u('different-result-v1'))
    if task=='update-result':c.execute("UPDATE result_snapshot SET reported_value='changed' WHERE result_version_id=?",(u('r1-v1'),))
    if task=='delete-assessment':c.execute('DELETE FROM assessment_snapshot WHERE assessment_version_id=?',(u('a1-v1'),))
    if task=='late-level':c.execute('INSERT INTO scale_level VALUES(?,?,?)',(u('late-level'),u('scale-v3'),a.SOURCE))
    if task=='late-result':
        with b.transaction(c):
            a.add_artifact(c,u('late-result'),'RKM-C034','Later');a.stage_version(c,u('late-result-v1'),u('late-result'))
            a.insert_dict(c,'result_snapshot',dict(a.default_result('late-result'),assessment_version_id=u('a1-v1')))
    if task=='late-type':c.execute('INSERT INTO artifact_typing VALUES(?,?,?,?,?,?)',(old('artifact'),'RKM-C033',None,None,None,a.SOURCE))
    if task=='bad-type':c.execute('INSERT INTO artifact_typing VALUES(?,?,?,?,?,?)',(old('method'),'RKM-C033',None,None,None,a.SOURCE))
    if task=='invalid-bundle':row_bundle(c,case['patch'])
    if task=='bundle-rollback':
        before=state(c)
        try:row_bundle(c,{'score_kind':'COMPUTED'})
        except sqlite3.IntegrityError as exc:
            return str(exc)=='R-COMPUTATION-UNSUPPORTED' and state(c)==before
        return False
    if task=='history-new':
        before=list(c.execute('SELECT * FROM v_assessment_frame WHERE result_version_id=?',(u('r1-v1'),)))
        assessment=a.default_assessment('a1');assessment['assessment_version_id']=u('a1-v2')
        result=a.default_result('r1');result.update(result_version_id=u('r1-v2'),scale_version_id=u('scale-v4'),level_id=u('level-v4'),reported_value='7')
        a.issue_bundle(c,assessment,[result])
        return list(c.execute('SELECT * FROM v_assessment_frame WHERE result_version_id=?',(u('r1-v1'),)))==before and a.compare(c,u('r1-v1'),u('r1-v2'))=='NOT_ADMISSIBLE_BY_EXACT_PIN_POLICY'
    if task=='multi-result':
        a.issue_bundle(c,a.default_assessment('many'),[a.default_result('many-1'),dict(a.default_result('many-2'),reported_value='9',source_locator='synthetic/conflicting-source')])
        return c.execute('SELECT count(*) FROM v_assessment_frame WHERE assessment_version_id=?',(u('many-v1'),)).fetchone()[0]
    if task=='backup':
        d=b.connect();c.backup(d);a.health(d);same=a.snapshot(d)==a.snapshot(c);d.close();return same
    if task=='dump':
        d=b.connect();a.restore_dump(d,'\n'.join(c.iterdump()));same=a.snapshot(d)==a.snapshot(c);d.close();return same
    if task=='disk':
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'public-synthetic.sqlite';d=a.baseline(path);before=state(d);d.close();d=b.connect(path);a.migrate(d);same=state(d)==before;d.close();return same
    if task=='rdf':
        actual=graph(c,u('a1-v1'));expected=expected_graph()
        anchors=json.loads(FIXTURE.read_text())['native_expected_edges']
        return isomorphic(actual,expected) and all((URIRef(s),URIRef(RISK+p),URIRef(o)) in actual for s,p,o in anchors)
    if task=='named-graphs':
        dataset=Dataset()
        for gid,s,p,o in c.execute('SELECT graph_id,subject,predicate,object FROM v_assessment_quads'):
            dataset.graph(URIRef(gid)).add((URIRef(s),URIRef(p),URIRef(o)))
        reparsed=Dataset();reparsed.parse(data=dataset.serialize(format='trig'),format='trig')
        return all(isomorphic(dataset.graph(URIRef(g)),reparsed.graph(URIRef(g))) for g in (u('a1-v1'),u('a2-v1'),u('a-unknown-v1'))) and (URIRef(u('a2')),URIRef(RISK+'R-13'),URIRef(u('r2'))) not in dataset.graph(URIRef(u('a1-v1')))
    if task=='shacl':return compare_shacl(c)
    if task=='binding':
        value="'; DROP TABLE result_snapshot; --";row_bundle(c,{'reported_value':value},'binding');return c.execute('SELECT reported_value FROM result_snapshot WHERE result_version_id=?',(u('binding-result-v1'),)).fetchone()[0]
    if task=='design-audit':return design_audit(c)['findings']==[]
    if task=='one-column':
        c.execute('CREATE TABLE unexplained(id TEXT PRIMARY KEY NOT NULL) STRICT')
        return any(r['code']=='UNEXPLAINED_ONE_COLUMN_TABLE' for r in design_audit(c)['findings'])
    if task=='concurrency':
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'concurrency.sqlite';writer=a.baseline(path);writer.execute('PRAGMA journal_mode=WAL')
            reader=b.connect(path);reader.execute('PRAGMA busy_timeout=0');reader.execute('BEGIN')
            before=reader.execute('SELECT count(*) FROM source_record').fetchone()[0]
            writer.execute('BEGIN IMMEDIATE');writer.execute('INSERT INTO source_record VALUES(?,?)',(u('concurrent'),'{}'))
            invisible=reader.execute('SELECT count(*) FROM source_record').fetchone()[0]==before
            conflict=False
            contender=b.connect(path);contender.execute('PRAGMA busy_timeout=0')
            try:contender.execute('BEGIN IMMEDIATE')
            except sqlite3.OperationalError as exc:conflict=str(exc)=='database is locked'
            writer.execute('COMMIT');still_snapshot=reader.execute('SELECT count(*) FROM source_record').fetchone()[0]==before;reader.execute('COMMIT')
            visible=reader.execute('SELECT count(*) FROM source_record').fetchone()[0]==before+1
            contender.execute('BEGIN IMMEDIATE');contender.execute('ROLLBACK')
            for conn in (contender,reader,writer):conn.close()
            return invisible and conflict and still_snapshot and visible
    if task=='mutant-immutability':
        c.execute('DROP TRIGGER a_result_snapshot_update');c.execute("UPDATE result_snapshot SET reported_value='changed' WHERE result_version_id=?",(u('r1-v1'),))
        return c.execute('SELECT reported_value FROM result_snapshot WHERE result_version_id=?',(u('r1-v1'),)).fetchone()[0]
    if task=='mutant-version':
        c.execute('DROP TRIGGER a_assessment_snapshot_insert');row_bundle(c,{'context_version_id':u('method-v3')},'mutant')
        return c.execute('SELECT context_version_id FROM assessment_snapshot WHERE assessment_version_id=?',(u('mutant-v1'),)).fetchone()[0]==u('method-v3')
    if task=='tamper':c.execute('DROP TRIGGER a_result_snapshot_update');a.health(c)
    raise ValueError('Unknown action '+task)


def execute(case):
    if case['action'] in ('migration','ledger-drift','schema-drift'):
        c=b.connect();b.migrate(c,1);b.seed_v1(c,json.loads((b.OUT/'fixtures.json').read_text()));b.migrate(c)
    else:c=a.baseline()
    trace=[];before=state(c) if case['action'] not in ('migration','ledger-drift','schema-drift') else hashlib.sha256(json.dumps(b.logical_snapshot(c),sort_keys=True).encode()).hexdigest()
    c.set_trace_callback(trace.append);error=None;details=None
    try:
        observed=action(c,case)
        if isinstance(observed,dict):details=observed;observed=observed['matched']
    except (sqlite3.Error,ValueError) as exc:error=str(exc);observed=None
    after=state(c) if c.execute('PRAGMA user_version').fetchone()[0]==3 else hashlib.sha256(json.dumps(b.logical_snapshot(c),sort_keys=True).encode()).hexdigest()
    # Error cases that intentionally alter configuration/schema are preflight
    # controls; rejected domain writes must roll back without any partial rows.
    atomic=case['expected_error'] is None or case['action'] in ('ledger-drift','schema-drift','fk-off','triggers-off','tamper') or before==after
    status='PASS' if observed==case['expected'] and error==case['expected_error'] and atomic else 'FAIL'
    c.close()
    return dict(id=case['id'],action=case['action'],kind=case['kind'],requirements=case['requirements'],expected=case['expected'],observed=observed,
        expected_error=case['expected_error'],observed_error=error,status=status,rejected_write_atomic=atomic,before_state_sha256=before,after_state_sha256=after,sql_trace=trace,details=details)


def generated(fixture):
    c=a.baseline();rows=[]
    for item in fixture['generated_inputs']:
        label=item['id'].lower();assessment=a.default_assessment(label);result=a.default_result(label+'-result')
        result.update(reported_value=item['reported_value'],score_kind=item['expected_kind'])
        assessment['context_version_id']=item['context_version']
        with b.transaction(c):
            a.add_artifact(c,result['result_id'],'RKM-C034',item['duplicate_label'])
            a.issue_bundle(c,assessment,[result])
        observed=c.execute('SELECT f.score_kind,f.reported_value,f.context_version_id,a.label FROM v_assessment_frame f JOIN information_artifact a ON a.artifact_id=f.result_id WHERE result_version_id=?',(result['result_version_id'],)).fetchone()
        expected=(item['expected_kind'],item['expected_lexeme'],item['context_version'],item['duplicate_label'])
        rows.append(dict(id=item['id'],seed=item['seed'],expected=expected,observed=observed,status='PASS' if observed==expected else 'FAIL'))
    a.health(c)
    distinct=c.execute("SELECT count(DISTINCT result_id) FROM result_snapshot WHERE result_id LIKE 'urn:riskium:assessment:gen-%'").fetchone()[0]
    if distinct!=len(rows):raise ValueError('Generated equal labels collapsed identities')
    result=dict(inputs=len(rows),seeds=sorted({r['seed'] for r in rows}),rows=rows,distinct_generated_results=distinct,final_logical_state_sha256=state(c),real_case_population=False)
    c.close();return result


def benchmark():
    policy=load_policy()['synthetic_policy'];c=a.baseline()
    for i in range(policy['performance_records']):
        row_bundle(c,{'reported_value':str(i)},'workload-'+str(i))
    workloads={
      'pinned_result':((PROFILE/'queries/result_by_version.sql').read_text(),{'result_version':a.U('workload-500-result-v1')}),
      'source_trace':((PROFILE/'queries/source_trace.sql').read_text(),{'source_record':a.SOURCE}),
      'assessment_results':((PROFILE/'queries/results_for_assessment.sql').read_text(),{'assessment_version':a.U('workload-500-v1')}),
      'historical_versions':((PROFILE/'queries/result_history.sql').read_text(),{'artifact_id':a.U('workload-500-result')})}
    results=[]
    for name,(query,params) in workloads.items():
        expected=c.execute(query,params).fetchall()
        for _ in range(policy['warmups']):c.execute(query,params).fetchall()
        samples=[]
        for _ in range(policy['timing_repetitions']):
            start=time.perf_counter_ns();observed=c.execute(query,params).fetchall();samples.append((time.perf_counter_ns()-start)/1e6)
            if observed!=expected:raise ValueError('Workload changed answers')
        # Query-specific cardinality/value checks are independent of its first run.
        valid=(expected==[(a.U('workload-500-result'),'500',a.BASE('context-v1'),a.U('method-v3'),a.U('basis-v1'),a.U('scale-v3'),a.U('dimension'))] if name=='pinned_result' else
          expected==[(a.U('workload-500-result-v1'),)] if name=='assessment_results' else
          expected==[(a.U('workload-500-result-v1'),)] if name=='historical_versions' else len(expected)==policy['performance_records']+3)
        if not valid:raise ValueError('Workload answer oracle failed: '+name)
        results.append(dict(id=name,sql=query,parameters=params,answer_rows=len(expected),oracle_matched=True,
            explain_query_plan=[list(row) for row in c.execute('EXPLAIN QUERY PLAN '+query,params)],
            timing_ms=dict(median=statistics.median(samples),p95=sorted(samples)[math.ceil(.95*len(samples))-1],samples=samples)))
    a.health(c);c.close()
    return dict(dataset=dict(generated_assessments=policy['performance_records'],generated_results=policy['performance_records'],fixed_results=3),
        repetitions=policy['timing_repetitions'],warmups=policy['warmups'],storage='in-memory SQLite',workloads=results,
        approved_production_slo=None,production_performance_claimed=False,plan_text_compared_across_engines=False)


def run():
    policy=load_policy();fixture=json.loads(FIXTURE.read_text())
    if fixture['policy_sha256']!=sha(PROFILE/'policy.json') or fixture['requirements_sha256']!=sha(ROOT/'requirements/relational-requirements.json'):
        raise ValueError('Assessment oracle/policy/requirement binding changed')
    for name,text in build().items():
        if (PROFILE/name).read_text()!=text:raise ValueError('Generated assessment file changed: '+name)
    cases=[execute(case) for case in fixture['cases']]
    failed=[case for case in cases if case['status']!='PASS']
    if failed:
        for case in failed:print(json.dumps({k:case[k] for k in ('id','expected','observed','expected_error','observed_error','rejected_write_atomic')}),flush=True)
        raise ValueError('Assessment fixed-oracle mismatch')
    gen=generated(fixture)
    if any(r['status']!='PASS' for r in gen['rows']):raise ValueError('Generated property mismatch')
    c=a.baseline();audit=design_audit(c);c.close()
    if audit['findings']:raise ValueError('Schema design/dictionary findings remain')
    measured=benchmark()
    inputs=sorted(set(INPUTS)|set(policy['baseline_sha256'])|{str(p.relative_to(ROOT)) for p in (PROFILE/'queries').glob('*.sql')})
    report=dict(schema='riskium-assessment-relational-evidence-v1',generated_at_utc=datetime.now(timezone.utc).isoformat(),
        source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        source_commit_role='Execution checkout; exact evaluated bytes bound separately; receipt may be committed later.',
        initial_oracle_commit='3ed56e501bff3ece7d58a7e49167f6a928fd3739',inputs={p:sha(ROOT/p) for p in inputs},
        engine=dict(sqlite=sqlite3.sqlite_version,python=sys.version.split()[0],foreign_keys=True,recursive_triggers=True,
            rdflib=importlib.metadata.version('rdflib'),pyshacl=importlib.metadata.version('pyshacl')),
        summary=dict(fixed_cases=len(cases),statuses=dict(Counter(r['status'] for r in cases)),by_kind=dict(Counter(r['kind'] for r in cases)),
            generated_inputs=gen['inputs'],generated_matches=sum(r['status']=='PASS' for r in gen['rows']),schema_audit=audit['summary'],
            measured_workloads=len(measured['workloads']),shacl_engine_executions=2),
        cases=cases,generative=gen,schema_audit=audit,workload=measured,profile_version='0.2.0',drsd_version='0.1.0',
        native_semantics_changed=False,real_case_study_used=False,independent_semantic_acceptance=False,
        external_r2rml_engine_executed=False,full_private_migration_executed=False,production_acceptance=False,limits=policy['scope_limits'])
    return report


def verify_saved(old,new):
    for key in ('schema','initial_oracle_commit','inputs','summary','profile_version','drsd_version','native_semantics_changed',
      'real_case_study_used','independent_semantic_acceptance','external_r2rml_engine_executed','full_private_migration_executed','production_acceptance','limits'):
        if old[key]!=new[key]:raise ValueError('Assessment receipt differs: '+key)
    if old['schema_audit']!=new['schema_audit']:raise ValueError('Schema dictionary/FD audit changed')
    for before,after in zip(old['cases'],new['cases']):
        for key in ('id','action','kind','requirements','expected','observed','expected_error','observed_error','status','rejected_write_atomic','before_state_sha256','after_state_sha256','details'):
            if json.dumps(before[key],sort_keys=True)!=json.dumps(after[key],sort_keys=True):raise ValueError('Saved fixed oracle differs: '+after['id']+' '+key)
    if json.dumps(old['generative'],sort_keys=True)!=json.dumps(new['generative'],sort_keys=True):raise ValueError('Saved generated answers differ')
    for before,after in zip(old['workload']['workloads'],new['workload']['workloads']):
        for key in ('id','sql','parameters','answer_rows','oracle_matched'):
            if json.dumps(before[key])!=json.dumps(after[key]):raise ValueError('Workload answer contract differs')
    # Timings and SQLite plan text are observations of the declared runtime,
    # never fixed expected outcomes or fabricated cross-runtime equality.


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    report=run();path=OUT/'report.json.gz'
    if args.check:verify_saved(json.loads(gzip.decompress(path.read_bytes())),report)
    else:
        path.write_bytes(gzip.compress((json.dumps(report,indent=2,ensure_ascii=False)+'\n').encode(),mtime=0))
        (PROFILE/'schema-dictionary.md').write_text(render_design(report['schema_audit']))
        lines=['# Executed SQLite assessment profile 0.2.0','',
            'Bounded engineering evidence under #29/#12. Original v0.3.1, ORSD 0.4.3, paper 7.0.8 and SQL profile 0.1.0 remain unchanged. No new actual case study, PostgreSQL run, independent review or production certification.','',
            'The [database requirements](../../../requirements/relational-requirements.json), [policy](../../../implementation/relational/0.2.0/policy.json) and [48 fixed / 100 seeded inputs](../../../implementation/relational/0.2.0/fixtures.json) were committed before execution at `3ed56e501bff3ece7d58a7e49167f6a928fd3739`. The full RDF projection regression also uses separately hand-authored expected facts, not query output.','',
            'Summary: '+json.dumps(report['summary'])+'.','',
            '[Full receipt with exact SQL errors, before/after state hashes, traces, generated answers, schema audit, query plans and measurements](report.json.gz). [Actual schema dictionary and FD review](../../../implementation/relational/0.2.0/schema-dictionary.md).', '',
            'The two weakened-rule controls deliberately remove enforcement; their bad inputs becoming possible is sensitivity evidence, not valid domain data. Raw/unknown, managed rows and strict task eligibility remain distinct. Reported lexical zero is retained without arithmetic. Historical native interpretation facts are exported in separate named assessment-version graphs.','',
            'Timing samples describe 1,000 generated assessments/results in memory and four declared workloads; there is no approved production SLO or human usability result. Query-plan text is retained but not required byte-equal across SQLite versions. No normal-form or universal mapping correctness score is inferred from structural counts.','',
            '| Case | Expected | Observed | Result |','| --- | --- | --- | --- |']
        for row in report['cases']:lines.append(f"| {row['id']} | {row['expected_error'] or row['expected']} | {row['observed_error'] or row['observed']} | {row['status']} |")
        lines += ['', 'Replay: `python tools/run_relational_assessment.py --check`. Every input must match its saved SHA-256; source cases, runtime observations and generated test populations have separate meanings.']
        (OUT/'README.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(report['summary']),flush=True)


if __name__=='__main__':main()
