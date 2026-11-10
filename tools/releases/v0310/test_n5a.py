"""Composition, preserved history and source-routing controls."""
import copy
import os
import shutil
import tempfile
import unittest
from pathlib import Path
import yaml
import curation
import compose
import routing


class N5aContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = Path(os.environ['RISKIUM_N5A_TEST_COMPOSITION'])
        cls.manifest = curation.load(cls.base / 'site/publication-manifest.json')
        cls.tmp = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def work(self):
        p = Path(self.tmp.name) / self._testMethodName
        # Independent copies also work when the fixture and temp directory use different filesystems.
        shutil.copytree(self.base, p)
        self.addCleanup(shutil.rmtree, p)
        return p

    def replace(self, p, text):
        p.unlink()
        p.write_text(text)

    def update(self, root, name, wiki=False):
        p = root / 'site/publication-manifest.json'
        m = curation.load(p)
        m['wiki_files_sha256' if wiki else 'files_sha256'][name] = curation.sha((root / ('wiki' if wiki else 'site') / name).read_bytes())
        self.replace(p, curation.dump(m))

    def test_complete_reader_guides_and_historical_native_reference(self):
        self.assertEqual(len(self.manifest['pairs']), 111)
        self.assertEqual(len(self.manifest['retained_guides']), 20)
        self.assertEqual(len(self.manifest['wiki_files_sha256']), 114)
        self.assertEqual(len(self.manifest['historical_wiki_sha256']), 1)

    def test_legacy_write_is_disabled_without_changing_its_steps(self):
        d = {'permissions': {'contents': 'read'}, 'jobs': {'publish': {'permissions': {'contents': 'write'}, 'if': 'old', 'steps': [{'run': 'original command'}]}}}
        expected, roles = routing.expected(d)
        self.assertEqual(expected['jobs']['publish']['if'], '${{ false }}')
        self.assertEqual(expected['jobs']['publish']['steps'], d['jobs']['publish']['steps'])
        self.assertEqual(roles['publish'], 'DISABLED_LEGACY_WRITE')

    def test_read_only_replay_is_pinned_without_changing_oracle(self):
        d = {'jobs': {'suite': {'steps': [{'uses': 'actions/checkout@v4'}, {'run': 'original oracle'}]}}}
        e, _ = routing.expected(d)
        self.assertEqual(e['jobs']['suite']['steps'][0]['with']['ref'], routing.HISTORICAL)
        self.assertEqual(e['jobs']['suite']['steps'][1], d['jobs']['suite']['steps'][1])

    def test_historical_snapshot_change_rejected_after_rehash(self):
        p = self.work()
        name = next(n for n in self.manifest['frozen_snapshot_sha256'] if n.endswith('.html'))
        f = p / 'site' / name
        self.replace(f, f.read_text() + '\nchanged\n')
        self.update(p, name)
        with self.assertRaisesRegex(ValueError, 'Frozen snapshot changed'):
            compose.audit(p)

    def test_missing_retained_guide_rejected(self):
        p = self.work()
        (p / 'wiki/Using-the-Model.md').unlink()
        with self.assertRaisesRegex(ValueError, 'Wiki inventory'):
            compose.audit(p)

    def test_historical_wiki_change_rejected_after_rehash(self):
        p = self.work(); f = p / 'wiki/References.md'
        self.replace(f, f.read_text() + '\nchanged\n'); self.update(p, 'References.md', True)
        with self.assertRaisesRegex(ValueError, 'Historical Wiki reference changed'):
            compose.audit(p)

    def test_changed_wiki_semantics_rejected_after_rehash(self):
        p = self.work(); f = p / 'wiki/Home.md'
        self.replace(f, f.read_text().replace('## Choose a reading path', '## Unsupported meaning', 1))
        self.update(p, 'Home.md', True)
        with self.assertRaisesRegex(ValueError, 'text parity'):
            compose.audit(p)

    def test_premature_channel_readback_claim_rejected(self):
        p = self.work(); f = p / 'site/publication-manifest.json'; m = curation.load(f)
        m['live_channel_readback'] = True; self.replace(f, curation.dump(m))
        with self.assertRaisesRegex(ValueError, 'Premature channel acceptance'):
            compose.audit(p)

    def test_broken_composed_route_rejected_after_rehash(self):
        p = self.work(); name = 'current/guide/Home.html'; f = p / 'site' / name
        self.replace(f, f.read_text().replace('href="' + compose.SITE + '/current/concepts/index.html"', 'href="Missing.html"', 1))
        self.update(p, name)
        with self.assertRaisesRegex(ValueError, 'Missing composed HTML target'):
            compose.audit(p)


if __name__ == '__main__':
    unittest.main(verbosity=2)
