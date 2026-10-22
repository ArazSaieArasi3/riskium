"""Focused source, oracle and replay checks for C-11/C-12."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
try: import pyshacl
except ImportError: pyshacl=None
if pyshacl:
    from rdflib import Graph, RDF, RDFS
    from rdflib.compare import isomorphic
    import build_qualification_shapes as b
    import run_qualification_shacl as q


@unittest.skipUnless(pyshacl,"Install tools/requirements-shacl.txt")
class QualificationRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module=Graph().parse(b.OUT/"qualification.ttl")
        cls.receipt=json.loads((b.OUT/"receipt.json").read_text())
        model=json.loads((ROOT/"ontology/riskium-model.json").read_text())
        cls.taxonomy=Graph()
        for g in model["generalizations"]:
            cls.taxonomy.add((b.RISK[g["specific"]],RDFS.subClassOf,b.RISK[g["general"]]))
        cls.cases={x["id"]:x for x in q.specs(cls.receipt["vocabulary_classes"],set(cls.receipt["classified_term_classes"]))}

    def run_case(self,name,registry=None):
        return q.execute(self.cases[name],self.module,self.taxonomy,
                         set(self.receipt["classified_term_classes"]),{} if registry is None else registry)

    def test_source_and_two_obligations_pinned(self):
        graph,receipt=b.render()
        self.assertTrue(isomorphic(graph,self.module))
        self.assertEqual({o["id"] for o in receipt["obligations"]},{"SHACL-0626","SHACL-0628"})
        self.assertEqual(b.digest(b.OUT/"qualification.ttl"),self.receipt["shapes_sha256"])
        self.assertEqual(len(self.receipt["vocabulary_classes"]),14)

    def test_all_vocabulary_subtypes_and_distinct_keys(self):
        for cid in self.receipt["vocabulary_classes"]:
            self.assertEqual(self.run_case("VOC-"+cid)["status"],"PASS",cid)
        for name in ("VOC-DUPLICATE-KEY","VOC-OTHER-SCHEME","VOC-OTHER-EDITION",
                     "VOC-ASSERTED-ALIAS","VOC-SCHEME-MISMATCH"):
            self.assertEqual(self.run_case(name)["status"],"PASS",name)

    def test_roles_source_and_explicit_pairs(self):
        for name in ("EVIDENCE-SUPPORT","EVIDENCE-CHALLENGE","EVIDENCE-CONTEXT",
                     "EVIDENCE-SUPPORT-WITHOUT-PAIR","EVIDENCE-CHALLENGE-WITH-SUPPORT-PAIR",
                     "EVIDENCE-MISSING-ITEM-PAIR","EVIDENCE-LITERAL-SOURCE",
                     "EVIDENCE-UNKNOWN-ROLE"):
            self.assertEqual(self.run_case(name)["status"],"PASS",name)

    def test_mutations_are_detectable_and_oracles_are_specific(self):
        for name in ("VOC-DELETED-AGREEMENT","VOC-DELETED-UNIQUENESS",
                     "EVIDENCE-DELETED-ITEM-RULE","EVIDENCE-DELETED-ROLE-RULE"):
            self.assertEqual(self.run_case(name)["observed"],"CONFORMS",name)
        spec=dict(self.cases["VOC-DUPLICATE-KEY"],expected_findings=q.findings(
            "VocabularyRecord","ClassConstraintComponent",q.EX["v-record-RKM-C019"]))
        self.assertEqual(q.execute(spec,self.module,self.taxonomy,
            set(self.receipt["classified_term_classes"]),{})["status"],"FAIL")

    def test_raw_and_selected_integration(self):
        for name in ("VOC-RAW-INCOMPLETE","EVIDENCE-RAW","VOC-INTEGRATED","EVIDENCE-INTEGRATED"):
            self.assertEqual(self.run_case(name)["status"],"PASS",name)

    def test_snapshot_replay(self):
        registry={};row=self.run_case("VOC-DUPLICATE-KEY",registry)
        data,shapes=q.reconstruct_pair({"graphs":registry},row)
        self.assertFalse(pyshacl.validate(data_graph=data,shacl_graph=shapes,inference="none",meta_shacl=True)[0])

    def test_nonempty_focus_and_schema_guard(self):
        spec=dict(self.cases["VOC-RKM-C019"],requests=[])
        self.assertEqual(q.execute(spec,self.module,self.taxonomy,
            set(self.receipt["classified_term_classes"]),{})["status"],"ERROR")
        graph,record,term=q.vocab()
        graph.add((term,RDFS.subClassOf,b.RISK["RKM-C017"]))
        spec=dict(self.cases["VOC-RKM-C019"],raw=graph)
        self.assertEqual(q.execute(spec,self.module,self.taxonomy,
            set(self.receipt["classified_term_classes"]),{})["status"],"ERROR")


if __name__=="__main__":unittest.main()
