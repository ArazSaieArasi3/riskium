"""Public API, direct SQL and recovery boundaries beyond the 54 fixed controls."""
import copy
import json
from pathlib import Path
import sqlite3
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import relational_history as b
import relational_assessment as a
import relational_source_scenario as k
import relational_source_scenario_lineage as l
import run_relational_source_scenario_lineage as run


class SourceScenarioLineage(unittest.TestCase):
    def setUp(self):
        self.db = run.fresh()
        self.f = run.fixture()
        self.edge = copy.deepcopy(self.f['declared_edges'][0])

    def tearDown(self):
        self.db.close()

    def test_all_fixed_oracles_and_mutants_match_the_bound_receipt(self):
        actual = run.execute()
        expected = json.loads((run.OUT / 'report.json').read_text())
        self.assertEqual(actual['summary']['outcomes'], {'PASS': 54})
        self.assertEqual(actual['summary']['native_graph_oracles'], 10)
        for key in ('summary', 'cases', 'inputs_sha256'):
            self.assertEqual(actual[key], expected[key])

    def test_nested_failure_preserves_outer_work_and_removes_the_new_version(self):
        with b.transaction(self.db):
            self.db.execute('INSERT INTO source_record VALUES(?,?)', (k.U('outer-source'), '{}'))
            record = self.f['new_records'][0]
            edge = dict(self.f['declared_edges'][1], prior_version_id=k.U('scenario-b-v1'))
            with self.assertRaisesRegex(sqlite3.IntegrityError, 'R-LINEAGE-OWNER'):
                l.issue_corrected(self.db, record, edge)
            self.assertIsNone(self.db.execute('SELECT 1 FROM identity_registry WHERE resource_id=?', (record['version_id'],)).fetchone())
            self.assertIsNotNone(self.db.execute('SELECT 1 FROM source_record WHERE record_id=?', (k.U('outer-source'),)).fetchone())
        l.health(self.db)

    def test_atomic_api_cannot_attach_a_different_existing_child(self):
        before = run.state(self.db)
        with self.assertRaisesRegex(ValueError, 'R-LINEAGE-INPUT'):
            l.issue_corrected(self.db, self.f['new_records'][0], self.edge)
        self.assertEqual(before, run.state(self.db))

    def test_a_second_parent_cannot_replace_the_first_even_if_both_are_valid(self):
        l.declare(self.db, self.edge)
        l.issue(self.db, self.f['new_records'][0])
        other = dict(self.edge, prior_version_id=k.U('scenario-a-v3'))
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'R-LINEAGE-DUPLICATE'):
            l.declare(self.db, other)
        self.assertEqual(self.db.execute('SELECT prior_version_id FROM knowledge_correction').fetchone()[0], self.edge['prior_version_id'])

    def test_raw_sql_rejects_invalid_calendar_without_relying_on_python_validation(self):
        edge = dict(self.edge, recorded_at='2026-02-30T00:00:00Z')
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'R-LINEAGE-TIME'):
            self.db.execute('INSERT INTO knowledge_correction VALUES(?,?,?,?,?,?,?)', tuple(edge[key] for key in l.FIELDS))

    def test_declaration_must_follow_both_endpoint_timestamps(self):
        record = dict(self.f['new_records'][0], recorded_at='2026-10-28T05:00:00Z')
        l.issue(self.db, record)
        edge = self.f['declared_edges'][1]
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'R-LINEAGE-TIME'):
            l.declare(self.db, edge)
        l.declare(self.db, dict(edge, recorded_at='2026-10-28T05:00:00Z'))

    def test_parent_and_child_recording_order_does_not_imply_authority(self):
        record = dict(self.f['new_records'][0], recorded_at='2026-10-26T00:00:00Z')
        edge = self.f['declared_edges'][1]
        l.issue_corrected(self.db, record, edge)
        family = l.family(self.db, k.U('scenario-a-v1'))
        self.assertEqual(len(family['rows']), 2)
        self.assertEqual(family['authority'], 'NOT_SELECTED')
        self.assertEqual(family['independent_corroboration'], 'NOT_ASSESSED')

    def test_unissued_root_is_not_projected_as_a_correction_family(self):
        record = self.f['new_records'][0]
        k.stage(self.db, record)
        self.assertEqual(l.family(self.db, record['version_id'])['rows'], [])
        self.assertEqual(len(l.native_graph(self.db, record['version_id'])), 0)

    def test_corrected_payload_cannot_be_rewritten_after_declaration(self):
        l.issue_corrected(self.db, self.f['new_records'][0], self.f['declared_edges'][1])
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'R-ISSUED-IMMUTABLE'):
            self.db.execute("UPDATE version_snapshot SET payload_json='{}' WHERE version_id=?", (self.f['new_records'][0]['version_id'],))

    def test_declaration_does_not_change_case_query_or_documentary_payloads(self):
        before = l.by_case(self.db, a.BASE('case1'))
        sources = list(self.db.execute('SELECT * FROM source_record ORDER BY record_id'))
        l.declare(self.db, self.edge)
        self.assertEqual(l.by_case(self.db, a.BASE('case1')), before)
        self.assertEqual(list(self.db.execute('SELECT * FROM source_record ORDER BY record_id')), sources)
        self.assertNotEqual(self.db.execute('SELECT original_json FROM source_record WHERE record_id=?', (self.edge['source_record_id'],)).fetchone()[0],
                            self.db.execute('SELECT original_json FROM source_record WHERE record_id=?', (k.U('document-b'),)).fetchone()[0])

    def test_v5_reader_rejects_v6_and_v6_does_not_bootstrap_a_new_empty_database(self):
        with self.assertRaisesRegex(ValueError, 'R-KNOWLEDGE-LEDGER'):
            k.health(self.db)
        empty = b.connect()
        try:
            with self.assertRaisesRegex(ValueError, 'R-LINEAGE-REQUIRES-V5'):
                l.migrate(empty)
            self.assertEqual(b.schema_snapshot(empty), [])
        finally:
            empty.close()

    def test_reader_rejects_recursive_triggers_disabled(self):
        self.db.execute('PRAGMA recursive_triggers=OFF')
        with self.assertRaisesRegex(ValueError, 'R-CONNECTION-POLICY'):
            l.family(self.db, k.U('scenario-a-v1'))

    def test_v6_restore_retains_the_v5_payload_audit(self):
        lines = [line.replace('Possible supplier delay', 'tampered') if line.startswith('INSERT INTO "knowledge_snapshot"') else line for line in self.db.iterdump()]
        target = b.connect()
        try:
            with self.assertRaisesRegex(ValueError, 'R-KNOWLEDGE-DATA-PAYLOAD'):
                l.restore_dump(target, '\n'.join(lines))
            self.assertEqual(b.schema_snapshot(target), [])
        finally:
            target.close()

    def test_three_node_equal_timestamp_cycle_is_rejected(self):
        l.issue(self.db, self.f['new_records'][0])
        l.declare(self.db, self.edge)
        l.declare(self.db, dict(self.f['declared_edges'][1], prior_version_id=k.U('scenario-a-v2'), recorded_at=self.edge['recorded_at']))
        reverse = dict(self.edge, corrected_version_id=k.U('scenario-a-v1'), prior_version_id=k.U('scenario-a-v3'))
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'R-LINEAGE-CYCLE'):
            l.declare(self.db, reverse)
        l.health(self.db)

    def test_all_ten_new_and_old_version_graphs_retain_exact_native_directions(self):
        run.populate(self.db)
        from rdflib.compare import isomorphic
        for name in self.f['graphs']:
            with self.subTest(version=name):
                self.assertTrue(isomorphic(run.expected_graph(name), l.native_graph(self.db, k.U(name))))


if __name__ == '__main__':
    unittest.main()
