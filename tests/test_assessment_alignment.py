"""Mutations to the new scope cannot borrow old accounting or paper claims."""
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import audit_assessment_alignment as audit


class AssessmentAlignment(unittest.TestCase):
    def read(self, path):
        return json.loads((audit.ROOT / path).read_text())

    def altered(self, path, change, error):
        value = self.read(path)
        change(value)
        with self.assertRaisesRegex((ValueError, AssertionError), error):
            audit.build(overrides={path: json.dumps(value)})

    def test_combined_routes_and_paper_boundary(self):
        output = audit.build()
        report = json.loads(output[audit.OUT + '/report.json'])
        trace = json.loads(output[audit.OUT + '/traceability.json'])
        self.assertEqual(len(trace['rows']), 460)
        self.assertEqual(report['summary']['current_claim_routes'], 49)
        self.assertEqual(report['summary']['new_engineering_controls'], 44)
        self.assertEqual(report['summary']['pending_reader_criteria'], 6)
        self.assertEqual({r['manuscript']['state'] for r in trace['rows'][-10:]}, {'NOT_CLAIMED_IN_PAPER'})
        self.assertFalse(report['submission_ready'])

    def test_missing_requirement_route_rejected(self):
        self.altered(audit.OUT + '/policy.json', lambda d: d['derived_routes'].pop(), 'Missing/duplicate ASL route')

    def test_wrong_reader_disposition_rejected(self):
        self.altered(audit.EVIDENCE + '/traceability.json',
                     lambda d: d['rows'][-1].update(reader_status='PASS'), 'Stale source binding')

    def test_lost_observed_control_rejected(self):
        def drop(d):
            d['controls'].pop()
            d['summary']['PASS'] = 43
        self.altered(audit.EVIDENCE + '/report.json', drop, 'Stale source binding')

    def test_changed_observation_rejected_even_if_pass_label_retained(self):
        self.altered(audit.EVIDENCE + '/report.json',
                     lambda d: d['controls'][0].update(observed={'user_version': 9}), 'Stale source binding')

    def test_rewritten_original_oracle_rejected(self):
        self.altered(audit.BASE + '/fixtures.json',
                     lambda d: d['cases'][0]['expected'].update(user_version=8), 'Stale source binding')

    def test_changed_executable_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Stale source binding'):
            audit.build(overrides={'tools/relational_assessment_selection.py': '# altered executable\n'})

    def test_manuscript_promotion_rejected(self):
        self.altered(audit.OUT + '/policy.json',
                     lambda d: d.update(new_manuscript_disposition='CLAIMED_IN_PAPER'), 'Paper or release identity promoted')

    def test_previous_route_rewrite_rejected(self):
        self.altered('evaluation/consistency/current-0.3.0/traceability.json',
                     lambda d: d['rows'].pop(), 'Changed predecessor current overlay')

    def test_original_native_dispositions_rejected(self):
        def promote(d):
            next(r for r in d['rows'] if r['disposition'] == 'DEFERRED_NO_COMPLETE_SQL_MAPPING')['disposition'] = 'FULLY_IMPLEMENTED'
        self.altered('evaluation/relational/evidence-lifecycle/mapping-accounting.json', promote, 'Native disposition promoted')


if __name__ == '__main__':
    unittest.main()
