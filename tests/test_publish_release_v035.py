"""One-shot publication boundaries. Remote records here are software fixtures."""
import copy
from contextlib import contextmanager
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import publish_release_v035 as pub
import release_v035_final as release


class Publication035(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((ROOT / pub.PROFILE).read_bytes())
        cls.request = json.loads((ROOT / pub.REQUEST).read_bytes())
        cls.baseline = json.loads((ROOT / pub.BASELINE).read_bytes())['releases']
        cls.source = 'a' * 40

    def config_blob(self, config=None, request=None):
        values = {pub.PROFILE: config or self.config, pub.REQUEST: request or self.request}
        return lambda p: (json.dumps(values[p]) + '\n').encode()

    def run_record(self):
        return dict(id=11, path=pub.WORKFLOW, name=pub.WORKFLOW_NAME,
                    head_sha=self.source, head_branch='main', event='workflow_run',
                    repository=dict(full_name=pub.REPO), head_repository=dict(full_name=pub.REPO),
                    status='in_progress', conclusion=None)

    def artifact(self):
        return dict(id=22, name='riskium-v0.3.5-freeze-' + self.source,
                    digest='sha256:' + 'b' * 64, expired=False, size_in_bytes=1,
                    workflow_run=dict(id=11, head_sha=self.source, head_branch='main'))

    def getter(self, artifact=None, jobs=None, run=None):
        records = {
            'git/ref/heads/main': dict(object=dict(sha=self.source)),
            'actions/runs/11': run or self.run_record(),
            'actions/runs/11/jobs?per_page=100': dict(jobs=jobs or [
                dict(name=n, status='completed', conclusion='success') for n in ('freeze', 'staged')]),
            'actions/runs/11/artifacts?per_page=100': dict(artifacts=[artifact or self.artifact()]),
        }
        return lambda path, **kwargs: copy.deepcopy(records[path])

    def commit(self, root, allow_empty=False):
        subprocess.run(['git', '-C', str(root), 'add', '--all'], check=True)
        args = ['git', '-C', str(root), '-c', 'user.name=Publication Test',
                '-c', 'user.email=publication-test@example.invalid', 'commit', '-qm', 'software fixture']
        if allow_empty:
            args.append('--allow-empty')
        subprocess.run(args, check=True)
        return pub.git(root, 'rev-parse', 'HEAD')

    def intent_fixture(self, root, extra=False, wrong_parent=False):
        subprocess.run(['git', 'init', '-q', str(root)], check=True)
        parent = self.commit(root, allow_empty=True)
        request = dict(self.request, expected_parent='0' * 40 if wrong_parent else parent)
        for path, data in [(pub.PROFILE, self.config), (pub.REQUEST, request)]:
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(data))
        if extra:
            (root / 'unexpected.txt').write_text('Unreviewed source change')
        return self.commit(root)

    def live_prior(self):
        return [dict(tag_name=r['tag'], id=r['release_id'], name=r['name'],
                     draft=r['draft'], prerelease=r['prerelease'], published_at=r['published_at'],
                     html_url=r['url'], assets=[dict(a, browser_download_url=a['url']) for a in r['assets']])
                for r in self.baseline]

    def prior_getter(self, rows=None, wrong_tag=False):
        rows = rows if rows is not None else self.live_prior()
        sources = {r['tag']: r['source_commit'] for r in self.baseline}
        def get(path, **kwargs):
            if path == 'releases?per_page=100':
                return copy.deepcopy(rows)
            tag = path.removeprefix('git/ref/tags/')
            return dict(object=dict(type='commit', sha='0' * 40 if wrong_tag else sources[tag]))
        return get

    def test_actual_publication_profile_is_inside_the_offline_tooling_closure(self):
        release.validate_profile(ROOT)
        release.validate_publication_config(release.reader(ROOT))
        matrix = json.loads((ROOT / release.MATRIX).read_bytes())
        self.assertTrue({pub.PROFILE, pub.REQUEST, 'tools/publish_release_v035.py',
                         'tests/test_publish_release_v035.py'} <= set(matrix['finalization_tooling_sha256']))

    def test_publication_config_rejects_false_numeric_or_missing_authority_and_gates(self):
        for change in [dict(publish=False), dict(publish=1), dict(expected_parent='bad'),
                       dict(activation_id='replayed'), dict(prior_dry_freeze_source='0' * 40)]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                release.validate_publication_config(self.config_blob(request={**self.request, **change}))
        for key in ('draft_download_required', 'separate_public_readback_required',
                    'new_tag_release_required', 'exact_main_required'):
            with self.subTest(key=key), self.assertRaises(ValueError):
                release.validate_publication_config(self.config_blob(config={**self.config, key: False}))

    def test_real_git_authority_applies_only_to_the_commit_that_changed_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = self.intent_fixture(root)
            with patch.object(release, 'validate_profile', return_value={}):
                result = pub.resolve_intent(root, source, getter=lambda p: dict(object=dict(sha=source)))
                self.assertTrue(result['publish'])
                (root / 'later.txt').write_text('ordinary later maintenance')
                later = self.commit(root)
                getter = unittest.mock.Mock(side_effect=AssertionError('No remote authority for retained request'))
                self.assertFalse(pub.resolve_intent(root, later, getter=getter)['publish'])
                getter.assert_not_called()

    def test_wrong_parent_unreviewed_delta_and_advanced_main_block_publication(self):
        for kind in ('parent', 'delta', 'main'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                source = self.intent_fixture(root, extra=kind == 'delta', wrong_parent=kind == 'parent')
                with patch.object(release, 'validate_profile', return_value={}), self.assertRaises(ValueError):
                    pub.resolve_intent(root, source, getter=lambda p: dict(
                        object=dict(sha='0' * 40 if kind == 'main' else source)))

    def test_workflow_origin_rejects_other_source_repository_event_or_failed_run(self):
        pub.workflow_origin(self.run_record(), self.source)
        for mutation in [dict(head_sha='0' * 40), dict(head_branch='topic'), dict(event='pull_request'),
                         dict(repository=dict(full_name='other/repo')),
                         dict(status='completed', conclusion='failure')]:
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                pub.workflow_origin({**self.run_record(), **mutation}, self.source)

    def test_required_successful_jobs_cannot_be_replaced_by_count_or_duplicates(self):
        good = [dict(name=n, status='completed', conclusion='success') for n in ('freeze', 'staged')]
        pub.require_jobs(good, ('freeze', 'staged'))
        for rows in [good[:1], good + [good[0]], [{**r, 'conclusion': 'failure'} for r in good]]:
            with self.assertRaises(ValueError):
                pub.require_jobs(rows, ('freeze', 'staged'))

    def test_artifact_cannot_be_expired_rebound_or_taken_from_another_run(self):
        pub.authenticated_artifact(11, self.source, 22, 'b' * 64, getter=self.getter())
        for change in [dict(expired=True), dict(digest='sha256:' + 'c' * 64),
                       dict(workflow_run=dict(id=10, head_sha=self.source, head_branch='main'))]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                pub.authenticated_artifact(11, self.source, 22, 'b' * 64,
                                           getter=self.getter(artifact={**self.artifact(), **change}))

    def test_api_missing_is_only_a_real_404_and_other_failures_are_closed(self):
        with patch.object(subprocess, 'run', return_value=SimpleNamespace(returncode=1, stdout='', stderr='Forbidden (HTTP 403)')):
            with self.assertRaises(ValueError):
                pub.api('anything', missing_ok=True)
        with patch.object(subprocess, 'run', return_value=SimpleNamespace(returncode=1, stdout='', stderr='Not Found (HTTP 404)')):
            self.assertIsNone(pub.api('anything', missing_ok=True))

    def test_all_eleven_release_and_fifty_eight_asset_identities_and_tag_sources_are_preserved(self):
        proof = pub.previous_inventory(ROOT, self.prior_getter())
        self.assertEqual(len(proof), 11)
        self.assertEqual(sum(len(r['assets']) for r in proof), 58)
        bad = self.live_prior(); bad[0]['assets'][0]['digest'] = 'sha256:' + '0' * 64
        for getter in (self.prior_getter(bad), self.prior_getter(wrong_tag=True)):
            with self.assertRaises(ValueError):
                pub.previous_inventory(ROOT, getter)

    def test_new_release_guard_rejects_existing_tag_release_or_draft(self):
        for existing in ('tag', 'release', 'draft'):
            def getter(path, missing_ok=False):
                if path == 'releases?per_page=100':
                    return [dict(tag_name=pub.TAG)] if existing == 'draft' else []
                if existing == 'tag' and path.startswith('git/ref/'):
                    return dict(object=dict(sha=self.source))
                if existing == 'release' and path.startswith('releases/tags/'):
                    return dict(id=1)
                return None
            with self.subTest(existing=existing), self.assertRaises(ValueError):
                pub.assert_new(getter)

    def test_raw_zip_digest_and_six_asset_inventory_are_enforced(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); archive = root / 'source.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                for name in release.ASSETS:
                    z.writestr(name, b'SOFTWARE FIXTURE')
            pub.unpack_assets(archive, root / 'safe')
            self.assertEqual({p.name for p in (root / 'safe').iterdir()}, release.ASSETS)
            with zipfile.ZipFile(archive, 'a') as z:
                z.writestr('../escape', b'unsafe')
            with self.assertRaises(ValueError):
                pub.unpack_assets(archive, root / 'bad')
            with patch.object(subprocess, 'run', return_value=None):
                with self.assertRaises(ValueError):
                    pub.download_zip(dict(id=1, size_in_bytes=0, digest='sha256:' + '0' * 64), archive)

    def test_source_archive_requires_real_git_blob_identity_and_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'repo'; root.mkdir()
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / 'file.txt').write_bytes(b'original')
            source = self.commit(root)
            folder = Path(tmp) / 'assets'; folder.mkdir()
            for data, mode, accepted in [(b'original', 0o644, True), (b'changed', 0o644, False),
                                          (b'original', 0o755, False)]:
                with tarfile.open(folder / 'riskium-v0.3.5-source.tar.gz', 'w:gz') as tar:
                    member = tarfile.TarInfo('riskium-v0.3.5/file.txt')
                    member.size, member.mode = len(data), mode
                    tar.addfile(member, io.BytesIO(data))
                if accepted:
                    pub.verify_git_archive(root, folder, source)
                else:
                    with self.assertRaises(ValueError):
                        pub.verify_git_archive(root, folder, source)

    def test_writes_require_the_exact_canonical_actions_run(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(pub, 'gh') as writer:
            with self.assertRaises(ValueError):
                pub.publish(ROOT, self.source, 11, 22, 'b' * 64, Path('unused'))
            writer.assert_not_called()

    def test_draft_download_must_pass_before_publication_and_main_is_rechecked(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for name in release.ASSETS:
                (folder / name).write_text('fixture')
            events = []
            @contextmanager
            def trusted(*args, **kwargs):
                yield folder, {}, {}, dict(id=22, digest='sha256:' + 'b' * 64)
            def gh(*args):
                events.append(args[1])
            def download(*args, **kwargs):
                self.assertEqual(events, ['create'])
                self.assertTrue(kwargs['draft'])
                events.append('download')
                return dict(release_id=99, checks=[])
            def api(path, **kwargs):
                if path == 'releases/latest':
                    return dict(tag_name=pub.TAG if 'edit' in events else 'v0.3.4', id=99)
                if path == 'git/ref/heads/main':
                    return dict(object=dict(sha='0' * 40 if advanced else self.source))
                return None
            advanced = False
            with patch.object(pub, 'require_actions'), patch.object(pub, 'trusted_package', trusted), \
                 patch.object(pub, 'assert_new'), patch.object(pub, 'previous_inventory', return_value=[]), \
                 patch.object(pub, 'api', side_effect=api), patch.object(pub, 'gh', side_effect=gh), \
                 patch.object(pub, 'tag_commit', return_value=self.source), \
                 patch.object(pub, 'verify_download', side_effect=download):
                pub.publish(ROOT, self.source, 11, 22, 'b' * 64, folder / 'attempt.json')
                self.assertEqual(events, ['create', 'download', 'edit'])
                advanced = True
                events.clear()
                with self.assertRaises(ValueError):
                    pub.publish(ROOT, self.source, 11, 22, 'b' * 64, folder / 'attempt.json')
                self.assertEqual(events, ['create', 'download'])

    def test_public_download_checks_every_actual_body_and_github_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            assets = []
            for i, name in enumerate(sorted(release.ASSETS)):
                raw = ('SOFTWARE FIXTURE ' + name).encode(); (folder / name).write_bytes(raw)
                assets.append(dict(id=i, name=name, size=len(raw), digest='sha256:' + hashlib.sha256(raw).hexdigest(),
                                   browser_download_url='https://example.invalid/' + name))
            info = dict(id=99, tag_name=pub.TAG, draft=False, prerelease=False,
                        assets=assets, html_url='https://example.invalid/release', published_at='fixture')
            def download(*args):
                dest = Path(args[args.index('--dir') + 1])
                for name in release.ASSETS:
                    shutil.copyfile(folder / name, dest / name)
            freeze = dict(checks=[{}] * 28, release_specific_checks=[{}] * 13, frozen_at_utc='fixture')
            with patch.object(pub, 'api', return_value=info), patch.object(pub, 'tag_commit', return_value=self.source), \
                 patch.object(pub, 'gh', side_effect=download), \
                 patch.object(release, 'validate_package', return_value=(freeze, dict(file_count=1))):
                self.assertTrue(pub.verify_download(folder, self.source)['actual_downloaded_bytes_match'])
                info['assets'][0]['digest'] = 'sha256:' + '0' * 64
                with self.assertRaises(ValueError):
                    pub.verify_download(folder, self.source)

    def test_legacy_retirement_cannot_run_before_independent_public_verification(self):
        jobs = [dict(name=n, status='completed', conclusion='success')
                for n in ('freeze', 'staged', 'publish', 'verify')]
        jobs[-1]['conclusion'] = 'failure'
        writes = []
        def getter(path, **kwargs):
            if kwargs.get('method') == 'PUT':
                writes.append(path)
            if path.startswith('actions/runs/11/jobs'):
                return dict(jobs=jobs)
            return self.run_record()
        with patch.object(pub, 'require_actions'), patch.object(pub, 'resolve_intent', return_value=dict(publish=True)), \
             patch.object(pub, 'api', side_effect=getter), self.assertRaises(ValueError):
            pub.retire(ROOT, self.source, 11, Path('unused'))
        self.assertEqual(writes, [])

    def test_successful_retirement_is_limited_to_the_three_declared_workflows(self):
        with tempfile.TemporaryDirectory() as tmp:
            states = {i + 1: 'active' for i in range(3)}
            paths = {i + 1: path for i, path in enumerate(pub.LEGACY)}
            writes = []
            def getter(path, **kwargs):
                if path == 'actions/runs/11':
                    return self.run_record()
                if path == 'actions/runs/11/jobs?per_page=100':
                    return dict(jobs=[dict(name=n, status='completed', conclusion='success')
                                      for n in ('freeze', 'staged', 'publish', 'verify')])
                if path == 'git/ref/heads/main':
                    return dict(object=dict(sha=self.source))
                if path == 'releases/latest':
                    return dict(tag_name=pub.TAG)
                tail = path.removeprefix('actions/workflows/')
                if kwargs.get('method') == 'PUT':
                    ident = int(tail.split('/')[0]); states[ident] = 'disabled_manually'
                    writes.append(ident); return None
                ident = int(tail) if tail.isdigit() else next(i for i, p in paths.items() if Path(p).name == tail)
                return dict(id=ident, path=paths[ident], state=states[ident])
            with patch.object(pub, 'require_actions'), patch.object(pub, 'resolve_intent', return_value=dict(publish=True)), \
                 patch.object(pub, 'api', side_effect=getter), patch.object(pub, 'tag_commit', return_value=self.source), \
                 patch.object(pub, 'previous_inventory', return_value=[]):
                result = pub.retire(ROOT, self.source, 11, Path(tmp) / 'transition.json')
            self.assertEqual(writes, [1, 2, 3])
            self.assertEqual({r['path'] for r in result['retired_workflows']}, set(pub.LEGACY))


if __name__ == '__main__':
    unittest.main()
