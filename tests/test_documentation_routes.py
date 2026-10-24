"""Exercise frozen-route tampering, source identity and shared projection boundaries."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/publication'))
import guides
import site_registry as routes
import build_versioned_site as site


class DocumentationRoutes(unittest.TestCase):
    def fixture(self, root):
        subprocess.run(['git', 'init', '-q', str(root)], check=True)
        path = root / 'docs/releases/v1.2.3'
        path.mkdir(parents=True)
        (path / 'index.html').write_text('<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width"></head><body>original</body></html>')
        (path / 'publication-manifest.json').write_text(json.dumps({'semantic_source_commit': 'a' * 40, 'model_version': '1.2.3'}))
        subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(root), '-c', 'user.name=Documentation Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'frozen source'], check=True)
        commit = routes.git(root, 'rev-parse', 'HEAD').decode().strip()
        entry = dict(route='releases/v1.2.3', documentation_version='1.0.0', model_version='1.2.3',
                     semantic_source_commit='a' * 40, source_commit=commit, source_path='docs/releases/v1.2.3',
                     source_tree=routes.git(root, 'rev-parse', commit + ':docs/releases/v1.2.3').decode().strip(),
                     rendering='EXACT_SOURCE_COPY', files_sha256={p: routes.sha(b) for p, b in routes.file_map(path).items()})
        register = dict(schema='riskium-documentation-routes-v1', current_route='current', version_index='versions/index.html', releases={'v1.2.3': entry})
        reg = root / routes.REGISTRY
        reg.parent.mkdir(parents=True)
        reg.write_text(json.dumps(register))
        return register

    def test_registered_snapshot_cannot_be_mutated_or_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = self.fixture(Path(tmp))
            for replace in [None, dict(old['releases']['v1.2.3'], source_commit='b' * 40)]:
                new = deepcopy(old)
                if replace is None:
                    new['releases'].clear()
                else:
                    new['releases']['v1.2.3'] = replace
                with self.assertRaisesRegex(ValueError, 'cannot be replaced or removed'):
                    routes.guard(old, new)

    def test_actual_frozen_file_tampering_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            routes.check_registry(root)
            (root / 'docs/releases/v1.2.3/index.html').write_text('tampered')
            with self.assertRaisesRegex(ValueError, 'Frozen documentation bytes changed'):
                routes.check_registry(root)

    def test_recorded_source_tree_cannot_be_substituted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            register = self.fixture(root)
            register['releases']['v1.2.3']['source_tree'] = 'c' * 40
            (root / routes.REGISTRY).write_text(json.dumps(register))
            with self.assertRaisesRegex(ValueError, 'source tree mismatch'):
                routes.check_registry(root)

    def test_routes_and_file_traversal_are_rejected(self):
        for value in ['../private', '/absolute', 'foo/../bar', 'a\\b', './a']:
            with self.subTest(path=value), self.assertRaises(ValueError):
                routes.safe_path(value)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            register = self.fixture(root)
            register['releases']['v1.2.3']['route'] = 'current'
            (root / routes.REGISTRY).write_text(json.dumps(register))
            with self.assertRaisesRegex(ValueError, 'colliding snapshot route'):
                routes.read_registry(root)

    def test_archive_requires_an_exact_source_commit(self):
        with self.assertRaisesRegex(ValueError, 'exact commit'):
            routes.tree_files(ROOT, 'main', 'docs/current')

    def test_new_snapshot_addition_preserves_existing_registration(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = self.fixture(Path(tmp))
            new = deepcopy(old)
            new['releases']['v1.2.4'] = {'new': 'declared separately'}
            routes.guard(old, new)

    def test_shared_wiki_sources_and_cross_surface_links(self):
        rows = guides.entries()
        outputs = guides.wiki_outputs()
        for row in rows:
            source = ROOT / row['source']
            projected = outputs[row['wiki_slug'] + '.md']
            self.assertTrue(projected.startswith(source.read_text().splitlines()[0]))
            self.assertIn('/current/guide/' + row['slug'] + '.html', projected)
            self.assertIn(routes.sha(source.read_bytes()), projected)
        home = outputs['Home.md']
        self.assertIn('[scope](Scope)', home)
        self.assertIn('[modeling decisions](Modeling-Decisions)', home)

    def test_guide_url_cannot_escape_repository(self):
        with self.assertRaisesRegex(ValueError, 'escapes repository'):
            guides.wiki_link('../../../../private.txt', 'docs/guides/Home.md', guides.entries())

    def test_changed_existing_path_does_not_link_to_stale_release_bytes(self):
        self.assertEqual(guides.source_ref('ontology/riskium-model.json'), guides.SEMANTIC_COMMIT)
        self.assertEqual(guides.source_ref('docs/roadmap.md'), 'main')

    def test_snapshot_projection_rebases_root_links_and_pins_current_sources(self):
        inputs = routes.file_map(ROOT / 'docs/current')
        out = routes.freeze_files(inputs, 'v0.3.1', 'd' * 40, '0.1.0')
        page = out['widoco/index-en.html'].decode()
        self.assertIn('../../../THIRD-PARTY-DOCUMENTATION.txt', page)
        self.assertIn('Frozen documentation', page)
        guide = out['guide/Database-Assurance.html'].decode()
        self.assertNotIn(routes.REPO + '/blob/main/', guide)
        self.assertIn('/blob/' + 'd' * 40 + '/', guide)
        tool = json.loads(out['widoco/tool-provenance.json'])
        self.assertEqual(tool['frozen_presentation_projection']['original_tool_provenance_sha256'], routes.sha(inputs['widoco/tool-provenance.json']))
        self.assertEqual(tool['files_sha256']['index-en.html'], routes.sha(out['widoco/index-en.html']))
        self.assertEqual(out['widoco/ontology.ttl'], inputs['widoco/ontology.ttl'])
        self.assertEqual(out, routes.freeze_files(inputs, 'v0.3.1', 'd' * 40, '0.1.0'))

    def test_build_refuses_to_replace_the_repository(self):
        with self.assertRaisesRegex(ValueError, 'independent build directory'):
            site.build(ROOT)

    def test_legacy_snapshot_remains_exact(self):
        register = routes.check_registry()
        old = register['releases']['v0.3.1-rc.1']
        self.assertEqual(old['source_commit'], '3f332ea56cb27263d2435fa0ae20afb7a5d5f432')
        self.assertEqual(old['rendering'], 'EXACT_SOURCE_COPY')


if __name__ == '__main__':
    unittest.main()
