"""Gate released nature-task 0.4.5 publication on current source, v0.3.7 identity and settled publishers."""
import argparse
import json
import time

import released_nature_documentation as reader
import published_documentation as historical


DOCUMENTATION = 'Documentation integrity'
INCREMENTAL = 'Incremental release candidate'
PAGES = 'Publish versioned documentation'
STATUS = 'Publish verified source release status'
CURRENT = 'Publish current documentation 0.4.0'
CANDIDATE = 'v0.3.6 candidate reader on main'
PUBLISHED = 'Published v0.3.5 reader documentation'
OLD_SUITE = 'Post-v0.3.6 source-qualified full suite'
OLD_READER = 'Nature-task reader for proposed v0.3.7'
SUITE = 'Post-v0.3.7 source-qualified full suite'
NAMES = {DOCUMENTATION, INCREMENTAL, PAGES, STATUS, CURRENT, PUBLISHED, SUITE, CANDIDATE, OLD_SUITE, OLD_READER}
WORKFLOWS = {DOCUMENTATION: 'documentation.yml', INCREMENTAL: 'incremental-release.yml',
             PAGES: 'pages.yml', STATUS: 'publication-status.yml',
             CURRENT: 'current-documentation-pages.yml', PUBLISHED: 'published-documentation.yml',
             SUITE: 'v037-versioned-suite.yml', OLD_SUITE: 'v036-versioned-suite.yml', OLD_READER: 'released-reader-main.yml', CANDIDATE: 'assessment-reader-main.yml'}


def settled(runs, source, run_id, disabled=frozenset()):
    """Require terminal predecessor attempts, including descendants yet to be queued."""
    grouped = {}
    for run in runs:
        if (run['head_sha'] == source and run['head_branch'] == 'main'
                and run['event'] in ('push', 'workflow_run')
                and run['id'] != run_id and run['name'] in NAMES):
            grouped.setdefault(run['name'], []).append(run)
    pending = []
    for name in (DOCUMENTATION, INCREMENTAL, SUITE, OLD_SUITE):
        if name not in grouped:
            pending.append('Not yet observed: ' + name)
    for name, attempts in grouped.items():
        if any(run['status'] != 'completed' for run in attempts):
            pending.append('Running: ' + name)
    # These workflows are queued after predecessor completion, not with the push.
    for parent, child in ((DOCUMENTATION, PAGES), (PAGES, STATUS), (STATUS, CURRENT)):
        if any(run['status'] == 'completed' and run['conclusion'] == 'success'
               for run in grouped.get(parent, [])) and child not in grouped and child not in disabled:
            pending.append('Awaiting triggered successor: ' + child)
    if INCREMENTAL in grouped and PUBLISHED not in grouped:
        pending.append('Awaiting old reader boundary run')
    suite = grouped.get(SUITE, [])
    reader.require(not suite or all(run['status'] != 'completed' or run['conclusion'] == 'success'
                                   for run in suite), 'Source-qualified suite failed')
    return pending


def workflow_states(getter=reader.api):
    workflows = getter('actions/workflows?per_page=100')['workflows']
    disabled = set()
    for name, filename in WORKFLOWS.items():
        matches = [w for w in workflows if w['path'] == '.github/workflows/' + filename]
        reader.require(len(matches) == 1 and matches[0]['name'] == name, 'Missing or renamed workflow: ' + name)
        state = matches[0]['state']
        reader.require(state in ('active', 'disabled_manually'), 'Unexpected workflow state: ' + name)
        if state != 'active':
            reader.require(name in (PAGES, STATUS, CURRENT), 'Required source gate is disabled: ' + name)
            disabled.add(name)
    return disabled


def run_inventory(source, getter=reader.api):
    runs = []
    for page in range(1, 11):
        data = getter('actions/runs?head_sha=' + source + '&per_page=100&page=' + str(page))['workflow_runs']
        runs.extend(data)
        if len(data) < 100:
            break
    return runs


def verify_source(source):
    reader.require(reader.git(reader.ROOT, 'rev-parse', 'HEAD') == source, 'Wrong checkout')
    reader.require(not reader.git(reader.ROOT, 'status', '--porcelain'), 'Dirty deployment source')
    publication = json.loads(reader.read(reader.ROOT, reader.NS + '/publication.json'))
    reader.verify_live_release(publication, source)
    reader.preserved_inputs()
    reader.review()
    try:
        reader.predecessor.review()
    except ValueError as exc:
        reader.require('Active README drift' in str(exc), 'Unexpected previous reader boundary: ' + str(exc))
    else:
        raise ValueError('Previous reader accepts the new entrypoint')
    try:
        historical.preserved_inputs()
    except ValueError as exc:
        reader.require('Outside additive documentation scope' in str(exc),
                       'Unexpected old publisher failure: ' + str(exc))
    else:
        raise ValueError('Old reader publisher accepts candidate; competing deployment possible')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--run-id', required=True, type=int)
    parser.add_argument('--wait-seconds', type=int, default=0)
    args = parser.parse_args()
    deadline = time.monotonic() + args.wait_seconds
    while True:
        verify_source(args.source)
        disabled = workflow_states()
        pending = settled(run_inventory(args.source), args.source, args.run_id, disabled)
        if not pending:
            break
        reader.require(time.monotonic() < deadline, 'Predecessor deployments unsettled: ' + '; '.join(pending))
        print(json.dumps({'pending': pending}), flush=True)
        time.sleep(15)
    print(json.dumps(dict(status='SOURCE_QUALIFIED_MAIN_DEPLOYMENT_GATE_PASS',
                         source=args.source, prior_selected_files=903,
                         retired_predecessor_workflows=sorted(disabled),
                         old_reader_rejects_candidate=True, predecessor_deployments_settled=True)))


if __name__ == '__main__':
    main()
