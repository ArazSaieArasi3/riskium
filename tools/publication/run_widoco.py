"""Regenerate the pinned WIDOCO view, preserving the released RDF graph."""
from pathlib import Path
import argparse, hashlib, json, re, shutil, subprocess, tempfile
import xml.etree.ElementTree as ET
import markdown
from bs4 import BeautifulSoup
from rdflib import Graph, RDF, BNode, Literal
from rdflib.compare import to_canonical_graph, isomorphic
from rdflib.namespace import split_uri
from build_portal import ROOT, TOOLS, PREFIX, TAG, COMMIT, OWL_SOURCE, frozen, digest, json_text

JAR_SHA256 = 'be57a270fffb91e55810fa308717e704a44e2e7c027a3d68125a49da6c8b4e2b'
DOWNLOAD = 'https://github.com/dgarijo/Widoco/releases/download/v1.4.25/widoco-1.4.25-jar-with-dependencies_JDK-17.jar'

def ordered(value):
    if isinstance(value,dict):return {k:ordered(v) for k,v in sorted(value.items())}
    if isinstance(value,list):return sorted((ordered(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    return value

def finish(raw, out):
    out.mkdir(parents=True,exist_ok=True)
    soup = BeautifulSoup((raw/'index-en.html').read_text(), 'html.parser')
    soup.html['lang']='en'
    viewport=soup.new_tag('meta',attrs={'name':'viewport','content':'width=device-width,initial-scale=1'});soup.head.append(viewport)
    for script in list(soup.find_all('script')):
        if script.get('type')=='application/ld+json':
            data=json.loads(script.string);data['url']='https://github.com/ArazSaieArasi3/riskium/releases/tag/'+TAG
            data.pop('dateReleased',None);data.pop('image',None);script.string=json.dumps(data,sort_keys=True)
        else:script.decompose()
    for node in soup.select('.darkmode, meta[name="color-scheme"]'):node.decompose()
    for node in soup.select('link[rel="stylesheet"]'):
        if Path(node['href']).name in {'dark.css','light.css','slider.css'}:node.decompose()
    for node in list(soup.select('.markdown')):
        node.replace_with(BeautifulSoup(markdown.markdown(node.get_text()),'html.parser'))
    for img in list(soup.find_all('img')):img.replace_with(soup.new_string(img.get('alt','')))
    # WIDOCO's default header uses placeholder dates and a term namespace as
    # ontology IRI. Replace display metadata; the source ontology stays intact.
    meta=soup.select_one('.head dl');meta.clear()
    fields=[('Documentation source','<a href="../index.html">Riskium documentation portal</a>'),
            ('Release','<a href="https://github.com/ArazSaieArasi3/riskium/releases/tag/'+TAG+'">'+TAG+'</a>'),
            ('Ontology IRI','<code>https://github.com/ArazSaieArasi3/riskium/ontologies/riskium</code>'),
            ('Version IRI','<code>https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1</code>'),
            ('Source commit','<code>'+COMMIT+'</code>'),('Source SHA-256','<code>'+digest(frozen(OWL_SOURCE))+'</code>'),
            ('Authors','Araz Saie Arasi; Hassan Haghighi; Hossein Azgomi. <a href="../guide/Citation.html">Affiliations and citation</a>.'),
            ('Reuse','<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>; <a href="../downloads/RIGHTS.md">scopes and exclusions</a>.'),
            ('Download','<a href="ontology.ttl">Turtle</a> · <a href="ontology.owl">RDF/XML</a> · <a href="ontology.jsonld">JSON-LD</a> · <a href="ontology.nt">N-Triples</a>')]
    for label,value in fields:
        dt=soup.new_tag('dt');dt.string=label;dd=soup.new_tag('dd');dd.append(BeautifulSoup(value,'html.parser'));meta.extend([dt,dd])
    nav=BeautifulSoup('<nav aria-label="Documentation"><a href="../index.html">Overview</a> · <a href="../reference/native/index.html">Conceptual reference</a> · <a href="../explore/index.html">Explore OWL</a> · <a href="../guide/Evaluation.html">Evaluation</a> · <a href="../downloads/index.html">Downloads</a></nav><p class="riskium-note">Bounded typed-core export: 77 local classes, one local external-anchor proxy and 127 object properties. Three optional concepts and seven bridges are excluded. Ontology IRIs identify terms; they are not claims of deployed endpoints. Independent semantic acceptance remains open. This documentation was generated after the prerelease from its exact semantic source.</p>','html.parser')
    soup.select_one('.head').insert(0,nav)
    # The upstream template repeats the annotation-properties section ID.
    duplicate=soup.select_one('h3#annotationproperties')
    if duplicate:duplicate['id']='annotationproperties-headline'
    toc=soup.select_one('#toc');toc.clear();toc.append(BeautifulSoup('<h2>Table of contents</h2><ul>'+''.join('<li><a href="#'+h['id']+'">'+h.get_text().split(' back to')[0]+'</a></li>' for h in soup.select('h2.list[id],h3.list[id]'))+'</ul>','html.parser'))
    css=soup.new_tag('style');css.string='body{overflow-wrap:anywhere}nav{margin:1rem 0;line-height:1.8}.riskium-note{border-left:4px solid #135a7a;background:#f2f6f8;padding:1rem;color:#172b3a}.entity{scroll-margin-top:1rem}a:focus-visible{outline:3px solid #b45a13;outline-offset:3px}img{max-width:100%}pre{white-space:pre-wrap}@media(max-width:760px){body{padding:1rem!important;margin:0!important;min-width:0!important}.container{width:100%!important;padding:0!important}.status{display:none}.entity{padding:.65rem!important}h1{font-size:1.8rem}dl{margin-left:0}}';soup.head.append(css)
    # Preserve upstream generator credits, mark our post-processing.
    footer=soup.new_tag('p');footer.append(BeautifulSoup('WIDOCO 1.4.25 output modified by Riskium: static table of contents and Markdown, explicit release metadata, local navigation and exact-graph downloads. No remote scripts, badge images or upload service. <a href="../../../THIRD-PARTY-DOCUMENTATION.txt">Template notices</a>.','html.parser'));soup.select_one('#acknowledgments').append(footer)
    (out/'index-en.html').write_text(str(soup)+'\n')
    (out/'resources').mkdir(exist_ok=True)
    for name in ['primer.css','rec.css','extra.css','owl.css']:shutil.copyfile(raw/'resources'/name,out/'resources'/name)
    # No WIDOCO/OWL API reserialization replaces the pinned semantic graph.
    source=frozen(OWL_SOURCE);graph=to_canonical_graph(Graph().parse(data=source.decode(),format='turtle'))
    (out/'ontology.ttl').write_bytes(source)
    (out/'ontology.nt').write_text('\n'.join(sorted(graph.serialize(format='nt').splitlines()))+'\n')
    (out/'ontology.jsonld').write_text(json_text(ordered(json.loads(graph.serialize(format='json-ld')))))
    xml=ET.Element('{'+str(RDF)+'}RDF')
    for subject in sorted(set(graph.subjects()),key=lambda s:s.n3()):
        node=ET.SubElement(xml,'{'+str(RDF)+'}Description',{'{'+str(RDF)+('}nodeID' if isinstance(subject,BNode) else '}about'):str(subject)})
        for predicate,value in sorted(graph.predicate_objects(subject),key=lambda x:(str(x[0]),x[1].n3())):
            ns,name=split_uri(predicate);item=ET.SubElement(node,'{'+ns+'}'+name)
            if isinstance(value,Literal):
                item.text=str(value)
                if value.language:item.set('{http://www.w3.org/XML/1998/namespace}lang',value.language)
                if value.datatype:item.set('{'+str(RDF)+'}datatype',str(value.datatype))
            else:item.set('{'+str(RDF)+('}nodeID' if isinstance(value,BNode) else '}resource'),str(value))
    (out/'ontology.owl').write_text(ET.canonicalize(ET.tostring(xml,encoding='unicode'),rewrite_prefixes=True))
    hashes={}
    for name,fmt in [('ontology.ttl','turtle'),('ontology.nt','nt'),('ontology.owl','xml'),('ontology.jsonld','json-ld')]:
        if not isomorphic(graph,Graph().parse(out/name,format=fmt)):raise ValueError('Graph changed in '+name)
        hashes[name]=digest((out/name).read_bytes())
    (out/'serialization-receipt.json').write_text(json_text({'source_commit':COMMIT,'source_path':OWL_SOURCE,'source_sha256':digest(source),'rdf_triples':len(graph),'graph_isomorphic_to_source':True,'files_sha256':hashes}))
    provenance=out/'provenance';provenance.mkdir(exist_ok=True)
    (provenance/'provenance-en.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>WIDOCO generation provenance</title></head><body><h1>WIDOCO generation provenance</h1><p>WIDOCO 1.4.25, verified jar SHA-256 <code>'+JAR_SHA256+'</code>, generated this view from commit <code>'+COMMIT+'</code>. Riskium post-processing makes the page static and replaces display metadata and downloads; it does not change the source OWL graph.</p><p><a href="../index-en.html">Return to the OWL reference</a> · <a href="../serialization-receipt.json">Serialization verification</a> · <a href="../tool-provenance.json">Tool and configuration receipt</a></p></body></html>\n')
    output_hashes={p.relative_to(out).as_posix():digest(p.read_bytes()) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='tool-provenance.json'}
    (out/'tool-provenance.json').write_text(json_text({'widoco_version':'1.4.25','jar_download':DOWNLOAD,'jar_sha256':JAR_SHA256,'source_commit':COMMIT,'source_sha256':digest(source),'configuration_sha256':digest((TOOLS/'widoco.properties').read_bytes()),'postprocessor_sha256':digest(Path(__file__).read_bytes()),'files_sha256':output_hashes,'runtime_network':'No scripts, remote active assets, uploads or analytics in the published WIDOCO page. External hyperlinks load only when followed.'}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--jar',type=Path,required=True);args=parser.parse_args()
    if digest(args.jar.read_bytes())!=JAR_SHA256:raise SystemExit('Unexpected WIDOCO jar digest')
    with tempfile.TemporaryDirectory() as tmp:
        temp=Path(tmp);source=temp/'riskium.owl.ttl';source.write_bytes(frozen(OWL_SOURCE));raw=temp/'raw'
        subprocess.run(['java','-jar',str(args.jar.resolve()),'-ontFile',str(source),'-outFolder',str(raw),'-confFile',str(TOOLS/'widoco.properties'),'-rewriteAll','-includeAnnotationProperties','-uniteSections','-noPlaceHolderText','-lang','en'],cwd=temp,check=True)
        finish(raw,ROOT/'docs'/PREFIX/'widoco')
    print(json.dumps({'release':TAG,'source_commit':COMMIT,'widoco':'1.4.25','jar_sha256':JAR_SHA256}))
