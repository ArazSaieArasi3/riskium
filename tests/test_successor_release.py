"""Successor release trust boundaries; fixtures do not constitute a real freeze."""
import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
import tempfile
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import prepare_stable_release as stable
import publish_stable_release as publisher
import review_distribution as dist
import prepare_incremental_release as incremental


class SuccessorRelease(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._frozen = tempfile.TemporaryDirectory()
        cls.frozen = Path(cls._frozen.name)/'source'
        subprocess.run(['git','clone','--quiet','--shared','--no-checkout',str(ROOT),str(cls.frozen)],check=True)
        subprocess.run(['git','checkout','--quiet','--detach','67ebe1e9bd8b2e82649ed4ff43bfb1620c13bd48'],cwd=cls.frozen,check=True)

    @classmethod
    def tearDownClass(cls):
        cls._frozen.cleanup()

    def setUp(self):
        self.profile = stable.read(ROOT, 'releases/stable-profile-v0.3.2.json')
        self.matrix = stable.read(ROOT, self.profile['artifact_matrix'])

    def receipt(self):
        docs=self.matrix['documentation']
        files={'current/'+p:h for p,h in docs['current_files_sha256'].items()}
        files.update({docs['snapshot']['route']+'/'+p:h for p,h in docs['snapshot']['files_sha256'].items()})
        return dict(schema='riskium-successor-live-readback-v1', all_bytes_match=True,
                    component_matrix_sha256=dist.sha((json.dumps(self.matrix, indent=2)+'\n').encode()),
                    checked_at_utc=datetime.now(timezone.utc).isoformat(),
                    wiki_commit=self.matrix['documentation']['wiki_commit'], wiki_files=23,
                    current_files=53, frozen_files=53, files_sha256=files)

    def test_successor_keeps_original_model_and_twenty_explicit_components(self):
        p = stable.validate_profile(self.frozen, 'v0.3.2')
        self.assertEqual((p['tag'], p['model_version']), ('v0.3.2', '0.3.1'))
        self.assertEqual(len(dist.validate_distribution(self.frozen, p)['artifacts']), 20)

    def test_unregistered_and_unsafe_tags_are_rejected(self):
        for tag in ['v0.3.4', '../v0.3.2', 'v0.3.2-rc.1', 'v0.3.2\npublish=true']:
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                stable.profile_path(ROOT, tag)

    def test_incompatible_duplicate_or_changed_component_is_rejected(self):
        for kind in ['compatibility', 'duplicate', 'hash', 'selection', 'old-stable']:
            m = copy.deepcopy(self.matrix)
            if kind == 'compatibility': m['artifacts'][18]['compatible_model'] = '0.4.0'
            elif kind == 'duplicate': m['artifacts'][18]['id'] = m['artifacts'][19]['id']
            elif kind == 'hash': m['artifacts'][18]['files'][0]['sha256'] = '0'*64
            elif kind == 'selection': m['artifacts'][10]['version'] = '9.0.0'
            else: m['preserve_releases'].remove('v0.3.1')
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                dist.validate_matrix(m, lambda p:(self.frozen/p).read_bytes())

    def test_stale_wiki_source_or_projection_receipt_blocks_selection(self):
        for path in ['tools/publication/guide-registry.json', 'docs/work-plan.md', 'docs/wiki/Home.md']:
            def blob(p):
                data = (self.frozen/p).read_bytes()
                return data+b'changed' if p == path else data
            with self.subTest(path=path), self.assertRaises(ValueError):
                dist.validate_matrix(self.matrix, blob)

    def test_fresh_actual_readback_is_required_not_historical_receipt(self):
        dist.validate_freshness(self.matrix, self.receipt())
        for change in [dict(wiki_commit='0'*40), dict(wiki_files=22), dict(all_bytes_match=False),
                       dict(component_matrix_sha256='0'*64),
                       dict(checked_at_utc=(datetime.now(timezone.utc)-timedelta(days=2)).isoformat())]:
            r = self.receipt(); r.update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                dist.validate_freshness(self.matrix, r)

    def test_successor_manual_request_is_explicit_and_wrong_branch_fails(self):
        head=stable.git(ROOT,'rev-parse','HEAD').decode().strip()
        self.assertEqual(stable.resolve_intent(ROOT,'workflow_dispatch','refs/heads/main','',head,
                         {'publish':True,'release_tag':'v0.3.2'})['release_tag'],'v0.3.2')
        with self.assertRaises(ValueError):
            stable.resolve_intent(ROOT,'workflow_dispatch','refs/heads/topic','',head,
                                  {'publish':True,'release_tag':'v0.3.2'})

    def test_manual_dry_run_selects_registered_tag_without_publication(self):
        for tag in ['v0.3.1','v0.3.2']:
            self.assertEqual(stable.resolve_intent(ROOT,'workflow_dispatch','refs/heads/main','','',
                             {'publish':False,'release_tag':tag}),{'publish':False,'release_tag':tag})
        with self.assertRaises(ValueError):
            stable.resolve_intent(ROOT,'workflow_dispatch','refs/heads/main','','',
                                  {'publish':False,'release_tag':'v0.3.9'})

    def test_complete_package_roundtrip_and_changed_download_are_detected(self):
        # Explicit software-test fixture: these synthetic check records are never
        # submitted as a real workflow/freeze/publication result.
        checks=[dict(command=['python',*args],exit_code=0) for args in stable.CHECKS]
        head=stable.git(self.frozen,'rev-parse','HEAD').decode().strip()
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder)/'package'
            stable.package(self.frozen,out,self.profile,checks,self.receipt())
            freeze,manifest=publisher.validate_package(out,head)
            self.assertEqual(freeze['tag'],'v0.3.2')
            self.assertGreater(manifest['file_count'],568)
            with self.assertRaises(ValueError):
                publisher.validate_package(out,'0'*40)
            (out/'release-notes.md').write_text('altered downloaded asset')
            with self.assertRaisesRegex(ValueError,'digest mismatch'):
                publisher.validate_package(out,head)

    def test_successor_tag_or_existing_draft_cannot_be_overwritten(self):
        for existing in ['git/ref/tags/v0.3.2','releases/tags/v0.3.2']:
            def getter(repo,path,missing_ok=False):
                return [] if path=='releases?per_page=100' else ({'id':1} if path==existing else None)
            with self.subTest(existing=existing), self.assertRaises(ValueError):
                publisher.assert_new('owner/repo',getter,tag='v0.3.2')
        with self.assertRaises(ValueError):
            publisher.assert_new('owner/repo',lambda r,p,**k:[{'tag_name':'v0.3.2','draft':True}]
                                 if p=='releases?per_page=100' else None,tag='v0.3.2')

    def test_previous_inventory_includes_old_stable_for_successor(self):
        def api(repo,path):
            return dict(id=1,draft=False,prerelease=True,assets=[])
        with patch.object(publisher,'api',side_effect=api),patch.object(publisher,'tag_commit',return_value='a'*40):
            self.assertEqual([r['tag'] for r in publisher.previous_releases('owner/repo','v0.3.2')],
                             self.matrix['preserve_releases'])

    def test_head_change_during_checks_fails_even_with_identical_clean_files(self):
        from subprocess import CompletedProcess
        with patch.object(incremental,'git',side_effect=[b'',b'old',b'',b'new']), \
             patch.object(incremental,'CHECKS',[['fixture-only']]), \
             patch.object(incremental.subprocess,'run',return_value=CompletedProcess([],0,'','')):
            with self.assertRaisesRegex(ValueError,'HEAD changed'):
                incremental.run_checks(ROOT)

    def test_verify_job_can_access_selected_intent_tag(self):
        # Regression for a skipped/missing uploaded receipt after successful readback.
        workflow=(ROOT/'.github/workflows/stable-release.yml').read_text()
        self.assertIn('needs: [intent, freeze, publish]',workflow)
        self.assertIn('path: run-record/${{ needs.intent.outputs.release_tag }}-publication.json',workflow)

    def test_unreviewed_critical_screen_or_missing_gate_fails(self):
        original=dist.read
        for field,value in [('known_unresolved_critical_findings',['defect']),
                            ('component_matrix_sha256','0'*64),('new_owner_responses_generated',1)]:
            def read(root,path):
                x=copy.deepcopy(original(root,path))
                if path==self.profile['critical_screen']: x[field]=value
                return x
            with self.subTest(field=field),patch.object(dist,'read',side_effect=read),self.assertRaises(ValueError):
                dist.validate_distribution(self.frozen,self.profile)
        p=copy.deepcopy(self.profile);p['readback_required']=False
        with self.assertRaises(ValueError):dist.validate_distribution(ROOT,p)


if __name__=='__main__':
    unittest.main()
