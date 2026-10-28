"""Bind the derived correction requirements without claiming new native mappings."""
import argparse
from collections import Counter
import hashlib
import json

import relational_source_scenario_lineage as l

ROOT = l.ROOT
OUT = ROOT / 'evaluation/relational/source-scenario-lineage'
GROUPS = {
    'SCL-01': ['POPULATED_UPGRADE', 'LEGACY_NATIVE_PRESERVED', 'IDEMPOTENT_UPGRADE', 'FAILED_UPGRADE'],
    'SCL-02': ['DUPLICATE_PARENT', 'REPLACE_PARENT', 'SELF_PARENT', 'CYCLE', 'CROSS_ARTIFACT', 'CROSS_CLASS',
               'MISSING_CHILD', 'MISSING_PARENT', 'UNISSUED_CHILD', 'UNISSUED_PARENT', 'NONKNOWLEDGE_PARENT',
               'RAW_PARENT', 'MUTANT_OWNER_GUARD_EXPOSED'],
    'SCL-03': ['PROVENANCE_SEPARATE', 'ORIGINAL_CONTEXT_PIN', 'UNKNOWN_CONTEXT_RETAINED', 'MISSING_DECLARATION_SOURCE',
               'EMPTY_REASON', 'EMPTY_LOCATOR', 'EMPTY_INTERPRETATION', 'BAD_CALENDAR', 'NONCANONICAL_TIME',
               'EARLY_DECLARATION', 'UPDATE_DECLARATION', 'DELETE_DECLARATION', 'MUTANT_IMMUTABILITY_EXPOSED'],
    'SCL-04': ['SCENARIO_BRANCHES', 'REFERENCE_BRANCHES', 'DESCENDANT_ROOT', 'EQUAL_LABEL_SINGLETON',
               'PLAIN_VERSION_UNLINKED', 'UNKNOWN_ROOT', 'ALL_NATIVE_ORACLES', 'OLD_GRAPHS_UNCHANGED',
               'NO_NATIVE_CORRECTION', 'NO_ADMISSION_OR_OCCURRENCE', 'BOUND_PARAMETER', 'MUTANT_SOURCE_JOIN_EXPOSED'],
    'SCL-05': ['BACKUP_REOPEN', 'FILE_REOPEN', 'DUMP_RESTORE', 'ATOMIC_ISSUE_FAILURE', 'NONTEXT_INPUT',
               'CONFIGURATION_OFF', 'LEDGER_DRIFT', 'SCHEMA_DRIFT', 'RESTORE_OWNER_TAMPER', 'RESTORE_TIME_TAMPER',
               'RESTORE_CYCLE_TAMPER', 'RESTORE_PROVENANCE_TAMPER'],
    'SCL-06': ['NO_ADMISSION_OR_OCCURRENCE', 'NO_NATIVE_CORRECTION']}


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def encode(data):
    return json.dumps(data, indent=2) + '\n'


