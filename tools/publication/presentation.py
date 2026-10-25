"""Shared reader-facing presentation; semantic/reference sources stay separate."""
from pathlib import Path
import hashlib
import html
import os
from bs4 import BeautifulSoup
try:
    from .guides import entries
except ImportError:
    from guides import entries

HERE = Path(__file__).resolve().parent
REPO = 'https://github.com/ArazSaieArasi3/riskium'
SOURCE = '8afe169968b5c1396c02834dbc499af691b894b4'
GROUPS = {
    'Understand': ['Home','Scope','Overview','Decisions','Using-the-Model'],
    'Inspect and evaluate': ['Requirements','Competency-Questions','Formalization','Evaluation','Quality','Traceability','Database-Assurance','Reproduce'],
    'Sources and publication': ['Visualization','References','Citation','Limitations','Artifact-Versions','Publication','Publication-Comparison','Work-Plan'],
}

def graph_route():
    token = hashlib.sha256(b''.join((HERE/'webvowl'/p).read_bytes() for p in ['index.html','viewer.js','viewer.css'])).hexdigest()[:12]
    return 'webvowl/index.html?v='+token


def render(path, title, body, *, head='', scripts='', wide=False, section=None):
    path = Path(path)
    def url(target):
        return os.path.relpath(target.split('?')[0], path.parent).replace(os.sep,'/') + ('?'+target.split('?',1)[1] if '?' in target else '')
    def a(label,target,current=False):
        return '<a '+('aria-current="page" ' if current else '')+'href="'+html.escape(url(target),quote=True)+'">'+html.escape(label)+'</a>'
    sections=[('Overview','index.html'),('Conceptual reference','reference/native/index.html'),('OWL reference','widoco/index-en.html'),('Evaluation','guide/Evaluation.html'),('Explore','explore/index.html'),('WebVOWL',graph_route()),('Downloads','downloads/index.html')]
    nav=''.join(a(n,'current/'+p,str(path)=='current/'+p.split('?')[0]) for n,p in sections)
    rows={r['slug']:r for r in entries()}
    sidebar=''
    for name,slugs in GROUPS.items():
        sidebar+='<h2>'+name+'</h2><ul>'+''.join('<li>'+a(rows[s]['title'],'current/guide/'+s+'.html',str(path)=='current/guide/'+s+'.html')+'</li>' for s in slugs)+'</ul>'
    sidebar+='<h2>Reference tools</h2><ul>'+''.join('<li>'+a(n,'current/'+p)+'</li>' for n,p in [('Find a term','reference/search.html'),('Diagrams','reference/diagrams/index.html'),('Source record','publication-manifest.json')])+'<li>'+a('Documentation versions','versions/index.html')+'</li><li><a href="'+REPO+'/wiki">GitHub Wiki</a></li></ul>'
    soup=BeautifulSoup(body,'html.parser')
    toc=[]
    for i,h in enumerate(soup.find_all('h2'),1):
        if not h.get('id'):h['id']='section-'+str(i)
        label=h.get_text(' ',strip=True).split(' back to')[0]
        toc.append('<li><a href="#'+html.escape(h['id'])+'">'+html.escape(label)+'</a></li>')
    onpage='<h2>On this page</h2><ul>'+''.join(toc)+'</ul>'
    mobile='<details class="mobile-navigation"><summary>Documentation and page contents</summary><div>'+sidebar+onpage+'</div></details>'
    breadcrumb='<nav class="breadcrumbs" aria-label="Breadcrumb">'+a('Riskium','current/index.html')+'<span aria-hidden="true">/</span><span>'+html.escape(section or title)+'</span></nav>'
    footer='<footer class="site-footer"><div><strong>Riskium</strong><p>An ontology for modeling enterprise risk knowledge.</p></div><div>'+a('Citation and authors','current/guide/Citation.html')+' · '+a('Scope and limitations','current/guide/Limitations.html')+' · <a href="'+REPO+'">Repository</a><p>Scientific content: CC BY 4.0 · Original software: MIT. Araz Saie Arasi, Hassan Haghighi and Hossein Azgomi, for their respective contributions.</p></div></footer>'
    description='Riskium enterprise risk ontology: conceptual definitions, bounded OWL reference, evaluation and reproducible sources.'
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="'+description+'"><title>'+html.escape(title)+' — Riskium</title>'+head+'<link rel="stylesheet" href="'+url('current/assets/portal.css')+'?v='+hashlib.sha256((HERE/'portal.css').read_bytes()).hexdigest()[:12]+'"></head><body class="'+('wide-page' if wide else 'reading-page')+'" data-template="riskium-pages-1"><a class="skip-link" href="#content">Skip to content</a><header class="site-header"><div class="brand-row">'+a('Riskium','current/index.html')+'<p>Enterprise risk knowledge</p><div class="header-tools">'+a('Find a term','current/reference/search.html')+a('Versions','versions/index.html')+'</div></div><nav class="primary-nav" aria-label="Primary">'+nav+'</nav></header><div class="publication-context"><span>Current documentation · Model <strong>0.3.1</strong></span><span>Source distribution <a href="'+REPO+'/releases/tag/v0.3.2">v0.3.2</a> · '+a('Version policy','current/guide/Publication.html')+'</span></div>'+mobile+'<div class="layout"><aside class="sidebar" aria-label="Documentation navigation">'+sidebar+'</aside><main id="content" tabindex="-1">'+breadcrumb+str(soup)+'</main><aside class="toc" aria-label="On this page">'+onpage+'</aside></div>'+footer+scripts+'</body></html>\n'
