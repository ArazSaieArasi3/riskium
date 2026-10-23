"""Release boundary tests: tracked-source fidelity, untracked exclusion and maturity."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest

path = Path(__file__).resolve().parents[1] / 'tools/prepare_incremental_release.py'
spec = importlib.util.spec_from_file_location('incremental', path)
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)
request_path = path.with_name('resolve_release_request.py')
request_spec = importlib.util.spec_from_file_location('release_intent', request_path)
intent = importlib.util.module_from_spec(request_spec)
request_spec.loader.exec_module(intent)


class IncrementalRelease(unittest.TestCase):
    def test_archive_uses_committed_bytes_and_excludes_private_untracked_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'repo'; root.mkdir()
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / 'ontology').mkdir()
            (root / 'ontology/riskium-model.json').write_text(json.dumps({'version': '0.3.1'}))
            (root / 'tracked.txt').write_text('committed public evidence\n')
            (root / 'docs').mkdir()
            (root / 'docs/prerelease-v0.3.1-rc.2.md').write_text('Approved release-specific notes\n')
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Release Test', '-c',
                            'user.email=release-test@example.invalid', 'commit', '-qm', 'fixture'], check=True)
            (root / 'tracked.txt').write_text('uncommitted replacement\n')
            (root / 'docs/prerelease-v0.3.1-rc.2.md').write_text('Uncommitted notes must not leak\n')
            (root / 'private.sqlite').write_text('must never be packaged')
            one, two = Path(folder) / 'one', Path(folder) / 'two'
            release.snapshot(root, 'HEAD', one, 'v0.3.1-rc.2')
            release.snapshot(root, 'HEAD', two, 'v0.3.1-rc.2')
            a = one / 'riskium-v0.3.1-rc.2-source.tar.gz'
            self.assertEqual(a.read_bytes(), (two / a.name).read_bytes())
            notes = (one / 'release-notes.md').read_text()
            self.assertIn('Approved release-specific notes', notes)
            self.assertNotIn('Uncommitted notes', notes)
            with tarfile.open(a) as tar:
                self.assertEqual(tar.extractfile('riskium-v0.3.1-rc.2/tracked.txt').read(), b'committed public evidence\n')
                self.assertFalse(any('private.sqlite' in n for n in tar.getnames()))

    def test_stable_or_other_model_version_cannot_be_published_by_this_profile(self):
        for tag in ['v0.3.1', 'v0.3.2-rc.1', 'v0.3.1-rc.0', '../release', 'v0.3.1-rc.2;echo bad']:
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                release.require_prerelease(tag, '0.3.1')
        release.require_prerelease('v0.3.1-rc.2', '0.3.1')

    def test_checked_preparation_refuses_uncommitted_changes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / 'unreviewed.txt').write_text('pending change')
            with self.assertRaisesRegex(ValueError, 'clean source checkout'):
                release.run_checks(root)


class ReleaseIntent(unittest.TestCase):
    def commit(self, root):
        subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(root), '-c', 'user.name=Release Test', '-c',
                        'user.email=release-test@example.invalid', 'commit', '-qm', 'fixture'], check=True)
        return subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip()

    def test_changed_request_publishes_but_later_unrelated_push_does_not(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / 'docs').mkdir()
            (root / 'docs/prerelease-v0.3.1-rc.2.md').write_text('reviewed notes')
            before = self.commit(root)
            (root / 'releases').mkdir()
            (root / intent.REQUEST).write_text(json.dumps({'profile': 'development-prerelease',
                                                          'publish': True, 'tag': 'v0.3.1-rc.2'}))
            after = self.commit(root)
            self.assertEqual(intent.resolve(root, 'push', 'refs/heads/main', before, after),
                             {'release_tag': 'v0.3.1-rc.2', 'publish': True})
            (root / 'docs/unrelated.md').write_text('ordinary later documentation')
            later = self.commit(root)
            self.assertEqual(intent.resolve(root, 'push', 'refs/heads/main', after, later),
                             {'release_tag': '', 'publish': False})

    def test_manual_publication_rejects_stable_tags_and_non_main_refs(self):
        for ref, tag in [('refs/heads/main', 'v0.3.1'), ('refs/heads/topic', 'v0.3.1-rc.2'),
                         ('refs/heads/main', 'v0.3.1-rc.2\npublish=true')]:
            with self.subTest(ref=ref, tag=tag), self.assertRaises(ValueError):
                intent.resolve('.', 'workflow_dispatch', ref, '', 'HEAD',
                               {'release_tag': tag, 'publish': True})

    def test_publication_requires_committed_release_specific_notes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / 'readme').write_text('no release notes')
            after = self.commit(root)
            with self.assertRaises(subprocess.CalledProcessError):
                intent.resolve(root, 'workflow_dispatch', 'refs/heads/main', '', after,
                               {'release_tag': 'v0.3.1-rc.2', 'publish': True})
