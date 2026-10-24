"""Trace actual DB requirements, mapping, dictionary, oracles and scoped evidence."""
import argparse
from collections import Counter
import copy
import gzip
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evaluation/relational/assessment'
SPEC='requirements/relational-requirements.json'
REPORT='evaluation/relational/assessment/report.json.gz'


def read(path):return json.loads((ROOT/path).read_text())
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)


OBJECTS={
 1:['full source inventory','mapping.json'],2:['identity_registry','information_artifact','artifact_typing'],
 3:['mapping.json','v_assessment_quads'],4:['assessment_snapshot','result_snapshot','scale_snapshot','scale_level','method_scope'],
 5:['version_snapshot','version-owned guards','atomic issue_bundle'],6:['result_snapshot','source_record'],
 7:['source_record','result source_locator/interpretation_origin','owner-specific RDF source'],8:['result_snapshot.score_kind/reported_value'],
 9:['all table keys/FKs/STRICT/checks','configured connection'],10:['schema_migration','migration 3','atomic issue_bundle'],
 11:['backup API','restore_dump data audit','reopen'],12:['assessment_snapshot recorded/reference/validity fields'],
 13:['actual table purposes','authored FD/denormalization review','one-column controls'],14:['schema-dictionary.md'],
 15:['fixtures.json generated_inputs','seeded metamorphic checks'],16:['a_result_snapshot_update','a_assessment_snapshot_insert','exact error oracles'],
 17:['v_assessment_quads','mapping.ttl','expected_graph','SHACL selection task'],18:['queries/*.sql','historical version lookups'],
 19:['four workload SQL files','answer oracles','EXPLAIN QUERY PLAN','timing samples'],20:['two-connection WAL/snapshot/writer conflict'],
 21:['parameter binding','field whitelist','connection policy','schema/data health'],22:['declared and actual runtime/configuration'],
 23:['versioned manifest','artifact/requirement/case crosswalk','source hashes'],24:['all retained scoped gates'],
 25:['future PostgreSQL work'],26:['future authorized private full-schema migration'],27:['future formula/interval/workflow semantics'],28:['future real user/deployment acceptance']}


