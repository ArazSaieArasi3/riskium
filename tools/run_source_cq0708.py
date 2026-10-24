"""Run fixed source-backed correction lineage and unasserted case-identity queries."""
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
from rdflib import Graph,URIRef,Literal,RDF,DCTERMS,PROV,XSD
from run_cq import execute,ordered

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evaluation/sources/cq0708'
FREEZE='920524ee05d4f7f7468ce7a9aa75a70cc7c08503'
BASE='urn:riskium:source-cq0708:';APP='urn:riskium:source-cq-profile:0.3.0#'
RISK='https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'
CAND=URIRef('https://github.com/ArazSaieArasi3/riskium/profiles/catalog/0.3.0#candidate')
U=lambda s:URIRef(BASE+s);A=lambda s:URIRef(APP+s);N=lambda s:URIRef(RISK+s)
DEC=lambda s:Literal(s,datatype=XSD.decimal)
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda v:json.dumps(v,sort_keys=True,separators=(',',':'))
INPUTS=['ontology/riskium-model.json','ontology/derived/riskium.owl.ttl','evaluation/cq/report.json',
 'evaluation/sources/cq06/cohort.json','evaluation/sources/cq06/inspection.json','evaluation/sources/cq06/report.json.gz',
 'evaluation/sources/cq0708/cohort.json','evaluation/sources/cq0708/inspection.json','evaluation/sources/cq0708/expected.json',
 'evaluation/sources/cq0708/profile.json','evaluation/sources/cq0708/cq07.rq','evaluation/sources/cq0708/cq08.rq',
 'evaluation/sources/cq0708/mutants/cq07-reversed.rq','evaluation/sources/cq0708/mutants/cq07-overwrite-old.rq',
 'evaluation/sources/cq0708/mutants/cq08-bound-only.rq','evaluation/sources/cq0708/mutants/cq08-invent-case.rq',
 'tools/run_cq.py','tools/run_source_cq0708.py','tools/requirements-owl.txt']


def inputs():
    c=json.loads((OUT/'cohort.json').read_text());e=json.loads((OUT/'expected.json').read_text());i=json.loads((OUT/'inspection.json').read_text())
    for name in ('cohort.json','expected.json','inspection.json'):
        if (OUT/name).read_bytes()!=subprocess.check_output(['git','show',FREEZE+':evaluation/sources/cq0708/'+name],cwd=ROOT):raise ValueError('CQ0708 frozen input changed: '+name)
    if i['cohort_sha256']!=sha((OUT/'cohort.json').read_bytes()):raise ValueError('CQ0708 inspection binding differs')
    old=json.loads((ROOT/'evaluation/sources/cq06/cohort.json').read_text());withheld=[r for r in old['records'] if r['case_admission']=='WITHHELD']
    if c['prior_cq06_cohort_sha256']!=sha((ROOT/'evaluation/sources/cq06/cohort.json').read_bytes()) or c['prior_cq06_inspection_sha256']!=sha((ROOT/'evaluation/sources/cq06/inspection.json').read_bytes()):raise ValueError('CQ08 inherited source binding differs')
    if [r['id'] for r in c['identity_candidates']]!=e['cq08_unbound_case_ids'] or len(withheld)!=11 or len(c['identity_candidates'])!=11:raise ValueError('CQ08 candidate population differs')
    for row,prior in zip(c['identity_candidates'],withheld):
        if any(row[k]!=prior[k] for k in ('id','source_id','locator','case_admission','risk_case_identity','occurrence_asserted')) or row['prior_evidence_id']!=prior['evidence_id']:raise ValueError('CQ08 prior decision changed')
        if row['risk_case_identity'] is not None or row['occurrence_asserted']:raise ValueError('CQ08 case/occurrence promotion')
    cells={x['id']:[x['original']['value'],x['reissued']['value'],x['disposition']] for x in c['assertions']}
    if cells!={key:[a,b,status] for key,a,b,status in e['cq07_cells']} or len(cells)!=5 or e['independent_study_lineages']!=1 or e['retained_assertion_versions']!=10:raise ValueError('CQ07 independent oracle differs')
    sources={s['id']:s for s in c['sources']}
    if sources['original']['uri']!=e['original_source'] or sources['correction']['uri']!=e['correction_source'] or sources['original']['doi']==sources['correction']['doi']:raise ValueError('CQ07 source identities differ')
    for source in c['sources']:
        saved=next(x for x in i['source_pdfs'] if x['id']==source['id'])
        if any(saved[k]!=source[k] for k in saved if k!='id'):raise ValueError('CQ0708 PDF binding differs')
    return c,e,i


