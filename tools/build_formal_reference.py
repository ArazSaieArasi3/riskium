"""Project all 25 source/engine/accepted-scope routes into one reader explanation."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = [
    'ontology/riskium-model.json', 'ontology/native/riskium.ontouml.json',
    'ontology/derived/riskium.owl.ttl', 'evaluation/owl-mapping-review.md',
    'evaluation/hermit/report.json', 'evaluation/shacl/coverage-status.json',
    'evaluation/final-review/report.json', 'evaluation/owner-review/accepted-scope.json',
    'evaluation/relational/assessment/mapping-coverage.json',
    'tools/publication/formal-method-introduction.md',
]

def read(path):
    return json.loads((ROOT / path).read_text())

def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def build():
    model, hermit, shacl, preparation, accepted, assessment = [read(p) for p in (
        INPUTS[0], INPUTS[4], INPUTS[5], INPUTS[6], INPUTS[7], INPUTS[8])]
    expected = [f'C-{n:02d}' for n in range(1, 26)]
    sources = {r['id']: r for r in model['constraints']}
    owner = {r['id']: r for r in accepted['constraints']}
    if list(sources) != expected or list(owner) != expected:
        raise ValueError('Missing, duplicate or reordered constraint source/acceptance')
    if accepted['independent_validation'] or accepted['historical_engine_outcomes_changed']:
        raise ValueError('Unsupported acceptance promotion')
    if hermit['inputs']['owl_turtle_sha256'] != sha(INPUTS[2]) or shacl['source_sha256'] != sha(INPUTS[0]):
        raise ValueError('Engine receipt differs from source')
    for records in preparation['evidence_registry'].values():
        for record in records:
            if record['current_equality_required'] and sha(record['path']) != record['sha256']:
                raise ValueError('Stale evidence: ' + record['path'])
    for path, digest in assessment['inputs'].items():
        if sha(path) != digest:
            raise ValueError('Stale SQL overlay: ' + path)
    mapping = {}
    for line in (ROOT / INPUTS[3]).read_text().splitlines():
        cells = [s.strip() for s in line.strip('|').split('|')]
        if len(cells) == 3 and cells[0] in sources:
            mapping[cells[0]] = cells[1:]
    if set(mapping) != set(expected):
        raise ValueError('OWL mapping lacks a clause')
    prepared = {r['id']: r for r in preparation['constraints']}
    for ident in expected:
        if sources[ident] != prepared[ident]['source_clause']:
            raise ValueError('Changed conceptual clause requires review: ' + ident)
    supplement = {r['id']: r for r in assessment['rows'] if r['family'] == 'Constraint'}
    rows, evidence_paths = [], set()
    text = (ROOT / INPUTS[-1]).read_text().rstrip() + '\n\n'
    text += '| Constraint | Historical HermiT | Historical SHACL | Bounded disposition |\n| --- | --- | --- | --- |\n'
    for ident in expected:
        h = [r for r in hermit['obligations'] if r['source_element'] == ident]
        s = [r for r in shacl['obligations'] if r['source_element'] == ident]
        if len(h) != 1 or len(s) != 1:
            raise ValueError('Missing or ambiguous engine route: ' + ident)
        r = owner[ident]
        if r['owner_disposition'] != 'ACCEPTED_WITH_DECLARED_EXCLUSIONS':
            raise ValueError('Unreviewed accepted claim: ' + ident)
        paths = sorted({p['path'] for key in r['evidence_keys'] for p in preparation['evidence_registry'][key]})
        evidence_paths.update(paths)
        row = dict(id=ident, source=sources[ident], owl_encoding=mapping[ident][0],
                   owl_remainder=mapping[ident][1], hermit=h[0], shacl=s[0],
                   accepted_scope=r, evidence=paths, sql_assessment=supplement[ident])
        rows.append(row)
        text += f"| [{ident} {sources[ident]['title']}](#{ident}) | {h[0]['outcome']} | {s[0]['outcome']} | {r['proposed_disposition'].replace('_', ' ').lower()} |\n"
    for row in rows:
        ident, r = row['id'], row['accepted_scope']
        text += f'\n<h2 id="{ident}">{ident} — {row["source"]["title"]}</h2>\n\n'
        text += row['source']['statement'] + '\n\n'
        text += '**OWL encoding:** ' + row['owl_encoding'] + '\n\n'
        text += '**OWL boundary:** ' + row['owl_remainder'] + '\n\n'
        text += '**Historical outcomes:** ' + '; '.join(f"{engine} `{row[key]['id']}` **{row[key]['outcome']}**" for engine,key in [('HermiT','hermit'),('SHACL','shacl')]) + '.\n\n'
        text += '**Accepted bounded claim:** ' + r['retained_claim'] + '\n\n'
        text += '**Remaining/excluded:** ' + r['unclaimed_or_deferred'] + '\n\n'
        if row['sql_assessment']['disposition'] == 'SELECTED_SUBCLAUSES_ONLY':
            text += '**Later SQL assessment overlay (0.2.0):** selected subclauses only; consult the [assessment method](relational-assurance.md), [exact mapping](../implementation/relational/0.2.0/mapping.json) and [executed receipt](../evaluation/relational/assessment/report.json.gz). This does not expand the earlier owner acceptance or change either historical engine outcome.\n\n'
        text += '**Evidence:** ' + ' · '.join(f'[{p}](../{p})' for p in row['evidence']) + '.\n\n'
        text += '<details markdown="1"><summary>Original fixture identifiers and source route</summary>\n\n'
        text += '**HermiT cases:** ' + (row['hermit'].get('case_id') or 'No executed case for this obligation.') + '\n\n'
        text += '**SHACL cases:** ' + (', '.join(row['shacl']['case_ids']) or 'No executed case for this obligation.') + '\n\n'
        text += f'[Conceptual clause](https://arazsaiearasi3.github.io/riskium/current/reference/native/index.html#{ident}) · [Native exchange](../ontology/native/riskium.ontouml.json) · [OWL export](../ontology/derived/riskium.owl.ttl)\n\n</details>\n'
    text += '\n## Source and review record\n\nGenerated by `tools/build_formal_reference.py` from the conceptual source, reviewed OWL mapping, unchanged engine ledgers, [owner-accepted scope](../evaluation/owner-review/accepted-scope.json) and later SQL mapping. [Machine-readable routes and digests](../evaluation/formal-reference/register.json) preserve the original rows. The register is a reading aid, not a new execution receipt. The full cross-document consistency gate is [#39](https://github.com/ArazSaieArasi3/riskium/issues/39), scheduled before the next stable freeze.\n'
    paths = sorted(set(INPUTS) | evidence_paths | set(assessment['inputs']) | {'tools/build_formal_reference.py'})
    register = dict(schema='riskium-formal-reading-routes-v1', model_version=model['version'],
                    scientific_executions=0, independent_review_claimed=False,
                    input_sha256={p:sha(p) for p in paths}, constraints=rows,
                    summary=dict(constraints=len(rows), sql_selected_subclauses=sum(r['sql_assessment']['disposition']=='SELECTED_SUBCLAUSES_ONLY' for r in rows)))
    return {'docs/formal-method.md': text, 'evaluation/formal-reference/register.json': json.dumps(register,indent=2,ensure_ascii=False)+'\n'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for name, content in build().items():
        path=ROOT/name
        if args.check:
            if not path.exists() or path.read_text()!=content:raise SystemExit('Stale formal reading reference: '+name)
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    print(json.dumps(dict(status='FORMAL_READING_ROUTES_PASS',constraints=25,scientific_executions=0)))

if __name__=='__main__':main()
