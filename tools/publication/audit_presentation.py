"""Audit current reader routes; frozen presentations are assessed separately."""
from pathlib import Path
from bs4 import BeautifulSoup


def audit(docs):
    pages = sorted((docs/'current').rglob('*.html')) + [docs/'versions/index.html']
    titles=set();rows=[]
    for path in pages:
        soup=BeautifulSoup(path.read_text(),'html.parser')
        def require(ok,message):
            if not ok:raise ValueError(message+': '+str(path))
        title=soup.title.get_text() if soup.title else ''
        require(title and title not in titles,'Missing or duplicate page title');titles.add(title)
        require(len(soup.select('h1'))==1 and len(soup.select('main#content'))==1,'Reading landmarks differ')
        require(soup.body.get('data-template')=='riskium-pages-1','Unregistered current template')
        require(len(soup.select('nav[aria-label="Primary"]'))==1,'Missing primary navigation')
        require(bool(soup.select('a.skip-link[href="#content"]')),'Missing keyboard skip link')
        require(bool(soup.select('details.mobile-navigation')),'Missing narrow-screen navigation')
        require(bool(soup.select('.site-footer')),'Missing common footer')
        css=[n.get('href','') for n in soup.select('link[rel=stylesheet]')]
        require(any(n.endswith('assets/portal.css') for n in css),'Shared design tokens absent')
        rows.append(dict(path=path.relative_to(docs).as_posix(),title=title,template='riskium-pages-1',h1=1,main=1,primary_nav=True,skip=True,mobile_navigation=True))
    return dict(status='CURRENT_PRESENTATION_PASS',pages=len(rows),inventory=rows,
                limits='Static landmarks and shared presentation contract; browser behavior and usability are separate evidence.')
