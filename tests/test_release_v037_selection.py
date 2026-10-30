"""Exercise preservation, dependency and source-binding rejection paths."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('selection037', ROOT/'tools/releases/v037/selection.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class SelectedClosure(unittest.TestCase):
    def altered(self, path, transform):
        original = r.read
        def read(name, root=r.ROOT):
            data = original(name, root)
            return transform(data) if name == path else data
        return patch.object(r, 'read', side_effect=read)

    def test_preserves_released_payload_and_original_landing(self):
        matrix = r.selection()
        prior = json.loads(r.read(r.PRIOR))
        self.assertEqual(matrix['summary']['components'], 31)
        self.assertEqual(matrix['summary']['preserved_prior_files'], 779)
        for p, h in prior['selected_files_sha256'].items():
            if p != '.github/README.md':
                self.assertEqual(matrix['selected_files_sha256'][p], h)
        self.assertEqual(matrix['predecessor_landing']['sha256'], prior['selected_files_sha256']['.github/README.md'])
        self.assertEqual(r.read(r.MATRIX), r.encoded(matrix))

    def test_changed_prior_payload_is_rejected(self):
        with self.altered('ontology/riskium-model.json', lambda d: d+b' '), self.assertRaisesRegex(ValueError, 'Source binding'):
            r.selection()

    def test_changed_component_descriptor_is_rejected(self):
        with self.altered('implementation/relational/0.9.0/component.json', lambda d: d+b' '), self.assertRaisesRegex(ValueError, 'Source binding|descriptor'):
            r.selection()

    def test_changed_r4_observation_is_rejected(self):
        with self.altered(r.R4, lambda d: d+b' '), self.assertRaisesRegex(ValueError, 'R4 receipt'):
            r.selection()

    def test_wrong_dependency_version_and_cycle_are_rejected(self):
        versions = dict(a='1', b='2')
        with self.assertRaisesRegex(ValueError, 'Unresolved'):
            r.dependency_order(versions, dict(a=[dict(id='b', version='1')], b=[]))
        with self.assertRaisesRegex(ValueError, 'cycle'):
            r.dependency_order(versions, dict(a=[dict(id='b', version='2')], b=[dict(id='a', version='1')]))

    def test_transitive_versions_resolve_before_dependent_components(self):
        matrix = r.selection()
        order = matrix['dependency_order']
        for ident, edges in matrix['dependencies'].items():
            for edge in edges:
                self.assertLess(order.index(edge['id']), order.index(ident))
        self.assertFalse(matrix['release_published'])
        self.assertFalse(matrix['freeze_completed'])


if __name__ == '__main__':
    unittest.main()
