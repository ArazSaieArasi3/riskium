"""Freeze the explicit owner-accepted stable profile; never publish from this tool."""
import argparse
from collections import Counter
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile

from prepare_incremental_release import CHECKS, git, run_checks
import check_release_alignment as alignment

ROOT = Path(__file__).resolve().parents[1]
PROFILE = 'releases/stable-profile-v0.3.1.json'
REQUEST = 'releases/stable-request.json'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(root, path):
    return json.loads((Path(root) / path).read_bytes())


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def ensure_clean(root, ref='HEAD'):
    require(not git(root, 'status', '--porcelain').strip(), 'Stable freeze requires a clean source checkout')
    require(git(root, 'rev-parse', ref + '^{commit}') == git(root, 'rev-parse', 'HEAD'), 'Stable freeze must evaluate exact HEAD')


def validate_profile(root):
    root = Path(root)
    p = read(root, PROFILE)
    model = read(root, 'ontology/riskium-model.json')
    require(p['profile'] == 'stable-bounded-research-artifact', 'Wrong stable maturity profile')
    require(re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+', p['tag']) and p['tag'] == 'v' + model['version'] == 'v0.3.1', 'Stable tag/model mismatch')
    require(p['model_version'] == model['version'], 'Stable model version mismatch')
    require(p['orsd_revision'] == '0.4.3' and p['manuscript_version'] == '7.0.8', 'Unreviewed artifact version')
    for flag in ('publication_requires_clean_exact_head', 'publication_requires_all_checks',
                 'publication_requires_no_known_unresolved_critical_findings', 'publication_requires_new_tag_and_release', 'readback_required'):
        require(p.get(flag) is True, 'Missing stable gate: ' + flag)
    require(p['independent_validation_claimed'] is False and p['full_original_requirement_acceptance_claimed'] is False, 'Unsupported scientific maturity claim')
    accepted = read(root, p['accepted_scope'])
    owner = read(root, 'evaluation/owner-review/register.json')
    require(accepted['model_version'] == p['model_version'] and accepted['orsd_revision'] == p['orsd_revision'] and accepted['manuscript_version'] == p['manuscript_version'], 'Unaccepted stable scope')
    require(owner['ratings_recorded'] == 11 and Counter(r['owner_rating'] for r in owner['rows']) == {'ACCEPT_SCOPED': 9, 'REVISE_BEFORE_FINAL': 1, 'HOLD_UNTIL_FINAL_FREEZE': 1}, 'Missing explicit scoped/revision/conditional owner decisions')
    screen = read(root, p['critical_screen'])
    require(screen['target'] == p['tag'] and screen['reviewed_scope_commit'] == p['reviewed_scope_commit'], 'Critical screen version mismatch')
    require(screen['known_unresolved_critical_findings'] == [], 'Unresolved critical finding blocks release')
    require(screen['material_scientific_change_since_owner_acceptance'] is False and screen['new_owner_responses_generated'] == 0, 'Unreviewed scientific change or fabricated owner response')
    require(screen['universal_zero_defect_claimed'] is False and screen['independent_semantic_review_claimed'] is False, 'Invalid zero-defect or independence claim')
    # Exact owner-approved scientific/artifact inputs cannot change behind a new package tag.
    for component in read(root, p['artifact_matrix'])['artifacts']:
        for file in component['files']:
            require((root / file['path']).read_bytes() == git(root, 'show', p['reviewed_scope_commit'] + ':' + file['path']), 'Accepted artifact changed: ' + file['path'])
    for row in screen['reviewed_risks']:
        require(row['retained_evidence'] and row['fresh_gate'], 'Unexplained critical-screen route')
        for path in row['retained_evidence']:
            require((root / path).is_file(), 'Missing retained evidence: ' + path)
    citation = (root / 'CITATION.cff').read_text()
    require(re.search(r'^version: \"0\.3\.1\"$', citation, re.M) and re.search(r'^url: \"https://github\.com/ArazSaieArasi3/riskium/releases/tag/v0\.3\.1\"$', citation, re.M), 'Final citation designation missing')
    require((root / p['notes']).is_file(), 'Missing reviewed stable release notes')
    alignment.check(root)
    return p


def validate_checks(checks):
    require(len(checks) == len(CHECKS) and bool(checks), 'Missing final checks')
    require([c['command'] for c in checks] == [['python', *args] for args in CHECKS], 'Wrong final check set/order')
    require(all(c['exit_code'] == 0 for c in checks), 'Failed final check')


def resolve_intent(root, event, ref, before, after, inputs=None):
    inputs = inputs or {}
    request = None
    if event == 'workflow_dispatch' and inputs.get('publish') in (True, 'true'):
        request = {'profile': 'stable-bounded-research-artifact', 'tag': inputs.get('release_tag'), 'publish': True}
    elif event == 'push' and ref == 'refs/heads/main' and re.fullmatch(r'[0-9a-f]{40}', before or '') and set(before) != {'0'}:
        paths = git(root, 'diff', '--name-only', before, after, '--', REQUEST).decode().splitlines()
        if REQUEST in paths:
            request = json.loads(git(root, 'show', after + ':' + REQUEST))
    if request is None or request.get('publish') is False:
        return {'publish': False, 'release_tag': ''}
    require(request.get('publish') is True and request.get('profile') == 'stable-bounded-research-artifact', 'Explicit stable intent required')
    require(ref == 'refs/heads/main' and request.get('tag') == 'v0.3.1', 'Stable publication requires v0.3.1 on main')
    require(git(root, 'rev-parse', after + '^{commit}').strip().decode() == after, 'Stable intent must name an exact commit')
    return {'publish': True, 'release_tag': request['tag']}


def package(root, output, profile, checks):
    root, output = Path(root), Path(output)
    ensure_clean(root)
    validate_checks(checks)
    require(not output.resolve().is_relative_to(root.resolve()), 'Keep stable package outside the source checkout')
    output.mkdir(parents=True, exist_ok=True)
    require(not any(output.iterdir()), 'Never overwrite an existing stable package')
    commit = git(root, 'rev-parse', 'HEAD').decode().strip()
    tag = profile['tag']
    files, entries = [], []
    for record in git(root, 'ls-tree', '-r', '-z', commit).split(b'\0'):
        if not record:
            continue
        header, path = record.split(b'\t', 1)
        mode, kind, blob = header.split()
        path = path.decode()
        require(kind == b'blob' and mode in (b'100644', b'100755'), 'Only regular tracked source files are allowed')
        data = git(root, 'cat-file', 'blob', blob.decode())
        files.append((path, int(mode, 8) & 0o777, data))
        entries.append({'path': path, 'bytes': len(data), 'sha256': sha(data)})
    archive = output / ('riskium-' + tag + '-source.tar.gz')
    with archive.open('wb') as raw, gzip.GzipFile(fileobj=raw, filename='', mode='wb', mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode='w') as tar:
            for path, mode, data in files:
                item = tarfile.TarInfo('riskium-' + tag + '/' + path)
                item.mode, item.size, item.mtime = mode, len(data), 0
                tar.addfile(item, io.BytesIO(data))
    with tarfile.open(archive) as tar:
        inventory = [{'path': m.name.split('/', 1)[1], 'bytes': m.size, 'sha256': sha(tar.extractfile(m).read())} for m in tar]
    require(inventory == entries, 'Stable archive inventory mismatch')
    manifest = {'schema': 'riskium-stable-source-inventory-v1', 'tag': tag, 'source_commit': commit,
                'file_count': len(entries), 'files': entries, 'scope': 'Tracked public source only; author-facing manuscripts/private historical databases excluded.'}
    write(output / 'source-manifest.json', manifest)
    matrix = read(root, profile['artifact_matrix'])
    write(output / 'artifact-versions.json', {'schema': 'riskium-frozen-artifact-versions-v1', 'source_commit': commit, 'tag': tag,
                                              'matrix_sha256': sha((root / profile['artifact_matrix']).read_bytes()), 'matrix': matrix})
    freeze = {'schema': 'riskium-stable-freeze-v1', 'tag': tag, 'source_commit': commit,
              'model_version': profile['model_version'], 'maturity': profile['profile'], 'clean_exact_head': True,
              'profile_sha256': sha((root / PROFILE).read_bytes()),
              'critical_screen_sha256': sha((root / profile['critical_screen']).read_bytes()),
              'critical_screen_kind': 'Bounded release-engineering review of accepted scope; no universal zero-defect assertion',
              'known_unresolved_critical_findings': [], 'archive_inventory_verified': True,
              'checks': checks, 'passed_checks': len(checks),
              'artifact_scope_alignment': 'PASS', 'accepted_publication_condition': 'TECHNICAL_FREEZE_GATES_SATISFIED_BEFORE_PUBLICATION',
              'owner_decision_source': 'evaluation/owner-review/register.json; explicit 24 October 2026 scoped review',
              'new_owner_responses_generated': 0, 'independent_validation': False,
              'historical_outcomes_preserved': {'HermiT': {'PASS': 281, 'NOT_RUN': 14}, 'SHACL': {'PASS': 341, 'PARTIAL': 1, 'NOT_RUN': 17}},
              'fresh_replay_scope': ['C-08 metadata compatibility', 'C-13/C-18 selected comparison', 'SQLite identity/history', 'CQ06 source trace', 'CQ07/CQ08 correction and withheld identity', 'Shared-graph selected-task integration', 'SQLite assessment/result 0.2.0 fixed and seeded controls, schema audit and declared synthetic workloads'],
              'retained_historical_engine_scope': 'The unchanged full HermiT and early SHACL receipts are not claimed as new full engine executions at this freeze.',
              'publication_executed': False, 'downloaded_final_readback': 'Required after publication in a separate job'}
    write(output / 'freeze-receipt.json', freeze)
    notes = (root / profile['notes']).read_text() + '\n\nExact frozen source commit: `' + commit + '`.\n'
    (output / 'release-notes.md').write_text(notes)
    sums = ''.join(sha(p.read_bytes()) + '  ' + p.name + '\n' for p in sorted(output.iterdir()) if p.is_file())
    (output / 'SHA256SUMS.txt').write_text(sums)
    return freeze


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check-profile', action='store_true')
    args = parser.parse_args()
    profile = validate_profile(ROOT)
    if args.check_profile:
        print(json.dumps({'status': 'STABLE_PROFILE_REVIEW_MATCHED', 'tag': profile['tag'], 'publication_executed': False}))
        return
    require(args.output is not None, 'Stable freeze requires an output folder')
    ensure_clean(ROOT)
    checks = run_checks(ROOT)
    freeze = package(ROOT, args.output, profile, checks)
    print(json.dumps({k: freeze[k] for k in ('tag', 'source_commit', 'passed_checks', 'clean_exact_head', 'archive_inventory_verified', 'publication_executed')}))


if __name__ == '__main__':
    main()
