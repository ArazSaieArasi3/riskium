"""Negative and preservation contracts for documentary publication preparation."""
import copy
import json
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
import curation
import guard
import projection
import reader


class CurationContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = curation.validate()

    def mutant(self, change):
        data = copy.deepcopy(self.data)
        change(data)
        with self.assertRaises(ValueError):
            curation.validate(data)

    def test_82_unique_source_bound_dispositions(self):
        self.assertEqual(len({r['concept_id'] for r in self.data['concepts']}), 82)
        self.assertEqual(self.data['summary']['dispositions'], curation.EXPECTED)

    def test_duplicate_disposition_rejected(self):
        self.mutant(lambda d: d['concepts'].__setitem__(0, copy.deepcopy(d['concepts'][1])))

    def test_authored_definition_change_rejected(self):
        self.mutant(lambda d: d['concepts'][0].__setitem__('authored_definition', 'Altered meaning'))

    def test_formal_equivalence_promotion_rejected(self):
        self.mutant(lambda d: d['concepts'][0].__setitem__('formal_alignment', 'EQUIVALENT'))

    def test_independent_rating_promotion_rejected(self):
        self.mutant(lambda d: d['concepts'][0].__setitem__('independent_validation', 'PASSED'))

    def test_normative_deferral_cannot_become_inspected_term(self):
        def change(d):
            row = next(r for r in d['concepts'] if r['concept_id'] in curation.DEFERRED)
            row['normative_term_text_inspected'] = True
            row['exact_normative_mapping_adopted'] = True
        self.mutant(change)

    def test_packet_access_cannot_be_flattened(self):
        def change(d):
            p = next(p for p in d['packets'].values() if 'nist' in p['sources'])
            p['sources']['nist']['inspection_scope'] = 'Entire source freshly validated'
        self.mutant(change)

    def test_all_four_scientific_sections_preserved(self):
        def section(text, heading):
            return re.split(r'\n## ', text.split('## ' + heading + '\n', 1)[1], maxsplit=1)[0].strip()
        for row in self.data['concepts']:
            name = row['concept_id'] + '.md'
            before = (curation.BASE_READER / name).read_text()
            after = (reader.OUT / name).read_text()
            for heading in ('Authored source definition', 'Identity and source typing', 'Direct catalog associations', 'Direct inheritance'):
                self.assertEqual(section(before, heading), section(after, heading), (name, heading))

    def test_foundations_separate_from_domain_comparison(self):
        rows = [r for r in self.data['concepts'] if r.get('foundation_term_ids')]
        self.assertTrue(rows)
        for row in rows:
            self.assertIn('Modeling foundations, separate from the domain comparison', reader.section(row, self.data))

    def test_three_deferrals_explicit_in_reader(self):
        for cid in curation.DEFERRED:
            text = (reader.OUT / (cid + '.md')).read_text()
            self.assertIn('Normative mapping deferred', text)
            self.assertIn('/issues/78', text)
            self.assertIn('no exact normative term wording or clause is asserted', text)

    def test_added_evidence_reference_role_preserved(self):
        text = (reader.OUT / 'RKM-C065.md').read_text()
        self.assertIn('RKM-C076', text)

    def test_source_guard_scope(self):
        self.assertFalse(guard.permitted_new('ontology/0.3.3/changed.json'))
        self.assertFalse(guard.permitted_new('implementation/relational/1.0/schema.sql'))
        self.assertTrue(guard.permitted_new('documentation/0.4.10/reader/README.md'))
        self.assertNotIn('ontology/0.3.2/riskium-model.json', guard.MUTABLE)

    def test_source_guard_rejects_changed_or_deleted_historical_body(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            p = root / 'ontology/0.3.2/model.json'
            p.parent.mkdir(parents=True)
            p.write_bytes(b'preserved')
            tree = ('100644 blob ' + guard.blob_hash(b'preserved') + '\tontology/0.3.2/model.json\0').encode()
            with patch.object(guard.subprocess, 'check_output', return_value=tree):
                self.assertEqual(guard.check(root)['frozen_files_preserved'], 1)
                p.write_bytes(b'changed')
                with self.assertRaisesRegex(ValueError, 'Frozen source/history changed'):
                    guard.check(root)
                p.unlink()
                with self.assertRaisesRegex(ValueError, 'Missing or redirected'):
                    guard.check(root)


class ProjectionContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.base = Path(cls.tmp.name) / 'base'
        cls.result = projection.build(cls.base, curation.BASELINE)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def setUp(self):
        self.work = Path(self.tmp.name) / self._testMethodName
        shutil.copytree(self.base, self.work)

    def update_hash(self, name):
        path = self.work / 'projection-manifest.json'
        m = curation.load(path)
        m['files_sha256'][name] = curation.sha((self.work / name).read_bytes())
        path.write_text(curation.dump(m))

    def test_all_91_bodies_and_local_links(self):
        self.assertEqual(self.result['paired_bodies'], 91)
        self.assertEqual(self.result['wiki_pages'], 94)
        self.assertGreater(self.result['local_links_checked'], 5000)
        self.assertFalse(self.result['published'])

    def test_extra_projection_file_rejected(self):
        (self.work / 'extra.txt').write_text('undeclared')
        with self.assertRaisesRegex(ValueError, 'inventory'):
            projection.audit(self.work)

    def test_missing_projection_file_rejected(self):
        (self.work / 'wiki/RKM-C065.md').unlink()
        with self.assertRaisesRegex(ValueError, 'inventory'):
            projection.audit(self.work)

    def test_broken_link_rejected_even_with_updated_file_hash(self):
        name = 'site/current/concepts/index.html'
        p = self.work / name
        p.write_text(p.read_text().replace('href="Subdomains.html"', 'href="Missing.html"', 1))
        self.update_hash(name)
        with self.assertRaisesRegex(ValueError, 'Broken staged route'):
            projection.audit(self.work)

    def test_broken_anchor_rejected_even_with_updated_file_hash(self):
        name = 'site/current/concepts/index.html'
        p = self.work / name
        p.write_text(p.read_text().replace('href="Subdomains.html"', 'href="Subdomains.html#no-such-subdomain"', 1))
        self.update_hash(name)
        with self.assertRaisesRegex(ValueError, 'Broken staged anchor'):
            projection.audit(self.work)

    def test_wiki_text_drift_rejected_even_with_updated_file_hash(self):
        name = 'wiki/RKM-C065.md'
        p = self.work / name
        p.write_text(p.read_text().replace('## Current documentary comparisons', '## Unsupported semantic claim', 1))
        self.update_hash(name)
        with self.assertRaisesRegex(ValueError, 'text parity'):
            projection.audit(self.work)

    def test_premature_publication_claim_rejected(self):
        p = self.work / 'projection-manifest.json'
        m = curation.load(p)
        m['published'] = True
        p.write_text(curation.dump(m))
        with self.assertRaisesRegex(ValueError, 'Premature publication'):
            projection.audit(self.work)


if __name__ == '__main__':
    unittest.main(verbosity=2)
