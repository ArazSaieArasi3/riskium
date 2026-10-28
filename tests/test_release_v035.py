"""Prospective v0.3.5 support and actual unpacked-source trust boundaries.

Temporary archives/manifests below are software fixtures, not a freeze,
publication, channel readback or independent scientific review receipt.
"""
import copy
from contextlib import contextmanager
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import release_v035 as release


def encoded(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


class Release035Support(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = json.loads((ROOT / release.PROFILE).read_bytes())
        cls.matrix = json.loads((ROOT / release.MATRIX).read_bytes())
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.folder = Path(cls.temporary.name)
        cls.unpacked = cls.folder / 'source'
        cls.unpacked.mkdir()
        # A temporary index archives pending local delivery files as well as the
        # tracked tree. It never stages changes in the developer's real index.
        env = {**os.environ, 'GIT_INDEX_FILE': str(cls.folder / 'fixture-index')}
        subprocess.run(['git', 'read-tree', 'HEAD'], cwd=ROOT, env=env, check=True)
        subprocess.run(['git', 'add', '--all'], cwd=ROOT, env=env, check=True)
        tree = subprocess.check_output(['git', 'write-tree'], cwd=ROOT, env=env, text=True).strip()
        archive = subprocess.check_output(['git', 'archive', '--format=tar', tree], cwd=ROOT)
        with tarfile.open(fileobj=io.BytesIO(archive)) as source:
            for member in source:
                if member.isdir():
                    continue
                if not member.isfile() or Path(member.name).is_absolute() or '..' in Path(member.name).parts:
                    raise AssertionError('Unsafe generated fixture archive')
                target = cls.unpacked / member.name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.extractfile(member).read())
        cls.source = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        cls.manifest = cls.inventory()

    @classmethod
    def inventory(cls):
        records = [dict(path=p.relative_to(cls.unpacked).as_posix(), bytes=len(p.read_bytes()),
                        sha256=digest(p.read_bytes()))
                   for p in sorted(cls.unpacked.rglob('*')) if p.is_file()]
        return dict(schema='riskium-stable-source-inventory-v1', tag='v0.3.5',
                    source_commit=cls.source, file_count=len(records), files=records)

    @staticmethod
    def blob(path):
        return (ROOT / path).read_bytes()

    def changed_blob(self, replacements):
        return lambda path: replacements[path] if path in replacements else self.blob(path)

    @contextmanager
    def removed_file(self, path):
        target = self.unpacked / path
        data = target.read_bytes()
        target.unlink()
        try:
            yield
        finally:
            target.write_bytes(data)

    def test_actual_prospective_profile_preserves_selected_versions(self):
        self.assertEqual(release.validate_profile(ROOT)['tag'], 'v0.3.5')
        release.validate_profile_blob(self.profile, self.blob)
        release.validate_matrix(self.matrix, self.blob)
        self.assertEqual(len(self.matrix['artifacts']), 29)
        self.assertEqual(len(self.matrix['selected_files_sha256']), 687)
        self.assertEqual(sum(map(len, self.matrix['dependencies'].values())), 68)

    def test_real_unpacked_archive_validates_without_git_or_network(self):
        self.assertFalse((self.unpacked / '.git').exists())
        with patch('subprocess.Popen', side_effect=AssertionError('No process execution during offline validation')), \
                patch('urllib.request.urlopen', side_effect=AssertionError('No network during offline validation')), \
                patch('socket.create_connection', side_effect=AssertionError('No network during offline validation')):
            result = release.validate_unpacked(self.unpacked, self.manifest)
        self.assertIsInstance(result, dict)
        self.assertTrue(result['complete_manifest_verified'])
        self.assertFalse(result['source_commit_authenticated'])
        self.assertFalse(result['publication_executed'])
        self.assertFalse(result['source_freeze_executed'])

    def test_unpacked_cli_works_with_no_git_executable_and_no_history(self):
        manifest = self.folder / 'manifest.json'
        manifest.write_bytes(encoded(self.manifest))
        env = {**os.environ, 'PATH': str(self.folder / 'no-executables'), 'PYTHONDONTWRITEBYTECODE': '1'}
        result = subprocess.run([sys.executable, str(self.unpacked / 'tools/prepare_release_v035.py'),
                                 '--check-unpacked', str(self.unpacked), '--manifest', str(manifest)],
                                cwd=self.folder, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        status = json.loads(result.stdout)
        self.assertFalse(status['publication_executed'])
        self.assertFalse(status['source_freeze_executed'])
        self.assertTrue(status['complete_manifest_verified'])

    def test_missing_or_altered_selected_payload_is_rejected(self):
        path = 'tools/relational_evidence_lifecycle.py'
        with self.assertRaises(ValueError):
            release.validate_matrix(self.matrix, self.changed_blob({path: b'# substituted executable\n'}))
        with self.removed_file(path), self.assertRaises(ValueError):
            release.validate_unpacked(self.unpacked)

    def test_recomputed_manifest_cannot_omit_critical_runtime_or_release_tooling(self):
        paths = ['tools/relational_evidence_lifecycle.py',
                 'implementation/relational/0.7.0/008_evidence_lifecycle.sql',
                 'tools/prepare_release_v035.py']
        for path in paths:
            with self.subTest(path=path), self.removed_file(path):
                forged = self.inventory()
                self.assertNotIn(path, {r['path'] for r in forged['files']})
                with self.assertRaises(ValueError):
                    release.validate_unpacked(self.unpacked, forged)

    def test_changed_scope_dependencies_history_and_migration_are_rejected(self):
        changes = [
            lambda m: m['boundaries'].update(independent_validation_claimed=True),
            lambda m: m['historical_generation_dependencies']['DOCUMENTATION_SNAPSHOT'][-1].update(version='0.4.0'),
            lambda m: m['dependencies']['DOCUMENTATION'].pop(),
            lambda m: m['sqlite_migration_chain'].pop(),
            lambda m: m['artifacts'].pop(),
        ]
        for change in changes:
            value = copy.deepcopy(self.matrix)
            change(value)
            with self.subTest(change=change), self.assertRaises(ValueError):
                release.validate_matrix(value, self.changed_blob({release.MATRIX: encoded(value)}))

    def test_wrong_source_or_version_receipt_is_not_rebound_by_new_hashes(self):
        path = 'evaluation/releases/v0.3.5-selection/inputs/documentation-http.json'
        for field, value in [('source_commit', '0' * 40), ('documentation_version', '0.3.0')]:
            receipt = json.loads(self.blob(path))
            receipt[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                release.validate_matrix(self.matrix, self.changed_blob({path: encoded(receipt)}))

    def test_missing_profile_tooling_is_rejected_even_with_matching_screen_map(self):
        profile = copy.deepcopy(self.profile)
        profile['release_tooling_sha256'].pop('tools/prepare_release_v035.py')
        screen = json.loads(self.blob(release.SCREEN))
        screen['release_tooling_sha256'] = profile['release_tooling_sha256']
        with self.assertRaises(ValueError):
            release.validate_profile_blob(profile, self.changed_blob({release.SCREEN: encoded(screen)}))

    def test_changed_release_tooling_and_release_notes_are_rejected(self):
        for path in ['tools/prepare_release_v035.py', release.NOTES]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                release.validate_profile_blob(self.profile, self.changed_blob({path: self.blob(path) + b'altered\n'}))

    def test_every_final_publication_and_offline_validation_gate_remains_required(self):
        for gate in release.GATES:
            profile = copy.deepcopy(self.profile)
            profile[gate] = False
            with self.subTest(gate=gate), self.assertRaises(ValueError):
                release.validate_profile_blob(profile, self.blob)

    def test_profile_cannot_promote_stage_native_version_or_acceptance(self):
        mutations = [('stage', 'FROZEN'), ('registered_for_publication', True),
                     ('model_version', '0.4.0'), ('independent_validation_claimed', True),
                     ('full_original_requirement_acceptance_claimed', True)]
        for field, value in mutations:
            profile = copy.deepcopy(self.profile)
            profile[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                release.validate_profile_blob(profile, self.blob)

    def test_critical_findings_or_fabricated_review_cannot_be_cleared(self):
        for field, value in [('known_unresolved_critical_findings', ['missing closure']),
                             ('new_owner_responses_generated', 1),
                             ('independent_semantic_review_claimed', True),
                             ('source_freeze_executed', True),
                             ('publication_executed', True),
                             ('selection_source_commit', '0' * 40),
                             ('future_freeze_gates', ['unexplained'] * 5)]:
            screen = json.loads(self.blob(release.SCREEN))
            screen[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                release.validate_profile_blob(self.profile, self.changed_blob({release.SCREEN: encoded(screen)}))

    def test_prospective_support_rejects_publication_registration_or_request(self):
        for path in ['releases/stable-profiles.json', 'releases/successor-profiles.json']:
            register = json.loads(self.blob(path))
            register['profiles']['v0.3.5'] = release.PROFILE
            with self.subTest(path=path), self.assertRaises(ValueError):
                release.validate_profile_blob(self.profile, self.changed_blob({path: encoded(register)}))
        path = 'releases/stable-request-v0.3.5.json'
        request = encoded(dict(schema='riskium-reviewed-successor-request-v1', tag='v0.3.5',
                               profile='stable-bounded-research-artifact', publish=True))
        target = self.unpacked / path
        try:
            target.write_bytes(request)
            with self.assertRaises(ValueError):
                release.validate_unpacked(self.unpacked, self.inventory())
        finally:
            target.unlink()

    def test_duplicate_unsafe_absolute_and_git_manifest_paths_are_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest['files'].append(copy.deepcopy(manifest['files'][0]))
        manifest['file_count'] += 1
        with self.assertRaises(ValueError):
            release.validate_source_manifest(manifest, lambda p: (self.unpacked / p).read_bytes())
        for path in ['../secret', '/etc/passwd', 'tools\\escape.py', '.git/config']:
            manifest = copy.deepcopy(self.manifest)
            manifest['files'][0]['path'] = path
            with self.subTest(path=path), self.assertRaises(ValueError):
                release.validate_source_manifest(manifest, lambda p: (self.unpacked / p).read_bytes())

    def test_manifest_identity_count_size_and_hash_are_checked(self):
        for change in [lambda m: m.update(file_count=m['file_count'] + 1),
                       lambda m: m.update(tag='v0.3.4'),
                       lambda m: m.update(source_commit='unreviewed'),
                       lambda m: m['files'][0].update(bytes=m['files'][0]['bytes'] + 1),
                       lambda m: m['files'][0].update(sha256='0' * 64)]:
            manifest = copy.deepcopy(self.manifest)
            change(manifest)
            with self.subTest(change=change), self.assertRaises(ValueError):
                release.validate_source_manifest(manifest, lambda p: (self.unpacked / p).read_bytes())

    def test_full_manifest_rejects_extra_untracked_file(self):
        target = self.unpacked / 'unlisted-source.py'
        try:
            target.write_text('# excluded from the downloaded manifest\n')
            with self.assertRaises(ValueError):
                release.validate_unpacked(self.unpacked, self.manifest)
        finally:
            target.unlink()

    def test_unpacked_reader_rejects_symlink_even_without_manifest(self):
        target = self.unpacked / 'linked-source'
        try:
            target.symlink_to(self.unpacked / 'README.md')
            with self.assertRaises(ValueError):
                release.validate_unpacked(self.unpacked)
        finally:
            target.unlink()

    def test_unpacked_validation_rejects_retained_git_history(self):
        target = self.unpacked / '.git'
        try:
            target.mkdir()
            with self.assertRaises(ValueError):
                release.validate_unpacked(self.unpacked)
        finally:
            target.rmdir()


if __name__ == '__main__':
    unittest.main()
