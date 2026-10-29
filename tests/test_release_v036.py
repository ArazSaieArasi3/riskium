"""Corruption and unsafe-archive checks for the six-asset source distribution."""
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('release036', ROOT/'tools/release_v036.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)


class SourceDistribution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.folder = Path(cls.temp.name)/'assets'
        cls.source = 'a'*40  # Explicit synthetic package identity; never live freeze evidence.
        matrix = r.selection()
        names = set(matrix['selected_files_sha256']) | set(matrix['delivery_support_sha256']) | {r.PRIOR}
        entries = [(name, 0o644, r.read(name)) for name in sorted(names)]
        entries.append((r.MATRIX, 0o644, r.encoded(matrix)))
        evidence = dict(suite=dict(status='VERSIONED_SUITE_PASS',source_commit=cls.source,candidate_tests=524,published_reader_tests=10),
                        runtime=dict(summary=dict(PASS=44,FAIL=0,ERROR=0)),
                        channels=dict(actual_channels=dict(documentation_source_commit=cls.source,status='ACTUAL_PUBLISHED_READER_CHANNELS_PASS')))
        r.build_assets(cls.folder, cls.source, entries, matrix, evidence, 0)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def altered(self):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        folder = Path(tmp.name)/'assets'; shutil.copytree(self.folder,folder)
        return folder

    def rebind(self,folder):
        """A coherent checksum rewrite must not conceal a malformed package."""
        receipt=json.loads((folder/'freeze-receipt.json').read_bytes())
        receipt['payload_sha256']={n:r.sha((folder/n).read_bytes()) for n in receipt['payload_sha256']}
        (folder/'freeze-receipt.json').write_bytes(r.encoded(receipt))
        (folder/'SHA256SUMS.txt').write_text(''.join(r.sha((folder/n).read_bytes())+'  '+n+'\n'
                                                 for n in sorted(r.ASSETS-{'SHA256SUMS.txt'})))

    def test_closed_selection_retains_every_old_payload_and_exact_dependency_version(self):
        matrix=r.selection();prior=r.load(r.PRIOR)
        self.assertEqual(matrix['summary']['components'],30)
        for path,digest in prior['selected_files_sha256'].items():
            self.assertEqual(matrix['selected_files_sha256'][path],digest)
        versions={x['id']:x['version'] for x in matrix['artifacts']}
        for edges in matrix['dependencies'].values():
            for edge in edges:self.assertEqual(edge['version'],versions[edge['id']])

    def test_missing_qualitative_r4_observation_blocks_component_selection(self):
        original=r.load
        def changed(path,root=r.ROOT):
            value=original(path,root)
            if path.endswith('/r4-reader-review.json'):value['criteria'].pop()
            return value
        with patch.object(r,'load',changed),self.assertRaisesRegex(ValueError,'Incomplete R4'):
            r.selection()

    def test_complete_package_verifies_with_no_git_calls(self):
        with patch.object(r,'git',side_effect=AssertionError('Offline verification invoked Git')):
            self.assertEqual(r.verify_package(self.folder,self.source)['status'],'V036_SIX_ASSET_OFFLINE_PASS')

    def test_changed_payload_is_not_accepted_by_unchanged_checksums(self):
        folder=self.altered();(folder/'release-notes.md').write_text('changed')
        with self.assertRaisesRegex(ValueError,'checksum mismatch'):r.verify_package(folder)

    def test_external_source_pin_is_required_when_a_caller_supplies_one(self):
        with self.assertRaisesRegex(ValueError,'identity mismatch'):
            r.verify_package(self.folder,'b'*40)

    def test_duplicate_or_missing_checksum_cannot_hide_an_asset(self):
        folder=self.altered();p=folder/'SHA256SUMS.txt';lines=p.read_text().splitlines()
        p.write_text('\n'.join([*lines,lines[0]])+'\n')
        with self.assertRaisesRegex(ValueError,'Duplicate'):r.verify_package(folder)

    def test_rehashed_traversal_duplicate_and_symlink_members_are_rejected(self):
        for variant in ('traversal','duplicate','symlink'):
            with self.subTest(variant=variant):
                folder=self.altered()
                with tarfile.open(folder/r.ARCHIVE,'r:gz') as old:
                    members=[(m,old.extractfile(m).read()) for m in old]
                with tarfile.open(folder/r.ARCHIVE,'w:gz') as new:
                    for m,data in members:new.addfile(m,io.BytesIO(data))
                    extra=tarfile.TarInfo(r.TAG+'/../escape' if variant=='traversal' else members[0][0].name)
                    if variant=='symlink':extra.type=tarfile.SYMTYPE;extra.linkname='/etc/passwd'
                    extra.mode=0o644;new.addfile(extra,io.BytesIO(b''))
                self.rebind(folder)
                with self.assertRaisesRegex(ValueError,'Unsafe|Duplicate'):r.verify_package(folder)

    def test_rehashed_asset_version_disagreement_is_rejected(self):
        folder=self.altered();p=folder/'artifact-versions.json';d=json.loads(p.read_bytes());d['tag']='v0.3.5'
        p.write_bytes(r.encoded(d));self.rebind(folder)
        with self.assertRaisesRegex(ValueError,'identity mismatch'):r.verify_package(folder)

    def test_rehashed_missing_execution_evidence_is_rejected(self):
        folder=self.altered();p=folder/'freeze-receipt.json';d=json.loads(p.read_bytes())
        d['evidence']['runtime']['summary']['PASS']=43;p.write_bytes(r.encoded(d));self.rebind(folder)
        with self.assertRaisesRegex(ValueError,'Missing executed'):r.verify_package(folder)


if __name__=='__main__':unittest.main()
