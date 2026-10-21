"""Bounded structural checks for the Riskium conceptual design; no formal reasoning."""
import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def validate(model):
    errors=[]
    concepts=model['concepts'];relations=model['associations'];generals=model['generalizations']
    by={c['id']:c for c in concepts+model['imported_types']}
    for section in ['concepts','associations','generalizations','constraints','domains']:
        values=model[section]
        if len({x['id'] for x in values})!=len(values):errors.append('duplicate '+section+' identifier')
    members=[i for d in model['domains'] for i in d['concept_ids']]
    if len(members)!=len(concepts) or set(members)!={c['id'] for c in concepts}:errors.append('domain membership mismatch')
    for c in concepts:
        if c['scope_layer']=='FORMAL_CORE' and not c['ontouml_stereotype']:errors.append('untyped core concept')
    for r in relations:
        if r['source'] not in by or r['target'] not in by:
            errors.append('unresolved relation endpoint');continue
        if r['scope_layer']=='FORMAL_CORE' and any(by[r[end]]['scope_layer']=='OPTIONAL_PHENOMENON_BOUNDARY' for end in ['source','target']):errors.append('optional boundary in typed relation')
        for end in ['source','target']:
            card=r[end+'_end_cardinality'];match=re.fullmatch(r'(\d+)(?:\.\.(\d+|\*))?',card)
            if not match:errors.append('invalid cardinality')
            elif match[2] and match[2]!='*' and int(match[1])>int(match[2]):errors.append('reversed cardinality')
        if r.get('stereotype')=='mediation' and by[r['source']]['ontouml_stereotype']!='relator':errors.append('mediation without relator')
    parents={i:set() for i in by}
    for g in generals:
        if g['specific'] not in by or g['general'] not in by:errors.append('unresolved generalization endpoint');continue
        parents[g['specific']].add(g['general'])
    def ancestors(i,path=()):
        if i in path:raise ValueError('cycle')
        out=set(parents[i])
        for p in parents[i]:out|=ancestors(p,path+(i,))
        return out
    try:
        for c in concepts:
            a=ancestors(c['id'])
            if c['ontouml_stereotype']=='subkind' and c['identity_supplier'] not in a:errors.append('missing identity ancestor')
            if c['ontouml_stereotype'] in ['kind','subkind','role']:
                kinds={i for i in a|{c['id']} if by[i]['ontouml_stereotype']=='kind'}
                if len(kinds)!=1:errors.append('sortal identity ambiguity')
            if c['ontouml_stereotype'] in ['kind','subkind','category'] and any(by[i]['ontouml_stereotype'] in ['role','roleMixin'] for i in a):errors.append('rigid subtype of anti-rigid class')
    except ValueError:errors.append('generalization cycle')
    for c in concepts:
        if c['ontouml_stereotype']=='mode' and not any(r.get('stereotype')=='characterization' and r['target']==c['id'] and r['source_end_cardinality']=='1' for r in relations):errors.append('mode lacks exactly-one bearer')
    return sorted(set(errors))

if __name__=='__main__':
    model=json.loads((ROOT/'ontology/riskium-model.json').read_text())
    errors=validate(model)
    print(json.dumps({'status':'failed' if errors else 'passed','errors':errors,'scope':'Bounded structural checks; not native OntoUML, HermiT or SHACL execution.'},indent=2))
    raise SystemExit(bool(errors))
