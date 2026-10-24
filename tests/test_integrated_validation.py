"""Exercise shared-graph trust boundaries and cross-module failure sensitivity."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
try:
    import pyshacl
except ImportError:
    pyshacl = None
if pyshacl:
    from rdflib import BNode, Graph, Literal, OWL, RDF, URIRef
    import validate_integrated as v
    import run_integrated_validation as run


@unittest.skipUnless(pyshacl, 'Install tools/requirements-shacl.txt')
class IntegrationRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cohort = json.loads((run.OUT / 'cases.json').read_text())
        cls.cases = {c['id']: c for c in cls.cohort['cases']}

    def execute(self, name):
        return run.execute(self.cases[name], self.cohort, {})

    def test_two_separately_valid_version_selections_cannot_pass_the_joint_task(self):
        row = self.execute('MODULES-SEPARATELY-VALID-BUT-DIFFERENT-VERSION')
        self.assertEqual((row['status'], row['decision']), ('PASS', 'NOT_ADMISSIBLE_FOR_SCOPED_TASK'))
        self.assertEqual(row['findings'][0][0], str(v.IS.SharedThresholdScaleVersion))
        control = self.execute('MUTANT-DELETE-JOINT-VERSION-CHECK')
        self.assertEqual((control['status'], control['decision']), ('PASS', 'SCOPED_TASK_ADMISSIBLE'))

    def test_catalog_acceptance_and_staging_never_become_task_admission(self):
        for name in ('CATALOG-ACCEPTS-MISSING-TASK-UNIT', 'RAW-INCOMPLETE-PRESERVED'):
            row = self.execute(name)
            self.assertEqual(row['status'], 'PASS')
            self.assertFalse(row['task_admissible'])
        self.assertEqual(self.execute('MISSING-UNIT')['decision'], 'NOT_ADMISSIBLE_FOR_SCOPED_TASK')

    def test_catalog_metadata_does_not_heal_a_missing_native_type(self):
        row = self.execute('MISSING-NATIVE-INDICATOR-TYPE')
        self.assertEqual(row['status'], 'PASS')
        self.assertEqual(len(row['findings']), 3)
        self.assertTrue(all('ClassConstraintComponent' in x[1] for x in row['findings']))

    def test_alias_normalization_is_shared_by_metadata_native_joins_and_external_focus(self):
        row = self.execute('VERSION-ALIAS-NORMALIZES-ALL-MODULES')
        self.assertEqual((row['status'], row['decision']), ('PASS', 'SCOPED_TASK_ADMISSIBLE'))
        self.assertTrue(row['identity_map'])
        graph, requests = run.fixture(self.cases['JOINT-VALID'], self.cohort)
        original = requests['comparison'][2]
        alias = 'urn:riskium:external-focus-alias'
        graph.add((URIRef(alias), OWL.sameAs, URIRef(original)))
        requests['comparison'][2] = alias
        result = v.validate_graph(graph, requests)
        self.assertEqual(result['decision'], 'SCOPED_TASK_ADMISSIBLE')

    def test_aliases_of_every_module_vocabulary_are_rejected_before_engine(self):
        graph, requests = run.fixture(self.cases['JOINT-VALID'], self.cohort)
        for version in range(1, 8):
            bad = Graph()
            for triple in graph:
                bad.add(triple)
            bad.add((URIRef(v.PROJECT + f'shapes/0.{version}.0#Rule'), OWL.sameAs, URIRef('urn:replacement')))
            result = v.validate_graph(bad, requests)
            self.assertEqual(result['decision'], 'PROFILE_REJECTED')
            self.assertFalse(result['engine_executed'])

    def test_in_band_selectors_schema_and_shape_switches_cannot_hide_data(self):
        for name in ('IN-BAND-COMPARISON-SELECTOR', 'IN-BAND-INTEGRATION-SELECTOR',
                     'SCHEMA-INJECTION', 'IN-BAND-SHAPE-SWITCH', 'UNTARGETED-NATIVE-PARTICIPANT'):
            row = self.execute(name)
            self.assertEqual((row['status'], row['decision'], row['engine_executed']), ('PASS', 'PROFILE_REJECTED', False))

    def test_blank_node_labels_are_scoped_when_modules_are_merged(self):
        first, second, merged = Graph(), Graph(), Graph()
        first.add((BNode('shared'), v.SH.path, URIRef('urn:first')))
        second.add((BNode('shared'), v.SH.path, URIRef('urn:second')))
        v.merge(merged, first, 'first')
        v.merge(merged, second, 'second')
        self.assertEqual(len(set(merged.subjects())), 2)
        self.assertEqual(len(merged), 2)

    def test_compilation_never_mutates_callers_graph_or_request(self):
        graph, requests = run.fixture(self.cases['JOINT-VALID'], self.cohort)
        before = set(graph)
        request_before = json.dumps(requests, sort_keys=True)
        data, shapes, aliases = v.compile_graph(graph, requests, 'scoped-comparison')
        self.assertEqual(set(graph), before)
        self.assertEqual(json.dumps(requests, sort_keys=True), request_before)
        self.assertGreater(len(data), len(graph))
        self.assertGreater(len(shapes), 0)

    def test_wrong_shape_oracle_fails_even_when_decision_matches(self):
        case = dict(self.cases['MISSING-UNIT'], expected_findings=[])
        row = run.execute(case, self.cohort, {})
        self.assertEqual(row['decision'], 'NOT_ADMISSIBLE_FOR_SCOPED_TASK')
        self.assertEqual(row['status'], 'FAIL')

    def test_engine_crash_propagates_and_cannot_be_reported_as_domain_rejection(self):
        graph, requests = run.fixture(self.cases['JOINT-VALID'], self.cohort)
        with patch.object(v, 'validate', side_effect=RuntimeError('engine unavailable')):
            with self.assertRaisesRegex(RuntimeError, 'engine unavailable'):
                v.validate_graph(graph, requests)


if __name__ == '__main__':
    unittest.main()
