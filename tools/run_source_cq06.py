"""Replay source-backed CQ06 joins against a previously frozen source/answer cohort."""
import argparse
from collections import Counter
from datetime import datetime,timezone
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
from rdflib import Graph,URIRef,Literal,RDF,DCTERMS
from run_cq import execute,ordered,encoded

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evaluation/sources/cq06'
FREEZE='2542c5b0762c4390c2d5af132fe52a01249fe2fc'
BASE='urn:riskium:source-cq06:'
RISK='https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'
APP='urn:riskium:source-cq-profile:0.2.0#'
CAND=URIRef('https://github.com/ArazSaieArasi3/riskium/profiles/catalog/0.3.0#candidate')
ORIGIN=URIRef(BASE+'origin:assistant-paraphrase-reviewed-against-pdf')
COLS=['statement','source','locator','origin']
INPUTS=['ontology/riskium-model.json','ontology/derived/riskium.owl.ttl','evaluation/cq/report.json',
 'evaluation/sources/cq06/cohort.json','evaluation/sources/cq06/inspection.json','evaluation/sources/cq06/expected.json',
 'evaluation/sources/cq06/profile.json','evaluation/sources/cq06/query.rq',
 'evaluation/sources/cq06/mutants/cross-record.rq','evaluation/sources/cq06/mutants/reversed-native.rq',
 'evaluation/sources/cq06/mutants/missing-origin.rq','tools/run_cq.py','tools/run_source_cq06.py','tools/requirements-owl.txt']
U=lambda s:URIRef(BASE+s)
P=lambda s:URIRef(APP+s)
N=lambda s:URIRef(RISK+s)
sha=lambda b:hashlib.sha256(b).hexdigest()


def inputs():
    cohort=json.loads((OUT/'cohort.json').read_text());expected=json.loads((OUT/'expected.json').read_text());inspection=json.loads((OUT/'inspection.json').read_text())
    for name in ('cohort.json','expected.json','inspection.json'):
        if (OUT/name).read_bytes()!=subprocess.check_output(['git','show',FREEZE+':evaluation/sources/cq06/'+name],cwd=ROOT):
            raise ValueError('CQ06 frozen source/oracle changed: '+name)
    if inspection['cohort_sha256']!=sha((OUT/'cohort.json').read_bytes()):raise ValueError('CQ06 inspection binding differs')
    if len(cohort['records'])!=13 or len(expected['joins'])!=13 or len({r['id'] for r in cohort['records']})!=13:raise ValueError('CQ06 population differs')
    if [r['id'] for r in cohort['records'] if r['case_admission']=='WITHHELD']!=expected['withheld_case_ids'] or len(expected['withheld_case_ids'])!=11:raise ValueError('CQ06 withheld admission differs')
    if any(r['risk_case_identity'] is not None or r['occurrence_asserted'] for r in cohort['records']):raise ValueError('CQ06 case/occurrence promotion')
    sources={s['id']:s for s in cohort['sources']}
    actual={r['id']:(sources[r['source_id']]['uri'],r['locator'],r['interpretation_origin']) for r in cohort['records']}
    fixed={rid:(source,locator,expected['origin']) for rid,source,locator in expected['joins']}
    if actual!=fixed or expected['columns']!=COLS:raise ValueError('CQ06 cohort differs from independent answer vector')
    for s in cohort['sources']:
        saved=next(x for x in inspection['source_pdfs'] if x['id']==s['id'])
        if any(saved[k]!=s[k] for k in ('pdf_sha256','pdf_pages','inspected_pdf_pages','page_text_hashes')):raise ValueError('CQ06 PDF binding differs')
    return cohort,expected,inspection


def base(cohort,ids):
    g=Graph();sources={s['id']:s for s in cohort['sources']}
    for r in cohort['records']:
        if r['id'] not in ids:continue
        rid=r['id'];record=U('record:'+rid);ref=U('reference:'+rid);statement=U('statement:'+rid);item=U('evidence:'+r['evidence_id']);source=URIRef(sources[r['source_id']]['uri'])
        for subject,cls in ((ref,'RKM-C065'),(ref,'RKM-C014'),(statement,'RKM-C014'),(item,'RKM-C066'),(item,'RKM-C014')):g.add((subject,RDF.type,N(cls)))
        for triple in [(record,CAND,ref),(record,P('statement'),statement),(record,P('evidenceItem'),item),
            (record,DCTERMS.source,source),(record,P('sourceLocator'),Literal(r['locator'])),(record,P('interpretationOrigin'),URIRef(r['interpretation_origin'])),
            (ref,N('R-68'),statement),(ref,N('RX-021'),item),(item,DCTERMS.source,source),(item,P('sourceLocator'),Literal(r['locator'])),
            (statement,DCTERMS.description,Literal(r['paraphrase']))]:g.add(triple)
    return g


