"""Publish qualified v0.3.9 bodies without changing the frozen scientific inputs.

The delivery adapter changes publication labels and routes only. Historical
release snapshots retain their bytes; old visualizations retain model 0.3.1.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

import markdown
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
REPO = 'https://github.com/ArazSaieArasi3/riskium'
SITE = 'https://arazsaiearasi3.github.io/riskium'
SOURCE = 'ce0baefa3495d1bc3b42f56ad578154d5bc4f178'
READER = ROOT / 'documentation/0.4.9/reader'
PUBLICATION = ROOT / 'evaluation/releases/v0.3.9/publication.json'
MODEL_SHA = '060357495ee9c35d11e58ff9cf82bb7e64d88f1aa135a70c50966b44522226cb'
sha = lambda b: hashlib.sha256(b).hexdigest()
encode = lambda v: json.dumps(v, indent=2, ensure_ascii=False) + '\n'

CSS = '''
:root{color-scheme:light;--ink:#192f43;--muted:#41576b;--line:#c8d6df;--accent:#135e79}
*{box-sizing:border-box}body{margin:0;font:16px/1.62 system-ui,sans-serif;color:var(--ink);background:#fafcfd}
a{color:var(--accent);text-underline-offset:.16em}a:hover{color:#8b4500}a:focus-visible{outline:3px solid #d08229;outline-offset:3px}
header{background:#153e56;color:white;padding:1.15rem max(1.5rem,calc((100vw - 1450px)/2))}header a{color:#d3f1ff}
header p{margin:.3rem 0}header strong{font-size:1.4rem}.layout{max-width:1450px;margin:auto;display:grid;grid-template-columns:245px minmax(0,1fr);gap:2.5rem;padding:1.5rem}
aside{border-right:1px solid var(--line);padding-right:1.2rem}aside h2{font-size:1rem;margin:1rem 0 .25rem}aside ul{list-style:none;padding:0;margin:0}aside li{margin:.3rem 0}
main{min-width:0;max-width:1080px}h1{font-size:2rem;line-height:1.25}h2{margin-top:2rem;font-size:1.4rem}h3{font-size:1.13rem}p{max-width:95ch}
table{border-collapse:collapse;width:100%;font-size:.92rem;margin:1rem 0;display:block;overflow:auto}th,td{border:1px solid var(--line);padding:.5rem .6rem;vertical-align:top}th{background:#e8f1f5;text-align:left}
pre{overflow:auto;padding:1rem;background:#edf2f5}code{overflow-wrap:anywhere;font-size:.9em}img{max-width:100%;height:auto}footer{padding:1.5rem;border-top:1px solid var(--line);font-size:.9rem;background:#edf3f6}
.notice{padding:.8rem 1rem;border-left:4px solid #b36a17;background:#fff4df}.roles{font-size:.94rem;color:var(--muted)}details.mobile{display:none}
@media(max-width:850px){.layout{display:block;padding:1rem}.layout>aside{display:none}details.mobile{display:block;background:#eaf2f6;padding:.6rem 1rem}h1{font-size:1.65rem}header{padding:1rem}}
'''

NAV = [('Start here', [('Home','Overview'), ('Scope','Scope and RiskCase'), ('Using-the-Model','Use and profiles')]),
       ('Model and dictionary', [('Concept-Index','All concepts'), ('Subdomains','Subdomains and matrix'), ('Relations','Associations'), ('Generalizations','Inheritance'), ('Constraints','Constraints'), ('Set-policy','Generalization sets'), ('Visualization','Views and source files')]),
       ('Quality and reproduction', [('Requirements','Requirements'), ('Competency-Questions','Competency questions'), ('Quality','Quality and limits'), ('Reproduce','Reproduce'), ('Database-Assurance','Database boundary'), ('Traceability','Traceability')]),
       ('Publication', [('Publication','Release and downloads'), ('Artifact-Versions','Version roles'), ('External-Definitions','Earlier source comparisons'), ('Citation','Citation and rights'), ('Work-Plan','Open research')])]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def roles():
    return 'Package v0.3.9 · scientific model 0.3.2 · task profile 0.1.0 · reader 0.4.9'


def page_route(slug):
    if slug == 'Concept-Index': return 'current/concepts/index.html'
    if slug in ['Subdomains','Relations','Generalizations','Constraints','Set-policy','External-Definitions'] or slug.startswith(('RKM-','EXT-')):
        return 'current/concepts/' + slug + '.html'
    return 'current/guide/' + slug + '.html'


def shell(title, body, slug, source_url):
    nav = ''.join('<h2>'+group+'</h2><ul>'+''.join('<li><a href="'+SITE+'/'+page_route(k)+'">'+label+'</a></li>' for k,label in items)+'</ul>' for group,items in NAV)
    context = '<header><strong>Riskium</strong><p>Organizing ecosystem and enterprise risk knowledge</p><p>'+roles()+'</p><p><a href="'+REPO+'">Repository</a> · <a href="'+REPO+'/wiki">Wiki</a> · <a href="'+REPO+'/releases/tag/v0.3.9">Published package</a></p></header>'
    footer = '<footer><p>'+roles()+'.</p><a href="'+source_url+'">Explanatory source</a> · <a href="'+REPO+'/wiki/'+slug+'">Equivalent Wiki page</a> · <a href="'+SITE+'/current/index.html">Pages Home</a> · <a href="'+REPO+'">Repository</a><p>The article 7.2.21 and historical SQL/corpus receipts retain their original source bindings. The package is not a claim of independent semantic acceptance or production deployment.</p></footer>'
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+' | Riskium</title><style>'+CSS+'</style></head><body>'+context+'<details class="mobile"><summary>Navigation</summary>'+nav+'</details><div class="layout"><aside aria-label="Reader navigation">'+nav+'</aside><main>'+body+'</main></div>'+footer+'</body></html>\n'


def published_text(text):
    return text.replace('Selected scientific source **0.3.2** for package **v0.3.9**; publication has not yet occurred.',
                        'Published scientific source **0.3.2** in package **v0.3.9**; reader **0.4.9**.').replace('# Riskium selected concept dictionary', '# Riskium concept dictionary').replace('Candidate subdomain matrix', 'Subdomain matrix')


def build(out, wikiout):
    out, wikiout = Path(out).resolve(), Path(wikiout).resolve()
    require(not out.exists() and not wikiout.exists(), 'Use empty output destinations')
    p = json.loads(PUBLICATION.read_text())
    require(p['status']=='INDEPENDENT_PUBLIC_DOWNLOADS_PASS' and p['source_commit']==SOURCE and p['release_id']==440107328 and len(p['assets'])==6 and p['previous_releases_unchanged'], 'Publication record is not verified')
    selected = json.loads((ROOT/'releases/selection-v0.3.9.json').read_text())
    for n, digest in selected['selected_files_sha256'].items():
        require(sha((ROOT/n).read_bytes())==digest, 'Selected source drift: '+n)
    require(sha((ROOT/'ontology/0.3.2/riskium-model.json').read_bytes())==MODEL_SHA, 'Wrong current model')
    delivery_commit = subprocess.check_output(['git','log','-1','--format=%H','--','tools/releases/v039/delivery',str(PUBLICATION.relative_to(ROOT))],cwd=ROOT,text=True).strip()
    if not delivery_commit: delivery_commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    # Tracked frozen snapshots and historical tool resources retain their exact bytes.
    shutil.copytree(ROOT/'docs', out)
    wikiout.mkdir(parents=True)
    frozen_before = {x.relative_to(out).as_posix():sha(x.read_bytes()) for x in (out/'releases').rglob('*') if x.is_file()}
    changed = []
    # Keep legacy guide anchors available when their canonical routes advance.
    history=out/'history/model-0.3.1'
    shutil.copytree(out/'current',history)
    for f in list((out/'current').rglob('*.html'))+list(history.rglob('*.html')):
        s = BeautifulSoup(f.read_text(), 'html.parser')
        original=out/'current'/f.relative_to(history) if f.is_relative_to(history) else f
        for node in s.select('[href],img[src],script[src]'):
            key='href' if node.has_attr('href') else 'src';url=node[key];parts=urlsplit(url)
            if url.startswith(SITE+'/current/'):
                node[key]=url.replace(SITE+'/current/',SITE+'/history/model-0.3.1/',1)
            elif not parts.scheme and not url.startswith(('#','//')):
                target=(original.parent/unquote(parts.path)).resolve()
                require(target.is_relative_to(out),'Historical route escapes site: '+url)
                dest=target.relative_to(out).as_posix()
                if dest.startswith('current/'):dest='history/model-0.3.1/'+dest[len('current/'):]
                node[key]=SITE+'/'+dest+('?'+parts.query if parts.query else '')+('#'+parts.fragment if parts.fragment else '')
        if s.body:
            notice = BeautifulSoup('<div class="notice" style="padding:18px;border:3px solid #b36a17;background:#fff4df"><strong>Historical model 0.3.1 view.</strong> This retained visualization/reference is not regenerated for model 0.3.2. <a href="'+SITE+'/current/concepts/index.html">Open the current 0.3.2 dictionary</a> and <a href="'+SITE+'/current/guide/Visualization.html">current source files</a>.</div>', 'html.parser')
            s.body.insert(0, notice)
            f.write_text(str(s)+'\n')
    wiki = {}
    def emit(slug, text, source_path, is_reader=False):
        route = page_route(slug)
        source_url = REPO+'/blob/'+(SOURCE if is_reader else delivery_commit)+'/'+source_path
        def resolve(url, for_wiki=False):
            parsed = urlsplit(url)
            if parsed.scheme or url.startswith('//') or not parsed.path: return url
            frag = '#'+parsed.fragment if parsed.fragment else ''
            if parsed.path.endswith('.md') and '/' not in parsed.path:
                dest = 'Concept-Index' if parsed.path=='README.md' else parsed.path[:-3]
                return (dest if for_wiki else SITE+'/'+page_route(dest))+frag
            base = READER if is_reader else HERE/'guides'
            target = (base/unquote(parsed.path)).resolve()
            require(target.is_relative_to(ROOT) and target.is_file(), 'Unknown source target: '+url)
            if is_reader and target.parent==READER and target.suffix!='.md' and not for_wiki:
                return SITE+'/current/concepts/'+target.name+frag
            return REPO+'/blob/'+(SOURCE if is_reader else delivery_commit)+'/'+target.relative_to(ROOT).as_posix()+frag
        text = published_text(text) if is_reader else text
        doc = BeautifulSoup(markdown.markdown(text,extensions=['tables','fenced_code','toc','md_in_html']), 'html.parser')
        for a in doc.select('a[href]'): a['href']=resolve(a['href'])
        for a in doc.select('img[src]'): a['src']=resolve(a['src'])
        for th in doc.select('th'): th['scope']='col'
        title = doc.h1.get_text(' ',strip=True) if doc.h1 else slug.replace('-',' ')
        dest = out/route;dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(shell(title,str(doc),slug,source_url))
        changed.append(route)
        wt = re.sub(r'\]\(([^)]+)\)',lambda m:']('+resolve(m[1],True)+')',text)
        wiki[slug+'.md'] = wt.rstrip()+'\n\n---\n\n'+roles()+' · [Source]('+source_url+') · [Equivalent Pages page]('+SITE+'/'+route+') · [Repository]('+REPO+') · [Wiki Home](Home)\n'
    for f in sorted(READER.iterdir()):
        if f.suffix=='.md': emit('Concept-Index' if f.name=='README.md' else f.stem,f.read_text(),f.relative_to(ROOT).as_posix(),True)
        elif f.is_file():
            d=out/'current/concepts'/f.name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,d)
    for f in sorted((HERE/'guides').glob('*.md')): emit(f.stem,f.read_text(),f.relative_to(ROOT).as_posix())
    # Documentary comparisons have their own 0.3.1 binding; they are not new 0.3.2 equivalences.
    external = ROOT/'documentation/0.4.8/concepts/External-Definitions.md'
    text = '# Earlier external-definition review\n\nThis retained documentary review concerns the eighty-concept **model 0.3.1** population. It is historical reference material, not independent acceptance or an automatically migrated equivalence for model 0.3.2. [Current dictionary](README.md) and [open curation work]('+REPO+'/issues/85).\n\n'
    text += re.sub(r'\]\(([^)]+)\)',lambda m:']('+m[1]+')' if urlsplit(m[1]).scheme or m[1].startswith('#') else ']('+REPO+'/blob/'+SOURCE+'/'+(external.parent/unquote(urlsplit(m[1]).path)).resolve().relative_to(ROOT).as_posix()+('#'+urlsplit(m[1]).fragment if urlsplit(m[1]).fragment else '')+')',external.read_text())
    emit('External-Definitions',text,external.relative_to(ROOT).as_posix(),True)
    (out/'current/index.html').write_text((out/'current/guide/Home.html').read_text());changed.append('current/index.html')
    (out/'index.html').write_text((out/'current/index.html').read_text());changed.append('index.html')
    # Older links remain valid while the default concept route is source 0.3.2.
    (out/'current/concepts/subdomains.html').write_text((out/'current/concepts/Subdomains.html').read_text());changed.append('current/concepts/subdomains.html')
    for name in ['riskium-model.json','riskium.ontouml.json','riskium.owl.ttl','source-contract.json','mapping-receipt.json']:
        d=out/'current/source'/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/'ontology/0.3.2'/name,d)
    (out/'current/downloads').mkdir(exist_ok=True)
    (out/'current/downloads/index.html').write_text((out/'current/guide/Publication.html').read_text());changed.append('current/downloads/index.html')
    (out/'current/published-status.json').write_text(encode(dict(schema='riskium-current-reader-049',source_commit=SOURCE,documentation_commit=delivery_commit,source_release='v0.3.9',release_id=p['release_id'],model_version='0.3.2',documentation_version='0.4.9',task_profile_version='0.1.0',model_sha256=MODEL_SHA,manuscript_version='7.2.21',manuscript_public_assets=False,source_publication_verified=True,live_channel_readback=False,legacy_visualizations_model='0.3.1',wiki_files_sha256={n:sha(t.encode()) for n,t in wiki.items()})))
    wiki['_Sidebar.md'] = '# Riskium\n\n'+''.join('## '+group+'\n\n'+''.join('- ['+label+']('+k+')\n' for k,label in items)+'\n' for group,items in NAV)+'[Repository]('+REPO+') · [Pages]('+SITE+'/current/index.html) · [Release]('+REPO+'/releases/tag/v0.3.9)\n'
    wiki['_Footer.md'] = roles()+' · [Wiki Home](Home) · [Concept index](Concept-Index) · [Repository]('+REPO+') · [Pages]('+SITE+'/current/index.html) · [Release]('+REPO+'/releases/tag/v0.3.9)\n'
    for n,t in wiki.items(): (wikiout/n).write_text(t)
    status=json.loads((out/'current/published-status.json').read_text());status['wiki_files_sha256']={n:sha(t.encode()) for n,t in wiki.items()};(out/'current/published-status.json').write_text(encode(status))
    version=out/'releases/v0.3.9';require(not version.exists(),'Release snapshot already exists');shutil.copytree(out/'current',version)
    for f in version.rglob('*.html'):
        doc=BeautifulSoup(f.read_text(),'html.parser')
        original=out/'current'/f.relative_to(version)
        for node in doc.select('[href],img[src],script[src]'):
            key='href' if node.has_attr('href') else 'src';url=node[key];parts=urlsplit(url)
            if url.startswith(SITE+'/current/'):
                node[key]=url.replace(SITE+'/current/',SITE+'/releases/v0.3.9/',1)
            elif not parts.scheme and not url.startswith(('#','//')):
                target=(original.parent/unquote(parts.path)).resolve()
                require(target.is_relative_to(out),'Snapshot link escapes site: '+url)
                dest=target.relative_to(out).as_posix()
                if dest.startswith('current/'):dest='releases/v0.3.9/'+dest[len('current/'):]
                node[key]=SITE+'/'+dest+('?'+parts.query if parts.query else '')+('#'+parts.fragment if parts.fragment else '')
        f.write_text(str(doc)+'\n')
    vtext='# Documentation versions\n\nThe current reader **0.4.9** explains scientific model **0.3.2**, published in [v0.3.9]('+REPO+'/releases/tag/v0.3.9). The [v0.3.9 snapshot]('+SITE+'/releases/v0.3.9/index.html) preserves this view. The source package and delivery commit have distinct roles.\n\n## Preserved earlier snapshots\n\n'
    for d in sorted((out/'releases').iterdir()):
        if d.is_dir() and d.name!='v0.3.9' and (d/'index.html').exists():vtext+='- [Historical '+d.name+']('+SITE+'/releases/'+d.name+'/index.html) retains its original source and dated claims.\n'
    (out/'versions').mkdir(exist_ok=True);(out/'versions/index.html').write_text(shell('Documentation versions',markdown.markdown(vtext), 'Publication',REPO+'/tree/'+delivery_commit+'/tools/releases/v039/delivery'));changed.append('versions/index.html')
    require(all(sha((out/n).read_bytes())==h for n,h in frozen_before.items()), 'Historical frozen snapshot changed')
    (out/'.nojekyll').write_text('')
    manifest=dict(schema='riskium-coordinated-delivery-1',source_commit=SOURCE,documentation_commit=delivery_commit,model_version='0.3.2',documentation_version='0.4.9',package='v0.3.9',release_id=440107328,model_sha256=MODEL_SHA,catalog_concepts=82,external_anchors=1,wiki_files=len(wiki),historical_snapshot_files_preserved=len(frozen_before),historical_rendered_resources='Retained tracked documentation; old native/OWL visualizations explicitly marked model 0.3.1.',selected_source_bindings_checked=len(selected['selected_files_sha256']),current_html_checked=changed,files_sha256={f.relative_to(out).as_posix():sha(f.read_bytes()) for f in sorted(out.rglob('*')) if f.is_file() and f.relative_to(out).as_posix()!='publication-manifest.json'})
    (out/'publication-manifest.json').write_text(encode(manifest))
    result=audit(out,wikiout);(out/'delivery-validation.json').write_text(encode(result));manifest['files_sha256']['delivery-validation.json']=sha((out/'delivery-validation.json').read_bytes());(out/'publication-manifest.json').write_text(encode(manifest))
    return result


def audit(out,wikiout):
    out,wikiout=Path(out).resolve(),Path(wikiout).resolve();m=json.loads((out/'publication-manifest.json').read_text());count=0
    for n,h in m['files_sha256'].items():require(sha((out/n).read_bytes())==h,'Delivered body changed: '+n)
    checked=set(m['current_html_checked'])|{f.relative_to(out).as_posix() for f in (out/'releases/v0.3.9').rglob('*.html')}
    soup_cache={}
    def soup(f):
        if f not in soup_cache:soup_cache[f]=BeautifulSoup(f.read_text(),'html.parser')
        return soup_cache[f]
    for n in checked:
        f=out/n;s=soup(f)
        require(s.html and s.html.get('lang')=='en' and s.select_one('meta[name=viewport]'),'Missing language/viewport: '+n)
        for a in s.select('[href],img[src]'):
            url=a.get('href',a.get('src'));p=urlsplit(url)
            if url.startswith(SITE+'/'):target=out/unquote(p.path[len('/riskium/'):])
            elif p.scheme or url.startswith('//'):continue
            else:target=(f.parent/unquote(p.path)).resolve() if p.path else f
            require(target.is_relative_to(out) and target.is_file(),'Missing delivered route '+n+': '+url)
            if p.fragment and target.suffix=='.html':require(soup(target).find(id=unquote(p.fragment)) is not None,'Missing anchor '+n+': '+url)
            count+=1
    wikilinks=0
    for f in wikiout.glob('*.md'):
        for url in re.findall(r'\]\(([^)]+)\)',f.read_text()):
            p=urlsplit(url)
            if p.scheme or url.startswith('//'):continue
            target=wikiout/(p.path+'.md') if p.path else f
            require(target.is_file(),'Missing Wiki target: '+url)
            if p.fragment:
                doc=BeautifulSoup(markdown.markdown(target.read_text(),extensions=['tables','toc','fenced_code']),'html.parser')
                require(doc.find(id=unquote(p.fragment)) is not None,'Missing Wiki source anchor: '+url)
            wikilinks+=1
    for n in ['RKM-X01.md','RKM-C066.md','RKM-C075.md','RKM-C076.md','Set-policy.md']:
        text=(wikiout/n).read_text();require('publication has not yet occurred' not in text,'Stale publication state')
    return dict(status='COORDINATED_DELIVERY_LOCAL_PASS',source_commit=SOURCE,model_sha256=MODEL_SHA,current_and_snapshot_html_checked=len(checked),local_link_anchor_occurrences=count,wiki_link_anchor_occurrences=wikilinks,wiki_files=len(list(wikiout.glob('*.md'))),historical_snapshot_files_preserved=m['historical_snapshot_files_preserved'],selected_source_bindings_checked=m['selected_source_bindings_checked'],live_channel_readback=False)


def verify_live(site,wiki,receipt):
    site,wiki=Path(site),Path(wiki);result=audit(site,wiki);m=json.loads((site/'publication-manifest.json').read_text())
    names=list(m['files_sha256'])+['publication-manifest.json']
    def read(n):
        if n=='.nojekyll': return None
        with urlopen(Request(SITE+'/'+n,headers={'User-Agent':'Riskium-v039-readback','Cache-Control':'no-cache'}),timeout=45) as r:data=r.read()
        require(sha(data)==sha((site/n).read_bytes()),'Public Pages byte mismatch: '+n)
        return dict(path=n,sha256=sha(data),bytes=len(data))
    with ThreadPoolExecutor(max_workers=8) as pool:rows=[r for r in pool.map(read,names) if r]
    status=json.loads((site/'current/published-status.json').read_text())
    for n,h in status['wiki_files_sha256'].items():require(sha((wiki/n).read_bytes())==h,'Actual Wiki mismatch: '+n)
    result.update(status='COORDINATED_LIVE_CHANNELS_PASS',live_channel_readback=True,pages_files=len(rows),wiki_files=len(status['wiki_files_sha256']),pages=rows,wiki_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=wiki,text=True).strip(),boundary='Actual served Pages bodies and native Wiki checkout matched the source-bound delivery. Scientific correctness and operational deployment retain their scoped evidence.')
    Path(receipt).write_text(encode(result));return {k:v for k,v in result.items() if k!='pages'}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--wiki-output',type=Path,required=True);ap.add_argument('--verify-live',action='store_true');ap.add_argument('--receipt',type=Path);a=ap.parse_args()
    print(encode(verify_live(a.output,a.wiki_output,a.receipt) if a.verify_live else build(a.output,a.wiki_output)))
