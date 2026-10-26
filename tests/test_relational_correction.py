"""Correction lineage, source boundaries and restoration regression oracles."""
import json
from pathlib import Path
import sqlite3
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
import relational_assessment as a
import relational_correction as c
import run_relational_correction as run


class CorrectionRegression(unittest.TestCase):
    def test_saved_receipt_replays_and_retains_every_predeclared_negative(self):
        actual=run.execute();saved=json.loads((run.OUT/'report.json').read_text())
        for key in ('inputs_sha256','summary','cases'):self.assertEqual(saved[key],actual[key])
        negative=set(json.loads((c.OUT/'fixtures.json').read_text())['negative_cases'])
        self.assertTrue(negative.issubset({r['id'] for r in actual['cases']}))
        self.assertEqual(actual['summary']['passed'],actual['summary']['cases'])

    def test_conflicting_branches_preserve_sources_and_do_not_select_latest(self):
        db=run.fresh();run.complete_family(db)
        result=c.family(db,a.U('a1-v1'))
        self.assertEqual(result['selection'],'ALL_DECLARED_BRANCHES')
        self.assertEqual([r[3] for r in result['rows']],['0','0.25',None])
        self.assertEqual(result['rows'][-1][-1],a.U('other-source'))
        self.assertEqual(result['independent_corroboration'],'NOT_ASSESSED');db.close()

    def test_old_reader_rejects_new_schema_and_new_reader_rejects_tampering(self):
        db=run.fresh()
        with self.assertRaisesRegex(ValueError,'R-ASSESSMENT-MIGRATION-LEDGER'):a.health(db)
        db.execute('DROP INDEX correction_parent')
        with self.assertRaisesRegex(ValueError,'R-CORRECTION-SCHEMA'):c.health(db)
        db.close()

    def test_empty_bundle_has_no_partial_identity_or_version(self):
        db=run.fresh();old=run.state(db);assessment,_=run.bundle()
        with self.assertRaisesRegex(ValueError,'R-CORRECTION-EMPTY-BUNDLE'):
            c.issue_corrected(db,assessment,[],a.U('a1-v1'),'reason',run.TIME,a.SOURCE)
        self.assertEqual(run.state(db),old);db.close()

    def test_chain_depth_and_cycle_oracles_remain_distinct(self):
        db=run.fresh();prior=a.U('a1-v1')
        for n in range(2,26):
            run.issue(db,str(n),str(n),prior=prior);prior=a.U('a1-v'+str(n))
        depth=db.execute((c.OUT/'queries/descendants.sql').read_text(),dict(root=a.U('a1-v1'))).fetchall()
        self.assertEqual(max(d for _,d in depth),24)
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-CORRECTION-CYCLE'):
            db.execute('INSERT INTO assessment_correction VALUES(?,?,?,?,?)',(a.U('a1-v1'),prior,'cycle',run.TIME,a.SOURCE))
        self.assertEqual(c.family(db,a.U('a1-v1'))['rows'][0][3],'0');db.close()

    def test_bad_calendar_and_missing_role_fail_atomic_issuance(self):
        db=run.fresh();old=run.state(db);assessment,result=run.bundle();assessment['context_version_id']=a.U('absent')
        with self.assertRaises(sqlite3.IntegrityError):
            c.issue_corrected(db,assessment,[result],a.U('a1-v1'),'reason',run.TIME,a.SOURCE)
        self.assertEqual(old,run.state(db));db.close()

if __name__=='__main__':unittest.main()
