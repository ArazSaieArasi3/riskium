"""Maintained 0.4.7 reader with explicit prepared versus verified publication state."""
import argparse,json,os,re,sys,subprocess
from pathlib import Path
from bs4 import BeautifulSoup
import markdown
import dictionary_documentation as base
from presentation import render
from site_registry import file_map
from audit_versioned_site import audit
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools/releases/v038'));import release
VERSION='0.4.7';PUB='evaluation/releases/v0.3.8/publication.json'
def publication_check(p):
    release.require(p['status']=='INDEPENDENT_PUBLIC_DOWNLOADS_PASS' and p['tag']=='v0.3.8' and p['latest'] and p['previous_releases_unchanged'],'Unverified publication record')
    r=release.api('releases/tags/v0.3.8');t=release.api('git/ref/tags/v0.3.8')['object']
    release.require(r['id']==p['release_id']==release.api('releases/latest')['id'] and not r['draft'] and not r['prerelease'] and t['type']=='commit' and t['sha']==p['source_commit'],'Actual release source differs')
    release.require({a['name']:a['digest'] for a in r['assets']}=={a['name']:'sha256:'+a['sha256'] for a in p['assets']} and len(r['assets'])==6,'Actual release asset identity differs')
def build(out,wikiout):
    published=(ROOT/PUB).exists();p=json.loads((ROOT/PUB).read_text()) if published else None
    if p:publication_check(p)
    source=p['source_commit'] if p else subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    base.build(out,wikiout);before=file_map(out);wiki={f.name:f.read_text() for f in wikiout.glob('*.md')}
    rows=json.loads((ROOT/'documentation/0.4.7/guide-registry.json').read_text())['guides']
    label='Published source v0.3.8' if published else 'Prepared source v0.3.8 — not published'
    context='<div class="publication-context">Reader <strong>0.4.7</strong> · model <strong>0.3.1</strong> · <a href="'+base.REPO+'/releases/tag/v0.3.8">'+label+'</a> · <a href="'+base.REPO+'/wiki">Wiki</a></div>'
    hashes={}
    for row in rows:
        raw=(ROOT/row['source']).read_text();hashes[row['source']]=base.sha(raw.encode());text=raw.replace('SOURCE_COMMIT',source)
        page='current/guide/'+row['slug']+'.html';s=BeautifulSoup(markdown.markdown(text,extensions=['tables','fenced_code','toc','md_in_html']),'html.parser')
        for a in s.select('a[href]'):a['href']=base.prior.rewrite_link(a['href'],rows,page)
        s.append(BeautifulSoup('<p>Reader 0.4.7 · <a href="'+base.REPO+'/blob/'+source+'/'+row['source']+'">Explanatory source</a> · <a href="'+base.REPO+'/wiki/'+row['wiki_slug']+'">Equivalent Wiki guide</a>.</p>','html.parser'))
        (out/page).write_text(render(Path(page),row['title'],str(s)))
        wt=re.sub(r'(!?\[[^\]\n]*\])\(([^\s)]+)\)',lambda m:m[1]+'('+base.prior.rewrite_link(m[2],rows,'',wiki=True)+')',text)
        wiki[row['wiki_slug']+'.md']=wt+'\n\nReader **0.4.7** · '+label+' · [Explanatory source]('+base.REPO+'/blob/'+source+'/'+row['source']+') · [Equivalent Pages guide]('+base.SITE+'/'+page+') · [Repository]('+base.REPO+') · [Concept index](Concept-Index)\n'
    # Home and all guide bodies are generated from the same current sources.
    (out/'current/index.html').write_text((out/'current/guide/Home.html').read_text())
    # The copied Home must keep its original relative route context.
    s=BeautifulSoup((out/'current/index.html').read_text(),'html.parser')
    for node in s.select('[href],[src]'):
        key='href' if node.get('href') else 'src';url=node.get(key,'');parts=base.urlsplit(url)
        if not url or parts.scheme or url.startswith(('#','//')):continue
        dest=(Path('current/guide')/parts.path).as_posix();node[key]=os.path.relpath(os.path.normpath(dest),'current').replace(os.sep,'/')+('?'+parts.query if parts.query else '')+('#'+parts.fragment if parts.fragment else '')
    (out/'current/index.html').write_text(str(s)+'\n')
    for path in list((out/'current').rglob('*.html'))+[out/'versions/index.html']:
        s=BeautifulSoup(path.read_text(),'html.parser');c=s.select_one('.publication-context')
        if c:c.replace_with(BeautifulSoup(context,'html.parser'))
        # The dictionary's source footer describes its own projection version.
        if '/concepts/' in path.as_posix():
            for n in s.find_all(string=lambda t:t and 'Reader 0.4.6' in t):n.replace_with(n.replace('Reader 0.4.6','Dictionary projection 0.4.6'))
        if s.select_one('main'):
            local=os.path.relpath('current/concepts/index.html',path.relative_to(out).parent).replace(os.sep,'/')
            nav=s.select_one('nav.primary-nav')
            if nav and not nav.find('a',href=local):nav.append(BeautifulSoup('<a href="'+local+'">Concept dictionary</a>','html.parser'))
            for aside in s.select('aside.sidebar,details.mobile-navigation > div'):
                if not aside.find('a',href=local):aside.insert(0,BeautifulSoup('<h2>Concept dictionary</h2><ul><li><a href="'+local+'">All 80 concepts</a></li><li><a href="'+os.path.relpath('current/concepts/subdomains.html',path.relative_to(out).parent).replace(os.sep,'/')+'">Subdomains and relationships</a></li></ul>','html.parser'))
        path.write_text(str(s)+'\n')
    vp=out/'versions/index.html';vs=BeautifulSoup(vp.read_text(),'html.parser');first=vs.select_one('main p')
    if first:first.replace_with(BeautifulSoup('<p>Maintained reader <strong>0.4.7</strong> accompanies the selected v0.3.8 package. Dictionary content retains its qualified 0.4.6 source; earlier snapshots retain their original dated claims. '+label+'.</p>','html.parser'))
    vp.write_text(str(vs)+'\n')
    for n in ['Home.md','_Sidebar.md','_Footer.md']:
        if n!='Home.md':wiki[n]=wiki[n].replace('0.4.6','0.4.7').replace('v0.3.7','v0.3.8')
    wiki['Home.md']='[Concept index](Concept-Index) · [Subdomains and relationships](Subdomains) · [Pages]('+base.SITE+'/current/index.html) · [Repository]('+base.REPO+')\n\n'+wiki['Home.md']
    for n,t in wiki.items():(wikiout/n).write_text(t)
    # Current download links are actual publication URLs only after verification.
    body='# Source downloads\n\n'+label+'\n\n'
    if p:
        body+='Download all six assets together, verify their checksums and run the extracted standard-library verifier.\n\n'+'\n'.join('- ['+a['name']+']('+a['url']+')' for a in p['assets'])+'\n\n'
    body+='[Publication and verification](../guide/Publication.html) · [Reproduction](../guide/Reproduce.html) · [Artifact versions](../guide/Artifact-Versions.html)\n\nModel/OWL remain 0.3.1. Current author-held article 7.2.3 is separate from the historical 7.0.8 component; private binaries are excluded. The existing model/license files in this directory retain their model-source roles.'
    dp=out/'current/downloads/index.html';dp.write_text(render(Path('current/downloads/index.html'),'Downloads',markdown.markdown(body)));base.upgrade(dp,out);s=BeautifulSoup(dp.read_text(),'html.parser');s.select_one('.publication-context').replace_with(BeautifulSoup(context,'html.parser'));dp.write_text(str(s)+'\n')
    (out/'current/source-release.json').write_bytes(release.encode(p or dict(status='PREPARED_NOT_PUBLISHED',tag='v0.3.8')))
    status=json.loads((out/'current/published-status.json').read_text());status.update(documentation_version=VERSION,documentation_source_commit=source,guide_source_commit=source,guide_content_version=VERSION,source_release='v0.3.8' if published else 'v0.3.7',selected_source_release='v0.3.8',published_source_commit=source if published else status['published_source_commit'],release_id=p['release_id'] if p else status['release_id'],publication_receipt_sha256=base.sha(release.encode(p)) if p else None,publication_phase='PUBLISHED' if published else 'PREPARED_NOT_PUBLISHED',guide_sources_sha256=hashes,wiki_files_sha256={n:base.sha(t.encode()) for n,t in wiki.items()},native_wiki_files=len(wiki),reader_review_plan='documentation/0.4.7/review-plan.json',dictionary_source_commit=base.DICTIONARY_SOURCE,current_author_held_manuscript='7.2.3',new_source_distribution=published)
    (out/'current/published-status.json').write_bytes(release.encode(status))
    current=json.loads((out/'current/publication-manifest.json').read_text());current.update(documentation_version=VERSION,documentation_source_commit=source,guide_content_version=VERSION,guide_sources_sha256=hashes,guide_registry_sha256=base.sha((ROOT/'documentation/0.4.7/guide-registry.json').read_bytes()),release='v0.3.8' if published else 'v0.3.7',publication_checkpoint=dict(tag='v0.3.8',source_commit=source,release_id=p['release_id']) if p else None,release_routing=dict(published=p['release_url'] if p else base.REPO+'/releases/tag/v0.3.7',latest=base.REPO+'/releases/latest',target=None if p else 'v0.3.8'),documentation_note='Reader 0.4.7; dictionary source 0.4.6; technical historical checkpoints explicitly dated.')
    (out/'current/publication-manifest.json').write_bytes(release.encode(current))
    m=json.loads((out/'publication-manifest.json').read_text());m.update(current_source_commit=source,documentation_version=VERSION,publication_status_projection={k:status[k] for k in ['source_release','published_source_commit','release_id','publication_receipt_sha256','documentation_version']},published_reader_projection=dict(source_release=status['source_release'],published_source_commit=status['published_source_commit'],documentation_source_commit=source,source_namespace='documentation/0.4.7',semantic_changes=False))
    # Replace the current audit result; frozen snapshot files remain untouched.
    (out/'dictionary-validation.json').unlink();m['files_sha256']={n:base.sha(b) for n,b in file_map(out).items() if n!='publication-manifest.json'};(out/'publication-manifest.json').write_bytes(release.encode(m));r=audit(out);r.update(documentation_version=VERSION,concept_pages=80,wiki_files=105,publication_phase=status['publication_phase']);(out/'dictionary-validation.json').write_bytes(release.encode(r));m['files_sha256']['dictionary-validation.json']=base.sha((out/'dictionary-validation.json').read_bytes());(out/'publication-manifest.json').write_bytes(release.encode(m));audit(out)
    for n,b in before.items():
        if n.startswith('releases/'):release.require((out/n).read_bytes()==b,'Frozen snapshot changed')
    release.require(len(wiki)==105,'Wiki file population changed');return r
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--wiki-output',type=Path,default=Path('build/wiki'));p.add_argument('--verify-wiki',type=Path);p.add_argument('--receipt',type=Path);a=p.parse_args()
    if a.verify_wiki:
        r=base.verify_live(a.output,a.verify_wiki,a.receipt);r['documentation_version']=VERSION;a.receipt.write_bytes(release.encode(r))
    else:r=build(a.output,a.wiki_output)
    print(json.dumps(r,indent=2))
if __name__=='__main__':main()
