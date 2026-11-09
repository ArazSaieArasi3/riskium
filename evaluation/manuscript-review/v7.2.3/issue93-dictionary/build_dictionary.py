"""Build a complete candidate dictionary without changing frozen production readers."""
from collections import Counter,defaultdict
from pathlib import Path
from html import escape
import hashlib,json,re,sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'reader'
sys.path.insert(0,str(HERE.parent/'issue93-export-contract'))
import export_candidate as export

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def safe(s):return str(s).replace('|','\\|').replace('\n',' ')
def link(cid,cs):return '['+safe(cs[cid].get('display_title',cs[cid]['title']))+']('+cid+'.md)'

def analyze(m,n):
 cs={c['id']:c for c in m['concepts']};allcs={c['id']:c for c in m['concepts']+m['imported_types']}
 if len(cs)!=82 or len(allcs)!=83:raise ValueError('Catalog identity/count mismatch')
 allocated=[cid for d in m['domains'] for cid in d['concept_ids']]
 if Counter(allocated)!=Counter(cs.keys()):raise ValueError('Subdomain membership is not an exact partition')
 for d in m['domains']:
  rows=[c for c in m['concepts'] if c['domain_id']==d['id']]
  if [c['id'] for c in rows]!=d['concept_ids'] or len(rows)!=d['concept_count'] or sum(c['scope_layer']=='FORMAL_CORE' for c in rows)!=d['formal_core_count']:
   raise ValueError('Subdomain source accounting mismatch: '+d['id'])
 if len({r['id'] for r in m['associations']})!=len(m['associations']):raise ValueError('Duplicate relation IDs')
 if any(r[k] not in allcs for r in m['associations'] for k in ['source','target']):raise ValueError('Unresolved relation endpoint')
 pairs=Counter(tuple(sorted((cs[r['source']]['domain_id'],cs[r['target']]['domain_id']))) for r in m['associations'] if r['source'] in cs and r['target'] in cs and cs[r['source']]['domain_id']!=cs[r['target']]['domain_id'])
 by={e['id']:e for e in n['elements']}
 for c in m['concepts']:
  expected='Class' if c['scope_layer']=='FORMAL_CORE' else 'Note'
  if by[c['id']]['type']!=expected:raise ValueError('Native layer mismatch: '+c['id'])
 for g in m['generalizations']:
  if (by[g['id']]['specific'],by[g['id']]['general'])!=(g['specific'],g['general']):raise ValueError('Native inheritance mismatch')
 sets={e['id'] for e in n['elements'] if e['type']=='GeneralizationSet'}
 if sets!={s['id'] for s in m['generalization_set_policy']['retained_sets']}:raise ValueError('Native set-policy mismatch')
 return {'schema':'riskium-candidate-dictionary-structural-binding-1','source_version':m['version'],
  'model_sha256':sha(export.resolve(json.loads(export.CONTRACT.read_text())['source']['path'])),
  'native_sha256':sha(export.HERE/'generated/candidate.ontouml.json'),
  'owl_sha256':sha(export.HERE/'generated/candidate.owl.ttl'),
  'export_contract_sha256':sha(export.CONTRACT),
  'population':{'catalog_concepts':len(cs),'formal_source_classes':sum(c['scope_layer']=='FORMAL_CORE' for c in m['concepts']),
   'optional_catalog_boundaries':sum(c['scope_layer']!='FORMAL_CORE' for c in m['concepts']),'imported_anchor':len(m['imported_types']),
   'catalog_associations':len(m['associations']),'formal_relations':sum(r['scope_layer']=='FORMAL_CORE' for r in m['associations']),
   'generalizations':len(m['generalizations']),'constraints':len(m['constraints']),'retained_sets':len(sets),'subdomains':len(m['domains']),
   'native_elements':len(n['elements']),'cross_subdomain_pairs':len(pairs),'cross_subdomain_associations':sum(pairs.values())},
  'association_pairs':[{'source':a,'target':b,'relations':v} for (a,b),v in sorted(pairs.items())],
  'scope':'Catalog associations include optional bridges; imported-anchor endpoints and inheritance are excluded from the unordered package-pair population. These are structural counts, not semantic COH/COP or adequacy scores.'}

