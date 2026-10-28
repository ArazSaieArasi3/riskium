"""Exact-source successor registration, preservation and actual deploy assembly."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools/publication'))
import snapshot_registry as snapshots
import build_snapshot_site as site


class DocumentationSnapshot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy, cls.inputs = snapshots.review()
        cls.additions = json.loads(snapshots.read(ROOT, snapshots.ADDITIONS))

    def changed_read(self, path, value):
        before = snapshots.read
        return patch.object(snapshots, 'read', side_effect=lambda root, p:
                            snapshots.encode(value).encode() if p == path else before(root, p))

    def test_exact_source_model_and_component_are_bound_without_rewriting_prior_packets(self):
        component = snapshots.build_component()
        self.assertEqual(component, json.loads(snapshots.read(ROOT, snapshots.COMPONENT)))
        self.assertEqual(component['snapshot_source'], snapshots.SOURCE)
        self.assertEqual(component['snapshot_files'], 68)
        self.assertEqual(component['original_snapshots_preserved'], 3)
        self.assertTrue(component['selection_refresh_required'])
        self.assertFalse(component['source_distribution_published'])
        self.assertNotIn('releases/selection-v0.3.4.json', component['files_sha256'])
        self.assertIn('DOCUMENTATION_SNAPSHOT', component['id'])

    def test_an_unreviewed_label_source_or_documentation_version_cannot_write(self):
        for label, source, version in [('v0.3.5', snapshots.SOURCE, '0.3.0'),
                ('v0.3.4', 'main', '0.3.0'), ('v0.3.4', 'a' * 40, '0.3.0'),
                ('v0.3.4', snapshots.SOURCE, '0.4.0')]:
            with self.subTest(request=(label, source, version)), patch.object(snapshots, 'review', side_effect=AssertionError('must reject before reading/writing')):
                with self.assertRaisesRegex(ValueError, 'Unreviewed snapshot request'):
                    snapshots.register(label, source, version)

    def test_the_policy_cannot_promote_model_or_source_compatibility(self):
        for key, value in [('model_version', '0.4.0'), ('source_commit', 'a' * 40), ('documentation_version', '0.4.0')]:
            policy = copy.deepcopy(self.policy)
            policy[key] = value
            with self.subTest(key=key), self.changed_read(snapshots.POLICY, policy):
                with self.assertRaisesRegex(ValueError, 'Unreviewed snapshot compatibility'):
                    snapshots.review()

    def test_semantic_source_and_rendering_cannot_be_substituted(self):
        for key, value in [('semantic_source_commit', 'a' * 40), ('rendering', 'EXACT_SOURCE_COPY')]:
            policy = copy.deepcopy(self.policy)
            policy[key] = value
            with self.subTest(key=key), self.changed_read(snapshots.POLICY, policy):
                with self.assertRaisesRegex(ValueError, 'rendering/semantic source'):
                    snapshots.review()

    def test_source_publication_or_independent_acceptance_cannot_be_inferred(self):
        for key in ['source_distribution_published', 'independent_acceptance_claimed', 'stable_profile_registered']:
            policy = copy.deepcopy(self.policy)
            policy['boundaries'][key] = True
            with self.subTest(key=key), self.changed_read(snapshots.POLICY, policy):
                with self.assertRaisesRegex(ValueError, 'Unreviewed snapshot scope'):
                    snapshots.review()

    def test_prior_checkpoint_binding_cannot_be_omitted(self):
        policy = copy.deepcopy(self.policy)
        policy['preserved_files_sha256'].pop('releases/selection-v0.3.4.json')
        with self.changed_read(snapshots.POLICY, policy):
            with self.assertRaisesRegex(ValueError, 'binding omitted'):
                snapshots.review()

    def test_changed_old_registry_component_or_selection_is_rejected(self):
        original = snapshots.read
        for target in ['tools/publication/pages-registry.json', 'evaluation/documentation/current-0.3.0/component.json',
                       'releases/selection-v0.3.4.json']:
            with self.subTest(path=target), patch.object(snapshots, 'read', side_effect=lambda root, path:
                    original(root, path) + b' ' if path == target else original(root, path)):
                with self.assertRaisesRegex(ValueError, 'Preserved checkpoint changed'):
                    snapshots.review()

    def test_current_documentation_cannot_drift_while_reusing_the_approved_source(self):
        original = snapshots.original.file_map
        altered = dict(self.inputs, **{'index.html': b'changed'})
        with patch.object(snapshots.original, 'file_map', side_effect=lambda p:
                          altered if p == ROOT / 'docs/current' else original(p)):
            with self.assertRaisesRegex(ValueError, 'Current documentation differs'):
                snapshots.review()

    def test_the_source_tree_must_be_the_reviewed_commit_tree(self):
        policy = copy.deepcopy(self.policy)
        policy['source_tree'] = 'a' * 40
        with self.changed_read(snapshots.POLICY, policy):
            with self.assertRaisesRegex(ValueError, 'source tree differs'):
                snapshots.review()

    def test_unsafe_paths_and_symlinks_are_rejected(self):
        for p in ['../../private', '/etc/passwd', 'a\\b']:
            with self.subTest(path=p), self.assertRaises(ValueError):
                snapshots.read(ROOT, p)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'original').write_text('private')
            (root / 'alias').symlink_to(root / 'original')
            with self.assertRaisesRegex(ValueError, 'Unsafe snapshot source path'):
                snapshots.read(root, 'alias')

    def test_registered_addition_cannot_change_source_hashes_or_disappear(self):
        for altered in [None, dict(self.additions, releases={})]:
            with self.subTest(value=altered), self.assertRaisesRegex(ValueError, 'cannot be replaced or removed'):
                snapshots.guard(self.additions, altered)
        changed = copy.deepcopy(self.additions)
        changed['releases']['v0.3.4']['source_commit'] = 'a' * 40
        with self.changed_read(snapshots.ADDITIONS, changed):
            with self.assertRaisesRegex(ValueError, 'identity/source/output differs'):
                snapshots.check_additions()

    def test_frozen_output_tampering_is_rejected(self):
        original = snapshots.original.file_map
        with patch.object(snapshots.original, 'file_map', side_effect=lambda p:
                {'index.html': b'changed'} if p == ROOT / 'docs' / snapshots.ROUTE else original(p)):
            with self.assertRaisesRegex(ValueError, 'Frozen successor snapshot bytes changed'):
                snapshots.check_additions()

    def test_existing_route_cannot_be_registered_again(self):
        before = snapshots.read(ROOT, snapshots.ADDITIONS)
        with self.assertRaisesRegex(ValueError, 'already exists'):
            snapshots.register('v0.3.4', snapshots.SOURCE, '0.3.0')
        self.assertEqual(snapshots.read(ROOT, snapshots.ADDITIONS), before)

    def test_projection_preserves_all_four_rdf_files_and_pins_explanatory_sources(self):
        row, outputs = snapshots.expected_row(self.policy, self.inputs)
        for name in ['ontology.ttl', 'ontology.owl', 'ontology.nt', 'ontology.jsonld']:
            self.assertEqual(outputs['widoco/' + name], self.inputs['widoco/' + name])
        guide = outputs['guide/Database-Assurance.html'].decode()
        self.assertNotIn(snapshots.original.REPO + '/blob/main/', guide)
        self.assertIn('/blob/' + snapshots.SOURCE + '/', guide)
        self.assertEqual(row['documentation_version'], '0.3.0')
        self.assertEqual(outputs, snapshots.expected_row(self.policy, self.inputs)[1])

    def test_version_index_separates_documentation_snapshot_from_live_source_release(self):
        soup = BeautifulSoup(snapshots.version_index(snapshots.check_additions()), 'html.parser')
        self.assertIsNotNone(soup.select_one('a[href="../releases/v0.3.4/index.html"]'))
        self.assertIsNotNone(soup.select_one('a[href="https://github.com/ArazSaieArasi3/riskium/releases/latest"]'))
        self.assertIsNone(soup.select_one('a[href$="/releases/tag/v0.3.2"]'))
        self.assertIn('does not publish a source distribution', soup.get_text())
        self.assertIn('selection refresh', soup.get_text())

    def test_actual_deployment_assembles_four_snapshots_and_all_manifest_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'site'
            manifest = site.build(folder)
            result = site.audit(folder)
            self.assertEqual(result['frozen_snapshots'], 4)
            self.assertEqual(len(manifest['releases']), 4)
            self.assertEqual((folder / 'current/index.html').read_bytes(), self.inputs['index.html'])
            self.assertTrue(manifest['snapshot_preparation']['selection_refresh_required'])
            self.assertFalse(manifest['snapshot_preparation']['source_release_published'])
            self.assertEqual(snapshots.original.sha((folder / 'versions/index.html').read_bytes()),
                snapshots.build_component()['generated_versions_index_sha256'])

    def test_deployment_refuses_a_stale_snapshot_component(self):
        component = json.loads(snapshots.read(ROOT, snapshots.COMPONENT))
        component['files_sha256'].pop(next(iter(component['files_sha256'])))
        with self.changed_read(snapshots.COMPONENT, component), tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'Stale additive snapshot component'):
                site.build(Path(tmp) / 'site')

    def test_deployment_refuses_to_overwrite_the_repository(self):
        with self.assertRaisesRegex(ValueError, 'independent build directory'):
            site.build(ROOT)


if __name__ == '__main__':
    unittest.main()
