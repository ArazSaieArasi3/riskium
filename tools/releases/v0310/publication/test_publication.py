"""Publication guard tests use declared fixtures, never report a fabricated release."""
import copy
import unittest
from pathlib import Path
import build


class PublicationContracts(unittest.TestCase):
    def setUp(self):
        self.intent = {'source_commit': 'a' * 40, 'run_id': 777, 'assets': {str(i): {'bytes': i, 'sha256': 'b' * 64} for i in range(6)}}
        self.release = {'tag_name': 'v0.3.10', 'id': 1, 'draft': False, 'prerelease': False, 'published_at': 'TEST_ONLY',
                        'assets': [{'name': n, 'size': v['bytes'], 'digest': 'sha256:' + v['sha256']} for n, v in self.intent['assets'].items()]}
        self.tag = {'type': 'commit', 'sha': 'a' * 40}
        self.run = {'head_sha': 'a' * 40, 'status': 'completed', 'conclusion': 'success'}

    def test_exact_publication_fixture_is_accepted(self):
        self.assertTrue(build.verify_release(self.intent, self.release, self.release, self.tag, self.run))

    def test_draft_is_rejected(self):
        self.release['draft'] = True
        with self.assertRaises(ValueError):
            build.verify_release(self.intent, self.release, self.release, self.tag, self.run)

    def test_wrong_latest_is_rejected(self):
        latest = copy.deepcopy(self.release); latest['tag_name'] = 'v0.3.9'
        with self.assertRaises(ValueError):
            build.verify_release(self.intent, self.release, latest, self.tag, self.run)

    def test_wrong_tag_source_is_rejected(self):
        self.tag['sha'] = 'c' * 40
        with self.assertRaises(ValueError):
            build.verify_release(self.intent, self.release, self.release, self.tag, self.run)

    def test_failed_ci_is_rejected(self):
        self.run['conclusion'] = 'failure'
        with self.assertRaises(ValueError):
            build.verify_release(self.intent, self.release, self.release, self.tag, self.run)

    def test_missing_asset_is_rejected(self):
        self.release['assets'].pop()
        with self.assertRaises(ValueError):
            build.verify_release(self.intent, self.release, self.release, self.tag, self.run)

    def test_wrong_public_asset_digest_is_rejected(self):
        self.release['assets'][0]['digest'] = 'sha256:' + '0' * 64
        with self.assertRaises(ValueError):
            build.verify_release(self.intent, self.release, self.release, self.tag, self.run)

    def test_all_authored_scientific_sections_remain_present(self):
        release = {**self.release, 'html_url': 'https://example.invalid/TEST_ONLY'}
        for p in build.reader.OUT.glob('RKM-*.md'):
            before = p.read_text(); after = build.promoted(before, p.stem, self.intent, release)
            for h in ['Authored source definition', 'Identity and source typing', 'Direct catalog associations', 'Direct inheritance']:
                original = before.split('## ' + h + '\n', 1)[1].split('\n## ', 1)[0]
                current = after.split('## ' + h + '\n', 1)[1].split('\n## ', 1)[0]
                self.assertEqual(original, current)

    def test_three_normative_deferrals_survive_promotion(self):
        for cid in build.curation.DEFERRED:
            text = build.promoted((build.reader.OUT / (cid + '.md')).read_text(), cid, self.intent, self.release)
            self.assertIn('Normative mapping deferred', text)
            self.assertIn('/issues/78', text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
