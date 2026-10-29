"""Reject changed evidence, hidden omissions and premature research/release claims."""
import copy
import json
from pathlib import Path
import sys
import unittest

from rdflib import Dataset

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import audit_risk_nature_alignment as audit


class NatureAlignment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def read(name):
            return json.loads((audit.ROOT / name).read_text())
        cls.bundle = read(audit.RECEIPT)
        cls.fixtures = read(audit.BASE + '/fixtures.json')
        cls.negative = read(audit.BASE + '/negative-inputs.json')
        cls.oracles = read(audit.BASE + '/query-oracles.json')
        cls.inputs = read(audit.BASE + '/execution-fixture.json')
        cls.graphs = Dataset()
        cls.graphs.parse(audit.ROOT / audit.BASE / 'native-oracles.trig', format='trig')

    def altered_evidence(self, change, message):
        bundle = copy.deepcopy(self.bundle)
        change(bundle)
        with self.assertRaisesRegex(ValueError, message):
            audit.validate_observations(bundle, self.fixtures, self.negative, self.oracles, self.graphs, self.inputs)

    def test_generated_overlay_keeps_all_old_routes_and_pending_gates(self):
        output = audit.build()
        for path, value in output.items():
            self.assertEqual((audit.ROOT / path).read_text(), value, path)
        report = json.loads(output[audit.OUT + '/report.json'])
        mapping = json.loads(output[audit.OUT + '/native-accounting.json'])
        trace = json.loads(output[audit.OUT + '/traceability.json'])
        old = json.loads((audit.ROOT / audit.predecessor.OUT / 'traceability.json').read_text())
        self.assertEqual(trace['rows'][:460], old['rows'])
        self.assertEqual(len(mapping['rows']), 306)
        self.assertEqual(sum(bool(r['witnesses']) for r in mapping['rows']), 31)
        self.assertEqual(report['summary']['historical_deferred_unchanged'], 236)
        self.assertEqual(trace['rows'][-1]['completion'], 'PARTIAL_PENDING_R4_R5')
        self.assertFalse(report['source_release_published'])

    def test_pass_label_cannot_hide_wrong_observed_answer(self):
        self.altered_evidence(lambda b: b['actual_hosted_and_independent_completion']['controls'][9]['observed']['exact_row'].update(context_version_id='latest'), 'Fixed observation differs')

    def test_missing_control_is_rejected(self):
        self.altered_evidence(lambda b: b['actual_hosted_and_independent_completion']['controls'].pop(), 'Missing or duplicate fixed control')

    def test_negative_rejection_cannot_hide_state_change(self):
        self.altered_evidence(lambda b: b['actual_hosted_and_independent_completion']['negative_variants'][0]['observed'].update(all_preoperation_state_preserved=False), 'Negative answer differs')

    def test_full_query_keeps_verbatim_source_bytes(self):
        self.altered_evidence(lambda b: b['actual_local_full_vectors']['exact_queries']['urn:riskium:nature37:A-v1']['sources']['assertion'][0].update(original_json='{}'), 'Verbatim source vector differs')

    def test_exact_dependency_cannot_join_latest_version(self):
        self.altered_evidence(lambda b: b['actual_local_full_vectors']['exact_queries']['urn:riskium:nature37:A-v1']['dependencies']['context'][0].update(version_id='urn:riskium:nature37:context-v2'), 'Exact dependency vector differs')

    def test_missing_native_triple_cannot_borrow_pass_flag(self):
        self.altered_evidence(lambda b: b['actual_local_full_vectors']['native_graphs']['urn:riskium:nature37:A-v1'].pop(), 'Native triple vector differs')

    def test_receipt_cannot_be_reattributed_to_integration_source(self):
        self.altered_evidence(lambda b: b['actual_hosted_and_independent_completion'].update(source_commit='integration'), 'R2 executed source differs')

    def test_reader_release_and_paper_promotions_are_rejected(self):
        path = audit.OUT + '/policy.json'
        original = json.loads((audit.ROOT / path).read_text())
        for key, value in [('reader', 'PASS'), ('distribution', 'PUBLISHED'), ('new_manuscript_disposition', 'CLAIMED_IN_PAPER')]:
            policy = copy.deepcopy(original)
            policy[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'pending gate promoted'):
                audit.build(overrides={path: json.dumps(policy)})

    def test_evidence_hash_pins_lossless_published_bytes(self):
        with self.assertRaisesRegex(ValueError, 'Published R2 evidence bytes differ'):
            audit.build(overrides={audit.RECEIPT: json.dumps(self.bundle)})


if __name__ == '__main__':
    unittest.main()
