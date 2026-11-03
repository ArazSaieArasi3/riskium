"""Reproducible, bounded structural observations for manuscript 7.1.0.

No ontology is modified. Candidate patterns are review prompts, not defects.
"""
from pathlib import Path
from collections import Counter, defaultdict
from itertools import combinations
import hashlib, json, platform, subprocess, sys

BASE=Path(__file__).resolve().parent
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else BASE/'generated'
REPO=BASE.parents[3]
MODEL=REPO/'ontology/riskium-model.json'
M=json.loads(MODEL.read_text())
DEC=json.loads((REPO/'evaluation/native-review-decisions.json').read_text())
C={c['id']:c for c in M['concepts']+M['imported_types']}
CORE={i:c for i,c in C.items() if c.get('scope_layer')=='FORMAL_CORE' or i.startswith('EXT-')}
A=[a for a in M['associations'] if a['source'] in CORE and a['target'] in CORE]
G=M['generalizations']
parents=defaultdict(set)
for g in G:parents[g['specific']].add(g['general'])
def ancestors(x):
    out=set();q=list(parents[x])
    while q:
        z=q.pop()
        if z not in out:out.add(z);q.extend(parents[z])
    return out
anc={i:ancestors(i) for i in C}
desc={i:{j for j in C if i in anc[j]} for i in C}
st=lambda i:(C[i].get('ontouml_stereotype') or '').lower()
rigid={'kind','subkind','category','collective','quantity','relator','mode'}
anti={'role','rolemixin','phase','phasemixin'}
idtypes={'kind','collective','quantity'}
def upper(s):return float('inf') if s.split('..')[-1]=='*' else int(s.split('..')[-1])
def components(ids,pairs):
    adj={i:set() for i in ids}
    for a,b in pairs:
        if a in ids and b in ids:adj[a].add(b);adj[b].add(a)
    todo=set(ids);parts=[]
    while todo:
        q=[todo.pop()];part=[]
        while q:
            x=q.pop();part.append(x)
            for y in adj[x]&todo:todo.remove(y);q.append(y)
        parts.append(sorted(part))
    return sorted(parts), sum(not v for v in adj.values())

def structural():
    assoc=[(a['source'],a['target']) for a in M['associations']]
    gen=[(g['specific'],g['general']) for g in G]
    cross=Counter();crossgen=Counter();rows=[]
    for pairs,dest in [(assoc,cross),(gen,crossgen)]:
        for a,b in pairs:
            d1,d2=C[a].get('domain_id'),C[b].get('domain_id')
            if d1 and d2 and d1!=d2:dest[tuple(sorted((d1,d2)))]+=1
    for d in M['domains']:
        ids=set(d['concept_ids']);internal={tuple(sorted((a,b))) for a,b in assoc+gen if a in ids and b in ids and a!=b}
        parts,isolated=components(ids,internal)
        external=[(a,b) for a,b in assoc+gen if (a in ids)!=(b in ids)]
        neighbors={C[b if a in ids else a].get('domain_id') for a,b in external}-{None}
        rows.append(dict(id=d['id'],title=d['title'],n=len(ids),e=len(internal),k=len(parts),i=isolated,
                         x=len(external),b=len(neighbors),components=parts,
                         explanation='Internal connections are present.' if len(parts)==1 else 'One concept reaches the design through another subdomain; inspect the intended boundary.'))
    allids=set(C);full,isol=components(allids,assoc+gen);only,iso2=components(allids,assoc)
    return dict(unit='catalog subdomain; undirected associations plus generalizations; parallel internal pairs collapsed; cross relations counted individually; anchor excluded from neighbor count',
                metrics={'n':'local catalog concepts','e':'distinct internal unordered links','k':'internal connected components','i':'internally isolated concepts','x':'incident cross-boundary relations including the external anchor','b':'distinct other Riskium subdomains'},
                rows=rows,whole=dict(nodes=len(allids),components=len(full),isolated=isol,association_components=len(only),association_isolated=iso2),
                association_pairs=[dict(source=a,target=b,relations=n) for (a,b),n in sorted(cross.items())],
                generalization_pairs=[dict(source=a,target=b,relations=n) for (a,b),n in sorted(crossgen.items())],
                semantic_COH_COP='NOT_COMPUTED: these graph observations do not implement semantic dependency metrics')

