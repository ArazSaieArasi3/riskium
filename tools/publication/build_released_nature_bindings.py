"""Bind the post-publication 0.4.5 reader without rewriting the released checkpoint."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NS = 'documentation/0.4.5'


def build():
    paths = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / NS).rglob('*')
                   if p.is_file() and p.name not in ('policy.json', 'component.json'))
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
    policy = dict(schema='riskium-released-nature-reader-policy-v1', documentation_version='0.4.5',
                  source_release='v0.3.7', development_distribution=None, model_version='0.3.1', issue=66,
                  channel_evidence='ACTUAL_OBSERVATIONS_SEPARATE_IN_ISSUE_66', files_sha256=hashes)
    text = json.dumps(policy, indent=2) + '\n'
    code = ['tools/publication/released_nature_documentation.py',
            'tools/publication/released_nature_main_gate.py',
            'tools/publication/build_released_nature_bindings.py',
            'tools/run_v037_versioned_suite.py', 'tests/test_released_nature_documentation.py',
            '.github/workflows/released-v037-reader.yml', '.github/workflows/v037-versioned-suite.yml']
    hashes = dict(hashes)
    hashes[NS + '/policy.json'] = hashlib.sha256(text.encode()).hexdigest()
    hashes.update({p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in code})
    component = dict(schema='riskium-released-nature-reader-component-v1', id='DOCUMENTATION', version='0.4.5',
                     compatible_model='0.3.1', published_source_release='v0.3.7', proposed_distribution=None,
                     execution_issue=66, shared_guides=21, native_wiki_files=23, maintained_html_pages=31,
                     frozen_snapshots=4, prior_reader_source='86accc6695e4738dd1337d5b9addd73b82c73c3d',
                     files_sha256=hashes, new_source_distribution_published=False, independent_acceptance_claimed=False)
    return {NS + '/policy.json': text, NS + '/component.json': json.dumps(component, indent=2) + '\n'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, text in build().items():
        path = ROOT / name
        if args.check:
            if path.read_text() != text:
                raise ValueError('Released reader binding drift: ' + name)
        else:
            path.write_text(text)
    print(json.dumps(dict(status='RELEASED_NATURE_READER_BINDINGS_PASS', documentation='0.4.5')))
