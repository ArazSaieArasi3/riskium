"""Verify identity policy and the sensitivity of the scoped shape oracles."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
try:
    import pyshacl
except ImportError:
    pyshacl = None
if pyshacl:
    import run_shacl as s
    import build_shacl
    from rdflib import Graph, RDF, OWL
    from rdflib.compare import isomorphic


@unittest.skipUnless(pyshacl,"Install tools/requirements-shacl.txt for SHACL regressions")
class ShaclRegression(unittest.TestCase):
    def test_committed_profiles_match_builder_and_receipt(self):
        receipt=json.loads((s.PROFILE_DIR/"receipt.json").read_text())
        for name,expected in build_shacl.profiles().items():
            path=s.PROFILE_DIR/(name+".ttl")
            self.assertTrue(isomorphic(expected,Graph().parse(path,format="turtle")),name)
            self.assertEqual(s.digest(path.read_bytes()),receipt["profiles_sha256"][name])

    def test_identity_normalization_is_idempotent_and_symmetric(self):
        g=Graph();a,b,c=s.EX.a,s.EX.b,s.EX.c
        g.add((a,OWL.sameAs,b));g.add((b,RDF.type,s.RISK["RKM-C053"]))
        g.add((b,OWL.differentFrom,c))
        first,_=s.normalize_identity(g);second,_=s.normalize_identity(first)
        self.assertEqual(set(first),set(second))
        self.assertIn((a,RDF.type,s.RISK["RKM-C053"]),first)
        self.assertIn((c,OWL.differentFrom,a),first)

    def test_alias_conflict_rejects_managed_and_preserves_raw(self):
        specs={r["id"]:r for r in s.fixture_specs()}
        managed=s.execute(specs["S-C06-IDENTITY-CONFLICT"],Graph())
        raw=s.execute(specs["S-C06-RAW-IDENTITY-CONFLICT"],Graph())
        self.assertEqual(managed["observed"],"IDENTITY_CONFLICT")
        self.assertFalse(managed["engine_executed"])
        self.assertEqual(raw["observed"],"CONFORMS")
        self.assertTrue(raw["engine_executed"])

    def test_anchor_and_publication_mutations_change_admission(self):
        specs={r["id"]:r for r in s.fixture_specs()}
        for negative,mutant in (("S-C08-NO-ANCHOR","S-C08-DELETED-ANCHOR-RULE"),
                                ("S-C09-PUBLISHED-NO-TARGET","S-C09-DELETED-MINIMUM")):
            self.assertEqual(s.execute(specs[negative],Graph())["observed"],"VIOLATES")
            self.assertEqual(s.execute(specs[mutant],Graph())["observed"],"CONFORMS")

    def test_component_oracle_cannot_be_replaced_by_another_failure(self):
        spec=next(r for r in s.fixture_specs() if r["id"]=="S-C08-TWO-INDICATORS")
        spec=dict(spec,expected_components={"C08Indicator":"ClassConstraintComponent"})
        self.assertEqual(s.execute(spec,Graph())["status"],"FAIL")

    def test_compatibility_is_blocked_and_not_engine_pass(self):
        spec=next(r for r in s.fixture_specs() if r["id"]=="S-C08-TASK-DUAL-UNKNOWN")
        result=s.execute(spec,Graph())
        self.assertEqual(result["status"],"BLOCKED")
        self.assertFalse(result["engine_executed"])

if __name__=="__main__":unittest.main()
