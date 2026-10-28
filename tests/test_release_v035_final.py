"""Finalization trust boundaries using explicit temporary software fixtures.

All successful command/channel/provenance records constructed here are test
fixtures, not actual freezes, hosted runs, publication or human review evidence.
The real runtime obtains its records separately from actual checks/readbacks.
"""
import copy
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import release_v035 as support
import release_v035_final as release
import prepare_release_v035_final as prepare


def encoded(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


class Release035Finalization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = json.loads((ROOT / release.PROFILE).read_bytes())
        cls.envelope = json.loads((ROOT / release.MATRIX).read_bytes())
        cls.selection = json.loads((ROOT / support.MATRIX).read_bytes())
        cls.source = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.folder = Path(cls.temporary.name)
        # A temporary index includes pending local delivery files without
        # changing the real index or creating a synthetic production commit.
        env = {**os.environ, 'GIT_INDEX_FILE': str(cls.folder / 'fixture-index')}
        subprocess.run(['git', 'read-tree', 'HEAD'], cwd=ROOT, env=env, check=True)
        subprocess.run(['git', 'add', '--all'], cwd=ROOT, env=env, check=True)
        tree = subprocess.check_output(['git', 'write-tree'], cwd=ROOT, env=env, text=True).strip()
        raw = subprocess.check_output(['git', 'archive', '--format=tar', tree], cwd=ROOT)
        cls.entries = []
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
            for member in archive:
                if member.isdir():
                    continue
                if not member.isfile() or Path(member.name).is_absolute() or '..' in Path(member.name).parts:
                    raise AssertionError('Unsafe generated software fixture archive')
                # git archive applies tar.umask and emits 0664 for a 100644
                # blob; the package protocol preserves committed Git modes.
                mode = 0o755 if member.mode & 0o111 else 0o644
                cls.entries.append((member.name, mode, archive.extractfile(member).read()))
        cls.checks = cls.command_fixtures(release.CORE_CHECKS)
        cls.extra = cls.command_fixtures(release.EXTRA_CHECKS)
        cls.freshness = cls.channel_fixture()
        cls.provenance = dict(
            schema='riskium-v035-core-evidence-v1', source_commit=cls.source,
            workflow_name='Incremental release candidate', workflow_run_id=1,
            artifact_id=1, artifact_sha256='a' * 64, workflow_conclusion='success',
            artifact_digest_verified=True, archive_inventory_verified=True,
            checks_reused=28, archive_verified_against_git=True, github_api_verified=True,
        )
        cls.pristine = cls.folder / 'pristine'
        prepare.package(ROOT, cls.pristine, cls.profile, cls.checks, cls.extra,
                        cls.freshness, cls.provenance,
                        source_commit=cls.source, entries=cls.entries)
        # A second fixture uses only the real committed HEAD. It exercises
        # candidate consumption against Git; its command records are synthetic.
        from prepare_incremental_release import snapshot
        cls.candidate = cls.folder / 'candidate'
        snapshot(ROOT, 'HEAD', cls.candidate, checks=cls.checks)
        cls.candidate_zip = cls.folder / 'candidate.zip'
        with zipfile.ZipFile(cls.candidate_zip, 'w', compression=zipfile.ZIP_STORED) as archive:
            for path in sorted(cls.candidate.iterdir()):
                archive.write(path, path.name)
        cls.candidate_digest = digest(cls.candidate_zip.read_bytes())

    @staticmethod
    def command_fixtures(commands):
        records = [dict(command=['python', *args], exit_code=0,
                        stdout='SOFTWARE FIXTURE ONLY: no actual command was run.\n', stderr='')
                   for args in commands]
        for row in records:
            if row['command'][:3] == ['python', '-m', 'unittest']:
                row['stderr'] = 'SOFTWARE FIXTURE ONLY\nRan 1 tests in 0.001s\n\nOK\n'
        return records

    @classmethod
    def channel_fixture(cls):
        outputs = cls.selection['generated_outputs']
        snapshots = {}
        for path in ['tools/publication/pages-registry.json', 'tools/publication/snapshot-additions-v0.3.4.json']:
            snapshots.update(json.loads(cls.blob(path))['releases'])
        root_manifest = dict(
            current_source_commit=cls.source, current_documentation_version='0.4.0',
            files_sha256={**outputs['all_served_files_sha256'], '.nojekyll': digest(b'')},
            releases=snapshots, current_documentation_projection=dict(documentation_version='0.4.0'),
        )
        raw = encoded(root_manifest)
        return dict(
            schema='riskium-v035-live-readback-v1', source_commit=cls.source,
            checked_at_utc=datetime.now(timezone.utc).isoformat(),
            documentation_version='0.4.0',
            selection_matrix_sha256=support.SELECTION_HASHES[support.MATRIX],
            wiki_commit='1' * 40, wiki_files=23,
            wiki_files_sha256=outputs['wiki_files_sha256'], pages_files=311,
            files_sha256=outputs['all_served_files_sha256'], documentation_snapshots=4,
            all_bytes_match=True, root_manifest_utf8=raw.decode(),
            pages_manifest_sha256=digest(raw), rebuilt_manifest_sha256=digest(raw),
            root_manifest_http_status=200, http_responses=312,
            guide_source_commit=outputs['guide_source_commit'],
            http_checks=[dict(path=p, sha256=h, status=200, exact_match=True)
                         for p, h in sorted(outputs['all_served_files_sha256'].items())],
            wiki_checks=[dict(file=p, sha256=h, exact_match=True)
                         for p, h in sorted(outputs['wiki_files_sha256'].items())],
        )

    @staticmethod
    def blob(path):
        return (ROOT / path).read_bytes()

    def changed_blob(self, replacements):
        return lambda path: replacements[path] if path in replacements else self.blob(path)

    @contextmanager
    def package_copy(self):
        with tempfile.TemporaryDirectory(dir=self.folder) as temp:
            folder = Path(temp) / 'package'
            shutil.copytree(self.pristine, folder)
            yield folder

    @staticmethod
    def sums(folder):
        (folder / 'SHA256SUMS.txt').write_text(''.join(
            digest(path.read_bytes()) + '  ' + path.name + '\n'
            for path in sorted(folder.iterdir()) if path.name != 'SHA256SUMS.txt' and path.is_file()))

    @staticmethod
    def rewrite_json(folder, name, mutate):
        path = folder / name
        value = json.loads(path.read_bytes())
        mutate(value)
        path.write_bytes(encoded(value))

    @staticmethod
    def archive_entries(folder):
        path = folder / 'riskium-v0.3.5-source.tar.gz'
        with tarfile.open(path, 'r:gz') as archive:
            return [(copy.copy(m), archive.extractfile(m).read() if m.isfile() else None) for m in archive]

    def rewrite_archive(self, folder, transform, update_manifest=False):
        entries = transform(self.archive_entries(folder))
        path = folder / 'riskium-v0.3.5-source.tar.gz'
        with tarfile.open(path, 'w:gz', compresslevel=1) as archive:
            for member, raw in entries:
                if raw is not None:
                    member.size = len(raw)
                archive.addfile(member, io.BytesIO(raw) if raw is not None else None)
        if update_manifest:
            manifest = json.loads((folder / 'source-manifest.json').read_bytes())
            manifest['files'] = [dict(path=m.name.split('/', 1)[1], bytes=len(raw), sha256=digest(raw))
                                 for m, raw in entries if m.isfile()]
            manifest['file_count'] = len(manifest['files'])
            (folder / 'source-manifest.json').write_bytes(encoded(manifest))
        self.sums(folder)

    def test_actual_final_profile_keeps_the_original_domain_selection(self):
        self.assertEqual(release.validate_profile(ROOT)['tag'], 'v0.3.5')
        value = release.validate_profile_blob(self.profile, self.blob)
        self.assertEqual(value['domain_summary'], dict(components=29, selected_files=687, dependency_edges=68))
        self.assertEqual(self.blob(support.MATRIX), encoded(self.selection))
        self.assertFalse(self.profile['publication_enabled'])

    def test_final_profile_validation_needs_no_git_or_network(self):
        with patch('subprocess.Popen', side_effect=AssertionError('No Git or other process in offline validation')), \
                patch('urllib.request.urlopen', side_effect=AssertionError('No network in offline validation')), \
                patch('socket.create_connection', side_effect=AssertionError('No network in offline validation')):
            release.validate_profile_blob(self.profile, self.blob)

    def test_all_twenty_eight_core_commands_and_actual_outcomes_are_required(self):
        from prepare_incremental_release import CHECKS as original_contract
        self.assertEqual(release.CORE_CHECKS, original_contract)
        self.assertEqual(len(self.checks), 28)
        release.validate_checks(self.checks)
        for bad in [self.checks[:-1], list(reversed(self.checks)),
                    [{**r, 'exit_code': 1 if i == 4 else 0} for i, r in enumerate(self.checks)]]:
            with self.subTest(commands=len(bad)), self.assertRaises(ValueError):
                release.validate_checks(bad)

    def test_release_specific_checks_cannot_be_replaced_by_an_equal_count(self):
        self.assertEqual(len(self.extra), 13)
        self.assertIn(['python', 'tools/run_relational_evidence_lifecycle.py', '--check'],
                      [row['command'] for row in self.extra])
        release.validate_release_checks(self.extra)
        same_count = copy.deepcopy(self.extra)
        same_count[0]['command'] = ['python', '-c', 'pass']
        for bad in [self.extra[:-1], list(reversed(self.extra)), same_count,
                    [{**r, 'exit_code': 1 if i == 1 else 0} for i, r in enumerate(self.extra)]]:
            with self.subTest(commands=len(bad)), self.assertRaises(ValueError):
                release.validate_release_checks(bad)

    def test_profile_cannot_enable_publication_or_change_scientific_scope(self):
        for key, value in [('publication_enabled', True), ('model_version', '0.4.0'),
                           ('independent_validation_claimed', True),
                           ('full_original_requirement_acceptance_claimed', True)]:
            profile = copy.deepcopy(self.profile)
            profile[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                release.validate_profile_blob(profile, self.blob)

    def test_every_final_profile_gate_and_complete_tooling_are_required(self):
        for gate in support.GATES:
            profile = copy.deepcopy(self.profile)
            profile[gate] = False
            with self.subTest(gate=gate), self.assertRaises(ValueError):
                release.validate_profile_blob(profile, self.blob)
        envelope = copy.deepcopy(self.envelope)
        envelope['finalization_tooling_sha256'].pop('tools/prepare_release_v035_final.py')
        profile = copy.deepcopy(self.profile)
        profile['artifact_matrix_sha256'] = digest(encoded(envelope))
        with self.assertRaises(ValueError):
            release.validate_profile_blob(profile, self.changed_blob({release.MATRIX: encoded(envelope)}))

    def test_actual_finalization_registry_and_request_are_scoped_to_dry_freeze(self):
        registry = json.loads(self.blob(release.REGISTRY))
        registry['profiles']['v0.3.5'] = support.PROFILE
        with self.assertRaises(ValueError):
            release.validate_profile_blob(self.profile, self.changed_blob({release.REGISTRY: encoded(registry)}))
        request = json.loads(self.blob(release.REQUEST))
        request['publish'] = True
        with self.assertRaises(ValueError):
            release.validate_profile_blob(self.profile, self.changed_blob({release.REQUEST: encoded(request)}))

    def test_rehashed_critical_screen_cannot_clear_findings_or_invent_review(self):
        for field, value in [('known_unresolved_critical_findings', ['omitted source']),
                             ('new_owner_responses_generated', 1),
                             ('independent_semantic_review_claimed', True),
                             ('material_scientific_change_since_owner_acceptance', True),
                             ('universal_zero_defect_claimed', True),
                             ('source_freeze_executed', True), ('publication_executed', True)]:
            screen = json.loads(self.blob(release.SCREEN))
            screen[field] = value
            profile = copy.deepcopy(self.profile)
            profile['critical_screen_sha256'] = digest(encoded(screen))
            with self.subTest(field=field), self.assertRaises(ValueError):
                release.validate_profile_blob(profile, self.changed_blob({release.SCREEN: encoded(screen)}))

    def test_freshness_requires_the_complete_current_wiki_and_pages_inventory(self):
        release.validate_freshness(self.envelope, self.freshness, self.source)
        for key in ['wiki_files_sha256', 'files_sha256']:
            value = copy.deepcopy(self.freshness)
            value[key].pop(next(iter(value[key])))
            with self.subTest(key=key), self.assertRaises(ValueError):
                release.validate_freshness(self.envelope, value, self.source)
        for path in ['versions/index.html', 'current/index.html', 'releases/v0.3.4/index.html']:
            value = copy.deepcopy(self.freshness)
            value['files_sha256'].pop(path)
            with self.subTest(path=path), self.assertRaises(ValueError):
                release.validate_freshness(self.envelope, value, self.source)
        for mutate in [lambda r: r['http_checks'][0].update(status=404),
                       lambda r: r['http_checks'][0].update(exact_match=False),
                       lambda r: r['http_checks'].__setitem__(-1, copy.deepcopy(r['http_checks'][0])),
                       lambda r: r['wiki_checks'][0].update(sha256='0' * 64),
                       lambda r: r['wiki_checks'].__setitem__(-1, copy.deepcopy(r['wiki_checks'][0]))]:
            value = copy.deepcopy(self.freshness)
            mutate(value)
            with self.subTest(mutation=mutate), self.assertRaises(ValueError):
                release.validate_freshness(self.envelope, value, self.source)

    def test_old_future_wrong_source_or_incomplete_channel_receipt_is_rejected(self):
        now = datetime.now(timezone.utc)
        mutations = [dict(checked_at_utc=(now - timedelta(days=2)).isoformat()),
                     dict(checked_at_utc=(now + timedelta(days=1)).isoformat()),
                     dict(source_commit='0' * 40), dict(documentation_version='0.3.0'),
                     dict(documentation_snapshots=3), dict(wiki_files=22),
                     dict(pages_files=310), dict(all_bytes_match=False),
                     dict(root_manifest_http_status=404), dict(http_responses=311),
                     dict(guide_source_commit='0' * 40)]
        for mutation in mutations:
            value = copy.deepcopy(self.freshness)
            value.update(mutation)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                release.validate_freshness(self.envelope, value, self.source)

    def test_root_manifest_must_name_the_final_source_and_all_deployed_files(self):
        for change in [lambda m: m.update(current_source_commit='0' * 40),
                       lambda m: m.update(current_documentation_version='0.3.0'),
                       lambda m: m.update(releases={}),
                       lambda m: m['current_documentation_projection'].update(documentation_version='0.3.0'),
                       lambda m: m['files_sha256'].pop('.nojekyll'),
                       lambda m: m['files_sha256'].update({'current/index.html': '0' * 64})]:
            value = copy.deepcopy(self.freshness)
            root = json.loads(value['root_manifest_utf8'])
            change(root)
            raw = encoded(root)
            value.update(root_manifest_utf8=raw.decode(), pages_manifest_sha256=digest(raw),
                         rebuilt_manifest_sha256=digest(raw))
            with self.subTest(change=change), self.assertRaises(ValueError):
                release.validate_freshness(self.envelope, value, self.source)

    def test_old_root_manifest_digest_cannot_substitute_for_actual_rebuilt_bytes(self):
        value = copy.deepcopy(self.freshness)
        value['pages_manifest_sha256'] = self.selection['generated_outputs']['root_manifest_sha256']
        value['rebuilt_manifest_sha256'] = value['pages_manifest_sha256']
        with self.assertRaises(ValueError):
            release.validate_freshness(self.envelope, value, self.source)

    def test_actual_six_asset_roundtrip_validates_offline(self):
        with patch('subprocess.Popen', side_effect=AssertionError('Offline package validation cannot spawn Git')), \
                patch('urllib.request.urlopen', side_effect=AssertionError('Offline package validation cannot fetch network')), \
                patch('socket.create_connection', side_effect=AssertionError('Offline package validation cannot fetch network')):
            frozen, manifest = release.validate_package(self.pristine, self.source)
        self.assertEqual(frozen['source_commit'], self.source)
        self.assertFalse(frozen['publication_executed'])
        self.assertEqual(manifest['file_count'], len(self.entries))
        self.assertEqual(len(list(self.pristine.iterdir())), 6)

    def test_archived_cli_validates_six_assets_without_git_history_or_executable(self):
        with tempfile.TemporaryDirectory(dir=self.folder) as temp:
            folder = Path(temp)
            source = folder / 'source'
            source.mkdir()
            for member, raw in self.archive_entries(self.pristine):
                path = member.name.split('/', 1)[1]
                target = source / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
            self.assertFalse((source / '.git').exists())
            env = {**os.environ, 'PATH': str(folder / 'no-executables'), 'PYTHONDONTWRITEBYTECODE': '1'}
            run = subprocess.run([sys.executable, '-B', str(source / 'tools/release_v035_final.py'),
                                  '--check-package', str(self.pristine), '--source-commit', self.source],
                                 env=env, cwd=folder, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            self.assertEqual(json.loads(run.stdout)['tag'], 'v0.3.5')

    def test_reforged_checksum_list_cannot_hide_missing_or_failed_freeze_checks(self):
        for key in ['checks', 'release_specific_checks']:
            with self.subTest(key=key), self.package_copy() as folder:
                self.rewrite_json(folder, 'freeze-receipt.json', lambda r: r[key].pop())
                self.sums(folder)
                with self.assertRaises(ValueError):
                    release.validate_package(folder, self.source)
        with self.package_copy() as folder:
            self.rewrite_json(folder, 'freeze-receipt.json', lambda r: r['checks'][0].update(exit_code=1))
            self.sums(folder)
            with self.assertRaises(ValueError):
                release.validate_package(folder, self.source)

    def test_untrusted_or_wrong_source_core_provenance_is_rejected(self):
        mutations = [dict(source_commit='0' * 40), dict(workflow_conclusion='failure'),
                     dict(artifact_digest_verified=False), dict(archive_verified_against_git=False),
                     dict(github_api_verified=False),
                     dict(checks_reused=27), dict(artifact_sha256='not-a-digest')]
        for mutation in mutations:
            with self.subTest(mutation=mutation), self.package_copy() as folder:
                self.rewrite_json(folder, 'freeze-receipt.json',
                                  lambda r: r['core_evidence_provenance'].update(mutation))
                self.sums(folder)
                with self.assertRaises(ValueError):
                    release.validate_package(folder, self.source)

    def test_recomputed_archive_manifest_cannot_omit_required_migration_or_finalizer(self):
        for path in ['implementation/relational/0.7.0/008_evidence_lifecycle.sql',
                     'tools/prepare_release_v035_final.py']:
            with self.subTest(path=path), self.package_copy() as folder:
                self.rewrite_archive(folder, lambda entries: [(m, raw) for m, raw in entries
                                     if m.name.split('/', 1)[1] != path], update_manifest=True)
                with self.assertRaises(ValueError):
                    release.validate_package(folder, self.source)

    def test_altered_archived_science_or_finalization_profile_is_rejected(self):
        for path in ['ontology/riskium-model.json', release.PROFILE]:
            with self.subTest(path=path), self.package_copy() as folder:
                def transform(entries):
                    return [(m, raw + b'\nchanged\n' if m.name.split('/', 1)[1] == path else raw)
                            for m, raw in entries]
                self.rewrite_archive(folder, transform, update_manifest=True)
                with self.assertRaises((ValueError, json.JSONDecodeError)):
                    release.validate_package(folder, self.source)

    def test_archive_duplicate_paths_links_and_traversal_are_rejected(self):
        for kind in ['duplicate', 'symlink', 'traversal', 'mode']:
            with self.subTest(kind=kind), self.package_copy() as folder:
                def transform(entries):
                    member, raw = copy.copy(entries[0][0]), entries[0][1]
                    if kind == 'symlink':
                        member.name = 'riskium-v0.3.5/link'
                        member.type, member.linkname, member.size = tarfile.SYMTYPE, 'README.md', 0
                        raw = None
                    elif kind == 'traversal':
                        member.name = 'riskium-v0.3.5/../escape'
                    elif kind == 'mode':
                        member.mode = 0o777
                        return [(member, raw), *entries[1:]]
                    return entries + [(member, raw)]
                self.rewrite_archive(folder, transform)
                with self.assertRaises(ValueError):
                    release.validate_package(folder, self.source)

    def test_manifest_duplicates_wrong_source_and_extra_assets_are_rejected(self):
        for mutate in [lambda m: m.update(source_commit='0' * 40),
                       lambda m: (m['files'].append(copy.deepcopy(m['files'][0])),
                                  m.update(file_count=m['file_count'] + 1))]:
            with self.subTest(mutation=mutate), self.package_copy() as folder:
                self.rewrite_json(folder, 'source-manifest.json', mutate)
                self.sums(folder)
                with self.assertRaises(ValueError):
                    release.validate_package(folder, self.source)
        with self.package_copy() as folder:
            (folder / 'extra-asset.txt').write_text('not an approved release asset\n')
            self.sums(folder)
            with self.assertRaises(ValueError):
                release.validate_package(folder, self.source)

    def test_notes_and_artifact_versions_must_bind_the_exact_frozen_source(self):
        with self.package_copy() as folder:
            self.rewrite_json(folder, 'artifact-versions.json', lambda v: v.update(source_commit='0' * 40))
            self.sums(folder)
            with self.assertRaises(ValueError):
                release.validate_package(folder, self.source)
        with self.package_copy() as folder:
            path = folder / 'release-notes.md'
            path.write_text(path.read_text().replace(self.source, '0' * 40))
            self.sums(folder)
            with self.assertRaises(ValueError):
                release.validate_package(folder, self.source)

    def test_freeze_receipt_cannot_promote_independent_or_publication_acceptance(self):
        for field, value in [('publication_executed', True), ('independent_validation', True),
                             ('clean_exact_head', False), ('new_owner_responses_generated', 1)]:
            with self.subTest(field=field), self.package_copy() as folder:
                self.rewrite_json(folder, 'freeze-receipt.json', lambda r: r.update({field: value}))
                self.sums(folder)
                with self.assertRaises(ValueError):
                    release.validate_package(folder, self.source)

    def test_reused_candidate_checks_and_archive_are_bound_to_the_real_git_tree(self):
        checks, manifest = prepare.validate_candidate(self.candidate, ROOT, self.source)
        self.assertEqual(checks, self.checks)
        self.assertEqual(manifest['source_commit'], self.source)
        tracked = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', self.source],
                                          cwd=ROOT, text=True).splitlines()
        self.assertEqual(manifest['file_count'], len(tracked))
        with tempfile.TemporaryDirectory(dir=self.folder) as temp:
            folder = Path(temp) / 'candidate'
            shutil.copytree(self.candidate, folder)
            self.rewrite_json(folder, 'candidate-receipt.json', lambda r: r.update(source_commit='0' * 40))
            self.sums(folder)
            with self.assertRaises(ValueError):
                prepare.validate_candidate(folder, ROOT, self.source)

    def test_consumed_candidate_digest_and_extracted_receipts_cannot_diverge(self):
        self.assertEqual(prepare.verify_candidate_zip(self.candidate_zip, self.candidate,
                                                     self.candidate_digest), self.candidate_digest)
        with self.assertRaises(ValueError):
            prepare.verify_candidate_zip(self.candidate_zip, self.candidate, '0' * 64)
        with tempfile.TemporaryDirectory(dir=self.folder) as temp:
            folder = Path(temp) / 'candidate'
            shutil.copytree(self.candidate, folder)
            self.rewrite_json(folder, 'candidate-receipt.json', lambda r: r['checks'][0].update(stdout='reforged'))
            with self.assertRaises(ValueError):
                prepare.verify_candidate_zip(self.candidate_zip, folder, self.candidate_digest)
        repo = dict(full_name='ArazSaieArasi3/riskium')
        run = dict(id=1, name='Incremental release candidate',
                   path='.github/workflows/incremental-release.yml', status='completed',
                   conclusion='success', event='push', head_branch='main', head_sha=self.source,
                   repository=repo, head_repository=repo)
        artifact = dict(id=2, expired=False, name='riskium-candidate-' + self.source,
                        digest='sha256:' + self.candidate_digest,
                        workflow_run=dict(id=1, head_sha=self.source, head_branch='main'))
        def api(path):
            return run if '/runs/' in path else artifact
        remote = prepare.validate_remote_candidate(self.source, 1, 2, self.candidate_digest, api=api)
        self.assertTrue(remote['github_api_verified'])
        for target, field, value in [(run, 'head_sha', '0' * 40),
                                     (run, 'conclusion', 'failure'),
                                     (artifact, 'digest', 'sha256:' + '0' * 64)]:
            original = target[field]
            try:
                target[field] = value
                with self.subTest(field=field), self.assertRaises(ValueError):
                    prepare.validate_remote_candidate(self.source, 1, 2, self.candidate_digest, api=api)
            finally:
                target[field] = original

    def test_offline_archive_remains_verifiable_months_after_its_fresh_freeze(self):
        later = datetime.now(timezone.utc) + timedelta(days=90)

        class LaterClock(datetime):
            @classmethod
            def now(cls, tz=None):
                return later.astimezone(tz) if tz is not None else later.replace(tzinfo=None)

        # Readback freshness is measured when the source is frozen. A recipient
        # must still be able to verify that unchanged archive months later.
        with patch.object(release, 'datetime', LaterClock):
            frozen, manifest = release.validate_package(self.pristine, self.source)
        self.assertEqual(frozen['source_commit'], self.source)
        self.assertEqual(manifest['file_count'], len(self.entries))
        readback = datetime.fromisoformat(self.freshness['checked_at_utc'])
        for stamp in [readback - timedelta(seconds=1), readback + timedelta(days=2),
                      readback.replace(tzinfo=None)]:
            with self.subTest(frozen_at=stamp), self.package_copy() as folder:
                self.rewrite_json(folder, 'freeze-receipt.json',
                                  lambda r: r.update(frozen_at_utc=stamp.isoformat()))
                self.sums(folder)
                with self.assertRaises(ValueError):
                    release.validate_package(folder, self.source)


if __name__ == '__main__':
    unittest.main()
