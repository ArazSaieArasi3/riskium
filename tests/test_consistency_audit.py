"""Cross-document identity, provenance and acceptance regression oracles."""
from pathlib import Path
import importlib.util
import json
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('consistency',ROOT/'tools/audit_consistency.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)

class ConsistencyAudit(unittest.TestCase):
    def test_complete_join_retains_native_and_historical_denominators(self):
        data=json.loads(audit.build()['evaluation/consistency/traceability.json'])
        self.assertEqual(data['summary']['families'],{'REQUIREMENT':28,'MODEL':306,'MANUSCRIPT':65,'AMENDMENT':7,'RETAINED_CLAIM':12,'CORRECTION_REQUIREMENT':5})
        self.assertEqual(data['summary']['historical_hermit'],{'PASS':281,'NOT_RUN':14})
        self.assertEqual(data['summary']['historical_shacl'],{'PASS':341,'PARTIAL':1,'NOT_RUN':17})
        self.assertEqual(sum(r['family']=='MANUSCRIPT' and r['outcomes'][0]['disposition'].startswith('WITHDRAWN') for r in data['rows']),3)
        self.assertEqual(len({r['row_id'] for r in data['rows']}),423)
        self.assertTrue(all(not r['independent_acceptance'] for r in data['rows']))

    def test_missing_native_source_row_is_rejected(self):
        read=audit.read
        def changed(path):
            d=read(path)
            if path=='evaluation/relational/correction/mapping-accounting.json':d['rows'].pop()
            return d
        with patch.object(audit,'read',changed):
            with self.assertRaisesRegex(ValueError,'Native source denominator'):audit.build()

    def test_owner_scope_cannot_be_promoted_to_independent_acceptance(self):
        read=audit.read
        def changed(path):
            d=read(path)
            if path=='evaluation/owner-review/accepted-scope.json':d['independent_validation']=True
            return d
        with patch.object(audit,'read',changed):
            with self.assertRaisesRegex(ValueError,'Acceptance promoted'):audit.build()

    def test_lost_manuscript_claim_is_rejected(self):
        read=audit.read
        def changed(path):
            d=read(path)
            if path=='evaluation/manuscript-review/ledger.json':d['rows'].pop()
            return d
        with patch.object(audit,'read',changed):
            with self.assertRaisesRegex(ValueError,'Trace/claim denominator'):audit.build()

    def test_stale_source_binding_cannot_pass_the_join(self):
        sha=audit.sha
        with patch.object(audit,'sha',lambda p:'0'*64 if p=='ontology/riskium-model.json' else sha(p)):
            with self.assertRaisesRegex(ValueError,'Stale trace input'):audit.build()

if __name__=='__main__':unittest.main()
