"""The candidate projection keeps the public release identity and four snapshots."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools/publication'))
import assessment_documentation as docs


class CandidateReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.site = Path(cls.tmp.name) / 'site'
        cls.manifest, cls.wiki, cls.result = docs.build(cls.site)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_projections_have_correct_source_roles_and_reader_example(self):
        self.assertEqual(self.result['status'], 'CANDIDATE_READER_PROJECTION_PASS')
        self.assertEqual(self.result['frozen_snapshots'], 4)
        self.assertEqual(self.result['preserved_selected_files'], 687)
        self.assertEqual(len(self.wiki), 23)
        self.assertEqual(len(list((self.site / 'current').rglob('*.html'))) + 1, 31)
        home = BeautifulSoup((self.site / 'current/index.html').read_text(), 'html.parser').get_text(' ', strip=True)
        database = BeautifulSoup((self.site / 'current/guide/Database-Assurance.html').read_text(), 'html.parser').get_text(' ', strip=True)
        self.assertIn('v0.3.5', home)
        self.assertIn('v0.3.6', home)
        self.assertIn('WITHDRAWN', database)
        self.assertIn('NO_SELECTION', database)
        self.assertIn('A-v3', database)
        self.assertIn('v0.3.5 published', home)
        self.assertIn('v0.3.6', self.wiki['Home.md'])

    def test_manifest_does_not_promote_release_or_active_readme(self):
        state = json.loads((self.site / 'current/published-status.json').read_text())
        self.assertEqual(state['source_release'], 'v0.3.5')
        self.assertEqual(state['documentation_version'], '0.4.2')
        self.assertFalse(state['new_source_distribution'])
        self.assertEqual(self.manifest['published_reader_projection']['active_repository_readme'],
                         'documentation/0.4.1/Repository.md')
        self.assertEqual(self.manifest['published_reader_projection']['candidate_repository_readme'],
                         'documentation/0.4.2/Repository.md')


if __name__ == '__main__':
    unittest.main()
