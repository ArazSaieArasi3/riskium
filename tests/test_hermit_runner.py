"""Catch ignored OWLAPI conclusion axioms in source-bound HermiT fixtures."""
import json
import sys
import unittest
from pathlib import Path

from rdflib import BNode, Graph, RDF, OWL, RDFS

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import run_hermit as h


class HermitFixtureRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.full = Graph().parse(h.OWL_TTL, format="turtle")
        cls.model = json.loads(h.MODEL.read_text())

    def test_conclusions_declare_owl_terms_and_individuals(self):
        all_specs = h.scenario_specs(self.full, self.model) + h.consequence_specs(self.full, self.model)
        for spec in all_specs:
            c = spec.get("conclusion")
            if c is None:
                continue
            for subject, _, cls in c.triples((None, RDF.type, None)):
                if cls in (OWL.Class, OWL.ObjectProperty, OWL.NamedIndividual, OWL.Restriction):
                    continue
                self.assertIn((subject, RDF.type, OWL.NamedIndividual), c, spec["id"])
                if isinstance(cls, BNode):
                    self.assertIn((cls, RDF.type, OWL.Restriction), c, spec["id"])
                else:
                    self.assertIn((cls, RDF.type, OWL.Class), c, spec["id"])
            for subject, pred, obj in c:
                if str(pred).startswith(str(h.RISK)):
                    self.assertIn((pred, RDF.type, OWL.ObjectProperty), c, spec["id"])
                    self.assertIn((subject, RDF.type, OWL.NamedIndividual), c, spec["id"])
                    self.assertIn((obj, RDF.type, OWL.NamedIndividual), c, spec["id"])

    def test_context_inclusion_is_one_way(self):
        specs = {s["id"]: s for s in h.scenario_specs(self.full, self.model)}
        positive = specs["H-C23-ANALYZED-IMPLIES-CONTEXT"]["conclusion"]
        negative = specs["H-C23-NO-REVERSE-CONTEXT"]["conclusion"]
        self.assertIn((h.RISK["RX-001"], RDF.type, OWL.ObjectProperty), positive)
        self.assertIn((h.RISK["R-35"], RDF.type, OWL.ObjectProperty), negative)
        self.assertIn((h.RISK["R-35"], RDFS.subPropertyOf, h.RISK["RX-001"]), self.full)
        self.assertNotIn((h.RISK["RX-001"], RDFS.subPropertyOf, h.RISK["R-35"]), self.full)


if __name__ == "__main__":
    unittest.main()
