"""Validate the impact contract without mutating or qualifying a successor model."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import hashlib,json
import build_inventory as scan
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def load(n):return json.loads((HERE/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def owner(m,s):
 if s.startswith('concept:'):return next(c for c in m['concepts'] if c['id']==s.split(':')[1])
 if s.startswith('constraint:'):return next(c for c in m['constraints'] if c['id']==s.split(':')[1])
 return m['scope'] if s=='scope' else m

def audit():
 bindings=load('input-bindings.json');decisions=load('decisions.json')['decisions'];delta=load('proposed-source-delta.json');oracles=load('acceptance-oracles.json')['cases'];inventory=load('inventory.json')
 for d in decisions:
  for p in d['evidence']:assert sha(ROOT/p['path'])==p['sha256'],p['path']
 for p in bindings['inputs']:assert sha(ROOT/p['path'])==p['sha256'],p['path']
 assert scan.build()==inventory,'Inventory differs from pinned tracked source'
 ids={d['id'] for d in decisions};assert len(ids)==18
 assert all(r['decision'] in ids and r['changed_in_B1'] is False for r in inventory['files'])
 assert all(d['disposition'] in ['PROSE_CORRECTION','PROFILE_RELOCATION','MODEL_CHANGE','NO_CHANGE'] for d in decisions)
 model=json.loads((ROOT/delta['base_source']['path']).read_text());proposed=deepcopy(model)
 for p in delta['patches']:
  o=owner(proposed,p['selector']);assert o.get(p['field'])==p['before'],'Unexpected preimage';o[p['field']]=p['after']
 assert len(delta['patches'])==12
 structural=lambda m: {'concepts':[{k:c.get(k) for k in ['id','ontouml_stereotype','is_abstract','identity_supplier','scope_layer']} for c in m['concepts']],**{k:m[k] for k in ['imported_types','associations','generalizations','generalization_set_policy']}}
 assert structural(model)==structural(proposed),'Unauthorized structural change'
 assert all(a==b for a,b in zip(model['constraints'],proposed['constraints']) if a['id']!='C-16')
 case=next(c for c in model['concepts'] if c['id']=='RKM-X01');incident=[r for r in model['associations'] if case['id'] in (r['source'],r['target'])]
 assert len(incident)==24 and sum(r['scope_layer']=='FORMAL_CORE' for r in incident)==22
 entry=next(r for r in incident if r['id']=='R-01');assert (entry['source'],entry['target'],entry['source_end_cardinality'],entry['target_end_cardinality'])==('RKM-C022','RKM-X01','0..*','1')
 minima=[r['id'] for r in incident if r['source']=='RKM-X01' and not r['target_end_cardinality'].startswith('0')];assert set(minima)=={'RX-001','RX-003'}
 assert len(oracles)==20 and len({o['id'] for o in oracles})==20 and all(o['execution_status']=='NOT_RUN_B1' and o['expected'] and o['planned_mechanisms'] for o in oracles)
 probe=load('sqlite-probe.json');assert probe['case_rows']==1 and probe['register_entries']==0 and len(probe['case_type_export_rows'])==1 and probe['schema_unchanged'] and probe['integrity']=='ok' and probe['foreign_key_violations']==0
 return {'schema':'riskium-riskcase-impact-audit-1','status':'B1_COMPLETE_IMPACT_AND_ACCEPTANCE_CONTRACT_ONLY','source_commit':scan.PIN,
  'counts':{'tracked_files':inventory['tracked_files'],'utf8_text_files':inventory['utf8_text_files'],'direct_case_match_files':inventory['direct_case_match_files'],'admission_term_match_files':inventory['admission_term_match_files'],'inventory_files':len(inventory['files']),'decision_groups':18,'proposed_prose_or_scope_fields':12,'planned_acceptance_cases':20,'acceptance_cases_executed':0,'case_incident_associations':24,'formal_case_incident_associations':22},
  'decision_dispositions':dict(Counter(d['disposition'] for d in decisions)),'structural_delta_selected':False,'sqlite_probe':{'case_rows':1,'register_entries':0,'native_case_type_export_rows':1,'schema_unchanged':True},
  'checks':{'pinned_inventory_reproduced':True,'decision_and_input_hashes_match':True,'all_inventory_rows_have_disposition':True,'proposed_delta_preimages_match':True,'structural_signature_unchanged_in_memory':True,'other_constraints_unchanged':True,'entry_cardinality_orientation_preserved':True,'context_and_objective_minima_retained':True,'all_20_oracles_predeclared_unrun':True,'disposable_SQL_probe_matches_report':True},
  'packet_sha256':{p.name:sha(p) for p in sorted(HERE.glob('*')) if p.is_file() and p.name!='verification-report.json'},
  'boundary':'B1 inspects inputs and validates a proposed contract. It does not apply the 12 proposed field changes, generate a successor native/OWL graph, run its 20 acceptance cases, publish current channels, close #92/#93, or revise the manuscript. No fresh HermiT/SHACL/ROBOT result is claimed.'}
if __name__=='__main__':
 r=audit();(HERE/'verification-report.json').write_text(scan.dump(r));print(scan.dump({k:v for k,v in r.items() if k not in ['packet_sha256']}))
