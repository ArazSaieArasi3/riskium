"""Real source snapshot plus explicitly synthetic qualification fixtures for package guards."""
from pathlib import Path
from copy import deepcopy
import base64, gzip, hashlib, io, json, shutil, tarfile, tempfile, unittest
import build_package as builder
import verify_package as verifier

class PackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.commit = builder.git('rev-parse', 'HEAD').decode().strip()
        cls.report = json.loads((builder.ROOT / 'evaluation/releases/v0.3.9/R1-qualification.json').read_text())
        selection = json.loads((builder.ROOT / 'releases/selection-v0.3.9.json').read_text())
        cls.report.update(execution_commit=cls.commit, selection_summary=selection['summary'],
                          unit_test_fixture='Synthetic adapter input only; not a new engine or CI receipt.')
        cls.report['selection']['sha256'] = builder.digest((builder.ROOT / 'releases/selection-v0.3.9.json').read_bytes())
        cls.input = builder.encoded(cls.report)
        cls.assets = builder.render(cls.commit, cls.input)
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.out = Path(self.temp.name)
        for name, body in self.assets.items(): (self.out / name).write_bytes(body)
    def tearDown(self): self.temp.cleanup()
    def checksums(self):
        names = sorted(verifier.ASSETS - {'SHA256SUMS.txt'})
        (self.out / 'SHA256SUMS.txt').write_text(''.join(builder.digest((self.out/n).read_bytes())+'  '+n+'\n' for n in names))
    def mutate_json(self, name, edit):
        value = json.loads((self.out/name).read_text()); edit(value); (self.out/name).write_bytes(builder.encoded(value)); self.checksums()
    def reject(self, text):
        with self.assertRaisesRegex(ValueError, text): verifier.verify(self.out, self.commit)
    def archive_member(self, name, symlink=False):
        old = tarfile.open(fileobj=io.BytesIO((self.out/'riskium-v0.3.9-source.tar.gz').read_bytes()), mode='r:gz')
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode='w:gz') as new:
            for item in old: new.addfile(item, old.extractfile(item))
            extra = tarfile.TarInfo(name)
            if symlink: extra.type = tarfile.SYMTYPE; extra.linkname = '/tmp/outside'; new.addfile(extra)
            else: extra.size = 1; new.addfile(extra, io.BytesIO(b'x'))
        old.close(); (self.out/'riskium-v0.3.9-source.tar.gz').write_bytes(buf.getvalue()); self.checksums()
    def test_valid_offline_roundtrip(self):
        r = verifier.verify(self.out, self.commit)
        self.assertTrue(r['git_commit_and_full_tree_reconstructed']); self.assertEqual(r['assets_checked'], 6)
    def test_all_six_assets_are_reproducible(self):
        self.assertEqual(self.assets, builder.render(self.commit, self.input))
    def test_missing_asset(self):
        (self.out/'release-notes.md').unlink(); self.reject('exactly six')
    def test_extra_asset(self):
        (self.out/'unexpected.txt').write_text('extra'); self.reject('exactly six')
    def test_changed_transport_body(self):
        p = self.out/'riskium-v0.3.9-source.tar.gz'; p.write_bytes(p.read_bytes()+b'changed'); self.reject('checksum mismatch')
    def test_source_manifest_tamper_despite_new_checksums(self):
        self.mutate_json('source-manifest.json', lambda m:m['files'][0].update(sha256='0'*64)); self.reject('manifest body mismatch')
    def test_forged_commit_object(self):
        self.mutate_json('source-manifest.json', lambda m:m.update(commit_object_base64=base64.b64encode(b'tree '+'0'.encode()*40+b'\n').decode()))
        self.reject('Commit object')
    def test_substituted_component_version(self):
        self.mutate_json('artifact-versions.json', lambda v:v['components'][0].update(version='99.0'))
        self.reject('Component version')
    def test_wrong_qualification_commit(self):
        def edit(r):
            r['qualification_report']['execution_commit'] = '0'*40
            r['qualification_report_sha256'] = builder.digest(builder.encoded(r['qualification_report']))
        self.mutate_json('freeze-receipt.json', edit); self.reject('Qualification execution')
    def test_false_publication_claim(self):
        self.mutate_json('freeze-receipt.json', lambda r:r.update(public_release_created=True)); self.reject('publication claim')
    def test_local_preflight_cannot_be_called_ci(self):
        self.mutate_json('freeze-receipt.json', lambda r:r.update(build_mode='ci',status='PREPARED_CI_NOT_PUBLISHED'))
        self.reject('CI run binding')
    def test_wrong_external_ci_run(self):
        assets = builder.render(self.commit, self.input, mode='ci', run_id=123)
        for name, body in assets.items(): (self.out/name).write_bytes(body)
        with self.assertRaisesRegex(ValueError, 'CI run binding'): verifier.verify(self.out,self.commit,124)
    def test_notes_are_bound_to_source_template(self):
        p = self.out/'release-notes.md'; p.write_bytes(p.read_bytes()+b'\nUnreviewed superiority claim.\n')
        self.mutate_json('freeze-receipt.json', lambda r:r['bound_assets_sha256'].update({'release-notes.md':builder.digest(p.read_bytes())}))
        self.reject('Release notes differ')
    def test_duplicate_archive_member(self):
        first = json.loads((self.out/'source-manifest.json').read_text())['files'][0]['path']
        self.archive_member('riskium-v0.3.9/'+first); self.reject('Duplicate archive member')
    def test_archive_path_traversal(self):
        self.archive_member('riskium-v0.3.9/../escape'); self.reject('Unsafe archive member')
    def test_archive_symlink(self):
        self.archive_member('riskium-v0.3.9/outside-link',True); self.reject('Non-regular archive member')
    def test_builder_rejects_old_qualification(self):
        report = deepcopy(self.report); report['execution_commit'] = '0'*40
        with self.assertRaisesRegex(ValueError,'another commit'): builder.render(self.commit,builder.encoded(report))

if __name__ == '__main__': unittest.main()