def cq07_graph(c,ids):
    g=Graph();sources={s['id']:URIRef(s['uri']) for s in c['sources']}
    g.add((sources['correction'],A('correctsSource'),sources['original']))
    g.add((sources['correction'],A('independentStudyLineages'),Literal(1)))
    for r in c['assertions']:
        if r['id'] not in ids:continue
        key=r['id'];artifact=U('assertion:'+key);g.add((artifact,RDF.type,N('RKM-C014')))
        for label,data in [('original',r['original']),('reissued',r['reissued'])]:
            record=U('record:'+key+':'+label);version=U('version:'+key+':'+label)
            for triple in [(record,RDF.type,A('AssertionRecord')),(record,CAND,version),(version,RDF.type,N('RKM-C015')),
                (version,N('RX-006'),artifact),(record,DCTERMS.source,sources[data['source_id']]),(record,A('reportedValue'),DEC(data['value'])),
                (record,A('unit'),Literal('percent')),(record,A('cellContext'),Literal(canonical(r['context']))),(record,A('sourceLocator'),Literal(data['locator']))]:g.add(triple)
            for field,predicate,datatype in [('standard_error_percent','standardErrorPercent',XSD.decimal)]:
                if data[field] is not None:g.add((record,A(predicate),Literal(data[field],datatype=datatype)))
            if r['context']['total_paths'] is not None:g.add((record,A('totalPaths'),Literal(r['context']['total_paths'])))
        g.add((U('record:'+key+':reissued'),PROV.wasRevisionOf,U('record:'+key+':original')))
        g.add((U('record:'+key+':reissued'),A('disposition'),Literal(r['disposition'])))
    return g


def cq08_graph(c,ids):
    g=Graph();source=URIRef('https://doi.org/10.1080/13669877.2013.815653')
    for r in c['identity_candidates']:
        if r['id'] not in ids:continue
        record=U('raw:'+r['id']);candidate=URIRef('urn:riskium:source-cq06:statement:'+r['id'])
        for triple in [(record,RDF.type,A('RawScenarioRecord')),(record,CAND,candidate),(candidate,RDF.type,N('RKM-C014')),
            (record,DCTERMS.source,source),(record,A('sourceLocator'),Literal(r['locator'])),(record,A('caseAdmission'),Literal('WITHHELD')),
            (record,A('occurrenceAsserted'),Literal(False)),(record,A('priorRecord'),URIRef('urn:riskium:source-cq06:record:'+r['id']))]:g.add(triple)
    return g


def fixed_rows(e,route,ids):
    if route=='cq07':return ordered([[U('record:'+key+':reissued').n3(),U('record:'+key+':original').n3(),URIRef(e['correction_source']).n3(),DEC(old).n3(),DEC(new).n3(),Literal(status).n3()] for key,old,new,status in e['cq07_cells'] if key in ids])
    return ordered([[U('raw:'+key).n3(),URIRef('urn:riskium:source-cq06:statement:'+key).n3(),None] for key in e['cq08_unbound_case_ids'] if key in ids])


