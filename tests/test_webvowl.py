"""OWL projection oracles and fixed-source runtime boundaries, not semantic review."""
from pathlib import Path
import json
import sys
import unittest
import tempfile
from unittest.mock import patch
from rdflib import Graph, RDF, RDFS, OWL, URIRef

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/publication'))
import build_webvowl as wv
from bs4 import BeautifulSoup


class WebVOWL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(ROOT/wv.SOURCE).read_bytes()
        cls.data,cls.coverage=wv.project(cls.source)

    def test_all_declared_nodes_properties_and_named_subclasses_match_source(self):
        g=Graph().parse(data=self.source.decode(),format='turtle')
        ids=lambda nodes:{str(n).removeprefix(wv.BASE) for n in nodes if isinstance(n,URIRef)}
        self.assertEqual({r['id'] for r in self.data['class']},ids(g.subjects(RDF.type,OWL.Class)))
        attrs={r['iri']:r for r in self.data['propertyAttribute'] if 'iri'in r}
        self.assertEqual(set(attrs),set(map(str,g.subjects(RDF.type,OWL.ObjectProperty))))
        for iri,row in attrs.items():
            self.assertEqual({row['domain']},ids(g.objects(URIRef(iri),RDFS.domain)))
            self.assertEqual({row['range']},ids(g.objects(URIRef(iri),RDFS.range)))
        declared={(str(a).removeprefix(wv.BASE),str(b).removeprefix(wv.BASE)) for a,b in g.subject_objects(RDFS.subClassOf) if isinstance(a,URIRef)and isinstance(b,URIRef)}
        actual={(r['domain'],r['range'])for r in self.data['propertyAttribute']if r['id'].startswith('subclass-')}
        self.assertEqual(actual,declared)
        self.assertEqual((len(self.data['class']),len(attrs),len(actual)),(78,127,66))

    def test_missing_endpoint_never_becomes_an_invented_edge(self):
        g=Graph().parse(data=self.source.decode(),format='turtle');prop=next(g.subjects(RDF.type,OWL.ObjectProperty))
        g.remove((prop,RDFS.domain,None));data,report=wv.project(g.serialize(format='turtle').encode())
        self.assertNotIn(str(prop),{r.get('iri')for r in data['propertyAttribute']})
        self.assertEqual(report['omitted_properties'][0]['iri'],str(prop))
        self.assertEqual(report['rendered_object_properties'],126)

    def test_multiple_endpoints_are_not_arbitrarily_selected(self):
        g=Graph().parse(data=self.source.decode(),format='turtle');prop=next(g.subjects(RDF.type,OWL.ObjectProperty))
        g.add((prop,RDFS.range,OWL.Thing));data,report=wv.project(g.serialize(format='turtle').encode())
        self.assertNotIn(str(prop),{r.get('iri')for r in data['propertyAttribute']})
        self.assertEqual(len(report['omitted_properties']),1)

    def test_canonical_omission_accounting_is_complete_and_repeatable(self):
        g=Graph().parse(data=self.source.decode(),format='turtle')
        data,report=wv.project(g.serialize(format='turtle').encode())
        self.assertEqual(self.coverage['omission_inventory'],report['omission_inventory'])
        self.assertEqual(report['source_triples'],report['represented_source_triples']+report['omitted_source_triples'])
        self.assertEqual(report['source_triples'],2087)
        self.assertTrue(any('disjointness' in r['reason'].lower() for r in report['omission_inventory']))
        self.assertGreater(report['anonymous_terms'],0)

    def test_empty_source_is_rejected(self):
        with self.assertRaises(ValueError):wv.project(b'')

    def test_shell_has_no_upload_editor_or_external_active_resources(self):
        soup=BeautifulSoup((wv.HERE/'index.html').read_text(),'html.parser')
        self.assertFalse(soup.select('form,input[type=file],object,embed,iframe'))
        self.assertEqual([n['src']for n in soup.select('script')],['vendor/d3.min.js','vendor/webvowl.js','viewer.js'])
        self.assertIn("connect-src 'self'",soup.select_one('meta[http-equiv="Content-Security-Policy"]')['content'])
        js=(wv.HERE/'viewer.js').read_text()
        self.assertIn('fetch("data/riskium.json"',js)
        for word in ['localStorage','sessionStorage','sendBeacon','XMLHttpRequest','location.hash','location.search']:
            self.assertNotIn(word,js)
        for node in soup.find_all(True):self.assertFalse(any(k.startswith('on')for k in node.attrs))

    def test_source_and_runtime_byte_checks_pass(self):
        self.assertEqual(wv.audit(ROOT/'docs')['status'],'WEBVOWL_PROJECTION_RUNTIME_PASS')

    def test_changed_shell_assets_get_new_cache_identity(self):
        initial=BeautifulSoup(wv.shell_html(),'html.parser')
        with tempfile.TemporaryDirectory()as folder:
            root=Path(folder)
            for name in ['index.html','viewer.js','viewer.css']:(root/name).write_bytes((wv.HERE/name).read_bytes())
            (root/'viewer.js').write_text((root/'viewer.js').read_text()+'\n/* changed version */\n')
            with patch.object(wv,'HERE',root):changed=BeautifulSoup(wv.shell_html(),'html.parser')
        self.assertNotEqual(initial.select('script')[-1]['src'],changed.select('script')[-1]['src'])
        self.assertEqual(initial.select('script')[0]['src'],changed.select('script')[0]['src'])


if __name__=='__main__':unittest.main()
