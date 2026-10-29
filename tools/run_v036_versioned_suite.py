"""Run candidate tests here and the unchanged published-reader suite at its pinned main source."""
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


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def historical_identity():
    source = git('show', PUBLISHED_READER + ':' + HISTORICAL_TEST)
    current = (ROOT / HISTORICAL_TEST).read_bytes()
    if source != current:
        raise ValueError('The historical reader test must remain unchanged')
    if git('merge-base', PUBLISHED_READER, 'HEAD').decode().strip() != PUBLISHED_READER:
        raise ValueError('Candidate does not descend from reviewed published reader source')
    return hashlib.sha256(source).hexdigest()


def candidate_tests():
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'), pattern='test_*.py')
    published = []

    def split(tests):
        retained = unittest.TestSuite()
        for item in tests:
            if isinstance(item, unittest.TestSuite):
                retained.addTests(split(item))
            elif item.id().startswith('test_published_documentation.'):
                published.append(item.id())
            else:
                retained.addTest(item)
        return retained

    current = split(suite)
    if len(published) != 10 or len(set(published)) != 10 or current.countTestCases() < 500:
        raise ValueError('Lost candidate or historical test during source split')
    return current, published


def run_historical():
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / 'published-source'
        subprocess.run(['git', 'worktree', 'add', '--detach', str(target), PUBLISHED_READER], cwd=ROOT,
                       check=True, capture_output=True)
        try:
            result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests',
                                     '-p', 'test_published_documentation.py', '-v'], cwd=target,
                                    capture_output=True, text=True)
            if result.returncode or 'Ran 10 tests' not in result.stderr or 'OK' not in result.stderr:
                raise ValueError('Published-source reader suite failed:\n' + result.stdout + result.stderr)
        finally:
            subprocess.run(['git', 'worktree', 'remove', '--force', str(target)], cwd=ROOT,
                           check=True, capture_output=True)
    return 10


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='Inspect source split without executing suites')
    parser.add_argument('--receipt', type=Path, help='Save the actual successful source-qualified execution')
    args = parser.parse_args()
    digest = historical_identity()
    current, old = candidate_tests()
    if args.list:
        print(json.dumps(dict(status='VERSIONED_SUITE_DECLARED', candidate_tests=current.countTestCases(),
                              historical_tests=len(old), historical_source=PUBLISHED_READER,
                              historical_test_sha256=digest)))
        return
    historical = run_historical()
    result = unittest.TextTestRunner(verbosity=1).run(current)
    if not result.wasSuccessful() or result.skipped:
        raise ValueError('Candidate suite failed or unexpectedly skipped tests')
    receipt = dict(status='VERSIONED_SUITE_PASS', source_commit=git('rev-parse', 'HEAD').decode().strip(), candidate_tests=result.testsRun,
                          published_reader_tests=historical, historical_source=PUBLISHED_READER,
                          historical_test_sha256=digest)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
