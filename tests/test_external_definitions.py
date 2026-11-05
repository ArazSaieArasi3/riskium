"""Reject the scientific misclaims this documentary projection must prevent."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build_external_definitions as review


class ExternalDefinitions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data, cls.model = review.validate()

    def test_missing_or_duplicate_concept_cannot_count_as_complete(self):
        for rows in [self.data['concepts'][:-1], self.data['concepts'][:-1] + [self.data['concepts'][0]]]:
            data = deepcopy(self.data); data['concepts'] = rows
            with self.assertRaisesRegex(ValueError, 'Lost or duplicated'):
                review.validate(data)

    def test_unread_normative_source_cannot_supply_a_definition(self):
        data = deepcopy(self.data); data['terms']['invented'] = dict(source_id='iso', locator='invented clause', paraphrase='unsupported', url=data['sources']['iso']['url']+'#invented', quotation=False)
        with self.assertRaisesRegex(ValueError, 'unread source'):
            review.validate(data)

    def test_review_cannot_silently_change_meaning_or_award_independent_acceptance(self):
        for field,value in [('authored_definition_sha256','0'*64),('formal_alignment','VERIFIED_EQUIVALENCE'),('independent_validation','PASS')]:
            data = deepcopy(self.data);data['concepts'][0][field] = value
            with self.assertRaises(ValueError):
                review.validate(data)

    def test_generated_dossier_preserves_both_sides_of_external_section(self):
        old = review.original.build(); new = review.build()
        for c in self.model['concepts']:
            name=c['id']+'.md';prefix=old[name].split('## External definition and alignment status')[0];suffix=old[name].split('## Evidence and limits')[1]
            self.assertTrue(new[name].startswith(prefix))
            self.assertTrue(new[name].endswith('## Evidence and limits'+suffix))

    def test_published_html_has_the_actual_reviewed_decision_and_correct_source(self):
        rows={r['concept_id']:r for r in self.data['concepts']}
        for c in self.model['concepts']:
            soup=BeautifulSoup((ROOT/'build/site/current/concepts'/(c['id']+'.html')).read_text(),'html.parser')
            text=soup.get_text(' ',strip=True); row=rows[c['id']]
            self.assertIn(row['rationale'],text)
            self.assertIn(row['disposition'],text)
            self.assertIn('unassessed',text)
            for tid in row['term_ids']:
                self.assertIsNotNone(soup.find('a',href=self.data['terms'][tid]['url']))
            self.assertIsNotNone(soup.find('a',href='https://github.com/ArazSaieArasi3/riskium/wiki/'+c['id']))


if __name__ == '__main__':
    unittest.main()
