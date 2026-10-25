"""Reader route and generated-commitment regression oracles for Pages."""
from pathlib import Path
import subprocess
import sys
import unittest
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/publication'))
from audit_presentation import audit
from guides import sync_wiki

class PagesPresentation(unittest.TestCase):
    def test_every_current_page_and_version_index_has_one_reading_contract(self):
        report=audit(ROOT/'docs')
        self.assertEqual(report['status'],'CURRENT_PRESENTATION_PASS')
        self.assertGreaterEqual(report['pages'],31)

    def test_all_widoco_term_and_axiom_text_survives_template_integration(self):
        baseline=subprocess.check_output(['git','show','eb0ff1d64e87c8667aa9f3eab46d700ffc61a7ee:docs/current/widoco/index-en.html'],cwd=ROOT)
        before=BeautifulSoup(baseline,'html.parser')
        after=BeautifulSoup((ROOT/'docs/current/widoco/index-en.html').read_text(),'html.parser')
        expected={n['id']:n.get_text(' ',strip=True)for n in before.select('.entity[id]')}
        for added in after.select('.entity p.term-links'):added.decompose()
        actual={n['id']:n.get_text(' ',strip=True)for n in after.select('.entity[id]')}
        self.assertEqual(len(expected),215)
        self.assertEqual(actual,expected)

    def test_lookup_exposes_real_concept_relation_and_constraint_anchors(self):
        page=BeautifulSoup((ROOT/'docs/current/reference/search.html').read_text(),'html.parser')
        entries=page.select('.entry')
        self.assertEqual(len(entries),240)
        for ident in ['RKM-X01','RX-002','C-08']:
            row=page.find(id=ident)
            self.assertIsNotNone(row)
            self.assertIn('native/index.html#'+ident,[a['href'] for a in row.select('a')])
        constraint=page.find(id='C-08')
        self.assertFalse(any('widoco' in a['href']for a in constraint.select('a')))

    def test_shared_wiki_sources_match_without_claiming_live_publication(self):
        self.assertEqual(sync_wiki(ROOT,check=True),21)
        guide=(ROOT/'docs/guides/Visualization.md').read_text()
        self.assertIn('is deployed',guide)
        self.assertNotIn('not yet implemented',guide)

if __name__=='__main__':unittest.main()
