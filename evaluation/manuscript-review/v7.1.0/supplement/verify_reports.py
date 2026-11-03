"""Compare substantive replay outputs with the original 7.1.0 snapshots."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
OUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE / 'generated'
EXPECTED_MODEL = '4a052bb0b7321e5209417c69e96644089aa7dba1734cce4a70e5223f2ebbaf59'
actual_model = hashlib.sha256((REPO / 'ontology/riskium-model.json').read_bytes()).hexdigest()
assert actual_model == EXPECTED_MODEL, f'model digest changed: {actual_model}'

for name in ('structural-report', 'pattern-report', 'query-contract', 'query-parity-report'):
    original = json.loads((HERE / (name + '.json')).read_text())
    replay = json.loads((OUT / (name + '.json')).read_text())
    for key in ('repository_commit', 'script_sha256', 'python', 'sqlite', 'rdflib'):
        original.pop(key, None)
        replay.pop(key, None)
    if name == 'structural-report':
        for report in (original, replay):
            for row in report['rows']:
                row['components'] = sorted(row['components'])
    assert original == replay, f'substantive difference in {name}'
    print(name + ': MATCH')
