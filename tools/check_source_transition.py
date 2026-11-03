"""Qualify the documentation-only transition against its reviewed research source.

Frozen release tests execute in a detached worktree of BASELINE. Every unchanged
research file must be byte-identical in the candidate; current reader and new
manuscript experiments are checked separately by source-transition.yml.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '50f731aa5e065233c81fceeadaab8d87f5569de6'
PRE_PUBLICATION_SOURCE = '86accc6695e4738dd1337d5b9addd73b82c73c3d'
CURRENT_DOCUMENTS = {
    'README.md', 'evaluation/consistency/inventory.json',
}
SCHEDULERS = {
    '.github/workflows/documentation.yml',
    '.github/workflows/post-release-validation.yml',
    '.github/workflows/quality.yml',
    '.github/workflows/references.yml',
    '.github/workflows/requirements.yml',
    '.github/workflows/evidence-lifecycle.yml',

    '.github/workflows/current-alignment.yml',
    '.github/workflows/current-documentation.yml',
    '.github/workflows/release-support-v035.yml',
    '.github/workflows/release-selection-v035.yml',
    '.github/workflows/v036-versioned-suite.yml',
    '.github/workflows/v037-versioned-suite.yml',
    '.github/workflows/incremental-release.yml',
    '.github/workflows/stable-release.yml',
    '.github/workflows/release-v037.yml',
    '.github/workflows/published-documentation.yml',
    '.github/workflows/released-reader-main.yml',
    '.github/workflows/released-v037-reader.yml',
    '.github/workflows/pages.yml',
    '.github/workflows/publication-status.yml',
    '.github/workflows/current-documentation-pages.yml',
}
ADDITIVE_FILES = {
    '.github/workflows/subdomain-dictionary.yml',
    '.github/workflows/source-transition.yml',
    'tools/check_source_transition.py', 'tests/test_source_transition.py',
    'tools/audit_reader_consistency.py', 'tools/build_concept_dictionary.py',
    'tools/build_subdomain_relationships.py',
    'diagrams/subdomain-relationships.svg', 'diagrams/subdomain-relationships-matrix.svg',
    'docs/experiment-and-flow-inventory.md', 'docs/manuscript-and-release-roadmap.md',
    'docs/publication-consistency-checklist.md', 'docs/source-transition-validation.md',
    'references/followup-2026-11-03.json', 'references/followup-2026-11-03.md',
    'references/disposition-2026-11-04.md', 'references/full-pdf-update-2026-11-04.md',
    'tools/publication/dictionary_documentation.py', '.github/workflows/dictionary-reader.yml',
    'tests/test_dictionary_documentation.py',
}
ADDITIVE_PREFIXES = ('documentation/concepts/0.3.1/',
                     'evaluation/manuscript-review/v7.1.0/',
                     'evaluation/manuscript-review/v7.2.0/',
                     'evaluation/manuscript-review/v7.2.1/',
                     'evaluation/manuscript-review/v7.2.2/', 'evaluation/manuscript-review/v7.2.3/',
                     'documentation/0.4.6/', 'evaluation/documentation/dictionary-0.4.6/')


def require(value, message):
    if not value:
        raise ValueError(message)


def git(*args, root=ROOT):
    return subprocess.check_output(['git', *args], cwd=root)


def blob_digest(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def classify(path, old_digest, data):
    """Reject undeclared scientific changes rather than trusting an old replay."""
    require(data is not None, 'Deleted reviewed file: ' + path)
    if old_digest is not None:
        if blob_digest(data) == old_digest:
            return 'UNCHANGED_REVIEWED_SOURCE'
        require(path in CURRENT_DOCUMENTS or path in SCHEDULERS,
                'Research source changed; a new component qualification is required: ' + path)
        return 'CURRENT_READER_BINDING' if path in CURRENT_DOCUMENTS else 'CI_SCHEDULING'
    require(path in ADDITIVE_FILES or path.startswith(ADDITIVE_PREFIXES),
            'Unqualified added source: ' + path)
    return 'ADDITIVE_MANUSCRIPT_OR_READER'


def check(root=ROOT):
    root = Path(root)
    require(git('merge-base', BASELINE, 'HEAD', root=root).decode().strip() == BASELINE,
            'Candidate does not descend from the reviewed source')
    old = {}
    for item in git('ls-tree', '-rz', BASELINE, root=root).split(b'\0'):
        if item:
            meta, path = item.split(b'\t', 1)
            mode, kind, digest = meta.decode().split()
            require(kind == 'blob' and mode in ('100644', '100755'), 'Unsupported reviewed entry')
            old[path.decode()] = digest
    tracked = set(git('ls-files', '-z', root=root).decode().split('\0')) - {''}
    require(set(old) <= tracked, 'Reviewed source was removed from the candidate index')
    rows = []
    for name in sorted(set(old) | tracked):
        path = root / name
        require(not path.is_symlink(), 'Symlink in qualified source: ' + name)
        data = path.read_bytes() if path.is_file() else None
        disposition = classify(name, old.get(name), data)
        rows.append(dict(path=name, disposition=disposition,
                         candidate_sha256=hashlib.sha256(data).hexdigest(),
                         reviewed_blob=old.get(name)))
    return dict(status='DOCUMENTATION_SOURCE_TRANSITION_PASS',
                candidate_commit=git('rev-parse', 'HEAD', root=root).decode().strip(),
                historical_source=BASELINE,
                unchanged_reviewed_files=sum(r['disposition'] == 'UNCHANGED_REVIEWED_SOURCE' for r in rows),
                changed_reader_or_scheduler_files=[r['path'] for r in rows if r['disposition'] in ('CURRENT_READER_BINDING', 'CI_SCHEDULING')],
                rows=rows, scientific_model_changed=False, release_published=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--historical-worktree', type=Path)
    parser.add_argument('--historical-source', choices=(BASELINE, PRE_PUBLICATION_SOURCE), default=BASELINE)
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    receipt = check()
    receipt['historical_replay_source'] = args.historical_source
    if args.historical_worktree:
        target = args.historical_worktree.resolve()
        require(not target.exists(), 'Historical destination already exists')
        target.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'worktree', 'add', '--detach', str(target), args.historical_source],
                       cwd=ROOT, check=True, capture_output=True)
        require(git('rev-parse', 'HEAD', root=target).decode().strip() == args.historical_source,
                'Incorrect historical worktree')
        require(not git('status', '--porcelain', root=target).strip(), 'Dirty historical worktree')
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'rows'}))


if __name__ == '__main__':
    main()
