"""Audit exhaustive candidate reader coverage and actual local route targets."""
from pathlib import Path
import hashlib,json,re
import xml.etree.ElementTree as ET
from collections import Counter
import build_dictionary as build


def audit(files, model):
    catalog={c['id']:c for c in model['concepts']}
    allcs={c['id']:c for c in model['concepts']+model['imported_types']}
    expected={cid+'.md' for cid in allcs}|{'README.md','Subdomains.md','Relations.md','Generalizations.md','Constraints.md','Set-policy.md','Subdomain-matrix.svg','structural-binding.json','manifest.json'}
    if set(files)!=expected:raise ValueError('Incomplete or extra reader inventory')
    manifest=json.loads(files['manifest.json'])
    if manifest['source_model_sha256']!=build.sha(build.export.resolve(json.loads(build.export.CONTRACT.read_text())['source']['path'])):
        raise ValueError('Manifest source binding mismatch')
    for name,value in files.items():
        if name=='manifest.json':continue
        if manifest['files_sha256'].get(name)!=hashlib.sha256(value.encode()).hexdigest():raise ValueError('Reader hash mismatch: '+name)
    local_links=0;anchors=0
    for name,value in files.items():
        if not name.endswith('.md'):continue
        for target in re.findall(r'\]\(([^)]+)\)',value):
            if target.startswith(('http://','https://')):continue
            raw,_,fragment=target.partition('#');path=(build.OUT/(raw or name)).resolve()
            if not path.is_relative_to(build.ROOT):raise ValueError('Reader path escapes repository')
            if path.parent==build.OUT and path.name in files:body=files[path.name]
            elif path.is_file():body=path.read_text()
            else:raise ValueError('Broken reader link: '+name+' -> '+target)
            if fragment:
                if '<a id="'+fragment+'"></a>' not in body:raise ValueError('Missing reader anchor: '+target)
                anchors+=1
            local_links+=1
    for cid,c in allcs.items():
        text=files[cid+'.md']
        if c['definition'] not in text or c['identity_basis'] not in text:raise ValueError('Definition/identity missing: '+cid)
        if c.get('typing_rationale') and c['typing_rationale'] not in text:raise ValueError('Typing rationale missing: '+cid)
        if c.get('verification_status') and c['verification_status'] not in text:raise ValueError('Source status rewritten: '+cid)
        if cid in catalog and c['scope_layer']!='FORMAL_CORE' and 'native representation:** `Note`' not in text:
            raise ValueError('Optional boundary represented as a class')
        for r in model['associations']:
            if cid in (r['source'],r['target']) and '| '+r['id']+' |' not in text:raise ValueError('Incident relation missing: '+cid+' '+r['id'])
        for g in model['generalizations']:
            if g['specific']==cid and g['general']+'.md' not in text:raise ValueError('Missing direct parent')
            if g['general']==cid and g['specific']+'.md' not in text:raise ValueError('Missing direct subtype')
    for r in model['associations']:
        if '| '+r['id']+' |' not in files['Relations.md']:raise ValueError('Relation inventory missing')
    for g in model['generalizations']:
        if '| '+g['id']+' |' not in files['Generalizations.md']:raise ValueError('Inheritance inventory missing')
    for c in model['constraints']:
        if c['statement'] not in files['Constraints.md']:raise ValueError('Constraint statement missing')
    owners={cid:c['domain_id'] for cid,c in catalog.items()}
    pairs=Counter(tuple(sorted((owners[r['source']],owners[r['target']]))) for r in model['associations'] if r['source'] in owners and r['target'] in owners and owners[r['source']]!=owners[r['target']])
    structural=json.loads(files['structural-binding.json'])
    observed={(p['source'],p['target']):p['relations'] for p in structural['association_pairs']}
    if observed!=dict(pairs):raise ValueError('Structural pair accounting mismatch')
    if structural['population']['catalog_concepts']!=len(catalog) or structural['population']['cross_subdomain_associations']!=sum(pairs.values()):
        raise ValueError('Structural population mismatch')
    root=ET.fromstring(files['Subdomain-matrix.svg']);ns={'svg':'http://www.w3.org/2000/svg'}
    matrix_numbers=[int(x.text) for x in root.findall('.//svg:text',ns) if x.text and x.text.isdecimal()]
    if sorted(matrix_numbers)!=sorted(pairs.values()):raise ValueError('Matrix numeric cells differ from source')
    cells={(x.attrib['data-source'],x.attrib['data-target']):int(x.attrib['data-count']) for x in root.findall('.//svg:rect',ns) if 'data-source' in x.attrib and x.attrib['data-source']<x.attrib['data-target'] and int(x.attrib['data-count'])}
    if cells!=dict(pairs):raise ValueError('Matrix pair positions differ from source')
    if '[issue #92]' not in files['RKM-X01.md']:raise ValueError('RiskCase migration boundary absent')
    return {'catalog_pages':len(catalog),'anchor_pages':len(allcs)-len(catalog),'files':len(files),
            'local_links_checked':local_links,'explicit_anchors_checked':anchors,
            'associations':len(model['associations']),'generalizations':len(model['generalizations']),
            'constraints':len(model['constraints']),'cross_subdomain_pairs':len(pairs),
            'cross_subdomain_associations':sum(pairs.values()),'external_http_checked':False}


if __name__=='__main__':
    m,_=build.export.validate_contract(json.loads(build.export.CONTRACT.read_text()))
    print(build.dump(audit(build.write(check=True),m)))
