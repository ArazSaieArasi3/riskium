"""Verify coherence oracles, unbounded path intent, schema guards and replay."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "tools"))
try: import pyshacl
except ImportError: pyshacl = None
if pyshacl:
    import build_coherence_shapes as b
    import run_coherence_shacl as h
    from rdflib import Graph, OWL, RDF, RDFS
    from rdflib.compare import isomorphic


@unittest.skipUnless(pyshacl, "Install tools/requirements-shacl.txt")
class CoherenceRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = Graph().parse(b.OUT / "coherence.ttl")
        model = json.loads((ROOT / "ontology/riskium-model.json").read_text()); cls.taxonomy = Graph()
        for g in model["generalizations"]: cls.taxonomy.add((b.RISK[g["specific"]], RDFS.subClassOf, b.RISK[g["general"]]))
        cls.specs = {s["id"]: s for s in h.fixture_specs()}

    def run_spec(self, cid, registry=None):
        return h.execute(self.specs[cid], self.module, self.taxonomy, {} if registry is None else registry)

    def test_source_profiles_and_receipt_are_pinned(self):
        graph, receipt = b.render(); self.assertTrue(isomorphic(graph, self.module))
        self.assertEqual({r["id"] for r in receipt["obligations"]}, {"SHACL-0650", "SHACL-0652"})
        stored = json.loads((b.OUT / "receipt.json").read_text())
        self.assertEqual(stored["shapes_sha256"], b.digest(b.OUT / "coherence.ttl"))

    def test_context_direction_and_missing_explicit_pair(self):
        for cid, observed in (("C23-MATCH", "CONFORMS"), ("C23-GENERAL-ONLY", "CONFORMS"),
            ("C23-MISSING-GENERAL", "VIOLATES"), ("C23-DELETED-RULE", "CONFORMS"),
            ("C23-REVERSED-RULE", "VIOLATES")):
            row = self.run_spec(cid); self.assertEqual(row["status"], "PASS", cid); self.assertEqual(row["observed"], observed)

    def test_cycles_are_not_fixed_depth_and_branches_are_permitted(self):
        for cid in ("C24-CYCLE-1", "C24-CYCLE-3", "C24-CYCLE-17", "C24-BRANCH"):
            row = self.run_spec(cid); self.assertEqual(row["status"], "PASS", cid)
        self.assertEqual(len(self.run_spec("C24-CYCLE-17")["violations"]), 17)
        self.assertEqual(self.run_spec("C24-WEAKENED-CYCLE")["observed"], "CONFORMS")
        self.assertEqual(self.run_spec("C24-DELETED-CYCLE")["observed"], "CONFORMS")

    def test_entry_target_equality_and_lineage_are_distinct_rules(self):
        for cid in ("C24-DIFFERENT-ENTRY-TARGETS", "C24-CROSS-ENTRY", "C24-MISSING-VERSION-OF"):
            self.assertEqual(self.run_spec(cid)["status"], "PASS", cid)
        self.assertEqual(self.run_spec("C24-DELETED-EQUALITY")["observed"], "CONFORMS")
        self.assertEqual(self.run_spec("C24-DELETED-LINEAGE")["observed"], "CONFORMS")

    def test_raw_schema_identity_boundary_and_input_preservation(self):
        graph = h.context(); graph.add((b.RISK["RKM-X01"], OWL.sameAs, b.RISK["RKM-C022"]))
        with self.assertRaisesRegex(ValueError, "reserved vocabulary"): b.prepare(graph, "managed")
        raw, mapping = b.prepare(graph, "raw"); self.assertTrue(isomorphic(raw, graph)); self.assertEqual(mapping, {})
        graph = h.context(); graph.add((h.EX.fake, RDFS.subClassOf, b.RISK["RKM-X01"]))
        with self.assertRaisesRegex(ValueError, "schema/import"): b.prepare(graph, "managed")
        graph = h.context(); original = set(graph); b.prepare(graph, "managed"); self.assertEqual(set(graph), original)

    def test_aliases_are_normalized_but_labels_do_not_merge(self):
        for cid in ("C23-CONTEXT-ALIASES", "C23-LABELS-NOT-IDENTITY", "C24-ENTRY-ALIASES", "C24-ALIASED-SELF-LOOP", "C24-LABELS-NOT-IDENTITY"):
            self.assertEqual(self.run_spec(cid)["status"], "PASS", cid)

    def test_saved_blank_graphs_replay_and_unrelated_component_cannot_pass(self):
        registry = {}; row = self.run_spec("C24-BLANK-NODES", registry)
        data, shapes = h.reconstruct_pair({"graphs": registry}, row)
        self.assertTrue(pyshacl.validate(data_graph=data, shacl_graph=shapes, inference="none", meta_shacl=True)[0])
        wrong = dict(self.specs["C23-MISSING-GENERAL"], expected_findings=h.findings("C23Case", "ClassConstraintComponent", h.EX.case))
        self.assertEqual(h.execute(wrong, self.module, self.taxonomy, {})["status"], "FAIL")

    def test_selected_endpoint_and_admission_integration(self):
        for cid, spec in self.specs.items():
            if spec["integration"]: self.assertEqual(self.run_spec(cid)["status"], "PASS", cid)


if __name__ == "__main__": unittest.main()
