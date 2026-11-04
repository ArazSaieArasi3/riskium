"""Source-bound v0.3.8 selection, six-asset freeze and publication.

The extracted verifier uses only the standard library. Internal agreement is
not authenticity: obtain the archive digest/source from a trusted publication.
Original scientific receipts retain their original sources and pending states.
"""
import argparse,base64,copy,gzip,hashlib,io,json,os,re,subprocess,sys,tarfile,tempfile,time,zipfile
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
from urllib.request import Request,build_opener,HTTPRedirectHandler
from urllib.error import HTTPError,URLError
ROOT=Path(__file__).resolve().parents[3]
TAG='v0.3.8';REPO='ArazSaieArasi3/riskium'
POLICY='releases/selection-policy-v0.3.8.json';MATRIX='releases/selection-v0.3.8.json'
PRIOR='releases/selection-v0.3.7.json';NOTES='docs/release-v0.3.8.md'
BASELINE='evaluation/releases/v0.3.8/predecessor-publications.json'
DESCRIPTORS={'DOCUMENTATION':'documentation/0.4.7/component.json','MANUSCRIPT_REVIEW':'evaluation/manuscript-review/v7.2.3/component.json'}
ASSETS={'riskium-v0.3.8-source.tar.gz','source-manifest.json','artifact-versions.json','freeze-receipt.json','release-notes.md','SHA256SUMS.txt'}
CI_PACKETS=[('current','source-transition.yml','current-source-transition-'),('v036','v036-versioned-suite.yml','v036-source-suite-'),('v037','v037-versioned-suite.yml','v037-maintained-source-suite-')]
def require(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def object_id(kind,b):return hashlib.sha1(kind+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def tree_id(payload,modes):
    root={}
    for path,b in payload.items():
        parts=safe(path).split('/');node=root
        for name in parts[:-1]:
            require(name not in node or isinstance(node[name],dict),'Conflicting source paths');node=node.setdefault(name,{})
        require(parts[-1] not in node,'Conflicting source paths');require(modes[path] in (0o644,0o755),'Unsupported source mode');node[parts[-1]]=(0o100000|modes[path],object_id(b'blob',b))
    def visit(node):
        body=b''
        for name,value in sorted(node.items(),key=lambda x:(x[0]+('/' if isinstance(x[1],dict) else '')).encode()):
            mode,ident=(0o40000,visit(value)) if isinstance(value,dict) else value
            body+=format(mode,'o').encode()+b' '+name.encode()+b'\0'+bytes.fromhex(ident)
        return object_id(b'tree',body)
    return visit(root)
def encode(v):return (json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()
def safe(n):
    p=PurePosixPath(n);require(isinstance(n,str) and n and '\\' not in n and '\0' not in n and not p.is_absolute() and str(p)==n and not ({'.','..','.git'}&set(p.parts)),'Unsafe path: '+str(n));return n
def read(n,root=ROOT):
    p=root/safe(n);require(p.resolve().is_relative_to(root.resolve()) and not p.is_symlink(),'Unsafe source: '+n);return p.read_bytes()
def load(n,root=ROOT):return json.loads(read(n,root))
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def ordered(versions,graph):
    require(set(versions)==set(graph),'Dependency component set differs');left=list(graph);out=[]
    for edges in graph.values():
        require(len({e['id'] for e in edges})==len(edges),'Duplicate dependency')
        for e in edges:require(e['id'] in versions and e['version']==versions[e['id']],'Unresolved dependency')
    while left:
        ready=[i for i in left if all(e['id'] in out for e in graph[i])];require(ready,'Dependency cycle')
        for i in ready:out.append(i);left.remove(i)
    return out
def selection(root=ROOT):
    policy=load(POLICY,root);prior=load(PRIOR,root)
    require(sha(read(PRIOR,root))==policy['predecessor_selection_sha256'],'Predecessor selection changed')
    require(policy['target']==TAG and policy['expected_components']==32 and prior['scientific_versions']==policy['scientific_versions'],'Declared scope changed')
    aliases={p:policy['retained_prefix']+p for p in policy['declared_delivery_rebindings']}
    require(len(aliases)==15 and len(prior['selected_files_sha256'])==904,'Predecessor denominator differs')
    inventory={}
    def add(p,h):
        safe(p);require(sha(read(p,root))==h,'Binding changed: '+p);require(p not in inventory or inventory[p]==h,'Conflicting ownership: '+p);inventory[p]=h
    for p,h in prior['selected_files_sha256'].items():add(aliases.get(p,p),h)
    rows=copy.deepcopy(prior['artifacts'])
    for row in rows:
        for f in row['files']:
            if f['path'] in aliases:f['original_path']=f['path'];f['path']=aliases[f['path']]
    for ident,path in DESCRIPTORS.items():
        d=load(path,root);require(d['id']==ident and d['compatible_model']=='0.3.1','Wrong descriptor')
        require(d['version']==('0.4.7' if ident=='DOCUMENTATION' else '7.2.3'),'Component version differs')
        previous=next((r for r in rows if r['id']==ident),None)
        files={f['path']:f['sha256'] for f in previous['files']} if previous else {}
        files.update(d['files_sha256']);files[path]=sha(read(path,root))
        row=dict(id=ident,version=d['version'],compatible_model='0.3.1',descriptor_path=path,status='SELECTED_NOT_FROZEN',scope=d['scope'],files=[dict(path=p,sha256=h) for p,h in sorted(files.items())])
        if previous:rows[rows.index(previous)]=row
        else:rows.append(row)
    graph=copy.deepcopy(prior['dependencies']);graph['MANUSCRIPT_REVIEW']=[dict(id=i,version=next(r['version'] for r in rows if r['id']==i)) for i in ['MODEL','ORSD','FORMAL_REFERENCE','INTEGRATED_VALIDATION']]
    graph['DOCUMENTATION'].append(dict(id='MANUSCRIPT_REVIEW',version='7.2.3'))
    versions={r['id']:r['version'] for r in rows};require(len(versions)==len(rows)==32,'Component denominator differs')
    for edges in graph.values():
        for e in edges:e['version']=versions[e['id']]
    order=ordered(versions,graph)
    for row in rows:
        for f in row['files']:add(f['path'],f['sha256'])
    support=[POLICY,BASELINE,'plans/v0.3.8.md',NOTES,'tools/releases/v038/release.py','tests/test_release_v038.py','.github/workflows/release-v038.yml','tools/publication/v038_documentation.py','.github/workflows/reader-v038.yml']
    for p in support:add(p,sha(read(p,root)))
    paper=load('evaluation/manuscript-review/v7.2.3/receipt.json',root)
    require(paper['layout']['pages']==10 and paper['references']==36 and len(paper['all_six_author_papers_retained'])==6 and paper['status']=='AUTHOR_HELD_CANDIDATE_NOT_SUBMITTED','Manuscript receipt boundary differs')
    require(paper['source_model_sha256']==sha(read('ontology/riskium-model.json',root)),'Paper/model identity differs')
    return dict(schema='riskium-v038-source-selection-v1',target=TAG,issue=76,stage='SELECTED_NOT_FROZEN',scientific_versions=policy['scientific_versions'],current_author_held_manuscript='7.2.3',predecessor='v0.3.7',artifacts=rows,dependencies=graph,dependency_order=order,selected_files_sha256=dict(sorted(inventory.items())),historical_delivery_aliases=aliases,summary=dict(components=32,retained=30,replaced=1,added=1,preserved_predecessor_bodies=904,delivery_aliases=15,selected_files=len(inventory),dependency_edges=sum(map(len,graph.values()))),independent_semantic_acceptance=False,new_model_or_schema=False,organizational_admissions='11 WITHHELD',article_binaries_included=False)
def prepare():
    p=load(POLICY);prior=load(PRIOR)
    for name in p['declared_delivery_rebindings']:
        b=git('show',p['predecessor_source']+':'+name);require(sha(b)==prior['selected_files_sha256'][name],'Historical body changed')
        dest=ROOT/(p['retained_prefix']+name);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
    groups={'DOCUMENTATION':[n.as_posix() for n in ROOT.glob('documentation/0.4.7/**/*') if n.is_file() and n.name!='component.json']+['tools/publication/v038_documentation.py','tools/publication/dictionary_documentation.py','tools/build_concept_dictionary.py','tools/build_subdomain_relationships.py','diagrams/subdomain-relationships.svg','diagrams/subdomain-relationships-matrix.svg']+[n.relative_to(ROOT).as_posix() for n in ROOT.glob('documentation/concepts/0.3.1/*') if n.is_file()],
            'MANUSCRIPT_REVIEW':[n.relative_to(ROOT).as_posix() for ns in ['v7.1.0','v7.2.0','v7.2.1','v7.2.2','v7.2.3'] for n in (ROOT/'evaluation/manuscript-review'/ns).rglob('*') if n.is_file() and n.name!='component.json']+['references/followup-2026-11-03.json','references/followup-2026-11-03.md','references/disposition-2026-11-04.md','references/full-pdf-update-2026-11-04.md']}
    for ns in ['documentation/0.4.5','documentation/0.4.6','tools/publication']:
        groups['DOCUMENTATION'] += [n.relative_to(ROOT).as_posix() for n in (ROOT/ns).rglob('*') if n.is_file() and '__pycache__' not in n.parts and n.suffix!='.pyc']
    groups['DOCUMENTATION'] += ['tools/check_source_transition.py','tools/audit_reader_consistency.py','.github/workflows/dictionary-reader.yml','.github/workflows/reader-v038.yml']
    for ident,names in groups.items():
        names=[Path(n).relative_to(ROOT).as_posix() if Path(n).is_absolute() else n for n in names]
        d=dict(schema='riskium-v038-component-v1',id=ident,version='0.4.7' if ident=='DOCUMENTATION' else '7.2.3',compatible_model='0.3.1',scope='Maintained reader and model-derived dictionary; old technical checkpoints explicitly dated.' if ident=='DOCUMENTATION' else 'Public article review sources and receipts; author-held binaries excluded; no submission or independent semantic rating.',files_sha256={n:sha(read(n)) for n in sorted(set(names))})
        (ROOT/DESCRIPTORS[ident]).write_bytes(encode(d))
    m=selection();(ROOT/MATRIX).write_bytes(encode(m));return m['summary']
class CleanRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        r=super().redirect_request(req,fp,code,msg,headers,newurl)
        if r and __import__('urllib.parse',fromlist=['urlsplit']).urlsplit(newurl).netloc!=__import__('urllib.parse',fromlist=['urlsplit']).urlsplit(req.full_url).netloc:r.remove_header('Authorization')
        return r
def api(path,method='GET',data=None,binary=False):
    require('..' not in path and not path.startswith('/'),'Unsafe API route');headers={'Accept':'application/vnd.github+json','User-Agent':'riskium-v038-release'}
    if os.environ.get('GH_TOKEN'):headers['Authorization']='Bearer '+os.environ['GH_TOKEN']
    body=json.dumps(data).encode() if data is not None else None
    if body:headers['Content-Type']='application/json'
    for attempt in range(4):
        try:
            with build_opener(CleanRedirect()).open(Request('https://api.github.com/repos/'+REPO+'/'+path,data=body,headers=headers,method=method),timeout=45) as r:b=r.read()
            break
        except (HTTPError,URLError,TimeoutError) as exc:
            transient=not isinstance(exc,HTTPError) or exc.code in (429,500,502,503,504)
            if method!='GET' or not transient or attempt==3:raise
            time.sleep(2*(attempt+1))
    return b if binary else json.loads(b)
def inventory():
    tags={r['ref'].removeprefix('refs/tags/'):r['object'] for r in api('git/matching-refs/tags/')}
    return [dict(id=r['id'],tag=r['tag_name'],draft=r['draft'],prerelease=r['prerelease'],published_at=r['published_at'],body_sha256=sha((r['body'] or '').encode()),tag_object=tags[r['tag_name']],assets=[dict(id=a['id'],name=a['name'],bytes=a['size'],digest=a.get('digest')) for a in r['assets']]) for r in sorted(api('releases?per_page=100'),key=lambda r:r['tag_name']) if r['tag_name']!=TAG]
def evidence_check(e,source,root):
    wanted=set(load(POLICY,root)['required_ci_paths']);runs=e['required_runs'];require({r['path'] for r in runs}==wanted and len(runs)==len(wanted),'Incomplete required CI set')
    for r in runs:require(r['head_sha']==source and r['head_branch']=='main' and r['event']=='push' and r['status']=='completed' and r['conclusion']=='success' and r['repository']['full_name']==r['head_repository']['full_name']==REPO,'Unqualified CI source')
    require(set(e['downloaded_artifacts'])=={'current','v036','v037'},'Missing independently downloaded CI evidence')
    for p in e['downloaded_artifacts'].values():
        b=base64.b64decode(p['zip_base64'],validate=True);a=p['artifact'];require(a['digest']=='sha256:'+sha(b) and a['workflow_run']['head_sha']==source and not a['expired'],'Artifact identity differs')
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            require(len(set(z.namelist()))==len(z.namelist()),'Duplicate evidence member')
            for n in z.namelist():safe(n.rstrip('/'))
            bounds=[json.loads(z.read(n)) for n in z.namelist() if n.endswith(('source-boundary.json','current-source-boundary.json'))]
            require(bounds and all(r['candidate_commit']==source and r['scientific_model_changed'] is False for r in bounds),'Missing exact candidate boundary')
    require(e['previous_releases']==load(BASELINE,root),'Prior release inventory differs')
    return dict(required_ci=len(runs),downloaded_ci_artifacts=3,historical_receipts_rewritten=False)
def ci_evidence(source):
    wanted=load(POLICY)['required_ci_paths'];deadline=time.monotonic()+1200
    while True:
        require(api('git/ref/heads/main')['object']['sha']==source,'Main advanced during qualification')
        runs=api('actions/runs?head_sha='+source+'&per_page=100')['workflow_runs'];chosen=[]
        for path in wanted:
            rs=[r for r in runs if r['path']==path and r['event']=='push' and r['head_branch']=='main']
            if rs:chosen.append(max(rs,key=lambda r:r['id']))
        failed=[r for r in chosen if r['status']=='completed' and r['conclusion']!='success'];require(not failed,'Current CI failed: '+str([(r['name'],r['conclusion']) for r in failed]))
        if len(chosen)==len(wanted) and all(r['conclusion']=='success' for r in chosen):break
        require(time.monotonic()<deadline,'Qualification timed out');print('Awaiting exact-main CI',len(chosen),flush=True);time.sleep(15)
    packets={}
    for role,path,prefix in CI_PACKETS:
        run=next(r for r in chosen if r['path'].endswith('/'+path));arts=api('actions/runs/'+str(run['id'])+'/artifacts?per_page=100')['artifacts'];found=[a for a in arts if a['name']==prefix+source and not a['expired']];require(len(found)==1,'Exact-source artifact missing');a=found[0];b=api('actions/artifacts/'+str(a['id'])+'/zip',binary=True);packets[role]={'artifact':a,'zip_base64':base64.b64encode(b).decode()}
    e=dict(required_runs=chosen,downloaded_artifacts=packets,previous_releases=inventory());evidence_check(e,source,ROOT);return e
def write_assets(folder,source,entries,matrix,evidence,commit_object=None):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);require(not list(folder.iterdir()),'Freeze folder must be empty');require(re.fullmatch('[a-f0-9]{40}',source),'Invalid source')
    files={p:dict(sha256=sha(b),bytes=len(b),mode=mode) for p,mode,b in entries};require(len(files)==len(entries),'Duplicate source entry')
    for p in files:safe(p)
    with (folder/'riskium-v0.3.8-source.tar.gz').open('wb') as f,gzip.GzipFile(fileobj=f,mode='wb',mtime=0,filename='') as gz,tarfile.open(fileobj=gz,mode='w') as t:
        for p,mode,b in entries:
            i=tarfile.TarInfo(TAG+'/'+p);i.size=len(b);i.mode=mode;i.mtime=0;t.addfile(i,io.BytesIO(b))
    (folder/'source-manifest.json').write_bytes(encode(dict(tag=TAG,source_commit=source,files=files)))
    (folder/'artifact-versions.json').write_bytes(encode(matrix))
    (folder/'release-notes.md').write_bytes(dict((p,b) for p,mode,b in entries)[NOTES])
    (folder/'freeze-receipt.json').write_bytes(encode(dict(schema='riskium-v038-freeze-v1',tag=TAG,source_commit=source,commit_object_base64=base64.b64encode(commit_object).decode() if commit_object else None,stage='FROZEN_NOT_PUBLISHED',publication_executed=False,created_at_utc=datetime.now(timezone.utc).isoformat(),evidence=evidence,independent_semantic_validation=False)))
    (folder/'SHA256SUMS.txt').write_text(''.join(sha((folder/n).read_bytes())+'  '+n+'\n' for n in sorted(ASSETS-{'SHA256SUMS.txt'})))
def verify(folder,source):
    folder=Path(folder);require({p.name for p in folder.iterdir()}==ASSETS and all(p.is_file() and not p.is_symlink() for p in folder.iterdir()),'Exactly six regular assets required');sums={}
    for line in (folder/'SHA256SUMS.txt').read_text().splitlines():
        require(re.fullmatch('[a-f0-9]{64}  [A-Za-z0-9.\\-]+',line),'Malformed checksum');h,n=line.split('  ');require(n not in sums,'Duplicate checksum');sums[n]=h
    require(set(sums)==ASSETS-{'SHA256SUMS.txt'},'Checksum set differs')
    for n,h in sums.items():require(sha((folder/n).read_bytes())==h,'Asset checksum differs: '+n)
    m=json.loads((folder/'source-manifest.json').read_bytes());r=json.loads((folder/'freeze-receipt.json').read_bytes());require(m['tag']==r['tag']==TAG and m['source_commit']==r['source_commit']==source and r['stage']=='FROZEN_NOT_PUBLISHED' and r['publication_executed'] is False and r['independent_semantic_validation'] is False,'Freeze source/phase differs')
    payload={}
    with tarfile.open(folder/'riskium-v0.3.8-source.tar.gz','r:gz') as t:
        for i in t:
            require(i.isfile() and i.name.startswith(TAG+'/') and i.mode in (0o644,0o755) and i.uid==i.gid==0,'Unsafe archive member');p=safe(i.name[len(TAG)+1:]);require(p not in payload,'Duplicate archive member');b=t.extractfile(i).read();require(m['files'].get(p)==dict(sha256=sha(b),bytes=len(b),mode=i.mode),'Archive binding differs: '+p);payload[p]=b
    require(set(payload)==set(m['files']),'Source inventory incomplete');require(payload[NOTES]==(folder/'release-notes.md').read_bytes(),'Release notes differ')
    commit=base64.b64decode(r['commit_object_base64'] or '',validate=True)
    require(object_id(b'commit',commit)==source,'Git commit object identity differs')
    require(commit.split(b'\n',1)[0]==b'tree '+tree_id(payload,{p:f['mode'] for p,f in m['files'].items()}).encode(),'Archive does not reconstruct the committed Git tree')
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for p,b in payload.items():q=root/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
        s=selection(root);require(encode(s)==payload[MATRIX]==(folder/'artifact-versions.json').read_bytes(),'Selected closure differs');ec=evidence_check(r['evidence'],source,root)
    return dict(status='V038_SIX_ASSET_OFFLINE_PASS',source_commit=source,source_files=len(payload),components=32,preserved_predecessor_bodies=904,external_authenticity_required=True,**ec)
def freeze(folder,source):
    require(git('rev-parse','HEAD').decode().strip()==source and not git('status','--porcelain').strip(),'Clean exact source required');require(api('releases/latest')['tag_name']=='v0.3.7','Predecessor is no longer Latest')
    s=selection();require(encode(s)==read(MATRIX),'Selection drift');e=ci_evidence(source);entries=[]
    for item in git('ls-tree','-rz','HEAD').split(b'\0'):
        if not item:continue
        meta,p=item.split(b'\t',1);mode,kind,ident=meta.split();require(kind==b'blob' and mode in (b'100644',b'100755'),'Nonregular source');entries.append((p.decode(),int(mode,8)&0o777,git('cat-file','blob',ident.decode())))
    write_assets(folder,source,entries,s,e,git('cat-file','commit',source));result=verify(folder,source)
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        with tarfile.open(Path(folder)/'riskium-v0.3.8-source.tar.gz') as t:t.extractall(root,filter='data')
        env=dict(os.environ,PATH='/no-git');subprocess.run([sys.executable,'-S',str(root/TAG/'tools/releases/v038/release.py'),'verify','--folder',str(Path(folder).resolve()),'--source',source],env=env,check=True)
    return result
def public_readback(folder,source,output):
    release=api('releases/tags/'+TAG);require(not release['draft'] and not release['prerelease'] and api('releases/latest')['id']==release['id'],'Release not published Latest');tag=api('git/ref/tags/'+TAG)['object'];require(tag['type']=='commit' and tag['sha']==source,'Wrong release tag source')
    require({a['name'] for a in release['assets']}==ASSETS and len(release['assets'])==6,'Published asset set differs');folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);rows=[]
    for a in release['assets']:
        for attempt in range(4):
            try:
                with build_opener(CleanRedirect()).open(Request(a['browser_download_url'],headers={'User-Agent':'Riskium-independent-public-readback'}),timeout=60) as f:b=f.read()
                break
            except (HTTPError,URLError,TimeoutError) as exc:
                transient=not isinstance(exc,HTTPError) or exc.code in (404,429,500,502,503,504)
                if not transient or attempt==3:raise
                time.sleep(2*(attempt+1))
        require(sha(b)==a['digest'].removeprefix('sha256:') and len(b)==a['size'],'Public download differs');(folder/a['name']).write_bytes(b);rows.append(dict(name=a['name'],sha256=sha(b),bytes=len(b),url=a['browser_download_url']))
    result=verify(folder,source);require(inventory()==load(BASELINE),'Prior publications changed');record=dict(schema='riskium-v038-publication-v1',status='INDEPENDENT_PUBLIC_DOWNLOADS_PASS',tag=TAG,source_commit=source,release_id=release['id'],release_url=release['html_url'],published_at=release['published_at'],checked_at_utc=datetime.now(timezone.utc).isoformat(),latest=True,assets=rows,offline_verification=result,previous_releases_unchanged=True)
    Path(output).write_bytes(encode(record));return record
def publish(folder,source,output):
    verify(folder,source);require(api('git/ref/heads/main')['object']['sha']==source,'Main advanced before publication');require(inventory()==load(BASELINE),'Prior publication inventory drift')
    try:r=api('releases/tags/'+TAG)
    except HTTPError as e:
        if e.code!=404:raise
        require(api('releases/latest')['tag_name']=='v0.3.7','Unexpected latest release')
        try:api('git/ref/tags/'+TAG)
        except HTTPError as e:require(e.code==404,'Cannot inspect target tag')
        else:raise ValueError('Target tag already exists')
        r=api('releases',method='POST',data=dict(tag_name=TAG,target_commitish=source,name='Riskium v0.3.8 — manuscript evidence and current reader',body=(Path(folder)/'release-notes.md').read_text(),draft=True,prerelease=False))
    if not r['draft']:return public_readback(Path(folder).parent/'independent-public-downloads',source,output)
    require(r['target_commitish']==source and r['body']==(Path(folder)/'release-notes.md').read_text(),'Unrecognized draft; refusing mutation')
    existing={a['name']:a for a in r['assets']};require(set(existing)<=ASSETS,'Unexpected draft asset')
    for n in sorted(ASSETS):
        b=(Path(folder)/n).read_bytes()
        if n in existing:require(existing[n]['digest']=='sha256:'+sha(b),'Conflicting draft asset');continue
        url='https://uploads.github.com/repos/'+REPO+'/releases/'+str(r['id'])+'/assets?name='+n
        req=Request(url,data=b,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Content-Type':'application/octet-stream','User-Agent':'Riskium-v038-publisher'},method='POST')
        with build_opener(CleanRedirect()).open(req,timeout=90) as f:a=json.load(f)
        require(a['digest']=='sha256:'+sha(b),'Uploaded asset differs')
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['gh','release','download',TAG,'--repo',REPO,'--dir',tmp],check=True);verify(tmp,source)
    require(api('git/ref/heads/main')['object']['sha']==source,'Main advanced while draft was verified')
    api('releases/'+str(r['id']),method='PATCH',data=dict(draft=False,make_latest='true'))
    record=public_readback(Path(folder).parent/'independent-public-downloads',source,output)
    for a in record['assets']:require(a['sha256']==sha((Path(folder)/a['name']).read_bytes()),'Public asset differs from frozen input')
    return record
def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','check','freeze','verify','publish','readback']);p.add_argument('--folder',type=Path);p.add_argument('--source');p.add_argument('--output',default='publication.json');a=p.parse_args()
    if a.action=='prepare':result=prepare()
    elif a.action=='check':result=selection();require(encode(result)==read(MATRIX),'Selection differs');result={'status':'V038_SELECTION_PASS',**result['summary']}
    else:
        require(a.folder is not None and re.fullmatch('[a-f0-9]{40}',a.source or ''),'Folder and exact source are required')
        result=freeze(a.folder,a.source) if a.action=='freeze' else verify(a.folder,a.source) if a.action=='verify' else publish(a.folder,a.source,a.output) if a.action=='publish' else public_readback(a.folder,a.source,a.output)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
