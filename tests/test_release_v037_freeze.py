"""Synthetic packaging fixtures exercise corruption and offline boundaries only."""
import base64
import copy
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('freeze037',ROOT/'tools/releases/v037/freeze.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
sys.path.insert(0,str(ROOT/'tools'))
from run_relational_risk_nature import F, NEG, expected


def zipped(reports):
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name,data in reports.items():z.writestr(name,r.encode(data))
    return out.getvalue()


def packet(role,source,reports):
    prefix=dict(qualification='v037-packaging-qualification-',suite='v036-source-suite-',reader='released-actual-channels-')[role]
    data=zipped(reports)
    run=dict(id=dict(qualification=1,suite=2,reader=3)[role],head_sha=source,head_branch='main',
             event='workflow_run' if role=='reader' else 'push',path='.github/workflows/'+r.routing.PATHS[role],
             status='completed',conclusion='success',repository=dict(full_name=r.routing.REPO),head_repository=dict(full_name=r.routing.REPO))
    return dict(run=run,artifact=dict(name=prefix+source,digest='sha256:'+r.sha(data),expired=False,workflow_run=dict(head_sha=source)),zip_base64=base64.b64encode(data).decode())


def fixture(matrix,source):
    literal={x['id']:expected(x['expected']) for x in F['cases']}
    controls=[dict(id=x['id'],requirements=x['requirements'],expected=literal[x['id']],observed=literal[x['id']],status='PASS') for x in F['cases']]
    controls[-1].update(observed=None,status='PENDING_EXTERNAL_READBACK')
    declaration=json.loads((ROOT/'implementation/relational/0.9.0/declaration-manifest.json').read_bytes())
    raw=dict(source_commit=source,working_tree_clean=True,controls=controls,
             negative_variants=[dict(id=x['id'],control=x['control'],expected=x['expected'],observed=x['expected'],status='PASS') for x in NEG['variants']],
             runtime_source_sha256={**json.loads((ROOT/'implementation/relational/0.9.0/component.json').read_bytes())['files_sha256'],'implementation/relational/0.9.0/component.json':r.sha((ROOT/'implementation/relational/0.9.0/component.json').read_bytes())},native_semantic_acceptance=False,independent_ratings=0,summary=dict(PASS=59,FAIL=0,ERROR=0,PENDING_EXTERNAL_READBACK=1))
    suite=dict(source_commit=source,status='VERSIONED_SUITE_PASS',candidate_tests=570,historical_reader_tests=16)
    decl=dict(source_commit=source,status='RISK_NATURE_DECLARATION_VALID',runtime_controls_executed=0,files_sha256=declaration['files_sha256'])
    alignment=dict(source_commit=source,status='R3_ALIGNMENT_PASS',working_tree_clean=True)
    inventory=r.routing.current_inventory();inventory['source_commit']=source
    channel=copy.deepcopy(json.loads((ROOT/r.selection.R4).read_bytes())['actual_channels'])
    channel['source_commit']=source;channel['actual_channels']['documentation_source_commit']=source
    q={'releases/selection-v0.3.7.json':matrix,'build/v037-qualified-suite.json':suite,'build/v037-declaration.json':decl,
       'build/v037-runtime.json':raw,'build/v037-alignment.json':alignment,'build/v037-current-inventory.json':inventory}
    s={'versioned-suite.json':suite,'risk-nature-declaration.json':decl,'risk-nature-runtime.json':raw,'risk-nature-alignment.json':alignment}
    legacy=dict(id=4,head_sha=source,head_branch='main',event='push',path='.github/workflows/incremental-release.yml',status='completed',conclusion='failure',repository=dict(full_name=r.routing.REPO),head_repository=dict(full_name=r.routing.REPO))
    return dict(qualification=packet('qualification',source,q),suite=packet('suite',source,s),reader=packet('reader',source,{'actual-released-channels.json':channel}),
                legacy=dict(run=legacy,job_log='ValueError: '+r.routing.ERRORS[0]+'\nValueError: '+r.routing.ERRORS[1]),
                previous_releases=json.loads((ROOT/'evaluation/releases/v0.3.7/branch-qualification.json').read_bytes())['previous_release_inventory'],
                resolved_expectations=literal,independent_F60=dict(status='PASS',observed=F['cases'][-1]['expected']),synthetic_test_fixture=True)


class SixAssets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.folder=Path(cls.tmp.name)/'assets';cls.source='a'*40
        matrix=r.selection.selection()
        names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
        entries=[(p,0o644,(ROOT/p).read_bytes()) for p in sorted(set(names)) if (ROOT/p).is_file()]
        r.build_assets(cls.folder,cls.source,entries,matrix,fixture(matrix,cls.source),0)

    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()

    def changed(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);folder=Path(tmp.name)/'assets';shutil.copytree(self.folder,folder);return folder

    def rehash(self,folder):
        p=folder/'freeze-receipt.json';receipt=json.loads(p.read_bytes());receipt['payload_sha256']={n:r.sha((folder/n).read_bytes()) for n in receipt['payload_sha256']};p.write_bytes(r.encode(receipt))
        (folder/'SHA256SUMS.txt').write_text(''.join(r.sha((folder/n).read_bytes())+'  '+n+'\n' for n in sorted(r.ASSETS-{'SHA256SUMS.txt'})))

    def test_six_assets_verify_with_no_git_and_external_source_pin(self):
        with patch.object(r.common,'git',side_effect=AssertionError('Offline verifier invoked Git')):
            result=r.verify(self.folder,self.source)
        self.assertEqual(result['status'],'V037_SIX_ASSET_OFFLINE_PASS')
        self.assertEqual(result['controls'],60)
        self.assertTrue(result['external_authenticity_required'])
        self.assertFalse(result['publication_executed'])
        with self.assertRaisesRegex(ValueError,'identity'):r.verify(self.folder,'b'*40)

    def test_changed_notes_or_duplicate_checksums_are_rejected(self):
        folder=self.changed();(folder/'release-notes.md').write_text('changed')
        with self.assertRaisesRegex(ValueError,'checksum'):r.verify(folder)
        folder=self.changed();p=folder/'SHA256SUMS.txt';p.write_text(p.read_text()+p.read_text().splitlines()[0]+'\n')
        with self.assertRaisesRegex(ValueError,'Duplicate'):r.verify(folder)

    def test_coherently_rehashed_wrong_asset_version_is_rejected(self):
        folder=self.changed();p=folder/'artifact-versions.json';value=json.loads(p.read_bytes());value['tag']='v0.3.6';p.write_bytes(r.encode(value));self.rehash(folder)
        with self.assertRaisesRegex(ValueError,'identity'):r.verify(folder)

    def test_rehashed_traversal_duplicate_and_symlink_members_are_rejected(self):
        for variant in ('traversal','duplicate','symlink'):
            with self.subTest(variant=variant):
                folder=self.changed()
                with tarfile.open(folder/r.ARCHIVE) as old:members=[(m,old.extractfile(m).read()) for m in old]
                with tarfile.open(folder/r.ARCHIVE,'w:gz') as new:
                    for m,data in members:new.addfile(m,io.BytesIO(data))
                    extra=tarfile.TarInfo(r.TAG+'/../escape' if variant=='traversal' else members[0][0].name)
                    if variant=='symlink':extra.type=tarfile.SYMTYPE;extra.linkname='/etc/passwd'
                    new.addfile(extra,io.BytesIO(b''))
                self.rehash(folder)
                with self.assertRaisesRegex(ValueError,'Unsafe|Duplicate'):r.verify(folder)

    def test_rehashed_runtime_answer_and_overwritten_raw_F60_are_rejected(self):
        for variant in ('answer','F60'):
            folder=self.changed();p=folder/'freeze-receipt.json';receipt=json.loads(p.read_bytes());packet=receipt['evidence']['qualification'];reports=r.unpack(packet,r.QUALIFIED);raw=reports['v037-runtime.json']
            if variant=='answer':raw['controls'][0]['observed']={'invalid':'answer'}
            else:raw['controls'][-1]['status']='PASS'
            paths={('releases/' if n=='selection-v0.3.7.json' else 'build/')+n:v for n,v in reports.items()};data=zipped(paths);packet['zip_base64']=base64.b64encode(data).decode();packet['artifact']['digest']='sha256:'+r.sha(data)
            p.write_bytes(r.encode(receipt));self.rehash(folder)
            with self.assertRaisesRegex(ValueError,'Runtime answer|Raw F60'):r.verify(folder)

    def test_rehashed_stale_artifact_source_is_rejected(self):
        folder=self.changed();p=folder/'freeze-receipt.json';receipt=json.loads(p.read_bytes());receipt['evidence']['reader']['artifact']['workflow_run']['head_sha']='b'*40;p.write_bytes(r.encode(receipt));self.rehash(folder)
        with self.assertRaisesRegex(ValueError,'Artifact source'):r.verify(folder)

    def test_extracted_verifier_runs_with_standard_library_and_no_git_path(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        with tarfile.open(self.folder/r.ARCHIVE) as tar:tar.extractall(tmp.name,filter='data')
        import os
        run=subprocess.run([sys.executable,str(Path(tmp.name)/r.TAG/'tools/releases/v037/freeze.py'),'verify','--folder',str(self.folder),'--source',self.source],env=dict(os.environ,PATH='/nonexistent'),capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertEqual(json.loads(run.stdout)['status'],'V037_SIX_ASSET_OFFLINE_PASS')

if __name__ == '__main__':unittest.main()
