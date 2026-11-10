"""Make legacy CI a source-pinned read-only replay; current qualification is separate."""
import argparse
import copy
import re
import subprocess
from pathlib import Path
import yaml
import curation

BASELINE = '7b8f43847ca1d45f0735e8b73d9d9fabd8701e62'
HISTORICAL = '3ce6f5573e2e0a698591615a7ded75c2f9451444'
POLICY = curation.ROOT / 'releases/routing-v0.3.10.json'
CURRENT = '.github/workflows/curation-v0310.yml'
PUBLISHED_READERS = {'assessment-reader-main.yml', 'dictionary-reader.yml', 'released-reader-main.yml',
                     'released-v037-reader.yml', 'external-definition-reader.yml', 'reader-v038.yml'}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=curation.ROOT)


def baseline_workflows():
    names = git('ls-tree', '-r', '--name-only', BASELINE, '.github/workflows').decode().splitlines()
    return {n: git('show', BASELINE + ':' + n).decode() for n in names if n.endswith('.yml')}


def legacy_target(data):
    on = data.get('on', data.get(True, {}))
    push = on.get('push') or {}
    return 'main' in push.get('branches', []) or 'pull_request' in on or 'workflow_run' in on


def expected(data, path=''):
    d = copy.deepcopy(data)
    roles = {}
    for name, job in d['jobs'].items():
        permissions = {**d.get('permissions', {}), **job.get('permissions', {})}
        write = name in {'deploy', 'publish', 'retire'} or any(v == 'write' for v in permissions.values())
        retired_build = Path(path).name in PUBLISHED_READERS and name == 'build'
        if write or retired_build:
            job['if'] = '${{ false }}'
            roles[name] = 'RETIRED_PUBLISHED_READER_BUILD' if retired_build else 'DISABLED_LEGACY_WRITE'
        else:
            roles[name] = 'SOURCE_PINNED_READ_ONLY_REPLAY'
            for step in job.get('steps', []):
                if step.get('uses', '').startswith('actions/checkout@'):
                    step.setdefault('with', {})['ref'] = HISTORICAL
    return d, roles


def edit_text(text, target):
    lines = text.splitlines(keepends=True)
    jobs = [i for i, line in enumerate(lines) if re.fullmatch(r'  [A-Za-z0-9_-]+:\n', line)]
    # Rewrite only job if and checkout ref; parsed equality below rejects other changes.
    for i, start in reversed(list(enumerate(jobs))):
        end = jobs[i+1] if i+1 < len(jobs) else len(lines)
        name = lines[start].strip()[:-1]
        if name not in target['jobs']:
            continue
        block = lines[start:end]
        job = target['jobs'][name]
        if job.get('if') == '${{ false }}':
            for k in range(len(block)-1, 0, -1):
                if block[k].startswith('    if:'):
                    stop = k + 1
                    while stop < len(block) and (block[stop].startswith('      ') or not block[stop].strip()):
                        stop += 1
                    del block[k:stop]
            block.insert(1, '    if: ${{ false }}\n')
        else:
            for k in range(len(block)-1, 0, -1):
                if re.match(r'      - uses: actions/checkout@', block[k]):
                    stop = k + 1
                    while stop < len(block) and (block[stop].startswith('        ') or not block[stop].strip()):
                        stop += 1
                    ref = next((x for x in range(k+1, stop) if block[x].startswith('          ref:')), None)
                    with_at = next((x for x in range(k+1, stop) if block[x].startswith('        with:')), None)
                    if ref is not None:
                        block[ref] = '          ref: ' + HISTORICAL + '\n'
                    elif with_at is not None:
                        block.insert(with_at+1, '          ref: ' + HISTORICAL + '\n')
                    else:
                        block[k+1:k+1] = ['        with:\n', '          ref: ' + HISTORICAL + '\n']
        lines[start:end] = block
    result = ''.join(lines)
    curation.need(yaml.safe_load(result) == target, 'Unexpected scheduler transformation')
    return result


def build(check=False):
    rows = []
    for name, text in baseline_workflows().items():
        if name == CURRENT:
            continue
        parsed = yaml.safe_load(text)
        if not legacy_target(parsed):
            rows.append({'path': name, 'role': 'PRESERVED_BRANCH_SPECIFIC_SOURCE', 'sha256': curation.sha(text.encode())})
            curation.need((curation.ROOT / name).read_text() == text, 'Branch-specific workflow changed')
            continue
        target, roles = expected(parsed, name)
        result = edit_text(text, target)
        if check:
            curation.need((curation.ROOT / name).read_text() == result, 'Stale source-pinned scheduler: ' + name)
        else:
            (curation.ROOT / name).write_text(result)
        rows.append({'path': name, 'role': 'LEGACY_REPLAY_OR_DISABLED_WRITE', 'jobs': roles,
                     'baseline_sha256': curation.sha(text.encode()), 'routed_sha256': curation.sha(result.encode()),
                     'replay_source': HISTORICAL})
    data = {'schema': 'riskium-v0310-workflow-routing/1', 'baseline': BASELINE, 'historical_source': HISTORICAL,
            'current_workflow': CURRENT, 'current_mode': 'QUALIFY_AND_FREEZE_ONLY_NO_DEPLOYMENT', 'workflows': rows,
            'old_model_oracles_unchanged': True, 'legacy_writes_disabled': True,
            'next_gate': 'N5b must use the selected exact candidate, verified assets and channel readback.'}
    current = yaml.safe_load((curation.ROOT / CURRENT).read_text())
    curation.need(current['permissions'] == {'contents': 'read'} and set(current['jobs']) == {'qualify', 'package'}, 'Current workflow must only qualify/package')
    curation.need(not any(v == 'write' for j in current['jobs'].values() for v in j.get('permissions', {}).values()), 'Current workflow has write permission')
    if check:
        curation.need(curation.load(POLICY) == data, 'Stale workflow routing inventory')
    else:
        POLICY.write_text(curation.dump(data))
    return data


if __name__ == '__main__':
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--check', action='store_true')
    d = build(a.parse_args().check)
    print(curation.dump({'workflows': len(d['workflows']), 'historical_source': HISTORICAL,
                        'disabled_write_jobs': sum(v == 'DISABLED_LEGACY_WRITE' for w in d['workflows'] for v in w.get('jobs', {}).values())}))
