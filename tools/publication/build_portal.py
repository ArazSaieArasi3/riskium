"""Build the OntoSPK-style portal from an immutable Riskium semantic source."""
from pathlib import Path
import argparse, hashlib, html, json, os, re, shutil, subprocess, tempfile
from urllib.parse import urlsplit, unquote
import markdown
from bs4 import BeautifulSoup
from rdflib import Graph, RDF, RDFS, OWL, URIRef, BNode, Literal

ROOT = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
TAG = 'v0.3.1-rc.1'
COMMIT = 'cfb85905ab37549c7090f00a41ca62cdd3364ab5'
PREFIX = Path('releases') / TAG
REPO = 'https://github.com/ArazSaieArasi3/riskium'
MODEL = 'ontology/riskium-model.json'
OWL_SOURCE = 'ontology/derived/riskium.owl.ttl'
NAMESPACE = 'https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#'
GUIDES = [('Overview', 'docs/overview.md'), ('Decisions', 'docs/modeling-decisions.md'),
          ('Requirements', 'requirements/ontology-requirements.md'),
          ('Artifact-Versions', 'docs/artifact-versions.md'),
          ('Competency-Questions', 'requirements/cq/README.md'),
          ('Traceability', 'evaluation/traceability/README.md'),
          ('References', 'references/README.md'),
          ('Quality', 'evaluation/quality/README.md'),
          ('Formalization', 'evaluation/owl-mapping-review.md'),
          ('Evaluation', 'evaluation/README.md'), ('Reproduce', 'docs/reproducibility.md'),
          ('Citation', 'AUTHORS.md'), ('Limitations', 'docs/portal-limitations.md')]

def digest(data): return hashlib.sha256(data).hexdigest()
def esc(value): return html.escape(str(value), quote=True)
def frozen(path):
    return subprocess.check_output(['git', 'show', f'{COMMIT}:{path}'], cwd=ROOT)
def json_text(data): return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + '\n'
def href(path): return REPO + '/blob/' + COMMIT + '/' + path

