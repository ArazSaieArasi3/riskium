"""Execute fixed synthetic CQ answer oracles and independently stored query mutants."""
from pathlib import Path
from collections import Counter
import argparse, hashlib, importlib.metadata, json, re, subprocess, sys
from datetime import datetime, timezone
from rdflib import Dataset, Graph, URIRef, OWL, RDF

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evaluation/cq/report.json'
SEMANTIC_COMMIT='cfb85905ab37549c7090f00a41ca62cdd3364ab5'
EVIDENCE_BASE='098f8249394756333801d216de7f5eed63fb2ef1'
RISK='https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'

def sha(data):return hashlib.sha256(data).hexdigest()
def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def dump(value):return json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False)+'\n'
def ordered(rows):return sorted(rows,key=encoded)
def object_digest(value):return sha(encoded(value).encode())

def execute(graph,query,columns):
    # Local, read-only SELECT evaluation only; no graph loading or remote service.
    if re.search(r'\b(SERVICE|FROM|LOAD|INSERT|DELETE|CLEAR|DROP|CREATE|MOVE|COPY|ADD)\b',query,re.I):
        raise ValueError('Non-local or non-read query')
    result=graph.query(query)
    if result.type!='SELECT' or list(map(str,result.vars))!=columns:
        raise ValueError('Unexpected query result type or column order')
    return ordered([[None if value is None else value.n3() for value in row] for row in result])

