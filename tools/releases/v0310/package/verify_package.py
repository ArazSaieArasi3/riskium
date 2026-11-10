"""Offline verifier independent of the builder, repository and ontology toolchain."""
from pathlib import Path, PurePosixPath
import argparse, base64, hashlib, io, json, re, tarfile

ASSETS = {'riskium-v0.3.10-source.tar.gz', 'source-manifest.json', 'artifact-versions.json',
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
    check({p.name for p in directory.iterdir()} == ASSETS and
          all((directory / n).is_file() and not (directory / n).is_symlink() for n in ASSETS), 'Expected exactly six regular package assets')
    assets = {n: (directory / n).read_bytes() for n in ASSETS}
    checksums = {}
    for line in assets['SHA256SUMS.txt'].decode().splitlines():
        match = re.fullmatch(r'([a-f0-9]{64})  ([A-Za-z0-9._-]+)', line)
        check(match is not None and match[2] not in checksums, 'Malformed/duplicate checksum')
        checksums[match[2]] = match[1]
    check(set(checksums) == ASSETS - {'SHA256SUMS.txt'}, 'Incomplete checksum coverage')
    for name, digest in checksums.items():
        check(sha(assets[name]) == digest, 'Asset checksum mismatch: ' + name)
    m, r, v = [json.loads(assets[n]) for n in ['source-manifest.json', 'freeze-receipt.json', 'artifact-versions.json']]
    check(re.fullmatch('[a-f0-9]{40}', expected_source_commit) is not None, 'Independently pinned commit required')
    check(m['source_commit'] == r['source_commit'] == v['source_commit'] == expected_source_commit, 'Source commit disagreement')
    raw = base64.b64decode(m['commit_object_base64'], validate=True)
    check(git_hash('commit', raw) == expected_source_commit, 'Pinned Git commit differs')
    files, modes = archive_files(assets['riskium-v0.3.10-source.tar.gz'], 'riskium-v0.3.10')
    rows = m['files']
    check(len(rows) == m['file_count'] == len(files) and {x['path'] for x in rows} == set(files), 'Source inventory differs')
    for row in rows:
        body = files[row['path']]
        check(row['mode'] in {'100644', '100755'} and modes[row['path']] == int(row['mode'][-3:], 8), 'Source mode differs')
        check(len(body) == row['size'] and sha(body) == row['sha256'] and git_hash('blob', body) == row['git_blob'], 'Source blob differs')
    tree = tree_hash(rows)
    check(raw.splitlines()[0] == ('tree ' + tree).encode() and m['source_tree'] == r['source_tree'] == tree, 'Complete Git tree differs')
    policy = json.loads(files['tools/releases/v0310/package/policy.json'])
    check(m['tag'] == r['tag'] == v['tag'] == policy['tag'] == 'v0.3.10' and set(policy['assets']) == ASSETS, 'Package identity differs')
    check(m['archive_prefix'] == 'riskium-v0.3.10', 'Archive prefix differs')
    epoch = int(next(x for x in raw.decode().splitlines() if x.startswith('committer ')).rsplit(' ', 2)[1])
    check(epoch == m['commit_time'], 'Source epoch differs')
    selection = json.loads(files[policy['source_selection']])
    digest = sha(files[policy['source_selection']])
    check(m['selection_path'] == policy['source_selection'] and m['selection_sha256'] == v['selection_sha256'] == digest, 'Selection identity differs')
    for name, expected in selection['selected_files_sha256'].items():
        check(name in files and sha(files[name]) == expected, 'Selected binding differs: ' + name)
    check(selection['summary']['selected_files'] == len(selection['selected_files_sha256']), 'Selected denominator differs')
    check(v['components'] == selection['artifacts'] and v['dependencies'] == selection['dependencies'] and
          v['dependency_order'] == selection['dependency_order'] and v['summary'] == selection['summary'], 'Component projection differs')
    components = {a['id']: a for a in selection['artifacts']}
    check(len(components) == len(selection['artifacts']), 'Duplicate component')
    retained = [a for a in components.values() if a['id'].startswith('PRIOR039/')]
    active = [a for a in components.values() if not a['id'].startswith('PRIOR039/')]
    check(len(active) == policy['active_components'] == selection['summary']['active_components'] == 8 and
          len(retained) == policy['retained_predecessor_components'] == selection['summary']['historical_components'] == 38, 'Component roles differ')
    check({a['id'] for a in active} == set(selection['active_component_ids']), 'Active component identities differ')
    prior_bytes = files['releases/selection-v0.3.9.json']
    check(sha(prior_bytes) == selection['predecessor_selection_sha256'], 'Predecessor selection differs')
    prior = json.loads(prior_bytes)
    old = {a['id']: a for a in prior['artifacts']}
    for a in retained:
        previous = old[a['id'].split('/', 1)[1]]
        check(a['version'] == previous['version'] and a['compatible_model'] == previous['compatible_model'] and
              a['original_status'] == previous['status'] and a['status'] == 'RETAINED_AT_ORIGINAL_VERSION_AND_SOURCE', 'Predecessor role relabeled')
        check([(f['predecessor_path'], f['sha256']) for f in a['files']] == [(f['path'], f['sha256']) for f in previous['files']], 'Predecessor body binding differs')
    for name, expected in prior['selected_files_sha256'].items():
        alias = selection['historical_delivery_aliases'].get(name, name)
        check(sha(files[alias]) == expected, 'Preserved predecessor closure differs')
    done = set()
    for cid in selection['dependency_order']:
        check(cid in components and cid not in done, 'Invalid dependency order')
        for dep in selection['dependencies'][cid]:
            check(dep['id'] in done and components[dep['id']]['version'] == dep['version'], 'Unresolved component dependency')
        for f in components[cid]['files']:
            check(sha(files[f['path']]) == f['sha256'], 'Component body differs')
        done.add(cid)
    check(done == set(components), 'Incomplete dependencies')
    model_sha = sha(files[policy['model']])
    review = json.loads(files[policy['curation']]); reader = json.loads(files[policy['reader_manifest']])
    check(v['source_version'] == selection['source_version'] == '0.3.2' and v['review_version'] == '0.2.0' and
          v['reader_version'] == '0.4.10' and reader['model_sha256'] == review['model_sha256'] == model_sha, 'Source/review/reader roles differ')
    check(reader['review_sha256'] == sha(files[policy['curation']]), 'Review/reader binding differs')
    for name, expected in review['inputs_sha256'].items():
        check(sha(files[name]) == expected, 'Documentary input differs')
    check(len(review['concepts']) == len({x['concept_id'] for x in review['concepts']}) == 82, 'Review population differs')
    check(review['summary']['dispositions'] == {'RELATED': 40, 'CONTRAST': 20, 'ANALOGY': 19, 'NEEDS_LICENSED_SOURCE': 3}, 'Deferral accounting differs')
    for name, expected in reader['files_sha256'].items():
        check(sha(files['documentation/0.4.10/reader/' + name]) == expected, 'Reader body differs')
    contract = json.loads(files['ontology/0.3.2/source-contract.json'])
    check(contract['source']['sha256'] == model_sha == r['scientific_source_sha256'], 'Scientific contract differs')
    for f in contract['dependencies'] + contract['frozen_inputs'] + [contract['policy']]:
        check(sha(files[f['path']]) == f['sha256'], 'Scientific dependency differs')
    check(v['manuscript_version'] == r['manuscript_version'] == policy['article_version'] == '7.2.21' and
          v['article_binaries_included'] is False and not any(n.endswith(('.docx', '.pdf')) for n in files), 'Article role changed')
    check(set(r['bound_assets_sha256']) == ASSETS - {'freeze-receipt.json', 'SHA256SUMS.txt'}, 'Freeze coverage differs')
    for name, expected in r['bound_assets_sha256'].items():
        check(sha(assets[name]) == expected, 'Freeze asset differs')
    q = r['qualification_report']
    encoded = (json.dumps(q, ensure_ascii=False, indent=2) + '\n').encode()
    check(sha(encoded) == r['qualification_report_sha256'], 'Qualification digest differs')
    check(q['status'] == 'PASS_N5A_CANDIDATE_NOT_PUBLISHED' and q['source_ref'] == expected_source_commit and
          q['source_snapshot']['clean_exact_checkout'] is True and q['selection_sha256'] == digest, 'Exact source qualification differs')
    check(q['curation_contracts_passed'] == 20 and q['composition_contracts_passed'] >= 8 and
          q['composition']['paired_bodies'] == 111 and q['composition']['retained_guides'] == 20, 'Qualified scope incomplete')
    for name, expected in q['inputs_sha256'].items():
        check(sha(files[name]) == expected, 'Qualified input differs')
    check(r['public_release_created'] is False and r['maintained_channels_read_back'] is False and r['issues_closed'] == [], 'Premature publication claim')
    if r['build_mode'] == 'ci':
        check(r['status'] == 'PREPARED_CI_NOT_PUBLISHED' and isinstance(expected_run_id, int) and expected_run_id > 0 and
              r['workflow_run_id'] == expected_run_id and q['ci_run_id'] == str(expected_run_id) and q['environment'] == 'CI', 'CI run binding differs')
    else:
        check(r['build_mode'] == 'local-preflight' and r['status'] == 'LOCAL_PREFLIGHT_NOT_PUBLISHED' and
              expected_run_id is None and r['workflow_run_id'] is None, 'Local package relabeled CI')
    notes = files['tools/releases/v0310/package/release-notes-template.md'].decode().replace('{{SOURCE_COMMIT}}', expected_source_commit)
    check(assets['release-notes.md'] == notes.encode(), 'Release notes differ')
    return {'status': 'PASS_V0310_PACKAGE_NOT_PUBLISHED', 'source_commit': expected_source_commit, 'source_tree': tree,
            'workflow_run_id': expected_run_id, 'source_files': len(files), 'selected_files': len(selection['selected_files_sha256']),
            'active_components': 8, 'retained_components': 38, 'assets_checked': 6, 'checksums_checked': 5,
            'full_git_commit_tree_verified': True, 'historical_bindings_preserved': True,
            'qualification_bound': True, 'published': False, 'live_channel_readback': False}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--assets', type=Path, required=True)
    p.add_argument('--expected-source-commit', required=True)
    p.add_argument('--expected-run-id', type=int)
    p.add_argument('--report', type=Path)
    a = p.parse_args()
    value = verify(a.assets, a.expected_source_commit, a.expected_run_id)
    body = json.dumps(value, indent=2) + '\n'
    if a.report:
        a.report.write_text(body)
    print(body)

