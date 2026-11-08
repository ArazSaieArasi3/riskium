"""Execute combined-candidate checks and concrete downstream compatibility probes."""
from pathlib import Path
from copy import deepcopy
import argparse,importlib.util,json,subprocess,sys,time,sqlite3
from unittest.mock import patch
from hashlib import sha256
from rdflib import Graph,Namespace,URIRef,Literal,BNode
from rdflib.namespace import RDF,RDFS,OWL,SH
from rdflib.collection import Collection
from pyshacl import validate
from jsonschema import Draft202012Validator,FormatChecker

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
E=HERE.parent/'issue93-evidence-use';G=HERE.parent/'issue93-generalization-sets'
sys.path.insert(0,str(E))
import verify_candidate as evidence_checks
spec=importlib.util.spec_from_file_location('combined_builder',G/'build_candidate.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
RISK=builder.RISK;EU=evidence_checks.EU;EX=evidence_checks.EX
def digest(p):return sha256(Path(p).read_bytes()).hexdigest()
def dumps(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def load(p):return json.loads(Path(p).read_text())
def command(args,timeout=90):
 start=time.monotonic();p=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
 return dict(exit_code=p.returncode,stdout=p.stdout.strip(),stderr=p.stderr.strip(),elapsed_ms=round((time.monotonic()-start)*1000))
def make_shapes():
 import build_shacl
 base=Graph().parse(E/'evidence-use.shacl.ttl',format='turtle')
 guard=BNode();base.add((EU.EvidenceUseShape,SH.sparql,guard))
 base.add((guard,SH.message,Literal('The two mediated participants must not be aliases under explicit sameAs paths.')))
 base.add((guard,SH.select,Literal('''PREFIX risk: <https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#>
 PREFIX owl: <http://www.w3.org/2002/07/owl#>
 SELECT $this WHERE { $this risk:RE-001 ?item ; risk:RE-002 ?ref .
 FILTER EXISTS { ?item (owl:sameAs|^owl:sameAs)+ ?ref } }''')))
 combined=base+build_shacl.managed()
 combined.serialize(HERE/'combined-managed.shacl.ttl',format='turtle')
 return combined
def shcheck(data,shapes,owl):
 ok,rg,_=validate(data,shacl_graph=shapes,ont_graph=owl,inference='none',advanced=False,do_owl_imports=False)
 return bool(ok),[dict(focus=str(rg.value(r,SH.focusNode)),component=str(rg.value(r,SH.sourceConstraintComponent)),message=str(rg.value(r,SH.resultMessage))) for r in rg.subjects(RDF.type,SH.ValidationResult)]
def relation_projection_probe(shapes,owl):
 import run_relational_evidence as run
 import relational_evidence as ev
 db=run.fresh();run.populate(db);rows=[]
 for r in run.fixture()['records']:
  graph=ev.native_graph(db,r['version_id']);ok,findings=shcheck(graph,shapes,owl)
  rows.append(dict(version=r['version_id'],triples=len(graph),candidate_conforms=ok,
   missing_use_relators=not any(graph.subjects(RDF.type,RISK['RKM-C075'])),
   missing_reference_roles=not any(graph.subjects(RDF.type,RISK['RKM-C076'])),
   finding_components=sorted({x['component'] for x in findings})))
 health={'sqlite':sqlite3.sqlite_version,'integrity':db.execute('PRAGMA integrity_check').fetchone()[0],'foreign_key_violations':len(db.execute('PRAGMA foreign_key_check').fetchall())}
 db.close()
 return {'scope':'Existing synthetic SQLite v7 qualified-evidence fixture; not pharmaceutical source records or production data.',
  'health':health,'records':rows,'migration_ready':False,
  'reason':'Existing exports have contextual EvidenceItem typing but no explicit use relator, participating reference role, or use-grounding record. A reference must not be backfilled into an actual-use fact without justification.'}
def adapter_probes(model,native):
 import build_owl,build_concept_dictionary,build_shacl,build_native
 model_path=G/'candidate-model.json';native_path=G/'candidate.ontouml.json'
 review=load(ROOT/'evaluation/native-review-decisions.json');review['source_model_sha256']=digest(model_path);review['generalization_sets']=model['generalization_set_policy']['retained_sets']
 temp=HERE/'generated';temp.mkdir(exist_ok=True);rp=temp/'candidate-review-input.json';rp.write_text(dumps(review))
 probes=[]
 with patch.object(build_owl,'SOURCE',model_path),patch.object(build_owl,'NATIVE',native_path),patch.object(build_owl,'POLICY',rp):
  try:build_owl.render();result='UNEXPECTED_ACCEPTANCE'
  except ValueError as e:result=str(e)
 probes.append(dict(id='production-owl-generator',observed=result,ready=False,action='Add an explicit candidate source/profile input contract; retain frozen 0.3.1 generation and historical receipts. Do not remove version/count guards without replacement checks.'))
 legacy=build_native.build(model,digest(model_path));oldsets={e['id'] for e in legacy['elements'] if e['type']=='GeneralizationSet'};newsets={e['id'] for e in native['elements'] if e['type']=='GeneralizationSet'}
 probes.append(dict(id='production-native-set-policy',regenerated_extra_sets=sorted(oldsets-newsets),ready=False,action='Route the explicit generalization-set policy through a candidate-aware serializer before replacing the production source.'))
 struct=temp/'candidate-structural-binding.json';struct.write_text(dumps({'model_sha256':digest(model_path)}))
 with patch.object(build_concept_dictionary,'MODEL',model_path),patch.object(build_concept_dictionary,'REPORT',struct):
  try:build_concept_dictionary.build();result='UNEXPECTED_ACCEPTANCE'
  except ValueError as e:result=str(e)
 probes.append(dict(id='production-concept-dictionary',observed=result,ready=False,action='Generate a separately version-bound dictionary/structural receipt for 82 concepts; preserve archived 80-concept pages.'))
 return probes
def documents(model):
 dest=HERE/'definitions';dest.mkdir(exist_ok=True);cs={c['id']:c for c in model['concepts']}
 for cid in ['RKM-C014','RKM-C047','RKM-C065','RKM-C066','RKM-C075','RKM-C076']:
  c=cs[cid];parents=[g['general'] for g in model['generalizations'] if g['specific']==cid]
  links=[r for r in model['associations'] if cid in [r['source'],r['target']]]
  lines=['# '+c['title'],'','Isolated combined candidate '+model['version']+'; not a published current definition.','',c['definition'],'',
   '- Source ID: '+cid,'- Stereotype: '+c['ontouml_stereotype'],'- Identity supplier: '+(c['identity_supplier'] or 'No single supplier; identity follows the bearer kind'),'- Identity basis: '+c['identity_basis'],
   '- Direct parents: '+(', '.join(parents) or 'None'),'', '## Integration interpretation','']
  note={'RKM-C014':'Documentary identity is retained. The blanket set mixing documentary specialization and evidential use is omitted; individual subtype edges remain.',
   'RKM-C047':'Bearer-kind classification remains separate from mandate participation. AgentKinds remains disjoint and incomplete; responsible/authorizing participation is not globally exclusive.',
   'RKM-C065':'The documentary reference and its proposed evidential reading do not alone establish actual evidential use. Participation is expressed by EvidenceReferenceRole and the grounded use relationship.',
   'RKM-C066':'The artifact retains documentary identity and participates through RE-001 in a grounded use; pointer RX-021 is still ordinary. Explicit aliases between the two mediated participants are rejected by the integration profile.',
   'RKM-C075':'Two distinct documentary participants, a grounding record, context and purpose qualify this proposed relationship. Database export cannot invent it from a citation record.',
   'RKM-C076':'The participating reference inherits documentary identity through EvidenceReference. A proposed-use record remains distinct from actual participation.'}
  lines+=[note[cid],'','## Incident relations','', '| ID | Source | Predicate | Target |','|---|---|---|---|']
  lines+=['| '+r['id']+' | '+r['source']+' | '+r['predicate']+' | '+r['target']+' |' for r in links]
  (dest/(cid+'.md')).write_text('\n'.join(lines)+'\n')
 # Exact selected class/relation fragment with explicit label placement.
 from html import escape
 positions={'RKM-C014':(400,20,240,80),'RKM-C065':(710,200,270,80),'RKM-C066':(40,200,230,80),'RKM-C075':(300,580,280,80),'RKM-C076':(710,400,270,80)}
 parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="725" viewBox="0 0 1100 725">',
 '<rect width="1100" height="725" fill="white"/><defs><marker id="generalization" markerWidth="16" markerHeight="16" refX="15" refY="8" orient="auto" markerUnits="userSpaceOnUse"><path d="M15 8 L1 1 L1 15 Z" fill="white" stroke="#475569"/></marker></defs>',
 '<g fill="none" stroke="#475569" stroke-width="1.5">',
 '<path d="M155 200 L455 100" marker-end="url(#generalization)"/><path d="M845 200 L585 100" marker-end="url(#generalization)"/><path d="M845 400 V280" marker-end="url(#generalization)"/>',
 '<path d="M710 240 H270"/><path d="M900 200 H1030 V60 H640"/>',
 '<path d="M355 580 L155 280"/><path d="M580 620 L845 480"/><path d="M300 620 H15 V60 H400"/></g>']
 for cid,(x,y,w,h) in positions.items():
  c=cs[cid];fill='#e9e3f4' if cid=='RKM-C014' else '#e4e8f0'
  parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#475569" stroke-width="1.5"/>')
  for yy,text,size in [(y+22,'«'+c['ontouml_stereotype']+'»',15),(y+46,c['title'],17),(y+66,cid,13)]:parts.append(f'<text x="{x+w/2}" y="{yy}" text-anchor="middle" font-family="Arial, sans-serif" font-size="{size}" fill="#1e293b">{escape(text)}</text>')
 rels={r['id']:r for r in model['associations']}
 def label(x,y,text,size=13,anchor='middle',rotation=None):
  width=len(text)*size*0.55+8
  parts.append(f'<g transform="translate({x} {y}) rotate({rotation or 0})"><rect x="{-width/2}" y="{-size+1}" width="{width}" height="{size+5}" fill="white"/><text text-anchor="{anchor}" font-family="Arial, sans-serif" font-size="{size}" fill="#1e293b">{escape(text)}</text></g>')
 for rid,x,y in [('RX-021',490,226),('R-68',885,123),('RE-001',215,405),('RE-002',735,570),('RE-003',15,350)]:
  label(x,y,rid+' '+rels[rid]['predicate'],rotation=-90 if rid=='RE-003' else None)
  if rels[rid].get('stereotype')=='mediation':label(x,y+18,'«mediation»',12)
 for rid,source,target in [('RX-021',(687,257),(286,257)),('R-68',(925,192),(665,51)),('RE-001',(333,560),(159,305)),('RE-002',(607,636),(839,505)),('RE-003',(275,640),(375,48))]:
  label(*source,rels[rid]['source_end_cardinality']);label(*target,rels[rid]['target_end_cardinality'])
 label(550,695,'Isolated candidate fragment. Hollow triangles denote inheritance; ordinary and mediation lines have no navigability arrows.',12)
 label(550,714,'Grounded evidential use does not establish the truth of the referenced claim. Context and purpose attributes are omitted.',12)
 parts.append('</svg>');(HERE/'evidence-fragment.svg').write_text(''.join(parts))

def main(a):
 frozen={p:digest(ROOT/p) for p in ['ontology/riskium-model.json','ontology/native/riskium.ontouml.json','ontology/derived/riskium.owl.ttl','evaluation/native-review-decisions.json']}
 assert digest(a.schema)==evidence_checks.SCHEMA_SHA256
 assert digest(a.robot)=='53cd275c8e4c0dad1fc2c1c34174876795cd7d6b6926e1444adcbb0cb3c7ab26'
 m,n,owl=builder.render();documents(m)
 owl.serialize(HERE/'generated-premise.rdf',format='xml')
 shapes=make_shapes();fixtures=evidence_checks.cases()
 g=evidence_checks.fixture();g.add((EX.item,OWL.sameAs,EX.ref));fixtures.append(('aliased-participants',g,False))
 g=evidence_checks.fixture();g.add((EX.item,OWL.sameAs,EX.alias));g.add((EX.ref,OWL.sameAs,EX.alias));fixtures.append(('alias-chain-participants',g,False))
 rows=[]
 for name,graph,expected in fixtures:
  ok,findings=shcheck(graph,shapes,owl);rows.append(dict(id=name,expected_conforms=expected,observed_conforms=ok,status='PASS' if ok==expected else 'FAIL',findings=findings))
 mutated=Graph()+shapes
 for constraint in list(mutated.objects(EU.EvidenceUseShape,SH.sparql)):
  if 'sameAs' in str(mutated.value(constraint,SH.select)):mutated.remove((EU.EvidenceUseShape,SH.sparql,constraint))
 mutant_ok,_=shcheck(fixtures[-2][1],mutated,owl)
 schema_errors=[str(e.json_path)+': '+e.message for e in Draft202012Validator(load(a.schema),format_checker=FormatChecker(formats=['date','date-time','uri'])).iter_errors(n)]
 sdk=command([str(a.node),str(HERE/'native_roundtrip.cjs'),str(G/'candidate.ontouml.json'),str(a.sdk),str(HERE/'native-roundtrip.json')])
 assert sdk['exit_code']==0,sdk
 h=command(['java','-Xmx512m','-cp',str(a.robot),'org.semanticweb.HermiT.cli.CommandLine','-k',str(HERE/'generated-premise.rdf')])
 consistent=h['exit_code']==0 and 'is satisfiable.' in h['stdout'] and 'not satisfiable' not in h['stdout']
 db=relation_projection_probe(shapes,owl);adapters=adapter_probes(m,n)
 unchanged=all(digest(ROOT/p)==sha for p,sha in frozen.items())
 bound=load(G/'candidate-report.json')['inputs_sha256']
 scope_checks={'source_model_and_native_match_B02_receipt':all(digest(G/name)==bound[name] for name in ['candidate-model.json','candidate.ontouml.json']),
  'focal_mixed_sets_absent':not {'GS-RKM-C014','GS-RKM-C047'} & {e['id'] for e in n['elements'] if e['type']=='GeneralizationSet'},
  'candidate_schema_valid':not schema_errors,'sdk_roundtrip':load(HERE/'native-roundtrip.json')['status']=='PASS','candidate_owl_consistent':consistent,
  'all_combined_data_expectations_match':all(r['status']=='PASS' for r in rows),'alias_guard_mutation_detected':mutant_ok,
  'old_database_integrity_retained':db['health']['integrity']=='ok' and db['health']['foreign_key_violations']==0,
  'old_projection_gap_demonstrated':all(not r['candidate_conforms'] and r['missing_use_relators'] for r in db['records']),
  'production_owl_guard_rejects_unqualified_candidate':adapters[0]['observed']!='UNEXPECTED_ACCEPTANCE',
  'production_dictionary_guard_rejects_unqualified_candidate':adapters[2]['observed']!='UNEXPECTED_ACCEPTANCE',
  'legacy_native_regroups_exactly_two_sets':adapters[1]['regenerated_extra_sets']==['GS-RKM-C014','GS-RKM-C047'],
  'frozen_model_exports_and_review_unchanged':unchanged}
 report={'schema':'riskium-issue93-integration-v1','date':'2026-11-08','candidate_version':m['version'],
  'candidate_source_commit':'74aedfb386f78210b17a2c87cafeee03f4093494',
  'status':'INTEGRATION_CHECKS_PASS_PROMOTION_BLOCKED' if all(scope_checks.values()) else 'CHECK_FAILURE',
  'checks':scope_checks,'native_schema_errors':schema_errors,'native_sdk':load(HERE/'native-roundtrip.json'),
  'fresh_hermit_consistency':h,'combined_shacl_cases':rows,'alias_mutant_accepts_counterexample':mutant_ok,'database_bridge':db,'production_adapter_probes':adapters,
  'source_hashes':{p.name:digest(p) for p in [G/'candidate-model.json',G/'candidate.ontouml.json',G/'candidate.owl.ttl',HERE/'combined-managed.shacl.ttl',HERE/'check_integration.py',HERE/'native_roundtrip.cjs']},
  'production_hashes_preserved':frozen,'summary':{'integration_checks':len(scope_checks),'integration_checks_passed':sum(scope_checks.values()),'combined_shacl_cases':len(rows),'combined_shacl_matches':sum(r['status']=='PASS' for r in rows),'negative_data_controls':sum(not e for _,_,e in fixtures),'sdk_elements':len(n['elements']),'legacy_projection_records':len(db['records']),'legacy_projection_records_ready_for_candidate':sum(r['candidate_conforms'] for r in db['records']),'candidate_definition_pages':6,'production_promoted':False},
  'promotion_decision':'DO_NOT_REPLACE_PRODUCTION_SOURCE_YET',
  'blockers':[{'id':'P1','work':'Candidate-aware native/OWL/SHACL/dictionary source contracts and new source/evidence bindings; keep historical version paths fixed.'},{'id':'P2','work':'Explicit EvidenceUse relational mapping and export; do not infer actual use or its grounding from the existence of an evidence reference.'},{'id':'P3','work':'Reconcile candidate definitions, diagrams and reader outputs, then exercise a candidate CI path before promotion.'}],
  'boundary':'B0-3 is a completed integration audit and a concrete promotion-path decision. The guarded rejections and old-projection mismatch are expected compatibility findings, not failures of the archived baseline or proof of a completed migration. Historical manuscript evidence and real case data are unchanged.'}
 (HERE/'integration-report.json').write_text(dumps(report));print(dumps({'status':report['status'],**report['summary']}))
 return int(not all(scope_checks.values()))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--schema',type=Path,required=True);p.add_argument('--robot',type=Path,required=True);p.add_argument('--sdk',type=Path,required=True);p.add_argument('--node',type=Path,required=True)
 a=p.parse_args()
 for k in ['schema','robot','sdk','node']:setattr(a,k,getattr(a,k).resolve())
 raise SystemExit(main(a))