def build(out):
    resolved = subprocess.check_output(['git', 'rev-parse', TAG + '^{commit}'], cwd=ROOT, text=True).strip()
    if resolved != COMMIT: raise ValueError('Published release tag no longer matches the fixed semantic source')
    version = out / PREFIX
    version.mkdir(parents=True, exist_ok=True)
    inputs = {}
    def source(path):
        data = frozen(path); inputs[path] = digest(data); return data
    def write(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode())
    model = json.loads(source(MODEL))
    owl_bytes = source(OWL_SOURCE)
    graph = Graph().parse(data=owl_bytes.decode(), format='turtle')
    hermit = json.loads(source('evaluation/hermit/report.json'))
    shacl = json.loads(source('evaluation/shacl/coverage-status.json'))
    if shacl['source_sha256'] != inputs[MODEL] or shacl['baseline'] != 359:
        raise ValueError('SHACL ledger does not match the frozen model and denominator')
    if hermit['inputs']['owl_turtle_sha256'] != inputs[OWL_SOURCE] or hermit['model_version'] != model['version']:
        raise ValueError('HermiT receipt does not match frozen OWL and model version')
    concepts = {x['id']:x for x in model['concepts'] + model['imported_types']}
    classes = sorted({s for s in graph.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)}, key=str)
    properties = sorted({s for s in graph.subjects(RDF.type, OWL.ObjectProperty) if isinstance(s, URIRef)}, key=str)
    names = {str(s):str(graph.value(s, RDFS.label) or s) for s in classes + properties}
    def rel(target, base): return os.path.relpath(target, base).replace(os.sep, '/')
    def link(label, target): return '<a href="'+esc(target)+'">'+esc(label)+'</a>'
    def local(label, target, base): return link(label, rel(version/target, base))
    def page(path, title, body, filtering=False):
        target = version/path; base = target.parent
        soup = BeautifulSoup(body, 'html.parser')
        if str(path) == 'downloads/index.html':
            for anchor in soup.find_all('a', href=True):
                url = urlsplit(anchor['href'])
                if url.path and not url.scheme and not url.path.endswith('.html'):
                    anchor['download'] = Path(url.path).name
        toc = []
        for i, heading in enumerate(soup.find_all('h2'), 1):
            if not heading.get('id'): heading['id'] = 'section-'+str(i)
            toc.append(link(heading.get_text(), '#'+heading['id']))
        sections = [('Overview','index.html'),('Conceptual reference','reference/native/index.html'),
                    ('OWL reference','widoco/index-en.html'),('Evaluation','guide/Evaluation.html'),
                    ('Explore','explore/index.html'),('Downloads','downloads/index.html')]
        nav = ''.join('<a '+('aria-current="page" ' if str(path)==p else '')+'href="'+rel(version/p,base)+'">'+n+'</a>' for n,p in sections)
        sidebar = ''.join('<li><a '+('aria-current="page" ' if str(path)=='guide/'+n+'.html' else '')+'href="'+rel(version/('guide/'+n+'.html'),base)+'">'+n+'</a></li>' for n,_ in GUIDES)
        context = 'Development prerelease '+TAG+' · conceptual design '+esc(model['version'])+' · source '+link(COMMIT[:12], REPO+'/tree/'+COMMIT)
        footer = 'Scientific content: '+link('CC BY 4.0','https://creativecommons.org/licenses/by/4.0/')+'. Original software: MIT. Copyright 2026 Araz Saie Arasi, Hassan Haghighi and Hossein Azgomi, for their respective original contributions. '+local('Citation and affiliations','guide/Citation.html',base)+' · '+local('Scope and limitations','guide/Limitations.html',base)+' · '+link('Repository', REPO)+'. Documentation generated after the release; semantic source is the fixed commit above.'
        script = '<script defer src="'+rel(version/'assets/filter.js',base)+'"></script>' if filtering else ''
        document = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Riskium ontology documentation for '+TAG+'"><title>'+esc(title)+' — Riskium</title><link rel="stylesheet" href="'+rel(version/'assets/portal.css',base)+'">'+script+'</head><body><a class="skip-link" href="#content">Skip to content</a><header><a class="brand" href="'+rel(version/'index.html',base)+'">Riskium</a><p>An Ontology for Modeling Enterprise Risk Knowledge</p><nav aria-label="Primary">'+nav+'</nav></header><div class="publication-context">'+context+'</div><div class="layout"><aside class="sidebar" aria-label="Documentation navigation"><h2>Documentation</h2><ul>'+sidebar+'<li>'+local('Version and source record','publication-manifest.json',base)+'</li><li>'+link('GitHub Wiki',REPO+'/wiki')+'</li></ul></aside><main id="content" tabindex="-1">'+str(soup)+'</main><aside class="toc" aria-label="On this page"><h2>On this page</h2><ul>'+''.join('<li>'+a+'</li>' for a in toc)+'</ul></aside></div><footer>'+footer+'</footer></body></html>\n'
        write(target, document)
    def filter_box(count):
        return '<label for="filter">Filter by name, identifier or description</label><input id="filter" type="search" placeholder="For example: Risk Case" aria-describedby="filter-status"><p id="filter-status" role="status" aria-live="polite">'+str(count)+' of '+str(count)+' entries shown</p><noscript><p>All entries and term links remain available without JavaScript.</p></noscript>'
    write(version/'assets/portal.css', (TOOLS/'portal.css').read_bytes())
    write(version/'assets/filter.js', (TOOLS/'filter.js').read_bytes())
    write(version/'assets/selected-model.svg', source('diagrams/selected-view.svg'))
    write(version/'assets/complete-model.svg', source('diagrams/complete-view.svg'))
    coverage = shacl['outcomes']; reasoned = hermit['coverage']
    coverage_text = f"HermiT: {sum(x['status']=='PASS' for x in hermit['cases'])} executed cases PASS; {reasoned['outcomes']['PASS']}/{reasoned['baseline_obligations']} baseline obligations, {reasoned['outcomes']['NOT_RUN']} NOT_RUN. SHACL: {coverage['PASS']} scoped PASS, {coverage['PARTIAL']} PARTIAL and {coverage['NOT_RUN']} NOT_RUN of {shacl['baseline']} obligations."
    cards = [('Understand the model','Keep cases, entries, scenarios and evidence distinct.','guide/Overview.html','Read the overview'),('Inspect the conceptual source','Browse all 80 catalog concepts, 134 relations and 25 interpretation constraints.','reference/native/index.html','Conceptual reference'),('Read the OWL commitments','Inspect 78 named classes, including the local anchor, and 127 object properties.','widoco/index-en.html','WIDOCO reference'),('Explore and reproduce','Follow asserted parent and relation links; inspect the exact source and finite evidence.','explore/index.html','Explore the typed core')]
    body = '<h1>Enterprise risk knowledge, explicitly modeled</h1><p class="eyebrow">Conceptual design 0.3.1 · WIDOCO reference</p><p>Riskium distinguishes a managed risk case from register entries, scenario specifications, assessment results and supporting evidence. Use the conceptual guide for meaning, the OWL reference for asserted logical commitments, and evaluation for the scope of executed checks.</p><p class="note">The first '+link('development prerelease '+TAG,REPO+'/releases/tag/'+TAG)+' is published. Independent semantic acceptance and a stable scientific release remain open.</p><div class="cards">'+''.join('<div class="card"><h2>'+t+'</h2><p>'+d+'</p>'+link(a,p)+'</div>' for t,d,p,a in cards)+'</div><h2>Evidence and limits</h2><p>'+coverage_text+'</p><p>These populations have different meanings. Their counts do not estimate overall semantic correctness. C-08 remains partial; external alignment and full profile integration remain open.</p><h2>Selected conceptual view</h2><p>The selected diagram is a subset. The complete catalog, optional boundaries and local external anchor are distinguished in the reference.</p><a href="assets/selected-model.svg"><img src="assets/selected-model.svg" alt="Selected conceptual view of Riskium; open the source SVG to inspect labels"></a><p>'+link('Complete diagram','assets/complete-model.svg')+' · '+link('Verified downloads','downloads/index.html')+'</p>'
    page(Path('index.html'), 'Enterprise risk knowledge, explicitly modeled', body)
    # The model owns every definition; no manually maintained duplicate catalog.
    body = '<h1>Conceptual reference</h1><p>Conceptual design 0.3.1: 80 catalog concepts, including 77 typed concepts and three optional boundaries; one local external anchor is listed separately. There are 134 associations or bridges, 66 generalizations and 25 interpretation constraints. This full catalog is broader than the bounded OWL export.</p>'+filter_box(305)
    body += '<h2 id="domains">Domains</h2><ul>'+''.join('<li><b>'+esc(d['title'])+'</b>: '+esc(d['definition'])+'</li>' for d in model['domains'])+'</ul><h2 id="concepts">Concepts</h2>'
    for c in model['concepts']:
        owl = '<a href="../../explore/index.html#'+esc(c['id'])+'">Explore OWL neighborhood</a>' if URIRef(NAMESPACE+c['id']) in classes else 'Optional boundary; excluded from typed OWL export.'
        body += '<article class="entry" id="'+esc(c['id'])+'"><h3>'+esc(c['display_title'])+'</h3><p>'+esc(c['definition'])+'</p><p class="meta">'+esc(c['id'])+' · '+esc(c['domain'])+' · '+esc(c['scope_layer'])+' · '+esc(c['ontouml_stereotype'] or 'untyped boundary')+'</p><p>'+owl+'</p></article>'
    body += '<h2 id="anchor">External anchor</h2>'
    for c in model['imported_types']:
        body += '<article id="'+esc(c['id'])+'"><h3>'+esc(c['display_title'])+'</h3><p>'+esc(c['definition'])+'</p><p>Local proxy only; no external import closure is asserted. '+link('Explore asserted OWL neighborhood','../../explore/index.html#'+c['id'])+'</p></article>'
    body += '<h2 id="relations">Relations</h2><table><thead><tr><th>Relation</th><th>Source (end count)</th><th>Target (end count)</th><th>Meaning</th></tr></thead><tbody>'
    for r in model['associations']:
        body += '<tr class="entry" id="'+esc(r['id'])+'"><td>'+esc(r['predicate'])+'<br>'+esc(r['id'])+'</td><td>'+link(r['source_title'],'#'+r['source'])+' ('+esc(r['source_end_cardinality'])+')</td><td>'+link(r['target_title'],'#'+r['target'])+' ('+esc(r['target_end_cardinality'])+')</td><td>'+esc(r['rationale'])+'</td></tr>'
    body += '</tbody></table><h2 id="generalizations">Generalizations</h2><ul>'
    for g in model['generalizations']:
        body += '<li class="entry" id="'+esc(g['id'])+'">'+link(concepts[g['specific']]['display_title'],'#'+g['specific'])+' is a '+link(concepts[g['general']]['display_title'],'#'+g['general'])+'.</li>'
    body += '</ul><h2 id="constraints">Interpretation constraints</h2>'
    for c in model['constraints']:
        body += '<article class="entry" id="'+esc(c['id'])+'"><h3>'+esc(c['title'])+'</h3><p>'+esc(c['statement'])+'</p><p class="meta">'+esc(c['id'])+'</p></article>'
    page(Path('reference/native/index.html'), 'Conceptual reference', body, True)
    # Alternative explorer: accessible local hypertext, grounded only in asserted RDF.
    def term_id(s): return str(s).removeprefix(NAMESPACE)
    def term_link(s): return link(names.get(str(s), term_id(s)), '#'+term_id(s))
    def expression(value):
        if isinstance(value, URIRef): return graph.namespace_manager.normalizeUri(value)
        if isinstance(value, Literal): return value.n3()
        if isinstance(value, BNode):
            return '[ '+' ; '.join(expression(p)+' '+expression(o) for p,o in sorted(graph.predicate_objects(value),key=lambda x:(str(x[0]),expression(x[1]))))+' ]'
        return str(value)
    body = '<h1>Explore the asserted OWL core</h1><p>Follow the named class hierarchy and relation endpoints in the exact released OWL graph. This local hypertext explorer contains 78 named classes (77 local concepts and one anchor proxy) and 127 object properties. It does not infer new facts, upload an ontology or query a server. Optional conceptual boundaries are available in the '+link('full conceptual reference','../reference/native/index.html')+'.</p>'+filter_box(len(classes)+len(properties))
    body += '<details><summary>Jump to a class</summary><ul class="term-links">'+''.join('<li>'+term_link(s)+'</li>' for s in classes)+'</ul></details><h2 id="classes">Class neighborhoods</h2>'
    explorer_rows = []
    for s in classes:
        ident = term_id(s)
        parents = sorted({o for o in graph.objects(s,RDFS.subClassOf) if o in classes},key=str)
        children = sorted({x for x in graph.subjects(RDFS.subClassOf,s) if x in classes},key=str)
        outgoing = sorted(set(graph.subjects(RDFS.domain,s)) & set(properties),key=str)
        incoming = sorted(set(graph.subjects(RDFS.range,s)) & set(properties),key=str)
        row = {'id':ident,'iri':str(s),'label':names[str(s)],'parents':[term_id(x) for x in parents], 'children':[term_id(x) for x in children], 'outgoing':[term_id(x) for x in outgoing], 'incoming':[term_id(x) for x in incoming]}; explorer_rows.append(row)
        body += '<article class="entry" id="'+esc(ident)+'"><h3>'+esc(names[str(s)])+'</h3><p><code>'+esc(s)+'</code></p><p>'+esc(graph.value(s,RDFS.comment) or '')+'</p>'
        for label,values in [('Asserted named parents',parents),('Asserted named children',children),('Outgoing properties',outgoing),('Incoming properties',incoming)]:
            body += '<p><strong>'+label+':</strong> '+(' · '.join(term_link(x) for x in values) if values else 'None asserted.')+'</p>'
        body += '<p>'+link('Conceptual source','../reference/native/index.html#'+ident)+' · '+link('WIDOCO term','../widoco/index-en.html#'+term_id(s))+'</p></article>'
    body += '<h2 id="properties">Object properties</h2>'
    for s in properties:
        ident = term_id(s); domains = sorted(graph.objects(s,RDFS.domain),key=str); ranges = sorted(graph.objects(s,RDFS.range),key=str)
        explorer_rows.append({'id':ident,'iri':str(s),'label':names[str(s)],'domain':[term_id(x) for x in domains], 'range':[term_id(x) for x in ranges]})
        body += '<article class="entry" id="'+esc(ident)+'"><h3>'+esc(names[str(s)])+'</h3><p><code>'+esc(s)+'</code></p><p>Domain: '+' · '.join(term_link(x) for x in domains)+' → Range: '+' · '.join(term_link(x) for x in ranges)+'</p><p>'+link('Conceptual relation','../reference/native/index.html#'+ident)+' · '+link('WIDOCO term','../widoco/index-en.html#'+term_id(s))+'</p><details><summary>Asserted predicates and expressions</summary><pre>'+esc('\n'.join(expression(p)+' '+expression(o) for p,o in sorted(graph.predicate_objects(s),key=lambda x:(str(x[0]),expression(x[1])))))+'</pre></details></article>'
    page(Path('explore/index.html'), 'Explore the asserted OWL core', body, True)
    write(version/'explore/graph.json',json_text({'source_commit':COMMIT,'source_sha256':inputs[OWL_SOURCE],'mode':'asserted hypertext neighborhoods; no inference','terms':explorer_rows}))
    # Curated explanatory sources stay distinct from the frozen semantic inputs.
    mapping = {(ROOT/p).resolve():version/('guide/'+n+'.html') for n,p in GUIDES}
    mapping[(ROOT/MODEL).resolve()] = version/'downloads/riskium-model.json'
    mapping[(ROOT/OWL_SOURCE).resolve()] = version/'widoco/ontology.ttl'
    mapping[(ROOT/'diagrams/selected-view.svg').resolve()] = version/'assets/selected-model.svg'
    mapping[(ROOT/'diagrams/complete-view.svg').resolve()] = version/'assets/complete-model.svg'
    guide_inputs = {}
    for name,src in GUIDES:
        data = (ROOT/src).read_bytes(); guide_inputs[src] = digest(data)
        soup = BeautifulSoup(markdown.markdown(data.decode(),extensions=['tables','fenced_code','toc']), 'html.parser')
        base = (version/('guide/'+name+'.html')).parent
        for node in soup.find_all(['a','img']):
            attr = 'src' if node.name=='img' else 'href'; url = node.get(attr,''); u = urlsplit(url)
            if not url or u.scheme or url.startswith('#'): continue
            target = ((ROOT/src).parent / unquote(u.path)).resolve()
            if target in mapping: node[attr] = rel(mapping[target],base)
            elif target.is_relative_to(ROOT):
                p = target.relative_to(ROOT).as_posix()
                # Current narrative sources may postdate the semantic release.
                ref = COMMIT if subprocess.run(['git','cat-file','-e',COMMIT+':'+p],cwd=ROOT,stderr=subprocess.DEVNULL).returncode == 0 else 'main'
                node[attr] = REPO+('/tree/' if target.is_dir() else '/blob/')+ref+'/'+p
            if u.fragment: node[attr] += '#'+u.fragment
        if name == 'Evaluation':
            soup.insert(0,BeautifulSoup('<p class="note">Frozen release evidence: '+coverage_text+' Independent semantic acceptance remains open.</p>','html.parser'))
        page(Path('guide/'+name+'.html'), name, str(soup))
    downloads = [('ontology/riskium-model.json','riskium-model.json'),('ontology/native/riskium.ontouml.json','riskium.ontouml.json'),('ontology/derived/typed-core.json','typed-core.json'),('CITATION.cff','CITATION.cff'),('RIGHTS.md','RIGHTS.md'),('LICENSE','LICENSE'),('NOTICE.md','NOTICE.md'),('LICENSES/CC-BY-4.0.txt','CC-BY-4.0.txt'),('LICENSES/MIT.txt','MIT.txt')]
    hashes = {}
    for src,name in downloads:
        data = source(src); write(version/'downloads'/name,data); hashes[name] = digest(data)
    write(version/'downloads/SHA256SUMS.txt',''.join(d+'  '+n+'\n' for n,d in sorted(hashes.items())))
    body = '<h1>Downloads</h1><p>These conceptual and native files are byte-identical to commit <code>'+COMMIT+'</code>. The OWL Turtle is also preserved exactly; its alternative serializations have a graph-isomorphism receipt. Citation metadata here is the historical tagged copy; the authoritative release designation is '+link(TAG,REPO+'/releases/tag/'+TAG)+'.</p><ul>'+''.join('<li>'+link(n,n)+'</li>' for _,n in downloads)+'<li>'+link('SHA-256 checksums','SHA256SUMS.txt')+'</li></ul><h2>OWL serializations</h2><ul>'+''.join('<li>'+link(label,'../widoco/'+name)+'</li>' for label,name in [('Turtle','ontology.ttl'),('RDF/XML','ontology.owl'),('JSON-LD','ontology.jsonld'),('N-Triples','ontology.nt'),('Serialization receipt','serialization-receipt.json')])+'</ul><h2>Release evidence package</h2><p>'+link('Open the published release assets',REPO+'/releases/tag/'+TAG)+' for the original source archive, 149-file source inventory, final-freeze evidence and checksums. Website download checksums cover this website subset, not the entire release.</p><p>Scientific artifacts use CC BY 4.0; original software uses MIT. Dependencies and third-party template resources retain their own notices. See '+link('rights','RIGHTS.md')+' and '+link('current template notices','../../../THIRD-PARTY-DOCUMENTATION.txt')+'.</p>'
    page(Path('downloads/index.html'),'Downloads',body)
    write(version/'publication-manifest.json',json_text({'schema_version':1,'release':TAG,'semantic_source_commit':COMMIT,'model_version':model['version'],'semantic_inputs_sha256':inputs,'guide_sources_sha256':guide_inputs,'documentation_note':'Post-release documentation projection of immutable semantic inputs; not an additional semantic validation run.','counts':{'catalog_concepts':len(model['concepts']),'owl_named_classes':len(classes),'owl_object_properties':len(properties),'owl_triples':len(graph)},'template':'OntoSPK-style documentation portal with WIDOCO 1.4.25; bounded asserted hypertext explorer'}))
    # Stable entry points; version routes are explicit and self-contained.
    def redirect(path,target,title):
        write(out/path,'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url='+target+'"><title>'+title+'</title></head><body><p>'+link(title,target)+'</p></body></html>\n')
    redirect(Path('index.html'),PREFIX.as_posix()+'/index.html','Open Riskium documentation')
    redirect(Path('site/index.html'),'../'+PREFIX.as_posix()+'/reference/native/index.html','Open the Riskium conceptual reference')
    previews = [('Overview', 'index.html'), ('Conceptual reference', 'reference/native/index.html'), ('OWL reference', 'widoco/index-en.html'), ('Explorer', 'explore/index.html')]
    review = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Riskium responsive interface review</title><style>body{font:16px/1.6 system-ui;margin:24px;color:#172b3a}section{margin:30px 0}.frames{display:flex;flex-wrap:wrap;gap:24px}iframe{border:1px solid #526574;height:620px;max-width:100%}a{color:#135a7a}</style></head><body><h1>Responsive interface review</h1><p>Maintainer review surface: the same versioned documents are rendered in real 390-pixel and 760-pixel frame viewports. Each frame has its own scroll area and keyboard focus. These checks concern reading and navigation, not ontology validation.</p><p><a href="'+PREFIX.as_posix()+'/index.html">Open the documentation</a></p>'
    for title, route in previews:
        review += '<section><h2>'+title+'</h2><div class="frames">'+''.join('<div><h3>'+str(width)+' pixels</h3><iframe width="'+str(width)+'" title="'+title+' at '+str(width)+' pixels" src="'+PREFIX.as_posix()+'/'+route+'"></iframe></div>' for width in [390,760])+'</div></section>'
    write(out/'interface-review.html',review+'</body></html>\n')
    write(out/'.nojekyll','')
    return {'release':TAG,'source_commit':COMMIT,'counts':{'conceptual_entries':305,'explorer_terms':len(explorer_rows),'owl_triples':len(graph)}}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true');args=ap.parse_args()
    if args.check:
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp);result=build(out);changed=[]
            for p in out.rglob('*'):
                if p.is_file():
                    existing=ROOT/'docs'/p.relative_to(out)
                    if not existing.exists() or existing.read_bytes()!=p.read_bytes():changed.append(p.relative_to(out).as_posix())
            if changed:raise SystemExit('Stale portal files: '+', '.join(changed))
    else:result=build(ROOT/'docs')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
