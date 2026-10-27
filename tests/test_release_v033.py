"""Second successor release boundaries; no fabricated publication evidence."""
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import review_distribution as dist
import prepare_stable_release as stable
import publish_stable_release as publisher


class Release033(unittest.TestCase):
    def setUp(self):
        self.profile = stable.read(ROOT, 'releases/stable-profile-v0.3.3.json')
        self.matrix = stable.read(ROOT, self.profile['artifact_matrix'])

    def test_selected_profile_preserves_science_and_pins_twenty_four_components(self):
        self.assertEqual(stable.validate_profile(ROOT, 'v0.3.3')['model_version'], '0.3.1')
        self.assertEqual(len(dist.validate_distribution(ROOT, self.profile)['artifacts']), 24)

    def test_missing_or_altered_selection_is_rejected(self):
        for kind in ['missing', 'correction', 'snapshot', 'wiki', 'prior-release', 'version']:
            m = copy.deepcopy(self.matrix)
            if kind == 'missing': m['artifacts'].pop(19)
            elif kind == 'correction': m['artifacts'][18]['files'].pop()
            elif kind == 'snapshot': m['documentation']['snapshot']['documentation_version'] = '9.0.0'
            elif kind == 'wiki': m['documentation']['wiki_files_sha256'].pop('Home.md')
            elif kind == 'prior-release': m['preserve_releases'].remove('v0.3.2')
            else: m['artifacts'][19]['version'] = '9.0.0'
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                dist.validate_matrix(m, lambda p: (ROOT / p).read_bytes())

    def test_selected_current_or_frozen_bytes_cannot_drift(self):
        for path in ['docs/current/index.html', 'docs/wiki/Home.md', 'docs/releases/v0.3.3/index.html',
                     'implementation/relational/0.3.0/004_correction.sql']:
            def blob(p):
                b = (ROOT / p).read_bytes()
                return b + b'changed' if p == path else b
            with self.subTest(path=path), self.assertRaises(ValueError):
                dist.validate_matrix(self.matrix, blob)

    def test_all_registered_snapshots_require_actual_fresh_readback(self):
        pages = dist.selected_pages(self.matrix)
        docs = self.matrix['documentation']
        self.assertEqual(len(docs['frozen_snapshots']), 3)
        for row in docs['frozen_snapshots'].values():
            self.assertIn(row['route'] + '/index.html', pages)
        receipt = dict(schema='riskium-successor-live-readback-v1', all_bytes_match=True,
                       component_matrix_sha256=dist.sha((json.dumps(self.matrix, indent=2)+'\n').encode()),
                       checked_at_utc=datetime.now(timezone.utc).isoformat(),
                       wiki_commit=docs['wiki_commit'], wiki_files=23, current_files=68,
                       frozen_files=len(pages)-68, files_sha256=pages)
        dist.validate_freshness(self.matrix, receipt)
        for path in ['current/index.html', 'releases/v0.3.2/index.html', 'releases/v0.3.3/index.html']:
            changed = copy.deepcopy(receipt)
            if path in changed['files_sha256']: changed['files_sha256'].pop(path)
            else: changed['frozen_files'] -= 1
            with self.subTest(path=path), self.assertRaises(ValueError):
                dist.validate_freshness(self.matrix, changed)

    def test_preceding_stable_v032_is_preserved_by_the_publisher(self):
        with patch.object(publisher, 'api', return_value=dict(id=1,draft=False,prerelease=False,assets=[])), \
             patch.object(publisher, 'tag_commit', return_value='a'*40):
            previous = publisher.previous_releases('owner/repo', 'v0.3.3')
        self.assertEqual([r['tag'] for r in previous], self.matrix['preserve_releases'])
        self.assertEqual(len(previous), 9)

    def test_profile_matrix_pairing_is_enforced(self):
        p = copy.deepcopy(self.profile)
        p['artifact_matrix'] = 'releases/distribution-v0.3.2.json'
        with self.assertRaisesRegex(ValueError, 'Profile/matrix tag mismatch'):
            dist.validate_distribution(ROOT, p)


if __name__ == '__main__':
    unittest.main()
