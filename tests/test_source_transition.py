"""Guard the transfer of historical evidence to unchanged candidate sources."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import check_source_transition as transition


class SourceTransition(unittest.TestCase):
    def test_research_implementation_drift_is_rejected(self):
        for path in ('ontology/riskium-model.json', 'implementation/relational/0.9.0/schema.sql',
                     'tools/relational_risk_nature.py', 'tests/test_risk_nature.py',
                     'releases/selection-v0.3.7.json'):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'Research source changed'):
                transition.classify(path, transition.blob_digest(b'original'), b'edited')

    def test_deleted_reviewed_files_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Deleted reviewed file'):
            transition.classify('README.md', 'a' * 40, None)

    def test_new_scientific_code_cannot_inherit_old_receipts(self):
        for path in ('tools/new_risk_engine.py', 'implementation/relational/1.0.0/schema.sql',
                     'ontology/replacement.owl', 'evaluation/hermit/new-report.json'):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'Unqualified added source'):
                transition.classify(path, None, b'new')

    def test_reader_replacement_is_explicit_and_unchanged_code_is_reused(self):
        self.assertEqual(transition.classify('README.md', transition.blob_digest(b'old'), b'new'),
                         'CURRENT_READER_BINDING')
        self.assertEqual(transition.classify('tools/relational_risk_nature.py',
                         transition.blob_digest(b'exact'), b'exact'), 'UNCHANGED_REVIEWED_SOURCE')

    def test_actual_candidate_has_complete_reviewed_source_accounting(self):
        result = transition.check()
        self.assertGreater(result['unchanged_reviewed_files'], 1300)
        self.assertEqual(result['historical_source'], transition.BASELINE)
        self.assertFalse(result['scientific_model_changed'])


if __name__ == '__main__':
    unittest.main()
