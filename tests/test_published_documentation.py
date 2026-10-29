"""Protect publication identity, historical evidence and reader navigation."""
import copy
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools/publication'))
import published_documentation as docs


class PublishedReaderDocumentation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.site = Path(cls.temp.name) / 'site'
        cls.manifest, cls.wiki, cls.result = docs.build(cls.site)
        cls.rows, cls.policy, cls.publication = docs.review()

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_current_surfaces_preserve_frozen_inputs_and_correct_published_status(self):
        self.assertEqual(self.result['frozen_snapshots'], 4)
        self.assertEqual(self.result['preserved_selected_files'], 687)
        self.assertEqual(len(self.wiki), 23)
        pages = list((self.site / 'current').rglob('*.html')) + [self.site / 'versions/index.html']
        self.assertEqual(len(pages), 31)
        for path in pages:
            context = BeautifulSoup(path.read_text(), 'html.parser').select_one('.publication-context')
            self.assertIn('v0.3.5 published', context.get_text())
            self.assertNotIn('preparation', context.get_text())
        for name, text in self.wiki.items():
            self.assertNotIn('Target v0.3.5', text, name)

    def test_all_twenty_five_clause_bodies_remain_verbatim(self):
        old = (docs.ROOT / 'documentation/0.4.0/guides/Formalization.md').read_text()
        new = (docs.ROOT / docs.NS / 'guides/Formalization.md').read_text()
        old_register = old[old.index('<h2 id="C-01">'):old.index('## Source and review record')]
        new_register = new[new.index('<details id="C-01"'):new.index('## Source and review record')]
        old_parts = list(re.finditer(r'<h2 id="(C-\d{2})">([^<]+)</h2>\n', old_register))
        new_parts = list(re.finditer(r'<details id="(C-\d{2})"[^>]*>\n<summary>([^<]+)</summary>\n', new_register))
        self.assertEqual(len(old_parts), 25)
        self.assertEqual(len(new_parts), 25)
        for i, (before, after) in enumerate(zip(old_parts, new_parts)):
            self.assertEqual((before[1], before[2]), (after[1], after[2]))
            original = old_register[before.end():old_parts[i + 1].start() if i < 24 else len(old_register)].strip()
            current = new_register[after.end():new_parts[i + 1].start() if i < 24 else len(new_register)]
            current = current.rsplit('</details>', 1)[0].strip()
            original = original.replace('ccc89a184a618ccc2c107ccbf27a15232060557e', docs.SOURCE)
            self.assertEqual(original, current, before[1])
        soup = BeautifulSoup((self.site / 'current/guide/Formalization.html').read_text(), 'html.parser')
        self.assertEqual(len(soup.select('details.constraint-record')), 25)
        self.assertIsNotNone(soup.select_one('#C-25 summary'))

    def test_changed_published_payload_is_rejected(self):
        original = docs.read
        target = 'ontology/riskium-model.json'
        def altered(root, path):
            return b'changed semantic source' if path == target else original(root, path)
        with patch.object(docs, 'read', side_effect=altered), self.assertRaisesRegex(ValueError, 'Published input changed'):
            docs.preserved_inputs()

    def test_unreviewed_reader_edit_is_rejected(self):
        original = docs.read
        def altered(root, path):
            return b'# Unreviewed claim\n' if path == self.rows[0]['source'] else original(root, path)
        with patch.object(docs, 'read', side_effect=altered), self.assertRaisesRegex(ValueError, 'Changed reviewed reader source'):
            docs.review()

    def test_active_repository_readme_cannot_drift(self):
        original = docs.read
        def altered(root, path):
            return b'# Stale landing page\n' if path == '.github/README.md' else original(root, path)
        with patch.object(docs, 'read', side_effect=altered), self.assertRaisesRegex(ValueError, 'Active README drift'):
            docs.review()

    def getter(self, *, tag='v0.3.5', asset_digest=None, main=None):
        latest = dict(tag_name=tag, id=docs.RELEASE_ID, draft=False, prerelease=False,
            assets=[dict(name=a['name'], id=a['id'], size=a['size'], digest='sha256:' + a['sha256']) for a in self.publication['assets']])
        if asset_digest:
            latest['assets'][0]['digest'] = asset_digest
        values = {'releases/latest': latest,
            'git/ref/tags/v0.3.5': {'object': {'type': 'commit', 'sha': docs.SOURCE, 'url': 'https://api.github.com/tag'}},
            'git/ref/heads/main': {'object': {'sha': main or self.manifest['current_source_commit']}}}
        return lambda path: copy.deepcopy(values[path])

    def test_stale_live_latest_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Live published release identity changed'):
            docs.verify_live_release(self.publication, self.manifest['current_source_commit'], self.getter(tag='v0.3.4'))

    def test_changed_live_asset_digest_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Live public asset identity/digest changed'):
            docs.verify_live_release(self.publication, self.manifest['current_source_commit'], self.getter(asset_digest='sha256:' + '0' * 64))

    def test_advanced_main_cannot_be_deployed_as_this_documentation_source(self):
        with self.assertRaisesRegex(ValueError, 'Documentation source is no longer main'):
            docs.verify_live_release(self.publication, self.manifest['current_source_commit'], self.getter(main='0' * 40))

    def test_missing_guide_and_escaping_link_are_rejected(self):
        for link in ['Missing.md', '../Home.md', '/Home.md']:
            with self.subTest(link=link), self.assertRaises(ValueError):
                docs.rewrite_link(link, self.rows, 'current/index.html')

    def test_actual_navigation_audit_detects_broken_fragment_even_with_fresh_hash(self):
        path = self.site / 'current/index.html'
        original = path.read_bytes()
        manifest_path = self.site / 'publication-manifest.json'
        manifest_original = manifest_path.read_bytes()
        try:
            path.write_bytes(original.replace(b'</main>', b'<a href="guide/Evaluation.html#missing-result">Broken result</a></main>'))
            manifest = json.loads(manifest_original)
            manifest['files_sha256']['current/index.html'] = docs.sha(path.read_bytes())
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'Missing deployed fragment'):
                docs.audit(self.site)
        finally:
            path.write_bytes(original)
            manifest_path.write_bytes(manifest_original)


if __name__ == '__main__':
    unittest.main()
