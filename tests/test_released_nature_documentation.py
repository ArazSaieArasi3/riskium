"""Check released identity, preservation and source-qualified publisher settlement."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools/publication'))
import released_nature_documentation as reader
import released_nature_main_gate as gate


class ReleasedNatureReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.site = Path(cls.tmp.name) / 'site'
        cls.manifest, cls.wiki, cls.result = reader.build(cls.site)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_released_source_and_model_roles_preserve_history(self):
        status = json.loads((self.site / 'current/published-status.json').read_text())
        self.assertEqual((status['source_release'], status['published_source_commit'], status['model_version']),
                         ('v0.3.7', reader.SOURCE, '0.3.1'))
        self.assertIsNone(status['development_distribution'])
        self.assertEqual((self.result['frozen_snapshots'], len(self.wiki), reader.preserved_inputs()), (4, 23, 903))
        home = BeautifulSoup((self.site / 'current/index.html').read_text(), 'html.parser')
        self.assertIn('v0.3.7 published', home.select_one('.publication-context').get_text(' ', strip=True))
        self.assertNotIn('in preparation', home.get_text(' ', strip=True))

    def test_live_identity_rejects_old_latest_and_wrong_asset_digest(self):
        publication = json.loads(reader.read(reader.ROOT, reader.NS + '/publication.json'))
        latest = dict(tag_name='v0.3.7', id=reader.RELEASE_ID, draft=False, prerelease=False,
                      assets=[dict(name=a['name'], id=a['id'], size=a['bytes'], digest='sha256:' + a['sha256'])
                              for a in publication['assets']])
        def getter(path):
            if path == 'releases/latest':
                return latest
            return dict(object=dict(sha=reader.SOURCE if '/tags/' in path else 'a' * 40,
                                    type='commit', url='verified-api-object'))
        self.assertEqual(reader.verify_live_release(publication, 'a' * 40, getter)['assets'], 6)
        latest['assets'][0]['digest'] = 'sha256:' + '0' * 64
        with self.assertRaisesRegex(ValueError, 'asset identity'):
            reader.verify_live_release(publication, 'a' * 40, getter)
        latest['tag_name'] = 'v0.3.6'
        with self.assertRaisesRegex(ValueError, 'release identity'):
            reader.verify_live_release(publication, 'a' * 40, getter)

    def test_changed_reviewed_guide_and_published_component_are_rejected(self):
        original = reader.read
        def changed(root, path):
            return original(root, path) + (b' changed' if path == reader.NS + '/guides/Home.md' else b'')
        with patch.object(reader, 'read', changed), self.assertRaisesRegex(ValueError, 'Changed reviewed'):
            reader.review()
        def changed_model(root, path):
            return original(root, path) + (b' changed' if path == 'ontology/riskium-model.json' else b'')
        with patch.object(reader, 'read', changed_model), self.assertRaisesRegex(ValueError, 'Published component'):
            reader.preserved_inputs()

    def test_deploy_waits_for_old_publishers_and_requires_new_suite(self):
        def run(name, status='completed', conclusion='failure'):
            return dict(id=len(name), name=name, head_sha='a' * 40, head_branch='main', event='push',
                        status=status, conclusion=conclusion)
        runs = [run(name) for name in (gate.DOCUMENTATION, gate.INCREMENTAL, gate.OLD_SUITE, gate.PUBLISHED)]
        runs.append(run(gate.SUITE, conclusion='success'))
        self.assertEqual(gate.settled(runs, 'a' * 40, 999), [])
        runs.append(run(gate.OLD_READER, status='in_progress', conclusion=None))
        self.assertIn('Running: ' + gate.OLD_READER, gate.settled(runs, 'a' * 40, 999))
        runs.pop()
        runs[-1]['conclusion'] = 'failure'
        with self.assertRaisesRegex(ValueError, 'Source-qualified suite failed'):
            gate.settled(runs, 'a' * 40, 999)


if __name__ == '__main__':
    unittest.main()
