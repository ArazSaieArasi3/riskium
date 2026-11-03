"""Matched SQL/SPARQL retrieval on a pinned, synthetic SQLite schema-10 population.

Hand-written answer rows are declared before generating the database/export.
No score-literal, correction-edge, source-truth or general semantic-preservation claim.
"""
from pathlib import Path
import hashlib, json, platform, sqlite3, sys, subprocess
BASE=Path(__file__).resolve().parent
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else BASE/'generated'
REPO=BASE.parents[3]
sys.path.insert(0,str(REPO/'tools'))
from rdflib import Dataset, URIRef, __version__ as rdfversion

R='https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'
N=lambda x:'urn:riskium:nature37:'+x
A=lambda x:'urn:riskium:assessment:'+x
S=lambda x:'urn:riskium:sql:'+x
T=lambda x:'urn:riskium:assessment-selection:'+x
BG='urn:riskium:manuscript710:base'
SQL={
'case_entries':'SELECT DISTINCT entry_id,register_id FROM register_entry WHERE case_id=:focus ORDER BY entry_id,register_id',
'assessment_frame':'''SELECT DISTINCT result_id,context_version_id,method_version_id,basis_version_id,scale_version_id,dimension_id
 FROM v_assessment_frame WHERE assessment_version_id=:focus
 ORDER BY result_id,context_version_id,method_version_id,basis_version_id,scale_version_id,dimension_id''',
'issued_nature':'''SELECT DISTINCT ns.case_id,ns.term_version_id,ns.context_version_id,ts.scheme_version_id,co.objective_version_id
 FROM nature_snapshot ns JOIN nature_support ts ON ts.version_id=ns.term_version_id
 JOIN nature_membership nm ON nm.artifact_id=ts.artifact_id
 JOIN nature_support ss ON ss.version_id=ts.scheme_version_id
 LEFT JOIN nature_objective co ON co.context_version_id=ns.context_version_id
 WHERE ns.version_id=:focus
 ORDER BY ns.case_id,ns.term_version_id,ns.context_version_id,ts.scheme_version_id,co.objective_version_id'''
}
PREFIX='PREFIX r: <'+R+'>\n'
RQ={
'case_entries':PREFIX+'''SELECT DISTINCT ?entry ?register WHERE { GRAPH <'''+BG+'''> {
 ?entry r:R-01 ?focus ; r:RX-008 ?register . }}''',
'assessment_frame':PREFIX+'''PREFIX cp: <https://github.com/ArazSaieArasi3/riskium/profiles/comparison/0.7.0#>
 SELECT DISTINCT ?result ?context ?method ?basis ?scale ?dimension WHERE { GRAPH ?focus {
 ?focus r:RX-006 ?assessment .
 ?assessment r:R-13 ?result ; r:RX-014 ?context ; r:RX-015 ?method ; cp:basisVersion ?basis .
 ?result r:RX-016 ?scale ; r:R-48 ?dimension . }}''',
'issued_nature':PREFIX+'''SELECT DISTINCT ?case ?termVersion ?contextVersion ?schemeVersion ?objectiveVersion WHERE { GRAPH ?focus {
 ?focus r:RX-006 ?statement . ?statement r:R-41 ?case ; r:R-42 ?term .
 ?termVersion r:RX-006 ?term . ?term r:R-05 ?scheme . ?schemeVersion r:RX-006 ?scheme .
 OPTIONAL { ?statement r:R-43 ?context . ?contextVersion r:RX-006 ?context .
   OPTIONAL { ?context r:RK2-011 ?objective . ?objectiveVersion r:RX-006 ?objective . } }
 }}'''
}

def frame(result,scale='scale-v3'):
    return [result,S('context-v1'),A('method-v3'),A('basis-v1'),A(scale),A('dimension')]
def nature(term,ctx,scheme,obj):
    return [N('case-1'),N(term),N(ctx) if ctx else None,N(scheme),N(obj) if obj else None]
CASES=[
 dict(id='CE-multiple',task='case_entries',focus=N('case-1'),expected=[[N('entry-1'),N('register')],[N('entry-extra'),N('register')]]),
 dict(id='CE-distinct-equal-label',task='case_entries',focus=N('case-2'),expected=[[N('entry-2'),N('register')]]),
 dict(id='CE-empty',task='case_entries',focus=N('case-empty'),expected=[]),
 dict(id='CE-absent',task='case_entries',focus=N('not-in-fixture'),expected=[]),
 dict(id='AF-original',task='assessment_frame',focus=A('a1-v1'),expected=[frame(A('r1'))]),
 dict(id='AF-two-results',task='assessment_frame',focus=T('M-v1'),expected=[frame(T('MR-left')),frame(T('MR-right'))]),
 dict(id='AF-other-scale',task='assessment_frame',focus=T('N-v1'),expected=[frame(T('NR'),'scale-v4')]),
 dict(id='AF-absent',task='assessment_frame',focus=A('absent'),expected=[]),
 dict(id='NV-original',task='issued_nature',focus=N('A-v1'),expected=[nature('negative-v1','context-v1','scheme-I-v1','objective-v1')]),
 dict(id='NV-corrected-content',task='issued_nature',focus=N('A-v2'),expected=[nature('positive-v1','context-v2','scheme-I-v1','objective-v2')]),
 dict(id='NV-later-independent',task='issued_nature',focus=N('A-v4'),expected=[nature('positive-v2','context-v2','scheme-I-v2','objective-v2')]),
 dict(id='NV-other-source-vocabulary',task='issued_nature',focus=N('B-v1'),expected=[nature('other-negative-v1','context-v1','scheme-II-v1','objective-v1')]),
 dict(id='NV-missing-context',task='issued_nature',focus=N('U-v1'),expected=[nature('negative-v1',None,'scheme-I-v1',None)]),
 dict(id='NV-empty-objectives',task='issued_nature',focus=N('Z-v1'),expected=[nature('negative-v1','context-empty-v1','scheme-I-v1',None)]),
]

