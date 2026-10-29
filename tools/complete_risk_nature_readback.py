"""Finish control 60 only after an independent hosted artifact download."""
import argparse
from datetime import datetime,timezone
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

import relational_risk_nature as x
from run_relational_risk_nature import expected,F


def complete(archive,expected_digest,artifact_id,run_id):
    data=archive.read_bytes()
    if hashlib.sha256(data).hexdigest()!=expected_digest:raise ValueError('Hosted ZIP digest differs from trusted metadata')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        if set(z.namelist())!={'versioned-suite.json','risk-nature-declaration.json','risk-nature-runtime.json'}:raise ValueError('Unexpected artifact inventory')
        suite=json.loads(z.read('versioned-suite.json'));declaration=json.loads(z.read('risk-nature-declaration.json'));report=json.loads(z.read('risk-nature-runtime.json'))
    source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=x.ROOT,text=True).strip()
    if not (suite['source_commit']==declaration['source_commit']==report['source_commit']==source):raise ValueError('Source-qualified receipts differ')
    if suite['status']!='VERSIONED_SUITE_PASS' or suite['candidate_tests']<550 or suite['historical_reader_tests']!=12:raise ValueError('Missing full suite')
    if not report['working_tree_clean']:raise ValueError('Hosted runtime source was dirty')
    if len(report['controls'])!=60 or len({r['id'] for r in report['controls']})!=60:raise ValueError('Lost runtime controls')
    if len(report['negative_variants'])!=51 or any(r['status']!='PASS' or r['observed']!=r['expected'] for r in report['negative_variants']):raise ValueError('Negative variants incomplete')
    for case,actual in zip(F['cases'][:59],report['controls'][:59]):
        if case['id']!=actual['id'] or actual['status']!='PASS' or actual['observed']!=expected(case['expected']):raise ValueError('Runtime answer differs: '+case['id'])
    if report['controls'][-1]['id']!='NRA-F60' or report['controls'][-1]['status']!='PENDING_EXTERNAL_READBACK':raise ValueError('Readback must be separate')
    x.bindings()
    for path,digest in report['runtime_source_sha256'].items():
        if x.sha((x.ROOT/path).read_bytes())!=digest:raise ValueError('Hosted runtime binding differs: '+path)
    for path,digest in declaration['files_sha256'].items():
        if x.sha((x.ROOT/path).read_bytes())!=digest:raise ValueError('Hosted declaration differs: '+path)
    for path in declaration['files_sha256']:
        if (x.ROOT/path).read_bytes()!=subprocess.check_output(['git','show','805b1edecff254f1e21131aa6fd098344affb398:'+path],cwd=x.ROOT):raise ValueError('Original expected file changed: '+path)
    observed=dict(fixed_controls=len(report['controls']),expected_files_unchanged=True,missing_or_skipped_controls=sum(r['status']!='PASS' for r in report['controls'][:59]),independent_download_matches=True,no_runtime_pass_in_declaration=all(r['status']=='NOT_RUN' and r['observed'] is None for r in F['cases']))
    if observed!=F['cases'][-1]['expected']:raise ValueError('External control differs')
    report['controls'][-1].update(observed=observed,status='PASS',details=dict(phase='INDEPENDENT_HOSTED_ARTIFACT_DOWNLOAD_VERIFIED',artifact_id=artifact_id,run_id=run_id,zip_bytes=len(data),zip_sha256=expected_digest))
    report['summary']=dict(PASS=60,FAIL=0,ERROR=0,PENDING_EXTERNAL_READBACK=0)
    report['independent_readback']=dict(observed_at=datetime.now(timezone.utc).isoformat(),artifact_id=artifact_id,run_id=run_id,zip_bytes=len(data),zip_sha256=expected_digest,suite=suite,declaration=declaration)
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--artifact',type=Path,required=True);p.add_argument('--expected-zip-sha256',required=True);p.add_argument('--artifact-id',type=int,required=True);p.add_argument('--run-id',type=int,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    result=complete(args.artifact,args.expected_zip_sha256,args.artifact_id,args.run_id);args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(source=result['source_commit'],summary=result['summary'],negative_variants=51,independent_download=True)))
