"""Regress source joins, preserved conflicts, genuine mutant execution and frozen oracles."""
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import run_source_cq06 as q
from rdflib import Graph

class SourceCQ06Regression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cohort,cls.expected,_=q.inputs();cls.specs={s['id']:s for s in q.specs(cls.cohort,cls.expected)}
    def execute(self,name):return q.case(self.specs[name],self.cohort,{})
    def test_frozen_source_population_preserves_11_withheld_and_no_cases(self):
        self.assertEqual(len(self.expected['withheld_case_ids']),11)
        self.assertTrue(all(r['risk_case_identity'] is None and not r['occurrence_asserted'] for r in self.cohort['records']))
        row=self.execute('SOURCED-COHORT-13');self.assertEqual(len(row['observed_rows']),13);self.assertTrue(row['trace_task_accepted'])
    def test_coherent_forgery_is_retrievable_but_never_admitted(self):
        row=self.execute('COHERENT-FORGED-SOURCE-IS-REJECTED')
        self.assertEqual(row['status'],'PASS');self.assertEqual(len(row['observed_rows']),1);self.assertFalse(row['validator_admits'])
        mutant=self.execute('GUARD-DELETION-EXPOSES-FORGED-SOURCE');self.assertTrue(mutant['validator_admits']);self.assertFalse(mutant['trace_task_accepted'])
    def test_cross_record_joins_and_missing_provenance_fail_for_exact_reasons(self):
        for name in ('CROSS-RECORD-EVIDENCE','CROSS-RECORD-STATEMENT','MISSING-SOURCE','MISSING-LOCATOR','MISSING-ORIGIN'):
            row=self.execute(name);self.assertEqual(row['status'],'PASS');self.assertFalse(row['trace_task_accepted'])
        spec=dict(self.specs['MISSING-SOURCE'],expected_findings=['unrelated error'])
        self.assertEqual(q.case(spec,self.cohort,{})['status'],'FAIL')
    def test_conflicting_origins_are_retained_without_repair(self):
        row=self.execute('CONFLICTING-ORIGINS-REMAIN-VISIBLE');self.assertEqual(len(row['observed_rows']),2);self.assertFalse(row['validator_admits'])
    def test_parser_failure_is_not_a_detected_mutant(self):
        with patch.object(q,'execute',side_effect=ValueError('broken syntax')):
            self.assertEqual(self.execute('QUERY-MUTANT-CROSS-RECORD')['status'],'ERROR')
        for name in ('QUERY-MUTANT-CROSS-RECORD','QUERY-MUTANT-REVERSED-NATIVE','QUERY-MUTANT-MISSING-ORIGIN'):
            row=self.execute(name);self.assertEqual(row['status'],'PASS');self.assertIsNone(row['error']);self.assertFalse(row['oracle_equal'])
    def test_label_equality_does_not_merge_and_native_case_promotion_is_rejected(self):
        self.assertEqual(len(self.execute('EQUAL-DESCRIPTIONS-KEEP-DISTINCT-IDS')['observed_rows']),2)
        for name in ('NO-CASE-PROMOTION','NO-SCENARIO-PROMOTION','UNTRACKED-RECORD-NOT-ADMITTED'):
            row=self.execute(name);self.assertEqual(row['status'],'PASS');self.assertFalse(row['validator_admits'])
    def test_saved_results_and_graph_mutation_are_detected(self):
        receipt=q.run();changed=copy.deepcopy(receipt);changed['cases'][0]['observed_rows']=[]
        with self.assertRaisesRegex(ValueError,'cases'):q.verify(changed,receipt)
        changed=copy.deepcopy(receipt);key=next(iter(changed['graphs']));changed['graphs'][key]+='\n'
        with self.assertRaisesRegex(ValueError,'graphs'):q.verify(changed,receipt)
        row=receipt['cases'][0];g=Graph().parse(data=receipt['graphs'][row['graph_sha256']],format='nt');self.assertGreater(len(g),0)

if __name__=='__main__':unittest.main()
