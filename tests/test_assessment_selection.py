"""Additional transactional, historical and restoration boundaries for SQL v9."""
import copy
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import run_assessment_selection as run
import relational_assessment_selection as x
import relational_history as b


class AssessmentSelection(unittest.TestCase):
    def setUp(self):
        self.db=run.fresh()

    def tearDown(self):
        self.db.close()

    def test_complete_bundle_has_no_other_version_results(self):
        run.timeline(self.db)
        answer=x.selection(self.db,run.U('A'),'X',2)
        self.assertEqual(answer['results'],[dict(r,assessment_version_id=run.U('A-v2')) for r in run.M['bundles']['A-v2']['results']])
        self.assertEqual(answer['assessment'],run.M['bundles']['A-v2']['assessment'])

    def test_issue_records_supplied_timestamp_and_each_source(self):
        row=run.M['bundles']['A-v4'];x.issue(self.db,row['assessment'],row['results'])
        for version,source in [(row['assessment']['assessment_version_id'],row['assessment']['source_record_id']), (row['results'][0]['result_version_id'],row['results'][0]['source_record_id'])]:
            self.assertEqual(self.db.execute('SELECT issued_at,source_record_id FROM version_snapshot WHERE version_id=?',(version,)).fetchone(),(row['assessment']['recorded_at'],source))

    def test_invalid_second_result_rolls_back_whole_issue(self):
        row=copy.deepcopy(run.M['bundles']['A-v4']);row['results'].append(dict(row['results'][0],result_version_id=run.U('bad-result'),reported_value=42))
        before=x.state(self.db)
        with self.assertRaisesRegex(ValueError,'LEXEME'):x.issue(self.db,row['assessment'],row['results'])
        self.assertEqual(x.state(self.db),before)

    def test_correction_failure_rolls_back_issued_bundle(self):
        row=run.M['bundles']['A-v4'];before=x.state(self.db)
        with self.assertRaises(sqlite3.IntegrityError):
            x.issue(self.db,row['assessment'],row['results'],dict(prior_version=run.U('B-v1'),reason='cross identity',recorded_at=run.M['correction_time'],source_record_id=run.U('S-decision')))
        self.assertEqual(x.state(self.db),before)

    def test_equal_times_and_reverse_names_use_sequence(self):
        x.append(self.db,run.event(ident='z-first'));x.append(self.db,run.event(target='A-v2',ident='a-second'))
        self.assertEqual(x.selection(self.db,run.U('A'),'X',1)['assessment_version'],run.U('A-v1'))
        self.assertEqual(x.selection(self.db,run.U('A'),'X',2)['assessment_version'],run.U('A-v2'))

    def test_raw_blank_provenance_and_context_are_rejected(self):
        for field in ('actor','reason','source_locator','interpretation_origin','decision_context_id'):
            ev=run.event();ev[field]='\t\n\r '
            result,error=run.rejected(self.db,lambda:run.sql_event(self.db,ev))
            self.assertTrue(result['rejected'],field);self.assertTrue(result['all_preoperation_state_preserved'])

    def test_raw_early_time_and_explicit_sequence_are_rejected(self):
        row=run.M['bundles']['A-v4'];x.issue(self.db,row['assessment'],row['results'])
        ev=run.event(target='A-v4');ev['recorded_at']='2026-10-29T09:00:00Z'
        self.assertTrue(run.rejected(self.db,lambda:run.sql_event(self.db,ev))[0]['rejected'])
        for seq in (-1,0,1,99):
            result,error=run.rejected(self.db,lambda:run.sql_event(self.db,run.event(),{'ordinal':seq}))
            self.assertTrue(result['rejected']);self.assertTrue(result['all_preoperation_state_preserved'])

    def test_duplicate_ignore_and_replace_cannot_hide_event(self):
        x.append(self.db,run.event())
        for conflict in ('IGNORE','REPLACE'):
            with self.assertRaises(sqlite3.IntegrityError):
                self.db.execute('INSERT OR '+conflict+' INTO assessment_selection_event SELECT * FROM assessment_selection_event')
        x.health(self.db)

    def test_legacy_evidence_clock_and_rows_are_preserved(self):
        before=self.db.execute('SELECT * FROM evidence_lifecycle_event').fetchall();clock=self.db.execute("SELECT seq FROM sqlite_sequence WHERE name='evidence_lifecycle_event'").fetchone()
        run.timeline(self.db)
        self.assertEqual(self.db.execute('SELECT * FROM evidence_lifecycle_event').fetchall(),before)
        self.assertEqual(self.db.execute("SELECT seq FROM sqlite_sequence WHERE name='evidence_lifecycle_event'").fetchone(),clock)
        x.health(self.db)

    def test_valid_but_edited_restore_is_rejected_by_trusted_digest(self):
        run.timeline(self.db);dump='\n'.join(self.db.iterdump());digest=x.state_sha256(self.db)
        changed=dump.replace("'X'","'brand-new-context'");self.assertNotEqual(dump,changed)
        target=b.connect()
        try:
            with self.assertRaisesRegex(ValueError,'RESTORE_DIGEST'):x.restore_dump(target,changed,digest)
            self.assertEqual(b.schema_snapshot(target),[])
        finally:target.close()

    def test_restore_rejects_external_database_statements(self):
        target=b.connect()
        try:
            with self.assertRaisesRegex(ValueError,'RESTORE_STATEMENT'):x.restore_dump(target,"ATTACH DATABASE ':memory:' AS external;\n",'0'*64)
            self.assertEqual(len(target.execute('PRAGMA database_list').fetchall()),1)
        finally:target.close()

    def test_context_and_selection_do_not_change_native_graphs(self):
        before=self.db.execute('SELECT * FROM v_assessment_quads ORDER BY graph_id,subject,predicate,object').fetchall()
        run.timeline(self.db)
        after=self.db.execute('SELECT * FROM v_assessment_quads ORDER BY graph_id,subject,predicate,object').fetchall()
        self.assertEqual(before,after)


if __name__=='__main__':unittest.main()
