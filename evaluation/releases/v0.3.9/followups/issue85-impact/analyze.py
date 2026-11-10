"""Conservative, source-bound documentary reuse impact; not semantic acceptance."""
import json,hashlib,csv,io,copy
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def classify(old,new,review):
 a={x['id']:x for x in old['concepts']};b={x['id']:x for x in new['concepts']};r={x['concept_id']:x for x in review['concepts']}
 assert len(a)==len(r)==80 and len(b)==82 and set(r)==set(a)
 assert {i for d in new['domains'] for i in d['concept_ids']}==set(b)
 for i,x in a.items():assert sha(x['definition'].encode())==r[i]['authored_definition_sha256'],i
 def links(m,i):return sorted([x for x in m['associations'] if i in [x['source'],x['target']]],key=lambda x:x['id'])
 def inherits(m,i):return sorted([x for x in m['generalizations'] if i in [x['specific'],x['general']]],key=lambda x:x['id'])
 descendants={'RKM-C014','RKM-C047'}
 while True:
  nxt=descendants|{g['specific'] for g in old['generalizations'] if g['general'] in descendants}
  if nxt==descendants:break
  descendants=nxt
 rows=[]
 for i,x in b.items():
  prev=a.get(i);fields=[] if prev is None else sorted(k for k in set(prev)|set(x) if prev.get(k)!=x.get(k))
  association_changed=prev is not None and links(old,i)!=links(new,i)
  inheritance_changed=prev is not None and inherits(old,i)!=inherits(new,i)
  set_affected=i in descendants
  kind='NEW_CONCEPT' if prev is None else 'AUTHORED_OR_TYPING_CHANGE' if fields else 'STRUCTURAL_CONTEXT_RECHECK' if association_changed or inheritance_changed or set_affected else 'REUSE_CANDIDATE'
  rows.append(dict(id=i,title=x['display_title'],subdomain=x['domain_id'],category=kind,changed_fields=fields,association_changed=association_changed,inheritance_changed=inheritance_changed,mixed_set_policy_context=set_affected,previous_disposition=r.get(i,{}).get('disposition'),source_ids=r.get(i,{}).get('source_ids',[]),followup_issues=r.get(i,{}).get('followup_issues',[]),definition_unchanged=prev is not None and prev['definition']==x['definition'],old_concept_sha256=sha(json.dumps(prev,sort_keys=True).encode()) if prev else None,new_concept_sha256=sha(json.dumps(x,sort_keys=True).encode()),action='Establish a sourced documentary disposition.' if prev is None else 'Review changed source fields and comparison scope before reuse.' if fields else 'Retain source evidence; recheck relation/inherited-set context before adopting current disposition.' if kind=='STRUCTURAL_CONTEXT_RECHECK' else 'Verify edition/locator and compatible comparison scope; reuse evidence without claiming equivalence.',accepted_for_current_curation=False))
 return rows

def main():
 old=json.loads((ROOT/'ontology/riskium-model.json').read_text());new=json.loads((ROOT/'ontology/0.3.2/riskium-model.json').read_text());review=json.loads((ROOT/'references/concept-definitions/0.1.0/review.json').read_text())
 assert sha((ROOT/'ontology/riskium-model.json').read_bytes())==review['model_sha256']
 rows=classify(old,new,review);tests=[]
 for label,mutate in [('missing_review',lambda o,n,r:r['concepts'].pop()),('stale_definition',lambda o,n,r:r['concepts'][0].update(authored_definition_sha256='0'*64)),('allocation_missing',lambda o,n,r:n['domains'][0]['concept_ids'].pop())]:
  o,n,r=copy.deepcopy((old,new,review));mutate(o,n,r)
  try:classify(o,n,r)
  except AssertionError:tests.append(dict(control=label,rejected=True))
  else:raise AssertionError('Undetected mutation '+label)
 result=dict(status='IMPACT_INVENTORY_COMPLETE_CURATION_NOT_ACCEPTED',baseline_commit='3ce6f5573e2e0a698591615a7ded75c2f9451444',inputs={p:sha((ROOT/p).read_bytes()) for p in ['ontology/riskium-model.json','ontology/0.3.2/riskium-model.json','references/concept-definitions/0.1.0/review.json']},summary=dict(Counter(x['category'] for x in rows)),old_population=80,current_population=82,definition_unchanged=sum(x['definition_unchanged'] for x in rows),mutation_controls=tests,rows=rows,boundary='Conservative documentary impact and reuse candidates only. Structural context flags do not prove defects or require discarding prior sources. No new external source/edition/locator or independent validation is asserted. External anchor is outside the 82-concept catalog population.')
 (OUT/'impact.json').write_text(json.dumps(result,indent=2)+'\n')
 s=io.StringIO();w=csv.writer(s);w.writerow(['id','title','category','changed_fields','association_changed','inheritance_changed','mixed_set_policy_context','previous_disposition','action'])
 for x in rows:w.writerow([x['id'],x['title'],x['category'],','.join(x['changed_fields']),x['association_changed'],x['inheritance_changed'],x['mixed_set_policy_context'],x['previous_disposition'],x['action']])
 (OUT/'impact.csv').write_text(s.getvalue());print(json.dumps({k:result[k] for k in ['status','summary','definition_unchanged','mutation_controls']}))
if __name__=='__main__':main()
