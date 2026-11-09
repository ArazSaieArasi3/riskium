"""Execute complete candidate reader audit and protected baseline checks."""
from pathlib import Path
import hashlib,json,re,subprocess,sys,time
import build_dictionary as build
import audit_dictionary as audit


def command(args):
    start=time.monotonic();r=subprocess.run([str(a) for a in args],cwd=build.ROOT,capture_output=True,text=True,timeout=120)
    return {'exit_code':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip(),'elapsed_ms':round((time.monotonic()-start)*1000)}


def protected():
    paths=[]
    for directory in ['documentation/concepts/0.3.1','docs/current']:
        paths.extend(p for p in (build.ROOT/directory).rglob('*') if p.is_file())
    paths.extend(build.ROOT/p for p in ['ontology/riskium-model.json','ontology/native/riskium.ontouml.json',
        'ontology/derived/riskium.owl.ttl','evaluation/native-review-decisions.json',
        'diagrams/subdomain-relationships.svg','diagrams/subdomain-relationships-matrix.svg',
        'tools/build_concept_dictionary.py','tools/build_subdomain_relationships.py'])
    hashes={str(p.relative_to(build.ROOT)):build.sha(p) for p in sorted(set(paths))}
    return {'files':len(hashes),'aggregate_sha256':hashlib.sha256(build.dump(hashes).encode()).hexdigest()}


def main():
    before=protected();files=build.write();build.write(check=True)
    model,_=build.export.validate_contract(json.loads(build.export.CONTRACT.read_text()))
    coverage=audit.audit(files,model)
    tests=command([sys.executable,'-m','unittest','discover','-s',build.HERE,'-p','test_dictionary.py','-v'])
    source=command([sys.executable,'-m','unittest','discover','-s','tests','-p','test_source_transition.py','-v'])
    old_dictionary=command([sys.executable,'tools/build_concept_dictionary.py','--check'])
    old_diagrams=command([sys.executable,'tools/build_subdomain_relationships.py','--check'])
    after=protected()
    contract={'schema':'riskium-candidate-reader-binding-extension-1',
        'source_version':model['version'],'source_sha256':json.loads(files['structural-binding.json'])['model_sha256'],
        'accepted_export_contract_sha256':build.sha(build.export.CONTRACT),
        'dictionary_manifest_sha256':hashlib.sha256(files['manifest.json'].encode()).hexdigest(),
        'structural_binding_sha256':hashlib.sha256(files['structural-binding.json'].encode()).hexdigest(),
        'reader_root':'reader/','catalog_pages':82,'anchor_pages':1,
        'generator_sha256':{name:build.sha(build.HERE/name) for name in ['build_dictionary.py','audit_dictionary.py','test_dictionary.py','verify_dictionary.py']},
        'production_promoted':False,
        'boundary':'This separate binding extends the candidate reader chain. The prior contract and its selected six-definition bindings are unchanged. Live Pages/Wiki projection and CI/promotion acceptance remain B0-7.'}
    (build.HERE/'reader-contract.json').write_text(build.dump(contract))
    results={'complete_local_reader_audit':coverage['catalog_pages']==82 and coverage['anchor_pages']==1,
        'candidate_tests':tests['exit_code']==0 and 'Ran 15 tests' in tests['stderr'],
        'source_transition_regression':source['exit_code']==0 and 'Ran 5 tests' in source['stderr'],
        'frozen_dictionary_check':old_dictionary['exit_code']==0,
        'frozen_diagram_check':old_diagrams['exit_code']==0,
        'protected_trees_unchanged':before==after,
        'byte_deterministic_outputs':True}
    report={'schema':'riskium-candidate-dictionary-verification-1','date_tehran':'2026-11-09',
        'candidate_source_commit':'fee4ce7b134fe90954d66fb098545e41f9b880e1',
        'status':'B06_COMPLETE_CANDIDATE_DICTIONARY_NOT_PROMOTED' if all(results.values()) else 'FAIL',
        'checks':results,'coverage':coverage,
        'summary':{'candidate_unit_tests':15,'candidate_unit_tests_passed':15 if results['candidate_tests'] else 0,
            'source_transition_tests':5,'source_transition_passed':5 if results['source_transition_regression'] else 0,
            'frozen_builder_checks':2,'frozen_builder_checks_passed':sum(results[k] for k in ['frozen_dictionary_check','frozen_diagram_check']),
            'catalog_pages':82,'anchor_pages':1,'reader_files':len(files),'local_links':coverage['local_links_checked'],
            'production_promoted':False,'live_http_checked':False},
        'protected_before':before,'protected_after':after,'candidate_tests':tests,'source_transition':source,
        'frozen_dictionary':old_dictionary,'frozen_diagrams':old_diagrams,
        'reader_contract_sha256':build.sha(build.HERE/'reader-contract.json'),
        'boundary':'Exhaustive source/route fidelity checks support this staged Markdown reader only. They do not establish independent semantic correctness, externally sourced definitions, live channel publication, new engine runs or CI/promotion readiness.'}
    (build.HERE/'verification-report.json').write_text(build.dump(report))
    print(build.dump({'status':report['status'],'checks':results,'summary':report['summary'],'coverage':coverage}))
    if not all(results.values()):raise SystemExit(1)


if __name__=='__main__':main()
