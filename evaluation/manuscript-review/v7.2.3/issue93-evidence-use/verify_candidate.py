"""Execute scoped candidate tests; do not relabel historical test results."""
from pathlib import Path
from copy import deepcopy
import argparse,json,subprocess,time,re,importlib.util
from rdflib import Graph,Namespace,URIRef,Literal,BNode
from rdflib.namespace import RDF,RDFS,OWL,SH
from jsonschema import Draft202012Validator,FormatChecker
from pyshacl import validate
from build_candidate import HERE,ROOT,RISK,EU,FROZEN_SHA,digest,dumps,render
from validate_native import check_fidelity,SCHEMA_SHA256

EX=Namespace('urn:riskium:evidence-use-test:')
def clone(g):return Graph()+g
def fixture(purpose='support',suffix=''):
 g=Graph();u=EX['use'+suffix];ref=EX['ref'+suffix];item=EX.item;ctx=EX['claim'+suffix];ground=EX['grounding'+suffix]
 for s,c in [(u,'RKM-C075'),(ref,'RKM-C076'),(ref,'RKM-C065'),(ref,'RKM-C014'),(item,'RKM-C066'),(item,'RKM-C014'),(ctx,'RKM-C014'),(ground,'RKM-C014')]:g.add((s,RDF.type,RISK[c]))
 for p,o in [('RE-001',item),('RE-002',ref),('RE-003',ground)]:g.add((u,RISK[p],o))
 g.add((u,EU.context,ctx));g.add((u,EU.purpose,Literal(purpose)));g.add((ref,RISK['RX-021'],item));g.add((ref,RISK['R-68'],ctx))
 return g
def shcheck(g,shapes):
 ok,rg,rt=validate(g,shacl_graph=shapes,inference='none',advanced=False,allow_infos=False,allow_warnings=False)
 return bool(ok),[{'focus':str(rg.value(r,SH.focusNode)),'component':str(rg.value(r,SH.sourceConstraintComponent)),'message':str(rg.value(r,SH.resultMessage))} for r in rg.subjects(RDF.type,SH.ValidationResult)]
def cases():
 out=[]
 def add(n,g,e):out.append((n,g,e))
 add('valid-support',fixture(),True);add('valid-challenge',fixture('challenge'),True);add('valid-context',fixture('context'),True)
 add('same-artifact-two-uses',fixture()+fixture('challenge','2'),True)
 raw=Graph();raw.add((EX.item,RDF.type,RISK['RKM-C014']));add('artifact-without-evidential-role',raw,True)
 raw=Graph();raw.add((EX.ref,RDF.type,RISK['RKM-C065']));raw.add((EX.ref,RDF.type,RISK['RKM-C014']));add('reference-record-without-actual-use',raw,True)
 raw=Graph();raw.add((EX.ref,RDF.type,RISK['RKM-C076']));add('orphan-reference-role',raw,False)
 raw=Graph();raw.add((EX.item,RDF.type,RISK['RKM-C066']));add('orphan-typed-role',raw,False)
 raw=Graph();raw.add((EX.ref,RDF.type,RISK['RKM-C065']));raw.add((EX.ref,RISK['RX-021'],EX.item));raw.add((EX.item,RDF.type,RISK['RKM-C066']));add('pointer-without-grounded-use',raw,False)
 g=fixture();g.remove((EX.use,RISK['RE-003'],None));add('missing-grounding',g,False)
 g=fixture();g.remove((EX.use,EU.purpose,None));add('missing-purpose',g,False)
 add('invalid-purpose',fixture('proves-true'),False)
 g=fixture();g.remove((EX.use,RISK['RE-002'],None));add('missing-reference',g,False)
 g=fixture();g.remove((EX.use,RISK['RE-001'],None));add('missing-item',g,False)
 g=fixture();g.set((EX.use,RISK['RE-001'],EX.ref));g.add((EX.ref,RDF.type,RISK['RKM-C066']));g.set((EX.ref,RISK['RX-021'],EX.ref));g.remove((EX.item,None,None));add('same-mediated-individual',g,False)
 g=fixture();g.set((EX.ref,RISK['RX-021'],EX.otherItem));add('reference-points-to-other-item',g,False)
 g=fixture();g.set((EX.ref,RISK['R-68'],EX.otherClaim));add('context-mismatch',g,False)
 g=fixture();g.set((EX.use,EU.context,EX.otherClaim));g.add((EX.otherClaim,RDF.type,RISK['RKM-C014']));add('use-context-mismatch',g,False)
 return out
