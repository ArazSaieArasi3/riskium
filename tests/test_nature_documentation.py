"""Check source roles and reject misleading reader projections before publication."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools/publication'))
import nature_documentation as reader
import build_nature_reader_bindings as bindings


class NatureReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.site = Path(cls.tmp.name) / 'site'
        cls.manifest, cls.wiki, cls.result = reader.build(cls.site)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_published_and_development_roles_and_snapshots(self):
        self.assertEqual(self.result['frozen_snapshots'], 4)
        self.assertEqual(len(self.wiki), 23)
        state = json.loads((self.site / 'current/published-status.json').read_text())
        self.assertEqual(state['documentation_version'], '0.4.4')
        self.assertEqual(state['source_release'], 'v0.3.6')
        self.assertEqual(state['development_distribution'], 'v0.3.7')
        self.assertFalse(state['new_source_distribution'])
        self.assertIn('executed development', self.wiki['Home.md'])
        self.assertIn('NOT_READY_CONTEXT_UNRECORDED', self.wiki['Reproduce.md'])

    def test_declared_journeys_land_on_real_guide_fragments(self):
        plan = json.loads(reader.read(reader.ROOT, reader.NS + '/review-plan.json'))
        for path in plan['audience_paths'].values():
            for slug in path:
                self.assertTrue((self.site / 'current/guide' / (slug + '.html')).is_file())
        home = BeautifulSoup((self.site / 'current/index.html').read_text(), 'html.parser')
        self.assertIn('v0.3.7 in preparation', home.select_one('.publication-context').get_text(' ', strip=True))
        for slug, fragment in [('Using-the-Model', 'risk-nature-history'), ('Database-Assurance', 'risk-nature-retrieval'), ('Reproduce', 'risk-nature-example')]:
            soup = BeautifulSoup((self.site / 'current/guide' / (slug + '.html')).read_text(), 'html.parser')
            self.assertIsNotNone(soup.find(id=fragment))
            self.assertTrue(all(t.has_attr('tabindex') for t in soup.select('main table')))

    def test_all_source_bindings_and_mutation_rejection(self):
        for path, expected in bindings.build().items():
            self.assertEqual((reader.ROOT / path).read_text(), expected)
        original = reader.read
        def changed(root, path):
            raw = original(root, path)
            return raw + b' altered' if path == reader.NS + '/guides/Home.md' else raw
        with patch.object(reader, 'read', changed), self.assertRaisesRegex(ValueError, 'Changed reviewed reader source'):
            reader.review()

    def test_release_gate_rejects_development_as_latest(self):
        publication = json.loads(reader.read(reader.ROOT, reader.NS + '/publication.json'))
        def wrong(path):
            return dict(tag_name='v0.3.7', id=1, draft=False, prerelease=False)
        with self.assertRaisesRegex(ValueError, 'Live published release identity changed'):
            reader.verify_live_release(publication, 'source', wrong)


if __name__ == '__main__':
    unittest.main()
