"""Bind runtime source and derived trace separately from the immutable R1 packet."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NS='implementation/relational/0.9.0/'
FILES=[NS+n for n in ('010_risk_nature.sql','README.runtime.md','schema-dictionary.md','queries/exact_version.sql','queries/by_case.sql','queries/family.sql','declaration-manifest.json')]
FILES+=['tools/'+n for n in ('build_risk_nature_schema.py','build_risk_nature_component.py','relational_risk_nature.py','run_relational_risk_nature.py','complete_risk_nature_readback.py')]
FILES+=['tests/test_risk_nature.py','evaluation/relational/risk-nature/README.md','evaluation/relational/risk-nature/traceability.json']
ROUTES={
 'NRA-01':['RKM-C005','G-07','RKM-C014','RKM-C015','RKM-C006','G2-050','G2-053','G2-052','R-05','RKM-C018'],
 'NRA-02':['R-41','R-42','R-43','R-44','RK2-011','RX-006'],
 'NRA-03':['RKM-C005','RKM-C014','RKM-C015'],
 'NRA-04':['R-41','R-42','R-43','RK2-011'],
 'NRA-05':['RKM-C005','RKM-C015'],
 'NRA-06':['R-41','R-42','R-43','R-44','RK2-011','R-05','RX-006','R-33','R-01','RX-008'],
 'NRA-07':['RKM-C014','RKM-C015'],
 'NRA-08':['RKM-C005','R-41','R-42','R-43','R-44','RK2-011'],
 'NRA-09':[], 'NRA-10':[]}


def encode(v):return json.dumps(v,indent=2)+'\n'
def build():
 c=json.loads((ROOT/NS/'contract.json').read_text())
 trace=dict(schema='riskium-risk-nature-derived-trace-v1',declaration_commit='805b1edecff254f1e21131aa6fd098344affb398',native_model='0.3.1',historical_native_dispositions_changed=False,
  requirements=[dict(requirement=r,selected_native_routes=ROUTES[r['id']],runtime='tools/relational_risk_nature.py',migration=NS+'010_risk_nature.sql',queries=[NS+'queries/'+q for q in ('exact_version.sql','by_case.sql','family.sql')],
                    original_oracles=[NS+f for f in ('fixtures.json','query-oracles.json','native-oracles.trig','negative-inputs.json')],
                    actual_evidence='Exact-source hosted runtime receipt and independent completion under issue 65',current_outcome='ACTUAL_OBSERVATIONS_RECORDED_SEPARATELY',full_native_acceptance=False) for r in c['requirements']],
  boundaries=['All 306 native dispositions retain their historical source-bound meanings; issue 66 reconciles the new bounded mapping routes.',
              'No new manuscript 7.0.8 claim, organizational admission or independent semantic rating.','Reader and distribution acceptance remain issue 66 gates.'])
 trace_path='evaluation/relational/risk-nature/traceability.json'
 hashes={p:hashlib.sha256((encode(trace).encode() if p==trace_path else (ROOT/p).read_bytes())).hexdigest() for p in sorted(FILES)}
 component=dict(schema='riskium-risk-nature-component-v1',id='RISK_NATURE_ASSERTION',version='0.9.0',schema_version=10,
  status='DEVELOPMENT_IMPLEMENTED_EXECUTION_RECORDED_SEPARATELY',declaration_commit='805b1edecff254f1e21131aa6fd098344affb398',implementation_issue=65,integration_issue=66,base_profile='0.8.0',compatible_model='0.3.1',native_changes=False,
  fixed_controls=60,concrete_negative_variants=51,additional_regressions=7,files_sha256=hashes,
  execution_evidence='Issue 65 records exact source, actual hosted/local receipts and independent ZIP readback. Original expectation files remain unchanged.',
  source_distribution='v0.3.7 proposed; no freeze/publication claimed',native_semantic_acceptance=False,independent_ratings=0)
 return {trace_path:encode(trace),NS+'component.json':encode(component)}


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
 for name,value in build().items():
  target=ROOT/name
  if args.check:
   if not target.exists() or target.read_text()!=value:raise ValueError('Stale component '+name)
  else:target.parent.mkdir(parents=True,exist_ok=True);target.write_text(value)
