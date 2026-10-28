"""Actual v0.3.5 source selection and meaningful corrupt-input boundaries."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import select_release_v035 as selection


class Release035Selection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = selection.build()
        cls.original_matrix = json.loads(cls.outputs[selection.MATRIX])
        cls.original_overlay = json.loads(cls.outputs[selection.OVERLAY])
        cls.policy = json.loads(selection.reader(selection.POLICY))

    def setUp(self):
        self.matrix = copy.deepcopy(self.original_matrix)
        self.overlay = copy.deepcopy(self.original_overlay)

    def validate(self, read=selection.reader):
        return selection.validate_selection(self.matrix, self.overlay, read)

    def row(self, ident):
        return next(r for r in self.matrix['artifacts'] if r['id'] == ident)

    def rebuild_union(self):
        files, owners = selection.shared.file_inventory(self.matrix['artifacts'], self.matrix['selection_tooling_sha256'], selection.reader)
        self.matrix['selected_files_sha256'], self.matrix['file_owners'] = files, owners

    def test_actual_twenty_nine_versions_complete_file_closure_and_schema_eight(self):
        summary = self.validate()
        self.assertEqual((summary['components'], summary['retained'], summary['replaced'], summary['added']), (29, 26, 2, 1))
        self.assertEqual([r['to_schema'] for r in self.matrix['sqlite_migration_chain']], [2, 3, 4, 5, 6, 7, 8])
        report = json.loads(selection.reader('evaluation/consistency/current-0.3.0/report.json'))
        self.assertLessEqual(set(report['input_sha256']), set(self.matrix['selected_files_sha256']))
        self.assertEqual(self.matrix['generated_outputs']['source_commit'], '1f8610657b3d9ab3c50589d3d76be7cffd8c7099')

    def test_retained_rows_and_snapshot_generation_are_not_silently_rewritten(self):
        old = json.loads(selection.frozen(selection.BASE_MATRIX))
        for row in old['artifacts']:
            if row['id'] not in selection.REPLACED:
                self.assertEqual(row, self.row(row['id']))
        self.assertEqual(self.matrix['historical_generation_components'], [r for ident in ('DOCUMENTATION', 'CONSISTENCY') for r in old['artifacts'] if r['id'] == ident])
        self.assertEqual(self.matrix['historical_generation_dependencies']['DOCUMENTATION_SNAPSHOT'], old['dependencies']['DOCUMENTATION_SNAPSHOT'])
        self.assertEqual(self.matrix['dependencies']['DOCUMENTATION_SNAPSHOT'], [{'id': 'MODEL', 'version': '0.3.1'}])

    def test_missing_and_duplicate_component_rejected(self):
        self.matrix['artifacts'].pop()
        with self.assertRaisesRegex(ValueError, 'V035-COMPONENT-SET'):
            self.validate()
        self.matrix = copy.deepcopy(self.original_matrix)
        self.matrix['artifacts'][-1] = copy.deepcopy(self.matrix['artifacts'][0])
        with self.assertRaisesRegex(ValueError, 'V035-COMPONENT-SET'):
            self.validate()

    def test_wrong_current_component_version_and_model_rejected(self):
        self.row('EVIDENCE_REFERENCE_LIFECYCLE')['version'] = '0.6.0'
        with self.assertRaisesRegex(ValueError, 'SEL-DEPENDENCY-VERSION'):
            self.validate()
        self.matrix = copy.deepcopy(self.original_matrix)
        self.row('DOCUMENTATION')['compatible_model'] = '0.4.0'
        with self.assertRaisesRegex(ValueError, 'V035-COMPATIBILITY'):
            self.validate()

    def test_missing_wrong_duplicate_and_cyclic_dependencies_rejected(self):
        mutations = [
            ('SEL-DEPENDENCY-MISSING', lambda g: g['MODEL'].append({'id': 'UNKNOWN', 'version': '1.0.0'})),
            ('SEL-DEPENDENCY-VERSION', lambda g: g['EVIDENCE_REFERENCE_LIFECYCLE'][0].update(version='0.5.0')),
            ('SEL-DEPENDENCY-DUPLICATE', lambda g: g['EVIDENCE_REFERENCE_LIFECYCLE'].append(copy.deepcopy(g['EVIDENCE_REFERENCE_LIFECYCLE'][0]))),
            ('SEL-DEPENDENCY-CYCLE', lambda g: g['MODEL'].append({'id': 'DOCUMENTATION', 'version': '0.4.0'})),
        ]
        for message, change in mutations:
            with self.subTest(message=message):
                self.matrix = copy.deepcopy(self.original_matrix)
                change(self.matrix['dependencies'])
                with self.assertRaisesRegex(ValueError, message):
                    self.validate()

    def test_acyclic_silent_dependency_removal_and_wrong_assembly_order_rejected(self):
        self.matrix['dependencies']['DOCUMENTATION'].pop()
        with self.assertRaisesRegex(ValueError, 'V035-DEPENDENCY-CONTRACT'):
            self.validate()
        self.matrix = copy.deepcopy(self.original_matrix)
        self.matrix['artifacts'].reverse()
        with self.assertRaisesRegex(ValueError, 'V035-DEPENDENCY-ORDER'):
            self.validate()

    def test_duplicate_and_unsafe_component_paths_rejected(self):
        self.row('MODEL')['files'].append(copy.deepcopy(self.row('MODEL')['files'][0]))
        with self.assertRaisesRegex(ValueError, 'SEL-FILE-DUPLICATE'):
            self.validate()
        self.matrix = copy.deepcopy(self.original_matrix)
        self.row('MODEL')['files'][0]['path'] = '../secret'
        with self.assertRaisesRegex(ValueError, 'SEL-PATH'):
            self.validate()

    def test_conflicting_shared_hash_and_forged_unique_hash_rejected(self):
        shared = next(f for r in self.matrix['artifacts'] for f in r['files'] if len(self.matrix['file_owners'][f['path']]) > 1)
        shared['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'SEL-FILE-CONFLICT'):
            self.validate()
        self.matrix = copy.deepcopy(self.original_matrix)
        unique = next(f for r in self.matrix['artifacts'] for f in r['files'] if len(self.matrix['file_owners'][f['path']]) == 1)
        unique['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'SEL-FILE-HASH'):
            self.validate()

    def test_hash_union_cannot_omit_current_source_input(self):
        self.matrix['selected_files_sha256'].pop('tools/relational_evidence_lifecycle.py')
        with self.assertRaisesRegex(ValueError, 'V035-INVENTORY'):
            self.validate()

    def test_omitted_descriptor_file_rejected_even_after_coherent_union_rebuild(self):
        row = self.row('EVIDENCE_REFERENCE_LIFECYCLE')
        row['files'] = [f for f in row['files'] if not f['path'].endswith('/software-tests.log')]
        self.rebuild_union()
        with self.assertRaisesRegex(ValueError, 'V035-DESCRIPTOR-CLOSURE'):
            self.validate()

    def test_historical_snapshot_cannot_be_rebound_to_new_documentation(self):
        self.matrix['historical_generation_dependencies']['DOCUMENTATION_SNAPSHOT'][-1]['version'] = '0.4.0'
        with self.assertRaisesRegex(ValueError, 'V035-HISTORICAL-GENERATION'):
            self.validate()

    def test_generated_outputs_cannot_point_at_old_source_bytes(self):
        self.matrix['generated_outputs']['current_files_sha256']['guide/Home.html'] = selection.sha(selection.reader('docs/current/guide/Home.html'))
        with self.assertRaisesRegex(ValueError, 'V035-GENERATED-OUTPUTS'):
            self.validate()

    def test_policy_cannot_omit_an_older_frozen_snapshot_file(self):
        policy = copy.deepcopy(self.policy)
        policy['frozen_snapshot_files_sha256'].pop(next(iter(policy['frozen_snapshot_files_sha256'])))
        with self.assertRaisesRegex(ValueError, 'V035-SNAPSHOT-INVENTORY'):
            selection.current_rows(policy, selection.reader)

    def test_wrong_source_http_receipt_rejected_even_before_current_file_selection(self):
        policy = copy.deepcopy(self.policy)
        spec = next(r for r in policy['descriptor_components'] if r['id'] == 'DOCUMENTATION')
        desc = json.loads(selection.reader(spec['descriptor']))
        path = policy['current_documentation_receipts']['http']
        receipt = json.loads(selection.reader(path))
        receipt['source_commit'] = '0' * 40
        def changed(p):
            return json.dumps(receipt).encode() if p == path else selection.reader(p)
        with self.assertRaisesRegex(ValueError, 'V035-CHANNEL-SOURCE'):
            selection.generated_outputs(policy, changed, desc)

    def test_substituted_current_executable_cannot_reuse_selected_receipts(self):
        def changed(path):
            return b'# substituted executable\n' if path == 'tools/relational_evidence_lifecycle.py' else selection.reader(path)
        with self.assertRaisesRegex(ValueError, 'SEL-FILE-HASH'):
            self.validate(changed)

    def test_stale_descriptor_hash_cannot_be_hidden_by_correct_report_hash(self):
        policy = copy.deepcopy(self.policy)
        spec = next(r for r in policy['descriptor_components'] if r['id'] == 'EVIDENCE_REFERENCE_LIFECYCLE')
        descriptor = json.loads(selection.reader(spec['descriptor']))
        descriptor['files_sha256']['tools/relational_evidence_lifecycle.py'] = '0' * 64
        encoded = json.dumps(descriptor).encode()
        spec['descriptor_sha256'] = selection.sha(encoded)
        def changed(path):
            return encoded if path == spec['descriptor'] else selection.reader(path)
        with self.assertRaisesRegex(ValueError, 'V035-STALE: tools/relational_evidence_lifecycle.py'):
            selection.checked_descriptor(spec, changed)

    def test_lifecycle_same_pass_count_cannot_hide_wrong_profile_or_predecessor(self):
        descriptor = json.loads(selection.reader('implementation/relational/0.7.0/component.json'))
        report = json.loads(selection.reader('evaluation/relational/evidence-lifecycle/report.json'))
        report['profile'] = '0.6.0'
        with self.assertRaisesRegex(ValueError, 'V035-LIFECYCLE-SCOPE'):
            selection.check_lifecycle_metadata(descriptor, report)
        report = json.loads(selection.reader('evaluation/relational/evidence-lifecycle/report.json'))
        descriptor['baseline_sql_profile'] = '0.5.0'
        with self.assertRaisesRegex(ValueError, 'V035-LIFECYCLE-SCOPE'):
            selection.check_lifecycle_metadata(descriptor, report)

    def test_selection_cannot_claim_freeze_publication_or_independent_acceptance(self):
        self.matrix['stage'] = 'FROZEN'
        with self.assertRaisesRegex(ValueError, 'V035-STAGE'):
            self.validate()
        self.matrix = copy.deepcopy(self.original_matrix)
        self.matrix['boundaries']['independent_validation_claimed'] = True
        with self.assertRaisesRegex(ValueError, 'V035-SCOPE'):
            self.validate()


if __name__ == '__main__':
    unittest.main()
