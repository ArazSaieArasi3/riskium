"""Validate prospective v0.3.5 release support; never freeze or publish."""
import argparse
import json
from pathlib import Path
import sys

# Checking an unpacked source must not add bytecode files to its inventory.
sys.dont_write_bytecode = True
import release_v035 as release


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check-profile', action='store_true')
    mode.add_argument('--check-unpacked', type=Path, metavar='SOURCE_ROOT')
    parser.add_argument('--manifest', type=Path, help='External source-manifest.json for exact package inventory checking')
    args = parser.parse_args()
    if args.manifest and not args.check_unpacked:
        parser.error('--manifest requires --check-unpacked')
    if args.check_profile:
        release.validate_profile()
        result = dict(status='V035_PROSPECTIVE_PROFILE_PASS', tag=release.TAG, stage=release.STAGE,
                      source_freeze_executed=False, registered_for_publication=False, publication_executed=False)
    else:
        manifest = json.loads(args.manifest.read_bytes()) if args.manifest else None
        result = release.validate_unpacked(args.check_unpacked, manifest)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
