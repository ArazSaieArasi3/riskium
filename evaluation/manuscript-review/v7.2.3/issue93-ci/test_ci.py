"""Guard staging fidelity, route validation and the narrow workflow boundary."""
from pathlib import Path
import importlib.util,json,tempfile,unittest
from unittest.mock import patch
import build_projection as p
ROOT=Path(__file__).resolve().parents[4]
spec=importlib.util.spec_from_file_location('source_transition_ci',ROOT/'tools/check_source_transition.py');transition=importlib.util.module_from_spec(spec);spec.loader.exec_module(transition)
class CandidateCI(unittest.TestCase):
 def test_workflow_is_explicitly_allowed(self):self.assertEqual(transition.classify('.github/workflows/issue93-candidate.yml',None,b'test'),'ADDITIVE_MANUSCRIPT_OR_READER')
 def test_arbitrary_workflow_is_not_allowed(self):
  with self.assertRaises(ValueError):transition.classify('.github/workflows/undeclared.yml',None,b'test')
 def test_research_source_change_still_rejected(self):
  with self.assertRaises(ValueError):transition.classify('ontology/riskium-model.json','old',b'changed')
 def test_routes_are_deterministic(self):
  self.assertEqual(p.route('README.md'),'index.html');self.assertEqual(p.route('RKM-C075.md'),'RKM-C075.html');self.assertEqual(p.slug('README.md'),'Issue93-Candidate-Home')
 def fixture(self,d):
  (d/'site').mkdir();(d/'wiki').mkdir();h=d/'site/index.html';h.write_text('<html lang="en"><head><meta name="viewport"></head><body><h1 id="ok">Test</h1><a href="#ok">Self</a></body></html>')
  w=d/'wiki/Home.md';w.write_text('[Home](Home)');m={'files_sha256':{'site/index.html':p.sha(h),'wiki/Home.md':p.sha(w)},'html_pages':1,'wiki_pages':1};(d/'publication-manifest.json').write_text(p.dump(m));return h,w,m
 def test_audit_accepts_valid_self_link(self):
  with tempfile.TemporaryDirectory() as tmp:self.assertEqual(self.valid(tmp),2)
 def valid(self,tmp):
  d=Path(tmp);self.fixture(d);return p.audit(d)['local_link_occurrences']
 def test_audit_rejects_hash_change(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp);h,w,m=self.fixture(d);h.write_text('changed')
   with self.assertRaises(ValueError):p.audit(d)
 def test_audit_rejects_missing_html_anchor(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp);h,w,m=self.fixture(d);h.write_text(h.read_text().replace('href="#ok"','href="#missing"'));m['files_sha256']['site/index.html']=p.sha(h);(d/'publication-manifest.json').write_text(p.dump(m))
   with self.assertRaises(ValueError):p.audit(d)
 def test_audit_rejects_missing_wiki_route(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp);h,w,m=self.fixture(d);w.write_text('[Missing](Absent)');m['files_sha256']['wiki/Home.md']=p.sha(w);(d/'publication-manifest.json').write_text(p.dump(m))
   with self.assertRaises(ValueError):p.audit(d)
if __name__=='__main__':unittest.main()
