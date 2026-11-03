"""Reader 0.4.6: source-bound concept dictionary over exact historical reader 0.4.5."""
import argparse,hashlib,html,json,os,re,subprocess,sys,tempfile
from pathlib import Path
from urllib.parse import urlsplit,unquote
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
import markdown
from bs4 import BeautifulSoup
import released_nature_documentation as prior
from presentation import render
from site_registry import file_map
from audit_versioned_site import audit
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import build_concept_dictionary as dictionary
VERSION='0.4.6'; BASELINE='50f731aa5e065233c81fceeadaab8d87f5569de6'
# The published dictionary owns its content source independently of later audit-tool fixes.
DICTIONARY_SOURCE='20b2983352d2a6491600fcdbd765259d3da456c2'
REPO=prior.REPO;SITE=prior.SITE
sha=lambda b:hashlib.sha256(b).hexdigest()
encode=lambda d:json.dumps(d,indent=2,ensure_ascii=False)+'\n'
def route(n):return 'index.html' if n=='README.md' else 'subdomains.html' if n=='Subdomains.md' else n[:-3]+'.html'
def link(url,source,wiki=False):
    p=urlsplit(url)
    if not url or p.scheme or url.startswith('//'):return url
    frag=re.sub(r'^(d\d\d)--',r'\1-',p.fragment)
    if not p.path:return '#'+frag
    if p.path.endswith('.md') and '/' not in p.path:
        n=p.path;dest=('Concept-Index' if n=='README.md' else 'Subdomains' if n=='Subdomains.md' else n[:-3]) if wiki else route(n)
        return dest+('#'+frag if frag else '')
    f=(ROOT/'documentation/concepts/0.3.1'/unquote(p.path)).resolve()
    if not f.is_relative_to(ROOT) or not f.is_file():raise ValueError('Unresolved concept source: '+url)
    return REPO+'/blob/'+source+'/'+f.relative_to(ROOT).as_posix()+('#'+frag if frag else '')
def project(text,source,wiki=False):
    if wiki:return re.sub(r'(!?\[[^\]\n]*\])\(([^\s)]+)\)',lambda m:m[1]+'('+link(m[2],source,True)+')',text)
    s=BeautifulSoup(markdown.markdown(text,extensions=['tables','fenced_code','toc']),'html.parser')
    for a in s.select('a[href]'):a['href']=link(a['href'],source)
    return str(s)
def upgrade(path,out):
    s=BeautifulSoup(path.read_text(),'html.parser')
    def dest(target):return os.path.relpath(target,path.relative_to(out).parent).replace(os.sep,'/')
    c=s.select_one('div.publication-context')
    if c:
        c.clear();c.append(BeautifulSoup('Reader <strong>0.4.6</strong> · model <strong>0.3.1</strong> · <a href="'+REPO+'/releases/tag/v0.3.7">Published source v0.3.7</a> · <a href="'+REPO+'/wiki">Wiki</a>','html.parser'))
    for sidebar in s.select('aside.sidebar, details.mobile-navigation > div'):
        group=BeautifulSoup('<h2>Concept dictionary</h2><ul><li><a href="'+dest('current/concepts/index.html')+'">All 80 concepts</a></li><li><a href="'+dest('current/concepts/subdomains.html')+'">Subdomains and relationships</a></li></ul>','html.parser')
        for n in reversed(list(group.contents)):sidebar.insert(0,n)
    nav=s.select_one('nav.primary-nav')
    if nav:nav.append(BeautifulSoup('<a href="'+dest('current/concepts/index.html')+'">Concept dictionary</a>','html.parser'))
    s.head.append(s.new_tag('link',rel='stylesheet',href=dest('current/assets/dictionary.css')))
    if path.relative_to(out).as_posix() in ['current/index.html','current/guide/Home.html']:
        m=s.select_one('main');h=m.find('h1');n=BeautifulSoup('<p><a href="'+dest('current/concepts/index.html')+'">Browse all concepts</a> · <a href="'+dest('current/concepts/subdomains.html')+'">Subdomains and map</a> · <a href="'+REPO+'">Repository</a> · <a href="'+REPO+'/wiki">Wiki</a></p>','html.parser');h.insert_after(n) if h else m.insert(0,n)
    for th in s.select('th'):th['scope']='col'
    for t in s.select('main table'):t['tabindex']='0'
    path.write_text(str(s)+'\n')
