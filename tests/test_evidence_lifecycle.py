"""Transaction, SQL guard, history, source and recovery boundaries for v8."""
import copy
import json
from pathlib import Path
import sqlite3
import sys
import unittest

from rdflib.compare import isomorphic

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import relational_evidence_lifecycle as x
import relational_evidence as e
import relational_history as b
import run_relational_evidence_lifecycle as run
import run_relational_evidence as old


class EvidenceLifecycle(unittest.TestCase):
    def setUp(self):
        self.db = run.fresh()

    def tearDown(self):
        self.db.close()

    def raw(self, event):
        self.db.execute('INSERT INTO evidence_lifecycle_event(' + ','.join(x.FIELDS) + ') VALUES(' +
                        ','.join('?' for _ in x.FIELDS) + ')', tuple(event[k] for k in x.FIELDS))

    def test_all_frozen_controls_and_actual_weakened_guard_match_the_receipt(self):
        actual = run.execute()
        expected = json.loads((run.OUT / 'report.json').read_text())
        self.assertEqual(actual['summary']['outcomes'], {'PASS': 43})
        self.assertEqual(actual['summary']['fixed_query_mutations'], 3)
        self.assertEqual(actual['supplementary_controls'][0]['status'], 'PASS')
        for key in ('summary', 'cases', 'supplementary_controls', 'inputs_sha256'):
            self.assertEqual(actual[key], expected[key])

    def test_raw_sql_cannot_select_a_withdrawn_version(self):
        run.seed_decisions(self.db, 20)
        before = run.state(self.db)
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'ELC-WITHDRAWN_IN_CONTEXT'):
            self.raw(run.event('SELECT', 'forbidden', 'ref-A@2', None, 'review-X'))
        self.assertEqual(run.state(self.db), before)

    def test_raw_sql_cycle_is_rejected_without_api_prevalidation(self):
        run.seed_corrections(self.db)
        before = run.state(self.db)
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'ELC-CYCLE'):
            self.raw(run.event(ident='cycle', version='ref-A@1', parent='ref-A@4'))
        self.assertEqual(run.state(self.db), before)

    def test_context_isolation_with_real_selections_in_both_contexts(self):
        x.append(self.db, run.event('SELECT', 'x', 'ref-A@2', None, 'review-X'))
        x.append(self.db, run.event('SELECT', 'y', 'ref-A@2', None, 'review-Y'))
        x.append(self.db, run.event('WITHDRAW', 'withdraw-x', 'ref-A@2', None, 'review-X'))
        self.assertEqual(x.selection(self.db, run.alias('ref-A'), 'review-X', 30)['status'], 'WITHDRAWN')
        self.assertEqual(x.selection(self.db, run.alias('ref-A'), 'review-Y', 30)['selected_version'], run.alias('ref-A@2'))
        self.assertEqual(x.selection(self.db, run.alias('ref-A'), 'review-X', 19)['status'], 'SELECTED')

    def test_equal_utc_and_reverse_event_names_still_use_database_sequence(self):
        x.append(self.db, run.event('SELECT', 'z-first', 'ref-A@2', None, 'review-X'))
        x.append(self.db, run.event('SELECT', 'a-second', 'ref-A@3', None, 'review-X'))
        self.assertEqual([r['sequence'] for r in x.ledger(self.db)], [10, 20])
        self.assertEqual(x.selection(self.db, run.alias('ref-A'), 'review-X', 19)['selected_version'], run.alias('ref-A@2'))
        self.assertEqual(x.selection(self.db, run.alias('ref-A'), 'review-X', 20)['selected_version'], run.alias('ref-A@3'))

    def test_nested_failed_issue_rolls_back_identity_event_and_allocator_only(self):
        record = dict(old.fixture()['records'][1], version_id=run.alias('ref-A@5'))
        with b.transaction(self.db):
            self.db.execute('INSERT INTO source_record VALUES(?,?)', ('urn:fixture:outer', '{}'))
            with self.assertRaisesRegex(ValueError, 'ELC-UNKNOWN_ENDPOINT'):
                x.issue_corrected(self.db, record, run.event(version='ref-A@5', parent='absent'))
            self.assertIsNone(self.db.execute('SELECT 1 FROM identity_registry WHERE resource_id=?', (record['version_id'],)).fetchone())
            self.assertIsNotNone(self.db.execute("SELECT 1 FROM source_record WHERE record_id='urn:fixture:outer'").fetchone())
            self.assertEqual(x.append(self.db, run.event())['sequence'], 10)
        x.health(self.db)

    def test_replace_and_ignore_cannot_suppress_duplicate_event_rejection(self):
        x.append(self.db, run.event('SELECT', 'unique', 'ref-A@2', None, 'review-X'))
        before = run.state(self.db)
        for conflict in ('REPLACE', 'IGNORE'):
            with self.assertRaisesRegex(sqlite3.IntegrityError, 'ELC-DUPLICATE_EVENT_ID'):
                self.db.execute('INSERT OR ' + conflict + ' INTO evidence_lifecycle_event SELECT * FROM evidence_lifecycle_event')
            self.assertEqual(run.state(self.db), before)

    def test_supplied_sequence_and_missing_provenance_are_never_filled(self):
        for item, code in ((dict(run.event(), ordinal=99), 'INVALID_INPUT'),
                           (dict(run.event(), source_locator=None), 'MISSING_PROVENANCE'),
                           (dict(run.event(), actor_id=' '), 'MISSING_PROVENANCE')):
            before = run.state(self.db)
            with self.assertRaisesRegex(ValueError, 'ELC-' + code):
                x.append(self.db, item)
            self.assertEqual(run.state(self.db), before)

    def test_as_of_is_explicit_nonnegative_integer_including_bool_rejection(self):
        for value in (None, -1, 1.0, True, '10', 2**63):
            with self.assertRaisesRegex(ValueError, 'ELC-INVALID_AS_OF_SEQUENCE'):
                x.selection(self.db, run.alias('ref-A'), 'review-X', value)
        self.assertEqual(x.selection(self.db, run.alias('ref-A'), 'review-X', 0)['status'], 'NO_SELECTION')

    def test_clear_preserves_withdrawal_notice_and_does_not_reinstate_a_version(self):
        run.seed_decisions(self.db)
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'ELC-WITHDRAWN_IN_CONTEXT'):
            x.append(self.db, run.event('SELECT', 'reinstate', 'ref-A@2', None, 'review-X'))
        self.assertEqual(len(x.ledger(self.db)), 4)
        self.assertEqual(x.selection(self.db, run.alias('ref-A'), 'review-X', 40)['status'], 'NO_SELECTION')

    def test_raw_sql_calendar_guard_checks_actual_date(self):
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'ELC-INVALID_RECORDED_TIME'):
            self.raw(dict(run.event(), recorded_at='2026-02-30T12:00:00Z'))
        self.assertEqual(x.ledger(self.db), [])

    def test_raw_sql_cannot_skip_the_ordinal_or_rewrite_it(self):
        event = run.event()
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'ELC-INVALID_SEQUENCE'):
            self.db.execute('INSERT INTO evidence_lifecycle_event(ordinal,' + ','.join(x.FIELDS) + ') VALUES(9,' +
                            ','.join('?' for _ in x.FIELDS) + ')', tuple(event[k] for k in x.FIELDS))
        self.assertEqual(x.append(self.db, event)['sequence'], 10)
        with self.assertRaisesRegex(sqlite3.IntegrityError, 'ELC-IMMUTABLE'):
            self.db.execute('UPDATE evidence_lifecycle_event SET ordinal=2')

    def test_declaration_source_is_distinct_from_artifact_origin_and_child_source(self):
        x.append(self.db, run.event(source='decision-source-1'))
        row = x.family(self.db, run.alias('ref-A@1'))['rows'][1]
        self.assertEqual(row['version_source'], run.alias('source-correction'))
        self.assertEqual(row['declaration_source'], run.alias('decision-source-1'))
        origin = self.db.execute('SELECT source_record_id FROM information_artifact WHERE artifact_id=?', (run.alias('ref-A'),)).fetchone()[0]
        self.assertEqual(origin, run.alias('source-original'))
        self.assertEqual(len({row['version_source'], row['declaration_source'], origin}), 3)

    def test_old_reader_refuses_v8_without_writing(self):
        before = run.state(self.db)
        with self.assertRaisesRegex(ValueError, 'R-EVIDENCE-LEDGER'):
            e.health(self.db)
        self.assertEqual(before, run.state(self.db))

    def test_dump_restore_clock_tamper_rolls_back_every_schema_object(self):
        run.seed_decisions(self.db)
        lines = list(self.db.iterdump())
        changed = []
        found = False
        for line in lines:
            if line.startswith('INSERT INTO "sqlite_sequence"'):
                line = 'INSERT INTO "sqlite_sequence" VALUES(\'evidence_lifecycle_event\',999);'
                found = True
            changed.append(line)
        self.assertTrue(found)
        target = b.connect()
        try:
            with self.assertRaisesRegex(ValueError, 'ELC-SEQUENCE'):
                x.restore_dump(target, '\n'.join(changed))
            self.assertEqual(b.schema_snapshot(target), [])
            self.assertEqual(target.execute('PRAGMA user_version').fetchone()[0], 0)
        finally:
            target.close()

    def test_restore_replays_new_contextual_withdrawal_audit(self):
        run.seed_decisions(self.db, 30)
        dump = '\n'.join(line.replace(run.alias('ref-A@3'), run.alias('ref-A@2'))
                         if line.startswith('INSERT INTO "evidence_lifecycle_event"') and "'SELECT'" in line else line
                         for line in self.db.iterdump())
        target = b.connect()
        try:
            with self.assertRaisesRegex(ValueError, 'ELC-DATA_WITHDRAWN_IN_CONTEXT'):
                x.restore_dump(target, dump)
            self.assertEqual(b.schema_snapshot(target), [])
        finally:
            target.close()

    def test_restore_retains_original_knowledge_payload_audit(self):
        dump = '\n'.join(line.replace('Possible supplier delay', 'tampered')
                         if line.startswith('INSERT INTO "knowledge_snapshot"') else line for line in self.db.iterdump())
        target = b.connect()
        try:
            with self.assertRaisesRegex(ValueError, 'R-KNOWLEDGE-DATA-PAYLOAD'):
                x.restore_dump(target, dump)
            self.assertEqual(b.schema_snapshot(target), [])
        finally:
            target.close()

    def test_schema_ledger_and_connection_drift_are_rejected(self):
        self.db.execute('PRAGMA recursive_triggers=OFF')
        with self.assertRaisesRegex(ValueError, 'R-CONNECTION-POLICY'):
            x.selection(self.db, run.alias('ref-A'), 'review-X', 0)
        self.db.execute('PRAGMA recursive_triggers=ON')
        with b.transaction(self.db):
            self.db.execute("UPDATE schema_migration SET sha256='tampered' WHERE version=8")
            with self.assertRaisesRegex(ValueError, 'ELC-LEDGER'):
                x.health(self.db)
            self.db.execute('UPDATE schema_migration SET sha256=? WHERE version=8', (x.digest(),))
        self.db.execute('DROP INDEX evidence_lifecycle_context')
        with self.assertRaisesRegex(ValueError, 'ELC-SCHEMA'):
            x.health(self.db)

    def test_plain_new_reference_issue_adds_no_correction_or_selection(self):
        original = x.native_graph(self.db, run.alias('ref-A@1'))
        record = dict(old.fixture()['records'][1], version_id=run.alias('ref-A@5'))
        x.issue(self.db, record)
        self.assertEqual(x.family(self.db, run.alias('ref-A@1'))['version_ids'], [run.alias('ref-A@1')])
        self.assertEqual(x.selection(self.db, run.alias('ref-A'), 'review-X', 999)['status'], 'NO_SELECTION')
        self.assertTrue(isomorphic(original, x.native_graph(self.db, run.alias('ref-A@1'))))

    def test_query_parameters_are_bound_without_cross_context_or_schema_effect(self):
        run.seed_decisions(self.db)
        before = run.state(self.db)
        self.assertEqual(x.selection(self.db, run.alias('ref-A'), "' OR 1=1 --", 999)['status'], 'NO_SELECTION')
        self.assertEqual(x.family(self.db, "'; DROP TABLE evidence_lifecycle_event; --")['rows'], [])
        self.assertEqual(before, run.state(self.db))


if __name__ == '__main__':
    unittest.main()
