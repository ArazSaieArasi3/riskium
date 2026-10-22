"""Regression checks for mapping fidelity and RDF syntax, not a reasoner suite."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD, URIRef

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_owl


class OwlMappingRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output, cls.receipt = build_owl.render()
        cls.graph = Graph().parse(data=cls.output, format="turtle")
        cls.risk = Namespace(build_owl.BASE)
        cls.model = json.loads(build_owl.SOURCE.read_text())

    def test_export_is_parseable_complete_and_pinned(self):
        self.assertEqual(self.output, build_owl.OUTPUT.read_text())
        self.assertEqual(self.receipt, json.loads(build_owl.RECEIPT.read_text()))
        self.assertEqual({"typed_classes": 77, "local_anchor_proxy": 1,
                          "generalizations": 66, "typed_object_properties": 127,
                          "cardinality_restrictions": 88, "reviewed_property_inclusions": 2,
                          "reviewed_property_disjointness": 1,
                          "conditional_anchor_unions": 1,
                          "qualified_version_target_rules": 4,
                          "reviewed_generalization_sets": 10,
                          "disjoint_sets": 3, "optional_boundaries_as_classes": 0},
                         self.receipt["coverage"])
        self.assertEqual(len({x for x in self.graph.subjects(RDF.type, OWL.Class) if isinstance(x, URIRef)}), 78)
        self.assertEqual(len(set(self.graph.subjects(RDF.type, OWL.ObjectProperty))), 127)
        for p, digest in self.receipt["inputs_sha256"].items():
            self.assertEqual(digest, build_owl.digest(ROOT / p))

    def test_all_source_subclasses_and_relation_typing_survive(self):
        for g in self.model["generalizations"]:
            self.assertIn((self.risk[g["specific"]], RDFS.subClassOf, self.risk[g["general"]]), self.graph)
        for r in self.model["associations"]:
            if r["scope_layer"] != "FORMAL_CORE":
                continue
            prop = self.risk[r["id"]]
            self.assertIn((prop, RDFS.domain, self.risk[r["source"]]), self.graph)
            self.assertIn((prop, RDFS.range, self.risk[r["target"]]), self.graph)

    def test_cardinality_direction_and_open_world_structure(self):
        relation = next(r for r in self.model["associations"] if r["id"] == "R-01")
        self.assertEqual((relation["source_end_cardinality"], relation["target_end_cardinality"]), ("0..*", "1"))
        source = self.risk[relation["source"]]
        target = self.risk[relation["target"]]
        restrictions = list(self.graph.objects(source, RDFS.subClassOf))
        matching = [b for b in restrictions if (b, OWL.onProperty, self.risk["R-01"]) in self.graph]
        self.assertEqual(len(matching), 1)
        self.assertIn((matching[0], OWL.onClass, target), self.graph)
        self.assertIn((matching[0], OWL.qualifiedCardinality, Literal(1, datatype=XSD.nonNegativeInteger)), self.graph)
        # The opposite 0..* end creates no inverse restriction.
        self.assertFalse(any(self.graph.value(b, OWL.inverseOf) == self.risk["R-01"]
                             for restriction in self.graph.objects(target, RDFS.subClassOf)
                             for b in self.graph.objects(restriction, OWL.onProperty)))

    def test_only_reviewed_disjointness_without_covering_or_import(self):
        sets = list(self.graph.subjects(RDF.type, OWL.AllDisjointClasses))
        self.assertEqual(len(sets), 3)
        self.assertEqual(len(list(self.graph.triples((None, OWL.unionOf, None)))), 1)
        self.assertEqual(list(self.graph.triples((None, OWL.imports, None))), [])
        for c in self.model["concepts"]:
            if c["scope_layer"] == "OPTIONAL_PHENOMENON_BOUNDARY":
                self.assertNotIn((self.risk[c["id"]], RDF.type, OWL.Class), self.graph)

    def test_only_source_backed_property_inclusions(self):
        expected = {(self.risk["R-35"], RDFS.subPropertyOf, self.risk["RX-001"]),
                    (self.risk["R-33"], RDFS.subPropertyOf, self.risk["RX-006"])}
        self.assertEqual(set(self.graph.triples((None, RDFS.subPropertyOf, None))), expected)

    def test_constraint_axioms_have_reviewed_scope(self):
        self.assertIn((self.risk["R-56"], OWL.propertyDisjointWith, self.risk["R-57"]), self.graph)
        union = list(self.graph.subjects(OWL.unionOf, None))
        self.assertEqual(len(union), 1)
        self.assertIn((self.risk["RKM-C070"], RDFS.subClassOf, union[0]), self.graph)
        # Publication is a separate profile: no unconditional RiskDescription aboutness union.
        self.assertFalse(any(self.graph.value(x, OWL.unionOf) is not None
                             for x in self.graph.objects(self.risk["RKM-C024"], RDFS.subClassOf)))
        for prop, artifact in build_owl.VERSION_TARGETS:
            source = next(r["source"] for r in self.model["associations"] if r["id"] == prop)
            matches = [x for x in self.graph.objects(self.risk[source], RDFS.subClassOf)
                       if (x, OWL.onProperty, self.risk[prop]) in self.graph and
                       self.graph.value(x, OWL.allValuesFrom) is not None]
            self.assertEqual(len(matches), 1, prop)
            inner = self.graph.value(matches[0], OWL.allValuesFrom)
            self.assertIn((inner, OWL.onProperty, self.risk["RX-006"]), self.graph)
            self.assertIn((inner, OWL.someValuesFrom, self.risk[artifact]), self.graph)

    def test_native_end_mutation_is_rejected(self):
        native = json.loads(build_owl.NATIVE.read_text())
        mutant = copy.deepcopy(native)
        end = next(e for e in mutant["elements"] if e["id"] == "R-01:target")
        end["cardinality"] = "0..*"
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "mutant.json"
            path.write_text(json.dumps(mutant))
            with patch.object(build_owl, "NATIVE", path):
                with self.assertRaisesRegex(ValueError, "Native relation end mismatch"):
                    build_owl.render()


if __name__ == "__main__":
    unittest.main()
