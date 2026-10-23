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


class IncrementalRelease(unittest.TestCase):
    def test_archive_uses_committed_bytes_and_excludes_private_untracked_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'repo'; root.mkdir()
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / 'ontology').mkdir()
            (root / 'ontology/riskium-model.json').write_text(json.dumps({'version': '0.3.1'}))
            (root / 'tracked.txt').write_text('committed public evidence\n')
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Release Test', '-c',
                            'user.email=release-test@example.invalid', 'commit', '-qm', 'fixture'], check=True)
            (root / 'tracked.txt').write_text('uncommitted replacement\n')
            (root / 'private.sqlite').write_text('must never be packaged')
            one, two = Path(folder) / 'one', Path(folder) / 'two'
            release.snapshot(root, 'HEAD', one, 'v0.3.1-rc.2')
            release.snapshot(root, 'HEAD', two, 'v0.3.1-rc.2')
            a = one / 'riskium-v0.3.1-rc.2-source.tar.gz'
            self.assertEqual(a.read_bytes(), (two / a.name).read_bytes())
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
