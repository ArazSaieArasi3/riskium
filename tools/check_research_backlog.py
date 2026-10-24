"""Audit explicit extension boundaries, unfilled review protocol and SQL scope.

This is static accounting. It executes no scientific engine, SQL migration or
human judgment, and does not increase any historical correctness denominator.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = 'evaluation/relational/coverage'


def read(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def element_sha(row):
    return hashlib.sha256(json.dumps(row, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def boundaries(model):
    register = read('requirements/extensions.json')
    require(register['model_sha256'] == sha('ontology/riskium-model.json'), 'Extension model binding changed')
    for key, path in (('references_sha256', 'references/corpus.json'), ('citation_sha256', 'CITATION.cff'), ('rights_sha256', 'RIGHTS.md')):
        require(register[key] == sha(path), 'Extension source/rights binding changed')
    require(register['native_semantics_changed'] is False and register['external_imports_added'] is False and register['adoption_decisions_recorded'] == 0, 'Boundary plan cannot imply adopted semantics')
    rows = register['rows']
    require(len({r['id'] for r in rows}) == len(rows) == 17, 'Extension inventory missing or duplicated')
    concepts = {c['id']: c for c in model['concepts']}
    optional = {c['id'] for c in model['concepts'] if c['scope_layer'] != 'FORMAL_CORE'}
    bridges = {r['id']: r for r in model['associations'] if r['scope_layer'] != 'FORMAL_CORE'}
    require({r['id'] for r in rows if r['kind'] == 'OPTIONAL_BOUNDARY'} == optional, 'Optional boundary omitted')
    require({r['id'] for r in rows if r['kind'] == 'OPTIONAL_BRIDGE'} == set(bridges), 'Optional bridge omitted')
    require({r['id'] for r in rows if r['kind'] == 'FOUNDATIONAL_ANCHOR'} == {r['id'] for r in model['imported_types']}, 'External anchor omitted')
    source_ids = {r['id'] for r in read('references/corpus.json')['sources']}
    for row in rows:
        for key in ('riskium_ownership', 'external_ownership', 'applicability', 'required_cq'):
            require(bool(row[key].strip()), 'Missing extension ownership/evidence definition')
        require(row['blocks_v0_3_1'] is False and len(row['adoption_evidence']) >= 6, 'Deferred boundary lacks adoption/deferral rules')
        require(row['status'] in ('DEFERRED_NOT_IMPLEMENTED', 'LOCAL_PROXY_ONLY', 'CANDIDATE_UNASSESSED'), 'Unjustified implemented alignment')
        if row['kind'] == 'OPTIONAL_BOUNDARY':
            require(concepts[row['current_representation']]['scope_layer'] == 'FORMAL_CORE', 'Documentary representation missing')
        if row['kind'] == 'OPTIONAL_BRIDGE':
            require((row['source'], row['target'], row['title']) == tuple(bridges[row['id']][k] for k in ('source', 'target', 'predicate')), 'Bridge signature changed')
        if row['kind'] == 'ALIGNMENT_CANDIDATE':
            require(row['source_register_id'] in source_ids, 'Uninspected source treated as established alignment')
    return dict(records=len(rows), kinds=dict(Counter(r['kind'] for r in rows)), implementation_or_adoption_claimed=False)


def review_protocol():
    protocol = read('evaluation/independent-review/protocol.json')
    responses = read('evaluation/independent-review/responses.json')
    inventory = read(protocol['inventory_path'])
    require(protocol['inventory_sha256'] == sha(protocol['inventory_path']), 'Historical independent inventory changed')
    require(protocol['model_sha256'] == sha('ontology/riskium-model.json'), 'Review model changed')
    require(protocol['full_inventory'] == inventory['cohorts'], 'Independent review denominator changed')
    groups = {g['id']: g for g in inventory['groups']}
    cohort = protocol['initial_cohort']
    require(len({g['group_id'] for g in cohort}) == len(cohort) == 40, 'Initial review cohort changed without protocol revision')
    for row in cohort:
        source = groups[row['group_id']]
        require(all(row[key] == source[key] for key in ('source_element', 'source_sha256', 'cohort', 'family', 'review_aspects')), 'Review group meaning/aspects drift')
        require(len(row['counterexample_prompts']) >= 2, 'Review counterexample prompts missing')
    for path, digest in protocol['packet_sha256'].items():
        require(sha(path) == digest, 'Review evidence packet changed: ' + path)
    require(protocol['eligibility']['minimum_distinct_reviewers'] == 2 and len(protocol['eligibility']['required_roles']) == 2, 'Paired independent review policy missing')
    require(protocol['status'] == 'PREPARED_NO_REVIEWER_RESPONSES', 'Prepared protocol is not adjudication')
    require(responses['protocol_version'] == protocol['protocol_version'] and responses['status'] == 'NO_ACTUAL_RESPONSES', 'Unknown review result state')
    require(responses['reviewers'] == responses['initial_ratings'] == responses['adjudications'] == [], 'Actual response ingestion needs attributable evidence and a separately reviewed result implementation; do not auto-fill')
    require(protocol['current_results'] == dict(eligible_reviewers_recorded=0, initial_ratings_recorded=0,
        paired_groups_adjudicated=0, independent_semantic_acceptance=False, overall_semantic_correctness_percent=None), 'Independent results invented')
    return dict(predeclared_initial_groups=len(cohort), inventory_groups=sum(inventory['cohorts'].values()),
                real_reviewers=0, actual_independent_ratings=0, adjudicated_groups=0)


def mapping_inventory(model):
    mapping = read('implementation/relational/0.1.0/mapping.json')
    require(mapping['source_model_sha256'] == sha('ontology/riskium-model.json'), 'SQL mapping source changed')
    classes = {r['id']: r for r in mapping['classes']}
    relations = {r['id']: r for r in mapping['relations']}
    constraints = {r['id']: r for r in mapping['constraints']}
    concepts = {r['id']: r for r in model['concepts']}
    associations = {r['id']: r for r in model['associations']}
    clauses = {r['id']: r for r in model['constraints']}
    require(len(classes) == 10 and len(relations) == 5 and len(constraints) == 4, 'Selected SQL mapping inventory changed')
    require(set(classes).issubset(concepts) and set(relations).issubset(associations) and set(constraints).issubset(clauses), 'SQL element not in ontology')
    for row in relations.values():
        require(all(row[k] == associations[row['id']][k] for k in ('source', 'target', 'predicate')), 'SQL relation signature differs')
    for row in constraints.values():
        require(row['statement'] == clauses[row['id']]['statement'] and row['sha256'] == element_sha(clauses[row['id']]), 'SQL clause source differs')
    rows = []
    for family, values in (('Concept', model['concepts']), ('Imported anchor', model['imported_types']),
                           ('Relation', model['associations']), ('Generalization', model['generalizations']),
                           ('Constraint', model['constraints'])):
        for source in values:
            sid = source['id']
            row = dict(id=sid, family=family, source_sha256=element_sha(source),
                title=source.get('title', source.get('predicate', source.get('specific', sid))))
            # Exact definitions stay in their authoritative model; bind them
            # by hash and retain only relationship structure needed to audit.
            row['source_structure'] = {key: source[key] for key in ('scope_layer', 'source', 'target', 'specific', 'general') if key in source}
            if family == 'Imported anchor' or source.get('scope_layer') in ('OPTIONAL_PHENOMENON_BOUNDARY', 'OPTIONAL_EXTERNAL_BRIDGE'):
                row.update(disposition='EXTERNAL_BOUNDARY_NOT_STORED', reason='External bearer/bridge ownership remains outside the public SQLite slice; documentary references do not establish referent truth.', next_evidence='Explicit external identity/alignment and source policy before any adopted mapping; requirements/extensions.json.')
            elif family == 'Concept' and sid in classes:
                row.update(disposition='SELECTED_STORAGE_REPRESENTATION', representation=classes[sid]['representation'],
                    reason='Explicitly named in schema/profile 0.1.0; representation is not full class or task admission.', next_evidence='Broader identity/inheritance, attributes and task-specific admission remain #12.')
            elif family == 'Relation' and sid in relations:
                row.update(disposition='SELECTED_NATIVE_EXPORT', representation='v_native_facts: ' + sid,
                    reason='One of the five selected native predicates; existing SQL receipt has exact history/round-trip evidence.', next_evidence='Complete context/method/scale/criteria assessment-subject mapping and applicable joins remain #12.')
            elif family == 'Constraint' and sid in constraints:
                row.update(disposition='SELECTED_SUBCLAUSES_ONLY', reason={
                    'C-01':'Exact case identifiers and selected entry joins; no complete real-world identity adjudication.',
                    'C-03':'Issued serialized payload/provenance/dependency guards; not full InformationContent or every ontology relation.',
                    'C-24':'Static and stored same-entry predecessor lineage; no full chronology semantics.',
                    'C-25':'Supplementary version-owned dependency kind/coherence checks, not native assessment-subject role admission.'}[sid], next_evidence='Retain unimplemented subclauses; review whole constraint before declaring complete operational support.')
            else:
                row.update(disposition='DEFERRED_NO_COMPLETE_SQL_MAPPING', reason='Not an explicit complete mapping in the public 0.1.0 profile; no implementation is inferred from storage of opaque JSON or a historical private schema.',
                    next_evidence='Declare storage/derivation/external ownership, preserve unknown and provenance, add exact migration/query/counterexample oracles, then execute under #12.')
            rows.append(row)
    require(len(rows) == 306 and len({(r['family'], r['id']) for r in rows}) == len(rows), 'Full source mapping denominator changed')
    inputs = ['ontology/riskium-model.json', 'implementation/relational/0.1.0/mapping.json',
        'implementation/relational/0.1.0/001_tables.sql', 'implementation/relational/0.1.0/002_guards.sql',
        'implementation/relational/0.1.0/fixtures.json', 'evaluation/relational/history/report.json.gz']
    report = dict(schema='riskium-full-relational-scope-inventory-v1', inventory_version='0.1.0',
        model_version='0.3.1', relational_profile='0.1.0', method='Static exhaustive source/mapping reconciliation; zero new SQL executions.',
        inputs={p: sha(p) for p in inputs}, summary=dict(total_source_elements=len(rows),
            families=dict(Counter(r['family'] for r in rows)), dispositions=dict(Counter(r['disposition'] for r in rows))),
        full_mapping_completed=False, native_semantics_changed=False, private_database_migration_executed=False,
        rows=rows)
    return report


def source_publication():
    """Reconcile previously inspected notices; do not invent new rights clearance."""
    paths = ['evaluation/sources/cq06/cohort.json', 'evaluation/sources/cq06/inspection.json',
        'evaluation/sources/cq0708/cohort.json', 'evaluation/sources/cq0708/inspection.json',
        'evaluation/owner-review/accepted-scope.json', 'RIGHTS.md', 'NOTICE.md']
    rows = []
    for path in (paths[0], paths[2]):
        cohort = read(path)
        for source in cohort['sources']:
            rows.append(dict(source_id=source['id'], doi=source['doi'], source_cohort=path,
                primary_pdf_sha256=source['pdf_sha256'], recorded_notice=source.get('rights', source.get('license')),
                source_pdf_redistributed=False, current_package_boundary='Citation, locators, hashes and selected curated paraphrases/assertions only; full source and private databases remain excluded.',
                new_license_clearance_claimed=False))
    require(len(rows) == 4 and all(r['recorded_notice'] for r in rows), 'Source notice inventory missing')
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    protected_hashes = {r['primary_pdf_sha256'] for r in rows}
    excluded_suffixes = {'.pdf', '.docx', '.sqlite', '.sqlite3', '.db', '.zip'}
    for path in filter(None, tracked):
        require(Path(path).suffix.lower() not in excluded_suffixes, 'New binary/source publication requires a separate rights/scope review: ' + path)
        require(sha(path) not in protected_hashes, 'Primary source bytes found in public tree')
    return dict(schema='riskium-source-publication-boundary-review-v1', review_version='0.1.0',
        method='Reconciliation of frozen inspected notices, machine-assistance declarations, owner-scoped dispositions and current tracked-publication exclusions; no new primary inspection or legal clearance.',
        inputs={p: sha(p) for p in paths}, sources=rows, original_source_pdfs_redistributed=False,
        private_database_or_manuscript_published=False, machine_assistance='Assistant selected, transcribed, paraphrased and prepared queries; the current owner scope is accepted, independent judgments remain unrecorded.',
        cohort_boundary=dict(cq06_selected_statements=13, cq07_old_reissued_pairs=5, cq08_candidates_withheld=11,
            new_organizational_risk_cases=0, new_independent_case_accuracy_estimate=False),
        original_historical_cohorts_unchanged=True, broader_case_study_completed=False)


def development_components():
    definitions = [
        ('INTEGRATED_VALIDATION', 'Application shared-graph validator', ['implementation/validation/0.1.0/policy.json', 'tools/validate_integrated.py', 'tools/run_integrated_validation.py', 'evaluation/integration/cases.json', 'evaluation/integration/fixtures.ttl', 'evaluation/integration/report.json.gz']),
        ('RELATIONAL_INVENTORY', 'Exhaustive static mapping inventory; schema stays 0.1.0', [OUTPUT + '/report.json']),
        ('EXTENSION_BOUNDARIES', 'External/domain adoption policy only', ['requirements/extensions.json']),
        ('INDEPENDENT_PROTOCOL', 'Prepared protocol; zero actual responses', ['evaluation/independent-review/protocol.json', 'evaluation/independent-review/responses.json']),
        ('SOURCE_PUBLICATION_REVIEW', 'Existing source/rights and disclosure boundary reconciliation', ['evaluation/sources/publication-review.json']),
    ]
    return dict(schema='riskium-development-component-overlay-v1', overlay_version='0.1.0',
        baseline_release='v0.3.1', baseline_source_commit='8afe169968b5c1396c02834dbc499af691b894b4',
        accepted_matrix_path='releases/artifact-matrix.json', accepted_matrix_sha256=sha('releases/artifact-matrix.json'),
        status='POST_RELEASE_DEVELOPMENT_NOT_PUBLISHED_AS_NEW_RELEASE',
        published_baseline_components_changed=False, new_owner_or_independent_acceptance_claimed=False,
        components=[dict(id=sid, description=description, version='0.1.0', compatible_model='0.3.1',
            status='DEVELOPMENT_SUPPLEMENT', files=[dict(path=path, sha256=sha(path)) for path in paths]) for sid, description, paths in definitions])


def render(report):
    lines = ['# Full relational mapping inventory', '',
        'This static audit accounts for all 306 source elements, including optional boundaries and the imported anchor. It identifies missing implementation; it does not close #12 or convert exclusions into support. No new SQL migration or scientific validation is performed by this report.', '',
        'The public SQLite 0.1.0 profile explicitly represents 10 classes and exports five native predicates. Four constraints have supported subclauses, with C-25 application bindings kept distinct from native assessment roles. All other rows retain their explicit unimplemented/external disposition.', '',
        'Summary: ' + json.dumps(report['summary']) + '.', '',
        '[Exact per-element JSON and source hashes](report.json). Reproduce: `python tools/check_research_backlog.py --check`.', '',
        '| Family | Element | Disposition | Representation or remaining scope |', '| --- | --- | --- | --- |']
    for row in report['rows']:
        lines.append('| ' + row['family'] + ' | ' + row['id'] + ' | ' + row['disposition'] + ' | ' + row.get('representation', row['reason']).replace('|', '\\|') + ' |')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    model = read('ontology/riskium-model.json')
    extension_status = boundaries(model)
    review_status = review_protocol()
    report = mapping_inventory(model)
    source_review = source_publication()
    outputs = {OUTPUT + '/report.json': json.dumps(report, indent=2) + '\n', OUTPUT + '/README.md': render(report),
        'evaluation/sources/publication-review.json': json.dumps(source_review, indent=2) + '\n'}
    for path, text in outputs.items():
        target = ROOT / path
        if args.check:
            require(target.exists() and target.read_text() == text, 'Generated mapping audit differs: ' + path)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
    overlay = development_components()
    overlay_path = ROOT / 'releases/development-components.json'
    overlay_text = json.dumps(overlay, indent=2) + '\n'
    if args.check:
        require(overlay_path.exists() and overlay_path.read_text() == overlay_text, 'Development component bindings differ')
    else:
        overlay_path.write_text(overlay_text)
    print(json.dumps(dict(status='POST_RELEASE_SCOPE_ACCOUNTING_PASS', extensions=extension_status,
        independent_review=review_status, relational=report['summary'], source_notices=len(source_review['sources']),
        development_components=len(overlay['components']), new_scientific_engine_runs=0)))


if __name__ == '__main__':
    main()
