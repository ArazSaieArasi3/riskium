"""Build/check explicit bindings for the separate nature-task reader source."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
NS='documentation/0.4.4'
def build():
    paths=sorted(p.relative_to(ROOT).as_posix() for p in (ROOT/NS).rglob('*') if p.is_file() and p.name not in ('policy.json','component.json'))
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    policy=dict(schema='riskium-nature-reader-policy-v1',documentation_version='0.4.4',source_release='v0.3.6',development_distribution='v0.3.7',model_version='0.3.1',issue=66,channel_evidence='ACTUAL_OBSERVATIONS_SEPARATE_IN_ISSUE_66',files_sha256=hashes)
    text=json.dumps(policy,indent=2)+'\n'
    code=['tools/publication/nature_documentation.py','tools/publication/nature_main_gate.py','tools/publication/build_nature_reader_bindings.py','tests/test_nature_documentation.py','.github/workflows/released-reader-main.yml',
          'evaluation/documentation/nature-v0.3.7/README.md','evaluation/documentation/nature-v0.3.7/inputs/r3-completion.json']
    hashes=dict(hashes);hashes[NS+'/policy.json']=hashlib.sha256(text.encode()).hexdigest()
    hashes.update({p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in code})
    component=dict(schema='riskium-nature-reader-component-v1',id='DOCUMENTATION',version='0.4.4',compatible_model='0.3.1',published_source_release='v0.3.6',proposed_distribution='v0.3.7',execution_issue=66,shared_guides=21,native_wiki_files=23,maintained_html_pages=31,frozen_snapshots=4,prior_reader_source='765cb4507d925037cf82c1dc42bdea0a52bf9dca',files_sha256=hashes,new_source_distribution_published=False,independent_acceptance_claimed=False)
    return {NS+'/policy.json':text,NS+'/component.json':json.dumps(component,indent=2)+'\n'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    for name,text in build().items():
        path=ROOT/name
        if a.check:
            if path.read_text()!=text:raise ValueError('Reader binding drift: '+name)
        else:path.write_text(text)
    print(json.dumps(dict(status='NATURE_READER_BINDINGS_PASS',documentation='0.4.4')))
