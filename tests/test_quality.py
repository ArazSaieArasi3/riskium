"""Guard against scientifically misleading aggregation or lost evidence gaps."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('quality_report', ROOT / 'tools/build_quality_report.py')
quality = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quality)


class QualityClaimGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads((ROOT / 'evaluation/quality/policy.json').read_text())
        cls.data, cls.inventory = quality.load_inputs(cls.policy)
        cls.report = quality.assemble(cls.policy, cls.data, cls.inventory)

    def test_missing_independent_review_never_becomes_correctness_score(self):
        self.assertIsNone(self.report['metrics']['Q-10']['percent'])
        self.assertIsNone(self.report['overall_semantic_correctness_percent'])
        self.assertIsNone(self.report['judgment']['critical_findings_count'])
        self.assertEqual(self.report['judgment']['stable_scientific_acceptance'], 'NOT_ESTABLISHED')

    def test_blocked_and_preflight_scenarios_are_not_engine_successes(self):
        conditional = self.report['shacl_modules'][0]
        self.assertEqual(conditional['scenarios'], 79)
        self.assertEqual(conditional['engine_executions'], 77)
        self.assertEqual(conditional['preflight_outcomes'], {'PASS': 1})
        self.assertEqual(conditional['blocked_scenarios'], ['S-C08-TASK-DUAL-UNKNOWN'])
        self.assertEqual(self.report['metrics']['Q-04']['outcomes']['PARTIAL'], 1)

    def test_row_relabel_cannot_hide_behind_unchanged_summary(self):
        changed = dict(self.data)
        p = 'evaluation/hermit/report.json'
        changed[p] = copy.deepcopy(self.data[p])
        row = next(r for r in changed[p]['obligations'] if r['outcome'] == 'NOT_RUN')
        row['outcome'] = 'PASS'
        with self.assertRaisesRegex(ValueError, 'hide row outcomes'):
            quality.assemble(self.policy, changed, self.inventory)

    def test_mutant_engine_error_cannot_count_as_detection(self):
        changed = dict(self.data)
        p = 'evaluation/cq/report.json'
        changed[p] = copy.deepcopy(self.data[p])
        row = next(r for r in changed[p]['cases'] if r['kind'] == 'query_mutant')
        row['error'] = 'parser/engine error'
        with self.assertRaisesRegex(ValueError, 'error incorrectly labeled PASS'):
            quality.assemble(self.policy, changed, self.inventory)

    def test_structural_boundary_review_does_not_discharge_engines(self):
        c14 = next(r for r in self.report['constraint_rows'] if r['id'] == 'C-14')
        self.assertEqual((c14['hermit']['outcome'], c14['shacl']['outcome']), ('NOT_RUN', 'NOT_RUN'))
        self.assertEqual(self.report['new_scientific_engine_executions'], 0)

    def test_later_corpus_evidence_has_explicit_overlay_not_rewritten_history(self):
        scope = next(r for r in self.report['trace_rows'] if r['id'] == 'RKM-SCOPE-04')
        self.assertEqual(scope['recorded_state'], 'NOT_RUN')
        self.assertEqual(scope['post_trace_reconciliation']['current_disposition'], 'BOUNDED_EDITORIAL_REVIEW_RECORDED')
        tolerance = next(r for r in self.report['trace_rows'] if r['id'] == 'RKM-SCOPE-03')
        self.assertEqual(tolerance['recorded_state'], 'PARTIAL')
        self.assertEqual(tolerance['post_trace_reconciliation']['issues'], [7, 14])


if __name__ == '__main__':
    unittest.main()