def fixed_rows(expected,ids):
    return ordered([[U('statement:'+rid).n3(),URIRef(source).n3(),Literal(locator).n3(),URIRef(expected['origin']).n3()]
        for rid,source,locator in expected['joins'] if rid in ids])


def findings(g,cohort,ids,check_frozen=True):
    results=[];known={r['id']:r for r in cohort['records']};sources={s['id']:s for s in cohort['sources']}
    expected_records={U('record:'+rid) for rid in ids}
    if set(g.subjects(CAND,None))!=expected_records:results.append('RECORD_POPULATION')
    for rid in ids:
        r=known[rid];record=U('record:'+rid);ref=U('reference:'+rid);item=U('evidence:'+r['evidence_id']);statement=U('statement:'+rid)
        checks=[(record,CAND,[ref],'REFERENCE'),(record,P('statement'),[statement],'STATEMENT_ENVELOPE'),(record,P('evidenceItem'),[item],'ITEM_ENVELOPE'),
            (ref,N('R-68'),[statement],'NATIVE_STATEMENT'),(ref,N('RX-021'),[item],'NATIVE_ITEM'),
            (ref,RDF.type,[N('RKM-C065'),N('RKM-C014')],'REFERENCE_TYPE'),(item,RDF.type,[N('RKM-C066'),N('RKM-C014')],'EVIDENCE_TYPE'),(statement,RDF.type,[N('RKM-C014')],'STATEMENT_TYPE')]
        for subject,predicate,wanted,code in checks:
            if set(g.objects(subject,predicate))!=set(wanted):results.append(rid+':'+code)
        for subject,role in ((record,'RECORD'),(item,'EVIDENCE')):
            for pred,wanted,code in [(DCTERMS.source,URIRef(sources[r['source_id']]['uri']),'SOURCE'),(P('sourceLocator'),Literal(r['locator']),'LOCATOR')]:
                values=list(g.objects(subject,pred))
                if len(values)!=1:results.append(rid+':'+role+'_'+code+'_CARDINALITY')
                elif check_frozen and values!=[wanted]:results.append(rid+':'+role+'_'+code+'_FROZEN')
        origin=list(g.objects(record,P('interpretationOrigin')))
        if origin!=[URIRef(r['interpretation_origin'])]:results.append(rid+':ORIGIN')
    for subject,cls in g.subject_objects(RDF.type):
        if cls in {N('RKM-X01'),N('RKM-C003')}:results.append('CASE_OR_SCENARIO_PROMOTION')
    return sorted(results)


