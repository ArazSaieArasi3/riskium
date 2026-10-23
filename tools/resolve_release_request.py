"""Resolve explicit prerelease intent; unchanged request files never republish."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REQUEST = 'releases/development-request.json'


def resolve(root, event, ref, before, after, inputs=None):
    inputs = inputs or {}
    tag, publish = '', False
    if event == 'workflow_dispatch':
        tag = inputs.get('release_tag', '')
        publish = inputs.get('publish', False) in (True, 'true')
    elif event == 'push' and ref == 'refs/heads/main':
        if not re.fullmatch(r'[0-9a-f]{40}', before or '') or set(before) == {'0'}:
            return {'release_tag': '', 'publish': False}
        changed = subprocess.check_output(['git', '-C', str(root), 'diff', '--name-only',
                                           before, after, '--', REQUEST]).decode().splitlines()
        if REQUEST in changed:
            data = json.loads(subprocess.check_output(['git', '-C', str(root), 'show', after + ':' + REQUEST]))
            if data.get('profile') != 'development-prerelease' or data.get('publish') is not True:
                raise ValueError('Changed release request must explicitly select the development prerelease profile')
            tag, publish = data['tag'], True
    if tag and not re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+-rc\.[1-9][0-9]*', tag):
        raise ValueError('An explicit development tag is required')
    if publish and (not tag or ref != 'refs/heads/main'):
        raise ValueError('Publication requires a development tag on reviewed main')
    if publish:
        # Read the release-specific notes from the same immutable source commit.
        subprocess.check_output(['git', '-C', str(root), 'show',
                                 after + ':docs/prerelease-' + tag + '.md'], stderr=subprocess.PIPE)
    return {'release_tag': tag, 'publish': publish}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--event-file', default=os.environ.get('GITHUB_EVENT_PATH'))
    args = p.parse_args()
    payload = json.loads(Path(args.event_file).read_text())
    result = resolve(ROOT, os.environ['GITHUB_EVENT_NAME'], os.environ['GITHUB_REF'],
                     payload.get('before', ''), os.environ['GITHUB_SHA'], payload.get('inputs'))
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
        output.write('release_tag=' + result['release_tag'] + '\n')
        output.write('publish=' + str(result['publish']).lower() + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
