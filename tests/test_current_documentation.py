"""Check the new projection and meaningful malformed source/version boundaries."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools/publication'))
import current_documentation as current


class CurrentDocumentation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.site = Path(cls.temp.name) / 'site'
        cls.descriptor, cls.wiki, cls.result = current.build(cls.site)
        cls.policy, cls.selection, cls.rows = current.review()

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_actual_full_site_keeps_all_four_frozen_snapshots(self):
        self.assertEqual(self.result['frozen_snapshots'], 4)
        self.assertEqual(self.result['status'], 'VERSIONED_DOCUMENTATION_PASS')
        self.assertEqual(self.descriptor['prior_published_file_bindings_preserved'], 380)
        self.assertEqual(self.descriptor['shared_guides'], 21)
        self.assertEqual(len(self.wiki), 23)
        current.checked_component(self.descriptor)
        current.check_wiki_sources(self.wiki)

    def test_all_actual_current_headers_and_guide_bodies_match_new_version(self):
        pages = list((self.site / 'current').rglob('*.html')) + [self.site / 'versions/index.html']
        self.assertEqual(len(pages), 31)
        for path in pages:
            current.check_header(BeautifulSoup(path.read_text(), 'html.parser'))
        for row in self.rows:
            soup = BeautifulSoup((self.site / 'current/guide' / (row['slug'] + '.html')).read_text(), 'html.parser')
            self.assertIn(current.sha(current.read_bytes(current.ROOT, row['source'])), soup.select_one('main').get_text())
            self.assertIn(self.selection['guide_source_commit'], self.wiki[row['wiki_slug'] + '.md'])

    def test_same_source_link_projects_to_registered_pages_and_native_wiki(self):
        self.assertEqual(current.internal_link('Decisions.md#cases', self.rows), 'Decisions.html#cases')
        self.assertEqual(current.internal_link('Decisions.md#cases', self.rows, wiki=True), 'Modeling-Decisions#cases')
        self.assertEqual(current.internal_link('https://example.org/source', self.rows), 'https://example.org/source')

    def test_unknown_or_escaping_guide_link_is_rejected(self):
        for value in ('Missing.md', '../Home.md', '/Home.md', 'Home.html'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                current.internal_link(value, self.rows)

    def test_duplicate_and_unsafe_registry_cannot_drop_a_guide(self):
        duplicate = copy.deepcopy(self.rows)
        duplicate[-1] = duplicate[0]
        with self.assertRaisesRegex(ValueError, 'Duplicate guide'):
            current.validate_registry(duplicate)
        unsafe = copy.deepcopy(self.rows)
        unsafe[0]['wiki_slug'] = '../Home'
        with self.assertRaisesRegex(ValueError, 'Unsafe guide slug'):
            current.validate_registry(unsafe)

    def test_changed_reviewed_guide_cannot_reuse_checkpoint(self):
        original = current.read_bytes
        target = self.rows[0]['source']
        def changed(root, path):
            return b'# Changed without review\n' if path == target else original(root, path)
        with patch.object(current, 'read_bytes', side_effect=changed), self.assertRaisesRegex(ValueError, 'Changed reviewed guide'):
            current.review()

    def test_stale_active_release_claim_is_rejected(self):
        for text in ('v0.3.4 is planned, not frozen', 'Next publication #45 must freeze', 'v0.3.4 preparation'):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'Stale active publication prose'):
                current.reject_stale(text)

    def test_wrong_current_header_is_rejected(self):
        soup = BeautifulSoup((self.site / 'current/index.html').read_text(), 'html.parser')
        soup.select_one('div.publication-context strong').string = '0.3.0'
        with self.assertRaisesRegex(ValueError, 'Wrong current documentation header'):
            current.check_header(soup)


if __name__ == '__main__':
    unittest.main()