def findings(g,c,route,ids,frozen=True,identity_guard=True):
    result=[]
    def exact(subject,predicate,wanted,code):
        if set(g.objects(subject,predicate))!=set(wanted):result.append(code)
    if route=='cq07':
        records={U('record:'+key+':'+suffix) for key in ids for suffix in ('original','reissued')}
        if set(g.subjects(RDF.type,A('AssertionRecord')))!=records:result.append('CQ07:RECORD_POPULATION')
        sources={s['id']:URIRef(s['uri']) for s in c['sources']}
        exact(sources['correction'],A('correctsSource'),[sources['original']],'CQ07:CORRECTION_SOURCE_LINK')
        exact(sources['correction'],A('independentStudyLineages'),[Literal(1)],'CQ07:INDEPENDENCE')
        for r in c['assertions']:
            if r['id'] not in ids:continue
            key=r['id'];artifact=U('assertion:'+key)
            exact(artifact,RDF.type,[N('RKM-C014')],key+':ARTIFACT_TYPE')
            for label,data in [('original',r['original']),('reissued',r['reissued'])]:
                rec=U('record:'+key+':'+label);version=U('version:'+key+':'+label);prefix=key+':'+label.upper()+'_'
                exact(rec,RDF.type,[A('AssertionRecord')],prefix+'TYPE');exact(rec,CAND,[version],prefix+'VERSION');exact(version,RDF.type,[N('RKM-C015')],prefix+'VERSION_TYPE');exact(version,N('RX-006'),[artifact],prefix+'TARGET')
                if frozen:
                    for predicate,wanted,code in [(DCTERMS.source,[sources[data['source_id']]],'SOURCE'),(A('reportedValue'),[DEC(data['value'])],'VALUE'),(A('unit'),[Literal('percent')],'UNIT'),(A('cellContext'),[Literal(canonical(r['context']))],'CONTEXT'),(A('sourceLocator'),[Literal(data['locator'])],'LOCATOR'),(A('standardErrorPercent'),[] if data['standard_error_percent'] is None else [DEC(data['standard_error_percent'])],'SE'),(A('totalPaths'),[] if r['context']['total_paths'] is None else [Literal(r['context']['total_paths'])],'DENOMINATOR')]:exact(rec,predicate,wanted,prefix+code)
            exact(U('record:'+key+':reissued'),PROV.wasRevisionOf,[U('record:'+key+':original')],key+':PARENT')
            exact(U('record:'+key+':reissued'),A('disposition'),[Literal(r['disposition'])],key+':DISPOSITION')
    else:
        records={U('raw:'+key) for key in ids}
        if set(g.subjects(RDF.type,A('RawScenarioRecord')))!=records:result.append('CQ08:RECORD_POPULATION')
        for r in c['identity_candidates']:
            if r['id'] not in ids:continue
            key=r['id'];rec=U('raw:'+key);candidate=URIRef('urn:riskium:source-cq06:statement:'+key)
            for subject,predicate,wanted,code in [(rec,CAND,[candidate],'CANDIDATE'),(candidate,RDF.type,[N('RKM-C014')],'CANDIDATE_TYPE'),(rec,DCTERMS.source,[URIRef('https://doi.org/10.1080/13669877.2013.815653')],'SOURCE'),(rec,A('sourceLocator'),[Literal(r['locator'])],'LOCATOR'),(rec,A('caseAdmission'),[Literal('WITHHELD')],'DECISION'),(rec,A('occurrenceAsserted'),[Literal(False)],'OCCURRENCE'),(rec,A('priorRecord'),[URIRef('urn:riskium:source-cq06:record:'+key)],'PRIOR_RECORD')]:exact(subject,predicate,wanted,key+':'+code)
            if identity_guard and list(g.objects(candidate,N('R-36'))):result.append(key+':CASE_LINK')
    if identity_guard:
        if (None,RDF.type,N('RKM-X01')) in g:result.append('NATIVE_CASE_PROMOTION')
        if (None,RDF.type,N('RKM-C003')) in g:result.append('NATIVE_SCENARIO_PROMOTION')
    return sorted(result)


