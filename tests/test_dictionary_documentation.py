"""Check that the publication projection preserves authored meanings and routes."""
import json,sys,unittest
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/publication'))
import dictionary_documentation as reader
class DictionaryPublication(unittest.TestCase):
    def test_every_authored_definition_and_identity_is_present(self):
        model=json.loads((ROOT/'ontology/riskium-model.json').read_text())
        for c in model['concepts']:
            p=ROOT/'build/site/current/concepts'/(c['id']+'.html')
            soup=BeautifulSoup(p.read_text(),'html.parser')
            self.assertIn(c['id'],soup.get_text())
            definition=BeautifulSoup(reader.markdown.markdown(c['definition']),'html.parser').get_text(' ',strip=True)
            self.assertIn(definition,soup.get_text(' ',strip=True))
            self.assertIn('unassessed',soup.get_text().lower())
            self.assertIsNotNone(soup.select_one('a[href$="/wiki/'+c['id']+'"]'))
    def test_all_routes_and_frozen_snapshots_remain_valid(self):
        result=reader.audit(ROOT/'build/site')
        self.assertEqual(result['frozen_snapshots'],4)
        self.assertGreater(result['html_pages'],100)
    def test_external_source_path_cannot_escape_repository(self):
        with self.assertRaises(ValueError):reader.link('../../../../../../etc/passwd','a'*40)
    def test_every_wiki_concept_link_has_a_projection(self):
        pages={p.stem for p in (ROOT/'build/wiki').glob('*.md')}
        for p in (ROOT/'build/wiki').glob('*.md'):
            for url in reader.re.findall(r'\]\(([^)]+)\)',p.read_text()):
                if reader.urlsplit(url).scheme or url.startswith('#'):continue
                self.assertIn(url.split('#')[0],pages,(p.name,url))
if __name__=='__main__':unittest.main()
