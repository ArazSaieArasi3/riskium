"""Verify the two explicit set-policy repairs with positive and negative oracles."""
from pathlib import Path
from copy import deepcopy
import argparse,importlib.util,json,subprocess,time
from rdflib import Graph,Namespace,URIRef,BNode
from rdflib.namespace import RDF,RDFS,OWL
from rdflib.collection import Collection
from rdflib.compare import isomorphic
from jsonschema import Draft202012Validator,FormatChecker
from build_candidate import HERE,ROOT,PREVIOUS,RISK,VERSION,REMOVED,render,dumps,digest,old,build_native
from validate_native import SCHEMA_SHA256

EX=Namespace('urn:riskium:set-policy-test:')
def run_command(cmd):
 start=time.monotonic();r=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
 return dict(exit_code=r.returncode,stdout=r.stdout.strip(),stderr=r.stderr.strip(),elapsed_ms=round(1000*(time.monotonic()-start)))
def screen(model,sets):
 spec=importlib.util.spec_from_file_location('selected_screen',ROOT/'evaluation/manuscript-review/v7.1.0/supplement/analyze_model.py')
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 classes={c['id']:c for c in model['concepts']+model['imported_types'] if c['scope_layer']=='FORMAL_CORE' or c['id']=='EXT-OBJECT'}
 return mod.screen(classes,[r for r in model['associations'] if r['scope_layer']=='FORMAL_CORE'],model['generalizations'],sets)[0]
def native_fidelity(model,native):
 # Check the actual candidate against the source and explicit policy. Do not
 # pretend that the frozen ten-set checker accepts the changed eight-set policy.
 legacy=build_native.build(model,digest(HERE/'candidate-model.json'))
 oldby={e['id']:e for e in legacy['elements']};by={e['id']:e for e in native['elements']}
 oldset={e['id'] for e in legacy['elements'] if e['type']=='GeneralizationSet'}
 pol={s['id']:s for s in model['generalization_set_policy']['retained_sets']}
 errors=[]
 if set(by)!=(set(oldby)-REMOVED):errors.append('Unexpected element allocation')
 for i,e in oldby.items():
  if e['type'] in ['GeneralizationSet','Package']:continue
  if by.get(i)!=e:errors.append('Non-set source element changed: '+i)
 for i,e in oldby.items():
  if e['type']!='Package':continue
  target=by.get(i,{})
  if [x for x in e['contents'] if x not in oldset]!=[x for x in target.get('contents',[]) if x not in oldset]:errors.append('Non-set package content changed: '+i)
 for i,s in pol.items():
  e=by.get(i,{})
  if any(e.get(k)!=s[k] for k in ['generalizations','isDisjoint','isComplete']):errors.append('Policy mismatch: '+i)
  if e.get('customProperties',{}).get('specializationCriterion')!=s['specialization_criterion']:errors.append('Criterion missing: '+i)
  if sum(i in e.get('contents',[]) for e in by.values() if e['type']=='Package')!=1:errors.append('Set owner missing or duplicated: '+i)
 for e in by.values():
  for k in ['properties','contents','generalizations']:
   if any(x not in by for x in e.get(k,[])):errors.append('Dangling reference: '+e['id'])
 return sorted(set(errors))
def no_metadata(graph):
 g=Graph()+graph
 for p in [OWL.versionIRI,RDFS.label,RISK.sourceDigest,RISK.nativeDigest]:g.remove((old.ONTO,p,None))
 return g
def data(*classes):
 g=Graph()
 for c in classes:g.add((EX.subject,RDF.type,RISK[c]))
 return g
def consistency(robot,graph,name,out):
 file=out/(name+'.rdf');graph.serialize(file,format='xml')
 r=run_command(['java','-Xmx512m','-cp',str(robot),'org.semanticweb.HermiT.cli.CommandLine','-k',str(file)])
 if r['exit_code']==0 and 'is satisfiable.' in r['stdout'] and 'not satisfiable' not in r['stdout']:value=True
 elif 'InconsistentOntologyException' in r['stderr'] or 'not satisfiable' in r['stdout']:value=False
 else:value=None
 r.update(input_sha256=digest(file),observed_consistent=value)
 return r
def entailment(robot,premise,conclusion,name,out):
 pre=out/(name+'-premise.rdf');con=out/(name+'-conclusion.rdf')
 premise.serialize(pre,format='xml');conclusion.serialize(con,format='xml')
 r=run_command(['java','-Xmx512m','-cp',str(robot),'org.semanticweb.HermiT.cli.CommandLine','--premise='+pre.as_uri(),'--conclusion='+con.as_uri(),'-E'])
 value={'true':True,'false':False}.get(r['stdout']) if r['exit_code']==0 else None
 r.update(input_sha256=digest(pre),conclusion_sha256=digest(con),observed_entailment=value)
 return r
