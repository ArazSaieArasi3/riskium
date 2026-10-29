"""Exact oracles, storage-boundary faults and recovery for the new SQL slice."""
import copy
from pathlib import Path
import sqlite3
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import relational_risk_nature as x
import run_relational_risk_nature as run
import build_risk_nature_schema as schema


class RiskNatureTests(unittest.TestCase):
    def setUp(self):self.db=run.fresh()
    def tearDown(self):self.db.close()

    def test_generated_sql_and_declaration_remain_bound(self):
        self.assertEqual(x.SQL.read_text(),schema.build());x.bindings()

    def test_literal_rows_graphs_and_unlinked_later_version(self):
        run.later(self.db)
        for v,expected in run.O['get'].items():
            self.assertEqual(x.get(self.db,v)['row'],expected)
        self.assertTrue(run.native_match(self.db,run.O['get']))
        self.assertEqual(x.family(self.db,run.U('A-v1'))['lineage'],run.O['family'][run.U('A-v1')])

    def test_sql_guards_reject_corrupted_values_after_api_validation(self):
        insert=x.insert
        for field,value,code in [('term_version_id',run.U('objective-v1'),'TERM_VERSION'),
                                  ('context_version_id',run.U('negative-v1'),'CONTEXT_VERSION'),
                                  ('source_locator','\t \n','PROVENANCE'),
                                  ('source_locator','\u00a0\u2007\u202f','PROVENANCE'),
                                  ('recorded_at','2026-02-30T08:00:00Z','TIME')]:
            def corrupt(db,table,row):
                return insert(db,table,dict(row,**{field:value}) if table=='nature_snapshot' else row)
            before=x.state(self.db)
            with patch.object(x,'insert',side_effect=corrupt),self.assertRaisesRegex(sqlite3.IntegrityError,'NRA-'+code):
                run.later(self.db)
            self.assertEqual(x.state(self.db),before)

    def test_sql_seal_detects_changed_payload_and_missing_recorders(self):
        with x.b.transaction(self.db):
            bundle=copy.deepcopy(run.I['later_unlinked_bundle']);x.stage_bundle(self.db,bundle)
            v=bundle['assertion']['version_id']
            with self.assertRaisesRegex(sqlite3.IntegrityError,'NRA-'):
                self.db.execute('UPDATE version_snapshot SET is_issued=1,issued_at=?,payload_json=? WHERE version_id=?',(bundle['assertion']['recorded_at'],'{}',v))
            with self.assertRaisesRegex(sqlite3.IntegrityError,'NRA-RECORDING'):
                x.a.seal(self.db,v,bundle['assertion']['recorded_at'])

    def test_restored_valid_but_rewritten_source_is_detected_by_trusted_digest(self):
        run.later(self.db);dump='\n'.join(self.db.iterdump());digest=x.state_sha256(self.db)
        changed=dump.replace('Reported unfavorable effect on delivery objective','Edited documentary source about delivery objective')
        self.assertNotEqual(changed,dump)
        target=x.b.connect()
        try:
            with self.assertRaisesRegex(ValueError,'NRA-RESTORE_DIGEST'):x.restore_dump(target,changed,digest)
            self.assertEqual(x.b.schema_snapshot(target),[])
        finally:target.close()

    def test_late_subtype_reuse_and_late_recording_link_are_blocked(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute('INSERT INTO nature_entry_link VALUES(?,?)',(run.U('entry-1-r1'),run.U('A-v2')))
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute('INSERT INTO knowledge_type VALUES(?,?)',(run.U('A'),'RKM-C003'))
        x.health(self.db)

    def test_schema_drift_and_valid_schema_data_tampering_are_separate(self):
        guard=self.db.execute("SELECT sql FROM sqlite_master WHERE name='nature_snapshot_update'").fetchone()[0]
        self.db.execute('DROP TRIGGER nature_snapshot_update')
        with self.assertRaisesRegex(ValueError,'NRA-SCHEMA'):x.health(self.db)
        self.db.execute('UPDATE nature_snapshot SET context_version_id=? WHERE version_id=?',(run.U('context-v2'),run.U('A-v1')))
        self.db.execute(guard)
        with self.assertRaisesRegex(ValueError,'NRA-DATA_PAYLOAD'):x.health(self.db)