def build(out,wikiout):
    source=DICTIONARY_SOURCE
    subprocess.run(['git','diff','--exit-code',source,'--','ontology/riskium-model.json','documentation/concepts/0.3.1','tools/build_concept_dictionary.py','diagrams/subdomain-relationships.svg','diagrams/subdomain-relationships-matrix.svg'],cwd=ROOT,check=True,capture_output=True)
    with tempfile.TemporaryDirectory() as tmp:
        old=Path(tmp)/'reviewed';subprocess.run(['git','worktree','add','--detach',str(old),BASELINE],cwd=ROOT,check=True,capture_output=True)
        try:manifest,wiki,_=prior.build(out,root=old)
        finally:subprocess.run(['git','worktree','remove','--force',str(old)],cwd=ROOT,check=True,capture_output=True)
    original=file_map(out);files=dictionary.build();model=json.loads((ROOT/'ontology/riskium-model.json').read_text());(out/'current/concepts').mkdir(parents=True,exist_ok=True)
    for name,text in files.items():
        if not name.endswith('.md'):continue
        if name=='Subdomains.md':
            for d in model['domains']:text+='\n## '+d['id']+' '+d['title']+'\n\n'+d['objective']+'\n'
        page='current/concepts/'+route(name);body=project(text,source)
        if name=='Subdomains.md':body='<p><img class="subdomain-map" src="../assets/subdomain-relationships.svg" alt="Eleven subdomains and 23 association pairs; inheritance excluded"></p><p><a href="../assets/subdomain-relationships.svg">Package SVG</a> · <a href="../assets/subdomain-relationships-matrix.svg">Exact association matrix SVG</a></p>'+body
        slug='Concept-Index' if name=='README.md' else name[:-3]
        body+='<p>Reader 0.4.6 · <a href="'+REPO+'/blob/'+source+'/documentation/concepts/0.3.1/'+name+'">Source dossier</a> · <a href="'+REPO+'/wiki/'+slug+'">Equivalent Wiki page</a>.</p>'
        (out/page).write_text(render(Path(page),'Concept dictionary' if name=='README.md' else name[:-3],body))
        wiki[slug+'.md']=project(text,source,True)+(('\n\n## Relationship map\n\n![Subdomain association map]('+SITE+'/current/assets/subdomain-relationships.svg)\n') if name=='Subdomains.md' else '')+'\n\n[Equivalent Pages page]('+SITE+'/'+page+') · [Repository]('+REPO+') · [Wiki Home](Home)\n'
    for name in ['subdomain-relationships.svg','subdomain-relationships-matrix.svg']:(out/'current/assets'/name).write_bytes((ROOT/'diagrams'/name).read_bytes())
    (out/'current/assets/dictionary.css').write_text('.subdomain-map{display:block;width:100%;height:auto;max-width:1100px;margin:1rem auto}main table{display:block;overflow-x:auto;max-width:100%}main td,main th{vertical-align:top}nav.primary-nav{flex-wrap:wrap}\n')
    for p in sorted((out/'current').rglob('*.html')):upgrade(p,out)
    p=out/'versions/index.html';upgrade(p,out);s=BeautifulSoup(p.read_text(),'html.parser');s.select_one('main').insert(0,BeautifulSoup('<p>Maintained reader <strong>0.4.6</strong> adds concept pages over preserved 0.4.5 guide content. Source remains v0.3.7; model/OWL remain 0.3.1.</p>','html.parser'));p.write_text(str(s)+'\n')
    wiki['Home.md']='## Concept dictionary\n\n[All 80 concepts](Concept-Index) · [Subdomains and relationships](Subdomains) · [Pages]('+SITE+'/current/index.html) · [Repository]('+REPO+')\n\nReader **0.4.6** adds model-derived concepts; original guide content remains **0.4.5**. Published source remains **v0.3.7**, model **0.3.1**.\n\n'+wiki['Home.md']
    wiki['_Sidebar.md']='### Concept dictionary\n\n- [All concepts](Concept-Index)\n- [Subdomains and relationships](Subdomains)\n- [Pages]('+SITE+'/current/index.html)\n- [Repository]('+REPO+')\n\n'+wiki['_Sidebar.md']
    wiki['_Footer.md']='Reader **0.4.6** · [Repository]('+REPO+') · [Pages]('+SITE+'/current/index.html) · [Concept index](Concept-Index) · [Source v0.3.7]('+REPO+'/releases/tag/v0.3.7)\n'
    for name in wiki:
        if name not in ['Home.md','_Footer.md','_Sidebar.md','Concept-Index.md','Subdomains.md'] and not name.startswith('RKM-'):wiki[name]+='\n[Concept dictionary](Concept-Index) · [Reader 0.4.6]('+SITE+'/current/index.html)\n'
    wikiout.mkdir(parents=True,exist_ok=True)
    for name,text in wiki.items():(wikiout/name).write_text(text)
    status=json.loads((out/'current/published-status.json').read_text());status.update(documentation_version=VERSION,documentation_source_commit=source,native_wiki_files=len(wiki),wiki_files_sha256={n:sha(t.encode()) for n,t in wiki.items()},concept_dictionary=json.loads(files['manifest.json']),guide_content_version='0.4.5');(out/'current/published-status.json').write_text(encode(status))
    current=json.loads((out/'current/publication-manifest.json').read_text());current.update(documentation_version=VERSION,guide_content_version='0.4.5',documentation_note='Reader 0.4.6 concept dictionary; exact historical guide content preserved.',documentation_source_commit=source);(out/'current/publication-manifest.json').write_text(encode(current))
    manifest.update(current_source_commit=source,documentation_version=VERSION);manifest['files_sha256']={n:sha(b) for n,b in file_map(out).items() if n!='publication-manifest.json'};(out/'publication-manifest.json').write_text(encode(manifest))
    for n,data in original.items():
        if n.startswith('releases/') and (out/n).read_bytes()!=data:raise ValueError('Changed frozen snapshot: '+n)
    result=audit(out);result.update(documentation_version=VERSION,concept_pages=80,wiki_files=len(wiki),model_sha256=sha((ROOT/'ontology/riskium-model.json').read_bytes()))
    (out/'dictionary-validation.json').write_text(encode(result));manifest['files_sha256']['dictionary-validation.json']=sha((out/'dictionary-validation.json').read_bytes());(out/'publication-manifest.json').write_text(encode(manifest));audit(out);return result

