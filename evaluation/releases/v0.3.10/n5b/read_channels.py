"""Read actual public bodies against the exact deployed authenticated artifact."""
import concurrent.futures,hashlib,json,pathlib,subprocess,sys,urllib.parse,urllib.request
artifact=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
site=artifact/'published/site';wiki=artifact/'published/wiki';m=json.loads((site/'publication-manifest.json').read_text())
assert m['source_ref']=='4ae0cdc72a1008e8107be320694d90324890b696'
assert m['documentation_commit']=='fb751343d19007c9fa8c43376181d8d1c5c2cb4f' and m['release_id']==440894153 and m['published']
files=dict(m['files_sha256']);files['publication-manifest.json']=hashlib.sha256((site/'publication-manifest.json').read_bytes()).hexdigest();files.pop('.nojekyll',None)
def read(item):
 name,digest=item;url='https://arazsaiearasi3.github.io/riskium/'+urllib.parse.quote(name,safe='/')
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Riskium-channel-readback'}),timeout=30) as r:b=r.read();status=r.status
  sha=hashlib.sha256(b).hexdigest();return {'path':name,'url':url,'http_status':status,'bytes':len(b),'sha256':sha,'expected_sha256':digest,'matches':sha==digest}
 except Exception as e:return {'path':name,'url':url,'matches':False,'error':str(e)}
rows=list(concurrent.futures.ThreadPoolExecutor(max_workers=24).map(read,sorted(files.items())))
pages={'schema':'riskium-actual-pages-readback-0310/1','source_commit':m['source_ref'],'documentation_commit':m['documentation_commit'],'release_id':m['release_id'],'expected':len(files),'matched':sum(x['matches'] for x in rows),'files':rows,'excluded_build_marker':'.nojekyll'}
(out/'pages-readback.json').write_text(json.dumps(pages,indent=2)+'\n')
clone=out/'native-wiki';subprocess.run(['git','clone','--quiet','https://github.com/ArazSaieArasi3/riskium.wiki.git',str(clone)],check=True)
wh=subprocess.check_output(['git','rev-parse','HEAD'],cwd=clone,text=True).strip();wr=[]
for name,digest in sorted(m['wiki_files_sha256'].items()):
 p=clone/name;b=p.read_bytes() if p.is_file() else None;sha=hashlib.sha256(b).hexdigest() if b is not None else None;wr.append({'path':name,'expected_sha256':digest,'actual_sha256':sha,'matches':sha==digest})
w={'schema':'riskium-actual-wiki-readback-0310/1','wiki_commit':wh,'expected':len(wr),'matched':sum(x['matches'] for x in wr),'files':wr,'unexpected':sorted(p.name for p in clone.glob('*.md') if p.name not in m['wiki_files_sha256'])}
(out/'wiki-readback.json').write_text(json.dumps(w,indent=2)+'\n')
s={'pages_expected':pages['expected'],'pages_matched':pages['matched'],'wiki_expected':w['expected'],'wiki_matched':w['matched'],'all_pages_match':pages['matched']==pages['expected'],'all_wiki_match':w['matched']==w['expected'],'coordinated_acceptance':pages['matched']==pages['expected'] and w['matched']==w['expected'],'wiki_status':'OPEN' if w['matched']!=w['expected'] else 'MATCHED'}
(out/'channel-summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s),flush=True)
assert s['all_pages_match'], 'Actual Pages bodies differ; inspect pages-readback.json'
