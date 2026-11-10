"""Guard the N5a candidate without modifying frozen scientific or N4 recipes."""
import hashlib
from pathlib import Path
import curation
import routing

MUTABLE = {'plans/next-releases.md', 'evaluation/releases/v0.3.9/followups/issue85-structural-review/README.md',
           'evaluation/releases/v0.3.10/README.md', routing.CURRENT}
NEW = ('tools/releases/v0310/', 'evaluation/releases/v0.3.10/')
FILES = {'releases/selection-v0.3.10.json', 'releases/routing-v0.3.10.json', '.github/workflows/publication-v0310.yml'}


def check():
    routed = routing.build(check=True)
    mutable = MUTABLE | {r['path'] for r in routed['workflows'] if r['role'] == 'LEGACY_REPLAY_OR_DISABLED_WRITE'}
    baseline = {}
    for row in routing.git('ls-tree', '-r', '-z', routing.BASELINE).split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            mode, kind, digest = meta.decode().split()
            curation.need(kind == 'blob', 'Unexpected baseline object')
            baseline[path.decode()] = (mode, digest)
    frozen = 0
    for name, (mode, digest) in baseline.items():
        p = curation.ROOT / name
        curation.need(p.is_file() and not p.is_symlink(), 'Missing/redirected baseline file: ' + name)
        if name not in mutable:
            body = p.read_bytes()
            actual = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
            curation.need(actual == digest, 'Frozen source/N4 evidence changed: ' + name)
            curation.need(bool(p.stat().st_mode & 0o111) == (mode == '100755'), 'Frozen file mode changed: ' + name)
            frozen += 1
    actual = {p.relative_to(curation.ROOT).as_posix() for p in curation.ROOT.rglob('*')
              if p.is_file() and '.git' not in p.relative_to(curation.ROOT).parts}
    additions = actual - set(baseline)
    curation.need(all(n in FILES or n.startswith(NEW) for n in additions), 'Undeclared candidate addition')
    curation.need(not any((curation.ROOT / n).is_symlink() for n in additions), 'Redirected candidate artifact')
    return {'status': 'PASS_N5A_ADDITIVE_BOUNDARY', 'baseline': routing.BASELINE,
            'frozen_files_preserved': frozen, 'new_files': len(additions), 'routed_workflows': len(mutable - MUTABLE),
            'scientific_source_changed': False, 'historical_oracles_changed': False}


if __name__ == '__main__':
    print(curation.dump(check()))
