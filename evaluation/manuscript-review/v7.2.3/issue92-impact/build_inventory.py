"""Enumerate pinned tracked text matches plus reviewed generic dependencies."""
from pathlib import Path
import hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
PIN='aafc9b77ea320d726fcd0ae3d78449d03c061a26'
CASE=re.compile(r'RiskCase|risk_case|riskCase|RKM-X01|governed identity|instituted.{0,40}(?:case|subject)|(?:case|subject).{0,40}instituted',re.I)
ADMISSION=re.compile(r'committee|approval|admission|withheld|governed identity|instituted',re.I)
def dump(v):return json.dumps(v,indent=2,ensure_ascii=False)+'\n'
def sha(b):return hashlib.sha256(b).hexdigest()
def classify(n):
 if n.startswith('evaluation/sources/'):return 'NO_CHANGE','D15','Preserve source-bound cohorts/decisions; new reassessment is a separate record.'
 if n.startswith('docs/releases/') or (n.startswith('documentation/') and not n.startswith('documentation/current/')):return 'NO_CHANGE','D14','Preserve versioned snapshots; generate a successor at its own source/version path.'
 if n.startswith('docs/current/'):return 'PROFILE_RELOCATION','D17','After qualification, select the new versioned reader; retain released scientific paths.'
 if n.startswith('docs/wiki/') or n.startswith('docs/guides/') or n in ('README.md','docs/overview.md','docs/formal-method.md','tools/publication/home.md'):return 'PROSE_CORRECTION','D17','Reconcile maintained reader labels/links and source-version roles after B2; do not blanket-replace historical numbers.'
 if n.startswith('ontology/'):return 'NO_CHANGE','D16','Frozen scientific input/output: preserve and qualify a separately versioned successor.'
 if n.startswith('implementation/relational/'):return 'NO_CHANGE','D10','Retain versioned schema/fixture; declare any next local task metadata separately.'
 if n.startswith('requirements/'):return 'NO_CHANGE','D13','Preserve source-bound requirement/receipt; carry applicable expectations into the successor contract.'
 if n.startswith('references/'):return 'NO_CHANGE','D18','Preserve source attribution and scoped mappings; no new equivalence claim.'
 if n.startswith('evaluation/manuscript-review/v7.2.3/issue93-'):return 'NO_CHANGE','D16','Keep accepted B0 bytes and receipts; fork a new candidate contract instead of rebinding.'
 if n.startswith('tools/'):return 'NO_CHANGE','D16','Keep the source-specific route/guard; use pure helper reuse or a separately bound successor route.'
 return 'NO_CHANGE','D16','Preserve pinned history or supporting evidence; no direct source edit selected by this impact review.'

def build():
 raw=subprocess.check_output(['git','ls-tree','-rz',PIN],cwd=ROOT);entries=[]
 for rec in raw.split(b'\0'):
  if not rec:continue
  meta,n=rec.split(b'\t',1);mode,kind,blob=meta.decode().split();entries.append((n.decode(),blob))
 decisions=json.loads((HERE/'decisions.json').read_text())['decisions'];deps={p['path'] for d in decisions for p in d['evidence']};rows=[];binary=[];text_count=0;direct_count=0;term_count=0
 for n,blob in sorted(entries):
  data=(ROOT/n).read_bytes()
  if hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=blob:raise ValueError('Pinned tracked source has changed: '+n)
  try:t=data.decode('utf-8')
  except UnicodeError:binary.append(n);continue
  text_count+=1;lines=t.splitlines();direct=[i for i,l in enumerate(lines,1) if CASE.search(l)];terms=[i for i,l in enumerate(lines,1) if ADMISSION.search(l)]
  direct_count+=bool(direct);term_count+=bool(terms)
  if not(direct or terms or n in deps):continue
  disposition,decision,action=classify(n)
  loc=direct or terms
  rows.append({'path':n,'sha256':sha(data),'git_blob':blob,'case_match_lines':direct,'admission_match_lines':terms,'generic_dependency_reviewed':n in deps,
   'first_match_excerpt':lines[loc[0]-1][:240] if loc else 'Generic generation/validation dependency reviewed; no lexical hit required.',
   'disposition':disposition,'decision':decision,'next_action':action,'changed_in_B1':False})
 return {'schema':'riskium-riskcase-pinned-impact-inventory-1','source_commit':PIN,'tracked_files':len(entries),'utf8_text_files':text_count,'non_utf8_files':binary,
  'direct_case_match_files':direct_count,'admission_term_match_files':term_count,'inventory_files':len(rows),'files':rows,
  'boundary':'Exhaustive tracked UTF-8 text scan for the stated lexical families, supplemented by reviewed generic dependencies. A lexical hit is not a defect, a required edit, semantic completeness, or a live Pages/Wiki readback. Untracked/private files and binary content are outside this scan.'}
if __name__=='__main__':
 result=build();(HERE/'inventory.json').write_text(dump(result));print(dump({k:v for k,v in result.items() if k not in ('files','non_utf8_files')}))