def specs(cohort,expected):
    ids=[r['id'] for r in cohort['records']];first=ids[0];allrows=fixed_rows(expected,ids);one=fixed_rows(expected,[first]);prefix=first+':'
    result=[dict(id='SOURCED-COHORT-13',ids=ids,action=None,query='query.rq',expected_rows=allrows,expected_findings=[],kind='source-query')]
    result += [dict(id='SOURCED-'+rid,ids=[rid],action=None,query='query.rq',expected_rows=fixed_rows(expected,[rid]),expected_findings=[],kind='source-query') for rid in ids]
    def add(cid,action,rows,codes,kind='synthetic-negative'):
        result.append(dict(id=cid,ids=[first],action=action,query='query.rq',expected_rows=rows,expected_findings=[prefix+c for c in codes],kind=kind))
    add('MISSING-SOURCE','missing-source',[],['RECORD_SOURCE_CARDINALITY'])
    add('MISSING-LOCATOR','missing-locator',[],['RECORD_LOCATOR_CARDINALITY'])
    add('MISSING-ORIGIN','missing-origin',[],['ORIGIN'])
    add('CROSS-SOURCE-RECORD','wrong-source',[],['RECORD_SOURCE_FROZEN'])
    add('CROSS-RECORD-EVIDENCE','wrong-item',[],['NATIVE_ITEM'])
    add('CROSS-RECORD-STATEMENT','wrong-statement',[],['NATIVE_STATEMENT'])
    add('MISSING-NATIVE-SUPPORT','missing-support',[],['NATIVE_STATEMENT'])
    add('MISSING-NATIVE-EVIDENCE','missing-evidence',[],['NATIVE_ITEM'])
    add('WRONG-LOCATOR','wrong-locator',[],['RECORD_LOCATOR_FROZEN'])
    add('MULTIPLE-SOURCES-REMAIN-VISIBLE','multiple-source',one,['RECORD_SOURCE_CARDINALITY'])
    changed=[list(one[0])];changed[0][1]=URIRef('https://doi.org/10.1186/2008-2231-21-69').n3()
    add('COHERENT-FORGED-SOURCE-IS-REJECTED','coherent-source',changed,['EVIDENCE_SOURCE_FROZEN','RECORD_SOURCE_FROZEN'])
    changed=[list(one[0])];changed[0][2]=Literal('Uninspected location').n3()
    add('COHERENT-FORGED-LOCATOR-IS-REJECTED','coherent-locator',changed,['EVIDENCE_LOCATOR_FROZEN','RECORD_LOCATOR_FROZEN'])
    changed=one+[[*one[0][:3],U('origin:unknown').n3()]]
    add('CONFLICTING-ORIGINS-REMAIN-VISIBLE','multiple-origin',ordered(changed),['ORIGIN'])
    add('GUARD-DELETION-EXPOSES-FORGED-SOURCE','coherent-source',[[one[0][0],URIRef('https://doi.org/10.1186/2008-2231-21-69').n3(),*one[0][2:]]],[],kind='guard-mutation')
    for name in ('cross-record','reversed-native','missing-origin'):
        result.append(dict(id='QUERY-MUTANT-'+name.upper(),ids=ids,action=None,query='mutants/'+name+'.rq',expected_rows=allrows,expected_findings=[],kind='query-mutation'))
    result.append(dict(id='EQUAL-DESCRIPTIONS-KEEP-DISTINCT-IDS',ids=ids[:2],action='equal-description',query='query.rq',expected_rows=fixed_rows(expected,ids[:2]),expected_findings=[],kind='identity-control'))
    add('UNTRACKED-RECORD-NOT-ADMITTED','untracked-record',one,[],kind='synthetic-negative')
    result[-1]['expected_findings']=['RECORD_POPULATION']
    for name in ('case','scenario'):
        add('NO-'+name.upper()+'-PROMOTION',name+'-promotion',one,['STATEMENT_TYPE'],kind='synthetic-negative')
        result[-1]['expected_findings'].append('CASE_OR_SCENARIO_PROMOTION')
    return result


def alter(g,s,cohort):
    a=s['action']
    if not a:return
    rid=s['ids'][0];r=next(x for x in cohort['records'] if x['id']==rid);record=U('record:'+rid);ref=U('reference:'+rid);item=U('evidence:'+r['evidence_id'])
    if a.startswith('missing-'):
        subject,pred={'missing-source':(record,DCTERMS.source),'missing-locator':(record,P('sourceLocator')),'missing-origin':(record,P('interpretationOrigin')),'missing-support':(ref,N('R-68')),'missing-evidence':(ref,N('RX-021'))}[a]
        g.remove((subject,pred,None))
    elif a=='wrong-item':g.set((ref,N('RX-021'),U('evidence:EV04-0037')))
    elif a=='wrong-statement':g.set((ref,N('R-68'),U('statement:UPX-MAT-004-002')))
    elif a in ('wrong-source','multiple-source','coherent-source'):
        value=URIRef('https://doi.org/10.1186/2008-2231-21-69')
        if a=='multiple-source':g.add((record,DCTERMS.source,value))
        else:g.set((record,DCTERMS.source,value))
        if a=='coherent-source':g.set((item,DCTERMS.source,value))
    elif a in ('wrong-locator','coherent-locator'):
        g.set((record,P('sourceLocator'),Literal('Uninspected location')))
        if a=='coherent-locator':g.set((item,P('sourceLocator'),Literal('Uninspected location')))
    elif a=='multiple-origin':g.add((record,P('interpretationOrigin'),U('origin:unknown')))
    elif a=='equal-description':
        for identity in s['ids']:g.set((U('statement:'+identity),DCTERMS.description,Literal('Same display text')))
    elif a=='untracked-record':g.add((U('record:untracked'),CAND,ref))
    elif a in ('case-promotion','scenario-promotion'):g.add((U('statement:'+rid),RDF.type,N('RKM-X01' if a=='case-promotion' else 'RKM-C003')))
    else:raise ValueError('Unknown CQ06 fixture edit')


