"""Bound N4 to additive documentary artifacts and two explicit planning updates."""
import argparse
import hashlib
import subprocess
from pathlib import Path
import curation

MUTABLE = {'plans/next-releases.md', 'evaluation/releases/v0.3.9/followups/issue85-structural-review/README.md'}
PREFIXES = ('tools/releases/v0310/', 'references/concept-definitions/0.2.0/',
            'documentation/0.4.10/reader/', 'evaluation/releases/v0.3.10/')
WORKFLOW = '.github/workflows/curation-v0310.yml'


def permitted_new(name):
    return name == WORKFLOW or name.startswith(PREFIXES)


def blob_hash(body):
    return hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()


def check(root=curation.ROOT):
    root = Path(root)
    raw = subprocess.check_output(['git', 'ls-tree', '-r', '-z', curation.BASELINE], cwd=root)
    baseline = {}
    for entry in raw.split(b'\0'):
        if not entry:
            continue
        meta, path = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        curation.need(kind == 'blob', 'Unexpected baseline object')
        baseline[path.decode()] = (mode, oid)
    preserved, changed = 0, []
    for name, (mode, oid) in baseline.items():
        p = root / name
        curation.need(p.is_file() and not p.is_symlink(), 'Missing or redirected historical file: ' + name)
        same = blob_hash(p.read_bytes()) == oid
        if name in MUTABLE:
            if not same:
                changed.append(name)
        else:
            curation.need(same, 'Frozen source/history changed: ' + name)
            curation.need(bool(p.stat().st_mode & 0o111) == (mode == '100755'), 'Frozen file mode changed: ' + name)
            preserved += 1
    # Include ignored files as well: no undeclared artifact is silently admitted.
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts}
    additions = actual - set(baseline)
    curation.need(all(permitted_new(n) for n in additions), 'Undeclared N4 paths: ' + ', '.join(sorted(n for n in additions if not permitted_new(n))))
    curation.need(not any(p.is_symlink() for prefix in PREFIXES for p in (root / prefix).rglob('*')), 'Redirected N4 artifact')
    return {'status': 'PASS_ADDITIVE_SOURCE_GUARD', 'baseline': curation.BASELINE,
            'frozen_files_preserved': preserved, 'allowed_planning_updates': sorted(changed),
            'new_files': len(additions)}


if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(curation.dump(check()))
