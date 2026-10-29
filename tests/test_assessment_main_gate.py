"""Deployment ordering must not race queued successors or accept a failed source suite."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools/publication'))
import assessment_main_gate as gate


class DeploymentOrdering(unittest.TestCase):
    def runs(self):
        return [dict(id=i, name=name, head_sha='candidate', head_branch='main',
                     event='push' if name in (gate.DOCUMENTATION, gate.INCREMENTAL, gate.SUITE) else 'workflow_run',
                     status='completed', conclusion='success' if name in (gate.DOCUMENTATION, gate.PAGES, gate.SUITE) else 'failure')
                for i, name in enumerate((gate.DOCUMENTATION, gate.INCREMENTAL, gate.SUITE,
                                          gate.PAGES, gate.STATUS, gate.PUBLISHED), start=1)]

    def test_completed_legacy_attempts_do_not_block_new_source(self):
        self.assertEqual(gate.settled(self.runs(), 'candidate', 99), [])

    def test_not_yet_queued_descendant_blocks_deployment(self):
        runs = [r for r in self.runs() if r['name'] != gate.STATUS]
        self.assertTrue(any(gate.STATUS in p for p in gate.settled(runs, 'candidate', 99)))

    def test_running_old_attempt_and_stale_source_cannot_be_treated_as_settled(self):
        runs = self.runs()
        runs[-1]['status'] = 'in_progress'
        self.assertTrue(gate.settled(runs, 'candidate', 99))
        self.assertTrue(gate.settled(self.runs(), 'another-source', 99))

    def test_failed_source_suite_blocks_even_after_all_publishers_finish(self):
        runs = self.runs()
        next(r for r in runs if r['name'] == gate.SUITE)['conclusion'] = 'failure'
        with self.assertRaisesRegex(ValueError, 'Source-qualified suite failed'):
            gate.settled(runs, 'candidate', 99)


if __name__ == '__main__':
    unittest.main()