def screen(classes, associations, generalizations, sets):
    """Selected catalogue triggers with explicit restrictions; not full language verification."""
    par=defaultdict(set)
    for g in generalizations:par[g['specific']].add(g['general'])
    def aa(i):
        done=set();q=list(par[i])
        while q:
            z=q.pop()
            if z not in done:done.add(z);q.extend(par[z])
        return done
    ancestry={i:aa(i) for i in classes};children={i:{j for j in classes if i in ancestry[j]} for i in classes}
    ty=lambda i:(classes[i].get('ontouml_stereotype') or '').lower()
    gschildren=lambda gs:{g['specific'] for g in generalizations if g['id'] in gs['generalizations']}
    disjoint=[gschildren(gs) for gs in sets if gs['isDisjoint']]
    def apart(a,b):return any(any(u in ancestry[a]|{a} and v in ancestry[b]|{b} for u,v in combinations(s,2)) or any(v in ancestry[a]|{a} and u in ancestry[b]|{b} for u,v in combinations(s,2)) for s in disjoint)
    def overlap(a,b):
        if apart(a,b):return False
        if a==b or a in ancestry[b] or b in ancestry[a]:return True
        ida={x for x in ancestry[a]|{a} if ty(x) in idtypes}
        idb={x for x in ancestry[b]|{b} if ty(x) in idtypes}
        if ty(a) in {'kind','subkind','role','phase'} and ty(b) in {'kind','subkind','role','phase'}:return bool(ida&idb)
        if ty(a)==ty(b) and ty(a) in {'mode','relator'}:return bool(ancestry[a]&ancestry[b])
        if ty(a) in {'category','mixin','rolemixin'} and ty(b) in {'category','mixin','rolemixin'}:
            return bool(children[a]&children[b]) or bool(ancestry[a]&ancestry[b])
        return False
    mediation=defaultdict(list)
    for a in associations:
        if a.get('stereotype')!='mediation':continue
        s,t=a['source'],a['target']
        if ty(s)=='relator':mediation[s].append((t,a['source_end_cardinality'],a['target_end_cardinality'],a['id']))
        elif ty(t)=='relator':mediation[t].append((s,a['target_end_cardinality'],a['source_end_cardinality'],a['id']))
    results={}
    results['GSRig']=[gs['id'] for gs in sets if ty(gs['parent']) in rigid and any(ty(i) in rigid for i in gschildren(gs)) and any(ty(i) in anti for i in gschildren(gs))]
    results['DepPhase']=[i for i in classes if ty(i)=='phase' and any(i==p for mm in mediation.values() for p,*_ in mm)]
    results['MixRig']=[i for i in classes if ty(i)=='mixin' and children[i] and (all(ty(j) in rigid for j in children[i]) or all(ty(j) in anti for j in children[i]))]
    results['RelRig']=[rid for rid,mm in mediation.items() for p,_,__,rid in mm if ty(p) in rigid]
    results['RepRel']=[i for i,mm in mediation.items() if sum(upper(rc)>1 for _,rc,_,_ in mm)>=2]
    results['ImpAbs']=[a['id'] for a in associations if any(upper(a[k])>=2 and len(children[a[n]])>=2 for n,k in [('source','source_end_cardinality'),('target','target_end_cardinality')])]
    results['BinOver']=[a['id'] for a in associations if overlap(a['source'],a['target'])]
    # Relation specialization is an endpoint-topology screen only. It is not property entailment.
    relspec=[]
    sub=lambda a,b:a==b or b in ancestry[a]
    for a,b in combinations(associations,2):
        def fits(x,y):return (sub(x['source'],y['source']) and sub(x['target'],y['target'])) or (sub(x['source'],y['target']) and sub(x['target'],y['source']))
        if fits(a,b) or fits(b,a):relspec.append([a['id'],b['id']])
    results['RelSpec']=relspec
    return results,mediation

