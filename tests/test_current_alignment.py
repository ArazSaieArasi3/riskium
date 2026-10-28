"""Real source mutations must invalidate current accounting, not improve claims."""
import copy
import json
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import audit_current_alignment as audit


class CurrentAlignment(unittest.TestCase):
    def document(self, path):
        return json.loads((audit.ROOT / path).read_text())

    def mutate(self, path, change, message):
        value = self.document(path)
        change(value)
        with self.assertRaisesRegex(ValueError, message):
            audit.build(overrides={path: json.dumps(value)})

    def test_actual_full_current_source_accounting_and_paper_dispositions(self):
        result = audit.build()
        report = json.loads(result[audit.OUT + '/report.json'])
        self.assertEqual(report['summary']['routes'], 450)
        self.assertEqual(report['summary']['native_ids'], 306)
        self.assertEqual(sum(r['cases'] for r in report['engineering_populations']), 213)
        self.assertFalse(report['submission_ready'])
        self.assertEqual(report['current_channel_alignment'], 'PENDING_R5_DOCUMENTATION_0.4.0_AND_ACTUAL_CHANNEL_READBACK')

    def test_missing_current_claim_rejected(self):
        self.mutate(audit.OUT + '/policy.json', lambda d: d['current_claims'].pop(), 'Lost/duplicate current retained claim')

    def test_missing_declared_route_is_not_silently_excluded(self):
        self.mutate(audit.OUT + '/policy.json', lambda d: d['required_current_claim_routes'].pop(), 'Orphan/missing current claim')

    def test_changed_executable_cannot_reuse_old_receipt(self):
        with self.assertRaisesRegex(ValueError, 'Stale source binding'):
            audit.build(overrides={'tools/relational_evidence_lifecycle.py': '# substituted executable\n'})

    def test_wrong_version_report_rejected(self):
        path = 'evaluation/relational/evidence-lifecycle/report.json'
        trace = self.document('evaluation/relational/evidence-lifecycle/traceability.json')
        report = self.document(path)
        report['profile'] = '0.6.0'
        with self.assertRaisesRegex(ValueError, 'Wrong-version report'):
            audit.validate_report(report, trace, '0.7.0', 43)

    def test_failed_observation_cannot_keep_pass_label(self):
        report = self.document('evaluation/relational/evidence-lifecycle/report.json')
        trace = self.document('evaluation/relational/evidence-lifecycle/traceability.json')
        report['cases'][0]['observed'] = 'FALSE_PASS'
        with self.assertRaisesRegex(ValueError, 'Actual oracle mismatch'):
            audit.validate_report(report, trace, '0.7.0', 43)

    def test_orphan_actual_case_detected_even_with_unchanged_denominator(self):
        report = self.document('evaluation/relational/evidence-lifecycle/report.json')
        trace = self.document('evaluation/relational/evidence-lifecycle/traceability.json')
        for row in trace['requirements']:
            row['case_ids'] = [v for v in row['case_ids'] if v != 'ELC-F01']
        with self.assertRaisesRegex(ValueError, 'Orphan or missing executed case'):
            audit.validate_report(report, trace, '0.7.0', 43)

    def test_duplicate_case_cannot_replace_lost_negative_control(self):
        report = self.document('evaluation/relational/qualified-evidence/report.json')
        trace = self.document('evaluation/relational/qualified-evidence/traceability.json')
        report['cases'][-1] = copy.deepcopy(report['cases'][0])
        with self.assertRaisesRegex(ValueError, 'Lost/duplicate actual case'):
            audit.validate_report(report, trace, '0.6.0', 62)

    def test_removed_native_id_rejected(self):
        self.mutate('evaluation/relational/evidence-lifecycle/mapping-accounting.json', lambda d: d['rows'].pop(), 'Lost native disposition')

    def test_deferred_native_disposition_cannot_be_promoted(self):
        def promote(d):
            row = next(r for r in d['rows'] if r['disposition'] == 'DEFERRED_NO_COMPLETE_SQL_MAPPING')
            row['disposition'] = 'FULLY_IMPLEMENTED'
        self.mutate('evaluation/relational/evidence-lifecycle/mapping-accounting.json', promote, 'Native disposition promoted')

    def test_paper_receipt_does_not_allow_changed_private_bytes(self):
        self.mutate(audit.OUT + '/manuscript-readback.json', lambda d: d['artifacts'][0].update(sha256='0' * 64), 'Actual paper bytes differ')

    def test_historical_withdrawn_claim_cannot_be_promoted(self):
        def promote(d):
            d['claim_dispositions'][-1]['historical_disposition'] = 'PASS'
        self.mutate(audit.OUT + '/manuscript-readback.json', promote, 'Paper/historical value promoted')

    def test_missing_approved_amendment_rejected(self):
        self.mutate(audit.OUT + '/manuscript-readback.json', lambda d: d['amendments'].pop(), 'Lost/duplicate approved amendment')

    def test_missing_current_claim_paper_disposition_rejected(self):
        self.mutate(audit.OUT + '/manuscript-readback.json', lambda d: d['current_claim_groups'].pop(), 'Missing current claim paper disposition')


if __name__ == '__main__':
    unittest.main()