def role_dependency(m,subject='RKM-C066'):
 cs={c['id']:c for c in m['concepts']};anc={subject}
 while True:
  n=anc|{g['general'] for g in m['generalizations'] if g['specific'] in anc}
  if n==anc:break
  anc=n
 return any(r['target'] in anc and r.get('stereotype')=='mediation' and cs[r['source']]['ontouml_stereotype']=='relator' and int(r['source_end_cardinality'].split('..')[0])>=1 for r in m['associations'])
def native_checks(m,n,base):
 rows=[]
 def add(k,ok):rows.append({'id':k,'pass':bool(ok)})
 add('baseline-lacks-role-dependency',not role_dependency(base));add('candidate-has-role-dependency',role_dependency(m))
 add('reference-role-has-role-dependency',role_dependency(m,'RKM-C076'))
 mutated=deepcopy(m);next(r for r in mutated['associations'] if r['id']=='RE-001')['stereotype']=None
 add('ordinary-pointer-mutant-rejected',not role_dependency(mutated))
 mutated=deepcopy(m);next(r for r in mutated['associations'] if r['id']=='RE-001')['source_end_cardinality']='0..*'
 add('optional-dependency-mutant-rejected',not role_dependency(mutated))
 add('source-pointer-unmodified',next(r for r in m['associations'] if r['id']=='RX-021')==next(r for r in base['associations'] if r['id']=='RX-021'))
 add('all-subtype-links-retained',m['generalizations'][:-1]==base['generalizations'] and m['generalizations'][-1]['specific']=='RKM-C076' and m['generalizations'][-1]['general']=='RKM-C065')
 add('identity-supplier-retained',next(c for c in m['concepts'] if c['id']=='RKM-C066')['identity_supplier']=='RKM-C014')
 add('relator-mediates-two-minimum-participants',sum(int(r['target_end_cardinality'].split('..')[0]) for r in m['associations'] if r['source']=='RKM-C075' and r.get('stereotype')=='mediation')>=2)
 add('two-GSRig-sets-still-explicit',{'GS-RKM-C014','GS-RKM-C047'}<={e['id'] for e in n['elements'] if e['type']=='GeneralizationSet'})
 add('native-source-fidelity',check_fidelity(m,n)==[])
 add('ordinary-reference-definition-preserved',next(c for c in m['concepts'] if c['id']=='RKM-C065')==next(c for c in base['concepts'] if c['id']=='RKM-C065'))
 return rows
def command(args,timeout=60):
 start=time.monotonic();p=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
 return {'exit_code':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip(),'elapsed_ms':round(1000*(time.monotonic()-start))}
