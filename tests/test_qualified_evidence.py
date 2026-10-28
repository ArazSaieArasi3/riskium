"""Qualification, contextual role, atomicity and inherited-audit boundaries."""
import copy
import json
from pathlib import Path
import sqlite3
import sys
import unittest

from rdflib import RDF, URIRef
from rdflib.compare import isomorphic

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import relational_history as b
import relational_assessment as a
import relational_source_scenario as k
import relational_source_scenario_lineage as l
import relational_evidence as e
import run_relational_evidence as run


class QualifiedEvidence(unittest.TestCase):
    def setUp(self):
        self.db = run.fresh()
        self.record = copy.deepcopy(run.fixture()['records'][0])

    def tearDown(self):
        self.db.close()

    def test_fixed_62_controls_and_mutations_match_bound_receipt(self):
        actual = run.execute()
        expected = json.loads((run.OUT / 'report.json').read_text())
        self.assertEqual(actual['summary']['outcomes'], {'PASS': 62})
        self.assertEqual(actual['summary']['kinds']['mutation'], 4)
        for key in ('summary', 'cases', 'inputs_sha256'):
            self.assertEqual(actual[key], expected[key])

    def test_nested_failed_issue_preserves_outer_work_without_partial_reference_identity(self):
        with b.transaction(self.db):
            self.db.execute('INSERT INTO source_record VALUES(?,?)', (e.U('outer-source'), '{}'))
            self.record['target_version_ids'].append(e.U('missing'))
            with self.assertRaisesRegex(ValueError, 'R-EVIDENCE-TARGET'):
                e.issue(self.db, self.record)
            self.assertIsNone(self.db.execute('SELECT 1 FROM identity_registry WHERE resource_id=?', (self.record['artifact_id'],)).fetchone())
            self.assertIsNotNone(self.db.execute('SELECT 1 FROM source_record WHERE record_id=?', (e.U('outer-source'),)).fetchone())
        e.health(self.db)

    def test_an_existing_knowledge_artifact_can_play_the_contextual_item_role(self):
        old = run.knowledge_graph(self.db, k.U('scenario-b-v1'))
        self.record['item_version_id'] = k.U('scenario-b-v1')
        e.issue(self.db, self.record)
        graph = e.native_graph(self.db, self.record['version_id'])
        self.assertIn((URIRef(k.U('scenario-b')), RDF.type, URIRef(k.RISK + 'RKM-C066')), graph)
        self.assertTrue(isomorphic(old, run.knowledge_graph(self.db, k.U('scenario-b-v1'))))
        self.assertNotIn((URIRef(k.U('scenario-b')), RDF.type, URIRef(k.RISK + 'RKM-C066')), old)

    def test_item_role_does_not_create_a_second_bearer_identity(self):
        before = list(self.db.execute('SELECT resource_id FROM identity_registry ORDER BY resource_id'))
        e.issue(self.db, self.record)
        after = set(x[0] for x in self.db.execute('SELECT resource_id FROM identity_registry'))
        self.assertEqual(after - {x[0] for x in before}, {self.record['artifact_id'], self.record['version_id']})
        self.assertEqual(self.db.execute('SELECT kind FROM information_artifact WHERE artifact_id=?', (e.U('item-a'),)).fetchone()[0], 'RKM-C014')

    def test_two_references_to_the_same_item_are_not_independent_corroboration(self):
        run.populate(self.db)
        answer = e.by_target(self.db, k.U('scenario-a-v1'))
        self.assertEqual(len(answer['rows']), 2)
        self.assertEqual(len({row[4] for row in answer['rows']}), 1)
        self.assertEqual(answer['independent_corroboration'], 'NOT_ASSESSED')
        self.assertEqual(answer['endorsement'], 'NOT_INFERRED')

    def test_same_update_cannot_smuggle_a_different_documentary_source(self):
        e.stage(self.db, self.record)
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'R-EVIDENCE-OWNER-SOURCE'):
            self.db.execute('UPDATE version_snapshot SET source_record_id=?,issued_at=?,is_issued=1 WHERE version_id=?',
                            (e.U('document-b'), self.record['recorded_at'], self.record['version_id']))
        self.assertEqual(self.db.execute('SELECT is_issued FROM version_snapshot WHERE version_id=?', (self.record['version_id'],)).fetchone()[0], 0)

    def test_raw_sql_calendar_check_is_not_only_an_api_check(self):
        e.stage(self.db, self.record)
        forged = dict(self.record, version_id=e.U('forged-v1'), item_id=e.U('item-a'), recorded_at='2026-02-30T00:00:00Z')
        a.stage_version(self.db, forged['version_id'], forged['artifact_id'], payload=e.payload(forged), source=forged['source_record_id'])
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'R-EVIDENCE-TIME'):
            self.db.execute('INSERT INTO evidence_snapshot VALUES(?,?,?,?,?,?,?,?,?,?)', tuple(forged[key] for key in e.FIELDS))

    def test_artifact_origin_does_not_replace_later_item_version_source(self):
        e.issue(self.db, run.fixture()['records'][1])
        row = e.by_target(self.db, k.U('scenario-a-v2'))['rows'][0]
        self.assertEqual(row[11], e.U('document-b'))
        self.assertEqual(self.db.execute('SELECT source_record_id FROM information_artifact WHERE artifact_id=?', (e.U('item-a'),)).fetchone()[0], e.U('document-a'))

    def test_v7_restore_preserves_prior_lineage_semantic_audits(self):
        lines = [line.replace('Revise scenario interpretation', '') if line.startswith('INSERT INTO "knowledge_correction"') else line for line in self.db.iterdump()]
        target = b.connect()
        target.execute('PRAGMA ignore_check_constraints=ON')
        try:
            with self.assertRaisesRegex(ValueError, 'R-LINEAGE-DATA-PROVENANCE'):
                e.restore_dump(target, '\n'.join(lines))
            self.assertEqual(b.schema_snapshot(target), [])
        finally:
            target.close()

    def test_v7_restore_preserves_prior_knowledge_payload_audits(self):
        lines = [line.replace('Possible supplier delay', 'tampered') if line.startswith('INSERT INTO "knowledge_snapshot"') else line for line in self.db.iterdump()]
        target = b.connect()
        try:
            with self.assertRaisesRegex(ValueError, 'R-KNOWLEDGE-DATA-PAYLOAD'):
                e.restore_dump(target, '\n'.join(lines))
            self.assertEqual(b.schema_snapshot(target), [])
        finally:
            target.close()

    def test_reference_cannot_gain_conflicting_knowledge_typing(self):
        e.issue(self.db, self.record)
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'R-EVIDENCE-TYPE'):
            self.db.execute('INSERT INTO knowledge_type VALUES(?,?)', (self.record['artifact_id'], 'RKM-C003'))

    def test_reference_cannot_gain_conflicting_assessment_typing(self):
        e.issue(self.db, self.record)
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'R-EVIDENCE-TYPE'):
            self.db.execute('INSERT INTO artifact_typing(artifact_id,native_class,source_record_id) VALUES(?,?,?)', (self.record['artifact_id'], 'RKM-C032', a.SOURCE))

    def test_reference_typing_cannot_be_replaced_or_deleted(self):
        e.issue(self.db, self.record)
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'R-EVIDENCE-DUPLICATE'):
            self.db.execute('INSERT OR REPLACE INTO evidence_reference_type VALUES(?)', (self.record['artifact_id'],))
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'R-EVIDENCE-IMMUTABLE'):
            self.db.execute('DELETE FROM evidence_reference_type')
        e.health(self.db)

    def test_old_reader_rejects_v7_and_new_reader_does_not_silently_bootstrap(self):
        with self.assertRaisesRegex(ValueError, 'R-LINEAGE-LEDGER'):
            l.health(self.db)
        empty = b.connect()
        try:
            with self.assertRaisesRegex(ValueError, 'R-EVIDENCE-REQUIRES-V6'):
                e.migrate(empty)
            self.assertEqual(b.schema_snapshot(empty), [])
        finally:
            empty.close()

    def test_nontext_target_pin_is_not_silently_coerced(self):
        self.record['target_version_ids'] = [0]
        before = run.state(self.db)
        with self.assertRaisesRegex(ValueError, 'R-EVIDENCE-INPUT'):
            e.issue(self.db, self.record)
        self.assertEqual(run.state(self.db), before)

    def test_reader_rejects_recursive_trigger_configuration_drift(self):
        self.db.execute('PRAGMA recursive_triggers=OFF')
        with self.assertRaisesRegex(ValueError, 'R-CONNECTION-POLICY'):
            e.by_target(self.db, k.U('scenario-a-v1'))


if __name__ == '__main__':
    unittest.main()
