"""Release selection trust boundaries; synthetic mutations are not publications."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build_release_selection as selection


class ReleaseSelection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = selection.build()
        cls.original_matrix = json.loads(cls.outputs[selection.MATRIX])
        cls.original_overlay = json.loads(cls.outputs[selection.OVERLAY])
        cls.policy = json.loads(selection.reader(selection.POLICY))

    def setUp(self):
        self.matrix = copy.deepcopy(self.original_matrix)
        self.overlay = copy.deepcopy(self.original_overlay)

    def validate(self):
        def read(path):
            return self.outputs[path].encode() if path in self.outputs else selection.reader(path)
        return selection.validate_selection(self.matrix, self.overlay, read)

    def row(self, ident):
        return next(r for r in self.matrix['artifacts'] if r['id'] == ident)

    def test_exact_twenty_seven_versions_dependencies_and_shared_file_owners(self):
        summary = self.validate()
        self.assertEqual((summary['components'], summary['retained'], summary['replaced'], summary['added']), (27, 22, 2, 3))
        self.assertEqual({r['id']: r['version'] for r in self.matrix['artifacts']},
                         {r['id']: r['version'] for r in self.policy['components']})
        self.assertGreater(max(map(len, self.matrix['file_owners'].values())), 1)

    def test_all_twenty_two_retained_component_rows_are_original_not_rehashed_versions(self):
        baseline = json.loads(selection.frozen('releases/distribution-v0.3.3.json'))
        for row in baseline['artifacts']:
            if row['id'] not in {'CONSISTENCY', 'DOCUMENTATION'}:
                with self.subTest(id=row['id']):
                    self.assertEqual(self.row(row['id']), row)

    def test_missing_and_duplicate_components_are_rejected(self):
        self.matrix['artifacts'].pop()
        with self.assertRaisesRegex(ValueError, 'SEL-COMPONENT-SET'):
            self.validate()
        self.matrix = copy.deepcopy(self.original_matrix)
        self.matrix['artifacts'][1] = copy.deepcopy(self.matrix['artifacts'][0])
        with self.assertRaisesRegex(ValueError, 'SEL-COMPONENT-SET'):
            self.validate()

    def test_wrong_selected_version_is_rejected(self):
        self.row('QUALIFIED_EVIDENCE')['version'] = '0.7.0'
        with self.assertRaisesRegex(ValueError, 'SEL-VERSION'):
            self.validate()

    def test_incompatible_model_and_promoted_acceptance_are_rejected(self):
        self.row('DOCUMENTATION')['compatible_model'] = '0.4.0'
        with self.assertRaisesRegex(ValueError, 'SEL-COMPATIBILITY'):
            self.validate()
        self.matrix = copy.deepcopy(self.original_matrix)
        self.matrix['boundaries']['independent_validation_claimed'] = True
        with self.assertRaisesRegex(ValueError, 'SEL-SCOPE'):
            self.validate()

    def test_a_missing_dependency_is_rejected_before_other_contract_checks(self):
        self.matrix['dependencies']['MODEL'] = [dict(id='UNKNOWN', version='1.0.0')]
        with self.assertRaisesRegex(ValueError, 'SEL-DEPENDENCY-MISSING'):
            self.validate()

    def test_wrong_dependency_version_is_rejected(self):
        self.matrix['dependencies']['QUALIFIED_EVIDENCE'][0]['version'] = '0.4.0'
        with self.assertRaisesRegex(ValueError, 'SEL-DEPENDENCY-VERSION'):
            self.validate()

    def test_duplicate_dependency_is_rejected(self):
        edge = self.matrix['dependencies']['QUALIFIED_EVIDENCE'][0]
        self.matrix['dependencies']['QUALIFIED_EVIDENCE'].append(copy.deepcopy(edge))
        with self.assertRaisesRegex(ValueError, 'SEL-DEPENDENCY-DUPLICATE'):
            self.validate()

    def test_actual_declared_cycle_is_rejected(self):
        self.matrix['dependencies']['MODEL'] = [dict(id='DOCUMENTATION', version='0.3.0')]
        with self.assertRaisesRegex(ValueError, 'SEL-DEPENDENCY-CYCLE'):
            self.validate()

    def test_dependents_cannot_precede_prerequisites(self):
        self.matrix['artifacts'].reverse()
        with self.assertRaisesRegex(ValueError, 'SEL-DEPENDENCY-ORDER'):
            self.validate()

    def test_a_silently_removed_prerequisite_is_rejected_even_if_graph_remains_acyclic(self):
        self.matrix['dependencies']['DOCUMENTATION'].pop(0)
        with self.assertRaisesRegex(ValueError, 'SEL-DEPENDENCY-CONTRACT'):
            self.validate()

    def test_unsafe_paths_are_rejected_before_file_access(self):
        for path in ('../../secret', '/etc/passwd', '.git/config', 'docs\\hidden', '.'):
            self.matrix = copy.deepcopy(self.original_matrix)
            self.matrix['artifacts'][0]['files'][0]['path'] = path
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'SEL-PATH'):
                self.validate()

    def test_duplicate_file_entries_are_not_silently_deduplicated(self):
        self.row('MODEL')['files'].append(copy.deepcopy(self.row('MODEL')['files'][0]))
        with self.assertRaisesRegex(ValueError, 'SEL-FILE-DUPLICATE'):
            self.validate()

    def test_shared_path_with_conflicting_hashes_is_rejected(self):
        row = self.row('DOCUMENTATION')
        item = next(f for f in row['files'] if len(self.matrix['file_owners'][f['path']]) > 1)
        item['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'SEL-FILE-CONFLICT'):
            self.validate()

    def test_a_forged_unique_file_hash_is_rejected(self):
        item = next(f for row in self.matrix['artifacts'] for f in row['files']
                    if len(self.matrix['file_owners'][f['path']]) == 1)
        item['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'SEL-FILE-HASH'):
            self.validate()

    def test_union_inventory_cannot_omit_a_selected_file(self):
        self.matrix['selected_files_sha256'].pop(next(iter(self.matrix['selected_files_sha256'])))
        with self.assertRaisesRegex(ValueError, 'SEL-INVENTORY'):
            self.validate()

    def test_receipt_omission_fails_even_after_rebuilding_a_consistent_file_union(self):
        row = self.row('QUALIFIED_EVIDENCE')
        row['files'] = [f for f in row['files'] if not f['path'].endswith('/software-tests.json')]
        read = lambda p: self.outputs[p].encode() if p in self.outputs else selection.reader(p)
        inventory, owners = selection.file_inventory(self.matrix['artifacts'], self.matrix['selection_tooling_sha256'], read)
        self.matrix['selected_files_sha256'], self.matrix['file_owners'] = inventory, owners
        with self.assertRaisesRegex(ValueError, 'SEL-DESCRIPTOR-CLOSURE'):
            self.validate()

    def test_consistency_keeps_exact_historical_rows_and_names_only_routing_metadata_changes(self):
        delta = json.loads(self.outputs[selection.DELTA])
        self.assertTrue(delta['rows_identical'])
        self.assertTrue(delta['historical_summary_unchanged'])
        self.assertEqual(delta['historical_rows'], 423)
        self.assertEqual(delta['changed_top_level_keys'], ['current_documentation', 'input_sha256', 'latest_published_distribution', 'planned_distribution'])
        current = json.loads(selection.reader('evaluation/consistency/traceability.json'))
        current['rows'].pop()
        def changed(path):
            return json.dumps(current).encode() if path == 'evaluation/consistency/traceability.json' else selection.reader(path)
        with self.assertRaisesRegex(ValueError, 'SEL-CONSISTENCY-ROWS'):
            selection.consistency_outputs(self.policy, changed)

    def test_consistency_cannot_promote_historical_summary_to_new_acceptance(self):
        current = json.loads(selection.reader('evaluation/consistency/traceability.json'))
        current['summary']['independent_ratings'] = 1
        def changed(path):
            return json.dumps(current).encode() if path == 'evaluation/consistency/traceability.json' else selection.reader(path)
        with self.assertRaisesRegex(ValueError, 'SEL-CONSISTENCY-METADATA'):
            selection.consistency_outputs(self.policy, changed)

    def test_historical_csv_cannot_drift_while_json_rows_stay_identical(self):
        def changed(path):
            data = selection.reader(path)
            return data + b'changed' if path == 'evaluation/consistency/traceability.csv' else data
        with self.assertRaisesRegex(ValueError, 'SEL-CONSISTENCY-CSV'):
            selection.consistency_outputs(self.policy, changed)

    def test_wrong_overlay_selection_is_rejected(self):
        self.overlay['components'].pop()
        with self.assertRaisesRegex(ValueError, 'SEL-OVERLAY'):
            self.validate()

    def test_sqlite_chain_pins_all_schemas_readers_and_ledger_hashes(self):
        chain = self.matrix['sqlite_migration_chain']
        self.assertEqual([r['to_schema'] for r in chain], [2, 3, 4, 5, 6, 7])
        self.assertEqual(chain[-1]['version'], '0.6.0')
        for row in chain:
            self.assertIn(row['reader'], self.matrix['selected_files_sha256'])
            self.assertTrue(row['schema_migration_ledger_sha256'])
        chain[-1]['from_schema'] = 5
        with self.assertRaisesRegex(ValueError, 'SEL-MIGRATION-CHAIN'):
            self.validate()

    def test_selection_cannot_claim_final_freeze_or_new_snapshot(self):
        self.matrix['stage'] = 'FROZEN'
        with self.assertRaisesRegex(ValueError, 'SEL-STAGE'):
            self.validate()
        self.matrix = copy.deepcopy(self.original_matrix)
        self.matrix['boundaries']['new_snapshot_registered'] = True
        with self.assertRaisesRegex(ValueError, 'SEL-SCOPE'):
            self.validate()

    def test_source_and_task_identity_cannot_be_relabelled(self):
        self.matrix['source_baseline'] = '0' * 40
        with self.assertRaisesRegex(ValueError, 'SEL-SOURCE-IDENTITY'):
            self.validate()
        self.matrix = copy.deepcopy(self.original_matrix)
        self.matrix['parent_issue'] = 99
        with self.assertRaisesRegex(ValueError, 'SEL-SELECTION-IDENTITY'):
            self.validate()

    def test_preserved_original_registers_cannot_be_silently_rehashed(self):
        def changed(path):
            data = self.outputs[path].encode() if path in self.outputs else selection.reader(path)
            return data + b' ' if path == 'releases/development-components.json' else data
        with self.assertRaisesRegex(ValueError, 'SEL-PRESERVED-REGISTER'):
            selection.validate_selection(self.matrix, self.overlay, changed)

    def test_the_validator_and_declared_policy_cannot_be_omitted_from_tooling_bindings(self):
        self.matrix['selection_tooling_sha256'].pop(selection.POLICY)
        with self.assertRaisesRegex(ValueError, 'SEL-TOOLING'):
            self.validate()

    def test_future_snapshot_freeze_and_readback_gates_cannot_disappear(self):
        self.matrix['future_gates'] = []
        with self.assertRaisesRegex(ValueError, 'SEL-FUTURE-GATES'):
            self.validate()

    def test_all_ten_prior_releases_stay_in_the_preservation_contract(self):
        self.assertEqual(self.matrix['preserve_releases'], ['v0.3.1-rc.' + str(n) for n in range(1, 8)] + ['v0.3.1', 'v0.3.2', 'v0.3.3'])
        self.matrix['preserve_releases'].remove('v0.3.3')
        with self.assertRaisesRegex(ValueError, 'SEL-RELEASE-PRESERVATION'):
            self.validate()


if __name__ == '__main__':
    unittest.main()
