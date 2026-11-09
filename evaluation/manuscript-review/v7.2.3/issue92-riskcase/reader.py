"""Reuse the reviewed reader renderer with explicit successor inputs and text."""
from pathlib import Path
from types import SimpleNamespace
import importlib.util,json,sys,hashlib,tempfile
import build_candidate as b
HERE=Path(__file__).resolve().parent;OUT=HERE/'reader'
sys.path.insert(0,str(HERE.parent/'issue93-dictionary'))
import build_dictionary as old
import audit_dictionary as audit

def generate(check=False):
 b.build(check=True)
 with tempfile.TemporaryDirectory(prefix='riskium-case-reader-') as tmp:
  transient=Path(tmp);(transient/'generated').mkdir()
  for name in ['candidate.ontouml.json','candidate.owl.ttl']:(transient/'generated'/name).write_bytes((HERE/name).read_bytes())
  facade=SimpleNamespace(CONTRACT=b.CONTRACT,HERE=transient,resolve=b.resolve,validate_contract=b.validate_contract,export=lambda c,check=False:b.build(check=True))
  old.export=facade;old.OUT=OUT;audit.build=old
  files=old.build()
 for n,t in list(files.items()):
  if not n.endswith('.md'):continue
  t=t.replace('[Rebuildable source recipe](../../issue93-generalization-sets/build_candidate.py)','[Rebuildable source recipe](../build_candidate.py)').replace('[Export contract](../../issue93-export-contract/input-contract.json)','[Export contract](../input-contract.json)')
  if n=='RKM-X01.md':
   old_note='The source RiskCase definition is retained in this candidate. The adopted broader RiskCase meaning and its profile/model migration are tracked separately in [issue #92](https://github.com/ArazSaieArasi3/riskium/issues/92); this dictionary does not silently perform that migration.'
   t=t.replace(old_note,'The adopted analytical-item definition is implemented in this successor source. [issue #92](https://github.com/ArazSaieArasi3/riskium/issues/92) tracks the remaining maintained-channel publication. Analytical task readiness and local operational-register eligibility are distinct; the [profile implementation](../case_profiles.py) supplies the selected explicit-data checks.')
  files[n]=t
 manifest=json.loads(files['manifest.json']);manifest['files_sha256']={n:hashlib.sha256(t.encode()).hexdigest() for n,t in sorted(files.items()) if n!='manifest.json'};files['manifest.json']=b.dump(manifest)
 if check:
  if not OUT.exists() or {p.name for p in OUT.iterdir() if p.is_file()}!=set(files):raise ValueError('Successor reader inventory mismatch')
  if any((OUT/n).read_text()!=t for n,t in files.items()):raise ValueError('Successor reader stale')
 else:
  OUT.mkdir(exist_ok=True)
  for n,t in files.items():(OUT/n).write_text(t)
 m=json.loads((HERE/'candidate-model.json').read_text());coverage=audit.audit(files,m)
 return files,coverage
if __name__=='__main__':f,c=generate('--check' in sys.argv);print(b.dump(c))
