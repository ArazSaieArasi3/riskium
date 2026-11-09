"""Stage namespace-separated HTML/Wiki candidate outputs; never deploy them."""
from pathlib import Path
import argparse,hashlib,html,importlib.util,json,os,re,sys
from urllib.parse import urlsplit,unquote
import markdown
from bs4 import BeautifulSoup
REPO='https://github.com/ArazSaieArasi3/riskium'
PREFIX='Issue93-Candidate-'
CSS='body{font-family:Arial,sans-serif;color:#203847;max-width:1180px;margin:auto;padding:24px;line-height:1.55}header{padding:16px;background:#eef3f6;border:1px solid #cad5df}nav{display:flex;gap:14px;flex-wrap:wrap;margin:16px 0}a{color:#155878}table{border-collapse:collapse;display:block;overflow-x:auto;max-width:100%;margin:18px 0}td,th{border:1px solid #aebdc7;padding:7px;vertical-align:top}th{background:#eef2f5}code{overflow-wrap:anywhere}footer{border-top:1px solid #cad5df;margin-top:32px;padding-top:16px}img{max-width:100%;height:auto}'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(x):return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def route(name):return 'index.html' if name=='README.md' else name[:-3]+'.html'
def slug(name):return PREFIX+('Home' if name=='README.md' else name[:-3])

def build(root,out,commit):
 root=Path(root).resolve();out=Path(out).resolve()
 p=root/'evaluation/manuscript-review/v7.2.3/issue93-dictionary';reader=p/'reader'
 sys.path.insert(0,str(p));import build_dictionary,audit_dictionary
 model,_=build_dictionary.export.validate_contract(json.loads(build_dictionary.export.CONTRACT.read_text()))
 files=build_dictionary.write(check=True);audit_dictionary.audit(files,model)
 web=out/'site/candidate/issue93/0.3.2-structural.2';wiki=out/'wiki';web.mkdir(parents=True,exist_ok=True);wiki.mkdir(parents=True,exist_ok=True)
 def resolve(url,name,for_wiki=False):
  parsed=urlsplit(url)
  if parsed.scheme or url.startswith('//'):return url
  if not parsed.path:return url
  target=(reader/parsed.path).resolve();frag=('#'+parsed.fragment) if parsed.fragment else ''
  if not target.is_relative_to(root):raise ValueError('Projection source link escapes repository')
  if target.parent==reader and target.name in files:
   if target.suffix=='.md':return (slug(target.name) if for_wiki else route(target.name))+frag
   if not for_wiki:return target.name+frag
  return REPO+'/blob/'+commit+'/'+target.relative_to(root).as_posix()+frag
 for name,text in files.items():
  if not name.endswith('.md'):
   (web/name).write_text(text);continue
  rendered=BeautifulSoup(markdown.markdown(text,extensions=['tables','fenced_code','toc']),'html.parser')
  for tag in rendered.find_all('a',href=True):tag['href']=resolve(tag['href'],name)
  for tag in rendered.find_all('img',src=True):tag['src']=resolve(tag['src'],name)
  for th in rendered.find_all('th'):th['scope']='col'
  title=rendered.h1.get_text(' ',strip=True) if rendered.h1 else name
  body='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>'+CSS+'</style></head><body><header><strong>Riskium candidate 0.3.2-structural.2</strong><p>Staged projection; not the published default ontology or reader.</p></header><nav><a href="index.html">Candidate index</a><a href="Subdomains.html">Subdomains</a><a href="Relations.html">Relations</a><a href="Constraints.html">Constraints</a><a href="'+REPO+'">Repository</a></nav><main>'+str(rendered)+'</main><footer><a href="'+REPO+'/blob/'+commit+'/'+(reader/name).relative_to(root).as_posix()+'">Source candidate dossier</a> · <a href="'+REPO+'/wiki">Published baseline Wiki</a> · <a href="https://arazsaiearasi3.github.io/riskium/current/index.html">Published baseline Pages</a><p>Source-bound local projection. No live publication or independent semantic acceptance is implied.</p></footer></body></html>\n'
  (web/route(name)).write_text(body)
  wiki_text=re.sub(r'\]\(([^)]+)\)',lambda m:']('+resolve(m.group(1),name,True)+')',text)
  wiki_text+='\n\n[Candidate index]('+slug('README.md')+') · [Repository]('+REPO+') · [Published baseline Wiki]('+REPO+'/wiki)\n\nStaged candidate Wiki projection; not uploaded to the live Wiki.\n'
  (wiki/(slug(name)+'.md')).write_text(wiki_text)
 manifest={'schema':'riskium-issue93-staged-publication-1','source_commit':commit,'source_model_sha256':json.loads(files['manifest.json'])['source_model_sha256'],
  'reader_manifest_sha256':sha(reader/'manifest.json'),'catalog_concepts':82,'anchor_dossiers':1,
  'html_pages':sum(n.endswith('.md') for n in files),'wiki_pages':sum(n.endswith('.md') for n in files),
  'route_map':{n:{'html':route(n),'wiki':slug(n)} for n in files if n.endswith('.md')},
  'deployed':False,'files_sha256':{x.relative_to(out).as_posix():sha(x) for x in sorted(out.rglob('*')) if x.is_file() and x.name!='publication-manifest.json'}}
 (out/'publication-manifest.json').write_text(dump(manifest));audit(out);return manifest

def audit(out):
 out=Path(out).resolve();manifest=json.loads((out/'publication-manifest.json').read_text());links=0
 for name,h in manifest['files_sha256'].items():
  p=out/name
  if sha(p)!=h:raise ValueError('Staged publication hash mismatch: '+name)
  if p.suffix=='.html':
   doc=BeautifulSoup(p.read_text(),'html.parser')
   if doc.html.get('lang')!='en' or not doc.select_one('meta[name=viewport]'):raise ValueError('Missing HTML language/viewport')
   for a in doc.select('[href],img[src]'):
    url=a.get('href',a.get('src'));parsed=urlsplit(url)
    if parsed.scheme or url.startswith('//'):continue
    target=(p.parent/unquote(parsed.path)).resolve() if parsed.path else p
    if not target.is_relative_to(out) or not target.is_file():raise ValueError('Broken staged HTML link: '+url)
    if parsed.fragment:
     other=BeautifulSoup(target.read_text(),'html.parser')
     if not other.find(id=parsed.fragment):raise ValueError('Missing staged HTML anchor: '+url)
    links+=1
  if name.startswith('wiki/'):
   for url in re.findall(r'\]\(([^)]+)\)',p.read_text()):
    parsed=urlsplit(url)
    if parsed.scheme or url.startswith(('#','//')):continue
    if not (p.parent/(parsed.path+'.md')).is_file():raise ValueError('Broken staged Wiki route: '+url)
    links+=1
 return {'html_pages':manifest['html_pages'],'wiki_pages':manifest['wiki_pages'],'local_link_occurrences':links,'deployed':False}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--commit',required=True);a=ap.parse_args();m=build(a.root,a.output,a.commit);print(dump({'html_pages':m['html_pages'],'wiki_pages':m['wiki_pages'],'audit':audit(a.output)}))
