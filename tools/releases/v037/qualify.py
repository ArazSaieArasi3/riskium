"""Qualify an exact v0.3.7 source without mixing historical reader contracts."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--receipt', type=Path, default=Path('build/v037-qualified-suite.json'))
    args = parser.parse_args()
    if args.list:
        subprocess.run([sys.executable, 'tools/run_v036_versioned_suite.py', '--list'], cwd=ROOT, check=True)
        return
    if git('status', '--porcelain'):
        raise ValueError('Qualification requires a clean committed source')
    source = git('rev-parse', 'HEAD')
    subprocess.run([sys.executable, 'tools/releases/v037/selection.py', '--check'], cwd=ROOT, check=True)
    receipt_path = args.receipt.resolve()
    subprocess.run([sys.executable, 'tools/run_v036_versioned_suite.py', '--receipt', str(receipt_path)], cwd=ROOT, check=True)
    receipt = json.loads(receipt_path.read_text())
    if (receipt['source_commit'] != source or git('rev-parse', 'HEAD') != source
            or git('status', '--porcelain') or receipt['status'] != 'VERSIONED_SUITE_PASS'
            or receipt['historical_reader_tests'] != 16):
        raise ValueError('Wrong or changed source-qualified receipt')
    print(json.dumps(dict(status='V037_SOURCE_QUALIFIED', source=source, release_published=False, freeze_completed=False)))


if __name__ == '__main__':
    main()