def verify_live(site,wikidir,receipt):
    expected=file_map(site);status=json.loads((site/'current/published-status.json').read_text())
    def read(n):
        with urlopen(Request(SITE+'/'+n,headers={'User-Agent':'Riskium-channel-verifier','Cache-Control':'no-cache'}),timeout=40) as f:data=f.read()
        if sha(data)!=sha(expected[n]):raise ValueError('Served byte mismatch: '+n)
        return n
    # GitHub Pages consumes this zero-byte build marker but does not serve it.
    public_paths=[n for n in expected if n!='.nojekyll']
    with ThreadPoolExecutor(max_workers=8) as pool:checked=list(pool.map(read,public_paths))
    for n,digest in status['wiki_files_sha256'].items():
        if sha((wikidir/n).read_bytes())!=digest:raise ValueError('Native Wiki mismatch: '+n)
    result=dict(status='LIVE_DICTIONARY_CHANNELS_PASS',documentation_version=VERSION,served_files=len(checked),build_markers_not_http_resources=['.nojekyll'],native_wiki_files=len(status['wiki_files_sha256']),concept_pages=80,all_served_bytes_match=True,local_link_audit=audit(site));receipt.write_text(encode(result));return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--wiki-output',type=Path,default=Path('build/wiki'));p.add_argument('--verify-wiki',type=Path);p.add_argument('--receipt',type=Path);a=p.parse_args();print(encode(verify_live(a.output,a.verify_wiki,a.receipt) if a.verify_wiki else build(a.output,a.wiki_output)))