def case(s,cohort,graphs):
    g=base(cohort,s['ids']);alter(g,s,cohort)
    graph='\n'.join(sorted(g.serialize(format='nt').splitlines()))+'\n';key=sha(graph.encode());graphs.setdefault(key,graph)
    faults=findings(g,cohort,s['ids'],check_frozen=s['kind']!='guard-mutation');query=(OUT/s['query']).read_text()
    error=None;observed=None
    try:observed=execute(g,query,COLS)
    except Exception as e:error=type(e).__name__+': '+str(e)
    equal=observed==s['expected_rows'];matched=(not equal if s['kind']=='query-mutation' else equal)
    passed=error is None and matched and faults==sorted(s['expected_findings'])
    return dict(id=s['id'],kind=s['kind'],record_ids=s['ids'],status='PASS' if passed else 'ERROR' if error else 'FAIL',
        query=s['query'],query_sha256=sha(query.encode()),graph_sha256=key,expected_rows=s['expected_rows'],observed_rows=observed,
        oracle_equal=equal,expected_behavior='DIFFERENT_FROM_FIXED_POSITIVE_ORACLE' if s['kind']=='query-mutation' else 'EXACT_RAW_BINDINGS_AND_FINDINGS',
        expected_findings=sorted(s['expected_findings']),observed_findings=faults,validator_admits=not faults,trace_task_accepted=not faults and s['kind'] not in ('query-mutation','guard-mutation'),error=error)


def run():
    cohort,expected,inspection=inputs();graphs={};rows=[case(s,cohort,graphs) for s in specs(cohort,expected)]
    if importlib.metadata.version('rdflib')!='7.6.0':raise ValueError('Use pinned RDFLib 7.6.0')
    model=json.loads((ROOT/'ontology/riskium-model.json').read_text());signature={r['id']:(r['source'],r['target']) for r in model['associations']}
    profile=json.loads((OUT/'profile.json').read_text())
    if any(signature[rid]!=tuple(pair) for rid,pair in profile['native'].items()):raise ValueError('CQ06 native signature changed')
    for path in ('ontology/riskium-model.json','ontology/derived/riskium.owl.ttl','evaluation/cq/report.json'):
        if (ROOT/path).read_bytes()!=subprocess.check_output(['git','show',FREEZE+':'+path],cwd=ROOT):raise ValueError('CQ06 retained historical bytes changed')
    for text in graphs.values():
        for s,p,o in Graph().parse(data=text,format='nt'):
            if str(p).startswith(APP) and str(p)[len(APP):] not in profile['terms']:raise ValueError('Undeclared source CQ06 metadata')
    failures=[r['id'] for r in rows if r['status']!='PASS']
    if failures:raise ValueError('CQ06 oracle failures: '+str([(r['id'],r['observed_findings'],r['expected_findings'],r['error']) for r in rows if r['id'] in failures]))
    return dict(schema='riskium-source-cq06-evidence-v1',source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        source_cohort_freeze_commit=FREEZE,recorded_at_utc=datetime.now(timezone.utc).isoformat(),inputs={p:sha((ROOT/p).read_bytes()) for p in INPUTS},
        engine={'name':'RDFLib SPARQL SELECT','version':importlib.metadata.version('rdflib'),'python':sys.version.split()[0],'inference':'none','remote_service':False},
        summary={'source_documents':2,'sourced_records':13,'withheld_case_admissions':11,'managed_cases_admitted':0,'scenarios':len(rows),'actual_query_executions':sum(r['observed_rows'] is not None for r in rows),
            'source_query_cases':sum(r['kind']=='source-query' for r in rows),'synthetic_negative_cases':sum(r['kind']=='synthetic-negative' for r in rows),
            'query_mutants_detected':sum(r['kind']=='query-mutation' and r['status']=='PASS' for r in rows),'guard_mutation_controls':sum(r['kind']=='guard-mutation' for r in rows),'identity_controls':sum(r['kind']=='identity-control' for r in rows),'statuses':dict(Counter(r['status'] for r in rows))},
        outcome='SCOPED_SOURCE_BACKED_CQ06_TRACE_EXECUTED',native_semantics_changed=False,owner_ratings_recorded=0,independent_semantic_acceptance=False,
        fresh_primary_pdf_reinspection_in_this_replay=False,source_inspection='inspection.json records the separate actual PDF inspection; automated replay uses the committed, hash-bound selected cohort. It does not rediscover source truth.',
        graphs=graphs,cases=rows)


