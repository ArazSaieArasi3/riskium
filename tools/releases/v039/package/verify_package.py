"""Offline verifier independent of the builder, repository and ontology toolchain."""
from pathlib import Path, PurePosixPath
import argparse, base64, hashlib, io, json, re, tarfile

ASSETS = {'riskium-v0.3.9-source.tar.gz', 'source-manifest.json', 'artifact-versions.json',
          'freeze-receipt.json', 'release-notes.md', 'SHA256SUMS.txt'}
def sha(data): return hashlib.sha256(data).hexdigest()
def check(ok, message):
    if not ok: raise ValueError(message)
def git_hash(kind, data):
    return hashlib.sha1(kind.encode() + b' ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def tree_hash(rows):
    tree = {}
    for row in rows:
        parts = row['path'].split('/'); node = tree
        for part in parts[:-1]:
            child = node.setdefault(part, {})
            check(isinstance(child, dict), 'Source path/file collision'); node = child
        check(parts[-1] not in node, 'Duplicate source path')
        node[parts[-1]] = (row['mode'], row['git_blob'])
    def encode(node):
        body = b''
        for name, value in sorted(node.items(), key=lambda p: (p[0] + ('/' if isinstance(p[1], dict) else '')).encode()):
            mode, digest = ('40000', encode(value)) if isinstance(value, dict) else value
            body += mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(digest)
        return git_hash('tree', body)
    return encode(tree)

def archive_files(data, prefix):
    files = {}; modes = {}; total = 0
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as tar:
        for member in tar:
            path = PurePosixPath(member.name)
            check(member.isfile() and not member.issym() and not member.islnk(), 'Non-regular archive member')
            check(not path.is_absolute() and str(path) == member.name and '..' not in path.parts and
                  '.git' not in path.parts and '\\' not in member.name, 'Unsafe archive member path')
            check(len(path.parts) >= 2 and path.parts[0] == prefix, 'Wrong archive root')
            name = '/'.join(path.parts[1:]); check(name not in files, 'Duplicate archive member')
            check(0 <= member.size <= 32 * 1024 * 1024 and len(files) < 20000, 'Archive member limit')
            total += member.size; check(total <= 256 * 1024 * 1024, 'Archive population limit')
            body = tar.extractfile(member).read()
            check(len(body) == member.size, 'Truncated archive member')
            files[name] = body; modes[name] = member.mode
    return files, modes

def verify(directory, expected_source_commit, expected_run_id=None):
    directory = Path(directory)
    actual = {p.name for p in directory.iterdir()}
    check(actual == ASSETS and all((directory / n).is_file() and not (directory / n).is_symlink() for n in ASSETS),
          'Expected exactly six regular package assets')
    assets = {name: (directory / name).read_bytes() for name in ASSETS}
    checksum_rows = assets['SHA256SUMS.txt'].decode().splitlines(); checksums = {}
    for line in checksum_rows:
        match = re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9._-]+)', line)
        check(match is not None, 'Malformed checksum line')
        digest, name = match.groups(); check(name not in checksums, 'Duplicate checksum entry'); checksums[name] = digest
    check(set(checksums) == ASSETS - {'SHA256SUMS.txt'}, 'Incomplete checksum coverage')
    for name, digest in checksums.items(): check(sha(assets[name]) == digest, 'Asset checksum mismatch: ' + name)
    manifest = json.loads(assets['source-manifest.json']); receipt = json.loads(assets['freeze-receipt.json'])
    versions = json.loads(assets['artifact-versions.json'])
    check(re.fullmatch('[0-9a-f]{40}', expected_source_commit) is not None, 'Expected commit must be independently pinned')
    check(manifest['source_commit'] == receipt['source_commit'] == versions['source_commit'] == expected_source_commit,
          'Source commit disagreement')
    raw = base64.b64decode(manifest['commit_object_base64'], validate=True)
    check(git_hash('commit', raw) == expected_source_commit, 'Commit object does not match pinned source')
    files, modes = archive_files(assets['riskium-v0.3.9-source.tar.gz'], 'riskium-v0.3.9')
    rows = manifest['files']; check(len(rows) == manifest['file_count'] == len(files), 'Source inventory count mismatch')
    check({r['path'] for r in rows} == set(files), 'Source inventory names differ')
    for row in rows:
        name = row['path']; body = files[name]
        check(row['mode'] in {'100644', '100755'} and modes[name] == int(row['mode'][-3:], 8), 'Source mode differs')
        check(len(body) == row['size'] and sha(body) == row['sha256'], 'Source manifest body mismatch: ' + name)
        check(git_hash('blob', body) == row['git_blob'], 'Git blob body mismatch: ' + name)
    root_tree = tree_hash(rows)
    check(raw.splitlines()[0] == ('tree ' + root_tree).encode() and root_tree == manifest['source_tree'] == receipt['source_tree'],
          'Full source Git tree mismatch')
    own = 'tools/releases/v039/package/'
    policy = json.loads(files[own + 'policy.json'])
    check(set(policy['assets']) == ASSETS and policy['tag'] == manifest['tag'] == receipt['tag'] == versions['tag'] == 'v0.3.9',
          'Package policy/tag disagreement')
    check(policy['archive_prefix'] == manifest['archive_prefix'] == 'riskium-v0.3.9', 'Archive prefix disagreement')
    epoch = int(next(x for x in raw.decode().splitlines() if x.startswith('committer ')).rsplit(' ', 2)[1])
    check(manifest['commit_time'] == epoch, 'Source epoch disagreement')
    selection = json.loads(files[policy['source_selection']]); contract = json.loads(files[policy['contract']])
    model = json.loads(files[policy['model']]); reader = json.loads(files[policy['reader_manifest']])
    selected_sha = sha(files[policy['source_selection']])
    check(manifest['selection_path'] == policy['source_selection'] and
          manifest['selection_sha256'] == versions['selection_sha256'] == selected_sha, 'Selection manifest disagreement')
    for name, digest in selection['selected_files_sha256'].items():
        check(name in files and sha(files[name]) == digest, 'Selected file body mismatch: ' + name)
    check(selection['summary']['selected_files'] == len(selection['selected_files_sha256']), 'Selected-file denominator mismatch')
    check(versions['components'] == selection['artifacts'] and versions['dependencies'] == selection['dependencies'] and
          versions['dependency_order'] == selection['dependency_order'] and versions['summary'] == selection['summary'],
          'Component version/dependency projection differs from committed selection')
    components = {c['id']: c for c in selection['artifacts']}
    check(len(components) == len(selection['artifacts']), 'Duplicate component ID')
    active = [c for c in components.values() if not c['id'].startswith('HISTORICAL/')]
    historical = [c for c in components.values() if c['id'].startswith('HISTORICAL/')]
    check(len(active) == policy['active_components'] == selection['summary']['active_components'] == 6 and
          len(historical) == policy['historical_components'] == selection['summary']['historical_components'] == 32,
          'Active/historical role denominator mismatch')
    check({c['id'] for c in active} == set(json.loads(files['releases/selection-policy-v0.3.9.json'])['active_component_ids']),
          'Undeclared active component')
    prior = {c['id']: c for c in json.loads(files['releases/selection-v0.3.8.json'])['artifacts']}
    for c in historical:
        old = prior[c['id'].split('/', 1)[1]]
        check(c['version'] == old['version'] and c['compatible_model'] == old['compatible_model'] and
              c['status'] == 'HISTORICAL_REFERENCE_NOT_032_REQUALIFIED', 'Historical component was relabeled')
        check([(f['original_path'], f['sha256']) for f in c['files']] == [(f['path'], f['sha256']) for f in old['files']],
              'Historical component bindings changed')
    for c in components.values():
        for f in c['files']: check(sha(files[f['path']]) == f['sha256'], 'Component body differs')
    completed = set()
    for cid in selection['dependency_order']:
        check(cid in components and cid not in completed, 'Invalid dependency order')
        for dep in selection['dependencies'][cid]:
            check(dep['id'] in completed and dep['version'] == components[dep['id']]['version'], 'Unresolved component dependency')
        completed.add(cid)
    check(completed == set(components), 'Incomplete dependency order')
    model_sha = sha(files[policy['model']])
    check(policy['source_version'] == versions['source_version'] == selection['source_version'] == model['version'] == '0.3.2',
          'Scientific version disagreement')
    check(policy['reader_version'] == versions['reader_version'] == reader['documentation_version'] == '0.4.9', 'Reader version disagreement')
    check(versions['manuscript_version'] == receipt['manuscript_version'] == policy['manuscript_version'] == '7.2.21', 'Manuscript role changed')
    check(contract['source']['sha256'] == reader['source_model_sha256'] == receipt['scientific_source_sha256'] == model_sha,
          'Scientific source/contract/reader disagreement')
    for binding in contract['dependencies'] + contract['frozen_inputs'] + [contract['policy']]:
        check(sha(files[binding['path']]) == binding['sha256'], 'Scientific dependency differs')
    mapping = json.loads(files['ontology/0.3.2/mapping-receipt.json'])
    check(mapping['output_sha256'] == sha(files['ontology/0.3.2/riskium.owl.ttl']), 'OWL mapping receipt differs')
    for name, digest in reader['files_sha256'].items():
        check(sha(files['documentation/0.4.9/reader/' + name]) == digest, 'Reader body differs')
    for name, digest in receipt['bound_assets_sha256'].items():
        check(name in ASSETS and name not in {'freeze-receipt.json', 'SHA256SUMS.txt'} and sha(assets[name]) == digest,
              'Freeze/asset disagreement')
    check(set(receipt['bound_assets_sha256']) == ASSETS - {'freeze-receipt.json', 'SHA256SUMS.txt'}, 'Incomplete freeze asset bindings')
    report = receipt['qualification_report']; serial = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode()
    check(sha(serial) == receipt['qualification_report_sha256'], 'Qualification report digest differs')
    check(report['status'] == policy['qualification_status'] == 'PASS_R1_NOT_PUBLISHED' and report['execution_commit'] == expected_source_commit,
          'Qualification execution disagreement')
    check(report['source_sha256'] == model_sha and report['source_contract_sha256'] == sha(files[policy['contract']]) and
          report['selection']['sha256'] == selected_sha, 'Qualification input disagreement')
    q = report['fresh_oracle_summary']
    check(q['planned_cases'] == q['cases_executed'] == q['cases_matched'] == 20 and
          q['actual_SHACL_invocations'] == 13 and q['actual_HermiT_invocations'] == q['HermiT_matches'] == 8,
          'Insufficient exact-source qualification')
    check(report['selection_summary'] == selection['summary'] and
          report['projection_audit']['html_pages'] == report['projection_audit']['wiki_pages'] == 89,
          'Qualified selection/projection population differs')
    check(receipt['public_release_created'] is False and receipt['maintained_channels_read_back'] is False and receipt['issues_closed'] == [],
          'Prepared package makes a publication claim')
    if receipt['build_mode'] == 'ci':
        check(receipt['status'] == 'PREPARED_CI_NOT_PUBLISHED' and isinstance(expected_run_id, int) and expected_run_id > 0 and
              receipt['workflow_run_id'] == expected_run_id, 'CI run binding differs')
    else:
        check(receipt['build_mode'] == 'local-preflight' and receipt['status'] == 'LOCAL_PREFLIGHT_NOT_PUBLISHED' and
              receipt['workflow_run_id'] is None and expected_run_id is None, 'Local preflight relabeled as CI')
    notes = files[own + 'release-notes-template.md'].decode()
    for key, value in {'SOURCE_COMMIT': expected_source_commit, 'ACTIVE_COMPONENTS': str(len(active)),
                       'HISTORICAL_COMPONENTS': str(len(historical)), 'SELECTED_FILES': str(selection['summary']['selected_files'])}.items():
        notes = notes.replace('{{' + key + '}}', value)
    check(assets['release-notes.md'] == notes.encode(), 'Release notes differ from committed template')
    check(not any(name.endswith(('.docx', '.pdf')) for name in files) and versions['article_binaries_included'] is False,
          'Unexpected article/document binary in source snapshot')
    return {'status': 'PASS_PACKAGE_NOT_PUBLISHED', 'source_commit': expected_source_commit,
        'workflow_run_id': expected_run_id, 'source_tree': root_tree, 'source_files': len(files),
        'selected_files': len(selection['selected_files_sha256']), 'active_components': len(active),
        'historical_components': len(historical), 'assets_checked': len(ASSETS),
        'checksums_checked': len(checksums), 'git_commit_and_full_tree_reconstructed': True,
        'source_contract_and_reader_checked': True, 'qualification_bound': True,
        'public_release_created': False, 'live_channel_readback': False,
        'boundary': 'Offline package and provenance-binding checks. Actual CI run/artifact origin and later public-release availability require separate authenticated/live readback.'}

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--assets', type=Path, required=True)
    ap.add_argument('--expected-source-commit', required=True); ap.add_argument('--expected-run-id', type=int)
    ap.add_argument('--report', type=Path); a = ap.parse_args()
    result = verify(a.assets, a.expected_source_commit, a.expected_run_id)
    body = json.dumps(result, indent=2) + '\n'
    if a.report: a.report.write_text(body)
    print(body)
