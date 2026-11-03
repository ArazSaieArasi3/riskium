"""Check that the publication projection preserves authored meanings and routes."""
import json,sys,unittest,io,tempfile
from unittest.mock import patch
from urllib.error import HTTPError
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
    def test_live_audit_distinguishes_build_marker_from_real_resource(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);site=root/'site';site.mkdir();(site/'current').mkdir();wiki=root/'wiki';wiki.mkdir()
            files={'index.html':b'<html lang="en"><head><meta name="viewport" content="width=device-width"></head><body>Fixture</body></html>',
                   'current/published-status.json':b'{"wiki_files_sha256":{}}','.nojekyll':b''}
            manifest={'current_source_commit':'fixture','releases':{},'files_sha256':{n:reader.sha(b) for n,b in files.items()}}
            files['publication-manifest.json']=json.dumps(manifest).encode()
            for n,b in files.items():(site/n).write_bytes(b)
            calls=[];corrupt=False
            def get(request,timeout):
                name=request.full_url.removeprefix(reader.SITE+'/');calls.append(name)
                if name=='.nojekyll':raise HTTPError(request.full_url,404,'Unserved build marker',{},None)
                return io.BytesIO(b'corrupt' if corrupt and name=='index.html' else files[name])
            with patch.object(reader,'urlopen',get):
                result=reader.verify_live(site,wiki,root/'receipt.json')
                self.assertEqual(result['served_files'],3)
                self.assertNotIn('.nojekyll',calls)
                corrupt=True
                with self.assertRaisesRegex(ValueError,'Served byte mismatch: index.html'):
                    reader.verify_live(site,wiki,root/'receipt.json')
    def test_every_wiki_concept_link_has_a_projection(self):
        pages={p.stem for p in (ROOT/'build/wiki').glob('*.md')}
        for p in (ROOT/'build/wiki').glob('*.md'):
            for url in reader.re.findall(r'\]\(([^)]+)\)',p.read_text()):
                if reader.urlsplit(url).scheme or url.startswith('#'):continue
                self.assertIn(url.split('#')[0],pages,(p.name,url))
if __name__=='__main__':unittest.main()
