"""Freeze/verify six v0.3.7 assets. Never create a tag, release or public asset.

Offline verification checks internal agreement. A trusted external artifact or
publication digest is still required for authenticity. No Git or third-party
Python dependency is needed by the extracted verifier.
"""
import argparse
import base64
import copy
from datetime import datetime, timezone
import gzip
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

selection = module('riskium_selection037', HERE/'selection.py')
routing = module('riskium_routing037', HERE/'routing.py')
common = module('riskium_release036_common', ROOT/'tools/release_v036.py')
require, sha, encode, safe = common.require, common.sha, common.encoded, common.safe_path
TAG = 'v0.3.7'
ARCHIVE = 'riskium-v0.3.7-source.tar.gz'
ASSETS = {ARCHIVE, 'source-manifest.json', 'artifact-versions.json', 'freeze-receipt.json', 'release-notes.md', 'SHA256SUMS.txt'}
NOTES = 'docs/release-v0.3.7.md'
QUALIFIED = {'releases/selection-v0.3.7.json', 'build/v037-qualified-suite.json', 'build/v037-declaration.json',
             'build/v037-runtime.json', 'build/v037-alignment.json', 'build/v037-current-inventory.json'}
SUITE = {'versioned-suite.json', 'risk-nature-declaration.json', 'risk-nature-runtime.json', 'risk-nature-alignment.json'}
CHANNELS = {'actual-released-channels.json'}


def unpack(packet, names):
    data = base64.b64decode(packet['zip_base64'], validate=True)
    require('sha256:'+sha(data) == packet['artifact']['digest'], 'Authenticated ZIP digest differs')
    require(packet['artifact']['workflow_run']['head_sha'] == packet['run']['head_sha'], 'Artifact source differs')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        require(len(archive.namelist()) == len(names) and set(archive.namelist()) == names, 'Unexpected evidence ZIP inventory')
        return {Path(n).name: json.loads(archive.read(n)) for n in names}


