"""Bind all 306 native accounting rows and correction requirements to evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import relational_correction as c

ROOT=c.ROOT
OUT=ROOT/'evaluation/relational/correction'
GROUPS={
 'COR-01':['POPULATED_UPGRADE','IDEMPOTENT_UPGRADE','FAILED_UPGRADE','LEDGER_DRIFT','SCHEMA_DRIFT'],
 'COR-02':['CROSS_IDENTITY','MISSING_PARENT','SELF_EDGE','DUPLICATE_EDGE','REPLACE_EDGE','UPDATE_EDGE','DELETE_EDGE','CYCLE','UNISSUED_PARENT','MUTANT_IDENTITY_EXPOSED'],
 'COR-03':['EMPTY_REASON','MISSING_SOURCE','BAD_CALENDAR','EARLY_DECLARATION','ATOMIC_BUNDLE_FAILURE','OLD_VALUE','NEW_VALUE'],
 'COR-04':['ALL_BRANCH_VALUES','BRANCH_DEPTHS','CORROBORATION_NOT_INFERRED','STAGING_NOT_PUBLISHED','NATIVE_RDF_V1','NATIVE_RDF_V2','NATIVE_RDF_V3'],
 'COR-05':['BACKUP_REOPEN','FILE_REOPEN','DUMP_RESTORE','RESTORE_TAMPER','CONFIGURATION_OFF','MUTANT_UPDATE_EXPOSED','BOUND_QUERY_INJECTION']}


def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def encoded(data):return json.dumps(data,indent=2)+'\n'


def build():
    policy=c.contract();report=json.loads((OUT/'report.json').read_text())
    baseline_path='evaluation/relational/assessment/mapping-coverage.json'
    baseline=json.loads((ROOT/baseline_path).read_text())
    for path,digest in report['inputs_sha256'].items():
        if sha(path)!=digest:raise ValueError('Stale executed correction input: '+path)
    cases={r['id']:r for r in report['cases']}
    if len(cases)!=36 or any(r['status']!='PASS' for r in cases.values()):raise ValueError('Lost/failing correction case')
    if set().union(*map(set,GROUPS.values()))!=set(cases):raise ValueError('Lost requirement/case trace')
    semantic={r['id'] for r in json.loads((ROOT/'requirements/requirements.json').read_text())}
    trace=[]
    for req in policy['requirements']:
        if not set(req['source_requirements']).issubset(semantic):raise ValueError('Unknown requirement source')
        trace.append(dict(requirement=req,implementation=['assessment_correction','relational_correction.py'],case_ids=GROUPS[req['id']],status='SCOPED_EXECUTED',acceptance='Engineering oracle match; not full original ORSD/constraint or independent acceptance'))
    rows=baseline['rows']
    if len(rows)!=306 or len({r['id'] for r in rows})!=306:raise ValueError('Native accounting missing/duplicated')
    model=json.loads((ROOT/'ontology/riskium-model.json').read_text())
    source={r['id']:r for family in ('concepts','imported_types','associations','generalizations','constraints') for r in model[family]}
    for row in rows:
        actual=hashlib.sha256(json.dumps(source[row['id']],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
        if actual!=row['source_sha256']:raise ValueError('Stale source element '+row['id'])
    inventory=dict(schema='riskium-correction-source-accounting-v1',profile='0.3.0',baseline_path=baseline_path,baseline_sha256=sha(baseline_path),summary=baseline['summary'],new_native_classes=0,new_native_predicates=0,full_mapping_completed=False,
      rows=[dict(r,correction_overlay='SELECTED_APPLICATION_HISTORY_ONLY' if r['id'] in ('C-03','C-17') else 'NO_ADDITIONAL_NATIVE_MAPPING') for r in rows])
    inputs=set(report['inputs_sha256'])|set(policy['source_sha256'])|{baseline_path,'tools/build_correction_inventory.py','tests/test_relational_correction.py','implementation/relational/0.3.0/README.md','implementation/relational/0.3.0/schema-dictionary.md','evaluation/relational/correction/report.json','evaluation/relational/correction/README.md'}
    trace_doc=dict(schema='riskium-correction-requirement-trace-v1',profile='0.3.0',original_drsd_unchanged='0.1.0',requirements=trace,input_sha256={p:sha(p) for p in sorted(inputs)})
    # These generated accounting bytes are component inputs too; avoid a self hash.
    accounting=encoded(inventory);trace_text=encoded(trace_doc)
    files={p:sha(p) for p in sorted(inputs)}
    for name,data in [('evaluation/relational/correction/mapping-accounting.json',accounting),('evaluation/relational/correction/traceability.json',trace_text)]:files[name]=hashlib.sha256(data.encode()).hexdigest()
    component=dict(schema='riskium-sql-correction-component-v1',id='SQL_ASSESSMENT_CORRECTION',version='0.3.0',schema_version=4,compatible_model='0.3.1',baseline_sql_profile='0.2.0',published_distribution_selected=False,status='POST_RELEASE_DEVELOPMENT_SUPPLEMENT',files_sha256=files,summary=report['summary'],source_accounting=baseline['summary'])
    return {'evaluation/relational/correction/mapping-accounting.json':accounting,'evaluation/relational/correction/traceability.json':trace_text,'implementation/relational/0.3.0/component.json':encoded(component)}


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    for name,data in build().items():
        target=ROOT/name
        if args.check:
            if not target.exists() or target.read_text()!=data:raise ValueError('Stale correction accounting: '+name)
        else:target.parent.mkdir(parents=True,exist_ok=True);target.write_text(data)
    print(encoded(dict(status='CORRECTION_ACCOUNTING_PASS',native_elements=306,new_native_mappings=0,requirements=5)))

if __name__=='__main__':main()
