"""Mutation checks for native-export fidelity; not a semantic ontology suite."""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build_native import build
from validate_native import check_fidelity

MODEL = json.loads((ROOT / 'ontology/riskium-model.json').read_text())


class NativeExchangeRegression(unittest.TestCase):
    def setUp(self):
        self.native = build(MODEL, hashlib.sha256((ROOT / 'ontology/riskium-model.json').read_bytes()).hexdigest())
        self.by = {e['id']: e for e in self.native['elements']}

    def assert_rejected(self, text):
        self.assertTrue(any(text in e for e in check_fidelity(MODEL, self.native)))

    def test_current_export(self):
        self.assertEqual(check_fidelity(MODEL, self.native), [])

    def test_bearer_cardinality_lost(self):
        self.by['RK3-004:source']['cardinality'] = '0..*'
        self.assert_rejected('endpoint/cardinality changed')

    def test_relation_direction_reversed(self):
        self.by['R-01']['properties'].reverse()
        self.assert_rejected('relation end order changed')

    def test_identity_supplier_changed(self):
        self.by['RKM-C022']['customProperties']['identitySupplier'] = 'RKM-X01'
        self.assert_rejected('class semantics changed')

    def test_abstract_stereotype_is_not_abstract_flag(self):
        self.assertEqual(self.by['RKM-C016']['stereotype'], 'abstract')
        self.assertFalse(self.by['RKM-C016']['isAbstract'])
        self.by['RKM-C016']['isAbstract'] = True
        self.assert_rejected('class semantics changed')

    def test_untyped_boundary_promoted(self):
        self.by['RKM-C007']['type'] = 'Class'
        self.assert_rejected('typed class allocation mismatch')

    def test_generalization_reversed(self):
        g = self.by['G-01']
        g['specific'], g['general'] = g['general'], g['specific']
        self.assert_rejected('generalization direction changed')

    def test_unjustified_covering_added(self):
        self.by['GS-RKM-C047']['isComplete'] = True
        self.assert_rejected('generalization-set decision changed')

    def test_constraint_note_lost(self):
        self.native['elements'] = [e for e in self.native['elements'] if e['id'] != 'C-22']
        self.assert_rejected('constraint note changed')

    def test_external_bridge_changed(self):
        self.by['R-66']['customProperties']['target'] = 'RKM-X01'
        self.assert_rejected('bridge disposition changed')

    def test_domain_member_lost(self):
        self.by['D01']['contents'].remove('RKM-X01')
        self.assert_rejected('native domain membership lost')


if __name__ == '__main__':
    unittest.main()
