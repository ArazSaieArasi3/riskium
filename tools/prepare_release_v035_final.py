"""Freeze exact v0.3.5 source after trusted candidate and fresh channel checks.

This command only prepares six local staged assets. It never publishes a tag,
release or asset. Public package helpers also support temporary software fixtures;
only freeze() performs the real clean-source/candidate/channel execution path.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import zipfile

# Do not add generated Python files to a source tree while checking it.
sys.dont_write_bytecode = True
import release_v035_final as release

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://arazsaiearasi3.github.io/riskium/'
WIKI = 'https://github.com/ArazSaieArasi3/riskium.wiki.git'
REPO = 'ArazSaieArasi3/riskium'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def write(path, value):
    Path(path).write_bytes(encoded(value))


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def ensure_clean(root, source=None):
    require(not git(root, 'status', '--porcelain').strip(), 'V035-FREEZE-DIRTY-SOURCE')
    current = git(root, 'rev-parse', 'HEAD').decode().strip()
    require(re.fullmatch('[a-f0-9]{40}', current), 'V035-FREEZE-SOURCE')
    if source is not None:
        require(current == source, 'V035-FREEZE-SOURCE-CHANGED')
    return current


def source_entries(root, source):
    """Read the immutable committed public tree, rejecting nonregular entries."""
    entries = []
    for record in git(root, 'ls-tree', '-r', '-z', source).split(b'\0'):
        if not record:
            continue
        header, raw_path = record.split(b'\t', 1)
        mode, kind, ident = header.split()
        path = release.support.safe_path(raw_path.decode())
        require(kind == b'blob' and mode in (b'100644', b'100755'), 'V035-FREEZE-NONREGULAR: ' + path)
        raw = git(root, 'cat-file', 'blob', ident.decode())
        entries.append((path, int(mode, 8) & 0o777, raw))
    require(bool(entries), 'V035-FREEZE-EMPTY-SOURCE')
    return entries


def github_api(path):
    """Read canonical public metadata, authenticating when Actions supplies a token."""
    require(os.environ.get('GITHUB_REPOSITORY', REPO) == REPO
            and os.environ.get('GH_REPO', REPO) == REPO, 'V035-CORE-CANONICAL-REPOSITORY')
    headers = {'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = 'Bearer ' + token
    request = urllib.request.Request('https://api.github.com/repos/' + REPO + '/' + path, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        require(response.status == 200, 'V035-CORE-GITHUB-RESPONSE')
        return release.loads(response.read())


def ensure_remote_main(source, api=None):
    api = api or github_api
    require(api('git/ref/heads/main')['object']['sha'] == source, 'V035-FREEZE-REMOTE-MAIN-ADVANCED')


def validate_remote_candidate(source, run_id, artifact_id, digest, api=None):
    """Authenticate reused checks against actual run/artifact GitHub metadata."""
    api = api or github_api
    require(type(run_id) is int and run_id > 0 and type(artifact_id) is int and artifact_id > 0
            and isinstance(digest, str) and re.fullmatch('[a-f0-9]{64}', digest),
            'V035-CORE-PROVENANCE-REFERENCE')
    run = api('actions/runs/' + str(run_id))
    require(run['id'] == run_id and run['name'] == 'Incremental release candidate'
            and run['path'] == '.github/workflows/incremental-release.yml'
            and run['status'] == 'completed' and run['conclusion'] == 'success'
            and run['event'] in ('push', 'workflow_dispatch') and run['head_branch'] == 'main'
            and run['head_sha'] == source and run['repository']['full_name'] == REPO
            and run['head_repository']['full_name'] == REPO, 'V035-CORE-UNTRUSTED-WORKFLOW')
    artifact = api('actions/artifacts/' + str(artifact_id))
    require(artifact['id'] == artifact_id and artifact['expired'] is False
            and artifact['name'] == 'riskium-candidate-' + source
            and artifact['digest'] == 'sha256:' + digest
            and artifact['workflow_run']['id'] == run_id
            and artifact['workflow_run']['head_sha'] == source
            and artifact['workflow_run']['head_branch'] == 'main', 'V035-CORE-UNTRUSTED-ARTIFACT')
    return dict(schema='riskium-v035-core-evidence-v1', source_commit=source,
        workflow_name='Incremental release candidate', workflow_run_id=run_id,
        artifact_id=artifact_id, artifact_sha256=digest, workflow_conclusion='success',
        github_api_verified=True)


def verify_candidate_zip(candidate_zip, folder, expected_sha256):
    """Bind the consumed candidate receipts to the original downloaded ZIP."""
    folder = Path(folder)
    require(re.fullmatch('[a-f0-9]{64}', expected_sha256 or ''), 'V035-CORE-ARTIFACT-DIGEST')
    raw = Path(candidate_zip).read_bytes()
    require(sha(raw) == expected_sha256, 'V035-CORE-ZIP-DIGEST')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) == 5, 'V035-CORE-ZIP-INVENTORY')
        require(all(Path(p).name == p and p not in ('', '.', '..') for p in names), 'V035-CORE-ZIP-PATH')
        actual = {}
        for path in folder.rglob('*'):
            require(not path.is_symlink(), 'V035-CORE-FOLDER-SYMLINK')
            require(path.is_file(), 'V035-CORE-FOLDER-NONFILE')
            actual[path.relative_to(folder).as_posix()] = path.read_bytes()
        require(set(actual) == set(names), 'V035-CORE-ZIP-FOLDER-SET')
        for name in names:
            require(archive.read(name) == actual[name], 'V035-CORE-ZIP-FOLDER-BYTES: ' + name)
    return expected_sha256


def validate_candidate(folder, root, source):
    """Verify actual candidate checks and every archived byte against Git."""
    folder = Path(folder)
    receipt = json.loads((folder / 'candidate-receipt.json').read_bytes())
    manifest = json.loads((folder / 'source-manifest.json').read_bytes())
    require(receipt['schema'] == 'riskium-incremental-candidate-v1'
            and receipt['source_commit'] == manifest['source_commit'] == source
            and receipt['package_name'] == 'candidate-' + source[:12]
            and receipt['publication_executed'] is False
            and receipt['independent_semantic_acceptance'] == 'NOT_ESTABLISHED'
            and receipt['archive_inventory_verified'] is True, 'V035-CORE-RECEIPT')
    release.validate_checks(receipt['checks'])
    archive_name = 'riskium-candidate-' + source[:12] + '-source.tar.gz'
    expected = {archive_name, 'source-manifest.json', 'candidate-receipt.json', 'release-notes.md'}
    sums = {}
    for line in (folder / 'SHA256SUMS.txt').read_text().splitlines():
        digest, name = line.split('  ', 1)
        require(Path(name).name == name and name not in sums
                and re.fullmatch('[a-f0-9]{64}', digest), 'V035-CORE-SUM-PATH')
        sums[name] = digest
    require(set(sums) == expected and {p.name for p in folder.iterdir()} == expected | {'SHA256SUMS.txt'},
            'V035-CORE-ASSET-INVENTORY')
    for name, digest in sums.items():
        require(sha((folder / name).read_bytes()) == digest, 'V035-CORE-SUM: ' + name)
    committed = source_entries(root, source)
    wanted = [dict(path=p, bytes=len(raw), sha256=sha(raw)) for p, mode, raw in committed]
    require(manifest['schema'] == 'riskium-incremental-inventory-v1'
            and manifest['file_count'] == len(wanted) and manifest['files'] == wanted,
            'V035-CORE-MANIFEST-GIT')
    by_path = {p: (mode, raw) for p, mode, raw in committed}
    seen = set()
    with tarfile.open(folder / archive_name, 'r:gz') as archive:
        for member in archive:
            prefix = 'riskium-candidate-' + source[:12] + '/'
            require(member.isfile() and member.name.startswith(prefix), 'V035-CORE-ARCHIVE-NONREGULAR')
            path = release.support.safe_path(member.name[len(prefix):])
            require(path not in seen and path in by_path, 'V035-CORE-ARCHIVE-PATH')
            seen.add(path)
            mode, raw = by_path[path]
            require(member.mode == mode and archive.extractfile(member).read() == raw,
                    'V035-CORE-ARCHIVE-GIT: ' + path)
    require(seen == set(by_path), 'V035-CORE-ARCHIVE-COVERAGE')
    return receipt['checks'], manifest


def live_readback(root, profile):
    """Build at HEAD, clone native Wiki and read every selected HTTP body."""
    root = Path(root)
    source = ensure_clean(root)
    sys.path.insert(0, str(root / 'tools/publication'))
    import current_documentation as documentation
    selection = json.loads((root / release.support.MATRIX).read_bytes())
    selected_outputs = selection['generated_outputs']
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / 'site'
        descriptor, wiki_outputs, audit = documentation.build(output, root=root)
        documentation.checked_component(descriptor, root=root)
        documentation.check_wiki_sources(wiki_outputs, root=root)
        rebuilt = (output / 'publication-manifest.json').read_bytes()
        manifest = json.loads(rebuilt)
        require(manifest['current_source_commit'] == source
                and manifest['current_documentation_version'] == '0.4.0'
                and len(manifest['releases']) == audit['frozen_snapshots'] == 4,
                'V035-LIVE-REBUILT-SOURCE')
        served = {p: h for p, h in manifest['files_sha256'].items() if p != '.nojekyll'}
        require(served == selected_outputs['all_served_files_sha256'] and len(served) == 311,
                'V035-LIVE-SERVED-SELECTION')
        expected_wiki = {p: sha(text.encode()) for p, text in wiki_outputs.items()}
        require(expected_wiki == selected_outputs['wiki_files_sha256'] and len(expected_wiki) == 23,
                'V035-LIVE-WIKI-SELECTION')
        wiki_folder = Path(tmp) / 'wiki'
        subprocess.run(['git', 'clone', '--quiet', '--depth=1', WIKI, str(wiki_folder)],
                       check=True, timeout=90)
        wiki_commit = git(wiki_folder, 'rev-parse', 'HEAD').decode().strip()
        actual_wiki = {}
        for record in git(wiki_folder, 'ls-tree', '-r', '-z', 'HEAD').split(b'\0'):
            if not record:
                continue
            header, raw_path = record.split(b'\t', 1)
            mode, kind, blob = header.split()
            name = release.support.safe_path(raw_path.decode())
            require(mode in (b'100644', b'100755') and kind == b'blob'
                    and name in expected_wiki and name not in actual_wiki,
                    'V035-LIVE-WIKI-INVENTORY')
            path = wiki_folder / name
            require(path.is_file() and not path.is_symlink(), 'V035-LIVE-WIKI-NONREGULAR')
            actual_wiki[name] = sha(path.read_bytes())
        require(actual_wiki == expected_wiki and len(actual_wiki) == 23, 'V035-LIVE-WIKI-BYTES')

        def fetch(path):
            path = release.support.safe_path(path)
            request = urllib.request.Request(SITE + path, headers={'Cache-Control': 'no-cache'})
            with urllib.request.urlopen(request, timeout=30) as response:
                require(response.status == 200 and response.url.startswith(SITE), 'V035-LIVE-HTTP-RESPONSE: ' + path)
                return response.read()

        actual_root = fetch('publication-manifest.json')
        require(actual_root == rebuilt, 'V035-LIVE-ROOT-MANIFEST-NOT-EXACT-SOURCE')
        http_checks = []

        def check(item):
            path, expected = item
            raw = fetch(path)
            require(sha(raw) == expected and raw == (output / path).read_bytes(),
                    'V035-LIVE-HTTP-BYTES: ' + path)
            return dict(path=path, sha256=sha(raw), status=200, exact_match=True)

        with ThreadPoolExecutor(max_workers=8) as pool:
            http_checks = list(pool.map(check, sorted(served.items())))
        result = dict(schema='riskium-v035-live-readback-v1', source_commit=source,
            checked_at_utc=datetime.now(timezone.utc).isoformat(), documentation_version='0.4.0',
            selection_matrix_sha256=release.support.SELECTION_HASHES[release.support.MATRIX],
            wiki_commit=wiki_commit, wiki_files=23, wiki_files_sha256=actual_wiki,
            pages_files=311, files_sha256=served, documentation_snapshots=4, all_bytes_match=True,
            root_manifest_utf8=actual_root.decode(), pages_manifest_sha256=sha(actual_root),
            rebuilt_manifest_sha256=sha(rebuilt), http_checks=http_checks,
            wiki_checks=[dict(file=p, sha256=h, exact_match=True) for p, h in sorted(actual_wiki.items())],
            root_manifest_http_status=200, http_responses=312,
            guide_source_commit=descriptor['guide_source_commit'],
            scope='Fresh actual exact-source deployment and native Wiki bytes; not independent semantic review.')
    ensure_clean(root, source)
    envelope = json.loads((root / profile['artifact_matrix']).read_bytes())
    release.validate_freshness(envelope, result, source)
    return result


def package(root, output, profile, checks, extra, freshness, provenance, *,
            source_commit=None, entries=None):
    """Create six assets; explicit entries overrides are for software fixtures."""
    root, output = Path(root), Path(output)
    if entries is None:
        source = ensure_clean(root, source_commit)
        entries = source_entries(root, source)
    else:
        require(source_commit is not None and re.fullmatch('[a-f0-9]{40}', source_commit),
                'V035-PACKAGE-FIXTURE-SOURCE')
        source = source_commit
    release.validate_checks(checks)
    release.validate_release_checks(extra)
    profile_blob = lambda p: (root / release.support.safe_path(p)).read_bytes()
    envelope = release.validate_profile_blob(profile, profile_blob)
    release.validate_freshness(envelope, freshness, source)
    require(not output.resolve().is_relative_to(root.resolve()), 'V035-PACKAGE-OUTPUT-IN-SOURCE')
    output.mkdir(parents=True, exist_ok=True)
    require(not any(output.iterdir()), 'V035-PACKAGE-OVERWRITE')
    seen = set()
    inventory = []
    archive_path = output / ('riskium-' + release.TAG + '-source.tar.gz')
    with archive_path.open('wb') as stream, gzip.GzipFile(fileobj=stream, filename='', mode='wb', mtime=0) as zipped:
        with tarfile.open(fileobj=zipped, mode='w') as archive:
            for path, mode, raw in entries:
                release.support.safe_path(path)
                require(path not in seen and mode in (0o644, 0o755) and isinstance(raw, bytes),
                        'V035-PACKAGE-SOURCE-ENTRY')
                seen.add(path)
                member = tarfile.TarInfo('riskium-' + release.TAG + '/' + path)
                member.size, member.mode, member.mtime = len(raw), mode, 0
                archive.addfile(member, io.BytesIO(raw))
                inventory.append(dict(path=path, bytes=len(raw), sha256=sha(raw)))
    write(output / 'source-manifest.json', dict(schema='riskium-stable-source-inventory-v1',
        tag=release.TAG, source_commit=source, file_count=len(inventory), files=inventory,
        scope='Tracked regular public source only; private author manuscripts and databases excluded.'))
    write(output / 'artifact-versions.json', dict(schema='riskium-v035-frozen-artifact-versions-v1',
        tag=release.TAG, source_commit=source, matrix_sha256=sha(profile_blob(release.MATRIX)), matrix=envelope))
    selected = json.loads(profile_blob(release.support.MATRIX))
    freeze_receipt = dict(schema='riskium-v035-final-freeze-v1', tag=release.TAG,
        source_commit=source, stage='EXACT_SOURCE_DRY_FROZEN', clean_exact_head=True,
        frozen_at_utc=datetime.now(timezone.utc).isoformat(),
        archive_inventory_verified=True, source_freeze_executed=True, publication_executed=False,
        profile_path=release.PROFILE, profile_sha256=sha(profile_blob(release.PROFILE)),
        artifact_matrix_path=release.MATRIX, artifact_matrix_sha256=sha(profile_blob(release.MATRIX)),
        critical_screen_path=release.SCREEN, critical_screen_sha256=sha(profile_blob(release.SCREEN)),
        release_tooling_sha256=envelope['finalization_tooling_sha256'],
        scientific_versions=release.support.SCIENCE, selected_components=29, selected_files=687,
        dependency_edges=68, selected_documentation_snapshots=4,
        preserve_releases=selected['preserve_releases'], new_owner_responses_generated=0,
        independent_validation=False, full_original_requirement_acceptance=False,
        checks=checks, passed_checks=len(checks), release_specific_checks=extra,
        publication_freshness=freshness, core_evidence_provenance=provenance,
        independent_public_download_readback='Required after separate explicit publication.',
        historical_engine_scope='Retained original HermiT/SHACL populations; not fresh full engine executions.')
    write(output / 'freeze-receipt.json', freeze_receipt)
    notes = profile_blob(release.NOTES) + ('\n\nExact frozen source commit: ' + chr(96) + source + chr(96) + '.\n').encode()
    (output / 'release-notes.md').write_bytes(notes)
    sums = ''.join(sha(p.read_bytes()) + '  ' + p.name + '\n' for p in sorted(output.iterdir()))
    (output / 'SHA256SUMS.txt').write_text(sums)
    release.validate_package(output, source)
    return freeze_receipt


def freeze(output, candidate_folder, candidate_zip, candidate_run_id, candidate_artifact_id,
           candidate_artifact_sha256, root=ROOT):
    root = Path(root)
    source = ensure_clean(root)
    profile = release.validate_profile(root)
    require(type(candidate_run_id) is int and candidate_run_id > 0
            and type(candidate_artifact_id) is int and candidate_artifact_id > 0,
            'V035-CORE-PROVENANCE-ID')
    ensure_remote_main(source)
    provenance = validate_remote_candidate(source, candidate_run_id, candidate_artifact_id,
                                           candidate_artifact_sha256)
    verify_candidate_zip(candidate_zip, candidate_folder, candidate_artifact_sha256)
    checks, manifest = validate_candidate(candidate_folder, root, source)
    provenance.update(artifact_digest_verified=True, archive_inventory_verified=True,
                      checks_reused=28, archive_verified_against_git=True)
    extra = []
    for args in release.EXTRA_CHECKS:
        run = subprocess.run([sys.executable, '-B', *args], cwd=root, capture_output=True, text=True)
        extra.append(dict(command=['python', *args], exit_code=run.returncode,
                          stdout=run.stdout, stderr=run.stderr))
        require(run.returncode == 0, 'V035-FREEZE-CHECK-FAILED: ' + str(args) + '\n' + run.stdout + run.stderr)
    release.validate_release_checks(extra)
    freshness = live_readback(root, profile)
    ensure_clean(root, source)
    release.validate_profile(root)
    result = package(root, output, profile, checks, extra, freshness, provenance, source_commit=source)
    ensure_clean(root, source)
    ensure_remote_main(source)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-profile', action='store_true')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--candidate-folder', type=Path)
    parser.add_argument('--candidate-zip', type=Path)
    parser.add_argument('--candidate-run-id', type=int)
    parser.add_argument('--candidate-artifact-id', type=int)
    parser.add_argument('--candidate-artifact-sha256')
    args = parser.parse_args()
    if args.check_profile:
        require(not any((args.output, args.candidate_folder, args.candidate_zip,
                         args.candidate_run_id, args.candidate_artifact_id, args.candidate_artifact_sha256)),
                'V035-FREEZE-PROFILE-MODE-ARGUMENTS')
        release.validate_profile()
        print(json.dumps(dict(status='V035_FINALIZATION_PROFILE_PASS', tag=release.TAG,
                              source_freeze_executed=False, publication_executed=False)))
        return
    if not all((args.output, args.candidate_folder, args.candidate_zip, args.candidate_run_id,
                args.candidate_artifact_id, args.candidate_artifact_sha256)):
        parser.error('--output and all --candidate-* inputs are required')
    result = freeze(args.output, args.candidate_folder, args.candidate_zip, args.candidate_run_id,
                    args.candidate_artifact_id, args.candidate_artifact_sha256)
    print(json.dumps(dict(status='V035_EXACT_SOURCE_DRY_FROZEN', tag=release.TAG,
        source_commit=result['source_commit'], source_freeze_executed=True,
        core_checks=len(result['checks']), release_specific_checks=len(result['release_specific_checks']),
        selected_components=29, selected_files=687, dependency_edges=68, staged_assets=6,
        publication_executed=False)))


if __name__ == '__main__':
    main()
