"""Regression guards for declared comparison tasks and reviewer separation."""
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"tools"))
try:import pyshacl
except ImportError:pyshacl=None
if pyshacl:
    from rdflib import Graph, Literal, OWL, RDF, RDFS
    import build_comparison_shapes as b
    import run_comparison_shacl as h


@unittest.skipUnless(pyshacl,"Install tools/requirements-shacl.txt")
class ComparisonRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module,cls.receipt=b.render();cls.taxonomy=Graph()
        for g in json.loads((ROOT/"ontology/riskium-model.json").read_text())["generalizations"]:
            cls.taxonomy.add((b.RISK[g["specific"]],RDFS.subClassOf,b.RISK[g["general"]]))
        cls.specs={s["id"]:s for s in h.fixture_specs()}

    def execute(self,spec,registry=None):
        return h.execute(spec,self.module,self.receipt,self.taxonomy,{} if registry is None else registry)

    def test_fixture_graphs_are_independent_and_explicit_difference_is_retained(self):
        bad=self.specs["CROSS-TEMPORAL-CONTEXT"]["raw"];unknown=self.specs["UNRESOLVED-TEMPORAL-CONTEXT"]["raw"]
        self.assertIn((h.EX.otherTemporal,OWL.differentFrom,h.EX.temporal),bad)
        self.assertNotIn((h.EX.otherTemporal,OWL.differentFrom,h.EX.temporal),unknown)
        before=set(bad);unknown.add((h.EX.extra,RDFS.label,Literal("changed")));self.assertEqual(set(bad),before)

    def test_empty_and_graph_supplied_focus_cannot_be_accepted(self):
        with self.assertRaisesRegex(ValueError,"five named"):b.prepare(h.base(),"direct-comparison",[])
        g=h.base();g.add((h.EX.request,b.SP.leftAssessment,h.EX.leftAssessment))
        with self.assertRaisesRegex(ValueError,"focus selectors"):b.prepare(g,"direct-comparison",h.REQUEST)
        g=h.base();g.add((b.SP.source,OWL.sameAs,b.SP.temporalContext))
        with self.assertRaisesRegex(ValueError,"reserved"):b.prepare(g,"direct-comparison",h.REQUEST)

    def test_equal_codes_and_labels_cannot_override_method_version_mismatch(self):
        row=self.execute(self.specs["EQUAL-LABELS-AND-NUMBERS-NOT-COMPARABLE"])
        self.assertEqual((row["status"],row["observed"]),("PASS","NOT_COMPARABLE"))

    def test_missing_time_and_unresolved_identity_do_not_become_zero_or_acceptance(self):
        for cid in ("MISSING-TIME","UNRESOLVED-TEMPORAL-CONTEXT"):
            row=self.execute(self.specs[cid]);self.assertEqual((row["status"],row["observed"]),("PASS","NOT_READY"))

    def test_missing_membership_mutation_is_detectable_and_oracle_is_exact(self):
        row=self.execute(self.specs["MISSING-MEMBERSHIP"]);self.assertEqual(row["observed"],"NOT_READY")
        mutant=self.execute(self.specs["DELETED-MEMBERSHIP-RULE"]);self.assertEqual(mutant["observed"],"DIRECT_COMPARISON_ADMISSIBLE")
        wrong=dict(self.specs["MISSING-MEMBERSHIP"],expected_findings=h.findings("RightMissingMembership"))
        self.assertEqual(self.execute(wrong)["status"],"FAIL")

    def test_metadata_envelopes_do_not_repair_missing_domain_type_and_graphs_replay(self):
        registry={};row=self.execute(self.specs["INTEGRATED-UNTYPED-RESULT"],registry)
        self.assertEqual((row["status"],row["observed"]),("PASS","INVALID"))
        data,shapes=h.reconstruct_pair({"graphs":registry},row)
        self.assertNotIn((h.EX.leftResult,RDF.type,b.RISK["RKM-C034"]),data)
        self.assertFalse(pyshacl.validate(data_graph=data,shacl_graph=shapes,inference="none",meta_shacl=True)[0])

    def test_aliases_and_temporal_rule_deletion_have_distinct_fixed_oracles(self):
        for cid in ("METHOD-EXPLICIT-ALIASES","TEMPORAL-EXPLICIT-ALIAS","DELETED-TEMPORAL-RULE"):
            row=self.execute(self.specs[cid]);self.assertEqual((row["status"],row["observed"]),("PASS","DIRECT_COMPARISON_ADMISSIBLE"))


if __name__=="__main__":unittest.main()
