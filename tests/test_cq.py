"""CQ regressions for false joins, invented identity and misleading error passes."""
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from rdflib import Graph
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import run_cq
PREFIX='''@prefix risk: <https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#> .
@prefix ex: <urn:test:> . @prefix dct: <http://purl.org/dc/terms/> .
@prefix app: <urn:riskium:cq-profile:0.1.0#> .
@prefix ap: <https://github.com/ArazSaieArasi3/riskium/profiles/catalog/0.3.0#> .
@prefix prov: <http://www.w3.org/ns/prov#> .'''

class CQRegression(unittest.TestCase):
    def query(self,n,ttl,columns):
        graph=Graph().parse(data=PREFIX+'\n'+ttl,format='turtle')
        query=(ROOT/'requirements/cq/queries'/f'RQ-CQ{n:02}.rq').read_text()
        return run_cq.execute(graph,query,columns)

    def test_shared_assessment_does_not_cross_join_score_inputs(self):
        rows=self.query(3,'''ex:a risk:R-17 ex:s1, ex:s2; risk:R-13 ex:r1, ex:r2 .
        ex:s1 risk:R-18 ex:r1 . ex:s2 risk:R-18 ex:r2 .
        ex:r1 risk:RX-016 ex:v1 . ex:r2 risk:RX-016 ex:v2 .
        ex:v1 risk:RX-006 ex:scale1 . ex:v2 risk:RX-006 ex:scale2 .
        ex:scale1 a risk:RKM-C036 . ex:scale2 a risk:RKM-C036 .
        ex:m1 ap:candidate ex:s1; app:numericValue 7 .
        ex:m2 ap:candidate ex:s2; app:numericValue 7 .''',['score','value','scaleVersion','scale'])
        self.assertEqual([(r[0],r[2]) for r in rows],[('<urn:test:s1>','<urn:test:v1>'),('<urn:test:s2>','<urn:test:v2>')])

    def test_equal_labels_do_not_join_different_cases(self):
        self.assertEqual(self.query(1,'''ex:e1 a risk:RKM-C022; risk:R-01 ex:c1; dct:title "same" .
        ex:e2 a risk:RKM-C022; risk:R-01 ex:c2; dct:title "same" .''',['case','entry']),[])

    def test_source_on_another_record_is_not_support(self):
        rows=self.query(6,'''ex:ref risk:R-68 ex:statement; risk:RX-021 ex:item .
        ex:r ap:candidate ex:ref; app:sourceLocator "p1"; app:interpretationOrigin "author" .
        ex:wrong dct:source ex:source .''',['statement','source','locator','origin'])
        self.assertEqual(rows,[])

    def test_same_artifact_does_not_create_correction_lineage(self):
        self.assertEqual(self.query(7,'''ex:r1 ap:candidate ex:v1; dct:source ex:s .
        ex:r2 ap:candidate ex:v2 . ex:v1 risk:RX-006 ex:a . ex:v2 risk:RX-006 ex:a .''',['correctionRecord','previousRecord','source']),[])

    def test_raw_candidate_with_equal_label_stays_without_case(self):
        self.assertEqual(self.query(8,'''ex:r a app:RawScenarioRecord; ap:candidate ex:candidate .
        ex:candidate dct:title "same" . ex:case a risk:RKM-X01; dct:title "same" .''',['record','candidate','case']),[['<urn:test:r>','<urn:test:candidate>',None]])

    def test_closure_does_not_become_asserted_cessation(self):
        rows=self.query(5,'''ex:r risk:R-33 ex:e; risk:R-23 ex:assertion . ex:e risk:R-01 ex:c .
        ex:assertion risk:R-32 ex:closed . ex:closed dct:identifier "closed" .''',['revision','case','cessationEvidence'])
        self.assertEqual(rows,[['<urn:test:r>','<urn:test:c>','"NO_ASSERTED_CESSATION"']])

    def test_remote_service_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'Non-local'):
            run_cq.execute(Graph(),'SELECT ?s WHERE { SERVICE <https://example.org/sparql> { ?s ?p ?o } }',['s'])

    def test_query_error_is_never_a_detected_mutant(self):
        with patch.object(run_cq,'execute',side_effect=ValueError('simulated parse/engine error')):
            report=run_cq.run()
        self.assertEqual(report['status'],'FAIL')
        self.assertEqual(report['summary']['mutants_detected'],0)
        self.assertEqual(report['summary']['query_executions'],0)
        self.assertEqual(report['summary']['statuses'],{'ERROR':40})

    def test_stale_oracle_receipt_is_rejected(self):
        report=run_cq.run();tampered=copy.deepcopy(report)
        tampered['cases'][0]['observed_rows']=[]
        with self.assertRaisesRegex(ValueError,'stale'):
            run_cq.verify(tampered,report)

    def test_independent_population_is_not_promoted_to_accepted(self):
        report=run_cq.run()
        pending={c['cq_id'] for c in report['contracts'] if c['source_population_execution']=='NOT_RUN_ON_DECLARED_INDEPENDENT_POPULATION'}
        self.assertEqual(pending,{'RQ-CQ06','RQ-CQ07','RQ-CQ08'})
        self.assertTrue(all(c['independent_or_real_data_acceptance']=='NOT_ESTABLISHED' for c in report['contracts']))

if __name__=='__main__':unittest.main()
