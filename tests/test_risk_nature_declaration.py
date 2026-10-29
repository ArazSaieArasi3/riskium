"""Meaningful negative controls for the immutable preimplementation declaration."""
import copy
import json
from pathlib import Path
import sys
import unittest

from rdflib import Dataset, RDF, URIRef

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import check_risk_nature_declaration as declaration


class RiskNatureDeclarationTests(unittest.TestCase):
    def setUp(self):
        path = ROOT / declaration.NS
        self.model = json.loads((ROOT / 'ontology/riskium-model.json').read_text())
        self.contract = json.loads((path / 'contract.json').read_text())
        self.fixtures = json.loads((path / 'fixtures.json').read_text())
        self.inputs = json.loads((path / 'execution-fixture.json').read_text())
        self.oracles = json.loads((path / 'query-oracles.json').read_text())
        self.prior = json.loads((path / 'prior-population.json').read_text())
        self.dataset = Dataset()
        self.dataset.parse(path / 'native-oracles.trig', format='trig')

    def validate(self):
        return declaration.validate_semantics(self.model, self.contract, self.fixtures, self.inputs,
                                              self.oracles, self.dataset, self.prior)

    def test_source_and_literal_oracles_without_runtime_results(self):
        result = declaration.check()
        self.assertEqual(result['literal_graphs'], 8)
        self.assertEqual(result['literal_rdf_query_rows'], 9)
        self.assertEqual(result['runtime_controls_executed'], 0)

    def test_latest_objective_substitution_is_rejected(self):
        self.oracles['get'][declaration.N + 'A-v1']['objective_version_ids'] = [declaration.N + 'objective-v2']
        with self.assertRaisesRegex(ValueError, 'objective/context pin'):
            self.validate()

    def test_reversed_or_strengthened_native_routes_are_rejected(self):
        for key, value in [('source', 'RKM-C005'), ('source_end_cardinality', '1')]:
            changed = copy.deepcopy(self.contract)
            route = next(r for r in changed['native_routes'] if r['id'] == 'R-44')
            route['source_structure'][key] = value
            with self.assertRaisesRegex(ValueError, 'Native structure drift'):
                declaration.validate_native_routes(self.model, changed)

    def test_missing_recording_owner_is_rejected(self):
        self.inputs['recording_revisions'] = [r for r in self.inputs['recording_revisions']
                                              if declaration.N + 'A-v1' not in r['nature_version_ids']]
        with self.assertRaisesRegex(ValueError, 'Recording revision ownership'):
            self.validate()

    def test_inferred_plain_version_correction_is_rejected(self):
        self.oracles['family'][declaration.N + 'A-v1'].append(
            [declaration.N + 'A-v4', 1, declaration.N + 'A-v1'])
        with self.assertRaisesRegex(ValueError, 'correction family'):
            self.validate()

    def test_native_version_typing_and_optional_context_are_checked(self):
        graph = self.dataset.graph(URIRef(declaration.N + 'U-v1'))
        graph.add((URIRef(declaration.N + 'U-v1'), RDF.type, URIRef(declaration.RISK + 'RKM-C005')))
        with self.assertRaisesRegex(ValueError, 'Version mis-typed'):
            self.validate()

    def test_fixed_runtime_observations_cannot_be_promoted(self):
        self.fixtures['cases'][0]['observed'] = {'passed': True}
        self.fixtures['cases'][0]['status'] = 'PASS'
        with self.assertRaisesRegex(ValueError, 'Promoted/missing fixed outcome'):
            self.validate()

    def test_changed_source_hash_is_rejected(self):
        changed = copy.deepcopy(self.contract)
        changed['source_sha256']['ontology/riskium-model.json'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Source binding drift'):
            declaration.check_sources(changed)


if __name__ == '__main__':
    unittest.main()