def specs(c,e):
    ids7=[r[0] for r in e['cq07_cells']];ids8=e['cq08_unbound_case_ids'];result=[]
    def add(cid,route,ids,action=None,expected=None,codes=(),kind='synthetic-negative',query=None):
        result.append(dict(id=cid,route=route,ids=ids,action=action,expected_rows=[list(row) for row in (fixed_rows(e,route,ids) if expected is None else ordered(expected))],expected_findings=sorted(codes),kind=kind,query=query or route+'.rq'))
    add('SOURCE-CQ07-ALL-FIVE','cq07',ids7,kind='source-query');add('SOURCE-CQ08-ALL-ELEVEN','cq08',ids8,kind='source-query')
    for key in ids7:add('SOURCE-CQ07-'+key,'cq07',[key],kind='source-query')
    for key in ids8:add('SOURCE-CQ08-'+key,'cq08',[key],kind='source-query')
    key=ids7[0];old=U('record:'+key+':original');new=U('record:'+key+':reissued');one=fixed_rows(e,'cq07',[key]);prefix=key+':'
    def n7(cid,action,rows=None,codes=()):add(cid,'cq07',[key],action,one if rows is None else rows,[prefix+x if not x.startswith('CQ07:') else x for x in codes])
    n7('CQ07-MISSING-LINEAGE','missing-lineage',[],['PARENT'])
    n7('CQ07-WRONG-PARENT','wrong-parent',[],['PARENT'])
    n7('CQ07-CROSS-ARTIFACT','wrong-target',[],['REISSUED_TARGET'])
    n7('CQ07-MISSING-ORIGINAL-TYPE','missing-old-type',[],['ORIGINAL_TYPE','CQ07:RECORD_POPULATION'])
    n7('CQ07-MISSING-ORIGINAL-SOURCE','missing-old-source',[],['ORIGINAL_SOURCE'])
    n7('CQ07-MISSING-CORRECTION-NOTICE','missing-source-link',[],['CQ07:CORRECTION_SOURCE_LINK'])
    n7('CQ07-UNRELATED-CORRECTION','wrong-source-link',[],['CQ07:CORRECTION_SOURCE_LINK'])
    n7('CQ07-WRONG-LOCATOR','wrong-locator',codes=['REISSUED_LOCATOR'])
    n7('CQ07-MISSING-LOCATOR','missing-locator',codes=['REISSUED_LOCATOR'])
    n7('CQ07-WRONG-UNIT','wrong-unit',codes=['REISSUED_UNIT'])
    n7('CQ07-WRONG-CONTEXT','wrong-context',[],['REISSUED_CONTEXT'])
    n7('CQ07-COHERENT-WRONG-CONTEXT','coherent-context',codes=['ORIGINAL_CONTEXT','REISSUED_CONTEXT'])
    changed=[list(one[0])];changed[0][2]=URIRef('urn:riskium:synthetic-unrelated-publication').n3()
    n7('CQ07-COHERENT-FORGED-SOURCE','coherent-source',changed,['REISSUED_SOURCE'])
    changed=[list(one[0])];changed[0][4]=DEC('999').n3()
    n7('CQ07-FORGED-REPORTED-VALUE','wrong-value',changed,['REISSUED_VALUE'])
    changed=[list(row) for row in one]+[[*one[0][:4],DEC('999').n3(),one[0][5]]]
    n7('CQ07-CONFLICTING-VALUES-PRESERVED','extra-value',changed,['REISSUED_VALUE'])
    changed=[list(one[0])];changed[0][3]=DEC('48.6').n3()
    n7('CQ07-ORIGINAL-OVERWRITE-DETECTED','overwrite-old',changed,['ORIGINAL_VALUE'])
    n7('CQ07-CORRECTION-NOT-CORROBORATION','independent-two',codes=['CQ07:INDEPENDENCE'])
    changed=[list(one[0])];changed[0][5]=Literal('REISSUED_UNCHANGED').n3()
    n7('CQ07-WRONG-DISPOSITION','wrong-disposition',changed,['DISPOSITION'])
    # The Table 1 example has unknown cell denominator/SE: neither can be filled with zero.
    n7('CQ07-UNKNOWN-DENOMINATOR-NOT-ZERO','invent-denominator',codes=['REISSUED_DENOMINATOR'])
    # Two different panels include numeric equality; deliberately giving them equal labels must not merge identity.
    add('CQ07-EQUAL-TITLES-DISTINCT-ASSERTIONS','cq07',ids7[:2],'equal-title',kind='identity-control')
    add('CQ07-DELETED-SOURCE-GUARD-EXPOSES-FORGERY','cq07',[key],'coherent-source',[[one[0][0],one[0][1],URIRef('urn:riskium:synthetic-unrelated-publication').n3(),*one[0][3:]]],kind='guard-mutation')
    key=ids8[0];one=fixed_rows(e,'cq08',[key]);prefix=key+':'
    def n8(cid,action,rows=None,codes=()):add(cid,'cq08',[key],action,one if rows is None else rows,[prefix+x if not x.startswith('NATIVE_') and not x.startswith('CQ08:') else x for x in codes])
    n8('CQ08-MISSING-CANDIDATE','missing-candidate',[],['CANDIDATE'])
    n8('CQ08-MISSING-SOURCE','missing-raw-source',codes=['SOURCE'])
    n8('CQ08-WRONG-SOURCE','wrong-raw-source',codes=['SOURCE'])
    n8('CQ08-WRONG-LOCATOR','wrong-raw-locator',codes=['LOCATOR'])
    n8('CQ08-WRONG-PRIOR-RECORD','wrong-prior',codes=['PRIOR_RECORD'])
    n8('CQ08-UNAUTHORIZED-ADMISSION','promote-decision',codes=['DECISION'])
    n8('CQ08-UNAUTHORIZED-OCCURRENCE','promote-occurrence',codes=['OCCURRENCE'])
    changed=[[one[0][0],one[0][1],U('synthetic-case').n3()]]
    n8('CQ08-FALSE-CASE-LINK','case-link',changed,['CASE_LINK'])
    n8('CQ08-NATIVE-CASE-PROMOTION','case-type',codes=['NATIVE_CASE_PROMOTION'])
    n8('CQ08-NATIVE-SCENARIO-PROMOTION','scenario-type',codes=['CANDIDATE_TYPE','NATIVE_SCENARIO_PROMOTION'])
    changed=[list(row) for row in one]+[[one[0][0],one[0][1],U('synthetic-case').n3()]];changed[0][2]=U('synthetic-case-2').n3()
    n8('CQ08-CONFLICTING-CASE-LINKS-PRESERVED','two-cases',changed,['CASE_LINK'])
    changed=[[one[0][0],URIRef('urn:riskium:source-cq06:statement:'+ids8[1]).n3(),None]]
    n8('CQ08-ALIAS-DOES-NOT-ALLOCATE-CASE','wrong-candidate',changed,['CANDIDATE'])
    add('CQ08-EQUAL-TITLES-DISTINCT-CANDIDATES','cq08',ids8[:2],'equal-title',kind='identity-control')
    add('CQ08-DELETED-IDENTITY-GUARD-EXPOSES-PROMOTION','cq08',[key],'case-link',[[one[0][0],one[0][1],U('synthetic-case').n3()]],kind='guard-mutation')
    for name,route,ids in [('cq07-reversed','cq07',ids7),('cq07-overwrite-old','cq07',ids7),('cq08-bound-only','cq08',ids8),('cq08-invent-case','cq08',ids8)]:add('QUERY-MUTANT-'+name.upper(),route,ids,kind='query-mutation',query='mutants/'+name+'.rq')
    for route,ids in [('cq07',ids7),('cq08',ids8)]:add('SERIALIZE-REPARSE-'+route.upper(),route,ids,'roundtrip',kind='roundtrip')
    return result