def reasoner_cases(robot,owl_graph,fs,outdir):
 rows=[];paths={name:g for name,g,_ in fs}
 specs=[('whole-candidate-consistent',None,True),('grounded-use-consistent','valid-support',True),('same-artifact-different-uses-consistent','same-artifact-two-uses',True),('same-participant-inconsistent','same-mediated-individual',False),('missing-explicit-use-open-world-consistent','orphan-typed-role',True),('missing-grounding-open-world-consistent','missing-grounding',True)]
 for name,fixture_name,expected in specs:
  graph=clone(owl_graph)
  if fixture_name:graph+=paths[fixture_name]
  fp=outdir/(name+'.rdf');graph.serialize(fp,format='xml')
  r=command(['java','-Xmx512m','-cp',str(robot),'org.semanticweb.HermiT.cli.CommandLine','-k',str(fp)])
  observed='is satisfiable.' in r['stdout'] and 'not satisfiable' not in r['stdout']
  if r['exit_code']!=0 and 'InconsistentOntologyException' in r['stderr']:observed=False
  r.update(id=name,expected_consistent=expected,observed_consistent=observed,input_sha256=digest(fp),status='PASS' if observed==expected and (r['exit_code']==0 or 'InconsistentOntologyException' in r['stderr']) else 'FAIL')
  rows.append(r)
 # Two names are not proof of distinctness: explicitly equating the participants must conflict.
 graph=clone(owl_graph)+fixture();graph.add((EX.ref,OWL.sameAs,EX.item));fp=outdir/'sameAs-participants.rdf';graph.serialize(fp,format='xml')
 r=command(['java','-Xmx512m','-cp',str(robot),'org.semanticweb.HermiT.cli.CommandLine','-k',str(fp)])
 bad=r['exit_code']!=0 and 'InconsistentOntologyException' in r['stderr']
 r.update(id='sameAs-participants-inconsistent',expected_consistent=False,observed_consistent=not bad,input_sha256=digest(fp),status='PASS' if bad else 'FAIL');rows.append(r)
 graph=clone(owl_graph)+fixture();prem=outdir/'no-occurrence-inference-premise.rdf';graph.serialize(prem,format='xml')
 conclusion=Graph();conclusion.add((RISK['RKM-C004'],RDF.type,OWL.Class));conclusion.add((EX.claim,RDF.type,OWL.NamedIndividual));conclusion.add((EX.claim,RDF.type,RISK['RKM-C004']));con=outdir/'no-occurrence-inference-conclusion.rdf';conclusion.serialize(con,format='xml')
 r=command(['java','-Xmx512m','-cp',str(robot),'org.semanticweb.HermiT.cli.CommandLine','--premise='+prem.as_uri(),'--conclusion='+con.as_uri(),'-E']);ok=r['exit_code']==0 and r['stdout']=='false'
 r.update(id='evidential-use-does-not-establish-occurrence',expected_entailment=False,observed_output=r['stdout'],input_sha256=digest(prem),conclusion_sha256=digest(con),status='PASS' if ok else 'FAIL');rows.append(r)
 return rows
