"""Execute the twenty B1 oracles with separate task, SQL and logical receipts."""
from pathlib import Path
from copy import deepcopy
import argparse,hashlib,json,subprocess,sys,time
from rdflib import Graph,Dataset,Namespace,URIRef,BNode,Literal,RDF,RDFS,OWL,XSD
from rdflib.compare import isomorphic
from jsonschema import Draft202012Validator,FormatChecker
from pyshacl import validate
import build_candidate as b
import case_profiles as p
import reader
sys.path.insert(0,str(b.ROOT/'tools'))
import relational_history as history
RISK=p.RISK;APP=p.APP;SH=p.SH;EX=Namespace('urn:riskium:case-fixture:')

def main(a):
 out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
 if b.sha(a.schema)!='094324d8e6ac4505ef5ae983a45bb9b56a8b3b6960151c57736756a037344d38':raise ValueError('Unpinned native schema')
 if b.sha(a.robot)!='53cd275c8e4c0dad1fc2c1c34174876795cd7d6b6926e1444adcbb0cb3c7ab26':raise ValueError('Unpinned ROBOT')
 before={str(f.relative_to(b.ROOT)):b.sha(f) for directory in ['ontology','implementation','evaluation/sources'] for f in (b.ROOT/directory).rglob('*') if f.is_file() and '__pycache__' not in f.parts}
 b.build(check=True);files,coverage=reader.generate(check=True)
 contract=json.loads(b.CONTRACT.read_text());model,_=b.validate_contract(contract)
 native=json.loads((b.HERE/'candidate.ontouml.json').read_text());owl=Graph().parse(b.HERE/'candidate.owl.ttl',format='turtle')
 old_native,old_owl,_=b.prior.render(json.loads(b.prior.CONTRACT.read_text()))
 def logical(g):
  annotations=set(g.subjects(RDF.type,OWL.AnnotationProperty))|{RDFS.label,RDFS.comment,OWL.versionIRI};ontos=set(g.subjects(RDF.type,OWL.Ontology))
  x=Graph()
  for s,q,o in g:
   if q not in annotations and s not in ontos:x.add((s,q,o))
  return x
 iso=isomorphic(logical(owl),logical(Graph().parse(data=old_owl,format='turtle')))
 oracles=json.loads((b.IMPACT/'acceptance-oracles.json').read_text())['cases'];rows=[];shacl_runs=[];hermit_runs=[];commands=[]
 def command(label,argv):
  start=time.monotonic();r=subprocess.run([str(x) for x in argv],cwd=b.ROOT,capture_output=True,text=True,timeout=120)
  d=out/'engine-logs';d.mkdir(exist_ok=True);(d/(label+'.stdout.txt')).write_text(r.stdout);(d/(label+'.stderr.txt')).write_text(r.stderr)
  receipt={'label':label,'exit_code':r.returncode,'elapsed_ms':round((time.monotonic()-start)*1000),'stdout_sha256':b.sha(d/(label+'.stdout.txt')),'stderr_sha256':b.sha(d/(label+'.stderr.txt'))};commands.append(receipt);return r,receipt
 def dataset(label,data,shapes,report):
  ds=Dataset()
  for name,g in [('data',data),('shapes',shapes),('report',report)]:
   for t in g:ds.graph(URIRef('urn:riskium:replay:'+name)).add(t)
  d=out/'shacl';d.mkdir(exist_ok=True);f=d/(label+'.trig');ds.serialize(f,format='trig');return {'path':str(f.relative_to(out)),'sha256':b.sha(f),'data_triples':len(data),'shape_triples':len(shapes),'report_triples':len(report)}
 def check(raw,task='analytical-case',focus=None,label='check'):
  snapshot=set(raw);result,data,shapes,report=p.evaluate(raw,[EX.case] if focus is None else focus,task)
  assert set(raw)==snapshot,'Profile mutated raw input'
  receipt=dataset(str(len(shacl_runs)+1).zfill(2)+'-'+label,data,shapes,report);receipt.update(task=task,status=result['status'],conforms=result['conforms']);shacl_runs.append(receipt)
  return result,data,shapes,report
 def fixture(case=EX.case):
  g=Graph()
  for t in [(case,RDF.type,RISK['RKM-X01']),(case,RDFS.label,Literal('Synthetic risk item')),(case,RISK['RX-001'],EX.context),(case,RISK['RX-003'],EX.objective),(EX.context,RDF.type,RISK['RKM-C002']),(EX.objective,RDF.type,RISK['RKM-X02'])]:g.add(t)
  return g
 def entry(g,approved=None,link=True):
  if link:
   for t in [(EX.case,APP.entry,EX.entry),(EX.entry,RDF.type,RISK['RKM-C022']),(EX.entry,RISK['R-01'],EX.case)]:g.add(t)
  if approved is not None:
   g.add((EX.case,APP.approved,Literal(approved)));g.add((EX.case,APP.approvalSource,EX.syntheticApprovalRecord))
  return g
 def fresh():
  db=history.connect();history.migrate(db,2)
  db.execute('INSERT INTO source_record VALUES(?,?)',(str(EX.source),'{}'))
  history.add_identity(db,str(EX.case),'case');db.execute('INSERT INTO risk_case VALUES(?,?,?,?)',(str(EX.case),'case','Same label',str(EX.source)))
  return db
 def artifact(db,key,kind):
  history.add_identity(db,str(key),'artifact');db.execute('INSERT INTO information_artifact VALUES(?,?,?,?,?)',(str(key),'artifact',kind,'Synthetic record',str(EX.source)))
 def addentry(db,key):
  if not db.execute('SELECT 1 FROM information_artifact WHERE artifact_id=?',(str(EX.register),)).fetchone():artifact(db,EX.register,'RKM-C030')
  artifact(db,key,'RKM-C022');db.execute('INSERT INTO register_entry(entry_id,case_id,register_id) VALUES(?,?,?)',(str(key),str(EX.case),str(EX.register)))
 def sql_graph(db):
  g=Graph()
  for s,q,o in db.execute('SELECT subject,predicate,object FROM v_native_facts'):g.add((URIRef(s),URIRef(q),URIRef(o)))
  return g
 def hermit(label,abox,expected='SAT'):
  g=Graph()+owl
  for t in abox:g.add(t)
  d=out/'hermit';d.mkdir(exist_ok=True);f=d/(label+'.rdf');g.serialize(f,format='xml')
  r,log=command(label,['java','-Xmx512m','-cp',a.robot,'org.semanticweb.HermiT.cli.CommandLine','-k',f])
  state=('UNSAT' if 'org.semanticweb.owlapi.reasoner.InconsistentOntologyException: Inconsistent ontology' in r.stderr else 'ERROR') if r.returncode else ('UNSAT' if 'not satisfiable' in r.stdout else ('SAT' if 'is satisfiable.' in r.stdout else 'ERROR'))
  receipt={'label':label,'expected':expected,'observed':state,'status':'PASS' if state==expected else 'FAIL','input_sha256':b.sha(f),'input_file':str(f.relative_to(out)),'log':log};hermit_runs.append(receipt)
  assert state==expected,receipt
  return receipt
 def absence(g,case,rel,inverse=False):
  restriction=BNode();prop=BNode() if inverse else RISK[rel]
  if inverse:g.add((prop,OWL.inverseOf,RISK[rel]))
  for t in [(restriction,RDF.type,OWL.Restriction),(restriction,OWL.onProperty,prop),(restriction,OWL.maxCardinality,Literal(0,datatype=XSD.nonNegativeInteger)),(case,RDF.type,restriction)]:g.add(t)
  return g
 def run(number,fn):
  oracle=oracles[number-1];start=time.monotonic()
  try:observation=fn();status='PASS'
  except Exception as e:observation={'error':repr(e)};status='FAIL'
  rows.append({'id':oracle['id'],'scope':oracle['scope'],'expected':oracle['expected'],'status':status,'observed':observation,'elapsed_ms':round((time.monotonic()-start)*1000)});print(oracle['id']+': '+status,flush=True)
 def c01():
  g=fixture();r,_,_,_=check(g,label='no-entry');assert r['conforms'];assert not list(g.subjects(RDF.type,RISK['RKM-C022'])) and not list(g.subjects(RDF.type,RISK['RKM-C004']))
  db=fresh();counts=[db.execute('SELECT count(*) FROM risk_case').fetchone()[0],db.execute('SELECT count(*) FROM register_entry').fetchone()[0]];assert counts==[1,0];db.close()
  h=hermit('H01-zero-register-entries',absence(fixture(),EX.case,'R-01',True));return {'task':r,'SQL_case_and_entry_counts':counts,'HermiT':h['observed'],'zero_entry_restriction_explicit':True}
 def c02():
  r,_,_,_=check(entry(fixture()),'operational-register',label='approval-unknown');assert r['status']=='INCOMPLETE_FOR_SELECTED_TASK' and r['approval']=='UNKNOWN';return r
 def c03():
  r,_,_,_=check(entry(fixture(),False),'operational-register',label='approval-denied');assert r['status']=='NOT_ELIGIBLE_FOR_SELECTED_TASK' and r['approval']=='DENIED';return r
 def c04():
  g=entry(fixture(),True);r,_,_,_=check(g,'operational-register',label='local-positive');s,_,_,_=check(g,label='same-analytical');assert r['conforms'] and s['conforms'];return {'operational':r,'analytical':s}
 def c05():
  r,_,_,_=check(entry(fixture(),True,False),'operational-register',label='entry-missing');assert r['status']=='INCOMPLETE_FOR_SELECTED_TASK';return r
 def c06():
  blank=BNode('case-blank');r,_,_,_=check(fixture(blank),focus=[blank],label='blank-identity');assert not r['conforms'] and any(x['component']==str(SH.NodeKindConstraintComponent) for x in r['findings'])
  db=fresh()
  try:history.add_identity(db,'bad identity','case');raise AssertionError('Invalid SQL identity accepted')
  except history.sqlite3.IntegrityError as e:error=str(e)
  db.close();return {'SHACL':r,'SQL_rejection':error,'raw_blank_preserved':True}
 def c07():
  g=fixture();g.remove((EX.case,RISK['RX-001'],None));r,_,_,_=check(g,label='context-missing');assert r['status']=='INCOMPLETE_FOR_SELECTED_TASK'
  h=hermit('H02-missing-explicit-context',g);n=hermit('H03-deny-context-existence',absence(Graph()+g,EX.case,'RX-001'),'UNSAT');return {'task':r,'missing_explicit_context':h['observed'],'context_existence_denied':n['observed']}
 def c08():
  g=fixture();g.remove((EX.case,RISK['RX-003'],None));r,_,_,_=check(g,label='objective-missing');assert r['status']=='INCOMPLETE_FOR_SELECTED_TASK'
  h=hermit('H04-missing-explicit-objective',g);n=hermit('H05-deny-objective-existence',absence(Graph()+g,EX.case,'RX-003'),'UNSAT');return {'task':r,'missing_explicit_objective':h['observed'],'objective_existence_denied':n['observed']}
 def c09():
  db=fresh();addentry(db,EX.entry1);addentry(db,EX.entry2);g=sql_graph(db);sql=[db.execute('SELECT count(*) FROM risk_case').fetchone()[0],db.execute('SELECT count(*) FROM register_entry').fetchone()[0]];rdf=[len(list(g.subjects(RDF.type,RISK['RKM-X01']))),len(list(g.subjects(RISK['R-01'],EX.case)))];assert sql==rdf==[1,2];db.close();return {'SQL':sql,'asserted_RDF':rdf}
 def c10():
  db=fresh();history.add_identity(db,str(EX.case2),'case');db.execute('INSERT INTO risk_case VALUES(?,?,?,?)',(str(EX.case2),'case','Same label',str(EX.source)));rows0=[list(r) for r in db.execute('SELECT case_id FROM risk_case WHERE label=? ORDER BY case_id',('Same label',))];assert len(rows0)==2;g=sql_graph(db);assert len(list(g.subjects(RDF.type,RISK['RKM-X01'])))==2;db.close()
  same=fixture()+fixture(EX.case2);same.add((EX.case,OWL.differentFrom,EX.case2));h=hermit('H06-equal-labels-distinct',same);return {'distinct_SQL_identifiers':rows0,'HermiT':h['observed'],'distinctness_explicit_not_adjudicated':True}
 def c11():
  db=fresh();addentry(db,EX.entry)
  try:db.execute('INSERT INTO risk_case VALUES(?,?,?,?)',(str(EX.entry),'case','Collision',str(EX.source)));raise AssertionError('Cross-family case identity accepted')
  except history.sqlite3.IntegrityError as e:error=str(e)
  assert db.execute('PRAGMA foreign_key_check').fetchall()==[];db.close();return {'SQL_rejection':error,'new_OWL_disjointness_added':False}
 def c12():
  g=fixture();g.add((EX.scenario,RDF.type,RISK['RKM-C003']));g.add((EX.scenario,RISK['R-36'],EX.case));answer=list(g.query('SELECT (COUNT(?o) AS ?n) WHERE { ?o a <'+str(RISK['RKM-C004'])+'> }'))[0][0].toPython();assert answer==0 and (EX.scenario,RISK['R-36'],EX.case) in g;return {'asserted_occurrence_query_count':answer,'scenario_link_retained':True,'not_a_claim_that_no_occurrence_exists':True}
 def c13():
  g=fixture()
  for i in [1,2]:
   n=EX['nature'+str(i)];ctx=EX['context'+str(i)];obj=EX['objective'+str(i)];term=EX['favorable' if i==2 else 'unfavorable']
   for t in [(n,RDF.type,RISK['RKM-C005']),(n,RISK['R-41'],EX.case),(n,RISK['R-42'],term),(n,RISK['R-43'],ctx),(n,APP.objective,obj),(ctx,RDF.type,RISK['RKM-C002']),(obj,RDF.type,RISK['RKM-X02']),(term,RDF.type,RISK['RKM-C006']),(EX.case,RISK['RX-003'],obj),(APP.objective,RDF.type,OWL.ObjectProperty)]:g.add(t)
  q='SELECT ?n ?term ?ctx ?obj WHERE {?n <'+str(RISK['R-41'])+'> <'+str(EX.case)+'>; <'+str(RISK['R-42'])+'> ?term; <'+str(RISK['R-43'])+'> ?ctx; <'+str(APP.objective)+'> ?obj} ORDER BY ?n';answers=[[str(v) for v in r] for r in g.query(q)];assert len(answers)==2 and len(list(g.subjects(RDF.type,RISK['RKM-X01'])))==1;h=hermit('H07-context-qualified-natures',g);return {'qualified_assertions':answers,'case_count':1,'HermiT':h['observed'],'objective_qualifier':'Local explicit-data property, not a new native relation.'}
 def c14():
  inputs=json.loads((b.IMPACT/'input-bindings.json').read_text())['inputs'];cohorts=[e for e in inputs if e['path'].startswith('evaluation/sources/')];assert all(b.sha(b.ROOT/e['path'])==e['sha256'] for e in cohorts);return {'unchanged_cohort_files':[e['path'] for e in cohorts],'new_real_case_admissions':0}
 def c15():
  try:p.evaluate(fixture(),[],'analytical-case');raise AssertionError('Empty request accepted')
  except ValueError as e:return {'request_rejected':str(e)}
 def c16():
  bads=[(EX.case,APP.requestedTask,Literal('raw')),(EX.case,RDFS.subClassOf,RISK['RKM-X01']),(RISK['RKM-X01'],OWL.sameAs,EX.case),(APP['request-0'],APP.entry,EX.entry)];errors=[]
  for triple in bads:
   g=fixture();g.add(triple)
   try:p.evaluate(g,[EX.case],'analytical-case');raise AssertionError('Untrusted selector/schema accepted')
   except ValueError as e:errors.append(str(e))
  try:p.evaluate(fixture(),[EX.case],'raw');raise AssertionError('Unselected lenient task accepted')
  except ValueError as e:errors.append(str(e))
  return {'rejected_requests':len(errors),'findings':errors}
 def c17():
  db=fresh();sql=[[r[0],r[1]] for r in db.execute('SELECT c.case_id,COUNT(e.entry_id) FROM risk_case c LEFT JOIN register_entry e ON e.case_id=c.case_id GROUP BY c.case_id ORDER BY c.case_id')];g=sql_graph(db);query='SELECT ?c (COUNT(?e) AS ?n) WHERE {?c a <'+str(RISK['RKM-X01'])+'> OPTIONAL {?e <'+str(RISK['R-01'])+'> ?c}} GROUP BY ?c ORDER BY ?c';rdf=[[str(r[0]),r[1].toPython()] for r in g.query(query)];assert sql==rdf==[[str(EX.case),0]]
  health={'integrity':db.execute('PRAGMA integrity_check').fetchone()[0],'foreign_key_violations':len(db.execute('PRAGMA foreign_key_check').fetchall())};assert health=={'integrity':'ok','foreign_key_violations':0};db.close();(out/'identity-query.rq').write_text(query+'\n');g.serialize(out/'identity-export.ttl',format='turtle');return {'columns':['case_id','entry_count'],'SQL':sql,'SPARQL':rdf,'health':health,'context_approval_persistence_claimed':False}
 def c18():
  g=entry(fixture());g.add((EX.case,APP.approvalSource,EX.syntheticApprovalRecord));r,data,shapes,_=check(g,'operational-register',label='approval-guard-negative');assert not r['conforms']
  mutant=Graph()+shapes
  for owner0,q,shape in list(mutant.triples((None,SH.property,None))):
   if str(shape).endswith('-approval'):mutant.remove((owner0,q,shape))
  ok,rep,_=validate(data,shacl_graph=mutant,inference='none',advanced=False,do_owl_imports=False);receipt=dataset(str(len(shacl_runs)+1).zfill(2)+'-approval-mutant',data,mutant,rep);receipt.update(task='operational-register-MUTANT',conforms=bool(ok));shacl_runs.append(receipt);assert bool(ok);return {'fixed_profile_conforms':False,'deleted_approval_rule_conforms':True,'fixed_negative_oracle_detects_mutation':True}
 def c19():
  g=entry(fixture(),True);g.remove((EX.entry,RISK['R-01'],None));g.add((EX.entry,RISK['R-01'],EX.otherCase));g.add((EX.otherCase,RDF.type,RISK['RKM-X01']));r,_,_,_=check(g,'operational-register',label='wrong-entry-case');assert r['status']=='NOT_ELIGIBLE_FOR_SELECTED_TASK'
  g.remove((EX.case,APP.approved,None));s,_,_,_=check(g,'operational-register',label='wrong-entry-and-unknown-approval');assert s['status']=='NOT_ELIGIBLE_FOR_SELECTED_TASK';return {'wrong_entry':r,'wrong_entry_and_unknown_approval':s}
 def c20():
  errors=[str(e.json_path)+': '+e.message for e in Draft202012Validator(json.loads(a.schema.read_text()),format_checker=FormatChecker(formats=['date','date-time','uri'])).iter_errors(native)];assert errors==[],errors
  r,sdk=command('native-sdk',[a.node,b.HERE.parent/'issue93-integration/native_roundtrip.cjs',b.HERE/'candidate.ontouml.json',a.sdk,out/'sdk-roundtrip.json']);assert r.returncode==0,r.stderr
  r,dl=command('owl-DL',['java','-Xmx512m','-jar',a.robot,'validate-profile','--input',b.HERE/'candidate.owl.ttl','--profile','DL','--output',out/'owl-profile-DL.txt']);assert r.returncode==0,r.stderr
  h=hermit('H08-whole-candidate',Graph());assert iso
  assert len(native['elements'])==596 and {s['id'] for s in model['generalization_set_policy']['retained_sets']}=={e['id'] for e in native['elements'] if e['type']=='GeneralizationSet'}
  return {'schema_errors':errors,'sdk_exit_code':sdk['exit_code'],'native_elements':596,'retained_sets':8,'logical_graph_isomorphic_to_prior_candidate':iso,'HermiT':h['observed'],'ROBOT_OWL2_DL_exit_code':dl['exit_code'],'reader':coverage}
 tests=[c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20]
 assert len(oracles)==len(tests)==20 and [r['id'] for r in oracles]==['RKC-'+str(i).zfill(2) for i in range(1,21)]
 for i,test in enumerate(tests,1):run(i,test)
 unchanged=before=={n:b.sha(b.ROOT/n) for n in before}
 report={'schema':'riskium-riskcase-candidate-verification-1','status':'PASS_B2_CANDIDATE_NOT_PUBLISHED' if all(r['status']=='PASS' for r in rows) and unchanged else 'FAIL','candidate_version':b.VERSION,
  'execution_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=b.ROOT,text=True).strip(),'input_contract_sha256':b.sha(b.CONTRACT),'oracle_sha256':b.sha(b.IMPACT/'acceptance-oracles.json'),
  'summary':{'planned_cases':20,'cases_executed':len(rows),'cases_matched':sum(r['status']=='PASS' for r in rows),'actual_SHACL_invocations':len(shacl_runs),'actual_HermiT_invocations':len(hermit_runs),'HermiT_matches':sum(r['status']=='PASS' for r in hermit_runs),'native_elements':596,'reader_pages':83,'reader_files':92,'reader_local_links':coverage['local_links_checked'],'historical_input_files_preserved':len(before)},
  'cases':rows,'SHACL_receipts':shacl_runs,'HermiT_receipts':hermit_runs,'commands':commands,'frozen_inputs_unchanged':unchanged,
  'profile_boundary':'Task readiness is not universal ontology admission. The local approval-source IRI is a provenance requirement, not independent authorization verification. No raw candidate or historical WITHHELD decision is promoted.',
  'boundary':'Actual synthetic candidate checks only. SQLite identity/history schema 2 is a bounded baseline slice; no PostgreSQL or full context/approval persistence. Logical consistency/isomorphism is not independent semantic adequacy. Current-source qualification, package publication and live maintained-channel readback remain R1/R2. Manuscript 7.2.21 and prior scientific receipts are unchanged.'}
 (out/'verification-report.json').write_text(b.dump(report));print(b.dump({'status':report['status'],'execution_commit':report['execution_commit'],'summary':report['summary']}),flush=True)
 return int(report['status']=='FAIL')
if __name__=='__main__':
 ap=argparse.ArgumentParser()
 for name in ['output','schema','robot','sdk','node']:ap.add_argument('--'+name,type=Path,required=True)
 args=ap.parse_args()
 for name in ['output','schema','robot','sdk','node']:setattr(args,name,getattr(args,name).resolve())
 raise SystemExit(main(args))
