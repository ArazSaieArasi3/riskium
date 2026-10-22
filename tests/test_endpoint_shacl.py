"""Guard endpoint path direction, isolated violations and source-bound integration."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"tools"))
try:import pyshacl
except ImportError:pyshacl=None
if pyshacl:
    import build_endpoint_shapes as b
    import run_endpoint_shacl as h
    from rdflib import Graph
    from rdflib.compare import isomorphic


@unittest.skipUnless(pyshacl,"Install tools/requirements-shacl.txt for endpoint regressions")
class EndpointRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not pyshacl:return
        cls.module=Graph().parse(b.OUT/"endpoints.ttl",format="turtle")
        reviewed=json.loads((ROOT/"evaluation/coverage-review.json").read_text())["obligation_reviews"]
        cls.reviewed=[r for r in reviewed if r["engine"]=="SHACL" and r["family"]=="Managed-profile endpoint cardinality"]
        cls.specs={s["id"]:s for s in h.fixture_specs(cls.module,cls.reviewed)}

    def test_module_and_source_inventory_are_pinned(self):
        graph,receipt=b.render()
        self.assertTrue(isomorphic(graph,self.module))
        self.assertEqual(receipt["ordered_endpoint_shapes"],254)
        self.assertEqual({x["source_element"] for x in receipt["endpoints"]},
                         {x["source_element"] for x in self.reviewed})
        stored=json.loads((b.OUT/"receipt.json").read_text())
        self.assertEqual(stored["shapes_sha256"],h.sha((b.OUT/"endpoints.ttl").read_bytes()))

    def run_spec(self,identifier):return h.execute(self.specs[identifier],Graph(),{})

    def test_unbounded_paths_are_observable_and_mutation_sensitive(self):
        for end in ("source","target"):
            prefix="EP-R-06:"+end
            self.assertEqual(self.run_spec(prefix+"-PATH-WITNESS")["observed"],"CONFORMS")
            result=self.run_spec(prefix+"-REVERSED-PATH")
            self.assertEqual(result["status"],"PASS")
            self.assertEqual({r["component"] for r in result["violations"]},{str(b.SH.HasValueConstraintComponent)})

    def test_lower_and_upper_mutations_change_admission(self):
        for original,mutant in (("BELOW-MIN","RELAXED-MIN"),("ABOVE-MAX","RELAXED-MAX")):
            self.assertEqual(self.run_spec("EP-R-01:target-"+original)["observed"],"VIOLATES")
            self.assertEqual(self.run_spec("EP-R-01:target-"+mutant)["observed"],"CONFORMS")

    def test_paired_minima_report_both_intended_ends(self):
        result=self.run_spec("PAIR-R-56-MISSING")
        self.assertEqual(result["status"],"PASS")
        self.assertEqual({r["shape"] for r in result["violations"]},
            {str(b.E["R-56-source-count"]),str(b.E["R-56-target-count"])})

    def test_alias_and_blank_nodes_respect_value_node_counts(self):
        self.assertEqual(self.run_spec("EP-R-01:target-ALIASED-VALUES")["observed"],"CONFORMS")
        self.assertEqual(self.run_spec("EP-R-01:target-ONE-BLANK")["observed"],"CONFORMS")
        self.assertEqual(self.run_spec("EP-R-01:target-TWO-BLANKS")["observed"],"VIOLATES")

    def test_other_component_cannot_replace_intended_oracle(self):
        spec=dict(self.specs["EP-R-01:target-ABOVE-MAX"],expected=[
            (str(b.E["R-01-target-count"]),str(b.SH.MinCountConstraintComponent))])
        self.assertEqual(h.execute(spec,Graph(),{})["status"],"FAIL")


if __name__=="__main__":unittest.main()