def matrix(m,binding):
 ds=m['domains'];pairs={(r['source'],r['target']):r['relations'] for r in binding['association_pairs']}
 out=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="650" viewBox="0 0 1100 650" role="img" aria-labelledby="title desc">',
 '<title id="title">Candidate subdomain association matrix</title><desc id="desc">Eleven subdomains; 23 unordered pairs and 56 catalog associations. Inheritance is excluded; optional bridges are included. No navigability or process order is asserted.</desc>',
 '<rect width="1100" height="650" fill="white"/><g font-family="Arial, sans-serif" fill="#18384a">',
 '<text x="35" y="42" font-size="25" font-weight="bold">Riskium candidate: subdomain association matrix</text>',
 '<text x="35" y="69" font-size="15">'+escape(m['version'])+' · source-bound catalog view · not a published production diagram</text>']
 for i,d in enumerate(ds):
  y=120+i*39
  out.append(f'<text x="35" y="{y+24}" font-size="16">{escape(d["id"]+"  "+d["title"])}</text>')
  out.append(f'<text x="{460+i*48+22}" y="108" font-size="13" text-anchor="middle">{d["id"]}</text>')
  for j,e in enumerate(ds):
   x=460+j*48;v=pairs.get(tuple(sorted((d['id'],e['id']))),0) if i<j else 0
   color='#c9e3e8' if v else '#f0f4f7';color='#355b70' if i==j else color
   out.append(f'<rect x="{x}" y="{y}" width="43" height="34" rx="3" fill="{color}" data-source="{d["id"]}" data-target="{e["id"]}" data-count="{v}"/>')
   if v:out.append(f'<text x="{x+21}" y="{y+23}" font-size="16" text-anchor="middle">{v}</text>')
 out+=['<text x="35" y="590" font-size="15">23 unordered subdomain pairs represent 56 distinct catalog associations.</text>',
 '<text x="35" y="617" font-size="14">Blank upper cell: no direct catalog association. Lower triangle omitted; diagonal is self-comparison.</text>',
 '<text x="35" y="640" font-size="14">Includes optional boundary bridges; excludes inheritance. Counts do not express importance or direction.</text></g></svg>']
 return '\n'.join(out)+'\n'

