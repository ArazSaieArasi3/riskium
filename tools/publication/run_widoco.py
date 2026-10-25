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
    # Retain the genuine LODE/WIDOCO entities, expressions and anchors. The
    # project presentation adds reading context without rewriting declarations.
    for node in soup.select('.head, .status, #toc, #abstract, #namespacedeclarations'):
        node.decompose()
    for node in soup.find_all(['style','link']):
        node.decompose()
    for h in soup.select('h3#annotationproperties'):
        h['id']='annotationproperties-headline'
    for entity in soup.select('.entity'):
        entity['class']=entity.get('class',[])+['entry']
        ident=entity.get('id')
        if ident and ident.startswith(('RKM-','RX-','RK2-','RK3-','R-','EXT-')):
            extra=BeautifulSoup('<p class="term-links"><a href="../reference/native/index.html#'+ident+'">Conceptual definition</a><a href="../explore/index.html#'+ident+'">Text neighborhood</a></p>','html.parser')
            entity.append(extra)
    for node in soup.select('.entity:not([id])'):
        node['class']=[c for c in node.get('class',[]) if c != 'entry']
    structured=''.join(str(n) for n in soup.head.select('script[type="application/ld+json"]'))
    crossref=''.join(str(n) for n in soup.body.contents)
    metadata='<details class="source-record"><summary>Ontology identity, exact source and reuse</summary><dl><dt>Ontology IRI</dt><dd><code>https://github.com/ArazSaieArasi3/riskium/ontologies/riskium</code></dd><dt>Version IRI</dt><dd><code>https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1</code></dd><dt>Semantic source</dt><dd><a href="https://github.com/ArazSaieArasi3/riskium/tree/'+COMMIT+'">'+COMMIT+'</a></dd><dt>Turtle SHA-256</dt><dd><code>'+digest(frozen(OWL_SOURCE))+'</code></dd><dt>Authors</dt><dd>Araz Saie Arasi; Hassan Haghighi; Hossein Azgomi. <a href="../guide/Citation.html">Affiliations and citation</a>.</dd><dt>Reuse</dt><dd>CC BY 4.0 for scientific content. <a href="../downloads/RIGHTS.md">Rights and exclusions</a>.</dd></dl><p><a href="provenance/provenance-en.html">WIDOCO generation record</a></p></details>'
    intro='<p class="eyebrow">WIDOCO 1.4.25 · Ontology model 0.3.1</p><h1>Riskium OWL reference</h1><p class="lead">The asserted logical commitments of the typed conceptual core, with definitions and links between classes and properties.</p><div class="actions"><a class="button primary" href="#classes">Browse classes</a><a class="button" href="#objectproperties">Browse properties</a><a class="button" href="../webvowl/index.html">Explore the graph</a></div><h2 id="abstract">Abstract</h2><p>Riskium distinguishes a continuing risk case from its records, scenario specifications, assessment artifacts and supporting evidence. This bounded OWL mapping expresses selected class, relation and restriction commitments from the conceptual model. It is narrower than the full conceptual catalog.</p><p class="note">77 local named classes, one local external-anchor proxy and 127 object properties. Three optional concepts and seven bridges are outside this export. The local anchor does not establish an external import closure.</p><h2 id="introduction">How to read this reference</h2><p>Each entry gives its IRI, definition when supplied, and the axioms asserted in the source. Domain and range statements describe OWL typing commitments; they are not data-admission checks. OWL uses an open-world interpretation and does not assume that different names denote different individuals. Read the <a href="../guide/Formalization.html">formalization explanation</a> for mapping limits and the separate SHACL/application routes.</p><label for="filter">Find a class or property</label><input type="search" id="filter" placeholder="For example: RiskCase or appliesPattern" aria-describedby="filter-status"><p id="filter-status" role="status" aria-live="polite">215 of 215 entries shown</p><noscript><p>All entries and in-page term links remain available without JavaScript.</p></noscript><details><summary>RDF downloads</summary><p><a href="ontology.ttl" download="ontology.ttl">Turtle</a> · <a href="ontology.owl" download="ontology.owl">RDF/XML</a> · <a href="ontology.jsonld" download="ontology.jsonld">JSON-LD</a> · <a href="ontology.nt" download="ontology.nt">N-Triples</a></p><p>The original Turtle is byte-preserved. <a href="serialization-receipt.json">All four serializations are graph-isomorphic</a>.</p></details>'+metadata
    intro+='<nav id="toc" aria-label="Reference sections"><h2>Reference contents</h2><ul class="hlist"><li><a href="#overv">Term index</a></li><li><a href="#classes">Classes</a></li><li><a href="#objectproperties">Object properties</a></li><li><a href="#annotationproperties">Annotation properties</a></li><li><a href="#interpretation">Scope and evidence</a></li></ul></nav>'
    tail='<h2 id="interpretation">Scope and evidence</h2><p>Restrictions, disjointness and other asserted axioms remain in the entries and exact RDF. The WebVOWL graph shows only named endpoints and subclass links. Neither a generated reference nor a successful reasoner check establishes domain adequacy or independent semantic acceptance. <a href="../guide/Evaluation.html">Evaluation and limitations</a> explains the executed evidence populations.</p><h2 id="namespaces">Namespace declarations</h2><table><thead><tr><th>Prefix</th><th>Namespace</th></tr></thead><tbody>'
    for prefix,uri in sorted(Graph().parse(data=frozen(OWL_SOURCE).decode(),format='turtle').namespaces()):
        if str(uri) in ['http://www.w3.org/2002/07/owl#','http://www.w3.org/1999/02/22-rdf-syntax-ns#','http://www.w3.org/2000/01/rdf-schema#','http://www.w3.org/2001/XMLSchema#'] or str(uri).startswith('https://github.com/ArazSaieArasi3/riskium/ontologies/'):
            tail+='<tr><td>'+str(prefix)+'</td><td><code>'+str(uri)+'</code></td></tr>'
    tail+='</tbody></table><h2 id="reference-sources">Sources and generator</h2><p><a href="../guide/References.html">Research sources</a> · <a href="../reference/native/index.html">Complete conceptual catalog</a> · <a href="../guide/Publication.html">Model and distribution versions</a></p><p>Cross-reference generated by WIDOCO 1.4.25 using LODE. Riskium adds static navigation, authored context, local filtering, accessible styles and exact-source downloads. Upstream entity/axiom content is retained. <a href="../../THIRD-PARTY-DOCUMENTATION.txt">Template notices</a>.</p>'
    from presentation import render
    page=render(Path('current/widoco/index-en.html'), 'OWL reference', '<div class="widoco">'+intro+crossref+tail+'</div>',
        head=structured+'<link rel="stylesheet" href="resources/primer.css"><link rel="stylesheet" href="resources/rec.css"><link rel="stylesheet" href="resources/extra.css"><link rel="stylesheet" href="resources/owl.css"><link rel="stylesheet" href="resources/riskium.css?v='+digest((TOOLS/'widoco.css').read_bytes())[:12]+'">', scripts='<script defer src="../assets/filter.js"></script>')
    (out/'index-en.html').write_text(page)
    (out/'resources').mkdir(exist_ok=True)
    for name in ['primer.css','rec.css','extra.css','owl.css']:shutil.copyfile(raw/'resources'/name,out/'resources'/name)
    shutil.copyfile(TOOLS/'widoco.css',out/'resources/riskium.css')
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
    (provenance/'provenance-en.html').write_text(render(Path('current/widoco/provenance/provenance-en.html'), 'WIDOCO generation record', '<h1>WIDOCO generation record</h1><p>WIDOCO 1.4.25 generated the cross-reference from the exact model 0.3.1 source. Riskium adds the common documentation shell and authored reading context; the source OWL graph and generated entity commitments are preserved.</p><dl><dt>Verified jar SHA-256</dt><dd><code>'+JAR_SHA256+'</code></dd><dt>Semantic source</dt><dd><code>'+COMMIT+'</code></dd></dl><p><a href="../index-en.html">Return to the OWL reference</a> · <a href="../serialization-receipt.json">Serialization verification</a> · <a href="../tool-provenance.json">Tool and configuration receipt</a></p>'))
    output_hashes={p.relative_to(out).as_posix():digest(p.read_bytes()) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='tool-provenance.json'}
    (out/'tool-provenance.json').write_text(json_text({'widoco_version':'1.4.25','jar_download':DOWNLOAD,'jar_sha256':JAR_SHA256,'source_commit':COMMIT,'source_sha256':digest(source),'configuration_sha256':digest((TOOLS/'widoco.properties').read_bytes()),'postprocessor_sha256':digest(Path(__file__).read_bytes()),'files_sha256':output_hashes,'runtime_network':'Only local text filtering. No remote active assets, uploads, storage or analytics. External hyperlinks load only when followed.'}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--jar',type=Path,required=True);args=parser.parse_args()
    if digest(args.jar.read_bytes())!=JAR_SHA256:raise SystemExit('Unexpected WIDOCO jar digest')
    with tempfile.TemporaryDirectory() as tmp:
        temp=Path(tmp);source=temp/'riskium.owl.ttl';source.write_bytes(frozen(OWL_SOURCE));raw=temp/'raw'
        subprocess.run(['java','-jar',str(args.jar.resolve()),'-ontFile',str(source),'-outFolder',str(raw),'-confFile',str(TOOLS/'widoco.properties'),'-rewriteAll','-includeAnnotationProperties','-uniteSections','-noPlaceHolderText','-lang','en'],cwd=temp,check=True)
        finish(raw,ROOT/'docs'/PREFIX/'widoco')
    print(json.dumps({'release':TAG,'source_commit':COMMIT,'widoco':'1.4.25','jar_sha256':JAR_SHA256}))