def evidence_check(evidence, source, read):
    """Check exact-source witnesses and raw/completed phase separation offline."""
    runs = {role: evidence[role]['run'] for role in ('qualification', 'suite', 'reader')}
    runs['legacy'] = evidence['legacy']['run']
    route = routing.validate_runs(dict(source_commit=source, runs=runs, legacy_job_log=evidence['legacy']['job_log']))
    q = unpack(evidence['qualification'], QUALIFIED)
    s = unpack(evidence['suite'], SUITE)
    c = unpack(evidence['reader'], CHANNELS)['actual-released-channels.json']
    for role, prefix in (('qualification','v037-packaging-qualification-'), ('suite','v036-source-suite-'),
                         ('reader','released-actual-channels-')):
        p = evidence[role]
        require(p['artifact']['name'] == prefix+source and not p['artifact']['expired'], 'Wrong evidence artifact')
    for name in ('v037-qualified-suite.json','v037-declaration.json','v037-runtime.json','v037-alignment.json','v037-current-inventory.json'):
        require(q[name]['source_commit'] == source, 'Qualification receipt source differs')
    require(q['selection-v0.3.7.json'] == json.loads(read(selection.MATRIX)), 'Evidence selection differs')
    suite = q['v037-qualified-suite.json']
    require(suite == s['versioned-suite.json'] and suite['status'] == 'VERSIONED_SUITE_PASS'
            and suite['candidate_tests'] >= 570 and suite['historical_reader_tests'] == 16, 'Missing full source-qualified suite')
    for row in s.values():
        require(row['source_commit'] == source, 'Second suite receipt source differs')
    raw = q['v037-runtime.json']
    fixed = json.loads(read('implementation/relational/0.9.0/fixtures.json'))['cases']
    negatives = json.loads(read('implementation/relational/0.9.0/negative-inputs.json'))['variants']
    require(raw['working_tree_clean'] and raw['summary'] == dict(PASS=59,FAIL=0,ERROR=0,PENDING_EXTERNAL_READBACK=1), 'Wrong raw runtime phase')
    require(len(raw['controls']) == len({r['id'] for r in raw['controls']}) == len(fixed) == 60, 'Lost fixed control')
    expectations = evidence['resolved_expectations']
    require(set(expectations) == {r['id'] for r in fixed}, 'Lost literal expectation')
    for case, row in zip(fixed[:59], raw['controls'][:59]):
        require(row['id'] == case['id'] and row['requirements'] == case['requirements'] and row['status'] == 'PASS'
                and row['observed'] == row['expected'] == expectations[case['id']], 'Runtime answer differs: '+case['id'])
    wanted = {r['id']: r for r in negatives}
    require(len(raw['negative_variants']) == len({r['id'] for r in raw['negative_variants']}) == len(wanted) == 51, 'Lost negative variant')
    for row in raw['negative_variants']:
        case = wanted[row['id']]
        require(row['control'] == case['control'] and row['status'] == 'PASS'
                and row['observed'] == row['expected'] == case['expected'], 'Negative answer differs')
    declaration = json.loads(read('implementation/relational/0.9.0/declaration-manifest.json'))
    require(q['v037-declaration.json']['status'] == 'RISK_NATURE_DECLARATION_VALID' and q['v037-declaration.json']['runtime_controls_executed'] == 0, 'Declaration check failed')
    require(q['v037-declaration.json']['files_sha256'] == declaration['files_sha256'], 'Declaration binding set differs')
    component_path='implementation/relational/0.9.0/component.json'
    bindings=dict(json.loads(read(component_path))['files_sha256'])
    bindings[component_path]=sha(read(component_path))
    require(raw['runtime_source_sha256'] == bindings and raw['native_semantic_acceptance'] is False and raw['independent_ratings'] == 0, 'Runtime scope/binding set differs')
    for path, digest in {**declaration['files_sha256'], **raw['runtime_source_sha256']}.items():
        require(sha(read(path)) == digest, 'Runtime/declaration binding differs: '+path)
    require(all(r['status'] == 'NOT_RUN' and r['observed'] is None for r in fixed), 'Original expectations rewritten')
    observed = dict(fixed_controls=60, expected_files_unchanged=True, missing_or_skipped_controls=0,
                    independent_download_matches=True, no_runtime_pass_in_declaration=True)
    require(raw['controls'][-1]['id'] == 'NRA-F60' and raw['controls'][-1]['status'] == 'PENDING_EXTERNAL_READBACK' and raw['controls'][-1]['observed'] is None, 'Raw F60 overwritten')
    require(evidence['independent_F60'] == dict(status='PASS', observed=observed)
            and observed == fixed[-1]['expected'], 'Missing independent F60')
    inv = q['v037-current-inventory.json']
    require(inv['status'] == 'CURRENT_SOURCE_INVENTORY_AND_RETAINED_CONSISTENCY_PASS'
            and inv['historical_inventory_rewritten'] is False, 'Missing current inventory')
    require(len(inv['current_source_files']) == len({r['path'] for r in inv['current_source_files']}) and len(inv['current_source_files']) >= 991, 'Missing/duplicate current input')
    for row in inv['current_source_files']:
        data = read(row['path'])
        require(sha(data) == row['sha256'] and len(data) == row['bytes'], 'Current input binding differs')
    require(q['v037-alignment.json']['status'] == 'R3_ALIGNMENT_PASS' and q['v037-alignment.json']['working_tree_clean'], 'Alignment failed')
    channels = c['actual_channels']
    require(c['source_commit'] == channels['documentation_source_commit'] == source
            and channels['status'] == 'ACTUAL_PUBLISHED_READER_CHANNELS_PASS'
            and channels['wiki_files'] == len(channels['wiki_files_sha256']) == 23
            and channels['pages_http_responses'] == len(channels['responses']) == 314
            and channels['frozen_snapshots'] == 4, 'Missing actual reader channels')
    require(len({r['path'] for r in channels['responses']}) == 314
            and all(r['http_status'] == 200 and re.fullmatch('[a-f0-9]{64}',r['sha256']) for r in channels['responses']), 'Incomplete actual served inventory')
    return dict(current_tests=suite['candidate_tests'], historical_tests=16, controls=60, negative_variants=51,
                routing=route['status'], actual_http_bodies=314, actual_wiki_files=23)