def alter(g,s):
    action=s['action'];key=s['ids'][0]
    if not action:return g
    if action=='roundtrip':return Graph().parse(data=g.serialize(format='turtle'),format='turtle')
    if action=='equal-title':
        for identity in s['ids']:g.add((U('assertion:'+identity) if s['route']=='cq07' else URIRef('urn:riskium:source-cq06:statement:'+identity),DCTERMS.title,Literal('Same display title')))
        return g
    if s['route']=='cq07':
        old=U('record:'+key+':original');new=U('record:'+key+':reissued');version=U('version:'+key+':reissued');source=URIRef('https://doi.org/10.1093/biostatistics/kxy072')
        if action=='missing-lineage':g.remove((new,PROV.wasRevisionOf,None))
        elif action=='wrong-parent':g.set((new,PROV.wasRevisionOf,U('record:unrelated:original')))
        elif action=='wrong-target':g.set((version,N('RX-006'),U('assertion:unrelated')))
        elif action=='missing-old-type':g.remove((old,RDF.type,None))
        elif action=='missing-old-source':g.remove((old,DCTERMS.source,None))
        elif action=='missing-source-link':g.remove((source,A('correctsSource'),None))
        elif action=='wrong-source-link':g.set((source,A('correctsSource'),U('unrelated-source')))
        elif action=='missing-locator':g.remove((new,A('sourceLocator'),None))
        elif action=='wrong-locator':g.set((new,A('sourceLocator'),Literal('Uninspected location')))
        elif action=='wrong-unit':g.set((new,A('unit'),Literal('ratio')))
        elif action in ('wrong-context','coherent-context'):
            g.set((new,A('cellContext'),Literal('Different panel')))
            if action=='coherent-context':g.set((old,A('cellContext'),Literal('Different panel')))
        elif action=='coherent-source':
            fake=URIRef('urn:riskium:synthetic-unrelated-publication');g.set((new,DCTERMS.source,fake));g.add((fake,A('correctsSource'),URIRef('https://doi.org/10.1093/biostatistics/kxx069')))
        elif action=='wrong-value':g.set((new,A('reportedValue'),DEC('999')))
        elif action=='extra-value':g.add((new,A('reportedValue'),DEC('999')))
        elif action=='overwrite-old':g.set((old,A('reportedValue'),DEC('48.6')))
        elif action=='independent-two':g.set((source,A('independentStudyLineages'),Literal(2)))
        elif action=='wrong-disposition':g.set((new,A('disposition'),Literal('REISSUED_UNCHANGED')))
        elif action=='invent-denominator':g.set((new,A('totalPaths'),Literal(0)))
        else:raise ValueError('Unknown CQ07 edit')
    else:
        rec=U('raw:'+key);candidate=URIRef('urn:riskium:source-cq06:statement:'+key)
        if action=='missing-candidate':g.remove((rec,CAND,None))
        elif action=='missing-raw-source':g.remove((rec,DCTERMS.source,None))
        elif action=='wrong-raw-source':g.set((rec,DCTERMS.source,U('unrelated-source')))
        elif action=='wrong-raw-locator':g.set((rec,A('sourceLocator'),Literal('Uninspected location')))
        elif action=='wrong-prior':g.set((rec,A('priorRecord'),U('unrelated-record')))
        elif action=='promote-decision':g.set((rec,A('caseAdmission'),Literal('ISSUED')))
        elif action=='promote-occurrence':g.set((rec,A('occurrenceAsserted'),Literal(True)))
        elif action in ('case-link','two-cases'):
            g.add((candidate,N('R-36'),U('synthetic-case')))
            if action=='two-cases':g.add((candidate,N('R-36'),U('synthetic-case-2')))
        elif action=='case-type':g.add((U('synthetic-case'),RDF.type,N('RKM-X01')))
        elif action=='scenario-type':g.add((candidate,RDF.type,N('RKM-C003')))
        elif action=='wrong-candidate':g.set((rec,CAND,URIRef('urn:riskium:source-cq06:statement:UPX-MAT-004-002')))
        else:raise ValueError('Unknown CQ08 edit')
    return g