def normalized(rows):return sorted({tuple(None if c is None else str(c) for c in row) for row in rows},key=lambda x:json.dumps(x))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    qdir=OUT/'queries';qdir.mkdir(exist_ok=True)
    for k in SQL:
        (qdir/(k+'.sql')).write_text(SQL[k]+'\n');(qdir/(k+'.rq')).write_text(RQ[k]+'\n')
    policy=dict(scope='Three bounded retrieval families on schema 10 and existing synthetic fixture. No inference; all graph names explicit; URI values only except unbound variables.',
       comparison='SQL SELECT DISTINCT and SPARQL SELECT DISTINCT; sorted sets of tuples; SQL NULL and SPARQL unbound normalize to null; no default-graph union; no OWL imports, sameAs reasoning, score-literal or correction-edge mapping.',
       independence='SQL queries use domain tables/views; SPARQL queries use public RDF projections. Literal expected answers above are hand-authored independently of both query outputs.',
       nonclaims=['No numeric score comparison.','No general correction-lineage export.','No production performance or independently specified real-case validation.'])
    (OUT/'query-contract.json').write_text(json.dumps(dict(policy=policy,cases=CASES),indent=2))
    contract_digest=digest(OUT/'query-contract.json')
    # Population construction begins only after the contract and queries exist.
    import run_relational_risk_nature as run
    db=run.fresh();run.later(db)
    ds=Dataset(default_union=False)
    for s,p,o in db.execute('SELECT subject,predicate,object FROM v_native_facts'):
        ds.graph(URIRef(BG)).add((URIRef(s),URIRef(p),URIRef(o)))
    for graph,s,p,o in db.execute('SELECT graph_id,subject,predicate,object FROM v_assessment_quads'):
        ds.graph(URIRef(graph)).add((URIRef(s),URIRef(p),URIRef(o)))
    for (version,) in db.execute('SELECT version_id FROM nature_snapshot ORDER BY version_id'):
        for triple in run.x.native_graph(db,version):ds.graph(URIRef(version)).add(triple)
    out=[]
    for c in CASES:
        sql=normalized(db.execute(SQL[c['task']],{'focus':c['focus']}).fetchall())
        rdf=normalized(ds.query(RQ[c['task']],initBindings={'focus':URIRef(c['focus'])}))
        exp=normalized(c['expected'])
        out.append(dict(**c,sql_rows=sql,sparql_rows=rdf,status='PASS' if sql==rdf==exp else 'FAIL'))
    mutants=[
       ('CE-multiple',RQ['case_entries'].replace('r:R-01 ?focus','r:RX-008 ?focus')),
       ('AF-original',RQ['assessment_frame'].replace('r:RX-015 ?method','r:RX-016 ?method')),
       ('NV-original',RQ['issued_nature'].replace('r:R-42 ?term','r:R-43 ?term'))]
    controls=[]
    for cid,q in mutants:
        c=next(x for x in CASES if x['id']==cid)
        rows=normalized(ds.query(q,initBindings={'focus':URIRef(c['focus'])}))
        controls.append(dict(case=cid,query=q,rows=rows,status='DETECTED' if rows!=normalized(c['expected']) else 'MISSED'))
    target=sqlite3.connect(OUT/'synthetic-query-population.sqlite');db.backup(target);target.close()
    ds.serialize(OUT/'synthetic-query-export.trig',format='trig')
    report=dict(repository_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
        model_sha256=digest(REPO/'ontology/riskium-model.json'),contract_sha256=contract_digest,script_sha256=digest(Path(__file__)),
        query_sha256={p.name:digest(p) for p in qdir.iterdir()},python=platform.python_version(),sqlite=sqlite3.sqlite_version,rdflib=rdfversion,
        policy=policy,schema_version=db.execute('PRAGMA user_version').fetchone()[0],named_graphs=len([g for g in ds.graphs() if len(g)]),
        cases=out,mutations=controls,summary=dict(matched_cases=len(out),passes=sum(x['status']=='PASS' for x in out),query_mutants=len(controls),detected=sum(x['status']=='DETECTED' for x in controls)))
    (OUT/'query-parity-report.json').write_text(json.dumps(report,indent=2))
    db.close()
    print(json.dumps(report['summary']))
    if report['summary']['passes']!=len(out):
        print(json.dumps([x for x in out if x['status']!='PASS'],indent=2));raise SystemExit(1)
    assert all(x['status']=='DETECTED' for x in controls)
if __name__=='__main__':main()
