"""Stable publication boundaries: exact scope, check completeness and immutable assets."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import prepare_stable_release as stable
import publish_stable_release as publication


class StableProfile(unittest.TestCase):
    def changed(self, path, mutate):
        original = stable.read
        def replacement(root, name):
            value = copy.deepcopy(original(root, name))
            if name == path:
                mutate(value)
            return value
        return patch.object(stable, 'read', side_effect=replacement)

    def test_stable_profile_matches_owner_accepted_components(self):
        self.assertEqual(stable.validate_profile(ROOT)['tag'], 'v0.3.1')

    def test_mismatched_model_tag_and_missing_gate_are_rejected(self):
        for mutation in [lambda x:x.update(tag='v0.3.2'), lambda x:x.update(model_version='0.4.0'), lambda x:x.update(readback_required=False)]:
            with self.subTest(mutation=mutation), self.changed(stable.PROFILE, mutation), self.assertRaises(ValueError):
                stable.validate_profile(ROOT)

    def test_critical_finding_and_unreviewed_scientific_change_block_release(self):
        for mutation in [lambda x:x.update(known_unresolved_critical_findings=['identity collapse']), lambda x:x.update(material_scientific_change_since_owner_acceptance=True)]:
            with self.subTest(mutation=mutation), self.changed('evaluation/finalization/v0.3.1-review.json', mutation), self.assertRaises(ValueError):
                stable.validate_profile(ROOT)

    def test_generic_or_missing_owner_acceptance_is_not_enough(self):
        with self.changed('evaluation/owner-review/register.json', lambda x:x.update(ratings_recorded=0)), self.assertRaises(ValueError):
            stable.validate_profile(ROOT)

    def test_missing_wrong_or_failed_checks_cannot_form_a_freeze(self):
        good = [{'command':['python', *args], 'exit_code':0} for args in stable.CHECKS]
        for checks in [[], good[:-1], list(reversed(good)), [{**c, 'exit_code':1 if i==0 else 0}for i,c in enumerate(good)]]:
            with self.subTest(count=len(checks)), self.assertRaises(ValueError):
                stable.validate_checks(checks)
        stable.validate_checks(good)

    def test_dirty_checkout_and_wrong_ref_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            subprocess.run(['git','init','-q',folder],check=True)
            (root/'pending').write_text('unreviewed')
            with self.assertRaisesRegex(ValueError,'clean source'):
                stable.ensure_clean(root)
        with patch.object(stable,'git',side_effect=[b'',b'older\n',b'HEAD\n']), self.assertRaisesRegex(ValueError,'exact HEAD'):
            stable.ensure_clean(ROOT,'older')

    def test_existing_tag_or_release_is_never_overwritten(self):
        for existing in ['git/ref/tags/v0.3.1','releases/tags/v0.3.1']:
            def getter(repo,path,missing_ok=False):return []if path=='releases?per_page=100' else ({'id':123}if path==existing else None)
            with self.subTest(existing=existing),self.assertRaisesRegex(ValueError,'never overwritten'):
                publication.assert_new('owner/repo',getter)
        publication.assert_new('owner/repo',lambda repo,path,**k:[]if path=='releases?per_page=100' else None)
        with self.assertRaisesRegex(ValueError,'draft stable release'):
            publication.assert_new('owner/repo',lambda repo,path,**k:[{'tag_name':'v0.3.1','draft':True}]if path=='releases?per_page=100' else None)

    def test_api_errors_fail_closed_instead_of_becoming_missing_tags(self):
        failed=subprocess.CompletedProcess([],1,'','HTTP 403 rate limited')
        with patch.object(publication.subprocess,'run',return_value=failed),self.assertRaisesRegex(ValueError,'failed closed'):
            publication.api('owner/repo','git/ref/tags/v0.3.1',missing_ok=True)
        missing=subprocess.CompletedProcess([],1,'','HTTP 404 not found')
        with patch.object(publication.subprocess,'run',return_value=missing):
            self.assertIsNone(publication.api('owner/repo','git/ref/tags/v0.3.1',missing_ok=True))

    def test_incomplete_asset_set_cannot_be_published(self):
        with tempfile.TemporaryDirectory()as folder:
            (Path(folder)/'freeze-receipt.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'Missing or unexpected'):
                publication.validate_package(folder,'0'*40)

    def test_changed_request_publishes_and_unrelated_later_push_does_not(self):
        with tempfile.TemporaryDirectory()as folder:
            root=Path(folder);subprocess.run(['git','init','-q',folder],check=True)
            (root/'releases').mkdir()
            def commit():
                subprocess.run(['git','-C',folder,'add','.'],check=True)
                subprocess.run(['git','-C',folder,'-c','user.name=Release Test','-c','user.email=release-test@example.invalid','commit','-qm','fixture'],check=True)
                return stable.git(root,'rev-parse','HEAD').decode().strip()
            (root/stable.REQUEST).write_text(json.dumps({'profile':'stable-bounded-research-artifact','tag':'v0.3.1','publish':False}))
            before=commit()
            (root/stable.REQUEST).write_text(json.dumps({'profile':'stable-bounded-research-artifact','tag':'v0.3.1','publish':True}))
            after=commit()
            self.assertEqual(stable.resolve_intent(root,'push','refs/heads/main',before,after),{'publish':True,'release_tag':'v0.3.1'})
            (root/'ordinary-doc').write_text('documentation maintenance');later=commit()
            self.assertEqual(stable.resolve_intent(root,'push','refs/heads/main',after,later),{'publish':False,'release_tag':''})

    def test_manual_stable_intent_rejects_prerelease_or_wrong_branch(self):
        for ref,tag in [('refs/heads/topic','v0.3.1'),('refs/heads/main','v0.3.1-rc.8'),('refs/heads/main','v0.3.1\npublish=true')]:
            with self.subTest(ref=ref,tag=tag),self.assertRaises(ValueError):
                stable.resolve_intent(ROOT,'workflow_dispatch',ref,'','0'*40,{'publish':True,'release_tag':tag})


if __name__=='__main__':
    unittest.main()