def build():
    contract = l.contract()
    report = json.loads((OUT / 'report.json').read_text())
    for path, digest in report['inputs_sha256'].items():
        if sha(path) != digest:
            raise ValueError('Stale lineage receipt: ' + path)
    cases = {row['id']: row for row in report['cases']}
    if len(cases) != 54 or report['summary']['outcomes'] != {'PASS': 54} or set().union(*map(set, GROUPS.values())) != set(cases):
        raise ValueError('Incomplete lineage execution/requirement trace')
    model = json.loads((ROOT / 'ontology/riskium-model.json').read_text())
    source = {row['id']: row for family in ('concepts', 'imported_types', 'associations', 'generalizations', 'constraints') for row in model[family]}
    baseline = 'evaluation/relational/source-scenario/mapping-accounting.json'
    old = json.loads((ROOT / baseline).read_text())
    rows = old['rows']
    if len(source) != len(rows) or len(source) != 306 or set(source) != {row['id'] for row in rows}:
        raise ValueError('Lost native source identities')
    for row in rows:
        actual = hashlib.sha256(json.dumps(source[row['id']], sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
        if row['source_sha256'] != actual:
            raise ValueError('Native source drift: ' + row['id'])
        row['lineage_overlay'] = ('SCOPED_APPLICATION_CORRECTION for the two knowledge classes; native disposition unchanged.'
                                  if row['id'] in {'RKM-C003', 'RKM-X06', 'C-03', 'C-17'}
                                  else 'NO_ADDITIONAL_MAPPING_OR_LINEAGE_IMPLEMENTATION')
    dispositions = dict(Counter(row['disposition'] for row in rows))
    if dispositions != old['current_dispositions'] or old['remaining_deferred'] != 242:
        raise ValueError('Native mapping scope promoted')
    inventory = dict(schema='riskium-source-scenario-lineage-accounting-v1', profile='0.5.0',
                     baseline_path=baseline, baseline_sha256=sha(baseline), source_elements=306,
                     source_sha256=sha('ontology/riskium-model.json'), current_dispositions=dispositions,
                     remaining_deferred=242, retained_partial_source_scenario_routes=8,
                     new_native_classes=0, new_native_properties=0, new_native_mapping_routes=0,
                     full_mapping_completed=False, rows=rows)
    req_ids = {row['id'] for row in json.loads((ROOT / 'requirements/requirements.json').read_text())}
    requirements = []
    for req in contract['requirements']:
        if not set(req['source_requirements']).issubset(req_ids):
            raise ValueError('Unknown original requirement')
        requirements.append(dict(requirement=req, cqs=['RQ-CQ02', 'RQ-CQ06', 'RQ-CQ08'],
                                 case_ids=GROUPS[req['id']], implementation=['006_source_scenario_lineage.sql', 'queries/family.sql', 'relational_source_scenario_lineage.py'],
                                 status='SCOPED_EXECUTED_ENGINEERING',
                                 limit='Selected application correction for two issued knowledge classes; no general native correction, complete original fulfillment or independent semantic acceptance.'))
    paths = set(report['inputs_sha256']) | set(contract['source_sha256']) | {
        baseline, 'implementation/relational/0.5.0/README.md', 'implementation/relational/0.5.0/schema-dictionary.md',
        'evaluation/relational/source-scenario-lineage/report.json', 'evaluation/relational/source-scenario-lineage/README.md',
        'tests/test_source_scenario_lineage.py', 'tools/build_source_scenario_lineage_inventory.py',
        'evaluation/sources/cq0708/cohort.json', 'evaluation/sources/cq0708/report.json.gz'}
    inputs = {path: sha(path) for path in sorted(paths)}
    trace = dict(schema='riskium-source-scenario-lineage-requirement-trace-v1', profile='0.5.0', execution_issue=43,
                 parent_issues=[35, 12], original_drsd='0.1.0 unchanged; SCL-01..06 are an explicit derived supplement',
                 requirements=requirements, inputs_sha256=inputs,
                 original_organizational_admissions='All 11 WITHHELD; no new admission or independent rating')
    outputs = {'evaluation/relational/source-scenario-lineage/mapping-accounting.json': encode(inventory),
               'evaluation/relational/source-scenario-lineage/traceability.json': encode(trace)}
    component = dict(schema='riskium-source-scenario-lineage-component-v1', id='SOURCE_SCENARIO_LINEAGE',
                     version='0.5.0', schema_version=6, compatible_model='0.3.1', baseline_sql_profile='0.4.0',
                     status='DEVELOPMENT_COMPONENT_NOT_SELECTED_BY_STABLE_DISTRIBUTION', stable_distribution_unchanged='v0.3.3',
                     summary=report['summary'], native_support=dict(new_classes=0, new_properties=0, new_mapping_routes=0, full_mapping_completed=False),
                     files_sha256=dict(inputs, **{p: hashlib.sha256(data.encode()).hexdigest() for p, data in outputs.items()}))
    outputs['implementation/relational/0.5.0/component.json'] = encode(component)
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, data in build().items():
        path = ROOT / name
        if args.check:
            if not path.is_file() or path.read_text() != data:
                raise ValueError('Stale lineage accounting: ' + name)
        else:
            path.write_text(data)
    print(encode(dict(status='SOURCE_SCENARIO_LINEAGE_ACCOUNTING_PASS', native_elements=306,
                      new_native_mapping_routes=0, requirements=6)))


if __name__ == '__main__':
    main()
