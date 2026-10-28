"""Current release navigation and immutable publication/source boundaries."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/publication'))
import build_documentation_component as component


class DocumentationComponent(unittest.TestCase):
    def test_current_component_matches_exact_selected_source_and_output_bytes(self):
        expected = json.loads((ROOT / component.OUT).read_text())
        self.assertEqual(component.build(), expected)
        self.assertEqual(expected['shared_guides'], 21)
        self.assertEqual(expected['native_wiki_files'], 23)
        self.assertFalse(expected['frozen_snapshot_registered'])
        self.assertFalse(expected['semantic_or_scientific_changes'])

    def test_all_current_headers_use_live_latest_routing_and_explicit_doc_version(self):
        for path in sorted((ROOT / 'docs/current').rglob('*.html')):
            with self.subTest(page=path.relative_to(ROOT)):
                soup = BeautifulSoup(path.read_text(), 'html.parser')
                header = soup.select_one('.publication-context')
                self.assertIsNotNone(header)
                self.assertIn('0.3.0', header.get_text())
                self.assertIsNotNone(header.select_one('a[href="https://github.com/ArazSaieArasi3/riskium/releases/latest"]'))
                self.assertNotIn('/releases/tag/v0.3.2', str(header))

    def test_edited_current_source_or_output_is_detected_by_component_binding(self):
        original = component.sha
        for path in ('docs/current/index.html', 'docs/guides/Home.md'):
            with self.subTest(path=path), patch.object(component, 'sha', side_effect=lambda p: '0' * 64 if p == path else original(p)):
                try:
                    changed = component.build()
                except ValueError:
                    continue
                self.assertNotEqual(changed, json.loads((ROOT / component.OUT).read_text()))

    def test_all_frozen_snapshot_and_rdf_bytes_remain_bound_to_prior_source(self):
        status = json.loads((ROOT / 'tools/publication/current-status.json').read_text())
        registry = json.loads((ROOT / 'tools/publication/pages-registry.json').read_text())
        for row in registry['releases'].values():
            for name, digest in row['files_sha256'].items():
                self.assertEqual(component.sha('docs/' + row['route'] + '/' + name), digest)
        for name in ('ontology.ttl', 'ontology.owl', 'ontology.nt', 'ontology.jsonld'):
            path = 'docs/current/widoco/' + name
            before = subprocess.check_output(['git', 'show', '2bb7c0848a826ba0fba4d22458f43e53736d7b72:' + path], cwd=ROOT)
            self.assertEqual((ROOT / path).read_bytes(), before)
        self.assertEqual(status['published_checkpoint']['tag'], 'v0.3.3')


if __name__ == '__main__':
    unittest.main()
