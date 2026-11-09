"""Replay candidate packets in a disposable worktree; preserve archived receipts."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,time
from rdflib import Graph
from rdflib.compare import isomorphic
HERE=Path(__file__).resolve().parent
BASE=Path('evaluation/manuscript-review/v7.2.3')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(v):return json.dumps(v,indent=2,ensure_ascii=False)+'\n'
def main(a):
 root=a.root.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
 before=subprocess.check_output(['git','diff','--binary','HEAD'],cwd=root)
 frozen=['ontology/riskium-model.json','ontology/native/riskium.ontouml.json','ontology/derived/riskium.owl.ttl','evaluation/native-review-decisions.json']
 protected={p:sha(root/p) for p in frozen}
 report={'schema':'riskium-issue93-ci-replay-1','execution_commit':commit,'runner_sha256':sha(__file__),'status':'RUNNING','phases':[],'live_deployment':False,'production_promoted':False}
 report['tools']={'schema_sha256':sha(a.schema),'robot_sha256':sha(a.robot),'sdk_package_sha256':sha(a.sdk/'package.json')}
 report['runner_matches_execution_commit']=subprocess.run(['git','cat-file','-e',commit+':'+str(HERE.relative_to(root)/'run_ci.py')],cwd=root,capture_output=True).returncode==0 and subprocess.check_output(['git','show',commit+':'+str(HERE.relative_to(root)/'run_ci.py')],cwd=root)==Path(__file__).read_bytes()
 temp=Path(tempfile.mkdtemp(prefix='riskium-issue93-'));work=temp/'repo';added=False
 def run(label,argv,packet=None,receipt=None):
  start=time.monotonic();r=subprocess.run([str(x) for x in argv],cwd=work,capture_output=True,text=True,timeout=300)
  d=out/label;d.mkdir(exist_ok=True);(d/'stdout.txt').write_text(r.stdout);(d/'stderr.txt').write_text(r.stderr)
  item={'phase':label,'exit_code':r.returncode,'elapsed_ms':round((time.monotonic()-start)*1000),'status':'PASS' if r.returncode==0 else 'FAIL'}
  if receipt:
   src=work/BASE/packet/receipt
   if src.exists():shutil.copy2(src,d/receipt);item['receipt_sha256']=sha(src)
  report['phases'].append(item);print(label+': '+item['status'],flush=True)
  if r.returncode:raise RuntimeError(label+' failed; see '+str(d))
 try:
  subprocess.run(['git','worktree','add','--detach',str(work),commit],cwd=root,check=True,capture_output=True);added=True
  py=sys.executable;engine=['--schema',a.schema,'--robot',a.robot];native=engine+['--sdk',a.sdk,'--node',a.node]
  run('B01',[py,BASE/'issue93-evidence-use/verify_candidate.py',*engine],'issue93-evidence-use','candidate-report.json')
  run('B02',[py,BASE/'issue93-generalization-sets/verify_candidate.py',*engine],'issue93-generalization-sets','candidate-report.json')
  profile=work/BASE/'issue93-integration/combined-managed.shacl.ttl';original=profile.read_bytes();original_sha=sha(profile)
  run('B03',[py,BASE/'issue93-integration/check_integration.py',*native],'issue93-integration','integration-report.json')
  shutil.copy2(profile,out/'B03/combined-managed.shacl.ttl')
  new_sha=sha(profile);equal=isomorphic(Graph().parse(data=original,format='turtle'),Graph().parse(profile,format='turtle'))
  if not equal:raise ValueError('Replayed SHACL profile differs logically from the frozen contract input')
  report['profile_input_selection']={'fresh_B03_sha256':new_sha,'selected_B04_contract_sha256':original_sha,'isomorphic':True,'reason':'B03 uses fresh serialization retained beside its receipt. B04 separately selects the committed contract input; blank-node byte order is not a source change.'}
  profile.write_bytes(original)
  run('B04',[py,BASE/'issue93-export-contract/verify_export.py',*native],'issue93-export-contract','verification-report.json')
  run('B05',[py,BASE/'issue93-relational-use/verify_use.py'],'issue93-relational-use','verification-report.json')
  run('B06',[py,BASE/'issue93-dictionary/verify_dictionary.py'],'issue93-dictionary','verification-report.json')
  run('B07-projection',[py,HERE/'build_projection.py','--root',work,'--output',out/'projection','--commit',commit])
  run('B07-tests',[py,'-m','unittest','discover','-s',HERE,'-p','test_ci.py','-v'])
  run('source-transition',[py,'tools/check_source_transition.py'])
  report['protected_files_unchanged']=protected=={p:sha(work/p) for p in frozen}
  if not report['protected_files_unchanged']:raise ValueError('Frozen scientific source changed during replay')
  report['status']='PASS_CANDIDATE_REPLAY_AND_STAGED_PUBLICATION'
 except Exception as e:
  report['status']='FAIL';report['error']=str(e)
 finally:
  if added:subprocess.run(['git','worktree','remove','--force',str(work)],cwd=root,check=True,capture_output=True)
  shutil.rmtree(temp,ignore_errors=True)
  report['original_checkout_diff_unchanged']=before==subprocess.check_output(['git','diff','--binary','HEAD'],cwd=root)
  if not report['original_checkout_diff_unchanged']:report['status']='FAIL';report['error']='Original checkout changed during replay'
  (out/'ci-report.json').write_text(dump(report));print(dump({'status':report['status'],'execution_commit':commit,'phases':report['phases']}),flush=True)
 return int(report['status']=='FAIL')
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ['root','output','schema','robot','sdk','node']:p.add_argument('--'+name,type=Path,required=True)
 a=p.parse_args()
 for name in ['schema','robot','sdk','node']:setattr(a,name,getattr(a,name).resolve())
 raise SystemExit(main(a))