def verify(args):
 m,n,g=render();_,before=old.candidate_model()
 policy=m['generalization_set_policy'];sets=policy['retained_sets'];out=HERE/'reasoner-inputs';out.mkdir(exist_ok=True)
 assert digest(args.schema)==SCHEMA_SHA256
 schema_errors=[str(e.json_path)+': '+e.message for e in Draft202012Validator(json.loads(args.schema.read_text()),format_checker=FormatChecker(formats=['date','date-time','uri'])).iter_errors(n)]
 findings=screen(m,sets);original=build_native.generalization_sets(m);rows=[]
 def check(k,ok):rows.append(dict(id=k,status='PASS' if ok else 'FAIL'))
 errors=native_fidelity(m,n)
 check('native-fidelity-to-explicit-policy',not errors)
 check('all-67-subtype-links-retained',m['generalizations']==before['generalizations'] and len(m['generalizations'])==67)
 check('all-concepts-relations-constraints-retained',all(m[k]==before[k] for k in ['concepts','associations','constraints']))
 check('exactly-two-focal-sets-removed',{s['id'] for s in original}-{s['id'] for s in sets}==REMOVED and len(sets)==8)
 check('selected-GSRig-no-longer-triggered',findings['GSRig']==[])
 check('bearer-kinds-disjoint-incomplete',next(s for s in sets if s['id']=='GS-AgentKinds')['isDisjoint'] and not next(s for s in sets if s['id']=='GS-AgentKinds')['isComplete'])
 check('all-three-disjointness-decisions-preserved',{s['id'] for s in sets if s['isDisjoint']}=={s['id'] for s in original if s['isDisjoint']})
 check('no-unjustified-covering-sets',not any(s['isComplete'] for s in sets))
 check('no-role-exclusivity-added',all(not s['isDisjoint'] for s in sets if s['id'] in {'GS-RKM-C048','GS-RKM-C049'}))
 check('positive-screen-control-retains-original-triggers',set(screen(m,original)['GSRig'])==REMOVED)
 prior_graph=Graph().parse(PREVIOUS/'candidate.owl.ttl',format='turtle')
 check('OWL-logical-graph-preserved',isomorphic(no_metadata(g),no_metadata(prior_graph)))
 check('production-model-unchanged',digest(ROOT/'ontology/riskium-model.json')==old.FROZEN_SHA)
 hermit=[]
 for name,ds,expected in [
  ('whole-candidate-consistent',Graph(),True),('person-and-organization-exclusive',data('RKM-C048','RKM-C049'),False),
  ('same-person-responsible-and-authorizing',data('RKM-C055','RKM-C057'),True),
  ('documentary-subkind-and-evidence-role-overlap',data('RKM-C022','RKM-C066'),True),
  ('human-and-organization-role-bearers-exclusive',data('RKM-C055','RKM-C056'),False),
  ('agent-without-declared-bearer-subkind-allowed',data('RKM-C047'),True)]:
  r=consistency(args.robot,g+ds,name,out);r.update(id=name,expected_consistent=expected,status='PASS' if r['observed_consistent']==expected else 'FAIL');hermit.append(r)
 con=Graph()
 for ge in m['generalizations']:
  for cid in [ge['specific'],ge['general']]:con.add((RISK[cid],RDF.type,OWL.Class))
  con.add((RISK[ge['specific']],RDFS.subClassOf,RISK[ge['general']]))
 r=entailment(args.robot,g,con,'all-source-subtype-links',out);r.update(id='all-67-source-subtype-links-entailed',expected_entailment=True,status='PASS' if r['observed_entailment'] is True else 'FAIL');hermit.append(r)
 con=Graph();union=BNode();head=BNode();Collection(con,head,[RISK['RKM-C048'],RISK['RKM-C049']]);con.add((union,RDF.type,OWL.Class));con.add((union,OWL.unionOf,head))
 for c in ['RKM-C047','RKM-C048','RKM-C049']:con.add((RISK[c],RDF.type,OWL.Class))
 con.add((RISK['RKM-C047'],RDFS.subClassOf,union))
 r=entailment(args.robot,g,con,'no-agent-covering-axiom',out);r.update(id='agent-not-exhausted-by-person-organization',expected_entailment=False,status='PASS' if r['observed_entailment'] is False else 'FAIL');hermit.append(r)
 mutants=[]
 for mid in sorted(REMOVED):
  ms=sets+[deepcopy(next(s for s in original if s['id']==mid))]
  detected=mid in screen(m,ms)['GSRig'];mutants.append(dict(id='restore-'+mid,status='DETECTED' if detected else 'NOT_DETECTED',unit='native set-policy trigger'))
 broken=deepcopy(n);broken['elements']=[e for e in broken['elements'] if e['id']!='GE-001']
 mutants.append(dict(id='delete-valid-subtype-link',status='DETECTED' if native_fidelity(m,broken) else 'NOT_DETECTED',unit='native source fidelity'))
 mg=Graph()+g
 for node in list(mg.subjects(RDF.type,OWL.AllDisjointClasses)):
  head=mg.value(node,OWL.members)
  if head and set(Collection(mg,head))=={RISK['RKM-C048'],RISK['RKM-C049']}:mg.remove((node,None,None))
 r=consistency(args.robot,mg+data('RKM-C048','RKM-C049'),'mutant-no-bearer-exclusivity',out)
 mutants.append(dict(id='remove-bearer-exclusivity',status='DETECTED' if r['observed_consistent'] is True else 'NOT_DETECTED',unit='HermiT mutation',execution=r))
 mg=Graph()+g;mg.add((RISK['RKM-C053'],OWL.disjointWith,RISK['RKM-C054']))
 r=consistency(args.robot,mg+data('RKM-C055','RKM-C057'),'mutant-global-role-exclusivity',out)
 mutants.append(dict(id='add-global-role-exclusivity',status='DETECTED' if r['observed_consistent'] is False else 'NOT_DETECTED',unit='HermiT mutation',execution=r))
 profile=run_command(['java','-jar',str(args.robot),'validate-profile','--profile','DL','--input',str(HERE/'candidate.owl.ttl'),'--output',str(HERE/'owl-profile-DL.txt')])
 good=not schema_errors and all(r['status']=='PASS' for r in rows+hermit) and all(r['status']=='DETECTED' for r in mutants) and profile['exit_code']==0
 report={'schema':'riskium-explicit-set-policy-candidate-v1','candidate_version':VERSION,'date':'2026-11-08','status':'PASS' if good else 'FAIL',
  'previous_candidate_commit':'b81549f2a9b139fef5feae57f3a2e2f8008b32a8','baseline_main_commit':'07774a46b946d1a4cebb110e483cbe977c9635bd',
  'inputs_sha256':{p.name:digest(p) for p in [HERE/'build_candidate.py',HERE/'verify_candidate.py',HERE/'candidate-model.json',HERE/'candidate.ontouml.json',HERE/'candidate.owl.ttl',HERE/'set-policy.json']},
  'dependencies_sha256':{'previous_candidate_builder':digest(PREVIOUS/'build_candidate.py'),'legacy_element_serializer':digest(ROOT/'tools/build_native.py'),'selected_trigger_screen':digest(ROOT/'evaluation/manuscript-review/v7.1.0/supplement/analyze_model.py'),'native_schema':digest(args.schema),'robot':digest(args.robot)},
  'engines':{'HermiT':'1.4.5.456 bundled in ROBOT 1.9.11','ROBOT':'1.9.11','rdflib':'7.6.0','jsonschema':'4.25.1'},
  'inventory':{'catalog_concepts':len(m['concepts']),'associations':len(m['associations']),'subtype_links':len(m['generalizations']),'generalization_sets':len(sets),'native_elements':len(n['elements'])},
  'native_schema_errors':schema_errors,'native_fidelity_errors':errors,'source_policy_checks':rows,'hermit_cases':hermit,'mutation_controls':mutants,'owl_profile':profile,'selected_pattern_candidates':findings,
  'summary':{'source_policy_checks':len(rows),'source_policy_checks_passed':sum(r['status']=='PASS' for r in rows),'native_schema_errors':len(schema_errors),'retained_sets':len(sets),'retained_subtype_links':len(m['generalizations']),'selected_GSRig_candidates':len(findings['GSRig']),'hermit_cases':len(hermit),'hermit_cases_matching':sum(r['status']=='PASS' for r in hermit),'mutation_controls':len(mutants),'mutation_controls_detected':sum(r['status']=='DETECTED' for r in mutants),'owl2_dl':profile['exit_code']==0},
  'boundary':'Both focal grouping repairs are implemented in an isolated combined candidate. Other retained sets and catalogue triggers are not independently accepted. No production promotion, database migration, release or replacement of manuscript historical engine counts is claimed. B0-3 integration review remains open.'}
 (HERE/'candidate-report.json').write_text(dumps(report));print(dumps({'status':report['status'],**report['summary']}))
 return int(not good)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--schema',type=Path,required=True);p.add_argument('--robot',type=Path,required=True);a=p.parse_args();a.schema=a.schema.resolve();a.robot=a.robot.resolve();raise SystemExit(verify(a))
