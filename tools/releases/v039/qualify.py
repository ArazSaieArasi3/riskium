"""Fresh exact-source R1 qualification; neither releases nor Wiki/Pages are mutated."""
from pathlib import Path
from types import SimpleNamespace
import argparse, hashlib, importlib.util, json, subprocess, sys, tempfile
import source, reader, selection, projection

def main(args):
    if Path(reader.__file__).resolve() != source.HERE / 'reader.py':
        raise ValueError('Wrong reader module loaded')
    out = args.output.resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError('Qualification output must be empty')
    out.mkdir(parents=True, exist_ok=True)
    selected = selection.build(check=True)
    mapping = json.loads((source.OUT / 'mapping-receipt.json').read_text())
    if mapping['output_sha256'] != source.sha(source.OUT / 'riskium.owl.ttl'):
        raise ValueError('OWL mapping receipt hash mismatch')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source.ROOT, text=True).strip()
    # Bind all selected bodies to the commit, not merely to a dirty worktree.
    for path, digest in selected['selected_files_sha256'].items():
        body = subprocess.check_output(['git', 'show', commit + ':' + path], cwd=source.ROOT)
        if hashlib.sha256(body).hexdigest() != digest:
            raise ValueError('Selected input is not the execution commit body: ' + path)
    bound = {'path': str(selection.OUT.relative_to(source.ROOT)), 'sha256': source.sha(selection.OUT)}
    body = subprocess.check_output(['git', 'show', commit + ':' + bound['path']], cwd=source.ROOT)
    if hashlib.sha256(body).hexdigest() != bound['sha256']:
        raise ValueError('Selection manifest does not belong to execution commit')
    spec = importlib.util.spec_from_file_location('riskium_r1_oracles', source.b2.HERE / 'verify_candidate.py')
    verifier = importlib.util.module_from_spec(spec)
    saved_path = sys.path[:]
    sys.path.insert(0, str(source.b2.HERE))
    try:
        spec.loader.exec_module(verifier)
    finally:
        sys.path[:] = saved_path
    # The adapter only supplies stable-version inputs to the unchanged B2 runner.
    # The temporary sibling keeps the runner's reviewed SDK script path intact.
    with tempfile.TemporaryDirectory(prefix='r1-exact-source-', dir=source.PACKET) as tmp:
        transient = Path(tmp)
        for alias, name in source.NAMES.items():
            (transient / alias).write_bytes((source.OUT / name).read_bytes())
        verifier.b = SimpleNamespace(HERE=transient, ROOT=source.ROOT, IMPACT=source.b2.IMPACT,
            CONTRACT=source.CONTRACT, VERSION=source.VERSION, sha=source.sha, dump=source.dump,
            build=source.build, validate_contract=source.validate_contract,
            prior=source.b2.prior, prior_inputs=source.b2.prior_inputs)
        verifier.reader = reader
        code = verifier.main(SimpleNamespace(output=out / 'fresh-oracles', schema=args.schema,
            robot=args.robot, sdk=args.sdk, node=args.node))
        if code:
            raise ValueError('Selected-source acceptance mismatch')
    raw = json.loads((out / 'fresh-oracles/verification-report.json').read_text())
    if raw['candidate_version'] != source.VERSION or raw['execution_commit'] != commit:
        raise ValueError('Oracle execution source mismatch')
    manifest = projection.build(source.ROOT, out / 'publication', commit)
    if manifest['source_model_sha256'] != source.sha(source.OUT / 'riskium-model.json'):
        raise ValueError('Publication projection source differs from the selected scientific source')
    if manifest['source_commit'] != commit:
        raise ValueError('Publication projection execution commit mismatch')
    routes = projection.audit(out / 'publication')
    # Every generated commit-pinned repository target must actually exist.
    import re
    targets = set()
    for p in (out / 'publication').rglob('*'):
        if p.suffix not in {'.html', '.md'}:
            continue
        targets.update(re.findall(re.escape(projection.REPO + '/blob/' + commit + '/') + r'([^\s)\"<>#]+)', p.read_text()))
    for path in sorted(targets):
        subprocess.run(['git', 'cat-file', '-e', commit + ':' + path], cwd=source.ROOT, check=True, capture_output=True)
    routes['commit_pinned_repository_targets_checked'] = len(targets)
    routes['external_http_checked'] = False
    report = {'schema': 'riskium-v039-R1-qualification-1', 'status': 'PASS_R1_NOT_PUBLISHED',
        'execution_commit': commit, 'package_target': 'v0.3.9', 'source_version': source.VERSION,
        'source_sha256': source.sha(source.OUT / 'riskium-model.json'),
        'source_contract_sha256': source.sha(source.CONTRACT), 'selection': bound,
        'selection_summary': selected['summary'], 'fresh_oracle_summary': raw['summary'],
        'oracle_receipt_sha256': source.sha(out / 'fresh-oracles/verification-report.json'),
        'projection_manifest_sha256': source.sha(out / 'publication/publication-manifest.json'),
        'projection_audit': routes, 'published': False, 'maintained_channels_read_back': False,
        'runner_adapter': 'Unchanged B2 twenty-oracle runner executes freshly using selected 0.3.2 source/native/OWL/contract and reader. Its raw PASS_B2_CANDIDATE_NOT_PUBLISHED label is retained as runner vocabulary, not reused historical evidence.',
        'boundary': 'R1 qualifies selected source bodies and staged routes. R2 must package, independently download/verify and publish, then read back maintained channels. Historical 0.3.1 components are not 0.3.2-qualified production implementations. Manuscript 7.2.21 is unchanged.'}
    (out / 'qualification-report.json').write_text(source.dump(report))
    print(source.dump(report))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    for name in ['output', 'schema', 'robot', 'sdk', 'node']:
        ap.add_argument('--' + name, type=Path, required=True)
    args = ap.parse_args()
    for name in ['output', 'schema', 'robot', 'sdk', 'node']:
        setattr(args, name, getattr(args, name).resolve())
    main(args)
