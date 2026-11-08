"""Contract failure controls and independent output comparisons for B0-4."""
import copy
import json
import unittest
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL
from rdflib.compare import isomorphic
import export_candidate as export
import candidate_owl

RISK = Namespace(export.TERM_NS)


def logical(graph):
    """Discard documentary annotations only; retain OWL/RDFS logical axioms."""
    annotations = set(graph.subjects(RDF.type, OWL.AnnotationProperty)) | {RDFS.label, RDFS.comment}
    result = Graph()
    for s, p, o in graph:
        if p in annotations or p == OWL.versionIRI:
            continue
        result.add((s, p, o))
    return result


class CandidateContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(export.CONTRACT.read_text())
        cls.model, cls.policy = export.validate_contract(cls.contract)
        cls.native_text, cls.owl_text, cls.mapping = export.render(cls.contract)
        cls.native = json.loads(cls.native_text)
        cls.graph = Graph().parse(data=cls.owl_text, format='turtle')

    def test_generation_is_byte_deterministic(self):
        self.assertEqual((self.native_text, self.owl_text, self.mapping), export.render(self.contract))

    def test_native_is_identical_to_combined_candidate(self):
        old = export.HERE.parent / 'issue93-generalization-sets/candidate.ontouml.json'
        self.assertEqual(self.native_text, old.read_text())
        sets = {e['id'] for e in self.native['elements'] if e['type'] == 'GeneralizationSet'}
        self.assertEqual(sets, {s['id'] for s in self.policy['retained_sets']})
        self.assertFalse(sets & {'GS-RKM-C014', 'GS-RKM-C047'})
        self.assertEqual(sum(e['type'] == 'Generalization' for e in self.native['elements']), 67)

    def test_owl_logical_axioms_match_previous_candidate(self):
        old = Graph().parse(export.HERE.parent / 'issue93-generalization-sets/candidate.owl.ttl', format='turtle')
        self.assertTrue(isomorphic(logical(old), logical(self.graph)))

    def test_current_class_annotations_come_from_candidate(self):
        for c in self.model['concepts'] + self.model['imported_types']:
            if c['scope_layer'] == 'FORMAL_CORE' or c['id'] == 'EXT-OBJECT':
                self.assertIn((RISK[c['id']], RDFS.comment, Literal(c['definition'])), self.graph)
        self.assertEqual(set(self.graph.objects(URIRef(self.contract['ontology_iri']), OWL.versionIRI)), {URIRef(export.VERSION_IRI)})

    def test_all_source_edges_and_typed_signatures_survive(self):
        for g in self.model['generalizations']:
            self.assertIn((RISK[g['specific']], RDFS.subClassOf, RISK[g['general']]), self.graph)
        for r in self.model['associations']:
            if r['scope_layer'] == 'FORMAL_CORE':
                self.assertIn((RISK[r['id']], RDFS.domain, RISK[r['source']]), self.graph)
                self.assertIn((RISK[r['id']], RDFS.range, RISK[r['target']]), self.graph)
        self.assertIn((RISK['RE-001'], OWL.propertyDisjointWith, RISK['RE-002']), self.graph)
        self.assertEqual(len(list(self.graph.subjects(RDF.type, OWL.AllDisjointClasses))), 3)
        self.assertFalse(list(self.graph.triples((None, OWL.imports, None))))

    def test_wrong_version_is_rejected(self):
        c = copy.deepcopy(self.contract); c['source_version'] = '0.3.1'
        with self.assertRaisesRegex(ValueError, 'source version'): export.render(c)

    def test_wrong_digest_is_rejected(self):
        c = copy.deepcopy(self.contract); c['source']['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'digest'): export.render(c)

    def test_wrong_inventory_is_rejected(self):
        c = copy.deepcopy(self.contract); c['inventory']['concepts'] += 1
        with self.assertRaisesRegex(ValueError, 'Inventory'): export.render(c)

    def test_namespace_change_is_rejected(self):
        for field in ['term_namespace', 'version_iri', 'evidence_namespace', 'ontology_iri']:
            c = copy.deepcopy(self.contract); c[field] += '/different'
            with self.assertRaises(ValueError): export.render(c)

    def test_stale_downstream_binding_is_rejected(self):
        c = copy.deepcopy(self.contract); c['downstream_bindings']['shacl']['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'digest'): export.render(c)
        c = copy.deepcopy(self.contract); c['downstream_bindings']['definitions'].pop()
        with self.assertRaisesRegex(ValueError, 'definition binding'): export.render(c)

    def test_missing_generator_binding_is_rejected(self):
        c = copy.deepcopy(self.contract); c['generator_inputs'].pop()
        with self.assertRaisesRegex(ValueError, 'Generator'): export.render(c)

    def test_promotion_and_path_escape_are_rejected(self):
        c = copy.deepcopy(self.contract); c['production_promotion'] = True
        with self.assertRaisesRegex(ValueError, 'promote'): export.render(c)
        c = copy.deepcopy(self.contract); c['source']['path'] = '../source.json'
        with self.assertRaisesRegex(ValueError, 'escapes'): export.render(c)

    def test_native_relation_mutation_is_rejected(self):
        native = copy.deepcopy(self.native)
        next(e for e in native['elements'] if e['id'] == 'RE-001:target')['cardinality'] = '0..*'
        with self.assertRaisesRegex(ValueError, 'relation end mismatch'):
            candidate_owl.render(self.model, native, self.policy, self.contract, {})

    def test_legacy_native_grouping_is_rejected(self):
        builder = export.load_builder()
        native = builder.build_native.build(self.model, self.contract['source']['sha256'])
        # The candidate renderer must reject a native set surface with extras,
        # rather than silently ignore the historical auto-grouping rule.
        with self.assertRaisesRegex(ValueError, 'Native set inventory'):
            candidate_owl.render(self.model, native, self.policy, self.contract, {})


if __name__ == '__main__':
    unittest.main()
