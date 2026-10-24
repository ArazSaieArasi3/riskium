"""Generate or check the native Wiki projection from the shared guide registry."""
import argparse
import json
from guides import sync_wiki

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print(json.dumps({'status': 'SHARED_WIKI_SOURCE_PASS', 'reader_pages': sync_wiki(check=args.check),
                      'live_publication_claimed': False}))
