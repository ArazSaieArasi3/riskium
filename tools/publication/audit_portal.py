"""Verify documentation links, provenance, downloads and actual OWL neighborhoods."""
from pathlib import Path
import argparse, json, re
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
from rdflib import Graph, RDF, RDFS, OWL, URIRef
from rdflib.compare import isomorphic
from build_portal import ROOT, TOOLS, PREFIX, TAG, COMMIT, MODEL, OWL_SOURCE, NAMESPACE, frozen, digest, json_text


def audit(docs):
    errors=[];pages={};ids_by_path={};links=0
    def require(ok,message):
        if not ok:errors.append(message)
    version=docs/PREFIX
    manifest=json.loads((version/'publication-manifest.json').read_text())
    require(manifest['semantic_source_commit']==COMMIT,'wrong semantic source commit')
    require(manifest['guide_registry_sha256']==digest((TOOLS/'guide-registry.json').read_bytes()),'shared explanatory registry changed')
    for path,sha in manifest['semantic_inputs_sha256'].items():require(digest(frozen(path))==sha,'frozen input changed: '+path)
    for path,sha in manifest['guide_sources_sha256'].items():require(digest((ROOT/path).read_bytes())==sha,'guide source changed: '+path)
    for p in docs.rglob('*.html'):
        # Audit generated version routes and entry pages; existing raw prose is not a site.
        if not p.is_relative_to(version) and p not in [docs/'index.html',docs/'site/index.html',docs/'interface-review.html']:continue
        soup=BeautifulSoup(p.read_text(),'html.parser');pages[p.resolve()]=soup
        require(soup.html is not None and soup.html.get('lang')=='en','missing document language: '+str(p))
        require(bool(soup.select('meta[name="viewport"]')),'missing viewport: '+str(p))
        ids=[node['id'] for node in soup.select('[id]')];ids_by_path[p.resolve()]=set(ids)
        require(len(ids)==len(set(ids)),'duplicate IDs: '+str(p))
        require(not soup.select('input[type="file"], form, object, embed'),'unexpected upload/embed surface: '+str(p))
        require(not soup.select('iframe') or p == docs/'interface-review.html','iframe outside explicit responsive review page: '+str(p))
        for frame in soup.select('iframe'):require(frame.get('title') and frame.get('src','').startswith(PREFIX.as_posix()+'/'),'unexpected responsive frame target')
        for node in soup.find_all(True):
            require(not any(k.lower().startswith('on') for k in node.attrs),'inline event handler: '+str(p))
            for attr in ['src','poster']:
                if node.has_attr(attr):require(not urlsplit(node[attr]).scheme and not node[attr].startswith('//'),'external active asset: '+node[attr])
            if node.name=='link' and 'stylesheet' in node.get('rel',[]):require(not urlsplit(node.get('href','')).scheme,'external stylesheet')
        for script in soup.find_all('script'):
            if script.get('type')=='application/ld+json':continue
            require(script.get('src','').endswith('/filter.js') or script.get('src')=='filter.js','unexpected runtime script: '+str(p))
    for p,soup in pages.items():
        for node in soup.find_all(['a','img','script','link']):
            url=node.get('href') or node.get('src') or '';u=urlsplit(url)
            if not url or u.scheme or url.startswith('//'):continue
            links+=1;target=(p.parent/unquote(u.path)).resolve() if u.path else p
            require(target.is_relative_to(docs.resolve()),'local link escapes document root: '+url)
            require(target.exists(),'missing local target: '+str(p.relative_to(docs.resolve()))+' -> '+url)
            if u.fragment and target.suffix=='.html' and target in pages:
                frag=unquote(u.fragment)
                require(frag in ids_by_path[target],'missing fragment: '+str(p.relative_to(docs.resolve()))+' -> '+url)
    for css in version.rglob('*.css'):
        require(not re.search(r'url\(\s*[\'\"]?(?:https?:)?//',css.read_text()),'remote CSS resource: '+str(css))
        require('@import' not in css.read_text(),'CSS import requires review: '+str(css))
    for svg in (version/'assets').glob('*.svg'):
        text=svg.read_text();require('<script' not in text and '<image' not in text,'active or embedded SVG content: '+str(svg))
    original=frozen(OWL_SOURCE);graph=Graph().parse(data=original.decode(),format='turtle')
    receipt=json.loads((version/'widoco/serialization-receipt.json').read_text())
    require(receipt['source_commit']==COMMIT and receipt['source_sha256']==digest(original),'wrong serialization provenance')
    for name,fmt in [('ontology.ttl','turtle'),('ontology.nt','nt'),('ontology.owl','xml'),('ontology.jsonld','json-ld')]:
        path=version/'widoco'/name
        require(digest(path.read_bytes())==receipt['files_sha256'][name],'serialization digest mismatch: '+name)
        require(isomorphic(graph,Graph().parse(path,format=fmt)),'serialization graph mismatch: '+name)
    require((version/'widoco/ontology.ttl').read_bytes()==original,'Turtle is not byte-identical')
    provenance=json.loads((version/'widoco/tool-provenance.json').read_text())
    require(provenance['configuration_sha256']==digest((TOOLS/'widoco.properties').read_bytes()),'stale WIDOCO configuration')
    require(provenance['postprocessor_sha256']==digest((TOOLS/'run_widoco.py').read_bytes()),'stale WIDOCO postprocessor')
    for name,sha in provenance['files_sha256'].items():require(digest((version/'widoco'/name).read_bytes())==sha,'WIDOCO output changed: '+name)
    for line in (version/'downloads/SHA256SUMS.txt').read_text().splitlines():
        sha,name=line.split('  ',1);require(digest((version/'downloads'/name).read_bytes())==sha,'download hash mismatch: '+name)
    model=json.loads(frozen(MODEL));native=pages[(version/'reference/native/index.html').resolve()]
    require(len(native.select('.entry'))==305,'conceptual reference count differs from 305')
    for family in ['concepts','associations','generalizations','constraints']:
        for item in model[family]:require(item['id'] in ids_by_path[(version/'reference/native/index.html').resolve()],'conceptual entity missing: '+item['id'])
    explorer=json.loads((version/'explore/graph.json').read_text())
    require(explorer['source_commit']==COMMIT and explorer['source_sha256']==digest(original),'wrong explorer provenance')
    classes={s for s in graph.subjects(RDF.type,OWL.Class) if isinstance(s,URIRef)}
    props={s for s in graph.subjects(RDF.type,OWL.ObjectProperty) if isinstance(s,URIRef)}
    terms={row['iri']:row for row in explorer['terms']}
    require(set(terms)==set(map(str,classes|props)),'explorer inventory differs from asserted graph')
    def ids(values):return sorted(str(x).removeprefix(NAMESPACE) for x in values)
    for s in classes:
        row=terms[str(s)]
        expected={'parents':ids(set(graph.objects(s,RDFS.subClassOf))&classes),'children':ids(set(graph.subjects(RDFS.subClassOf,s))&classes),'outgoing':ids(set(graph.subjects(RDFS.domain,s))&props),'incoming':ids(set(graph.subjects(RDFS.range,s))&props)}
        for key,value in expected.items():require(row[key]==value,'wrong class neighborhood '+str(s)+' '+key)
    for s in props:
        row=terms[str(s)]
        for key,p in [('domain',RDFS.domain),('range',RDFS.range)]:require(row[key]==ids(graph.objects(s,p)),'wrong property endpoint '+str(s))
    exp=pages[(version/'explore/index.html').resolve()]
    require(len(exp.select('.entry'))==len(classes|props),'explorer HTML inventory differs from graph')
    for row in terms.values():require(row['id'] in ids_by_path[(version/'explore/index.html').resolve()],'explorer HTML term absent: '+row['id'])
    require((docs/'THIRD-PARTY-DOCUMENTATION.txt').exists() and (docs/'WIDOCO-Apache-2.0.txt').exists(),'missing template notices')
    runtime=(version/'assets/filter.js').read_text()
    require(not re.search(r'\b(fetch|XMLHttpRequest|WebSocket|sendBeacon|localStorage|sessionStorage)\b',runtime),'runtime network/storage behavior requires review')
    require(runtime==(TOOLS/'filter.js').read_text(),'stale filter script')
    if errors:raise ValueError('\n'.join(errors))
    return {'status':'PASS','scope':'Documentation/source/serialization/interface structure checks; not ontology validation or browser execution.','release':TAG,'semantic_source_commit':COMMIT,'html_pages':len(pages),'local_links_checked':links,'conceptual_entries':305,'explorer_classes':len(classes),'explorer_object_properties':len(props),'owl_triples':len(graph),'graph_isomorphic_serializations':4,'runtime_external_assets':0,'upload_surfaces':0,'limitations':['Browser keyboard/mobile and deployed readback are recorded separately.','External source hyperlinks are not asserted to be dereferenceable vocabulary endpoints.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args()
    result=audit(ROOT/'docs')
    if args.write:(ROOT/'evaluation/documentation-audit.json').write_text(json_text(result))
    print(json_text(result))