def build():
    spec=read(SPEC);mapping=read('implementation/relational/0.2.0/mapping.json')
    model=read('ontology/riskium-model.json');fixture=read('implementation/relational/0.2.0/fixtures.json')
    report=json.loads(gzip.decompress((ROOT/REPORT).read_bytes()))
    for path,expected in spec['source_hashes'].items():require(sha(path)==expected,'Original semantic requirements/model changed: '+path)
    for path,expected in report['inputs'].items():require(sha(path)==expected,'Database executed input changed: '+path)
    require(fixture['requirements_sha256']==sha(SPEC),'DRSD oracle binding differs')
    require(mapping['source_model_sha256']==sha('ontology/riskium-model.json'),'Mapping source differs')
    require(report['profile_version']==mapping['profile_version']==spec['relational_profile']=='0.2.0','Profile version mismatch')
    require(report['drsd_version']==spec['document_version']=='0.1.0','DRSD version mismatch')
    require(report['native_semantics_changed'] is False and report['real_case_study_used'] is False and report['production_acceptance'] is False and report['independent_semantic_acceptance'] is False,'Unsupported scientific/deployment acceptance')
    require(report['summary']['fixed_cases']==48 and report['summary']['statuses']=={'PASS':48},'Fixed scenario failures or denominator changed')
    require([r['id'] for r in report['cases']]==[r['id'] for r in fixture['cases']],'Fixed case identity differs')
    require(report['summary']['generated_inputs']==report['summary']['generated_matches']==100,'Generated oracle failures')
    require(report['schema_audit']['findings']==[] and report['summary']['measured_workloads']==4,'Design/workload gate missing')
    semantic={r['id']:r for r in read('requirements/requirements.json')};clauses={r['id'] for r in model['constraints']}
    requirements=spec['requirements']
    require(len(requirements)==28 and {r['id'] for r in requirements}=={f'DBR-{i:02}' for i in range(1,29)},'DRSD denominator changed')
    cases={r['id']:r for r in report['cases']}
    rows=[]
    for i,req in enumerate(requirements,1):
        require(set(req['derived_from_orsd']).issubset(semantic) and set(req['constraint_ids']).issubset(clauses),'Broken semantic derivation: '+req['id'])
        linked=[r['id'] for r in report['cases'] if req['id'] in r['requirements']]
        methods=['EXECUTED_FIXED_CASES'] if linked else []
        extra=[]
        if i==1:methods+=['STATIC_EXHAUSTIVE_SOURCE_ACCOUNTING'];extra+=['mapping-coverage.json']
        if i==15:methods+=['EXECUTED_SEEDED_PROPERTIES'];extra+=['generative:100']
        if i==19:methods+=['MEASURED_SYNTHETIC_WORKLOAD'];extra+=[w['id'] for w in report['workload']['workloads']]
        if i in (13,14):methods+=['ACTUAL_SCHEMA_INSPECTION','AUTHORED_DESIGN_REVIEW'];extra+=['schema_audit']
        if i==22:methods+=['RECORDED_RUNTIME_AND_CONFIGURATION'];extra+=['engine']
        if i==23:methods+=['STATIC_HASH_AND_TRACE_INTEGRITY'];extra+=['component/requirement/case references']
        if i==24:methods+=['SCOPED_RETAINED_GATE_ACCOUNTING'];extra+=['all current DBR-01..DBR-23 evidence']
        if i<=24:
            require(req['applies_to_current_profile'] is True and req['scope']=='PUBLIC_SQLITE_0.2.0','Current requirement silently excluded')
            require(bool(methods) and all(cases[c]['status']=='PASS' for c in linked),'Missing/failed evidence: '+req['id'])
        else:
            require(req['applies_to_current_profile'] is False and req['scope']=='FUTURE_NOT_EXECUTED','Future requirement silently accepted')
        rows.append(dict(id=req['id'],title=req['title'],priority=req['priority'],scope=req['scope'],
            derived_from_orsd=req['derived_from_orsd'],constraint_ids=req['constraint_ids'],
            source_requirement_sha256=hashlib.sha256(json.dumps(req,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest(),
            implementation_objects=OBJECTS[i],case_ids=linked,additional_evidence=extra,evidence_kinds=methods,
            status='PASS_WITH_DECLARED_PROFILE_LIMITS' if i<=24 else 'NOT_RUN_FUTURE',
            remaining_issue=12 if i>24 else None))
    for case in report['cases']:
        require(set(case['requirements']).issubset({r['id'] for r in requirements}),'Case points to unknown DBR')
    orsd=[]
    reasons={'RKRS-07':'Responsibility and actual mandates are outside this assessment/result slice.',
       'RKRS-09':'External/mode bearer boundary remains in the model; no new full relational bearer mapping.',
       'RKRS-10':'Appetite, tolerance and threshold task tables are not implemented here.'}
    for sid,req in semantic.items():
        children=[r['id'] for r in rows if sid in r['derived_from_orsd']]
        orsd.append(dict(id=sid,original_priority=req['priority'],database_requirements=children,
            status='DERIVED_SUBCLAUSES_ONLY_NOT_FULL_ORSD_ACCEPTANCE' if children else 'NO_CURRENT_DB_IMPLEMENTATION',
            reason=reasons.get(sid,'Current DBR scope supplies only the named subclauses; original semantic/application acceptance is not inherited.')))
    cq_status={
      'RQ-CQ01':('BASE_PROFILE_EVIDENCE_ONLY',['original 67-case history suite'],'Selected case/entry joins remain the original public profile, not independently adjudicated cases.'),
      'RQ-CQ02':('NOT_IMPLEMENTED',[],'No scenario-to-case relational population is added.'),
      'RQ-CQ03':('SCOPED_SQL_TASK_SUPPLEMENT',['DIRECT-COMPARISON-DIFFERENT-VERSION','EXACT-VERSION-PINNED-LOOKUP'],'Equal lexical scores retain distinct pins; no arithmetic/ranking is supplied.'),
      'RQ-CQ04':('NOT_IMPLEMENTED',[],'Assignment/actual mandate mapping remains separate.'),
      'RQ-CQ05':('NOT_IMPLEMENTED',[],'No full workflow/cessation engine or acceptance is supplied.'),
      'RQ-CQ06':('SCOPED_SYNTHETIC_SQL_TRACE_ONLY',['RAW-INPUT-EXACT','SQL-RDF-FIXED-FACTS'],'Source FK/locator/origin engineering; not the independent literature/source accuracy population.'),
      'RQ-CQ07':('NOT_IMPLEMENTED_GENERAL_CORRECTION',[],'Artifact version grouping and original entry lineage do not implement general corrected-assertion semantics.'),
      'RQ-CQ08':('BOUNDARY_PRESERVED_NOT_FULL_TASK',[],'No new governed organizational case is admitted; no original independent population is relabeled.')}
    cq=[dict(id=q['id'],question=q['question'],status=cq_status[q['id']][0],evidence=cq_status[q['id']][1],limits=cq_status[q['id']][2]) for q in read('requirements/competency-questions.json')]
    # Extend the old source inventory without rewriting its separately bound 0.1.0 report.
    coverage=copy.deepcopy(read('evaluation/relational/coverage/report.json'))
    new_classes={r['id'] for r in mapping['new_classes']};new_relations={r['id'] for r in mapping['new_relations']}
    partial={'C-01','C-03','C-04','C-05','C-13','C-16','C-17','C-18','C-21','C-24','C-25'}
    for row in coverage['rows']:
        if row['id'] in new_classes and row['family']=='Concept':
            row.update(disposition='SELECTED_STORAGE_REPRESENTATION',representation='0.2.0 information_artifact + artifact_typing/version-owned facts',reason='Explicit selected membership and identity/pin enforcement, not full class admission.',next_evidence='Retain all unimplemented native/task subclauses under #12.')
        if row['id'] in new_relations and row['family']=='Relation':
            row.update(disposition='SELECTED_NATIVE_EXPORT',representation='0.2.0 v_assessment_quads; named assessment-version graph',reason='Selected version-owned native edge with exact fixture/projection expectations.',next_evidence='Complete unselected populations and semantics remain open.')
        if row['family']=='Constraint' and row['id'] in partial:
            row.update(disposition='SELECTED_SUBCLAUSES_ONLY',reason='Original 0.1.0 and new 0.2.0 named engineering subclauses only; no full original constraint acceptance.',next_evidence='Follow the explicit policy/ORSD exclusions; broad #12/#4/#5 remains open.')
    coverage.update(schema='riskium-assessment-full-source-accounting-v1',inventory_version='0.2.0',relational_profile='0.2.0',method='Static 306-element reconciliation over executed selected base/assessment profiles; not 306 engine passes.',
        inputs={**coverage['inputs'],'implementation/relational/0.2.0/mapping.json':sha('implementation/relational/0.2.0/mapping.json'),REPORT:sha(REPORT)},
        summary=dict(total_source_elements=len(coverage['rows']),families=dict(Counter(r['family'] for r in coverage['rows'])),dispositions=dict(Counter(r['disposition'] for r in coverage['rows']))))
    require(coverage['summary']['total_source_elements']==306 and coverage['summary']['dispositions']['SELECTED_STORAGE_REPRESENTATION']==15 and coverage['summary']['dispositions']['SELECTED_NATIVE_EXPORT']==19,'Current mapping support accounting differs')
    artifacts=[SPEC,REPORT,'implementation/relational/0.2.0/mapping.json','implementation/relational/0.2.0/policy.json',
      'implementation/relational/0.2.0/schema-dictionary.md','tools/check_database_assurance.py',
      'docs/relational-assurance-request.md','docs/relational-assurance.md']
    assurance=dict(schema='riskium-database-assurance-trace-v1',assurance_version='0.1.0',drsd_version='0.1.0',relational_profile='0.2.0',model_version='0.3.1',orsd_revision='0.4.3',
        inputs={p:sha(p) for p in artifacts},summary=dict(database_requirements=28,retained=24,retained_with_scoped_evidence=24,future_not_run=4,original_requirements_accounted=12,original_cqs_accounted=8,
            orphan_requirements=0,orphan_fixed_case_links=0,fixed_scenarios=48,generated_inputs=100,selected_class_representations=15,selected_native_predicates=19),
        status='SCOPED_DATABASE_ENGINEERING_GATES_PASS',overall_semantic_correctness_percent=None,full_original_orsd_acceptance=False,
        actual_user_acceptance=False,production_slo_approved=False,independent_semantic_acceptance=False,
        db_requirements=rows,original_orsd=orsd,original_cqs=cq,limits=report['limits'])
    lines=['# Database requirements, mapping and executed evidence','',
       'This trace separates static source accounting, authored design review, fixed executions, generated properties and workload observations. Current scope is public SQLite 0.2.0/DRSD 0.1.0, not full original ORSD or deployment acceptance. Four future MUST requirements remain NOT_RUN rather than being removed or silently downgraded.','',
       '[Machine trace/readiness](assurance.json), [all 306 source dispositions](mapping-coverage.json), [actual SQL receipt](report.json.gz), [method and checklist](../../../docs/relational-assurance.md).','',
       '| DB requirement | Source ORSD | Implementation objects | Evidence | Status |','| --- | --- | --- | --- | --- |']
    for row in rows:
        lines.append('| '+row['id']+' '+row['title']+' | '+', '.join(row['derived_from_orsd'])+' | '+', '.join(row['implementation_objects'])+' | '+', '.join(row['case_ids']+row['additional_evidence'])+' | '+row['status']+' |')
    lines+=['','## Original ORSD crosswalk','','| Original requirement | DBR derivations | Current boundary |','| --- | --- | --- |']
    for row in orsd:lines.append('| '+row['id']+' | '+', '.join(row['database_requirements'])+' | '+row['status']+': '+row['reason']+' |')
    lines+=['','## Original CQ crosswalk','','| CQ | Current database evidence | Remaining boundary |','| --- | --- | --- |']
    for row in cq:lines.append('| '+row['id']+' | '+row['status']+' | '+row['limits']+' |')
    return {'assurance.json':json.dumps(assurance,indent=2)+'\n','mapping-coverage.json':json.dumps(coverage,indent=2)+'\n','traceability.md':'\n'.join(lines)+'\n'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    outputs=build()
    for name,text in outputs.items():
        path=OUT/name
        if args.check:require(path.exists() and path.read_text()==text,'Database trace differs: '+name)
        else:path.write_text(text)
    print(json.dumps(dict(status='SCOPED_DATABASE_ASSURANCE_PASS',retained_requirements=24,future_requirements_not_run=4,source_elements=306,
        selected_class_representations=15,selected_native_predicates=19,full_original_orsd_acceptance=False,production_acceptance=False)))


if __name__=='__main__':main()