def pattern_report():
    result,mediation=screen(CORE,A,G,DEC['generalization_sets'])
    identity=[]
    for i,c in CORE.items():
        if st(i) not in {'kind','subkind','role','phase','collective','quantity'}:continue
        suppliers={j for j in anc[i]|{i} if st(j) in idtypes}
        identity.append(dict(id=i,suppliers=sorted(suppliers),status='SATISFIED' if len(suppliers)==1 else 'REVIEW'))
    role=[]
    mediated={p for mm in mediation.values() for p,*_ in mm}
    for i in CORE:
        if st(i) in {'role','rolemixin'}:
            role.append(dict(id=i,inherited_mediation=sorted((anc[i]|{i})&mediated),status='SUPPORTED_STRUCTURE' if (anc[i]|{i})&mediated else 'REVIEW_DEPENDENCE_INTERPRETATION'))
    mode=[]
    for i in CORE:
        if st(i)=='mode':
            r=[a for a in A if a.get('stereotype')=='characterization' and i in (a['source'],a['target'])]
            exact=bool(r) and all((a['target_end_cardinality'] if a['source']==i else a['source_end_cardinality'])=='1' for a in r)
            mode.append(dict(id=i,relations=[a['id'] for a in r],status='EXACTLY_ONE_BEARER' if exact else 'REVIEW'))
    # Independent small structures exercise both positive and negative trigger oracles.
    toy={i:dict(id=i,ontouml_stereotype=t) for i,t in [('P','kind'),('S','subkind'),('R','role'),('L','relator'),('X','rolemixin'),('Y','rolemixin')]}
    gens=[dict(id='g1',specific='S',general='P'),dict(id='g2',specific='R',general='P')]
    sets=[dict(id='gs',parent='P',generalizations=['g1','g2'],isDisjoint=False)]
    rels=[dict(id='m1',source='L',target='X',stereotype='mediation',source_end_cardinality='0..*',target_end_cardinality='1'),dict(id='m2',source='L',target='Y',stereotype='mediation',source_end_cardinality='0..*',target_end_cardinality='1'),dict(id='a1',source='P',target='S',stereotype=None,source_end_cardinality='0..*',target_end_cardinality='1')]
    pos,_=screen(toy,rels,gens,sets)
    controls=[dict(id='mixed-rigidity-positive',expected=['gs'],observed=pos['GSRig']),dict(id='repeatable-relator-positive',expected=['L'],observed=pos['RepRel']),dict(id='inherited-overlap-positive',expected=['a1'],observed=pos['BinOver']),dict(id='rigid-mediated-negative',expected=[],observed=pos['RelRig'])]
    r2=[dict(a,source_end_cardinality='1') if a['id'] in ('m1','m2') else a for a in rels]
    neg,_=screen(toy,r2,gens,[])
    controls += [dict(id='repeatable-relator-negative',expected=[],observed=neg['RepRel']),dict(id='mixed-rigidity-negative',expected=[],observed=neg['GSRig'])]
    for x in controls:x['status']='PASS' if x['expected']==x['observed'] else 'FAIL'
    assert all(x['status']=='PASS' for x in controls),controls
    return dict(scope='77 typed core concepts and one local foundational anchor; 127 typed relations; 66 generalizations; 10 reviewed generalization sets',
        method='New author-implemented structural screening of eight selected documented catalogue triggers; no plugin-wide or complete catalogue conformance claim',
        sources={k:'https://ontouml.readthedocs.io/en/latest/anti-patterns/'+k+'/index.html' for k in result},
        patterns=dict(identity=identity,role_dependence=role,intrinsic_mode=mode,relator=[dict(id=i,mediations=[x[3] for x in mm],minimum_declared_participants=sum(int(x[2].split('..')[0]) for x in mm)) for i,mm in mediation.items()]),
        anti_patterns={k:dict(count=len(v),candidates=v,status='STRUCTURAL_CANDIDATES_REQUIRE_INTERPRETATION' if v else 'NO_CANDIDATE_UNDER_SELECTED_RULE') for k,v in result.items()},
        exclusions=['FreeRole and full DecInt are not computed by this screen.','RelOver, full overlap metaproperties and instance-level restrictions are not covered.','Remaining catalogue families require their own declared detector and semantic adjudication.','No candidate count is a defect count or acceptance score.'],
        controls=controls,model_changed=False)

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    common=dict(repository_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),model_sha256=hashlib.sha256(MODEL.read_bytes()).hexdigest(),python=platform.python_version())
    for name,body in [('structural-report',structural()),('pattern-report',pattern_report())]:
        (OUT/(name+'.json')).write_text(json.dumps(dict(**common,**body),indent=2))
    print(json.dumps(dict(structural_rows=len(structural()['rows']),patterns={k:v['count'] for k,v in pattern_report()['anti_patterns'].items()},control_passes=len(pattern_report()['controls']))))