def case(s,c,e,graphs):
    graph=cq07_graph(c,s['ids']) if s['route']=='cq07' else cq08_graph(c,s['ids']);g=alter(graph,s)
    snapshot='\n'.join(sorted(g.serialize(format='nt').splitlines()))+'\n';key=sha(snapshot.encode());graphs.setdefault(key,snapshot)
    flags={'frozen':False} if s['kind']=='guard-mutation' and s['route']=='cq07' else {'identity_guard':False} if s['kind']=='guard-mutation' else {}
    faults=findings(g,c,s['route'],s['ids'],**flags);query=(OUT/s['query']).read_text();observed=None;error=None
    try:observed=execute(g,query,e[s['route']+'_columns'])
    except Exception as exc:error=type(exc).__name__+': '+str(exc)
    equal=observed==s['expected_rows'];matches=not equal if s['kind']=='query-mutation' else equal
    passed=error is None and matches and faults==s['expected_findings']
    return dict(id=s['id'],route=s['route'],kind=s['kind'],population_ids=s['ids'],status='PASS' if passed else 'ERROR' if error else 'FAIL',query=s['query'],query_sha256=sha(query.encode()),graph_sha256=key,
        expected_rows=s['expected_rows'],observed_rows=observed,oracle_equal=equal,expected_findings=s['expected_findings'],observed_findings=faults,
        expected_behavior='DIFFERENT_FROM_FIXED_POSITIVE_ORACLE' if s['kind']=='query-mutation' else 'EXACT_RAW_BINDINGS_AND_FINDINGS',validator_admits=not faults,
        inspection_task_accepted=not faults and s['kind'] not in ('query-mutation','guard-mutation'),error=error)


