"""A maintained reader must bind a real release and preserve frozen source roles."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools/publication'))
import released_documentation as reader
import released_main_gate as gate


class PublishedReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.site = Path(cls.tmp.name) / 'site'
        cls.manifest, cls.wiki, cls.result = reader.build(cls.site)
        cls.publication = json.loads(reader.read(reader.ROOT, reader.NS + '/publication.json'))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_current_views_have_one_released_state_and_keep_snapshot_roles(self):
        self.assertEqual(self.result['status'], 'PUBLISHED_READER_PROJECTION_PASS')
        self.assertEqual(self.result['frozen_snapshots'], 4)
        self.assertEqual(self.result['preserved_selected_files'], 779)
        self.assertEqual(len(self.wiki), 23)
        state = json.loads((self.site / 'current/published-status.json').read_text())
        self.assertEqual((state['source_release'], state['documentation_version']), ('v0.3.6', '0.4.3'))
        self.assertFalse(state['new_source_distribution'])
        self.assertFalse(state['independent_semantic_acceptance'])
        maintained = list((self.site / 'current').rglob('*.html')) + [self.site / 'versions/index.html']
        self.assertEqual(len(maintained), 31)
        for path in maintained:
            soup = BeautifulSoup(path.read_text(), 'html.parser')
            header = soup.select_one('div.publication-context').get_text(' ', strip=True)
            self.assertIn('0.4.3', header)
            self.assertIn('v0.3.6 published', header)
        self.assertIn('v0.3.6', self.wiki['Home.md'])
        self.assertNotIn('is being prepared', self.wiki['Home.md'])
        self.assertIn('WITHDRAWN', self.wiki['Database-Assurance.md'])
        self.assertIn('V036_SIX_ASSET_OFFLINE_PASS', self.wiki['Reproduce.md'])
        self.assertEqual(self.manifest['published_reader_projection']['active_repository_readme'],
                         'documentation/0.4.3/Repository.md')

    def live_fixture(self):
        latest = dict(tag_name='v0.3.6', id=428331704, draft=False, prerelease=False,
                      assets=[dict(name=a['name'], id=a['id'], size=a['bytes'], digest='sha256:' + a['sha256'])
                              for a in self.publication['assets']])
        return {'releases/latest': latest,
                'git/ref/tags/v0.3.6': dict(object=dict(sha=reader.SOURCE, type='commit', url='exact-tag')),
                'git/ref/heads/main': dict(object=dict(sha='documentation-source'))}

    def test_wrong_release_tag_main_or_asset_cannot_reach_publication_gate(self):
        good = self.live_fixture()
        self.assertEqual(reader.verify_live_release(self.publication, 'documentation-source', good.__getitem__)['assets'], 6)
        for kind in ('release', 'draft', 'prerelease', 'tag', 'main', 'digest', 'inventory'):
            data = copy.deepcopy(good)
            if kind == 'release': data['releases/latest']['id'] = 1
            elif kind in ('draft', 'prerelease'): data['releases/latest'][kind] = True
            elif kind == 'tag': data['git/ref/tags/v0.3.6']['object']['sha'] = 'wrong'
            elif kind == 'main': data['git/ref/heads/main']['object']['sha'] = 'newer-source'
            elif kind == 'digest': data['releases/latest']['assets'][0]['digest'] = 'sha256:changed'
            else: data['releases/latest']['assets'].pop()
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                reader.verify_live_release(self.publication, 'documentation-source', data.__getitem__)

    def test_guide_edits_require_new_reviewed_bindings(self):
        original = reader.read
        def changed(root, path):
            data = original(root, path)
            return data + b'changed' if path.endswith('/guides/Home.md') else data
        with patch.object(reader, 'read', changed), self.assertRaisesRegex(ValueError, 'Changed reviewed reader'):
            reader.review()

    def test_outstanding_old_candidate_attempt_blocks_the_new_deployment(self):
        runs = [dict(id=i, name=name, head_sha='source', head_branch='main',
                     event='push', status='completed', conclusion='success' if name == gate.SUITE else 'failure')
                for i, name in enumerate((gate.DOCUMENTATION, gate.INCREMENTAL, gate.SUITE, gate.PUBLISHED), 1)]
        self.assertEqual(gate.settled(runs, 'source', 99, {gate.PAGES, gate.STATUS, gate.CURRENT}), [])
        runs.append(dict(id=88, name=gate.CANDIDATE, head_sha='source', head_branch='main',
                         event='workflow_run', status='in_progress', conclusion=None))
        self.assertIn('Running: ' + gate.CANDIDATE,
                      gate.settled(runs, 'source', 99, {gate.PAGES, gate.STATUS, gate.CURRENT}))


if __name__ == '__main__':
    unittest.main()
