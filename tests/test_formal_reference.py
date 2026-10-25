"""Evidence integrity and reader-route oracles for the formal explanation."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('formal_reference',ROOT/'tools/build_formal_reference.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class FormalReference(unittest.TestCase):
    def test_every_clause_preserves_engine_rows_and_readable_route(self):
        outputs=module.build()
        register=json.loads(outputs['evaluation/formal-reference/register.json'])
        self.assertEqual(register['scientific_executions'],0)
        expected={f'C-{i:02d}' for i in range(1,26)}
        self.assertEqual({r['id'] for r in register['constraints']},expected)
        self.assertEqual(sum(r['hermit']['outcome']=='NOT_RUN' for r in register['constraints']),14)
        self.assertEqual(sum(r['shacl']['outcome']=='NOT_RUN' for r in register['constraints']),17)
        self.assertEqual([r['id'] for r in register['constraints'] if r['shacl']['outcome']=='PARTIAL'],['C-08'])
        self.assertEqual(register['summary']['sql_selected_subclauses'],11)
        page=BeautifulSoup((ROOT/'docs/current/guide/Formalization.html').read_text(),'html.parser')
        for ident in expected:
            self.assertIsNotNone(page.find(id=ident))
        fixture=page.select('main details')[7]
        self.assertIn('H-C08-ANCHOR-UNION',fixture.get_text())
        self.assertTrue(fixture.select('a[href]'))
        self.assertNotIn('**HermiT cases:**',fixture.get_text())
        for path, prefix in [('reference/native/index.html','../../guide/'),('reference/search.html','../guide/')]:
            source=BeautifulSoup((ROOT/'docs/current'/path).read_text(),'html.parser')
            for ident in expected:
                self.assertIn(prefix+'Formalization.html#'+ident,[a['href']for a in source.find(id=ident).select('a[href]')])

    def test_missing_acceptance_cannot_silently_drop_clause(self):
        original=module.read
        def changed(path):
            data=original(path)
            if path=='evaluation/owner-review/accepted-scope.json':data['constraints'].pop()
            return data
        with patch.object(module,'read',changed):
            with self.assertRaisesRegex(ValueError,'Missing'):module.build()

    def test_stale_engine_source_binding_is_rejected(self):
        original=module.sha
        with patch.object(module,'sha',lambda p:'0'*64 if p=='ontology/derived/riskium.owl.ttl' else original(p)):
            with self.assertRaisesRegex(ValueError,'Engine receipt'):module.build()

if __name__=='__main__':unittest.main()
