"""Build a version-bound reader using the reviewed exhaustive dictionary renderer."""
from pathlib import Path
from types import SimpleNamespace
import hashlib, json, os, re, sys, tempfile
import source

OUT = source.ROOT / 'documentation/0.4.9/reader'
sys.path.insert(0, str(source.PACKET / 'issue93-dictionary'))
import build_dictionary as renderer
import audit_dictionary as auditor

def generate(check=False):
    source.build(check=True)
    old_reader = source.PACKET / 'issue93-dictionary/reader'
    with tempfile.TemporaryDirectory(prefix='riskium-selected-reader-') as tmp:
        transient = Path(tmp)
        (transient / 'generated').mkdir()
        for alias in ['candidate.ontouml.json', 'candidate.owl.ttl']:
            (transient / 'generated' / alias).write_bytes((source.OUT / source.NAMES[alias]).read_bytes())
        renderer.export = SimpleNamespace(CONTRACT=source.CONTRACT, HERE=transient,
            resolve=source.resolve, validate_contract=source.validate_contract,
            export=lambda c, check=False: source.build(check=True))
        renderer.OUT = OUT
        auditor.build = renderer
        files = renderer.build()
    for name, text in list(files.items()):
        if not name.endswith('.md'):
            continue
        def remap(match):
            target = match.group(1)
            if target.startswith(('http://', 'https://', '#')):
                return match.group(0)
            path, mark, fragment = target.partition('#')
            old = (old_reader / path).resolve()
            if old.parent == old_reader:
                return match.group(0)
            if old == old_reader.parent / 'README.md':
                new = source.ROOT / 'plans/v0.3.9.md'
            elif old == source.PACKET / 'issue93-generalization-sets/build_candidate.py':
                new = source.HERE / 'source.py'
            elif old == source.PACKET / 'issue93-export-contract/input-contract.json':
                new = source.CONTRACT
            else:
                new = old
            return '](' + os.path.relpath(new, OUT) + (mark + fragment if mark else '') + ')'
        text = re.sub(r'\]\(([^)]+)\)', remap, text)
        text = text.replace('Candidate **' + source.VERSION + '**; not the published current dictionary.',
                            'Selected scientific source **' + source.VERSION + '** for package **v0.3.9**; publication has not yet occurred.')
        text = text.replace('# Riskium candidate concept dictionary', '# Riskium selected concept dictionary')
        text = text.replace('# Candidate ', '# ')
        text = text.replace('The current published reader and historical eighty-concept dictionary remain unchanged.', 'The earlier eighty-concept dictionary remains available with its original source binding.')
        text = text.replace('The [candidate execution receipts]', 'The [qualification and publication plan]')
        if name == 'RKM-X01.md':
            old_note = 'The source RiskCase definition is retained in this candidate. The adopted broader RiskCase meaning and its profile/model migration are tracked separately in [issue #92](https://github.com/ArazSaieArasi3/riskium/issues/92); this dictionary does not silently perform that migration.'
            profile = os.path.relpath(source.b2.HERE / 'case_profiles.py', OUT)
            text = text.replace(old_note, 'The adopted analytical-item definition is implemented in scientific source ' + source.VERSION + '. [issue #92](https://github.com/ArazSaieArasi3/riskium/issues/92) tracks maintained-channel publication. Analytical task readiness and local operational-register eligibility remain distinct; the [selected task profiles](' + profile + ') supply the explicit-data checks.')
        files[name] = text.replace('  \nDirect subtypes:', '<br>\nDirect subtypes:')
    svg = files['Subdomain-matrix.svg'].replace('Riskium candidate:', 'Riskium selected source:').replace('not a published production diagram', 'selected for v0.3.9; publication pending')
    files['Subdomain-matrix.svg'] = svg
    manifest = json.loads(files['manifest.json'])
    manifest.update(package_target='v0.3.9', documentation_version='0.4.9', stage='SELECTED_NOT_PUBLISHED')
    manifest['files_sha256'] = {n: hashlib.sha256(t.encode()).hexdigest() for n, t in sorted(files.items()) if n != 'manifest.json'}
    files['manifest.json'] = source.dump(manifest)
    if check:
        if not OUT.is_dir() or {p.name for p in OUT.iterdir() if p.is_file()} != set(files):
            raise ValueError('Selected reader inventory differs')
        for name, text in files.items():
            if (OUT / name).read_text() != text:
                raise ValueError('Stale selected reader: ' + name)
    else:
        OUT.mkdir(parents=True, exist_ok=True)
        for name, text in files.items():
            (OUT / name).write_text(text)
    model, _ = source.validate_contract(json.loads(source.CONTRACT.read_text()))
    return files, auditor.audit(files, model)

if __name__ == '__main__':
    print(source.dump(generate('--check' in sys.argv)[1]))
