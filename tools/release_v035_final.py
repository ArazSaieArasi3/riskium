"""Offline v0.3.5 finalization and six-asset integrity checks.

The earlier selection/support packets are immutable inputs. Runtime freshness and
exact-source checks belong to a separate freeze receipt. Offline integrity cannot
authenticate an arbitrary rewritten validator or a claimed remote workflow; the
caller must also compare the downloaded artifact to its trusted external digest.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile

sys.dont_write_bytecode = True
import release_v035 as support

ROOT = Path(__file__).resolve().parents[1]
TAG = 'v0.3.5'
STAGE = 'FINALIZATION_DECLARED_NOT_FROZEN'
MATRIX = 'releases/distribution-v0.3.5.json'
PROFILE = 'releases/final-profile-v0.3.5.json'
REGISTRY = 'releases/finalization-profiles.json'
REQUEST = 'releases/finalization-request-v0.3.5.json'
SCREEN = 'evaluation/finalization/v0.3.5-freeze-review.json'
NOTES = 'docs/final-release-v0.3.5.md'
SUPPORT_SOURCE = '7c0dc160c869a5f29742b3e0d8d056c48725e8ff'
GUIDE_SOURCE = '2c4b0c46f22c90a3a5782e7c918e79f791aa4816'
TOOLING = ('tools/release_v035_final.py', 'tools/prepare_release_v035_final.py',
           'tests/test_release_v035_final.py', '.github/workflows/final-release-v035.yml')
SUPPORT_ANCHORS = {
    'releases/stable-profile-v0.3.5.json': 'd9222df4cd74015b2741aed43578e097f0012409dd4a8865de633545be5f6efd',
    'evaluation/finalization/v0.3.5-review.json': '6b9d35847519ef2a2799a802df5d1b36a87fbec30394dde8ec9dc45510ef1134',
    'docs/release-v0.3.5.md': '0b94219d5a2bb8986c63ccb51b93acd7ed906e42e53dbf4dd4491a3740f2f64e',
    'tools/release_v035.py': '002a121da2dd9af75b5aa5c134716d494f5c7faaa174084eb69aacbcf5a12af4',
    'tools/prepare_release_v035.py': 'aa565dddaec9269552233ad16c667191e397034685370f254ea67760684583bd',
    'tests/test_release_v035.py': '3b893dbdf968ca3eed600cfe59b109ae48b4f54c8e9231359d13eef527781a15',
    '.github/workflows/release-support-v035.yml': 'deb5c29d21eac25544c840c7bf55f8cea23f3f7107559bdd3a4bed3f3d0bcf90',
}
SCIENCE = dict(model='0.3.1', orsd='0.4.3', original_drsd='0.1.0', manuscript='7.0.8')
GATES = ('publication_requires_clean_exact_head', 'publication_requires_all_checks',
         'publication_requires_no_known_unresolved_critical_findings',
         'publication_requires_new_tag_and_release', 'readback_required',
         'package_requires_offline_validation', 'final_source_channel_readback_required')
CORE_CHECKS = [
    ['tools/validate_model.py'], ['tools/build_native.py', '--check'],
    ['tools/build_owl.py', '--check'], ['tools/review_coverage.py'],
    ['tools/review_references.py', '--check'], ['tools/build_quality_report.py', '--check'],
    ['tools/run_cq.py', '--check'], ['tools/build_traceability.py', '--check'],
    ['tools/build_reference.py', '--check'], ['tools/publication/audit_portal.py'],
    ['tools/publication/build_versioned_site.py', '--check'],
    ['tools/run_compatibility_shacl.py', '--check'],
    ['tools/run_comparison_shacl.py', '--check'],
    ['tools/run_relational_history.py', '--check'],
    ['tools/run_source_cq06.py', '--check'], ['tools/run_source_cq0708.py', '--check'],
    ['tools/build_final_review.py', '--check'], ['tools/check_release_alignment.py'],
    ['tools/run_integrated_validation.py', '--check'],
    ['tools/build_relational_assessment.py', '--check'],
    ['tools/run_relational_assessment.py', '--check'],
    ['tools/check_database_assurance.py', '--check'],
    ['tools/run_relational_correction.py', '--check'],
    ['tools/build_correction_inventory.py', '--check'],
    ['tools/audit_consistency.py', '--check'], ['tools/check_research_backlog.py', '--check'],
    ['tools/review_distribution.py'], ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
]
EXTRA_CHECKS = [
    ['tools/select_release_v035.py', '--check'],
    ['tools/prepare_release_v035.py', '--check-profile'],
    ['tools/prepare_release_v035_final.py', '--check-profile'],
    ['tools/run_relational_source_scenario.py', '--check'],
    ['tools/build_source_scenario_inventory.py', '--check'],
    ['tools/run_relational_source_scenario_lineage.py', '--check'],
    ['tools/build_source_scenario_lineage_inventory.py', '--check'],
    ['tools/run_relational_evidence.py', '--check'],
    ['tools/build_evidence_inventory.py', '--check'],
    ['tools/run_relational_evidence_lifecycle.py', '--check'],
    ['tools/build_evidence_lifecycle_inventory.py', '--check'],
    ['tools/audit_current_alignment.py', '--check'],
    ['tools/publication/current_documentation.py', '--check'],
]
ASSETS = frozenset({'riskium-v0.3.5-source.tar.gz', 'source-manifest.json',
                    'artifact-versions.json', 'freeze-receipt.json',
                    'release-notes.md', 'SHA256SUMS.txt'})


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + '\n'


def safe_path(value):
    require(isinstance(value, str) and value and '\\' not in value and '\0' not in value,
            'V035-FINAL-UNSAFE-PATH')
    require(not value.startswith('/') and all(p not in ('', '.', '..', '.git') for p in value.split('/'))
            and PurePosixPath(value).as_posix() == value, 'V035-FINAL-UNSAFE-PATH: ' + value)
    return value


def read_blob(blob, path):
    try:
        data = blob(safe_path(path))
    except (FileNotFoundError, KeyError) as error:
        raise ValueError('V035-FINAL-MISSING: ' + path) from error
    require(isinstance(data, bytes), 'V035-FINAL-NONBYTES: ' + path)
    return data


def reader(root):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), 'V035-FINAL-ROOT')

    def read(path):
        target = root
        for part in safe_path(path).split('/'):
            target = target / part
            require(not target.is_symlink(), 'V035-FINAL-SYMLINK: ' + path)
        require(target.resolve().is_relative_to(root.resolve()), 'V035-FINAL-ESCAPE')
        if not target.exists():
            raise FileNotFoundError(path)
        require(target.is_file(), 'V035-FINAL-NONFILE: ' + path)
        return target.read_bytes()
    return read


def loads(data):
    def unique(items):
        result = {}
        for key, value in items:
            require(key not in result, 'V035-FINAL-DUPLICATE-JSON-KEY: ' + key)
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=unique)


def hashes(bindings, blob):
    require(isinstance(bindings, dict) and bindings, 'V035-FINAL-HASH-REGISTER')
    for path, digest in bindings.items():
        require(isinstance(digest, str) and re.fullmatch('[a-f0-9]{64}', digest), 'V035-FINAL-DIGEST')
        require(sha(read_blob(blob, path)) == digest, 'V035-FINAL-STALE: ' + path)


def validate_profile_blob(profile, blob):
    hashes(SUPPORT_ANCHORS, blob)
    selection = support.validate_profile_blob(loads(read_blob(blob, support.PROFILE)), blob)
    require(profile['schema'] == 'riskium-v035-finalization-profile-v1'
            and profile['stage'] == STAGE and profile['tag'] == TAG, 'V035-FINAL-PROFILE')
    require(profile['scientific_versions'] == SCIENCE and profile['model_version'] == '0.3.1'
            and profile['orsd_revision'] == '0.4.3' and profile['manuscript_version'] == '7.0.8'
            and profile['reviewed_scope_commit'] == '3afa861b5296addefc98ce401767c7ab7d025d2c'
            and profile['accepted_scope'] == 'evaluation/owner-review/accepted-scope.json', 'V035-FINAL-SCIENCE')
    for flag in ('publication_enabled', 'independent_validation_claimed',
                 'full_original_requirement_acceptance_claimed'):
        require(profile.get(flag) is False, 'V035-FINAL-UNSUPPORTED-AUTHORITY: ' + flag)
    require(all(profile.get(flag) is True for flag in GATES), 'V035-FINAL-MISSING-GATE')
    require(profile['artifact_matrix'] == MATRIX and profile['critical_screen'] == SCREEN
            and profile['notes'] == NOTES, 'V035-FINAL-PROFILE-PATHS')
    hashes({MATRIX: profile['artifact_matrix_sha256'], SCREEN: profile['critical_screen_sha256'],
            NOTES: profile['notes_sha256']}, blob)
    envelope = loads(read_blob(blob, MATRIX))
    require(envelope['schema'] == 'riskium-v035-final-distribution-v1'
            and envelope['target'] == TAG and envelope['stage'] == STAGE
            and envelope['selection_path'] == support.MATRIX
            and envelope['selection_sha256'] == support.SELECTION_HASHES[support.MATRIX]
            and envelope['prospective_profile_path'] == support.PROFILE
            and envelope['prospective_profile_sha256'] == SUPPORT_ANCHORS[support.PROFILE]
            and envelope['support_source_commit'] == SUPPORT_SOURCE, 'V035-FINAL-ENVELOPE')
    require(envelope['scientific_versions'] == SCIENCE
            and envelope['domain_summary'] == dict(components=29, selected_files=687, dependency_edges=68)
            and envelope['preserve_releases'] == selection['preserve_releases'], 'V035-FINAL-ENVELOPE-SCOPE')
    docs = dict(documentation_version='0.4.0', wiki_files_sha256=selection['generated_outputs']['wiki_files_sha256'],
                served_files_sha256=selection['generated_outputs']['all_served_files_sha256'], frozen_snapshots=4)
    require(envelope['documentation'] == docs, 'V035-FINAL-DOCUMENTATION')
    require(set(envelope['finalization_tooling_sha256']) == set(TOOLING), 'V035-FINAL-TOOLING-CLOSURE')
    hashes(envelope['finalization_tooling_sha256'], blob)
    registry = loads(read_blob(blob, REGISTRY))
    request = loads(read_blob(blob, REQUEST))
    require(registry['schema'] == 'riskium-v035-finalization-registry-v1'
            and registry['profiles'] == {TAG: PROFILE}, 'V035-FINAL-REGISTRY')
    require(request['schema'] == 'riskium-v035-finalization-request-v1'
            and request['tag'] == TAG and request['profile'] == PROFILE
            and request.get('dry_freeze') is True and request.get('publish') is False,
            'V035-FINAL-REQUEST')
    screen = loads(read_blob(blob, SCREEN))
    require(screen['schema'] == 'riskium-v035-freeze-screen-v1' and screen['target'] == TAG
            and screen['stage'] == STAGE
            and screen['component_matrix_sha256'] == profile['artifact_matrix_sha256']
            and screen['release_tooling_sha256'] == envelope['finalization_tooling_sha256']
            and screen['required_core_checks'] == [['python', *a] for a in CORE_CHECKS]
            and screen['required_release_checks'] == [['python', *a] for a in EXTRA_CHECKS], 'V035-FINAL-SCREEN')
    require(screen['known_unresolved_critical_findings'] == []
            and type(screen['new_owner_responses_generated']) is int
            and screen['new_owner_responses_generated'] == 0, 'V035-FINAL-CRITICAL-FINDINGS')
    for flag in ('independent_semantic_review_claimed', 'material_scientific_change_since_owner_acceptance',
                 'universal_zero_defect_claimed', 'source_freeze_executed', 'publication_executed'):
        require(screen.get(flag) is False, 'V035-FINAL-SCREEN-SCOPE: ' + flag)
    risks = screen['reviewed_risks']
    require(len(risks) >= 8 and len({r['id'] for r in risks}) == len(risks), 'V035-FINAL-RISK-SET')
    for risk in risks:
        require(risk['id'] and risk['fresh_gate'] and risk['retained_evidence'], 'V035-FINAL-RISK-GATE')
        for path in risk['retained_evidence']:
            require(bool(read_blob(blob, path)), 'V035-FINAL-RISK-EVIDENCE')
    return envelope


def validate_profile(root=ROOT):
    blob = reader(root)
    profile = loads(read_blob(blob, PROFILE))
    validate_profile_blob(profile, blob)
    return profile


def validate_command_checks(checks, commands, label):
    require(isinstance(checks, list) and [c['command'] for c in checks] == [['python', *a] for a in commands],
            'V035-FINAL-' + label + '-COMMANDS')
    require(all(type(c['exit_code']) is int and c['exit_code'] == 0
                and isinstance(c.get('stdout'), str) and isinstance(c.get('stderr'), str) for c in checks),
            'V035-FINAL-' + label + '-FAILED')


def validate_checks(checks):
    validate_command_checks(checks, CORE_CHECKS, 'CORE')
    full = checks[-1]
    text = full['stdout'] + '\n' + full['stderr']
    require(re.search(r'Ran [1-9][0-9]* tests? in [0-9.]+s', text)
            and re.search(r'^OK(?:\s*\([^\n]*\))?\s*$', text, re.M), 'V035-FINAL-CORE-TEST-RESULT')


def validate_release_checks(checks):
    validate_command_checks(checks, EXTRA_CHECKS, 'RELEASE')


def validate_freshness(envelope, receipt, source, now=None):
    require(isinstance(source, str) and re.fullmatch('[a-f0-9]{40}', source), 'V035-FINAL-SOURCE')
    docs = envelope['documentation']
    require(receipt['schema'] == 'riskium-v035-live-readback-v1'
            and receipt['source_commit'] == source and receipt['documentation_version'] == '0.4.0'
            and receipt['selection_matrix_sha256'] == support.SELECTION_HASHES[support.MATRIX]
            and receipt['all_bytes_match'] is True, 'V035-FINAL-READBACK-IDENTITY')
    require(receipt['wiki_files'] == 23 and receipt['wiki_files_sha256'] == docs['wiki_files_sha256']
            and isinstance(receipt['wiki_commit'], str) and re.fullmatch('[a-f0-9]{40}', receipt['wiki_commit'])
            and receipt['pages_files'] == 311 and receipt['files_sha256'] == docs['served_files_sha256']
            and receipt['documentation_snapshots'] == docs['frozen_snapshots'] == 4,
            'V035-FINAL-READBACK-INVENTORY')
    require(receipt.get('guide_source_commit') == GUIDE_SOURCE
            and receipt.get('root_manifest_http_status') == 200
            and receipt.get('http_responses') == 312, 'V035-FINAL-READBACK-RESPONSES')
    http_checks = receipt.get('http_checks', [])
    wiki_checks = receipt.get('wiki_checks', [])
    require(isinstance(http_checks, list) and len(http_checks) == 311
            and len({row['path'] for row in http_checks}) == 311
            and {safe_path(row['path']): row['sha256'] for row in http_checks} == docs['served_files_sha256']
            and all(row.get('status') == 200 and row.get('exact_match') is True for row in http_checks),
            'V035-FINAL-READBACK-HTTP-ROWS')
    require(isinstance(wiki_checks, list) and len(wiki_checks) == 23
            and len({row['file'] for row in wiki_checks}) == 23
            and {safe_path(row['file']): row['sha256'] for row in wiki_checks} == docs['wiki_files_sha256']
            and all(row.get('exact_match') is True for row in wiki_checks), 'V035-FINAL-READBACK-WIKI-ROWS')
    stamp = datetime.fromisoformat(receipt['checked_at_utc'])
    require(stamp.tzinfo is not None, 'V035-FINAL-READBACK-TIMEZONE')
    age = ((now or datetime.now(timezone.utc)) - stamp).total_seconds()
    require(0 <= age < 86400, 'V035-FINAL-READBACK-AGE')
    require(isinstance(receipt['root_manifest_utf8'], str), 'V035-FINAL-ROOT-MANIFEST')
    raw = receipt['root_manifest_utf8'].encode()
    manifest = loads(raw)
    require(receipt['pages_manifest_sha256'] == receipt['rebuilt_manifest_sha256'] == sha(raw),
            'V035-FINAL-ROOT-MANIFEST-DIGEST')
    expected = dict(docs['served_files_sha256'], **{'.nojekyll': sha(b'')})
    require(len(expected) == 312 and manifest['current_source_commit'] == source
            and manifest['current_documentation_version'] == '0.4.0'
            and isinstance(manifest.get('releases'), dict) and len(manifest['releases']) == 4
            and manifest.get('current_documentation_projection', {}).get('documentation_version') == '0.4.0'
            and manifest['files_sha256'] == expected, 'V035-FINAL-ROOT-MANIFEST-SOURCE')
    return receipt


def validate_provenance(provenance, source):
    require(provenance['schema'] == 'riskium-v035-core-evidence-v1'
            and provenance['source_commit'] == source
            and provenance['workflow_name'] == 'Incremental release candidate'
            and provenance['workflow_conclusion'] == 'success', 'V035-FINAL-CORE-PROVENANCE')
    require(all(type(provenance[k]) is int and provenance[k] > 0 for k in ('workflow_run_id', 'artifact_id'))
            and isinstance(provenance['artifact_sha256'], str)
            and re.fullmatch('[a-f0-9]{64}', provenance['artifact_sha256']), 'V035-FINAL-CORE-PROVENANCE-REFERENCE')
    require(provenance['artifact_digest_verified'] is True and provenance['archive_inventory_verified'] is True
            and provenance['archive_verified_against_git'] is True and provenance['checks_reused'] == 28,
            'V035-FINAL-CORE-PROVENANCE-VERIFICATION')
    require(provenance.get('github_api_verified') is True, 'V035-FINAL-CORE-API-REFERENCE')


def validate_package(folder, source_commit):
    """Verify all six assets and archived source; no extraction, Git or network."""
    require(isinstance(source_commit, str) and re.fullmatch('[a-f0-9]{40}', source_commit), 'V035-FINAL-SOURCE')
    folder = Path(folder)
    require(folder.is_dir() and not folder.is_symlink(), 'V035-FINAL-PACKAGE-ROOT')
    entries = list(folder.iterdir())
    require({p.name for p in entries} == ASSETS and all(p.is_file() and not p.is_symlink() for p in entries),
            'V035-FINAL-SIX-ASSETS')
    expected_checksums = set(ASSETS) - {'SHA256SUMS.txt'}
    checksums = {}
    for line in (folder / 'SHA256SUMS.txt').read_text().splitlines():
        parts = line.split('  ')
        require(len(parts) == 2 and re.fullmatch('[a-f0-9]{64}', parts[0])
                and parts[1] in expected_checksums and parts[1] not in checksums, 'V035-FINAL-CHECKSUM-INVENTORY')
        checksums[parts[1]] = parts[0]
    require(set(checksums) == expected_checksums, 'V035-FINAL-CHECKSUM-INVENTORY')
    for name, digest in checksums.items():
        require(sha((folder / name).read_bytes()) == digest, 'V035-FINAL-ASSET-DIGEST: ' + name)
    blobs = {}
    with tarfile.open(folder / 'riskium-v0.3.5-source.tar.gz', mode='r:gz') as archive:
        for member in archive:
            prefix = 'riskium-v0.3.5/'
            require(member.isfile() and member.mode in (0o644, 0o755)
                    and member.name.startswith(prefix), 'V035-FINAL-ARCHIVE-MEMBER')
            path = safe_path(member.name[len(prefix):])
            require(path not in blobs, 'V035-FINAL-ARCHIVE-DUPLICATE: ' + path)
            raw = archive.extractfile(member).read()
            require(len(raw) == member.size, 'V035-FINAL-ARCHIVE-SIZE')
            blobs[path] = raw
    manifest = loads((folder / 'source-manifest.json').read_bytes())
    require(manifest['schema'] == 'riskium-stable-source-inventory-v1' and manifest['tag'] == TAG
            and manifest['source_commit'] == source_commit, 'V035-FINAL-MANIFEST-SOURCE')
    support.validate_source_manifest(manifest, blobs.__getitem__)
    require(len(manifest['files']) == len(blobs) and {r['path'] for r in manifest['files']} == set(blobs),
            'V035-FINAL-ARCHIVE-INVENTORY')
    profile = loads(read_blob(blobs.__getitem__, PROFILE))
    envelope = validate_profile_blob(profile, blobs.__getitem__)
    versions = loads((folder / 'artifact-versions.json').read_bytes())
    require(versions['schema'] == 'riskium-v035-frozen-artifact-versions-v1' and versions['tag'] == TAG
            and versions['source_commit'] == source_commit and versions['matrix'] == envelope
            and versions['matrix_sha256'] == sha(blobs[MATRIX]), 'V035-FINAL-FROZEN-MATRIX')
    freeze = loads((folder / 'freeze-receipt.json').read_bytes())
    require(freeze['schema'] == 'riskium-v035-final-freeze-v1' and freeze['tag'] == TAG
            and freeze['source_commit'] == source_commit and freeze['stage'] == 'EXACT_SOURCE_DRY_FROZEN'
            and freeze['clean_exact_head'] is True and freeze['archive_inventory_verified'] is True
            and freeze['source_freeze_executed'] is True and freeze['publication_executed'] is False,
            'V035-FINAL-FREEZE-IDENTITY')
    require(freeze['profile_path'] == PROFILE and freeze['profile_sha256'] == sha(blobs[PROFILE])
            and freeze['artifact_matrix_path'] == MATRIX and freeze['artifact_matrix_sha256'] == sha(blobs[MATRIX])
            and freeze['critical_screen_path'] == SCREEN and freeze['critical_screen_sha256'] == sha(blobs[SCREEN])
            and freeze['release_tooling_sha256'] == envelope['finalization_tooling_sha256'], 'V035-FINAL-FREEZE-BINDINGS')
    require(freeze['scientific_versions'] == SCIENCE and freeze['selected_components'] == 29
            and freeze['selected_files'] == 687 and freeze['dependency_edges'] == 68
            and freeze['selected_documentation_snapshots'] == 4
            and freeze['preserve_releases'] == envelope['preserve_releases']
            and type(freeze['new_owner_responses_generated']) is int and freeze['new_owner_responses_generated'] == 0
            and freeze['independent_validation'] is False and freeze['full_original_requirement_acceptance'] is False,
            'V035-FINAL-FREEZE-SCOPE')
    validate_checks(freeze['checks'])
    require(freeze['passed_checks'] == len(CORE_CHECKS), 'V035-FINAL-FREEZE-CHECK-COUNT')
    validate_release_checks(freeze['release_specific_checks'])
    validate_provenance(freeze['core_evidence_provenance'], source_commit)
    frozen_at = datetime.fromisoformat(freeze['frozen_at_utc'])
    require(frozen_at.tzinfo is not None, 'V035-FINAL-FREEZE-TIMEZONE')
    # A retained archive remains verifiable after its live-readback age window.
    # The actual freeze path checks wall-clock freshness before packaging; this
    # offline check preserves that relationship at the recorded freeze instant.
    validate_freshness(envelope, freeze['publication_freshness'], source_commit, now=frozen_at)
    expected_notes = blobs[NOTES] + ('\n\nExact frozen source commit: `' + source_commit + '`.\n').encode()
    require((folder / 'release-notes.md').read_bytes() == expected_notes, 'V035-FINAL-NOTES-SOURCE')
    return freeze, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check-profile', action='store_true')
    mode.add_argument('--check-package', type=Path)
    parser.add_argument('--source-commit')
    args = parser.parse_args()
    if args.check_profile:
        require(args.source_commit is None, 'Source argument requires --check-package')
        validate_profile()
        result = dict(status='V035_FINALIZATION_PROFILE_PASS', tag=TAG, publication_executed=False)
    else:
        require(args.source_commit is not None, 'Exact source required for package verification')
        freeze, manifest = validate_package(args.check_package, args.source_commit)
        result = dict(status='V035_SIX_ASSET_PACKAGE_PASS', tag=TAG, source_commit=freeze['source_commit'],
                      source_files=manifest['file_count'], core_checks=len(freeze['checks']),
                      release_checks=len(freeze['release_specific_checks']), publication_executed=False,
                      publisher_authentication='REQUIRES_TRUSTED_EXTERNAL_ARTIFACT_DIGEST')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