def run():
    c,e,i=inputs();profile=json.loads((OUT/'profile.json').read_text());model=json.loads((ROOT/'ontology/riskium-model.json').read_text());signatures={r['id']:[r['source'],r['target']] for r in model['associations']}
    if any(signatures[rid]!=pair for rid,pair in profile['native_signatures'].items()):raise ValueError('CQ0708 native signature changed')
    for path in ('ontology/riskium-model.json','ontology/derived/riskium.owl.ttl','evaluation/cq/report.json','evaluation/sources/cq06/report.json.gz'):
        if (ROOT/path).read_bytes()!=subprocess.check_output(['git','show',FREEZE+':'+path],cwd=ROOT):raise ValueError('CQ0708 historical source/evidence changed: '+path)
    if importlib.metadata.version('rdflib')!='7.6.0':raise ValueError('Use pinned RDFLib 7.6.0')
    graphs={};rows=[case(s,c,e,graphs) for s in specs(c,e)]
    for text in graphs.values():
        for s,p,o in Graph().parse(data=text,format='nt'):
            for term in (p,o if p==RDF.type else None):
                if term is not None and str(term).startswith(APP) and str(term)[len(APP):] not in profile['terms']:raise ValueError('Undeclared CQ0708 metadata term')
    failed=[{k:r[k] for k in ('id','error','expected_findings','observed_findings','expected_rows','observed_rows')} for r in rows if r['status']!='PASS']
    if failed:raise ValueError('CQ0708 oracle mismatch: '+json.dumps(failed))
    return dict(schema='riskium-source-cq0708-evidence-v1',source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),source_oracle_freeze_commit=FREEZE,
        recorded_at_utc=datetime.now(timezone.utc).isoformat(),inputs={p:sha((ROOT/p).read_bytes()) for p in INPUTS},engine={'name':'RDFLib SPARQL SELECT','version':importlib.metadata.version('rdflib'),'python':sys.version.split()[0],'inference':'none','remote_service':False},
        summary={'correction_source_documents':2,'independent_study_lineages':1,'selected_assertion_pairs':5,'retained_assertion_versions':10,'changed_selected_values':4,'unchanged_reissued_values':1,'withheld_identity_candidates':11,'managed_cases_admitted':0,
            'scenarios':len(rows),'actual_query_executions':sum(r['observed_rows'] is not None for r in rows),'by_route':dict(Counter(r['route'] for r in rows)),'by_kind':dict(Counter(r['kind'] for r in rows)),
            'query_mutants_detected':sum(r['kind']=='query-mutation' and r['status']=='PASS' for r in rows),'statuses':dict(Counter(r['status'] for r in rows))},
        outcome='SCOPED_SOURCE_BACKED_CQ07_CQ08_EXECUTED',native_semantics_changed=False,owner_ratings_added=0,independent_semantic_acceptance=False,
        fresh_primary_pdf_reinspection_in_this_replay=False,source_inspection='inspection.json records the actual separate supplied PDF review. This replay uses frozen public selected cells and inherited case decisions, not fresh source truth discovery.',
        graphs=graphs,cases=rows)


