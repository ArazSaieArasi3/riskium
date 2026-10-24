"""Protect source-edition lineage and preservation of already-withheld case identity."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from rdflib import Graph,RDF
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import run_source_cq0708 as q

class SourceCQ0708Regression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c,cls.e,_=q.inputs();cls.specs={s['id']:s for s in q.specs(cls.c,cls.e)}
    def execute(self,name):return q.case(self.specs[name],self.c,self.e,{})
    def test_original_and_correction_are_distinct_works_with_ten_curated_versions(self):
        sources={s['uri'] for s in self.c['sources']};self.assertEqual(len(sources),2)
        g=q.cq07_graph(self.c,[a['id'] for a in self.c['assertions']]);versions=set(g.subjects(RDF.type,q.N('RKM-C015')))
        self.assertEqual(len(versions),10);self.assertFalse(versions & sources)
        self.assertEqual(len(self.execute('SOURCE-CQ07-ALL-FIVE')['observed_rows']),5)
        self.assertEqual(sum(a['disposition']=='REISSUED_UNCHANGED' for a in self.c['assertions']),1)
    def test_all_11_case_bindings_stay_unbound_without_nonexistence_or_promotion(self):
        row=self.execute('SOURCE-CQ08-ALL-ELEVEN');self.assertEqual(len(row['observed_rows']),11)
        self.assertTrue(all(r[2] is None for r in row['observed_rows']))
        g=q.cq08_graph(self.c,self.e['cq08_unbound_case_ids']);self.assertNotIn((None,RDF.type,q.N('RKM-X01')),g);self.assertNotIn((None,RDF.type,q.N('RKM-C003')),g)
    def test_coherent_forgery_and_identity_guard_deletions_are_observable(self):
        for name in ('CQ07-COHERENT-FORGED-SOURCE','CQ08-FALSE-CASE-LINK'):
            row=self.execute(name);self.assertEqual(row['status'],'PASS');self.assertFalse(row['validator_admits']);self.assertGreater(len(row['observed_rows']),0)
        for name in ('CQ07-DELETED-SOURCE-GUARD-EXPOSES-FORGERY','CQ08-DELETED-IDENTITY-GUARD-EXPOSES-PROMOTION'):
            row=self.execute(name);self.assertTrue(row['validator_admits']);self.assertFalse(row['inspection_task_accepted'])
    def test_original_values_null_denominator_and_single_study_lineage_survive(self):
        for name in ('CQ07-ORIGINAL-OVERWRITE-DETECTED','CQ07-UNKNOWN-DENOMINATOR-NOT-ZERO','CQ07-CORRECTION-NOT-CORROBORATION'):
            row=self.execute(name);self.assertEqual(row['status'],'PASS');self.assertFalse(row['validator_admits'])
        first=self.c['assertions'][0];self.assertIsNone(first['context']['total_paths']);self.assertIsNone(first['original']['standard_error_percent'])
    def test_parser_errors_and_unrelated_findings_do_not_pass(self):
        with patch.object(q,'execute',side_effect=ValueError('malformed query')):
            self.assertEqual(self.execute('QUERY-MUTANT-CQ07-REVERSED')['status'],'ERROR')
        spec=dict(self.specs['CQ07-WRONG-PARENT'],expected_findings=['UNRELATED'])
        self.assertEqual(q.case(spec,self.c,self.e,{})['status'],'FAIL')
        for name in ('QUERY-MUTANT-CQ07-REVERSED','QUERY-MUTANT-CQ07-OVERWRITE-OLD','QUERY-MUTANT-CQ08-BOUND-ONLY','QUERY-MUTANT-CQ08-INVENT-CASE'):
            row=self.execute(name);self.assertEqual(row['status'],'PASS');self.assertIsNone(row['error']);self.assertFalse(row['oracle_equal'])
    def test_expected_fixture_rows_are_independent_and_raw_conflicts_preserved(self):
        row=self.execute('CQ08-MISSING-SOURCE');self.assertIsNone(row['expected_rows'][0][2])
        mutated=copy.deepcopy(self.specs);mutated['CQ08-MISSING-SOURCE']['expected_rows'][0][2]='changed'
        self.assertIsNone(mutated['CQ08-WRONG-SOURCE']['expected_rows'][0][2])
        self.assertEqual(len(self.execute('CQ08-CONFLICTING-CASE-LINKS-PRESERVED')['observed_rows']),2)
        self.assertEqual(len(self.execute('CQ07-CONFLICTING-VALUES-PRESERVED')['observed_rows']),2)
    def test_query_roundtrips_and_title_identity_are_preserved(self):
        for name in ('SERIALIZE-REPARSE-CQ07','SERIALIZE-REPARSE-CQ08','CQ07-EQUAL-TITLES-DISTINCT-ASSERTIONS','CQ08-EQUAL-TITLES-DISTINCT-CANDIDATES'):
            self.assertEqual(self.execute(name)['status'],'PASS')
    def test_saved_bindings_and_graph_tampering_are_rejected(self):
        r=q.run();bad=copy.deepcopy(r);bad['cases'][0]['observed_rows']=[]
        with self.assertRaisesRegex(ValueError,'cases'):q.verify(bad,r)
        bad=copy.deepcopy(r);key=next(iter(bad['graphs']));bad['graphs'][key]+='\n'
        with self.assertRaisesRegex(ValueError,'graphs'):q.verify(bad,r)
        graph=Graph().parse(data=r['graphs'][r['cases'][0]['graph_sha256']],format='nt');self.assertGreater(len(graph),0)

if __name__=='__main__':unittest.main()
