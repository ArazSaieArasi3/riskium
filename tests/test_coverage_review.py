"""Adversarial checks for coverage omissions and misleading execution claims."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from review_coverage import audit, load_inputs


class CoverageReviewRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = load_inputs()

    def reject(self, mutate, message):
        value = copy.deepcopy(self.baseline)
        mutate(value)
        self.assertTrue(any(message in e for e in audit(value)['errors']))

    def test_current_contract(self):
        report = audit(self.baseline)
        self.assertEqual(report['errors'], [])
        self.assertEqual(report['summary']['formal_cases_executed'], 0)

    def test_lost_obligation(self):
        self.reject(lambda d: d['rows'].pop(), 'obligation allocation mismatch')

    def test_duplicate_replaces_distinct_obligation(self):
        self.reject(lambda d: d['rows'].__setitem__(1, copy.deepcopy(d['rows'][0])),
                    'obligation allocation mismatch')

    def test_direction_reversed(self):
        def change(d):
            next(r for r in d['rows'] if r['family'] == 'Managed-profile endpoint cardinality')['direction'] = 'source; direct property path'
        self.reject(change, 'endpoint direction/profile mismatch')

    def test_false_pass(self):
        self.reject(lambda d: d['rows'][0].update(status='PASS'), 'unverified formal execution claim')

    def test_stale_model_binding(self):
        self.reject(lambda d: d['contract'].update(source_model_sha256='0' * 64), 'source model digest mismatch')

    def test_constraint_disappears(self):
        self.reject(lambda d: d['contract']['constraint_dispositions'].pop(), 'constraint disposition allocation mismatch')

    def test_constraint_statement_changes(self):
        self.reject(lambda d: d['model']['constraints'][0].update(statement='changed'), 'stale constraint disposition')

    def test_requirement_expectation_changes(self):
        self.reject(lambda d: d['requirements'][0].update(acceptance_criterion='changed'), 'stale requirement expectation')

    def test_scope_requirement_lost(self):
        self.reject(lambda d: d['scope'].pop(), 'scope requirement allocation mismatch')

    def test_optional_boundary_added_to_core(self):
        def change(d):
            next(c for c in d['model']['concepts'] if c['ontouml_stereotype'] is None)['scope_layer'] = 'FORMAL_CORE'
        self.reject(change, 'obligation allocation mismatch')

    def test_unbounded_count_is_not_a_negative_test(self):
        report = audit(self.baseline)
        row = next(r for r in report['obligation_reviews'] if r['source_element'] == 'R-01:source')
        self.assertEqual(row['cases']['focus_class'], 'RKM-X01')
        self.assertEqual(row['cases']['property_path'], 'inverse')
        self.assertEqual(row['cases']['below_minimum']['expected'], 'NOT_APPLICABLE')
        self.assertEqual(row['cases']['above_maximum']['expected'], 'NOT_APPLICABLE')


if __name__ == '__main__':
    unittest.main()
