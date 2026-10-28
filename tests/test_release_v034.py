"""v0.3.4 profile/intent/freshness and downloaded-package trust boundaries.

Synthetic check/freshness records below are temporary software fixtures, never
retained or submitted as a real freeze/publication result.
"""
import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import release_v034 as release
import prepare_release_v034 as prepare
import prepare_stable_release as stable
import publish_stable_release as publisher


class Release034(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile=json.loads((ROOT/release.PROFILE).read_text())
        cls.matrix=json.loads((ROOT/cls.profile['artifact_matrix']).read_text())

    def blob(self,path):
        return (ROOT/path).read_bytes()

    def receipt(self):
        return dict(schema='riskium-v034-live-readback-v1',all_bytes_match=True,
            component_matrix_sha256=release.sha(self.blob(self.profile['artifact_matrix'])),
            files_sha256=self.matrix['documentation']['deployed_files_sha256'],pages_files=311,
            documentation_snapshots=4,wiki_files=23,wiki_commit=self.matrix['documentation']['wiki_commit'],
            checked_at_utc=datetime.now(timezone.utc).isoformat(),pages_source_commit='24c0323d4b731baf6d4d6c9a079cf66628ca4f39',
            pages_source_is_ancestor=True)

    def test_actual_profile_matches_preserved_science_and_full_prepared_matrix(self):
        self.assertEqual(release.validate_profile(ROOT)['tag'],'v0.3.4')
        self.assertEqual(len(release.validate_profile_blob(self.profile,self.blob)['artifacts']),28)

    def test_additive_profile_registration_preserves_original_registry_contract(self):
        before=stable.git(ROOT,'show','24c0323d4b731baf6d4d6c9a079cf66628ca4f39:'+stable.REGISTRY)
        self.assertEqual(self.blob(stable.REGISTRY),before)
        self.assertEqual(release.profile_path(ROOT),release.PROFILE)
        with self.assertRaises(ValueError):stable.profile_path(ROOT,'v0.3.4')

    def test_downloaded_matrix_validation_is_self_contained_without_git_history(self):
        with patch.object(release.prepared,'archived',side_effect=AssertionError('must not read Git history')):
            self.assertEqual(len(release.validate_matrix(self.matrix,self.blob)['artifacts']),28)

    def test_changed_source_or_missing_selected_component_is_rejected_offline(self):
        value=copy.deepcopy(self.matrix);value['artifacts'].pop()
        with self.assertRaises(ValueError):release.validate_matrix(value,self.blob)
        path='docs/releases/v0.3.4/index.html'
        with self.assertRaises(ValueError):
            release.validate_matrix(self.matrix,lambda p:self.blob(p)+b'changed' if p==path else self.blob(p))

    def test_native_version_or_independent_acceptance_promotion_is_rejected(self):
        for key,value in [('model_version','0.4.0'),('independent_validation_claimed',True),
                          ('full_original_requirement_acceptance_claimed',True)]:
            profile=copy.deepcopy(self.profile);profile[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):release.validate_profile_blob(profile,self.blob)

    def test_missing_publication_gate_or_tooling_closure_is_rejected(self):
        for kind in ['gate','tooling']:
            profile=copy.deepcopy(self.profile)
            if kind=='gate':profile['readback_required']=False
            else:profile['release_tooling_sha256'].pop(next(iter(profile['release_tooling_sha256'])))
            with self.subTest(kind=kind),self.assertRaises(ValueError):release.validate_profile_blob(profile,self.blob)

    def test_changed_release_tooling_is_rejected(self):
        path='tools/prepare_release_v034.py'
        with self.assertRaisesRegex(ValueError,'Release tooling drift'):
            release.validate_profile_blob(self.profile,lambda p:self.blob(p)+b'changed' if p==path else self.blob(p))

    def test_critical_finding_or_fabricated_review_cannot_be_cleared_by_packaging(self):
        for field,value in [('known_unresolved_critical_findings',['defect']),
                ('new_owner_responses_generated',1),('material_scientific_change_since_owner_acceptance',True)]:
            screen=json.loads(self.blob(release.SCREEN));screen[field]=value
            def blob(path):return json.dumps(screen).encode() if path==release.SCREEN else self.blob(path)
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'critical screen'):
                release.validate_profile_blob(self.profile,blob)

    def test_all_ten_release_checks_are_required_in_exact_order(self):
        good=[dict(command=['python',*a],exit_code=0) for a in release.EXTRA_CHECKS]
        self.assertEqual(len(good),10)
        release.validate_release_checks(good)
        for bad in [[],good[:-1],list(reversed(good)),[{**c,'exit_code':1 if i==4 else 0}for i,c in enumerate(good)]]:
            with self.subTest(length=len(bad)),self.assertRaises(ValueError):release.validate_release_checks(bad)

    def test_freshness_requires_every_system_current_and_four_snapshot_body(self):
        release.validate_freshness(self.matrix,self.receipt())
        for path in ['versions/index.html','current/index.html','releases/v0.3.1-rc.1/index.html','releases/v0.3.4/index.html']:
            receipt=copy.deepcopy(self.receipt());receipt['files_sha256'].pop(path)
            with self.subTest(path=path),self.assertRaises(ValueError):release.validate_freshness(self.matrix,receipt)

    def test_old_future_unrelated_or_wrong_matrix_readback_is_rejected(self):
        for mutation in [dict(checked_at_utc=(datetime.now(timezone.utc)-timedelta(days=2)).isoformat()),
                dict(checked_at_utc=(datetime.now(timezone.utc)+timedelta(days=1)).isoformat()),
                dict(pages_source_is_ancestor=False),dict(component_matrix_sha256='0'*64),
                dict(wiki_files=22),dict(documentation_snapshots=3),dict(all_bytes_match=False)]:
            receipt=copy.deepcopy(self.receipt());receipt.update(mutation)
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):release.validate_freshness(self.matrix,receipt)

    def intent_fixture(self,root):
        subprocess.run(['git','init','-q',str(root)],check=True)
        for path in [release.REGISTRY,release.PROFILE]:
            target=root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(self.blob(path))
        (root/release.REQUEST).write_text(json.dumps(dict(schema='riskium-reviewed-successor-request-v1',
            tag=release.TAG,profile='stable-bounded-research-artifact',publish=False)))
        return self.commit(root)

    def commit(self,root):
        subprocess.run(['git','-C',str(root),'add','.'],check=True)
        subprocess.run(['git','-C',str(root),'-c','user.name=Release Test','-c','user.email=release-test@example.invalid',
                        'commit','-qm','release fixture'],check=True)
        return stable.git(root,'rev-parse','HEAD').decode().strip()

    def test_new_explicit_intent_publishes_only_that_commit_not_later_pushes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);before=self.intent_fixture(root)
            request=json.loads((root/release.REQUEST).read_text());request.update(publish=True,reviewed_source_commit=before)
            (root/release.REQUEST).write_text(json.dumps(request));after=self.commit(root)
            self.assertEqual(release.resolve_intent(root,'push','refs/heads/main',before,after),dict(publish=True,release_tag=release.TAG))
            (root/'unrelated').write_text('later maintenance');later=self.commit(root)
            self.assertEqual(release.resolve_intent(root,'push','refs/heads/main',after,later),dict(publish=False,release_tag=''))

    def test_unreviewed_code_changes_after_dry_freeze_block_publication_intent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);before=self.intent_fixture(root)
            request=json.loads((root/release.REQUEST).read_text());request.update(publish=True,reviewed_source_commit=before)
            (root/release.REQUEST).write_text(json.dumps(request));(root/'changed-code').write_text('unreviewed')
            after=self.commit(root)
            with self.assertRaisesRegex(ValueError,'Unreviewed changes after dry freeze'):
                release.resolve_intent(root,'push','refs/heads/main',before,after)

    def test_missing_reviewed_source_wrong_branch_or_non_boolean_intent_is_rejected(self):
        for mutation,ref in [(dict(publish=True),'refs/heads/main'),(dict(publish=1),'refs/heads/main'),
                              (dict(publish=True),'refs/heads/topic')]:
            with tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);before=self.intent_fixture(root)
                request=json.loads((root/release.REQUEST).read_text());request.update(mutation)
                (root/release.REQUEST).write_text(json.dumps(request));after=self.commit(root)
                with self.subTest(mutation=mutation,ref=ref),self.assertRaises(ValueError):
                    release.resolve_intent(root,'push',ref,before,after)

    def test_manual_dry_run_is_distinct_from_explicit_publication(self):
        self.assertEqual(release.resolve_intent(ROOT,'workflow_dispatch','refs/heads/main','','',
            dict(release_tag=release.TAG,publish=False)),dict(publish=False,release_tag=release.TAG))
        with self.assertRaises(ValueError):release.resolve_intent(ROOT,'workflow_dispatch','refs/heads/topic','','',dict(release_tag=release.TAG,publish=True))

    def test_preceding_release_inventory_includes_all_ten_tags(self):
        with patch.object(publisher,'api',return_value=dict(id=1,draft=False,prerelease=False,assets=[])), \
             patch.object(publisher,'tag_commit',return_value='a'*40):
            previous=publisher.previous_releases('owner/repo',release.TAG)
        self.assertEqual([r['tag'] for r in previous],self.matrix['preserve_releases'])

    def test_real_archive_roundtrip_is_self_contained_and_rejects_reforged_missing_gates(self):
        # Temporary software fixture, not a real check run or publication receipt.
        checks=[dict(command=['python',*a],exit_code=0) for a in stable.CHECKS]
        extra=[dict(command=['python',*a],exit_code=0) for a in release.EXTRA_CHECKS]
        source=stable.git(ROOT,'rev-parse','HEAD').decode().strip()
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/'package'
            receipt=stable.package(ROOT,folder,self.profile,checks,self.receipt(),
                profile_resolver=release.profile_path,freshness_validator=release.validate_freshness)
            prepare.finalize(folder,receipt,self.profile,extra)
            with patch.object(release.prepared,'archived',side_effect=AssertionError('archive must not require Git')):
                frozen,manifest=publisher.validate_package(folder,source)
            self.assertEqual(frozen['tag'],release.TAG)
            self.assertEqual(manifest['file_count'],len(stable.git(ROOT,'ls-tree','-r','--name-only','HEAD').splitlines()))
            receipt['release_specific_checks']=[];stable.write(folder/'freeze-receipt.json',receipt)
            (folder/'SHA256SUMS.txt').write_text(''.join(stable.sha(p.read_bytes())+'  '+p.name+'\n'
                for p in sorted(folder.iterdir()) if p.name!='SHA256SUMS.txt'))
            with self.assertRaisesRegex(ValueError,'release checks'):publisher.validate_package(folder,source)


if __name__=='__main__':
    unittest.main()