def verify(saved,current):
    for key in ('source_oracle_freeze_commit','inputs','summary','outcome','native_semantics_changed','owner_ratings_added','independent_semantic_acceptance','graphs','cases'):
        if saved[key]!=current[key]:raise ValueError('CQ0708 saved evidence differs: '+key)
    for key,text in saved['graphs'].items():
        if sha(text.encode())!=key:raise ValueError('CQ0708 graph hash differs')


def verify_pdfs(directory):
    from pypdf import PdfReader
    c,_,_=inputs();digests={sha(p.read_bytes()):p for p in Path(directory).glob('*.pdf')}
    for source in c['sources']:
        if source['pdf_sha256'] not in digests:raise ValueError('Missing exact source PDF: '+source['id'])
        r=PdfReader(digests[source['pdf_sha256']]);assert len(r.pages)==source['pdf_page_count']
        for page,digest in source['page_text_hashes'].items():
            if sha(r.pages[int(page)-1].extract_text().encode())!=digest:raise ValueError('Source page-text extraction differs')
    return {'exact_source_pdfs_rechecked':2,'source_page_hashes_matched':6,'pypdf':importlib.metadata.version('pypdf')}


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--verify-pdfs',type=Path);a=p.parse_args()
    if a.verify_pdfs:print(json.dumps(verify_pdfs(a.verify_pdfs)));return
    r=run();path=OUT/'report.json.gz'
    if a.check:verify(json.loads(gzip.decompress(path.read_bytes())),r)
    else:
        path.write_bytes(gzip.compress((json.dumps(r,indent=2)+'\n').encode(),mtime=0))
        lines=['# Executed source-backed CQ07/CQ08 packet','',
            '**Scoped correction/identity inspection, not complete native admission, clinical estimate validation, independent review or owner acceptance.**','',
            'Execution checkout `'+r['source_commit']+'`; source/oracle freeze `'+FREEZE+'`. [Scope, dictionary, rights and sources](README.md); [complete receipt](report.json.gz). Exact inputs/query/graph/binding/finding oracles are retained.','',
            'Engine: '+json.dumps(r['engine'])+'. CI replays frozen public selected source data; the actual primary PDF review is separately recorded in inspection.json.','',
            'Summary: '+json.dumps(r['summary'])+'. Source queries, synthetic negatives, identity/guard/mutant controls and round trips are disjoint scenario kinds. An unbound case is an absent graph assertion, not a real-world nonexistence result.','',
            '| Case | CQ | Kind | Raw answers | Validator admits | Verdict |','| --- | --- | --- | --- | --- | --- |']
        for row in r['cases']:lines.append(f"| {row['id']} | {row['route']} | {row['kind']} | {len(row['observed_rows']) if row['observed_rows'] is not None else 'ERROR'} | {row['validator_admits']} | {row['status']} |")
        lines+=['','A deliberately deleted guard may admit a synthetic forgery; its PASS means sensitivity matched its fixed oracle, not that the forged record is acceptable. Parser/engine failures are ERROR. No old assertion is overwritten, no correction adds independent corroboration, no withheld candidate is admitted and no historical engine denominator is rewritten.','',
            'Replay: `python tools/run_source_cq0708.py --check`. Optional privately held exact PDF recheck: `python tools/run_source_cq0708.py --verify-pdfs /path/to/private-pdfs` (pypdf required; no PDF is packaged).']
        (OUT/'report.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(dict(r['summary'],engine=r['engine'])))

if __name__=='__main__':main()
