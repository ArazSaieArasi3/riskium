"""Freeze the reviewed v0.3.4 exact source; this command never publishes."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

import prepare_stable_release as stable
import release_v034 as release


def finalize(output, receipt, profile, extra):
    release.validate_release_checks(extra)
    receipt['release_specific_checks'] = extra
    receipt['release_tooling_sha256'] = profile['release_tooling_sha256']
    receipt['selected_components'] = 28
    receipt['selected_documentation_snapshots'] = 4
    receipt['preserve_releases'] = ['v0.3.1-rc.'+str(n) for n in range(1,8)] + ['v0.3.1','v0.3.2','v0.3.3']
    receipt['fresh_replay_scope'] += ['SQLite source/scenario 0.4.0', 'SQLite correction lineage 0.5.0',
                                     'SQLite qualified evidence/contextual roles 0.6.0']
    stable.write(Path(output)/'freeze-receipt.json',receipt)
    sums = ''.join(stable.sha(p.read_bytes())+'  '+p.name+'\n' for p in sorted(Path(output).iterdir()) if p.name != 'SHA256SUMS.txt')
    (Path(output)/'SHA256SUMS.txt').write_text(sums)
    return receipt


def freeze(output, root=release.ROOT):
    profile = release.validate_profile(root)
    stable.ensure_clean(root)
    source = stable.git(root,'rev-parse','HEAD').decode().strip()
    freshness = release.live_readback(root,profile)
    checks = stable.run_checks(root)
    extra = []
    for args in release.EXTRA_CHECKS:
        run = subprocess.run([sys.executable,*args],cwd=root,capture_output=True,text=True)
        extra.append(dict(command=['python',*args],exit_code=run.returncode,stdout=run.stdout,stderr=run.stderr))
        release.require(run.returncode == 0,'v0.3.4 release check failed: '+str(args)+'\n'+run.stdout+run.stderr)
    release.validate_release_checks(extra)
    release.require(stable.git(root,'rev-parse','HEAD').decode().strip() == source,'Source changed during v0.3.4 freeze')
    release.validate_profile(root)
    receipt = stable.package(root,output,profile,checks,freshness,
                             profile_resolver=release.profile_path,freshness_validator=release.validate_freshness)
    return finalize(output,receipt,profile,extra)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check-profile',action='store_true')
    args = parser.parse_args()
    if args.check_profile:
        release.validate_profile()
        print(json.dumps(dict(status='V034_REVIEWED_PROFILE_PASS',tag=release.TAG,publication_executed=False)))
        return
    if not args.output:
        parser.error('--output is required unless --check-profile is used')
    receipt = freeze(args.output)
    print(json.dumps(dict(status='V034_EXACT_SOURCE_FROZEN',tag=release.TAG,source_commit=receipt['source_commit'],
        passed_checks=receipt['passed_checks'],release_specific_checks=len(receipt['release_specific_checks']),
        selected_components=28,selected_documentation_snapshots=4,clean_exact_head=True,
        archive_inventory_verified=True,publication_executed=False)))


if __name__ == '__main__':
    main()
