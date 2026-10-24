"""Regression checks for versioned SQL mapping, restoration and source boundaries."""
import json
from pathlib import Path
import sqlite3
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
import relational_assessment as a
import relational_history as b
import run_relational_assessment as run
from audit_relational_design import inspect,PURPOSES


class AssessmentRegression(unittest.TestCase):
    def setUp(self):self.c=a.baseline()
    def tearDown(self):self.c.close()

    def test_populated_upgrade_preserves_old_rows_and_is_idempotent(self):
        c=b.connect();b.migrate(c,1);b.seed_v1(c,json.loads((b.OUT/'fixtures.json').read_text()));b.migrate(c)
        old=b.logical_snapshot(c);ledger=list(c.execute('SELECT * FROM schema_migration'));a.migrate(c)
        self.assertEqual(old,b.logical_snapshot(c));self.assertEqual(ledger,list(c.execute('SELECT * FROM schema_migration WHERE version<3')))
        before=run.state(c);a.migrate(c);self.assertEqual(before,run.state(c));c.close()

    def test_failed_additive_migration_rolls_back_schema_data_and_ledger(self):
        c=b.connect();b.migrate(c,1);b.seed_v1(c,json.loads((b.OUT/'fixtures.json').read_text()));b.migrate(c)
        before=(b.logical_snapshot(c),b.schema_snapshot(c),list(c.execute('SELECT * FROM schema_migration')),c.execute('PRAGMA user_version').fetchone())
        text=a.migration_text()+'\nINSERT INTO injected_missing VALUES(1);\n'
        with patch.object(a,'migration_text',return_value=text):
            with self.assertRaisesRegex(sqlite3.OperationalError,'injected_missing'):a.migrate(c)
        self.assertEqual(before,(b.logical_snapshot(c),b.schema_snapshot(c),list(c.execute('SELECT * FROM schema_migration')),c.execute('PRAGMA user_version').fetchone()));c.close()

    def test_direct_role_without_version_cannot_use_a_wrong_native_kind(self):
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-ROLE-KIND'):
            run.row_bundle(self.c,{'method_version_id':None,'method_id':a.BASE('context')},'wrong-method')

    def test_issued_artifact_cannot_gain_a_new_concrete_type(self):
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-TYPE-ALREADY-ISSUED'):
            self.c.execute('INSERT INTO artifact_typing VALUES(?,?,?,?,?,?)',(a.BASE('artifact'),'RKM-C033',None,None,None,a.SOURCE))

    def test_result_identity_cannot_move_to_a_different_assessment_identity(self):
        result=a.default_result('r1');result['result_version_id']=a.U('r1-v2')
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-RESULT-PARENT-IDENTITY'):
            a.issue_bundle(self.c,a.default_assessment('another-assessment'),[result])

    def test_recorded_reference_and_validity_times_remain_distinct_and_calendar_checked(self):
        assessment=a.default_assessment('time-fields');assessment.update(reference_at='2024-02-29T10:00:00Z',valid_from='2026-10-01T00:00:00Z',valid_to='2026-10-31T00:00:00Z')
        a.issue_bundle(self.c,assessment,[a.default_result('time-fields-result')])
        self.assertEqual(self.c.execute('SELECT recorded_at,reference_at,valid_from,valid_to FROM assessment_snapshot WHERE assessment_id=?',(assessment['assessment_id'],)).fetchone(),(a.TIME,'2024-02-29T10:00:00Z','2026-10-01T00:00:00Z','2026-10-31T00:00:00Z'))
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-TIME-LEXICAL'):run.row_bundle(self.c,{'reference_at':'2025-02-29T00:00:00Z'},'bad-leap')

    def test_late_metadata_cannot_change_a_sealed_interpretation(self):
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-ISSUED-METADATA'):
            self.c.execute('INSERT INTO method_scope VALUES(?,?,?,?)',(a.U('method-v3'),a.BASE('scale'),a.U('other-dimension'),a.SOURCE))

    def test_unknown_zero_and_high_precision_lexemes_are_not_coerced_to_numbers(self):
        for index,value in enumerate((None,'0','0.000','100000000000000000000.0001')):
            run.row_bundle(self.c,{'reported_value':value,'score_kind':'UNKNOWN' if value is None else 'REPORTED'},'lexical-'+str(index))
            self.assertEqual(self.c.execute('SELECT reported_value FROM result_snapshot WHERE result_version_id=?',(a.U('lexical-'+str(index)+'-result-v1'),)).fetchone()[0],value)
        with self.assertRaisesRegex(ValueError,'R-REPORTED-LEXEME-TYPE'):run.row_bundle(self.c,{'reported_value':0},'numeric-coercion')

    def test_assessment_rdf_source_is_not_borrowed_from_a_result_source(self):
        other=a.U('other-source');self.c.execute('INSERT INTO source_record VALUES(?,?)',(other,'{"synthetic":"other"}'))
        result=a.default_result('separate-source-result');result['source_record_id']=other
        assessment=a.default_assessment('separate-source');a.issue_bundle(self.c,assessment,[result])
        sources=self.c.execute('SELECT object FROM v_assessment_quads WHERE graph_id=? AND subject=? AND predicate=?',(assessment['assessment_version_id'],assessment['assessment_id'],run.SP+'source')).fetchall()
        self.assertEqual(sources,[(a.SOURCE,)])
        self.assertEqual(self.c.execute('SELECT source_record_id FROM result_snapshot WHERE result_version_id=?',(result['result_version_id'],)).fetchone()[0],other)

    def test_optional_direct_reference_absence_preserves_known_version_target_typing(self):
        from rdflib import RDF,URIRef
        run.row_bundle(self.c,{'context_id':None,'method_id':None},'no-direct')
        graph=run.graph(self.c,a.U('no-direct-v1'))
        self.assertIn((URIRef(a.BASE('context')),RDF.type,URIRef(run.RISK+'RKM-C002')),graph)
        self.assertNotIn((URIRef(a.U('no-direct')),URIRef(run.RISK+'R-45'),URIRef(a.BASE('context'))),graph)
        self.assertEqual(a.compare(self.c,a.U('r1-v1'),a.U('no-direct-result-v1')),'NOT_READY')

    def test_second_result_failure_rolls_back_even_a_first_sealed_result(self):
        before=run.state(self.c);good=a.default_result('bundle-good');bad=a.default_result('bundle-bad');bad['score_kind']='COMPUTED'
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-COMPUTATION-UNSUPPORTED'):a.issue_bundle(self.c,a.default_assessment('bundle'),[good,bad])
        self.assertEqual(run.state(self.c),before)

    def test_restore_audits_data_semantics_even_when_foreign_keys_are_valid(self):
        text='\n'.join(self.c.iterdump());lines=text.splitlines()
        for index,line in enumerate(lines):
            if line.startswith('INSERT INTO "assessment_snapshot"') and a.U('a1-v1') in line:
                lines[index]=line.replace("'"+a.BASE('context-v1')+"'","'"+a.U('method-v3')+"'")
        restored=b.connect()
        with self.assertRaisesRegex(ValueError,'R-ASSESSMENT-DATA-CONTEXT'):a.restore_dump(restored,'\n'.join(lines))
        self.assertEqual(restored.execute("SELECT count(*) FROM sqlite_schema WHERE type='table'").fetchone()[0],0)
        restored.close()

    def test_dropped_guards_block_task_acceptance_instead_of_silently_passing(self):
        self.c.execute('DROP TRIGGER a_result_snapshot_update')
        with self.assertRaisesRegex(ValueError,'R-ASSESSMENT-SCHEMA-DRIFT'):a.compare(self.c,a.U('r1-v1'),a.U('r2-v1'))

    def test_partial_frame_stays_not_ready_in_sql_and_shacl(self):
        result=run.compare_shacl(self.c)
        self.assertTrue(result['matched']);self.assertEqual([r['observed'] for r in result['cases']],['DIRECT_COMPARISON_ADMISSIBLE','NOT_READY'])

    def test_key_only_membership_can_be_justified_but_unexplained_table_is_flagged(self):
        self.c.execute('CREATE TABLE supported_membership(artifact_id TEXT PRIMARY KEY NOT NULL REFERENCES information_artifact(artifact_id)) STRICT')
        report=inspect(self.c,dict(PURPOSES,supported_membership='Explicit subtype membership of an existing artifact; PK/FK supplies its identity.'))
        self.assertFalse(any(r['table']=='supported_membership' for r in report['findings']))
        self.c.execute('CREATE TABLE unexplained(id TEXT PRIMARY KEY NOT NULL) STRICT')
        self.assertTrue(any(r['code']=='UNEXPLAINED_ONE_COLUMN_TABLE' for r in inspect(self.c)['findings']))

    def test_supplied_field_names_cannot_inject_sql_and_failure_rolls_back(self):
        before=run.state(self.c);assessment=a.default_assessment('fields');assessment['x); DROP TABLE result_snapshot; --']='bad'
        with self.assertRaisesRegex(ValueError,'R-API-FIELDS'):a.issue_bundle(self.c,assessment,[a.default_result('fields-result')])
        self.assertEqual(run.state(self.c),before)

    def test_unrelated_error_cannot_satisfy_a_fixed_failure_oracle(self):
        cohort=json.loads(run.FIXTURE.read_text());case=next(c for c in cohort['cases'] if c['id']=='COMPUTED-WITHOUT-FORMULA')
        observed=run.execute(dict(case,expected_error='unrelated'))
        self.assertEqual(observed['observed_error'],'R-COMPUTATION-UNSUPPORTED');self.assertEqual(observed['status'],'FAIL')


if __name__=='__main__':unittest.main()