def verify(saved,current):
    for key in ('source_cohort_freeze_commit','inputs','summary','outcome','native_semantics_changed','owner_ratings_recorded','independent_semantic_acceptance','graphs','cases'):
        if saved[key]!=current[key]:raise ValueError('CQ06 saved evidence differs: '+key)
    for key,graph in saved['graphs'].items():
        if sha(graph.encode())!=key:raise ValueError('CQ06 stored graph hash differs')


def verify_pdfs(directory):
    from pypdf import PdfReader
    cohort,_,_=inputs();paths=list(Path(directory).glob('*.pdf'));digests={sha(p.read_bytes()):p for p in paths}
    for source in cohort['sources']:
        p=digests.get(source['pdf_sha256'])
        if p is None:raise ValueError('Missing exact inspected PDF bytes: '+source['id'])
        r=PdfReader(p)
        if len(r.pages)!=source['pdf_pages']:raise ValueError('PDF page count differs')
        for page,digest in source['page_text_hashes'].items():
            if sha(r.pages[int(page)-1].extract_text().encode())!=digest:raise ValueError('PDF text extraction differs; inspect runtime before updating the source receipt')
    return {'exact_source_pdfs_rechecked':2,'inspected_page_hashes_matched':3,'pypdf':importlib.metadata.version('pypdf')}


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--verify-pdfs',type=Path);a=p.parse_args()
    if a.verify_pdfs:print(json.dumps(verify_pdfs(a.verify_pdfs)));return
    r=run();path=OUT/'report.json.gz'
    if a.check:verify(json.loads(gzip.decompress(path.read_bytes())),r)
    else:
        path.write_bytes(gzip.compress((json.dumps(r,indent=2)+'\n').encode(),mtime=0))
        lines=['# Executed source-backed CQ06 trace packet','',
            '**Scoped source-trace query evidence; no native managed-case admission, independent semantic acceptance or owner judgment.**','',
            'Execution checkout `'+r['source_commit']+'`; prior source/oracle freeze `'+FREEZE+'`. [Cohort and inspected-source/rights policy](README.md); [complete receipt](report.json.gz). Exact code/input/graph/query hashes and answer/finding oracles are retained.','',
            'Engine: '+json.dumps(r['engine'])+'. Automated replay uses the frozen selected source data; primary PDF inspection is separately recorded in inspection.json, not falsely repeated by CI.','',
            'Summary: '+json.dumps(r['summary'])+'. Source-backed records and deliberately synthetic failures/mutants are separate populations. A raw query can retrieve coherent forged metadata; frozen-cohort inspection checks reject it. Queries alone do not prove source truth.','',
            '| Case | Population/control | Raw answers | Task accepted | Verdict |','| --- | --- | --- | --- | --- |']
        for row in r['cases']:lines.append(f"| {row['id']} | {row['kind']} | {len(row['observed_rows']) if row['observed_rows'] is not None else 'ERROR'} | {row['trace_task_accepted']} | {row['status']} |")
        lines+=['','The 13 sourced records include 11 still-WITHHELD scenario descriptions and two review labels. No source score, probability, primary corroboration, event occurrence, full data accuracy or whole-ontology acceptance is claimed. CQ07/08 and owner review remain separate; old 40 synthetic CQ and scientific receipts retain their actual denominators.','',
            'Replay: `python tools/run_source_cq06.py --check`. Optional exact supplied PDF recheck: `python tools/run_source_cq06.py --verify-pdfs /path/to/private-pdfs` (requires pypdf; no PDF is published).']
        (OUT/'report.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(dict(r['summary'],engine=r['engine'])))

if __name__=='__main__':main()
