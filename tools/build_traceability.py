"""Reconcile public requirement/CQ identities and evidence without declaring full acceptance."""
from pathlib import Path
from collections import Counter
import argparse, csv, gzip, json, subprocess
from run_cq import ROOT, SEMANTIC_COMMIT, EVIDENCE_BASE, sha, object_digest, dump, run, verify

PUBLIC_BASE='5dcd74b838d9986a480df2d2460c6bd4b7f65afd'
OUT=ROOT/'evaluation/traceability'
SOURCE_FILES=['requirements/requirements.json','requirements/scope-requirements.json','requirements/competency-questions.json']

def render():
    inputs={}
    def read(path):
        data=(ROOT/path).read_bytes();inputs[path]=sha(data);return data
    def js(path):return json.loads(read(path))
    model=js('ontology/riskium-model.json')
    requirements,scopes,cqs=[js(p) for p in SOURCE_FILES]
    objects={x['id']:x for group in ['concepts','associations','generalizations','constraints','imported_types','domains'] for x in model[group]}
    sources={x['id']:x for group in [requirements,scopes,cqs] for x in group}
    if len(requirements)!=12 or len(scopes)!=8 or len(cqs)!=8 or len(sources)!=28:raise ValueError('Public source allocation changed')
    plan=js('requirements/traceability-plan.json')
    if len(plan['requirements_and_scope'])!=20 or {r['id'] for r in plan['requirements_and_scope']}!={x['id'] for x in requirements+scopes}:raise ValueError('Requirement/scope trace plan incomplete or duplicated')
    review=js('evaluation/coverage-review.json');contract=js('evaluation/coverage-contract.json')
    h=js('evaluation/hermit/report.json');s=js('evaluation/shacl/coverage-status.json')
    for path in ['evaluation/hermit/report.json','evaluation/shacl/coverage-status.json']:
        if (ROOT/path).read_bytes()!=subprocess.check_output(['git','show',EVIDENCE_BASE+':'+path],cwd=ROOT):raise ValueError('Historical evidence changed; requires a separate reviewed execution update: '+path)
    read('ontology/derived/riskium.owl.ttl')
    if h['inputs']['owl_turtle_sha256']!=inputs['ontology/derived/riskium.owl.ttl'] or s['source_sha256']!=inputs['ontology/riskium-model.json']:raise ValueError('Engine receipt input mismatch')
    if len(review['obligation_reviews'])!=674 or contract['source_model_sha256']!=inputs['ontology/riskium-model.json']:raise ValueError('Coverage planning baseline changed')
    combined={x['source_element']:x for x in review['obligation_reviews'] if x['engine']=='Combined'}
    for item in requirements+cqs:
        if item['id'] not in combined or combined[item['id']]['source_element_sha256']!=object_digest(item):raise ValueError('Stale baseline requirement/CQ identity: '+item['id'])
    # Independently read old receipts; this tool does not execute formal engines.
    archived={'evaluation/hermit/report.json':h}
    for receipt in s['evidence']:
        data=read(receipt['path'])
        if sha(data)!=receipt['sha256']:raise ValueError('Historical receipt digest mismatch: '+receipt['path'])
        archived[receipt['path']]=json.loads(gzip.decompress(data) if receipt['path'].endswith('.gz') else data)
    for row in h['obligations']:
        case_ids=[i.strip() for i in row.get('case_id','').split(',') if i.strip()]
        actual={c['id'] for c in h['cases']}
        if not set(case_ids)<=actual:raise ValueError('Unknown referenced HermiT case')
    for row in s['obligations']:
        if row.get('case_ids'):
            if row['evidence'] not in archived:raise ValueError('Unknown SHACL evidence file')
            if not set(row['case_ids'])<={c['id'] for c in archived[row['evidence']]['cases']}:raise ValueError('Unknown referenced SHACL case')
    cq=js('evaluation/cq/report.json');verify(cq,run())
    cq_rows={c['cq_id']:c for c in cq['contracts']}
    for path in ['evaluation/owl-mapping-receipt.json','evaluation/native-exchange-checks.json','evaluation/c14-boundary-review.json','evaluation/shacl/admission/report-index.json','tools/build_traceability.py']:
        read(path)
    if cq['status']!='PASS':raise ValueError('Query execution receipt failed')
    # Reconcile retained public identities only. No restricted acquisition data
    # or hidden legacy claims are fetched, imported or guessed.
    history=[]
    for path in SOURCE_FILES+['ontology/riskium-model.json']:
        original_bytes=subprocess.check_output(['git','show',PUBLIC_BASE+':'+path],cwd=ROOT)
        original=json.loads(original_bytes);current=model if path.startswith('ontology/') else js(path)
        groups=['concepts','associations','generalizations','constraints','imported_types','domains'] if isinstance(original,dict) else [None]
        for group in groups:
            before={x['id']:x for x in original[group] if 'id' in x} if group else {x['id']:x for x in original}
            after={x['id']:x for x in current[group] if 'id' in x} if group else {x['id']:x for x in current}
            if set(before)!=set(after):raise ValueError('Public identity gained/lost without a separate reviewed disposition: '+path)
            for ident in sorted(before):
                a,b=object_digest(before[ident]),object_digest(after[ident])
                history.append({'id':ident,'source_file':path,'group':group,'first_public_sha256':a,'current_sha256':b,'disposition':'RETAINED_UNCHANGED' if a==b else 'RETAINED_REVISED_PUBLIC_RECORD'})
    historical={'first_public_commit':PUBLIC_BASE,'current_semantic_commit':SEMANTIC_COMMIT,'evidence_base_commit':EVIDENCE_BASE,'scope':'Only retained public identities from the first public repository import; pre-public private requirements/CQs and historical test counts remain outside the claim.','summary':{'requirement_scope_cq_ids':28,'model_ids':len(history)-28,'unreconciled_public_ids':0,'dispositions':dict(Counter(r['disposition'] for r in history))},'identities':history}
    all_rows=[];by_req={r['id']:r for r in plan['requirements_and_scope'] if r['id'].startswith('RKRS-')}
    def evidence(elements,constraints):
        selected=set(elements)|set(constraints);result=[]
        for row in h['obligations']:
            if row['source_element'] in selected:
                case_ids=[v.strip() for v in row.get('case_id','').split(',') if v.strip()]
                result.append({'engine':'HermiT','id':row['id'],'source_element':row['source_element'],'recorded_outcome':row['outcome'],'scope':row.get('scope',row.get('reason','Mapping/element obligation; not requirement acceptance')),'receipt':'evaluation/hermit/report.json','case_ids':case_ids})
        for row in s['obligations']:
            element=row['source_element'];key=element.split(':',1)[0]
            if element in selected or key in selected:
                result.append({'engine':'SHACL','id':row['id'],'source_element':element,'recorded_outcome':row['outcome'],'scope':'Recorded module obligation only; not whole-requirement acceptance','receipt':row.get('evidence'),'case_ids':row.get('case_ids',[])})
        return result
    for item in plan['requirements_and_scope']:
        source=sources[item['id']];elements=set(item['model_elements']);constraints=set(source.get('constraint_ids',[]))
        for rid in item.get('requirement_ids',[]):
            if rid not in by_req:raise ValueError('Unknown linked requirement')
            elements.update(by_req[rid]['model_elements']);constraints.update(sources[rid]['constraint_ids'])
        if not elements<=objects.keys() or not constraints<=objects.keys() or not set(item['cq_ids'])<=cq_rows.keys():raise ValueError('Unknown model/constraint/CQ link: '+item['id'])
        if not item['mapping_rationale'] or not item['remaining_obligation'] or not item['follow_up_issues']:raise ValueError('Missing trace justification/gap owner')
        if 'ACCEPTED' in item['acceptance_state'] or item['acceptance_state']=='PASS':raise ValueError('Full acceptance cannot be inferred from this trace tool')
        all_rows.append({'id':item['id'],'kind':'requirement' if item['id'].startswith('RKRS-') else 'scope','title':source['title'],'source_file':SOURCE_FILES[0] if item['id'].startswith('RKRS-') else SOURCE_FILES[1],'source_element_sha256':object_digest(source),'baseline_obligation':combined.get(item['id'],{}).get('obligation_id'),'outside_674_baseline':item['id'].startswith('RKM-SCOPE-'),'acceptance_criterion':source['acceptance_criterion'],'negative_acceptance_criterion':source['negative_acceptance_criterion'],'trace_status':'COMPLETE','acceptance_state':item['acceptance_state'],'mapping_rationale':item['mapping_rationale'],'model_elements':[{'id':ident,'sha256':object_digest(objects[ident])} for ident in sorted(elements)],'constraint_ids':sorted(constraints),'query_case_ids':[case for qid in item['cq_ids'] for case in cq_rows[qid]['case_ids']],'formal_evidence':evidence(elements,constraints),'remaining_obligation':item['remaining_obligation'],'follow_up_issues':item['follow_up_issues']})
    for source in cqs:
        c=cq_rows[source['id']]
        all_rows.append({'id':source['id'],'kind':'competency_question','title':source['question'],'source_file':SOURCE_FILES[2],'source_element_sha256':object_digest(source),'baseline_obligation':combined[source['id']]['obligation_id'],'outside_674_baseline':False,'acceptance_criterion':source['expected_result'],'negative_acceptance_criterion':source['rejection'],'original_population':source['population'],'source_population_execution':c['source_population_execution'],'trace_status':'COMPLETE','acceptance_state':'BOUNDED_SYNTHETIC_QUERY_EXECUTED' if c['source_population_execution']=='EXECUTED_SYNTHETIC_QUERY_CONTRACT' else 'INDEPENDENT_POPULATION_NOT_RUN_SYNTHETIC_CONTROL_ONLY','model_elements':[{'id':ident,'sha256':object_digest(objects[ident])} for ident in c['model_elements']],'query_case_ids':c['case_ids'],'query_receipt':'evaluation/cq/report.json','query_scope':c['answer_scope'],'formal_evidence':evidence(c['model_elements'],[]),'remaining_obligation':c['uncovered_obligation'],'follow_up_issues':[5,7,12,13]})
    if len(all_rows)!=28 or {r['id'] for r in all_rows}!=sources.keys():raise ValueError('Trace ledger is not a 28-row bijection')
    ledger={'version':'0.1.0','semantic_source_commit':SEMANTIC_COMMIT,'evidence_base_commit':EVIDENCE_BASE,'input_sha256':inputs,'summary':{'trace_rows':28,'requirements_traced':12,'scope_obligations_traced':8,'cq_contracts_traced':8,'combined_baseline_rows_reconciled':20,'scope_rows_outside_674_baseline':8,'trace_complete':28,'query_executions':cq['summary']['query_executions'],'source_synthetic_contracts_executed':5,'independent_population_contracts_pending':3,'full_requirement_acceptance_claimed':False,'acceptance_states':dict(Counter(r['acceptance_state'] for r in all_rows))},'rows':all_rows,'limits':['Trace completeness is source/evidence accounting, not an ontology semantic-correctness or requirement-acceptance percentage.','Original source JSON/CSV and the 674-row coverage plan retain historical planning states; this separate ledger reports current evidence.','Eight supplementary scope rows are not added to the 674-row baseline or HermiT/SHACL denominators.','The eight query contracts have 32 fixed synthetic answer cases plus eight detected query mutants; CQ06-CQ08 still lack their declared independent population.','Native numeric, source-locator and general correction-lineage adequacy gaps are explicit; supplementary fields do not silently extend the core.','Independent meaning/source review, actual immutable history, computation/readiness and real case/CQ acceptance remain assigned to existing #5/#7/#8/#11/#12/#13 issues.','Archived formal evidence is linked and verified, not rerun or relabeled as new tests.']}
    md='# Requirement and competency-question traceability\n\n'
    md+='Conceptual design 0.3.1; semantic source `'+SEMANTIC_COMMIT+'`. This post-prerelease author trace review completes #6 as **evidence reconciliation**, not full requirement or independent scientific acceptance.\n\n'
    md+='All **12 requirements, eight scope obligations and eight CQs** have source hashes, exact model identifiers, acceptance/rejection criteria, current evidence and named remaining routes. The 20 Combined baseline identities are reconciled; eight scope rows remain outside the 674-row denominator.\n\n'
    md+='Eight query contracts executed **40 local SPARQL queries: 32 fixed answer cases and eight successfully executed, detected query mutants**. Five original synthetic-task contracts now have bounded execution. CQ06–CQ08 have synthetic controls only; their declared independent evidence-preservation population remains NOT_RUN in #13. Query execution does not prove native-only adequacy or real-data acceptance.\n\n'
    md+='| ID | Subject | Current acceptance/evidence state | Remaining work |\n| --- | --- | --- | --- |\n'
    for row in all_rows:md+='| '+row['id']+' | '+row['title'].replace('|','/')+' | '+row['acceptance_state']+' | '+row['remaining_obligation'].replace('|','/')+' |\n'
    md+='\n## Evidence and reproduction\n\nThe [full ledger](ledger.json) retains source hashes, original criteria, exact model element hashes, baseline IDs and historical formal receipt/case IDs. [Public identity continuity](historical-identities.json) reconciles '+str(len(history))+' retained public identities ('+str(len(history)-28)+' model/domain elements plus 28 requirement/scope/CQ records) from the first public import. Restricted acquisition records and pre-public denominators are not copied or claimed reconciled.\n\n'
    md+='The [CQ receipt](../cq/report.json), [contract/oracle files](../../requirements/cq/contracts.json), [named fixtures](../cq/fixtures.trig), [eight SELECT queries](../../requirements/cq/queries), [query mutants](../../requirements/cq/mutants) and [supplementary data policy](../../requirements/cq/profile.json) are separately inspectable. Values/locators/correction metadata outside the core are explicitly identified. All populations are synthetic; independent literature data preparation and expert acceptance remain #13/#7.\n\n'
    md+='```sh\npython3 -m venv .venv-owl\n.venv-owl/bin/pip install -r tools/requirements-owl.txt\n.venv-owl/bin/python tools/run_cq.py --check\n.venv-owl/bin/python tools/build_traceability.py --check\n```\n\n'
    md+='Use `--write` only after reviewing an intentional input/oracle change. The query receipt records execution time, Python/RDFLib versions, per-case expected/observed rows, graph snapshots, query hashes and the declared inference policy. A query error never counts as a detected mutant. Negative and conflicting fixtures are retrieval tests, not claims that those graphs satisfy managed admission. Missing asserted values are not logical negation.\n\n'
    md+='Historical HermiT coverage remains **281/295, 14 NOT_RUN**. SHACL remains **341 scoped PASS, 1 PARTIAL, 17 NOT_RUN / 359**. Report sizes, test counts and the 28-row trace denominator are separate from semantic correctness.\n'
    return {'ledger.json':dump(ledger),'historical-identities.json':dump(historical),'README.md':md}

def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group();g.add_argument('--write',action='store_true');g.add_argument('--check',action='store_true');args=p.parse_args();outputs=render()
    OUT.mkdir(parents=True,exist_ok=True)
    for name,content in outputs.items():
        path=OUT/name
        if args.write:path.write_text(content)
        elif not path.exists() or path.read_text()!=content:raise SystemExit('Stale trace output; review before --write: '+name)
    print(json.dumps({'status':'PASS','trace_rows':28,'combined_baseline_identities':20,'separate_scope_rows':8,'full_requirement_acceptance':False}))

if __name__=='__main__':main()
