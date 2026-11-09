"""Source-bound reader tests and negative controls for B0-6."""
import copy,json,unittest
from unittest.mock import patch
import build_dictionary as build
import audit_dictionary as audit


class CandidateDictionary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files=build.build()
        cls.model,_=build.export.validate_contract(json.loads(build.export.CONTRACT.read_text()))
        cls.native=json.loads((build.export.HERE/'generated/candidate.ontouml.json').read_text())

    def test_complete_reader_and_all_local_routes(self):
        r=audit.audit(self.files,self.model)
        self.assertEqual((r['catalog_pages'],r['anchor_pages'],r['files']),(82,1,92))
        self.assertEqual((r['associations'],r['generalizations'],r['constraints']),(137,67,26))

    def test_generation_is_byte_deterministic(self):self.assertEqual(self.files,build.build())

    def test_native_boundaries_remain_notes(self):
        for c in self.model['concepts']:
            if c['scope_layer']!='FORMAL_CORE':
                self.assertIn('native representation:** `Note`',self.files[c['id']+'.md'])
                self.assertIn('not make it an exported typed-core class',self.files[c['id']+'.md'])

    def test_evidence_role_dependency_and_source_typing_survive(self):
        for cid in ['RKM-C066','RKM-C075','RKM-C076']:
            self.assertIn('RE-00',self.files[cid+'.md'])
            self.assertIn('Selected integration interpretation',self.files[cid+'.md'])
        self.assertIn('mandatory mediation',self.files['RKM-C066.md'])

    def test_exact_partition_rejects_duplicate_allocation(self):
        m=copy.deepcopy(self.model);m['domains'][0]['concept_ids'].append(m['domains'][1]['concept_ids'][0])
        with self.assertRaisesRegex(ValueError,'partition'):build.analyze(m,self.native)

    def test_unresolved_relation_is_rejected(self):
        m=copy.deepcopy(self.model);m['associations'][0]['target']='ABSENT'
        with self.assertRaisesRegex(ValueError,'endpoint'):build.analyze(m,self.native)

    def test_native_layer_drift_is_rejected(self):
        cid=next(c['id'] for c in self.model['concepts'] if c['scope_layer']!='FORMAL_CORE')
        n=copy.deepcopy(self.native);next(x for x in n['elements'] if x['id']==cid)['type']='Class'
        with self.assertRaisesRegex(ValueError,'layer mismatch'):build.analyze(self.model,n)

    def test_native_extra_mixed_set_is_rejected(self):
        n=copy.deepcopy(self.native);n['elements'].append({'id':'GS-RKM-C014','type':'GeneralizationSet'})
        with self.assertRaisesRegex(ValueError,'set-policy'):build.analyze(self.model,n)

    def test_missing_page_is_rejected(self):
        f=dict(self.files);del f['RKM-C075.md']
        with self.assertRaisesRegex(ValueError,'inventory'):audit.audit(f,self.model)

    def test_stale_page_is_rejected(self):
        f=dict(self.files);f['RKM-C075.md']+='stale'
        with self.assertRaisesRegex(ValueError,'hash mismatch'):audit.audit(f,self.model)

    def rehash(self,f,name):
        import hashlib
        manifest=json.loads(f['manifest.json']);manifest['files_sha256'][name]=hashlib.sha256(f[name].encode()).hexdigest();f['manifest.json']=build.dump(manifest)

    def test_broken_link_is_rejected_even_with_updated_hash(self):
        f=dict(self.files);f['README.md']+='\n[broken](ABSENT.md)\n';self.rehash(f,'README.md')
        with self.assertRaisesRegex(ValueError,'Broken reader link'):audit.audit(f,self.model)

    def test_definition_omission_is_rejected_even_with_updated_hash(self):
        f=dict(self.files);c=next(c for c in self.model['concepts'] if c['id']=='RKM-C075')
        f['RKM-C075.md']=f['RKM-C075.md'].replace(c['definition'],'Omitted.');self.rehash(f,'RKM-C075.md')
        with self.assertRaisesRegex(ValueError,'Definition/identity'):audit.audit(f,self.model)

    def test_pair_count_mutation_is_rejected_even_with_updated_hash(self):
        f=dict(self.files);s=json.loads(f['structural-binding.json']);s['association_pairs'][0]['relations']+=1
        f['structural-binding.json']=build.dump(s);self.rehash(f,'structural-binding.json')
        with self.assertRaisesRegex(ValueError,'pair accounting'):audit.audit(f,self.model)

    def test_source_status_and_riskcase_boundary_are_explicit(self):
        self.assertIn('source status is preserved verbatim',self.files['RKM-C001.md'])
        self.assertIn('issue #92',self.files['RKM-X01.md'])
        self.assertIn('external anchor',self.files['README.md'])

    def test_matrix_pair_position_mutation_is_rejected(self):
        f=dict(self.files);f['Subdomain-matrix.svg']=f['Subdomain-matrix.svg'].replace('data-source="D01" data-target="D03" data-count="1"','data-source="D01" data-target="D03" data-count="2"')
        self.assertNotEqual(f['Subdomain-matrix.svg'],self.files['Subdomain-matrix.svg']);self.rehash(f,'Subdomain-matrix.svg')
        with self.assertRaisesRegex(ValueError,'Matrix pair positions'):audit.audit(f,self.model)


if __name__=='__main__':unittest.main()
