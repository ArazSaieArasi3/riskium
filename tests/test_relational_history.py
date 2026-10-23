"""Protect atomic migration, exact SQL oracles and independently fixed history."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import run_relational_history as r

class RelationalRegression(unittest.TestCase):
    def setUp(self):self.specs={s['id']:s for s in r.specs()}
    def test_populated_upgrade_and_invalid_legacy_are_atomic(self):
        for cid in ('MIGRATE-POPULATED-V1','MIGRATE-INVALID-CYCLE-ATOMIC','MIGRATE-FOREIGN-KEY-ATOMIC'):
            self.assertEqual(r.execute(self.specs[cid],{})['status'],'PASS')
    def test_failed_issue_preserves_draft_and_allocated_identity(self):
        row=r.execute(self.specs['ISSUE-ROLLBACK-WRONG-DEPENDENCY-KIND'],{})
        self.assertEqual(row['before_state'],row['after_state']);self.assertEqual(row['status'],'PASS')
    def test_unrelated_sql_error_cannot_satisfy_oracle(self):
        spec=dict(self.specs['ISSUED-NO-DELETE'],error='FOREIGN KEY constraint failed')
        self.assertEqual(r.execute(spec,{})['status'],'FAIL')
    def test_replacement_and_late_dependency_append_are_blocked(self):
        for cid in ('ISSUED-NO-REPLACE','SOURCE-NO-REPLACE','DEPENDENCY-NO-REPLACE','DEPENDENCY-NO-LATE-APPEND'):
            self.assertEqual(r.execute(self.specs[cid],{})['status'],'PASS')
    def test_fixed_history_and_dump_roundtrip(self):
        for cid in ('HISTORY-EXACT','NATIVE-EDGES-EXACT','SQL-DUMP-RESTORE-EXACT'):
            self.assertEqual(r.execute(self.specs[cid],{})['status'],'PASS')
    def test_deleted_guards_expose_corruption(self):
        for cid in ('DELETED-IMMUTABILITY-EXPOSES-CHANGE','DELETED-CYCLE-GUARD-EXPOSES-CYCLE'):
            row=r.execute(self.specs[cid],{});self.assertEqual(row['status'],'PASS');self.assertNotEqual(row['before_state'],row['after_state'])
    def test_source_binding_and_state_tampering_are_rejected(self):
        fresh=r.run();bad=copy.deepcopy(fresh);bad['inputs']['tools/relational_history.py']='changed'
        with self.assertRaisesRegex(ValueError,'binding'):r.verify_saved(bad,fresh)
        bad=copy.deepcopy(fresh);next(iter(bad['states'].values()))['json']='{}'
        with self.assertRaisesRegex(ValueError,'state hash'):r.verify_saved(bad,fresh)

if __name__=='__main__':unittest.main()
