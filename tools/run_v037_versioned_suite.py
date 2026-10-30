"""Run current tests here and unchanged historical readers at their reviewed sources."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED_READER = '41caeaa78c7a152787d1070540e20ae0c6a2395a'
HISTORICAL_TEST = 'tests/test_published_documentation.py'
HISTORICAL_SUITES = (
    ('86accc6695e4738dd1337d5b9addd73b82c73c3d', 'tests/test_nature_documentation.py', 4),
    ('86accc6695e4738dd1337d5b9addd73b82c73c3d', 'tests/test_release_v037_selection.py', 6),
    ('86accc6695e4738dd1337d5b9addd73b82c73c3d', 'tests/test_release_v037_routing.py', 4),
    ('86accc6695e4738dd1337d5b9addd73b82c73c3d', 'tests/test_release_v037_freeze.py', 7),

    (PUBLISHED_READER, HISTORICAL_TEST, 10),
    ('765cb4507d925037cf82c1dc42bdea0a52bf9dca', 'tests/test_released_documentation.py', 4),
    ('58ff468ec4e8f3500ace6869601a25ea263c3d9f', 'tests/test_assessment_documentation.py', 2),
)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def historical_identity():
    identities = []
    for commit, path, count in HISTORICAL_SUITES:
        source = git('show', commit + ':' + path)
        if source != (ROOT / path).read_bytes():
            raise ValueError('Historical reader test changed: ' + path)
        if git('merge-base', commit, 'HEAD').decode().strip() != commit:
            raise ValueError('Current source does not descend from reviewed reader: ' + commit)
        identities.append(dict(source=commit, path=path, tests=count,
                               sha256=hashlib.sha256(source).hexdigest()))
    return identities


def candidate_tests():
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'), pattern='test_*.py')
    published = []

    def split(tests):
        retained = unittest.TestSuite()
        for item in tests:
            if isinstance(item, unittest.TestSuite):
                retained.addTests(split(item))
            elif any(item.id().startswith(Path(path).stem + '.') for _, path, _ in HISTORICAL_SUITES):
                published.append(item.id())
            else:
                retained.addTest(item)
        return retained

    current = split(suite)
    expected = sum(count for _, _, count in HISTORICAL_SUITES)
    if len(published) != expected or len(set(published)) != expected or current.countTestCases() < 500:
        raise ValueError('Lost candidate or historical test during source split')
    return current, published


def run_historical():
    total = 0
    for commit, path, count in HISTORICAL_SUITES:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'reader-source'
            subprocess.run(['git', 'worktree', 'add', '--detach', str(target), commit], cwd=ROOT,
                           check=True, capture_output=True)
            try:
                result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests',
                                         '-p', Path(path).name, '-v'], cwd=target,
                                        capture_output=True, text=True)
                if result.returncode or f'Ran {count} tests' not in result.stderr or 'OK' not in result.stderr:
                    raise ValueError('Historical reader failed at ' + commit + ':\n' + result.stdout + result.stderr)
            finally:
                subprocess.run(['git', 'worktree', 'remove', '--force', str(target)], cwd=ROOT,
                               check=True, capture_output=True)
        total += count
    return total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='Inspect source split without executing suites')
    parser.add_argument('--receipt', type=Path, help='Save the actual successful source-qualified execution')
    args = parser.parse_args()
    digest = historical_identity()
    current, old = candidate_tests()
    if args.list:
        print(json.dumps(dict(status='VERSIONED_SUITE_DECLARED', candidate_tests=current.countTestCases(),
                              historical_tests=len(old), historical_suites=digest)))
        return
    historical = run_historical()
    result = unittest.TextTestRunner(verbosity=1).run(current)
    if not result.wasSuccessful() or result.skipped:
        raise ValueError('Candidate suite failed or unexpectedly skipped tests')
    receipt = dict(status='VERSIONED_SUITE_PASS', source_commit=git('rev-parse', 'HEAD').decode().strip(), candidate_tests=result.testsRun,
                          published_reader_tests=10, historical_reader_tests=historical,
                          historical_suites=digest)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