def build():
 contract=json.loads(export.CONTRACT.read_text());m,policy=export.validate_contract(contract);export.export(contract,check=True)
 n=json.loads((export.HERE/'generated/candidate.ontouml.json').read_text());binding=analyze(m,n)
 cs={c['id']:c for c in m['concepts']+m['imported_types']};domains={d['id']:d for d in m['domains']}
 incident=defaultdict(list);parents=defaultdict(list);children=defaultdict(list)
 for r in m['associations']:
  incident[r['source']].append((r,r['target'],'outgoing'));incident[r['target']].append((r,r['source'],'incoming'))
 for g in m['generalizations']:parents[g['specific']].append(g['general']);children[g['general']].append(g['specific'])
 files={};intro='Candidate **'+m['version']+'**; not the published current dictionary. Source SHA-256: `'+binding['model_sha256']+'`.'
 nav='[All concepts](README.md) · [Subdomains](Subdomains.md) · [Relations](Relations.md) · [Inheritance](Generalizations.md) · [Constraints](Constraints.md) · [Set policy](Set-policy.md)'
 source='[Rebuildable source recipe](../../issue93-generalization-sets/build_candidate.py) · [Export contract](../../issue93-export-contract/input-contract.json) · [Structural binding](structural-binding.json)'
 for c in m['concepts']+m['imported_types']:
  cid=c['id'];native=next(e for e in n['elements'] if e['id']==cid)
  lines=['# '+c.get('display_title',c['title']),'',intro,'',nav,'','**Source ID:** `'+cid+'`; **source title:** `'+c['title']+'`; **layer:** `'+c['scope_layer']+'`; **native representation:** `'+native['type']+'`.','',
   '**Subdomain:** '+('['+c['domain_id']+' · '+domains[c['domain_id']]['title']+'](Subdomains.md#'+c['domain_id'].lower()+')' if 'domain_id' in c else 'External foundational anchor; outside the eleven catalog subdomains.'),'',
   '## Authored source definition','',c['definition'],'','## Identity and source typing','',
   '- OntoUML stereotype: `'+(c['ontouml_stereotype'] or 'not assigned')+'`; abstract: `'+('not specified' if c['is_abstract'] is None else str(c['is_abstract']).lower())+'`.',
   '- Identity supplier: '+(link(c['identity_supplier'],cs) if c.get('identity_supplier') in cs else safe(c.get('identity_supplier') or 'No identity supplier is assigned in this source record.')),
   '- Identity basis: '+c['identity_basis'],
   '- Typing rationale: '+(c.get('typing_rationale') or c.get('import_basis') or 'No source rationale recorded.'),
   '- Source aliases: '+(', '.join(safe(x) for x in c.get('aliases',[])) or 'None recorded.'),'',
   '## Direct catalog associations','', '| ID | Position and source predicate | Other endpoint | Source-end multiplicity | Target-end multiplicity | Layer |','|---|---|---|---|---|---|']
  for r,other,direction in sorted(incident[cid],key=lambda x:(x[0]['id'],x[2])):
   lines.append('| '+r['id']+' | '+direction+' `'+safe(r['predicate'])+'` | '+link(other,cs)+' | '+r['source_end_cardinality']+' | '+r['target_end_cardinality']+' | '+r['scope_layer']+' |')
  if not incident[cid]:lines.append('| — | No direct catalog association recorded. | — | — | — | — |')
  lines+=['','The source-end multiplicity counts sources per target; the target-end multiplicity counts targets per source. Position describes the source record, not asserted navigability. Optional bridges are catalog information, not typed-core relations.','',
   '## Direct inheritance','', 'Direct supertypes: '+(', '.join(link(x,cs) for x in parents[cid]) or 'None recorded.')+'  ', 'Direct subtypes: '+(', '.join(link(x,cs) for x in children[cid]) or 'None recorded.'),'',
   '## Evidence and alignment boundary','', '**Authored source status:** '+c.get('verification_status','Imported anchor; external identity and import closure are not independently established.'),'',
   'The source status is preserved verbatim. The [candidate execution receipts](../README.md) separately report the current bounded structural and engine checks. Neither the source label nor this generated page supplies independent semantic acceptance, a sourced external definition or standards equivalence. Term-level external alignment is not inferred here.']
  if cid in ['RKM-C014','RKM-C047','RKM-C065','RKM-C066','RKM-C075','RKM-C076']:lines+=['','[Selected integration interpretation](../../issue93-integration/definitions/'+cid+'.md) preserves the separate candidate design decision.']
  if cid=='RKM-X01':lines+=['','The source RiskCase definition is retained in this candidate. The adopted broader RiskCase meaning and its profile/model migration are tracked separately in [issue #92](https://github.com/ArazSaieArasi3/riskium/issues/92); this dictionary does not silently perform that migration.']
  if native['type']=='Note':lines+=['','This is an optional catalog boundary represented as a native Note; its displayed source stereotype does not make it an exported typed-core class.']
  lines+=['',source,'',nav,''];files[cid+'.md']='\n'.join(lines)
 index=['# Riskium candidate concept dictionary','',intro,'',
  'This source-bound reader covers **82 catalog concepts in eleven subdomains**, plus **one separately indexed external anchor**. Riskium has one general risk-knowledge domain; pharmaceutical material is a development case. The current published reader and historical eighty-concept dictionary remain unchanged.','',nav,'',source,'',
  '[Candidate subdomain matrix](Subdomain-matrix.svg) · [Earlier selected evidence fragment](../../issue93-integration/evidence-fragment.svg)','']
 sub=['# Candidate subdomains','',intro,'',nav,'',
  'The allocation is a partition of all 82 catalog concepts. The external anchor is excluded. These packages are subdomains, not independently validated executable modules.','',
  '| Subdomain | Source purpose | Concepts |','|---|---|---|']
 for d in m['domains']:
  index+=['## '+d['id']+' · '+d['title'],'',safe(d['objective']),'',' · '.join(link(cid,cs) for cid in d['concept_ids']),'']
  sub.append('| ['+d['id']+' · '+d['title']+'](#'+d['id'].lower()+') | '+safe(d['objective'])+' | '+', '.join(link(cid,cs) for cid in d['concept_ids'])+' |')
 for d in m['domains']:
  sub+=['','<a id="'+d['id'].lower()+'"></a>','## '+d['id']+' · '+d['title'],'',d['definition'],'',d['objective'],'',', '.join(link(cid,cs) for cid in d['concept_ids'])]
 sub+=['','## Cross-subdomain associations','',
  '[Matrix SVG](Subdomain-matrix.svg) · [Exact structural population](structural-binding.json)','',
  'Twenty-three unordered pairs contain 56 catalog associations. Optional bridges are included; inheritance and imported-anchor endpoints are excluded. Counts do not assert process order, navigability, importance or semantic COH/COP.','',
  '| Pair | Association count |','|---|---:|']
 sub+=['| '+r['source']+' ↔ '+r['target']+' | '+str(r['relations'])+' |' for r in binding['association_pairs']]
 index+=['## External anchor','',link('EXT-OBJECT',cs),'']
 files['README.md']='\n'.join(index);files['Subdomains.md']='\n'.join(sub)+'\n'
 rels=['# Candidate catalog associations','',intro,'',nav,'','All 137 catalog associations are listed; 130 are typed-core relations. The remaining seven retain their optional-boundary scope.','',
  '| ID | Source | Predicate | Target | Source-end | Target-end | Layer |','|---|---|---|---|---|---|---|']
 rels+=['| '+r['id']+' | '+link(r['source'],cs)+' | '+safe(r['predicate'])+' | '+link(r['target'],cs)+' | '+r['source_end_cardinality']+' | '+r['target_end_cardinality']+' | '+r['scope_layer']+' |' for r in m['associations']]
 files['Relations.md']='\n'.join(rels)+'\n'
 gens=['# Candidate direct inheritance','',intro,'',nav,'','All 67 asserted generalizations are retained. Generalization-set membership is a separate policy, not an automatic consequence of common parenthood.','',
  '| ID | Specific | General |','|---|---|---|']
 gens+=['| '+g['id']+' | '+link(g['specific'],cs)+' | '+link(g['general'],cs)+' |' for g in m['generalizations']];files['Generalizations.md']='\n'.join(gens)+'\n'
 cons=['# Candidate source constraints','',intro,'',nav,'','These 26 source statements are not all executable OWL or SHACL rules. Their source status and statement are preserved below; engine-specific coverage stays in the execution receipts.','']
 for c in m['constraints']:cons+=['## '+c['id']+' · '+c['title'],'','Source status: `'+c['status']+'`.','',c['statement'],'']
 files['Constraints.md']='\n'.join(cons)
 pol=['# Candidate generalization-set policy','',intro,'',nav,'',policy['strategy'],'','## Explicitly retained sets','']
 for s in policy['retained_sets']:
  pol+=['### '+s['id'],'','Parent: '+link(s['parent'],cs)+'; disjoint: `'+str(s['isDisjoint']).lower()+'`; complete: `'+str(s['isComplete']).lower()+'`.','',s['specialization_criterion'],'',s['rationale'],'','Members: '+', '.join('`'+g+'`' for g in s['generalizations'])+'.','', 'Criterion status: `'+s['criterion_status']+'`.','']
 pol+=['## Excluded blanket sets','']
 for s in policy['excluded_sets']:pol+=['### '+s['id'],'',s['rationale'],'']
 files['Set-policy.md']='\n'.join(pol)
 files['Subdomain-matrix.svg']=matrix(m,binding);files['structural-binding.json']=dump(binding)
 manifest={'schema':'riskium-candidate-dictionary-manifest-1','source_version':m['version'],'source_model_sha256':binding['model_sha256'],
  'catalog_concept_pages':82,'anchor_pages':1,'subdomains':11,'production_promoted':False,
  'files_sha256':{name:hashlib.sha256(value.encode()).hexdigest() for name,value in sorted(files.items())}}
 files['manifest.json']=dump(manifest)
 return files

def write(check=False):
 files=build()
 if check:
  actual={p.name for p in OUT.iterdir() if p.is_file()}
  if actual!=set(files):raise ValueError('Reader inventory mismatch')
  for name,text in files.items():
   if (OUT/name).read_text()!=text:raise ValueError('Stale reader output: '+name)
 else:
  OUT.mkdir(exist_ok=True)
  for name,text in files.items():(OUT/name).write_text(text)
 return files

if __name__=='__main__':
 files=write('--check' in sys.argv);print(dump({'files':len(files),'concept_pages':82,'anchor_pages':1,'status':'CANDIDATE_DICTIONARY_GENERATED_NOT_PROMOTED'}))
