"""Preserved inputs, selected snapshot/deployment and adversarial matrix controls."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build_prepared_distribution as prepared


class PreparedDistribution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        outputs = prepared.build()
        cls.original = json.loads(outputs[prepared.MATRIX])
        cls.original_overlay = json.loads(outputs[prepared.OVERLAY])

    def setUp(self):
        self.matrix = copy.deepcopy(self.original)
        self.overlay = copy.deepcopy(self.original_overlay)

    def validate(self, blob=prepared.read):
        return prepared.validate(self.matrix, self.overlay, blob)

    def changed(self, path, value):
        data = prepared.initial.encode(value).encode() if isinstance(value, (dict, list)) else value
        return lambda p: data if p == path else prepared.read(p)

    def snapshot(self):
        return next(r for r in self.matrix['artifacts'] if r['id'] == 'DOCUMENTATION_SNAPSHOT')

    def rebuild_union(self):
        supports = [dict(id='PREPARATION_INPUTS', files=[dict(path=p,sha256=h) for p,h in self.matrix['source_registers_sha256'].items()]),
                    dict(id='PUBLICATION_SUPPORT', files=[dict(path=p,sha256=h) for p,h in self.matrix['publication_support_sha256'].items()])]
        inventory, owners = prepared.initial.file_inventory(self.matrix['artifacts'] + supports,
            self.matrix['selection_tooling_sha256'], prepared.read)
        self.matrix['selected_files_sha256'], self.matrix['file_owners'] = inventory, owners

    def test_twenty_seven_original_rows_are_unchanged_and_exact_snapshot_is_added(self):
        result = self.validate()
        before = json.loads(prepared.archived('releases/selection-v0.3.4.json'))
        self.assertEqual(self.matrix['artifacts'][:27], before['artifacts'])
        self.assertEqual((result['components'], result['dependency_edges'], result['documentation_snapshots']), (28,61,4))
        self.assertEqual(len(self.snapshot()['files']), 82)
        self.assertEqual(self.snapshot()['version'], '0.1.0')

    def test_full_channel_and_publication_support_are_explicit_without_freshness_promotion(self):
        docs = self.matrix['documentation']
        self.assertEqual(len(docs['deployed_files_sha256']),311)
        self.assertEqual(len(docs['wiki_files_sha256']),23)
        self.assertEqual(len(self.matrix['publication_support_sha256']),5)
        self.assertEqual(docs['channel_evidence_status'],'RETAINED_CHECKPOINT_NOT_FINAL_SOURCE_FRESHNESS')
        for path in ['tools/publication/build_snapshot_site.py','.github/workflows/pages.yml','.github/workflows/documentation.yml']:
            self.assertIn(path,self.matrix['selected_files_sha256'])

    def test_missing_duplicate_or_wrong_version_components_are_rejected(self):
        for kind in ['missing','duplicate','wrong_version']:
            self.matrix=copy.deepcopy(self.original)
            if kind=='missing': self.matrix['artifacts'].pop()
            elif kind=='duplicate': self.matrix['artifacts'][-1]=copy.deepcopy(self.matrix['artifacts'][0])
            else: self.snapshot()['version']='0.2.0'
            with self.subTest(kind=kind),self.assertRaisesRegex(ValueError,'PREP-COMPONENTS'):
                self.validate()

    def test_incompatible_model_is_rejected(self):
        self.snapshot()['compatible_model']='0.4.0'
        with self.assertRaisesRegex(ValueError,'PREP-COMPATIBILITY'): self.validate()

    def test_unknown_wrong_duplicate_and_cyclic_dependencies_are_rejected(self):
        for kind in ['unknown','wrong_version','duplicate','cycle']:
            self.matrix=copy.deepcopy(self.original)
            if kind=='unknown': self.matrix['dependencies']['DOCUMENTATION_SNAPSHOT'][0]['id']='UNKNOWN'
            elif kind=='wrong_version': self.matrix['dependencies']['DOCUMENTATION_SNAPSHOT'][0]['version']='9.0.0'
            elif kind=='duplicate': self.matrix['dependencies']['DOCUMENTATION_SNAPSHOT'].append(copy.deepcopy(prepared.DEPS[0]))
            else: self.matrix['dependencies']['MODEL']=[dict(id='DOCUMENTATION_SNAPSHOT',version='0.1.0')]
            with self.subTest(kind=kind),self.assertRaises(ValueError): self.validate()

    def test_an_acyclic_silent_dependency_omission_is_rejected(self):
        self.matrix['dependencies']['DOCUMENTATION_SNAPSHOT'].pop()
        with self.assertRaisesRegex(ValueError,'PREP-DEPENDENCY-CONTRACT'): self.validate()

    def test_dependents_cannot_precede_their_prerequisites(self):
        self.matrix['artifacts'].reverse()
        with self.assertRaisesRegex(ValueError,'PREP-DEPENDENCY-ORDER'): self.validate()

    def test_a_receipt_cannot_be_lost_even_with_a_rebuilt_consistent_file_union(self):
        self.snapshot()['files']=[f for f in self.snapshot()['files'] if not f['path'].endswith('/software-tests.log')]
        self.rebuild_union()
        with self.assertRaisesRegex(ValueError,'PREP-ROW-CLOSURE'): self.validate()

    def test_shared_path_hash_conflicts_are_rejected(self):
        item=next(f for r in self.matrix['artifacts'] for f in r['files'] if len(self.matrix['file_owners'][f['path']])>1)
        item['sha256']='0'*64
        with self.assertRaises(ValueError): self.validate()

    def test_unsafe_paths_and_duplicate_file_entries_are_rejected(self):
        for path in ['../../private','/etc/passwd','.git/config','a\\b']:
            self.matrix=copy.deepcopy(self.original)
            self.snapshot()['files'][0]['path']=path
            with self.subTest(path=path),self.assertRaisesRegex(ValueError,'SEL-PATH'): self.validate()
        self.matrix=copy.deepcopy(self.original)
        self.snapshot()['files'].append(copy.deepcopy(self.snapshot()['files'][0]))
        with self.assertRaisesRegex(ValueError,'SEL-FILE-DUPLICATE'): self.validate()

    def test_union_inventory_or_owner_omissions_are_rejected(self):
        for field in ['selected_files_sha256','file_owners']:
            self.matrix=copy.deepcopy(self.original)
            self.matrix[field].pop(next(iter(self.matrix[field])))
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'PREP-INVENTORY'): self.validate()

    def test_preparation_tooling_cannot_be_omitted_even_after_rebuilding_the_union(self):
        self.matrix['selection_tooling_sha256'].pop('tools/build_prepared_distribution.py')
        self.rebuild_union()
        with self.assertRaisesRegex(ValueError,'PREP-SUPPORT-CLOSURE'): self.validate()

    def test_old_checkpoint_bytes_cannot_be_rehashed_or_relabelled(self):
        path='releases/selection-v0.3.4.json'
        with self.assertRaisesRegex(ValueError,'PREP-PRESERVED'):
            self.validate(self.changed(path,prepared.read(path)+b' '))

    def test_preserved_input_binding_cannot_be_removed_from_the_policy(self):
        policy=json.loads(prepared.read(prepared.POLICY))
        policy['preserved_inputs_sha256'].pop(next(iter(policy['preserved_inputs_sha256'])))
        self.matrix['policy_sha256']=prepared.initial.sha(prepared.initial.encode(policy).encode())
        with self.assertRaisesRegex(ValueError,'PREP-PRESERVED-SET'):
            self.validate(self.changed(prepared.POLICY,policy))

    def test_changed_snapshot_channel_receipts_are_rejected_by_exact_completion_hashes(self):
        path='evaluation/documentation/v0.3.4-snapshot/http-readback.json'
        value=json.loads(prepared.read(path));value['all_body_hashes_match']=False
        with self.assertRaisesRegex(ValueError,'PREP-RECEIPT-HASH'):
            self.validate(self.changed(path,value))

    def test_generated_version_index_or_frozen_snapshot_omissions_are_rejected(self):
        self.matrix['documentation']['generated_versions_index_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'PREP-DOCUMENTATION'): self.validate()
        self.matrix=copy.deepcopy(self.original)
        self.matrix['documentation']['frozen_snapshots'].pop('v0.3.1-rc.1')
        with self.assertRaisesRegex(ValueError,'PREP-DOCUMENTATION'): self.validate()

    def test_publication_support_cannot_be_dropped_even_with_consistent_hash_union(self):
        self.matrix['publication_support_sha256'].pop('docs/index.html')
        self.rebuild_union()
        with self.assertRaisesRegex(ValueError,'PREP-SUPPORT-CLOSURE'): self.validate()

    def test_prepared_matrix_cannot_claim_freeze_publication_or_independent_acceptance(self):
        self.matrix['stage']='FROZEN'
        with self.assertRaisesRegex(ValueError,'PREP-STAGE'): self.validate()
        for key in ['source_distribution_frozen_by_this_step','publication_requested_by_this_step','independent_validation_claimed']:
            self.matrix=copy.deepcopy(self.original)
            self.matrix['preparation_boundaries'][key]=True
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'PREP-SCIENTIFIC-SCOPE'): self.validate()

    def test_scientific_versions_and_future_freeze_gates_remain_explicit(self):
        self.matrix['scientific_versions']['model']='0.4.0'
        with self.assertRaisesRegex(ValueError,'PREP-SCIENTIFIC-SCOPE'): self.validate()
        self.matrix=copy.deepcopy(self.original);self.matrix['future_gates']=[]
        with self.assertRaisesRegex(ValueError,'PREP-FUTURE-GATES'): self.validate()

    def test_all_ten_releases_and_original_schema_chain_stay_preserved(self):
        self.assertEqual(len(self.matrix['preserve_releases']),10)
        self.assertEqual([r['to_schema'] for r in self.matrix['sqlite_migration_chain']],[2,3,4,5,6,7])
        self.matrix['preserve_releases'].pop()
        with self.assertRaisesRegex(ValueError,'PREP-PRESERVATION'): self.validate()

    def test_archived_initial_validation_does_not_certify_or_freeze_later_mutable_intent(self):
        for path in ['releases/stable-profiles.json','releases/stable-request.json']:
            with self.subTest(path=path):
                self.assertEqual(self.validate(self.changed(path,b'later independently validated release intent')),
                                 self.original['summary'])

    def test_overlay_cannot_omit_the_new_snapshot(self):
        self.overlay['components'].pop()
        with self.assertRaisesRegex(ValueError,'PREP-OVERLAY'): self.validate()


if __name__=='__main__':
    unittest.main()
