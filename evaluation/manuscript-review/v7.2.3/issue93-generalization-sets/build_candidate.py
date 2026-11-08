"""Explicit set-policy candidate; keeps production and the B0-1 receipt unchanged."""
from pathlib import Path
from copy import deepcopy
import importlib.util,json,sys
from rdflib import URIRef,Literal
from rdflib.namespace import OWL,RDFS

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
PREVIOUS=HERE.parent/'issue93-evidence-use'
sys.path.insert(0,str(ROOT/'tools'))
import build_native
spec=importlib.util.spec_from_file_location('evidence_use_builder',PREVIOUS/'build_candidate.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
RISK=old.RISK;digest=old.digest;dumps=old.dumps
VERSION='0.3.2-structural.2'
REMOVED={'GS-RKM-C014','GS-RKM-C047'}

def policy_for(model):
 historical=json.loads((ROOT/'evaluation/native-review-decisions.json').read_text())['generalization_sets']
 retained=[]
 for s in historical:
  if s['id'] in REMOVED:continue
  s=deepcopy(s)
  s['criterion_status']='CARRIED_FORWARD_NOT_REASSESSED_IN_THIS_PACKET'
  if s['id']=='GS-AgentKinds':
   s['specialization_criterion']='Bearer kind: human individual or organized social entity.'
   s['criterion_status']='EXPLICITLY_RETAINED_BEARER_KIND_CRITERION'
  else:
   s['specialization_criterion']='Existing reviewed set policy retained; its broader semantic review remains separate.'
  retained.append(s)
 return {'strategy':'Emit only explicitly listed retained sets; common parenthood is not a set-creation rule.',
  'retained_sets':retained,
  'excluded_sets':[
   {'id':'GS-RKM-C014','parent':'RKM-C014','decision':'NO_BLANKET_SET','criteria_distinguished':['Documentary specialization','Contextual evidential participation'],
    'rationale':'Shared documentary identity does not supply one specialization criterion for documentary subkinds and an evidential role. Retain every subtype edge; do not invent a replacement set for all subkinds.'},
   {'id':'GS-RKM-C047','parent':'RKM-C047','decision':'NO_BLANKET_SET','criteria_distinguished':['Agent bearer kind','Mandate participation'],
    'rationale':'Retain the separate, disjoint and incomplete AgentKinds set; responsible and authorizing participation must not compete with Person/Organization classification.'}],
  'scope':'Two focal mixed-criterion sets. Other eight reviewed sets are retained, not newly independently validated.'}

def build_native_with_policy(model,source_digest):
 # Reuse the legacy element serializer, but no automatically grouped set is
 # accepted as output. All emitted sets are reconstructed from explicit policy.
 native=build_native.build(model,source_digest)
 prototypes={e['id']:deepcopy(e) for e in native['elements'] if e['type']=='GeneralizationSet'}
 setids=set(prototypes)
 native['elements']=[e for e in native['elements'] if e['type']!='GeneralizationSet']
 by={e['id']:e for e in native['elements']};concepts={c['id']:c for c in model['concepts']+model['imported_types']}
 for e in native['elements']:
  if e['type']=='Package':e['contents']=[i for i in e['contents'] if i not in setids]
 for s in model['generalization_set_policy']['retained_sets']:
  e=prototypes[s['id']]
  for k in ['generalizations','isDisjoint','isComplete']:e[k]=deepcopy(s[k])
  e['description']={'en':s['rationale']}
  e['customProperties']={'specializationCriterion':s['specialization_criterion'],'criterionStatus':s['criterion_status']}
  native['elements'].append(e)
  parent=concepts[s['parent']];owner=by[parent.get('domain_id','PKG-FOUNDATION')];owner['contents'].append(e['id'])
 return native

def render():
 _,m=old.candidate_model();m['version']=VERSION
 m['publication_profile'].update(source_design_version=VERSION,representation='Isolated combined EvidenceItem and explicit generalization-set policy candidate; not promoted to main')
 m['generalization_set_policy']=policy_for(m)
 mp=HERE/'candidate-model.json';mp.write_text(dumps(m))
 native=build_native_with_policy(m,digest(mp));np=HERE/'candidate.ontouml.json';np.write_text(dumps(native))
 # Rebuild the earlier, isolated evidence-use projection. Its receipt is not
 # rewritten. The removed sets were incomplete and non-disjoint, so they had
 # introduced no OWL exclusion/covering axioms to delete.
 _,_,graph=old.render()
 for p in [OWL.versionIRI,RDFS.label,RISK.sourceDigest,RISK.nativeDigest]:graph.remove((old.ONTO,p,None))
 graph.add((old.ONTO,OWL.versionIRI,URIRef('https://github.com/ArazSaieArasi3/riskium/candidates/issue93/generalization-sets')))
 graph.add((old.ONTO,RDFS.label,Literal('Riskium isolated structural candidate '+VERSION)))
 graph.add((old.ONTO,RISK.sourceDigest,Literal(digest(mp))));graph.add((old.ONTO,RISK.nativeDigest,Literal(digest(np))))
 graph.serialize(HERE/'candidate.owl.ttl',format='turtle')
 (HERE/'set-policy.json').write_text(dumps(m['generalization_set_policy']))
 return m,native,graph

if __name__=='__main__':
 m,n,g=render();print(dumps({'version':VERSION,'sets':len(m['generalization_set_policy']['retained_sets']),'subtype_links':len(m['generalizations']),'native_elements':len(n['elements']),'production_unchanged':digest(ROOT/'ontology/riskium-model.json')==old.FROZEN_SHA}))