def run():
    inputs={}
    def read(path):
        data=(ROOT/path).read_bytes();inputs[path]=sha(data);return data
    model=json.loads(read('ontology/riskium-model.json'))
    for path in ['ontology/riskium-model.json','ontology/derived/riskium.owl.ttl']:
        current=read(path);frozen=subprocess.check_output(['git','show',SEMANTIC_COMMIT+':'+path],cwd=ROOT)
        if current!=frozen:raise ValueError('Semantic input differs from the declared release: '+path)
    owl=Graph().parse(data=read('ontology/derived/riskium.owl.ttl').decode(),format='turtle')
    plan=json.loads(read('requirements/cq/contracts.json'));profile=json.loads(read('requirements/cq/profile.json'))
    original=json.loads(read('requirements/competency-questions.json'))
    if {c['cq_id'] for c in plan['contracts']}!={c['id'] for c in original} or len(plan['contracts'])!=8:
        raise ValueError('CQ contract allocation differs from the eight source questions')
    if importlib.metadata.version('rdflib')!='7.6.0':raise ValueError('Use pinned RDFLib 7.6.0')
    read('tools/requirements-owl.txt');read('tools/run_cq.py')
    data=Dataset();data.parse(data=read(plan['fixture_file']).decode(),format='trig')
    ids={c['id'] for c in model['concepts']+model['imported_types']+model['associations']+model['generalizations']+model['constraints']}
    expected_graphs={case['graph'] for c in plan['contracts'] for case in c['cases']}
    if {str(g.identifier) for g in data.graphs() if len(g)}!=expected_graphs or len(expected_graphs)!=32:
        raise ValueError('Fixture graph allocation differs from the 32 declared cases')
    for graph in data.graphs():
        for s,p,o in graph:
            for value in [p,o if p==RDF.type else None]:
                if isinstance(value,URIRef) and str(value).startswith(RISK):
                    if value not in set(owl.subjects(RDF.type,OWL.Class))|set(owl.subjects(RDF.type,OWL.ObjectProperty)):
                        raise ValueError('Undeclared native term in fixture: '+str(value))
            for value in [p,o if p==RDF.type else None]:
                if isinstance(value,URIRef) and str(value).startswith(profile['namespace']) and str(value).removeprefix(profile['namespace']) not in profile['terms']:
                    raise ValueError('Undeclared supplementary field')
    sources={c['id']:c for c in original};results=[];contracts=[];snapshots={}
    for contract in plan['contracts']:
        cq=contract['cq_id']
        if len(contract['model_elements'])!=len(set(contract['model_elements'])) or not set(contract['model_elements'])<=ids:
            raise ValueError('Unknown or duplicate source model element: '+cq)
        queries={k:read(contract[k]).decode() for k in ['query','mutant_query']}
        for query in queries.values():
            native_terms=set(re.findall(r'\brisk:([\w-]+)',query))
            if any((URIRef(RISK+term),None,None) not in owl for term in native_terms):raise ValueError('Undeclared native query term: '+cq)
            if not native_terms<=set(contract['model_elements']):raise ValueError('Untraced native query term: '+cq)
        if {x['kind'] for x in contract['cases']}!={'positive','negative','incomplete','conflicting'} or len(contract['cases'])!=4:
            raise ValueError('Incomplete scenario allocation: '+cq)
        for spec in contract['cases']+[dict(contract['mutation_control'],kind='query_mutant')]:
            graph=data.graph(URIRef(spec['graph']))
            snapshot='\n'.join(sorted(graph.serialize(format='nt').splitlines()))+'\n'
            key=sha(snapshot.encode());snapshots[key]=snapshot
            expected=ordered(spec['expected_rows'])
            if any(len(row)!=len(contract['columns']) for row in expected):raise ValueError('Malformed expected oracle')
            if spec['kind']=='query_mutant' and expected!=ordered(contract['cases'][0]['expected_rows']):raise ValueError('Mutation must use unchanged positive answer oracle')
            if spec['kind']=='query_mutant' and spec['graph']!=contract['cases'][0]['graph']:raise ValueError('Mutation must use unchanged positive graph')
            query_path=contract['mutant_query' if spec['kind']=='query_mutant' else 'query']
            try:
                observed=execute(graph,queries['mutant_query' if spec['kind']=='query_mutant' else 'query'],contract['columns'])
                matched=Counter(map(encoded,observed))==Counter(map(encoded,expected))
                success=not matched if spec['kind']=='query_mutant' else matched
                status='PASS' if success else 'FAIL';error=None
            except Exception as exc:
                observed=None;matched=False;status='ERROR';error=type(exc).__name__+': '+str(exc)
            results.append({'id':spec['id'],'cq_id':cq,'kind':spec['kind'],'status':status,'query_path':query_path,'query_sha256':inputs[query_path],'fixture_graph':spec['graph'],'fixture_sha256':key,'columns':contract['columns'],'expected_rows':expected,'observed_rows':observed,'oracle_matched':matched,'expected_behavior':'DIFFERENT_FROM_ORACLE' if spec['kind']=='query_mutant' else 'EXACT_ORACLE_MATCH','error':error})
        contracts.append({'cq_id':cq,'source_cq_sha256':object_digest(sources[cq]),'answer_scope':contract['answer_scope'],'model_elements':contract['model_elements'],'execution_status':'PASS' if all(r['status']=='PASS' for r in results if r['cq_id']==cq) else 'FAIL','case_ids':[r['id'] for r in results if r['cq_id']==cq],'source_population_execution':'EXECUTED_SYNTHETIC_QUERY_CONTRACT' if sources[cq]['population']=='Synthetic design task' else 'NOT_RUN_ON_DECLARED_INDEPENDENT_POPULATION','independent_or_real_data_acceptance':'NOT_ESTABLISHED','uncovered_obligation':contract['uncovered_obligation']})
    return {'schema_version':1,'profile_version':plan['version'],'semantic_source_commit':SEMANTIC_COMMIT,'evidence_base_commit':EVIDENCE_BASE,'source_note':'The semantic/evidence commits identify existing inputs; new query implementation and fixtures are pinned separately by their file hashes. Publication commit is recorded in issue #6.','model_version':model['version'],'input_sha256':inputs,'population':plan['population'],'inference':plan['inference'],'engine':{'name':'RDFLib SPARQL SELECT','version':importlib.metadata.version('rdflib')},'summary':{'contracts':len(contracts),'contracts_with_matching_bounded_tests':sum(c['execution_status']=='PASS' for c in contracts),'source_synthetic_task_contracts_executed':sum(c['source_population_execution']=='EXECUTED_SYNTHETIC_QUERY_CONTRACT' for c in contracts),'independent_population_contracts_pending':sum(c['source_population_execution']=='NOT_RUN_ON_DECLARED_INDEPENDENT_POPULATION' for c in contracts),'query_attempts':len(results),'query_executions':sum(r['observed_rows'] is not None for r in results),'answer_cases':sum(r['kind']!='query_mutant' for r in results),'mutation_controls':sum(r['kind']=='query_mutant' for r in results),'mutants_detected':sum(r['kind']=='query_mutant' and r['status']=='PASS' for r in results),'statuses':dict(Counter(r['status'] for r in results))},'status':'PASS' if all(r['status']=='PASS' for r in results) else 'FAIL','contracts':contracts,'graphs':snapshots,'cases':results,'limitations':['All answer fixtures are synthetic author tests; this does not replace independently prepared literature data or expert acceptance.','Queries retrieve asserted graph bindings without identity normalization, inference, managed-record conformance or truth adjudication.','Supplementary numeric/provenance/revision metadata are explicitly separate from the original OWL; native-only adequacy gaps remain recorded.','A mutated query must run successfully and disagree with the fixed positive oracle; parser errors do not count as detected mutations.','No HermiT, SHACL or 674-row planning baseline result is rewritten or increased by this query run.']}

def verify(receipt,current):
    recorded=receipt.copy();recorded.pop('recorded_execution',None)
    if recorded!=current:raise ValueError('CQ receipt is stale or its outcomes/inputs changed; review before --write')

def main():
    parser=argparse.ArgumentParser(description=__doc__);group=parser.add_mutually_exclusive_group();group.add_argument('--write',action='store_true');group.add_argument('--check',action='store_true');args=parser.parse_args()
    result=run()
    if args.write:
        result['recorded_execution']={'at_utc':datetime.now(timezone.utc).isoformat(),'command':'.venv-shacl/bin/python tools/run_cq.py --write','python':sys.version,'exit_code':0 if result['status']=='PASS' else 1}
        OUT.write_text(dump(result))
    elif args.check:verify(json.loads(OUT.read_text()),result)
    print(dump({'status':result['status'],'summary':result['summary'],'failures':[{k:r[k] for k in ['id','status','expected_rows','observed_rows','error']} for r in result['cases'] if r['status']!='PASS']}))
    if result['status']!='PASS':raise SystemExit(1)

if __name__=='__main__':main()
