"""Bind qualified evidence requirements, selected routes and all 306 native identities."""
import argparse
from collections import Counter
import hashlib
import json

import relational_evidence as e

ROOT = e.ROOT
OUT = ROOT / 'evaluation/relational/qualified-evidence'
GROUPS = {
    'EQR-01': ['POPULATED_UPGRADE', 'LEGACY_GRAPHS_PRESERVED', 'LINEAGE_PRESERVED', 'IDEMPOTENT_UPGRADE', 'FAILED_UPGRADE'],
    'EQR-02': ['NO_TARGET', 'MISSING_TARGET', 'UNISSUED_TARGET', 'TARGET_OWNER_MISMATCH', 'DUPLICATE_TARGET',
               'TWO_VERSIONS_ONE_TARGET', 'MISSING_ITEM', 'UNISSUED_ITEM', 'ITEM_OWNER_MISMATCH', 'WRONG_REF_KIND',
               'CONFLICTING_TYPING', 'UNISSUED_EXCLUDED', 'ROLE_CONTEXTUAL', 'RAW_EXCLUSION'],
    'EQR-03': ['PROVENANCE_EXACT', 'ITEM_OLD_PIN', 'MISSING_SOURCE', 'EMPTY_PROVENANCE', 'BAD_CALENDAR',
               'SOURCE_MISMATCH', 'OWNER_MISMATCH', 'PAYLOAD_DRIFT', 'SEAL_SMUGGLE', 'DUPLICATE_VERSION',
               'UPDATE_SNAPSHOT', 'DELETE_SNAPSHOT', 'REPLACE_SNAPSHOT', 'UPDATE_TARGET', 'DELETE_TARGET',
               'REPLACE_TARGET', 'LATE_TARGET', 'INVALID_ROLE', 'NONTEXT_INPUT'],
    'EQR-04': ['TARGET_OLD', 'TARGET_NEW', 'MULTIPLE_TARGETS', 'NO_IMPLICIT_ENDORSEMENT', 'DUPLICATE_LABEL_IDENTITIES',
               'NATIVE_REFERENCE_A1', 'NATIVE_REFERENCE_A2', 'NATIVE_REFERENCE_B1', 'NATIVE_REFERENCE_C1',
               'BOUND_PARAMETER', 'MUTANT_SOURCE_JOIN_EXPOSED', 'MUTANT_DIRECTION_EXPOSED'],
    'EQR-05': ['BACKUP_REOPEN', 'FILE_REOPEN', 'DUMP_RESTORE', 'CONFIGURATION_OFF', 'LEDGER_DRIFT', 'SCHEMA_DRIFT',
               'ATOMIC_BUNDLE_FAILURE', 'RESTORE_PAYLOAD_TAMPER', 'RESTORE_ITEM_TAMPER', 'RESTORE_ROLE_TAMPER',
               'MUTANT_CARDINALITY_EXPOSED', 'MUTANT_IMMUTABILITY_EXPOSED'],
    'EQR-06': ['RAW_EXCLUSION', 'NO_IMPLICIT_ENDORSEMENT']}


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def encode(data):
    return json.dumps(data, indent=2) + '\n'


