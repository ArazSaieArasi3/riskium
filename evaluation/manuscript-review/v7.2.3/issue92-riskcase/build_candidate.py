"""Build the B1-declared RiskCase successor without rewriting prior packets."""
from pathlib import Path
from copy import deepcopy
import hashlib,importlib.util,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];IMPACT=HERE.parent/'issue92-impact'
OLD=HERE.parent/'issue93-export-contract';sys.path.insert(0,str(OLD))
import export_candidate as prior
import candidate_owl
VERSION='0.3.2-case.1';CONTRACT=HERE/'input-contract.json'
def dump(v):return json.dumps(v,ensure_ascii=False,indent=2)+'\n'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def resolve(p):
 q=(ROOT/p).resolve()
 if not q.is_relative_to(ROOT) or Path(p).is_absolute():raise ValueError('Unsafe input path')
 return q
def pin(p):return {'path':str(Path(p).relative_to(ROOT)),'sha256':sha(p)}
def checked(entry):
 p=resolve(entry['path'])
 if sha(p)!=entry['sha256']:raise ValueError('Pinned input changed: '+entry['path'])
 return p
def owner(m,s):
 if s.startswith('concept:'):return next(c for c in m['concepts'] if c['id']==s.split(':')[1])
 if s.startswith('constraint:'):return next(c for c in m['constraints'] if c['id']==s.split(':')[1])
 return m['scope'] if s=='scope' else m

def derive():
 inputs=json.loads((HERE/'adopted-inputs.json').read_text())
 for e in inputs['inputs']:checked(e)
 delta=json.loads((IMPACT/'proposed-source-delta.json').read_text());base=json.loads(checked(delta['base_source']).read_text());m=deepcopy(base)
 for p in delta['patches']:
  o=owner(m,p['selector'])
  if o.get(p['field'])!=p['before']:raise ValueError('Source delta preimage mismatch')
  o[p['field']]=deepcopy(p['after'])
 m['version']=VERSION;m['date_local']='2026-11-09'
 m['publication_profile'].update(source_design_version=VERSION,export_revision='2026-11-09',representation='Combined EvidenceItem/set-policy repair and adopted analytical RiskCase candidate; not promoted to current')
 signature=lambda x:([{k:c.get(k) for k in ['id','ontouml_stereotype','is_abstract','identity_supplier','scope_layer']} for c in x['concepts']],*[x[k] for k in ['imported_types','associations','generalizations','generalization_set_policy']])
 if signature(base)!=signature(m):raise ValueError('Undeclared structural change')
 return m

def contract_for(m):
 old=json.loads(prior.CONTRACT.read_text());prior.validate_contract(old)
 dependencies=[HERE/'adopted-inputs.json',IMPACT/'proposed-source-delta.json',IMPACT/'acceptance-oracles.json',prior.CONTRACT]
 dependencies+=[HERE/n for n in ['build_candidate.py','case_profiles.py','reader.py','verify_candidate.py']]
 return {'schema':'riskium-riskcase-candidate-contract-1','source_version':VERSION,'source':{'path':str((HERE/'candidate-model.json').relative_to(ROOT)),'sha256':hashlib.sha256(dump(m).encode()).hexdigest()},
  'term_namespace':old['term_namespace'],'ontology_iri':old['ontology_iri'],'evidence_namespace':old['evidence_namespace'],
  'version_iri':'https://github.com/ArazSaieArasi3/riskium/candidates/issue92/riskcase','inventory':old['inventory'],
  'policy':pin(HERE.parent/'issue93-generalization-sets/set-policy.json'),'dependencies':[pin(p) for p in dependencies],
  'frozen_inputs':old['frozen_inputs'],'previous_export_contract_sha256':sha(prior.CONTRACT),'production_promotion':False,
  'boundary':'Apply only the B1-declared prose/scope delta and successor metadata. Term IRIs are compatibility identifiers; the candidate versionIRI and source hash are separate. No operational approval is a universal axiom.'}

def render():
 m=derive();c=contract_for(m);policy=m['generalization_set_policy'];builder=prior.load_builder()
 n=builder.build_native_with_policy(m,c['source']['sha256']);native=dump(n)
 binding=deepcopy(c);binding['_receipt_digest']=hashlib.sha256(dump(c).encode()).hexdigest()
 owl,receipt=candidate_owl.render(m,n,policy,binding,{'source':c['source']['sha256'],'policy':c['policy']['sha256'],'native':hashlib.sha256(native.encode()).hexdigest()})
 if len(n['elements'])!=596:raise ValueError('Native population changed')
 return {'candidate-model.json':dump(m),'input-contract.json':dump(c),'candidate.ontouml.json':native,'candidate.owl.ttl':owl,'mapping-receipt.json':dump(receipt)}

def build(check=False):
 files=render()
 if check:
  for name,text in files.items():
   if not (HERE/name).exists() or (HERE/name).read_text()!=text:raise ValueError('Stale successor: '+name)
 else:
  for name,text in files.items():(HERE/name).write_text(text)
 return files

def validate_contract(c):
 if c!=json.loads(render()['input-contract.json']):raise ValueError('Candidate input contract mismatch')
 m=json.loads((checked(c['source'])).read_text())
 for e in c['dependencies']+c['frozen_inputs']+[c['policy']]:checked(e)
 return m,m['generalization_set_policy']
if __name__=='__main__':
 f=build('--check' in sys.argv);print(dump({'source_version':VERSION,'outputs':list(f),'production_promoted':False}))
