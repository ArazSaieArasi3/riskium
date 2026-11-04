"""Failure boundaries; fixture metadata below is not an actual CI observation."""
import copy,hashlib,importlib.util,io,json,shutil,tarfile,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('r038',ROOT/'tools/releases/v038/release.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
class Release038(unittest.TestCase):
    def test_git_object_identity_and_path_conflict(self):
        self.assertEqual(r.object_id(b'blob',b'hello\n'),'ce013625030ba8dba906f756967f9e9ca394464a')
        with self.assertRaisesRegex(ValueError,'Conflicting'):r.tree_id({'a':b'file','a/b':b'child'},{'a':0o644,'a/b':0o644})
        payload={};modes={}
        for item in r.git('ls-tree','-rz','HEAD').split(b'\0'):
            if not item:continue
            meta,path=item.split(b'\t',1);mode,kind,ident=meta.split();self.assertEqual(kind,b'blob');name=path.decode();payload[name]=r.git('cat-file','blob',ident.decode());modes[name]=int(mode,8)&0o777
        self.assertEqual(r.tree_id(payload,modes),r.git('rev-parse','HEAD^{tree}').decode().strip())
    def packet(self,root):
        r.write_assets(root,'a'*40,[(r.NOTES,0o644,b'Unit fixture: not a release')],{},{});return root
    def checksums(self,p):
        (p/'SHA256SUMS.txt').write_text(''.join(r.sha((p/n).read_bytes())+'  '+n+'\n' for n in sorted(r.ASSETS-{'SHA256SUMS.txt'})))
    def test_selected_closure_and_original_bodies(self):
        m=r.selection();self.assertEqual(m['summary']['components'],32);self.assertEqual(m['summary']['preserved_predecessor_bodies'],904);self.assertEqual(m['scientific_versions']['model'],'0.3.1');self.assertFalse(m['article_binaries_included'])
        for p,h in r.load(r.PRIOR)['selected_files_sha256'].items():self.assertEqual(r.sha(r.read(m['historical_delivery_aliases'].get(p,p))),h)
    def test_dependency_cycle_and_version_mismatch_are_rejected(self):
        with self.assertRaisesRegex(ValueError,'cycle'):r.ordered({'a':'1'},{'a':[{'id':'a','version':'1'}]})
        with self.assertRaisesRegex(ValueError,'Unresolved'):r.ordered({'a':'1'},{'a':[{'id':'a','version':'2'}]})
    def test_wrong_external_source_and_payload_corruption_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.packet(Path(d))
            with self.assertRaisesRegex(ValueError,'source/phase'):r.verify(p,'b'*40)
            with (p/'release-notes.md').open('ab') as f:f.write(b'corrupt')
            with self.assertRaisesRegex(ValueError,'checksum differs'):r.verify(p,'a'*40)
    def test_traversal_and_symlink_are_rejected_even_with_updated_checksums(self):
        for traversal in (True,False):
            with self.subTest(traversal=traversal),tempfile.TemporaryDirectory() as d:
                p=self.packet(Path(d))
                with tarfile.open(p/'riskium-v0.3.8-source.tar.gz','w:gz') as t:
                    i=tarfile.TarInfo('v0.3.8/../escape' if traversal else 'v0.3.8/link')
                    if not traversal:i.type=tarfile.SYMTYPE;i.linkname='../escape'
                    t.addfile(i,io.BytesIO(b''))
                self.checksums(p)
                with self.assertRaisesRegex(ValueError,'Unsafe'):r.verify(p,'a'*40)
                self.assertFalse((p.parent/'escape').exists())
    def test_missing_and_wrong_source_ci_are_rejected(self):
        with self.assertRaisesRegex(ValueError,'Incomplete'):r.evidence_check({'required_runs':[]},'a'*40,ROOT)
        runs=[dict(path=p,head_sha='b'*40,head_branch='main',event='push',status='completed',conclusion='success',repository={'full_name':r.REPO},head_repository={'full_name':r.REPO}) for p in r.load(r.POLICY)['required_ci_paths']]
        with self.assertRaisesRegex(ValueError,'Unqualified'):r.evidence_check({'required_runs':runs},'a'*40,ROOT)
    def test_inherited_model_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'repo';shutil.copytree(ROOT,dest,ignore=shutil.ignore_patterns('.git','build','__pycache__'))
            with (dest/'ontology/riskium-model.json').open('ab') as f:f.write(b' ')
            with self.assertRaisesRegex(ValueError,'Binding changed'):r.selection(dest)
if __name__=='__main__':unittest.main()
