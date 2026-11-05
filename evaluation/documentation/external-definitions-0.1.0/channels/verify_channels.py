"""Verify actual deployed HTTP bodies and a freshly fetched native Wiki snapshot."""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,subprocess,time
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError

sha=lambda b:hashlib.sha256(b).hexdigest()
def read(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url,headers={'User-Agent':'Riskium-source-review-verifier','Cache-Control':'no-cache'}),timeout=35) as f:
                return f.read()
        except (HTTPError,URLError,TimeoutError) as e:
            if isinstance(e,HTTPError) and e.code not in [429,500,502,503,504]:raise
            if attempt==2:raise
            time.sleep(attempt+1)

def run(site,wiki,source,out,allow_wiki_pending=False):
    files={p.relative_to(site).as_posix():p.read_bytes() for p in site.rglob('*') if p.is_file()}
    manifest=json.loads(files['publication-manifest.json'])
    assert manifest['current_source_commit']==source and manifest['documentation_version']=='0.4.8'
    # upload-pages-artifact omits the hidden build marker; it is not an HTTP resource.
    expected_public={n:h for n,h in manifest['files_sha256'].items() if n!='.nojekyll'}
    assert manifest['files_sha256'].get('.nojekyll')==sha(b'')
    assert expected_public=={n:sha(b) for n,b in files.items() if n not in ['publication-manifest.json','.nojekyll']}
    rows=[]
    def check(item):
        name,body=item;actual=read('https://arazsaiearasi3.github.io/riskium/'+name)
        assert actual==body,'HTTP byte mismatch: '+name
        return dict(path=name,sha256=sha(actual),bytes=len(actual))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        rows=list(pool.map(check,[(n,b) for n,b in sorted(files.items()) if n!='.nojekyll']))
    status=json.loads(files['current/published-status.json'])
    expected=status['wiki_files_sha256'];actual={p.name:sha(p.read_bytes()) for p in wiki.glob('*.md')}
    wiki_equal=actual==expected and len(actual)==106
    if not allow_wiki_pending:
        assert wiki_equal,'Wiki differs: '+str(set(actual)^set(expected))
    review=json.loads(files['current/concepts/external-definition-review.json'])
    assert review['summary']['concepts']==80 and review['summary']['formal_equivalences']==0
    result=dict(status='SOURCE_REVIEW_HTTP_AND_NATIVE_WIKI_PASS' if wiki_equal else 'SOURCE_REVIEW_HTTP_PASS_NATIVE_WIKI_PENDING',date='2026-11-05',source_commit=source,documentation_version='0.4.8',review_version='0.1.0',served_files=len(rows),all_served_bytes_match_ci_artifact=True,build_marker_not_http=['.nojekyll'],native_wiki_files=len(actual),expected_native_wiki_files=106,native_wiki_equal=wiki_equal,wiki_equal_files=sum(actual.get(n)==h for n,h in expected.items()),wiki_different_files=[n for n,h in expected.items() if n in actual and actual[n]!=h],wiki_missing_files=sorted(set(expected)-set(actual)),wiki_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=wiki,text=True).strip(),wiki_files_sha256=actual,review_summary=review['summary'],frozen_snapshots=4,model_sha256=review['model_sha256'],no_new_source_release=True,independent_ratings=0,http_files=rows)
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','served_files','native_wiki_files','source_commit','wiki_commit']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--site',type=Path,required=True);p.add_argument('--wiki',type=Path,required=True);p.add_argument('--source',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--allow-wiki-pending',action='store_true');a=p.parse_args();run(a.site,a.wiki,a.source,a.output,a.allow_wiki_pending)