def build():
    contract = e.contract()
    report = json.loads((OUT / 'report.json').read_text())
    for path, digest in report['inputs_sha256'].items():
        if sha(path) != digest:
            raise ValueError('Stale evidence receipt: ' + path)
    cases = {row['id']: row for row in report['cases']}
    if len(cases) != 62 or report['summary']['outcomes'] != {'PASS': 62} or set().union(*map(set, GROUPS.values())) != set(cases):
        raise ValueError('Incomplete qualified-evidence execution/requirement trace')
    model = json.loads((ROOT / 'ontology/riskium-model.json').read_text())
    source = {row['id']: row for family in ('concepts', 'imported_types', 'associations', 'generalizations', 'constraints') for row in model[family]}
    baseline = 'evaluation/relational/source-scenario-lineage/mapping-accounting.json'
    old = json.loads((ROOT / baseline).read_text())
    rows = old['rows']
    selected = set(contract['native_classes'] + contract['native_relations'] + contract['generalizations'])
    if len(source) != len(rows) or len(source) != 306 or set(source) != {row['id'] for row in rows} or len(selected) != 6:
        raise ValueError('Lost native source identities')
    for row in rows:
        actual = hashlib.sha256(json.dumps(source[row['id']], sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
        if row['source_sha256'] != actual:
            raise ValueError('Native source drift: ' + row['id'])
        row['historical_0_5_0_disposition'] = row['disposition']
        if row['id'] in selected:
            if row['disposition'] != 'DEFERRED_NO_COMPLETE_SQL_MAPPING':
                raise ValueError('Unexpected prior mapping: ' + row['id'])
            row['disposition'] = 'SCOPED_ADDITIVE_QUALIFIED_EVIDENCE_MAPPING'
            row['qualified_evidence_overlay'] = 'Selected reference storage/contextual item role, two native directions or inherited typing; no complete class/rule semantics.'
        elif row['id'] == 'C-12':
            row['qualified_evidence_overlay'] = 'Selected support/challenge/context qualification and no-endorsement projection; original native disposition/full semantic acceptance remains unchanged.'
        else:
            row['qualified_evidence_overlay'] = 'NO_ADDITIONAL_MAPPING'
    dispositions = dict(Counter(row['disposition'] for row in rows))
    if dispositions.get('DEFERRED_NO_COMPLETE_SQL_MAPPING') != 236:
        raise ValueError('Native deferred denominator changed unexpectedly')
    inventory = dict(schema='riskium-qualified-evidence-accounting-v1', profile='0.6.0', baseline_path=baseline,
                     baseline_sha256=sha(baseline), source_elements=306, source_sha256=sha('ontology/riskium-model.json'),
                     historical_summary=old['current_dispositions'], current_dispositions=dispositions,
                     remaining_deferred=236, retained_partial_source_scenario_routes=8, new_partial_evidence_routes=6,
                     new_reference_representations=1, new_contextual_item_role_routes=1, new_relation_exports=2,
                     inherited_typing_routes=2, full_mapping_completed=False, rows=rows)
    req_ids = {row['id'] for row in json.loads((ROOT / 'requirements/requirements.json').read_text())}
    requirements = []
    for req in contract['requirements']:
        if not set(req['source_requirements']).issubset(req_ids):
            raise ValueError('Unknown original requirement')
        requirements.append(dict(requirement=req, cqs=['RQ-CQ06', 'RQ-CQ08'], case_ids=GROUPS[req['id']],
                                 implementation=['implementation/relational/0.6.0/007_qualified_evidence.sql',
                                                 'implementation/relational/0.6.0/queries/by_target.sql', 'tools/relational_evidence.py'],
                                 status='SCOPED_EXECUTED_ENGINEERING',
                                 limit='Bounded qualified references/contextual role projection; no complete original/native semantic or independent acceptance.'))
    paths = set(report['inputs_sha256']) | set(contract['source_sha256']) | {
        'implementation/relational/0.6.0/README.md', 'implementation/relational/0.6.0/schema-dictionary.md',
        'evaluation/relational/qualified-evidence/report.json', 'evaluation/relational/qualified-evidence/README.md',
        'tests/test_qualified_evidence.py', 'tools/build_evidence_inventory.py',
        'evaluation/sources/cq0708/cohort.json', 'evaluation/sources/cq0708/report.json.gz'}
    inputs = {path: sha(path) for path in sorted(paths)}
    trace = dict(schema='riskium-qualified-evidence-requirement-trace-v1', profile='0.6.0', execution_issue=44, parent_issues=[35, 12],
                 original_drsd='0.1.0 unchanged; EQR-01..06 explicit derived supplement', requirements=requirements,
                 inputs_sha256=inputs, original_organizational_admissions='All 11 WITHHELD; zero new independent semantic ratings')
    outputs = {'evaluation/relational/qualified-evidence/mapping-accounting.json': encode(inventory),
               'evaluation/relational/qualified-evidence/traceability.json': encode(trace)}
    component = dict(schema='riskium-qualified-evidence-component-v1', id='QUALIFIED_EVIDENCE', version='0.6.0',
                     schema_version=7, compatible_model='0.3.1', baseline_sql_profile='0.5.0',
                     status='DEVELOPMENT_COMPONENT_NOT_SELECTED_BY_STABLE_DISTRIBUTION', stable_distribution_unchanged='v0.3.3',
                     proposed_successor='v0.3.4 PLANNED; selection/freeze/publication not executed', summary=report['summary'],
                     native_support=dict(reference_representations=1, contextual_item_role_routes=1, relation_exports=2,
                                         inherited_typing_routes=2, full_mapping_completed=False),
                     files_sha256=dict(inputs, **{p: hashlib.sha256(data.encode()).hexdigest() for p, data in outputs.items()}))
    outputs['implementation/relational/0.6.0/component.json'] = encode(component)
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, data in build().items():
        path = ROOT / name
        if args.check:
            if not path.is_file() or path.read_text() != data:
                raise ValueError('Stale evidence accounting: ' + name)
        else:
            path.write_text(data)
    print(encode(dict(status='QUALIFIED_EVIDENCE_ACCOUNTING_PASS', native_elements=306, new_partial_routes=6, remaining_deferred=236, requirements=6)))


if __name__ == '__main__':
    main()
