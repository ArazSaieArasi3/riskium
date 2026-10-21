"""Regressions for meaningful structural defects; not a formal ontology suite."""
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from validate_model import validate
MODEL=json.loads((ROOT/'ontology/riskium-model.json').read_text())

class StructuralRegression(unittest.TestCase):
    def mutate(self,change,expected):
        value=copy.deepcopy(MODEL);change(value);self.assertIn(expected,validate(value))
    def test_current_design(self):self.assertEqual(validate(MODEL),[])
    def test_duplicate_identity(self):self.mutate(lambda m:m['concepts'].append(copy.deepcopy(m['concepts'][0])),'duplicate concepts identifier')
    def test_lost_domain_member(self):self.mutate(lambda m:m['domains'][0]['concept_ids'].pop(),'domain membership mismatch')
    def test_unknown_endpoint(self):self.mutate(lambda m:m['associations'][0].update(target='missing'),'unresolved relation endpoint')
    def test_reversed_cardinality(self):self.mutate(lambda m:m['associations'][0].update(target_end_cardinality='3..1'),'reversed cardinality')
    def test_malformed_cardinality(self):self.mutate(lambda m:m['associations'][0].update(target_end_cardinality='several'),'invalid cardinality')
    def test_untyped_core(self):self.mutate(lambda m:m['concepts'][0].update(ontouml_stereotype=None),'untyped core concept')
    def test_inheritance_cycle(self):self.mutate(lambda m:m['generalizations'].append({'id':'test-cycle','specific':m['generalizations'][0]['general'],'general':m['generalizations'][0]['specific']}),'generalization cycle')
    def test_lost_bearer(self):self.mutate(lambda m:m.update(associations=[r for r in m['associations'] if r.get('stereotype')!='characterization']),'mode lacks exactly-one bearer')

if __name__=='__main__':unittest.main()