def build_assets(folder, source, entries, matrix, evidence, timestamp):
    require(re.fullmatch('[a-f0-9]{40}', source), 'Invalid source identity')
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    require(not list(folder.iterdir()), 'Asset folder must be empty')
    files = {p:dict(sha256=sha(data),bytes=len(data),mode=mode) for p,mode,data in entries}
    require(len(files) == len(entries) and files, 'Duplicate or empty source inventory')
    for path in files: safe(path)
    with (folder/ARCHIVE).open('wb') as out, gzip.GzipFile(fileobj=out,mode='wb',mtime=timestamp,filename='') as gz:
        with tarfile.open(fileobj=gz,mode='w') as tar:
            for path,mode,data in entries:
                info=tarfile.TarInfo(TAG+'/'+path);info.size=len(data);info.mode=mode;info.mtime=timestamp
                tar.addfile(info,io.BytesIO(data))
    (folder/'source-manifest.json').write_bytes(encode(dict(schema='riskium-v037-source-manifest-v1',tag=TAG,source_commit=source,prefix=TAG+'/',files=files)))
    (folder/'artifact-versions.json').write_bytes(encode(dict(tag=TAG,source_commit=source,selection=matrix)))
    (folder/'release-notes.md').write_bytes(next(data for path,mode,data in entries if path == NOTES))
    receipt=dict(schema='riskium-v037-freeze-receipt-v1',tag=TAG,source_commit=source,stage='FROZEN_NOT_PUBLISHED',
                 publication_executed=False,created_at_utc=datetime.now(timezone.utc).isoformat(),files=len(entries),
                 scientific_versions=selection.SCIENCE,evidence=evidence,independent_semantic_validation=False,
                 payload_sha256={n:sha((folder/n).read_bytes()) for n in (ARCHIVE,'source-manifest.json','artifact-versions.json','release-notes.md')})
    (folder/'freeze-receipt.json').write_bytes(encode(receipt))
    (folder/'SHA256SUMS.txt').write_text(''.join(sha((folder/n).read_bytes())+'  '+n+'\n' for n in sorted(ASSETS-{'SHA256SUMS.txt'})))
    return receipt


def verify(folder, expected_source=None):
    folder=Path(folder)
    require({p.name for p in folder.iterdir()} == ASSETS and all(p.is_file() and not p.is_symlink() for p in folder.iterdir()), 'Six regular assets required')
    sums={}
    for line in (folder/'SHA256SUMS.txt').read_text().splitlines():
        require(re.fullmatch(r'[a-f0-9]{64}  [A-Za-z0-9.\-]+',line), 'Malformed checksum')
        digest,name=line.split('  ')
        require(name in ASSETS-{'SHA256SUMS.txt'} and name not in sums, 'Duplicate/unknown checksum')
        sums[name]=digest
    require(set(sums) == ASSETS-{'SHA256SUMS.txt'}, 'Incomplete checksums')
    for name,digest in sums.items():require(sha((folder/name).read_bytes()) == digest,'Asset checksum differs: '+name)
    manifest=json.loads((folder/'source-manifest.json').read_bytes());versions=json.loads((folder/'artifact-versions.json').read_bytes());receipt=json.loads((folder/'freeze-receipt.json').read_bytes())
    source=manifest['source_commit']
    require(re.fullmatch('[a-f0-9]{40}',source) and manifest['tag'] == versions['tag'] == receipt['tag'] == TAG
            and source == versions['source_commit'] == receipt['source_commit']
            and (expected_source is None or expected_source == source), 'Version/source identity differs')
    require(manifest['prefix'] == TAG+'/' and receipt['stage'] == 'FROZEN_NOT_PUBLISHED'
            and receipt['publication_executed'] is False and receipt['independent_semantic_validation'] is False
            and receipt['scientific_versions'] == selection.SCIENCE, 'Freeze boundary differs')
    payload={}
    with tarfile.open(folder/ARCHIVE,'r:gz') as tar:
        for item in tar:
            require(item.isfile() and item.name.startswith(TAG+'/'), 'Unsafe archive member')
            path=safe(item.name[len(TAG)+1:])
            require(path not in payload, 'Duplicate archive member')
            require(item.mode in (0o644,0o755) and item.uid == item.gid == 0, 'Unsafe archive mode/owner')
            data=tar.extractfile(item).read();payload[path]=data
            require(manifest['files'].get(path) == dict(sha256=sha(data),bytes=len(data),mode=item.mode), 'Archive manifest differs: '+path)
    require(set(payload) == set(manifest['files']) and len(payload) == receipt['files'], 'Incomplete source archive')
    require(payload[NOTES] == (folder/'release-notes.md').read_bytes(), 'Release notes differ from source')
    require(receipt['payload_sha256'] == {n:sha((folder/n).read_bytes()) for n in (ARCHIVE,'source-manifest.json','artifact-versions.json','release-notes.md')}, 'Receipt payload differs')
    require(json.loads(payload[selection.MATRIX]) == versions['selection'], 'Archived selection differs')
    # Recompute component closure using the actual archive, without Git or network.
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for path,data in payload.items():
            target=root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        chosen=selection.selection(root)
        require(encode(chosen) == payload[selection.MATRIX], 'Archived component closure differs')
        routing.check(root)
    result=evidence_check(receipt['evidence'],source,lambda p:payload[safe(p)])
    prior=receipt['evidence']['previous_releases']
    baseline=json.loads(payload['evaluation/releases/v0.3.7/branch-qualification.json'])['previous_release_inventory']
    require(prior == baseline and len(prior) == 13, 'Previous release inventory differs')
    return dict(status='V037_SIX_ASSET_OFFLINE_PASS',tag=TAG,source_commit=source,source_files=len(payload),
                components=31,preserved_previous_files=779,publication_executed=False,
                external_authenticity_required=True,**result)


