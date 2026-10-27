"""Bind the additive source/scenario requirements and all 306 source elements."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import relational_source_scenario as k

ROOT=k.ROOT
OUT=ROOT/'evaluation/relational/source-scenario'
GROUPS={
'SSC-01':['POPULATED_UPGRADE','IDEMPOTENT_UPGRADE','FAILED_UPGRADE','LEGACY_GRAPH_PRESERVED'],
'SSC-02':['NO_CASE','MISSING_CASE','RAW_EXCLUSION','WRONG_CONTEXT_KIND','UNISSUED_CONTEXT','CONTEXT_OWNER_MISMATCH','REFERENCE_MULTI_CONTEXT','MIXED_CLASS','UNISSUED_EXCLUDED'],
'SSC-03':['PROVENANCE_EXACT','OLD_VERSION_CONTEXT','UNKNOWN_CONTEXT','MISSING_SOURCE','FORGED_SOURCE','EMPTY_PROVENANCE','BAD_CALENDAR','PAYLOAD_DRIFT','OWNER_DRIFT','IMMUTABLE_SNAPSHOT','IMMUTABLE_CASE','IMMUTABLE_CONTEXT','REPLACE_SNAPSHOT','REPLACE_CASE','REPLACE_CONTEXT','DUPLICATE_CASE','DUPLICATE_CONTEXT','DUPLICATE_VERSION','ATOMIC_BUNDLE_FAILURE'],
'SSC-04':['CASE1_HISTORY','CASE2_HISTORY','EQUAL_LABEL_IDENTITIES','NO_OCCURRENCE_CAUSATION','NO_GENERAL_CORRECTION','BOUND_PARAMETER','NATIVE_SCENARIO_A1','NATIVE_SCENARIO_A2','NATIVE_SCENARIO_B1','NATIVE_REFERENCE_A1','NATIVE_REFERENCE_A2','NATIVE_REFERENCE_B1','MUTANT_DIRECTION_EXPOSED'],
'SSC-05':['BACKUP_REOPEN','FILE_REOPEN','DUMP_RESTORE','RESTORE_TAMPER','CONFIGURATION_OFF','LEDGER_DRIFT','SCHEMA_DRIFT','MUTANT_CARDINALITY_EXPOSED','MUTANT_FROZEN_LINK_EXPOSED'],
'SSC-06':['RAW_EXCLUSION','NO_OCCURRENCE_CAUSATION','NO_GENERAL_CORRECTION']}

def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def encode(x):return json.dumps(x,indent=2)+'\n'

def build():
    contract=k.contract();report=json.loads((OUT/'report.json').read_text())
    for p,h in report['inputs_sha256'].items():
        if sha(p)!=h:raise ValueError('Stale source/scenario receipt input: '+p)
    if report['summary']['outcomes']!={'PASS':54}:raise ValueError('Source/scenario execution failed')
    cases={r['id']:r for r in report['cases']}
    if len(cases)!=54 or set().union(*map(set,GROUPS.values()))!=set(cases):raise ValueError('Lost source/scenario requirement/case trace')
    model=json.loads((ROOT/'ontology/riskium-model.json').read_text())
    source={r['id']:r for family in ('concepts','imported_types','associations','generalizations','constraints') for r in model[family]}
    baseline='evaluation/relational/correction/mapping-accounting.json'
    old=json.loads((ROOT/baseline).read_text());rows=old['rows']
    selected=set(contract['native_classes']+contract['native_relations']+contract['generalizations'])
    if len(source)!=306 or len(rows)!=306 or {r['id'] for r in rows}!=set(source) or len(selected)!=8:raise ValueError('Lost native accounting identity')
    for r in rows:
        actual=hashlib.sha256(json.dumps(source[r['id']],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
        if actual!=r['source_sha256']:raise ValueError('Native source drift: '+r['id'])
        r['historical_0_3_0_disposition']=r['disposition']
        if r['id'] in selected:
            r['disposition']='SCOPED_ADDITIVE_SOURCE_SCENARIO_MAPPING'
            r['source_scenario_overlay']='Executed 0.4.0 selected storage/native direction or inherited typing; no full semantic or independent acceptance.'
        else:r['source_scenario_overlay']='NO_ADDITIONAL_MAPPING'
    inventory=dict(schema='riskium-source-scenario-accounting-v1',profile='0.4.0',baseline_path=baseline,baseline_sha256=sha(baseline),source_elements=306,source_sha256=sha('ontology/riskium-model.json'),historical_summary=old['summary'],current_dispositions=dict(Counter(r['disposition'] for r in rows)),new_class_representations=2,new_relation_exports=4,inherited_typing_routes=2,remaining_deferred=242,additional_partial_routes=8,full_mapping_completed=False,rows=rows)
    trace=[]
    req_ids={r['id'] for r in json.loads((ROOT/'requirements/requirements.json').read_text())}
    for req in contract['requirements']:
        if not set(req['source_requirements']).issubset(req_ids):raise ValueError('Unknown original requirement')
        trace.append(dict(requirement=req,cqs=['RQ-CQ02','RQ-CQ06','RQ-CQ08'],case_ids=GROUPS[req['id']],implementation=['005_source_scenario.sql','relational_source_scenario.py','queries/by_case.sql','queries/provenance.sql'],status='SCOPED_EXECUTED_ENGINEERING',limit='Original ORSD/DRSD and engine/independent acceptance remain distinct; not full native class/rule completeness.'))
    paths=set(report['inputs_sha256'])|set(contract['source_sha256'])|{baseline,'requirements/requirements.json','requirements/competency-questions.json','tests/test_source_scenario.py','tools/build_source_scenario_inventory.py','implementation/relational/0.4.0/README.md','implementation/relational/0.4.0/schema-dictionary.md','evaluation/relational/source-scenario/report.json','evaluation/relational/source-scenario/README.md','evaluation/sources/cq0708/cohort.json','evaluation/sources/cq0708/report.json.gz'}
    inputs={p:sha(p) for p in sorted(paths)}
    tracing=dict(schema='riskium-source-scenario-requirement-trace-v1',profile='0.4.0',execution_issue=42,parent_issues=[35,12],original_drsd='0.1.0 unchanged; SSC-01..06 are an explicit derived supplement',requirements=trace,inputs_sha256=inputs,original_organizational_admissions='All 11 WITHHELD; no new real-data admission executed')
    outputs={'evaluation/relational/source-scenario/mapping-accounting.json':encode(inventory),'evaluation/relational/source-scenario/traceability.json':encode(tracing)}
    component=dict(schema='riskium-source-scenario-component-v1',id='SOURCE_SCENARIO',version='0.4.0',schema_version=5,compatible_model='0.3.1',baseline_sql_profile='0.3.0',status='DEVELOPMENT_COMPONENT_NOT_SELECTED_BY_STABLE_DISTRIBUTION',stable_distribution_unchanged='v0.3.3',summary=report['summary'],native_support=dict(classes=2,relations=4,inherited_typing_routes=2,full_mapping_completed=False),files_sha256=dict(inputs,**{p:hashlib.sha256(data.encode()).hexdigest() for p,data in outputs.items()}))
    outputs['implementation/relational/0.4.0/component.json']=encode(component)
    return outputs

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    for name,data in build().items():
        target=ROOT/name
        if args.check:
            if not target.is_file() or target.read_text()!=data:raise ValueError('Stale source/scenario accounting: '+name)
        else:target.write_text(data)
    print(encode(dict(status='SOURCE_SCENARIO_ACCOUNTING_PASS',native_elements=306,new_class_representations=2,new_relation_exports=4,requirements=6)))

if __name__=='__main__':main()
