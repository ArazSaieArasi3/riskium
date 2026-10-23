"""C-08 guards, exact oracles, preserved staging and declaration boundaries."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "tools"))
try: import pyshacl
except ImportError: pyshacl = None
if pyshacl:
    from rdflib import Graph, OWL, RDF, RDFS
    from rdflib.compare import isomorphic
    import build_compatibility_shapes as b
    import run_compatibility_shacl as h


@unittest.skipUnless(pyshacl, "Install tools/requirements-shacl.txt")
class CompatibilityRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module, _ = b.render(); cls.taxonomy = Graph()
        for g in json.loads((ROOT / "ontology/riskium-model.json").read_text())["generalizations"]:
            cls.taxonomy.add((b.RISK[g["specific"]], RDFS.subClassOf, b.RISK[g["general"]]))
        cls.specs = {s["id"]: s for s in h.fixture_specs()}

    def test_schema_and_reserved_aliases_reject_without_mutating_raw(self):
        g = h.base(); g.add((h.EX.fake, RDFS.subClassOf, b.RISK["RKM-C070"]))
        before = set(g)
        with self.assertRaisesRegex(ValueError, "schema/import"): b.prepare(g, "dual-anchor-metadata", [h.EX.threshold])
        raw, _ = b.prepare(g, "raw", [h.EX.threshold]); self.assertEqual(set(g), before); self.assertTrue(isomorphic(raw, g))
        g = h.base(); g.add((b.CP.Numeric, OWL.sameAs, b.CP.Qualitative))
        with self.assertRaisesRegex(ValueError, "reserved compatibility"): b.prepare(g, "dual-anchor-metadata", [h.EX.threshold])

    def test_empty_focus_and_bad_focus_do_not_become_acceptance(self):
        from rdflib import BNode
        for focus in ([], [BNode("threshold")]):
            with self.assertRaisesRegex(ValueError, "nonempty named"): b.prepare(h.base(), "dual-anchor-metadata", focus)

    def test_missing_metadata_cannot_be_mistaken_for_a_compatible_pair(self):
        spec = self.specs["C08-MISSING-INDICATOR-UNIT"]
        row = h.execute(spec, self.module, self.taxonomy, {})
        self.assertEqual((row["status"], row["observed"]), ("PASS", "NOT_READY"))
        wrong = dict(spec, expected_decision="COMPATIBLE_FOR_DECLARED_TASK", expected_findings=[])
        self.assertEqual(h.execute(wrong, self.module, self.taxonomy, {})["status"], "FAIL")

    def test_unrelated_failure_cannot_satisfy_exact_oracle(self):
        wrong = dict(self.specs["C08-DIFFERENT-UNIT"], expected_findings=h.findings("DimensionMatch"))
        self.assertEqual(h.execute(wrong, self.module, self.taxonomy, {})["status"], "FAIL")

    def test_saved_graphs_replay_and_rule_deletion_is_observable(self):
        registry = {}; row = h.execute(self.specs["C08-DIFFERENT-UNIT"], self.module, self.taxonomy, registry)
        data, shapes = h.reconstruct_pair({"graphs": registry}, row)
        self.assertFalse(pyshacl.validate(data_graph=data, shacl_graph=shapes, inference="none", meta_shacl=True)[0])
        mutant = h.execute(self.specs["C08-DELETED-UNIT-RULE"], self.module, self.taxonomy, {})
        self.assertEqual((mutant["status"], mutant["observed"]), ("PASS", "COMPATIBLE_FOR_DECLARED_TASK"))

    def test_mixed_incomplete_and_known_mismatch_is_never_accepted(self):
        violations = h.findings("UnitMatch") + h.findings("IndicatorSource", "MinCountConstraintComponent")
        self.assertEqual(h.decide(violations, "dual-anchor-metadata"), "INCOMPATIBLE")
        violations += h.findings("IndicatorUnit", "MaxCountConstraintComponent")
        self.assertEqual(h.decide(violations, "dual-anchor-metadata"), "INVALID")

    def test_integration_metadata_does_not_repair_missing_domain_types(self):
        spec = self.specs["C08-INTEGRATED-UNTYPED-THRESHOLD"]
        registry = {}; row = h.execute(spec, self.module, self.taxonomy, registry)
        self.assertEqual((row["status"], row["observed"]), ("PASS", "INVALID"))
        data, shapes = h.reconstruct_pair({"graphs": registry}, row)
        self.assertNotIn((h.EX.threshold, RDF.type, b.RISK["RKM-C070"]), data)


if __name__ == "__main__": unittest.main()