def run(args):
 m,n,g=render();base=json.loads((ROOT/'ontology/riskium-model.json').read_text())
 assert digest(args.schema)==SCHEMA_SHA256
 schema_errors=[str(e.json_path)+': '+e.message for e in Draft202012Validator(json.loads(args.schema.read_text()),format_checker=FormatChecker(formats=['date','date-time','uri'])).iter_errors(n)]
 fs=cases();shapes=Graph().parse(HERE/'evidence-use.shacl.ttl',format='turtle');rows=[]
 fixtures=HERE/'fixtures';fixtures.mkdir(exist_ok=True)
 for name,data,expected in fs:
  data.serialize(fixtures/(name+'.ttl'),format='turtle');ok,findings=shcheck(data,shapes)
  rows.append({'id':name,'expected_conforms':expected,'observed_conforms':ok,'status':'PASS' if ok==expected else 'FAIL','findings':findings,'fixture_sha256':digest(fixtures/(name+'.ttl'))})
 mutants=[]
 for mid,case_id,edit in [
  ('M1-remove-role-dependency','orphan-typed-role','role'),('M2-remove-distinctness','same-mediated-individual','distinct'),('M3-remove-grounding','missing-grounding','ground'),('M4-remove-context-coherence','context-mismatch','context')]:
  sm=clone(shapes)
  if edit=='role':
   for p in list(sm.objects(EU.EvidenceItemShape,SH.property)):sm.remove((EU.EvidenceItemShape,SH.property,p))
  if edit=='distinct':sm.remove((None,SH.disjoint,None))
  if edit=='ground':
   for p in list(sm.objects(EU.EvidenceUseShape,SH.property)):
    if sm.value(p,SH.path)==RISK['RE-003']:sm.remove((EU.EvidenceUseShape,SH.property,p))
  if edit=='context':sm.remove((EU.EvidenceUseShape,SH.sparql,None))
  ok,_=shcheck(next(d for name,d,_ in fs if name==case_id),sm)
  mutants.append({'id':mid,'counterexample':case_id,'mutant_accepts_counterexample':ok,'status':'DETECTED' if ok else 'NOT_DETECTED'})
 outdir=HERE/'reasoner-inputs';outdir.mkdir(exist_ok=True)
 h=reasoner_cases(args.robot.resolve(),g,fs,outdir)
 profile=command(['java','-jar',str(args.robot.resolve()),'validate-profile','--profile','DL','--input',str(HERE/'candidate.owl.ttl'),'--output',str(HERE/'owl-profile-DL.txt')])
 nc=native_checks(m,n,base)
 spec=importlib.util.spec_from_file_location('historical_selected_screen',ROOT/'evaluation/manuscript-review/v7.1.0/supplement/analyze_model.py');screen=importlib.util.module_from_spec(spec);spec.loader.exec_module(screen)
 from build_native import generalization_sets
 classes={c['id']:c for c in m['concepts']+m['imported_types'] if c['scope_layer']=='FORMAL_CORE' or c['id']=='EXT-OBJECT'}
 selected,_=screen.screen(classes,[r for r in m['associations'] if r['scope_layer']=='FORMAL_CORE'],m['generalizations'],generalization_sets(m))
 assert set(selected['GSRig'])=={'GS-RKM-C014','GS-RKM-C047'} and selected['RelRig']==[]
 assert 'RKM-C075' in selected['RepRel']
 passed=not schema_errors and all(r['pass'] for r in nc) and all(r['status']=='PASS' for r in rows+h) and all(r['status']=='DETECTED' for r in mutants) and profile['exit_code']==0
 report={'schema':'riskium-evidence-use-candidate-v1','candidate_version':m['version'],'date':'2026-11-08','status':'PASS' if passed else 'FAIL',
  'baseline_commit':'07774a46b946d1a4cebb110e483cbe977c9635bd','historical_model_commit':'50f731aa5e065233c81fceeadaab8d87f5569de6',
  'production_model_sha256':digest(ROOT/'ontology/riskium-model.json'),'production_unchanged':digest(ROOT/'ontology/riskium-model.json')==FROZEN_SHA,
  'inputs_sha256':{p.name:digest(p) for p in [HERE/'build_candidate.py',HERE/'verify_candidate.py',HERE/'candidate-model.json',HERE/'candidate.ontouml.json',HERE/'candidate.owl.ttl',HERE/'evidence-use.shacl.ttl']},
  'engines':{'rdflib':'7.6.0','pyshacl':'0.30.1','ROBOT':'1.9.11','HermiT':'1.4.5.456 from ROBOT 1.9.11 bundle','robot_sha256':digest(args.robot),'native_schema_sha256':digest(args.schema)},
  'candidate_selected_pattern_screen':{'candidates':selected,'interpretation':'Two original GSRig sets remain for the next repair. EvidenceUseRelator is a repeatable-relator candidate by design: different grounded contexts or purposes can involve the same artifact/reference pair; duplicate descriptions of one use do not create new identity. No full instance-identity adjudication is claimed. Topological relation-specialization candidates are not property-equivalence results.'},
  'native_schema_errors':schema_errors,'native_checks':nc,'explicit_data_cases':rows,'shape_mutants':mutants,'hermit_cases':h,'owl_profile':profile,
  'summary':{'native_checks':len(nc),'native_checks_passed':sum(r['pass'] for r in nc),'explicit_data_cases':len(rows),'explicit_data_cases_matching':sum(r['status']=='PASS' for r in rows),'negative_data_controls':sum(not x[2] for x in fs),'shape_mutants':len(mutants),'mutants_detected':sum(r['status']=='DETECTED' for r in mutants),'hermit_cases':len(h),'hermit_cases_matching':sum(r['status']=='PASS' for r in h),'owl2_dl':profile['exit_code']==0},
  'boundary':'A candidate implementation and scoped tests, not independent conceptual validation, actual use of a real source artifact, production migration, full identity adjudication, whole-model pattern acceptance or a release. Other two GSRig repairs remain open. Historical engine counts and manuscript evidence are unchanged.'}
 (HERE/'candidate-report.json').write_text(dumps(report));print(dumps({'status':report['status'],**report['summary']}))
 return 0 if passed else 1

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--schema',type=Path,required=True);p.add_argument('--robot',type=Path,required=True)
 raise SystemExit(run(p.parse_args()))
