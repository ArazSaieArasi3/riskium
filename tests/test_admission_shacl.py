"""Check focus integrity, taxonomy boundaries, exact oracles and replay fidelity."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
try:
    import pyshacl
except ImportError:
    pyshacl = None
if pyshacl:
    import build_admission_shapes as b
    import run_admission_shacl as h
    from rdflib import Graph, Literal, OWL, RDF, RDFS
    from rdflib.compare import isomorphic


@unittest.skipUnless(pyshacl, "Install tools/requirements-shacl.txt for admission checks")
class AdmissionRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads((b.OUT / "receipt.json").read_text())
        cls.model = json.loads((ROOT / "ontology/riskium-model.json").read_text())
        cls.module = Graph().parse(b.OUT / "admission.ttl")
        cls.taxonomy = Graph()
        for g in cls.model["generalizations"]:
            cls.taxonomy.add((b.RISK[g["specific"]], RDFS.subClassOf, b.RISK[g["general"]]))
        cls.endpoints = Graph().parse(ROOT / "ontology/shacl/0.2.0/endpoints.ttl")
        cls.catalog = set(cls.receipt["core_classes"] + cls.receipt["excluded_boundaries"])
        cls.specs = {s["id"]: s for s in h.fixture_specs(cls.model, cls.receipt["core_classes"], cls.receipt["excluded_boundaries"])}

    def run_spec(self, identifier, registry=None):
        return h.execute(self.specs[identifier], self.module, self.taxonomy, self.catalog,
                         {} if registry is None else registry, self.endpoints)

    def test_source_inventory_and_boundary_profiles(self):
        graph, receipt = b.render()
        self.assertTrue(isomorphic(graph, self.module))
        self.assertEqual(len(receipt["core_classes"]), 77)
        self.assertEqual(len(receipt["excluded_boundaries"]), 3)
        for cid in receipt["excluded_boundaries"]:
            self.assertFalse(any(graph.triples((b.A["For-" + cid], None, None))))
            self.assertEqual(self.run_spec(cid + "-CORE-EXCLUSION")["observed"], "VIOLATES")

    def test_empty_or_unknown_focus_configuration_cannot_pass(self):
        data, record, _ = h.fixture_record("RKM-C001")
        for requests, profile in (([], "managed-catalog"), ([(record, "UNKNOWN")], "managed-catalog"),
                                  ([(record, "RKM-C001")], "risk-assessment")):
            with self.assertRaises(ValueError): b.compile_request(self.module, data, requests, profile, self.catalog)

    def test_managed_schema_injection_is_rejected_and_raw_preserved(self):
        data, record, _ = h.fixture_record("RKM-C001")
        data.add((h.EX.ForgedClass, RDFS.subClassOf, b.RISK["RKM-C001"]))
        with self.assertRaisesRegex(ValueError, "schema/import"):
            b.compile_request(self.module, data, [(record, "RKM-C001")], "managed-catalog", self.catalog)
        _, raw, mapping = b.compile_request(self.module, data, [(record, "RKM-C001")], "raw", self.catalog)
        self.assertTrue(isomorphic(raw, data)); self.assertEqual(mapping, {})
        data, record, candidate = h.fixture_record("RKM-C001")
        data.set((candidate, RDF.type, b.RISK["RKM-C002"]))
        data.add((b.RISK["RKM-C002"], OWL.sameAs, b.RISK["RKM-C001"]))
        with self.assertRaisesRegex(ValueError, "reserved vocabulary"):
            b.compile_request(self.module, data, [(record, "RKM-C001")], "managed-catalog", self.catalog)
        _, raw, _ = b.compile_request(self.module, data, [(record, "RKM-C001")], "raw", self.catalog)
        self.assertTrue(isomorphic(raw, data))

    def test_identity_conflicts_are_not_engine_passes_and_raw_is_unmodified(self):
        data, record, candidate = h.fixture_record("RKM-C001")
        data.add((candidate, OWL.sameAs, h.EX.alias)); data.add((candidate, OWL.differentFrom, h.EX.alias))
        with self.assertRaisesRegex(ValueError, "identity conflict"):
            b.compile_request(self.module, data, [(record, "RKM-C001")], "managed-catalog", self.catalog)
        _, raw, _ = b.compile_request(self.module, data, [(record, "RKM-C001")], "raw", self.catalog)
        self.assertTrue(isomorphic(data, raw))

    def test_missing_metadata_and_rule_mutations_have_opposite_outcomes(self):
        for invalid, mutation in (("MISSING-SOURCE", "SOURCE-MUTANT"), ("UNTYPED", "UNTYPED-MUTANT")):
            self.assertEqual(self.run_spec("RKM-C001-" + invalid)["observed"], "VIOLATES")
            self.assertEqual(self.run_spec("RKM-C001-" + mutation)["observed"], "CONFORMS")

    def test_catalog_task_is_explicit_and_cannot_claim_risk_assessment(self):
        for name, outcome in (("TASK", "CONFORMS"), ("MISSING-TASK", "VIOLATES"),
                              ("UNSUPPORTED-TASK", "VIOLATES")):
            self.assertEqual(self.run_spec("RKM-C001-" + name)["observed"], outcome)

    def test_unrelated_violation_cannot_substitute_for_oracle(self):
        spec = dict(self.specs["RKM-C001-MISSING-SOURCE"], expected_findings=[
            (str(b.A.Source), str(b.SH.MaxCountConstraintComponent), str(h.EX["RKM-C001-record"]))])
        result = h.execute(spec, self.module, self.taxonomy, self.catalog, {}, self.endpoints)
        self.assertEqual(result["status"], "FAIL")

    def test_shared_blank_focus_replays_with_identical_outcome(self):
        registry = {}; row = self.run_spec("RKM-C001-BLANK-RECORD", registry)
        self.assertEqual(row["status"], "PASS")
        data, shapes = h.reconstruct_pair({"graphs": registry}, row)
        conforms, result, _ = pyshacl.validate(data_graph=data, shacl_graph=shapes, inference="none", meta_shacl=True)
        self.assertFalse(conforms)
        report = next(result.subjects(RDF.type, b.SH.ValidationReport))
        findings = [(result.value(n, b.SH.sourceShape), result.value(n, b.SH.sourceConstraintComponent))
                    for n in result.objects(report, b.SH.result)]
        self.assertEqual(findings, [(b.A.Record, b.SH.NodeKindConstraintComponent)])

    def test_candidate_does_not_inherit_record_metadata_requirements(self):
        data, record, candidate = h.fixture_record("RKM-C001")
        self.assertFalse(list(data.triples((candidate, b.DC.title, None))))
        shapes, _, _ = b.compile_request(self.module, data, [(record, "RKM-C001")], "managed-catalog", self.catalog)
        self.assertNotIn((b.A.Record, b.SH.targetNode, candidate), shapes)
        self.assertEqual(self.run_spec("RKM-C001-MANAGED")["status"], "PASS")

    def test_alias_focus_and_equal_labels_do_not_erase_scope(self):
        self.assertEqual(self.run_spec("RKM-C001-FOCUS-ALIAS")["status"], "PASS")
        self.assertEqual(self.run_spec("RKM-C001-SAME-LABEL")["status"], "PASS")
        data, record, _ = h.fixture_record("RKM-C001")
        data.add((record, OWL.sameAs, h.EX.alias))
        with self.assertRaisesRegex(ValueError, "Conflicting expected classes"):
            b.compile_request(self.module, data, [(record, "RKM-C001"), (h.EX.alias, "RKM-C002")],
                              "managed-catalog", self.catalog)


if __name__ == "__main__":
    unittest.main()
