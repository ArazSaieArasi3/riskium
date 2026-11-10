"""Package guard tests use the actual prerequisite qualification, not invented engine results."""
import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import build_package as builder
import verify_package as verifier


class PackageContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = Path(os.environ['RISKIUM_N5A_QUALIFICATION']).read_bytes()
        cls.report = json.loads(cls.raw)
        cls.commit = cls.report['source_ref']
        cls.mode = 'ci' if cls.report['environment'] == 'CI' else 'local-preflight'
        cls.ci_run_id = int(cls.report['ci_run_id']) if cls.mode == 'ci' else None
        cls.snapshot = builder.snapshot(cls.commit)
        with patch.object(builder, 'snapshot', return_value=cls.snapshot):
            cls.assets = builder.render(cls.commit, cls.raw, cls.mode, cls.ci_run_id)

    def verify(self, assets, commit=None, run=None):
        with tempfile.TemporaryDirectory() as temp:
            for n, b in assets.items():
                (Path(temp) / n).write_bytes(b)
            return verifier.verify(temp, commit or self.commit, self.ci_run_id if run is None else run)

    def rehash(self, assets):
        assets['SHA256SUMS.txt'] = ''.join(builder.digest(b) + '  ' + n + '\n' for n, b in sorted(assets.items()) if n != 'SHA256SUMS.txt').encode()

    def test_reproducible_assets_and_independent_verification(self):
        with patch.object(builder, 'snapshot', return_value=self.snapshot):
            self.assertEqual(self.assets, builder.render(self.commit, self.raw, self.mode, self.ci_run_id))
        self.assertEqual(self.verify(self.assets)['assets_checked'], 6)

    def test_wrong_pinned_commit_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Source commit disagreement'):
            self.verify(self.assets, commit='0' * 40)

    def test_unqualified_source_rejected(self):
        q = copy.deepcopy(self.report); q['status'] = 'INCOMPLETE'
        with patch.object(builder, 'snapshot', return_value=self.snapshot), self.assertRaisesRegex(ValueError, 'qualification required'):
            builder.render(self.commit, builder.encoded(q), self.mode, self.ci_run_id)

    def test_forged_normative_review_rejected_after_checksum_update(self):
        assets = copy.deepcopy(self.assets)
        value = json.loads(assets['artifact-versions.json']); value['review_version'] = 'verified-equivalences'
        assets['artifact-versions.json'] = builder.encoded(value); self.rehash(assets)
        with self.assertRaises(ValueError):
            self.verify(assets)

    def test_premature_publication_rejected_after_checksum_update(self):
        assets = copy.deepcopy(self.assets)
        value = json.loads(assets['freeze-receipt.json']); value['public_release_created'] = True
        assets['freeze-receipt.json'] = builder.encoded(value); self.rehash(assets)
        with self.assertRaisesRegex(ValueError, 'Premature publication'):
            self.verify(assets)

    def test_incomplete_six_asset_inventory_rejected(self):
        assets = copy.deepcopy(self.assets); del assets['release-notes.md']
        with self.assertRaisesRegex(ValueError, 'exactly six'):
            self.verify(assets)

    def test_archive_path_traversal_rejected(self):
        import io, tarfile
        output = io.BytesIO()
        with tarfile.open(fileobj=output, mode='w:gz') as tar:
            item = tarfile.TarInfo('riskium-v0.3.10/../outside'); item.size = 1
            tar.addfile(item, io.BytesIO(b'x'))
        with self.assertRaisesRegex(ValueError, 'Unsafe archive'):
            verifier.archive_files(output.getvalue(), 'riskium-v0.3.10')


if __name__ == '__main__':
    unittest.main(verbosity=2)
