"""Qualify an exact v0.3.7 source without mixing historical reader contracts."""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def main():
 p=argparse.ArgumentParser();p.add_argument('--list',action='store_true');p.add_argument('--receipt',type=Path,default=Path('build/v037-qualified-suite.json'));a=p.parse_args()
 if a.list:
  subprocess.run([sys.executable,'tools/run_v036_versioned_suite.py','--list'],cwd=ROOT,check=True);return
 if subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip():raise ValueError('Qualification requires a clean committed source')
 subprocess.run([sys.executable,'tools/run_v036_versioned_suite.py','--receipt',str(a.receipt.resolve())],cwd=ROOT,check=True)
 receipt=json.loads(a.receipt.read_text())
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 if receipt['source_commit']!=head or receipt['status']!='VERSIONED_SUITE_PASS' or receipt['historical_reader_tests']!=16:raise ValueError('Wrong source-qualified receipt')
 print(json.dumps(dict(status='V037_SOURCE_QUALIFIED',source=head,release_published=False,freeze_completed=False)))
if __name__=='__main__':main()
