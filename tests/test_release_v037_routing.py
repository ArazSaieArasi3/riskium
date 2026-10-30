"""Do not substitute a legacy failure, stale source or branch run for main qualification."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('routing037', ROOT/'tools/releases/v037/routing.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class MainRouting(unittest.TestCase):
    def evidence(self):
        source = 'a'*40
        return dict(source_commit=source, runs={role:dict(head_sha=source, head_branch='main',
            path='.github/workflows/'+filename, repository=dict(full_name=r.REPO),
            head_repository=dict(full_name=r.REPO), event='workflow_run' if role=='reader' else 'push',
            status='completed', conclusion='failure' if role=='legacy' else 'success')
            for role,filename in r.PATHS.items()}, legacy_job_log='\n'.join(r.ERRORS)+'\nFAILED (errors=3)')

    def test_selected_legacy_and_reader_sources_remain_unchanged(self):
        self.assertEqual(r.check()['required_success'], ['qualification','suite','reader'])

    def test_all_exact_main_gates_and_only_known_legacy_failure_are_required(self):
        self.assertEqual(r.validate_runs(self.evidence())['next_gate'],'FINAL_EXACT_SOURCE_FREEZE')
        for role in ('qualification','suite','reader'):
            evidence=self.evidence();evidence['runs'][role]['conclusion']='failure'
            with self.assertRaisesRegex(ValueError,'Unexpected'):r.validate_runs(evidence)

    def test_branch_stale_workflow_or_unsettled_runs_cannot_pass(self):
        for field,value in [('head_sha','b'*40),('head_branch','plan/v0.3.7-packaging'),
                            ('path','.github/workflows/incremental-release.yml'),('status','in_progress')]:
            evidence=self.evidence();evidence['runs']['qualification'][field]=value
            with self.assertRaises(ValueError):r.validate_runs(evidence)

    def test_other_legacy_errors_or_missing_gate_cannot_pass(self):
        evidence=self.evidence();evidence['legacy_job_log']='Unexpected error'
        with self.assertRaisesRegex(ValueError,'Unexpected legacy'):r.validate_runs(evidence)
        evidence=self.evidence();evidence['legacy_job_log']+='\nFAILED (failures=1, errors=3)'
        with self.assertRaisesRegex(ValueError,'additional'):r.validate_runs(evidence)
        evidence=self.evidence();evidence['runs'].pop('suite')
        with self.assertRaisesRegex(ValueError,'Missing'):r.validate_runs(evidence)


if __name__ == '__main__':
    unittest.main()