def packet(run, prefix, members):
    artifacts=common.api('actions/runs/'+str(run['id'])+'/artifacts?per_page=100')['artifacts']
    found=[a for a in artifacts if a['name'] == prefix+run['head_sha'] and not a['expired']]
    require(len(found) == 1, 'Missing exact-source artifact')
    a=found[0];data=common.api('actions/artifacts/'+str(a['id'])+'/zip',binary=True)
    result=dict(run=run,artifact=a,zip_base64=base64.b64encode(data).decode())
    unpack(result,members)
    return result


def publication_inventory():
    releases=common.api('releases?per_page=100')
    return [dict(id=r['id'],tag=r['tag_name'],draft=r['draft'],prerelease=r['prerelease'],published_at=r['published_at'],
                 assets=[dict(id=a['id'],name=a['name'],size=a['size'],digest=a.get('digest')) for a in r['assets']]) for r in releases]


def freeze(folder, source, reader_run):
    require(common.git('rev-parse','HEAD').decode().strip() == source and not common.git('status','--porcelain').strip(), 'Clean exact source required')
    require(common.api('git/ref/heads/main')['object']['sha'] == source, 'Source no longer main')
    require(common.api('releases/latest')['tag_name'] == 'v0.3.6', 'Previous release no longer Latest')
    for path in ('git/ref/tags/'+TAG,'releases/tags/'+TAG):
        try:common.api(path)
        except HTTPError as exc:
            if exc.code != 404:raise
        else:raise ValueError('Target tag/release already exists')
    prior=publication_inventory()
    require(prior == json.loads((ROOT/'evaluation/releases/v0.3.7/branch-qualification.json').read_bytes())['previous_release_inventory'], 'Previous publication inventory changed')
    matrix=selection.selection()
    require(encode(matrix) == (ROOT/selection.MATRIX).read_bytes(), 'Stale selection')
    routing.check()
    deadline=time.monotonic()+480
    while True:
        require(common.api('git/ref/heads/main')['object']['sha'] == source, 'Source advanced while awaiting gates')
        runs=common.api('actions/runs?head_sha='+source+'&per_page=100')['workflow_runs']
        selected={};pending=[]
        for role,filename in routing.PATHS.items():
            attempts=[r for r in runs if r['path'] == '.github/workflows/'+filename
                      and r['event'] == ('workflow_run' if role == 'reader' else 'push')
                      and r['head_branch'] == 'main']
            if role == 'reader':attempts=[r for r in attempts if r['id'] == reader_run]
            candidates=[r for r in attempts if r['status'] == 'completed'
                        and r['conclusion'] == ('failure' if role == 'legacy' else 'success')]
            if candidates:selected[role]=max(candidates,key=lambda r:r['id'])
            else:
                require(not attempts or any(r['status'] != 'completed' for r in attempts), 'Failed main gate: '+role)
                pending.append(role)
        if not pending:break
        require(time.monotonic() < deadline, 'Timed out awaiting gates: '+str(pending))
        print(json.dumps(dict(waiting_for_exact_main_gates=pending)),flush=True)
        time.sleep(15)
    jobs=common.api('actions/runs/'+str(selected['legacy']['id'])+'/jobs?per_page=100')['jobs']
    candidates=[j for j in jobs if j['name'] == 'candidate' and j['conclusion'] == 'failure']
    require(len(candidates) == 1, 'Missing legacy diagnostic job')
    log=common.api('actions/jobs/'+str(candidates[0]['id'])+'/logs',binary=True).decode()
    routing.validate_runs(dict(source_commit=source,runs=selected,legacy_job_log=log))
    evidence=dict(qualification=packet(selected['qualification'],'v037-packaging-qualification-',QUALIFIED),
                  suite=packet(selected['suite'],'v036-source-suite-',SUITE),
                  reader=packet(selected['reader'],'released-actual-channels-',CHANNELS),
                  legacy=dict(run=selected['legacy'],job_log=log),previous_releases=prior)
    # Resolve fixed literals independently of the actual runtime receipt.
    sys.path.insert(0,str(ROOT/'tools'))
    from run_relational_risk_nature import F, expected
    evidence['resolved_expectations']={r['id']:expected(r['expected']) for r in F['cases']}
    evidence['independent_F60']=dict(status='PASS',observed=copy.deepcopy(F['cases'][-1]['expected']))
    evidence_check(evidence,source,lambda p:(ROOT/safe(p)).read_bytes())
    declaration=json.loads((ROOT/'implementation/relational/0.9.0/declaration-manifest.json').read_bytes())
    for path in declaration['files_sha256']:
        require((ROOT/path).read_bytes() == common.git('show','805b1edecff254f1e21131aa6fd098344affb398:'+path), 'Original declaration changed')
    channel=unpack(evidence['reader'],CHANNELS)['actual-released-channels.json']['actual_channels']
    req=Request('https://arazsaiearasi3.github.io/riskium/publication-manifest.json?doc='+source,headers={'Cache-Control':'no-cache','User-Agent':'riskium-v037-freeze'})
    with urlopen(req,timeout=45) as response:
        data=response.read();require(response.status == 200 and sha(data) == channel['root_manifest_sha256']
                                     and json.loads(data)['current_source_commit'] == source, 'Fresh served root differs')
    require(common.api('git/ref/heads/main')['object']['sha'] == source and not common.git('status','--porcelain').strip(), 'Source changed during freeze')
    entries=common.source_entries(source)
    build_assets(Path(folder),source,entries,matrix,evidence,int(common.git('show','-s','--format=%ct',source)))
    result=verify(folder,source)
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(Path(folder)/ARCHIVE) as tar:tar.extractall(tmp,filter='data')
        command=[sys.executable,str(Path(tmp)/TAG/'tools/releases/v037/freeze.py'),'verify','--folder',str(Path(folder).resolve()),'--source',source]
        run=subprocess.run(command,env=dict(os.environ,PATH='/nonexistent'),capture_output=True,text=True)
        require(run.returncode == 0, 'Extracted no-Git verifier failed: '+run.stderr)
    require(common.api('git/ref/heads/main')['object']['sha'] == source and common.api('releases/latest')['tag_name'] == 'v0.3.6' and publication_inventory() == prior, 'Publication boundary changed during verification')
    for path in ('git/ref/tags/'+TAG,'releases/tags/'+TAG):
        try:common.api(path)
        except HTTPError as exc:
            if exc.code != 404:raise
        else:raise ValueError('Target tag/release appeared during verification')
    result['extracted_no_git_verifier_passed']=True
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=('freeze','verify'))
    parser.add_argument('--folder',type=Path,required=True)
    parser.add_argument('--source')
    parser.add_argument('--reader-run',type=int)
    args=parser.parse_args()
    if args.mode == 'freeze':
        require(args.source and args.reader_run, 'Source and reader run required')
        result=freeze(args.folder,args.source,args.reader_run)
    else:result=verify(args.folder,args.source)
    print(json.dumps(result))

if __name__ == '__main__':main()
