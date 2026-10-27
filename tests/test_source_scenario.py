"""Source/scenario trust boundaries beyond the fixed execution population."""
import copy
import json
from pathlib import Path
import sqlite3
import sys
import unittest
from rdflib.compare import isomorphic

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import relational_source_scenario as k
import relational_history as b
import relational_assessment as a
import run_relational_source_scenario as run

class SourceScenario(unittest.TestCase):
    def setUp(self):
        self.db=run.fresh(seed=True);self.r=copy.deepcopy(run.fixture()['records'][0])
    def tearDown(self):self.db.close()

    def test_fixed_population_and_mutations_match_all_54_predeclared_oracles(self):
        report=run.execute()
        self.assertEqual(report['summary']['outcomes'],{'PASS':54})
        self.assertEqual(report['summary']['kinds']['mutation'],3)
        stored=json.loads((run.OUT/'report.json').read_text())
        self.assertEqual(report['cases'],stored['cases'])
        self.assertEqual(report['inputs_sha256'],stored['inputs_sha256'])

    def test_seal_cannot_smuggle_new_payload_in_the_same_update(self):
        k.stage(self.db,self.r)
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-KNOWLEDGE-PAYLOAD'):
            self.db.execute("UPDATE version_snapshot SET payload_json=json_set(payload_json,'$.narrative','forged'),issued_at=?,is_issued=1 WHERE version_id=?",(self.r['recorded_at'],self.r['version_id']))
        self.assertEqual(self.db.execute('SELECT is_issued FROM version_snapshot WHERE version_id=?',(self.r['version_id'],)).fetchone()[0],0)

    def test_seal_cannot_smuggle_a_different_documentary_source(self):
        k.stage(self.db,self.r)
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-KNOWLEDGE-OWNER-SOURCE'):
            self.db.execute('UPDATE version_snapshot SET source_record_id=?,issued_at=?,is_issued=1 WHERE version_id=?',(k.U('document-b'),self.r['recorded_at'],self.r['version_id']))

    def test_new_case_link_after_issuance_is_rejected(self):
        k.issue(self.db,self.r)
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-KNOWLEDGE-FROZEN'):
            self.db.execute('INSERT INTO knowledge_case VALUES(?,?)',(self.r['version_id'],a.BASE('case2')))
        k.health(self.db)

    def test_valid_other_context_link_after_issuance_is_rejected(self):
        self.r['context_version_ids']=[];k.issue(self.db,self.r)
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-KNOWLEDGE-FROZEN'):
            self.db.execute('INSERT INTO knowledge_context VALUES(?,?,?)',(self.r['version_id'],a.BASE('context'),a.BASE('context-v1')))

    def test_context_multiplicity_for_scenario_is_not_reduced_to_one(self):
        a.add_artifact(self.db,k.U('context2'),'RKM-C002','Context 2')
        a.stage_version(self.db,k.U('context2-v1'),k.U('context2'));a.seal(self.db,k.U('context2-v1'))
        self.r['context_version_ids']=[a.BASE('context-v1'),k.U('context2-v1')]
        k.issue(self.db,self.r)
        self.assertEqual(self.db.execute('SELECT count(*) FROM knowledge_context').fetchone()[0],2)
        g=k.native_graph(self.db,self.r['version_id'])
        self.assertEqual(sum(str(p)==k.RISK+'RK2-010' for _,p,_ in g),2)

    def test_unlinked_source_reference_is_allowed_without_case_invention(self):
        r=copy.deepcopy(run.fixture()['records'][3]);r['case_ids']=[];r['context_version_ids']=[]
        before=list(self.db.execute('SELECT * FROM risk_case'));k.issue(self.db,r)
        self.assertEqual(list(self.db.execute('SELECT * FROM risk_case')),before)
        self.assertEqual(len(k.native_graph(self.db,r['version_id'])),4)

    def test_known_artifact_cannot_gain_conflicting_assessment_typing(self):
        k.issue(self.db,self.r)
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-KNOWLEDGE-TYPE'):
            self.db.execute('INSERT INTO artifact_typing(artifact_id,native_class,source_record_id) VALUES(?,?,?)',(self.r['artifact_id'],'RKM-C032',a.SOURCE))

    def test_existing_context_cannot_be_retyped_as_a_scenario(self):
        self.r['artifact_id']=a.BASE('context')
        with self.assertRaisesRegex(sqlite3.IntegrityError,'R-KNOWLEDGE-TYPE'):k.issue(self.db,self.r)

    def test_native_class_cannot_be_invented_by_the_api(self):
        self.r['native_class']='RKM-C004'
        with self.assertRaisesRegex(ValueError,'R-KNOWLEDGE-TYPE'):k.issue(self.db,self.r)

    def test_nontext_provenance_is_not_silently_coerced(self):
        self.r['source_locator']=0
        with self.assertRaisesRegex(ValueError,'R-KNOWLEDGE-INPUT'):k.issue(self.db,self.r)

    def test_failed_nested_issue_preserves_the_callers_outer_transaction(self):
        with b.transaction(self.db):
            self.db.execute('INSERT INTO source_record VALUES(?,?)',(k.U('outer-source'),'{}'))
            self.r['case_ids']=[k.U('absent-case')]
            with self.assertRaisesRegex(sqlite3.IntegrityError,'R-KNOWLEDGE-CASE'):k.issue(self.db,self.r)
            self.assertIsNotNone(self.db.execute('SELECT 1 FROM source_record WHERE record_id=?',(k.U('outer-source'),)).fetchone())
            self.assertIsNone(self.db.execute('SELECT 1 FROM identity_registry WHERE resource_id=?',(self.r['artifact_id'],)).fetchone())

    def test_a_wrong_document_join_is_exposed_by_the_fixed_provenance_answer(self):
        k.issue(self.db,self.r)
        sql=(k.OUT/'queries/provenance.sql').read_text()
        good=list(self.db.execute(sql,{'version_id':self.r['version_id']}).fetchone())
        bad=sql.replace('s.record_id=k.source_record_id',"s.record_id='urn:riskium:knowledge:document-b'")
        self.assertNotEqual(good,list(self.db.execute(bad,{'version_id':self.r['version_id']}).fetchone()))

    def test_later_source_does_not_replace_the_original_issued_graph(self):
        k.issue(self.db,self.r);original=k.native_graph(self.db,self.r['version_id'])
        later=copy.deepcopy(run.fixture()['records'][1]);k.issue(self.db,later)
        self.assertTrue(isomorphic(original,k.native_graph(self.db,self.r['version_id'])))
        self.assertEqual(self.db.execute('SELECT source_record_id FROM version_snapshot WHERE version_id=?',(self.r['version_id'],)).fetchone()[0],k.U('document-a'))
        self.assertEqual(self.db.execute('SELECT source_record_id FROM version_snapshot WHERE version_id=?',(later['version_id'],)).fetchone()[0],k.U('document-b'))

    def test_restore_audits_empty_provenance_even_if_table_checks_were_bypassed(self):
        k.issue(self.db,self.r)
        lines=[line.replace('Possible supplier delay','') if line.startswith('INSERT INTO') else line for line in self.db.iterdump()]
        other=b.connect();other.execute('PRAGMA ignore_check_constraints=ON')
        try:
            with self.assertRaisesRegex(ValueError,'R-KNOWLEDGE-DATA-PROVENANCE'):k.restore_dump(other,'\n'.join(lines))
            self.assertEqual(b.schema_snapshot(other),[])
        finally:other.close()

    def test_restore_audits_an_unknown_native_type_even_with_checks_bypassed(self):
        k.issue(self.db,self.r)
        lines=[line.replace('RKM-C003','RKM-UNKNOWN') if line.startswith('INSERT INTO') else line for line in self.db.iterdump()]
        other=b.connect();other.execute('PRAGMA ignore_check_constraints=ON')
        try:
            with self.assertRaisesRegex(ValueError,'R-KNOWLEDGE-DATA-TYPE'):k.restore_dump(other,'\n'.join(lines))
            self.assertEqual(b.schema_snapshot(other),[])
        finally:other.close()

if __name__=='__main__':unittest.main()
