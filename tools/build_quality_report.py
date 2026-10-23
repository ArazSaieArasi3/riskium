"""Synthesize claim-scoped quality evidence without running scientific engines."""
from pathlib import Path
from collections import Counter
import argparse
import gzip
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
POLICY = 'evaluation/quality/policy.json'
INPUTS = [
    'ontology/riskium-model.json', 'ontology/derived/riskium.owl.ttl',
    'evaluation/coverage-contract.json', 'evaluation/coverage-review.json',
    'evaluation/native-stage-receipt.json', 'evaluation/owl-mapping-receipt.json',
    'evaluation/hermit/report.json', 'evaluation/shacl/coverage-status.json',
    'evaluation/shacl/report.json', 'evaluation/shacl/endpoints/report.json',
    'evaluation/shacl/admission/report.json.gz', 'evaluation/shacl/coherence/report.json',
    'evaluation/shacl/qualification/report.json.gz', 'evaluation/c14-boundary-review.json',
    'evaluation/cq/report.json', 'evaluation/traceability/ledger.json',
    'evaluation/semantic-review-register.json', 'evaluation/references/report.json',
    'references/corpus.json', 'evaluation/documentation-audit.json',
    'evaluation/semantic-assurance-plan.md', 'docs/first-release-profile.md',
]
# These documents are historical evidence, not dependencies on mutable new projections.
HISTORICAL = {'evaluation/documentation-audit.json', 'evaluation/semantic-assurance-plan.md', 'docs/first-release-profile.md'}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_inputs(policy):
    data, inventory = {}, {}
    checkpoint = policy['evidence_checkpoint_commit']
    for name in INPUTS:
        raw = subprocess.check_output(['git', 'show', checkpoint + ':' + name], cwd=ROOT)
        if name not in HISTORICAL:
            require((ROOT / name).read_bytes() == raw, 'Evidence changed since checkpoint; review the synthesis binding: ' + name)
        inventory[name] = {'commit': checkpoint, 'sha256': digest(raw), 'working_copy_checked': name not in HISTORICAL}
        decoded = gzip.decompress(raw) if name.endswith('.gz') else raw
        data[name] = json.loads(decoded) if '.json' in name else decoded.decode()
    for name in ['ontology/riskium-model.json', 'ontology/derived/riskium.owl.ttl']:
        frozen = subprocess.check_output(['git', 'show', policy['semantic_source_commit'] + ':' + name], cwd=ROOT)
        require(inventory[name]['sha256'] == digest(frozen), 'Semantic source changed from the released model')
    return data, inventory


def fraction(numerator, denominator):
    return {'numerator': numerator, 'denominator': denominator,
            'percent': round(100 * numerator / denominator, 2) if denominator else None}


def ledger_counts(rows, expected_total, declared):
    require(len(rows) == expected_total and len({r['id'] for r in rows}) == expected_total, 'Obligation denominator or identity mismatch')
    actual = dict(Counter(r['outcome'] for r in rows))
    require(actual == {k: v for k, v in declared.items() if v}, 'Declared obligation counts hide row outcomes')
    return actual


def assemble(policy, d, inventory):
    model = d['ontology/riskium-model.json']
    h = d['evaluation/hermit/report.json']
    s = d['evaluation/shacl/coverage-status.json']
    cq = d['evaluation/cq/report.json']
    trace = d['evaluation/traceability/ledger.json']
    sem = d['evaluation/semantic-review-register.json']
    refs = d['evaluation/references/report.json']
    corpus = d['references/corpus.json']
    allocation = d['evaluation/coverage-review.json']['summary']
    model_hash = inventory['ontology/riskium-model.json']['sha256']
    require(h['inputs']['owl_turtle_sha256'] == inventory['ontology/derived/riskium.owl.ttl']['sha256'], 'HermiT OWL mismatch')
    require(h['inputs']['mapping_receipt_sha256'] == inventory['evaluation/owl-mapping-receipt.json']['sha256'], 'HermiT mapping mismatch')
    contract_hash = inventory['evaluation/coverage-review.json']['sha256']
    require(h['inputs']['contract_sha256'] == s['contract_sha256'] == contract_hash, 'Formal contract mismatch')
    require(s['source_sha256'] == sem['model_sha256'] == corpus['model_sha256'] == model_hash, 'Evidence model mismatch')
    require(allocation['by_engine'] == {'Combined': 20, 'HermiT': 295, 'SHACL': 359} and allocation['baseline_obligations'] == 674, 'Changed predeclared allocation')
    hc = ledger_counts(h['obligations'], 295, h['coverage']['outcomes'])
    sc = ledger_counts(s['obligations'], 359, s['outcomes'])
    modules = []
    for entry in s['evidence']:
        p = entry['path']; r = d[p]
        require(entry['sha256'] == inventory[p]['sha256'] and entry['source_commit'] == r['source_commit'], 'SHACL evidence-chain mismatch: ' + p)
        require(r['inputs']['ontology/riskium-model.json'] == model_hash, 'SHACL module model mismatch')
        cases = r['cases']
        runs = [c for c in cases if c.get('engine_executed', True)]
        modules.append({'receipt': p, 'recorded_source_commit': r['source_commit'], 'scenarios': len(cases),
                        'engine_executions': len(runs), 'engine_outcomes': dict(sorted(Counter(c['status'] for c in runs).items())),
                        'preflight_outcomes': dict(sorted(Counter(c['status'] for c in cases if not c.get('engine_executed', True) and c['status'] != 'BLOCKED').items())),
                        'blocked_scenarios': [c['id'] for c in cases if c['status'] == 'BLOCKED']})
    answers = [c for c in cq['cases'] if c['kind'] != 'query_mutant']
    mutants = [c for c in cq['cases'] if c['kind'] == 'query_mutant']
    require(len(answers) == cq['summary']['answer_cases'] and len(mutants) == cq['summary']['mutation_controls'], 'CQ answer/mutant denominator mismatch')
    require(all(not c['error'] for c in cq['cases'] if c['status'] == 'PASS'), 'CQ error incorrectly labeled PASS')
    answer_pass = sum(c['status'] == 'PASS' and c['oracle_matched'] and not c['error'] for c in answers)
    require(all(not c['oracle_matched'] and c['observed_rows'] != c['expected_rows'] for c in mutants if c['status'] == 'PASS'), 'Query mutant incorrectly credited without changed answers')
    mutant_pass = sum(c['status'] == 'PASS' and not c['error'] and not c['oracle_matched'] for c in mutants)
    require(len(cq['cases']) == cq['summary']['query_executions'] == 40, 'CQ execution denominator changed')
    contracts = cq['contracts']
    original_executed = sum(c['source_population_execution'] == 'EXECUTED_SYNTHETIC_QUERY_CONTRACT' for c in contracts)
    require(len(contracts) == 8 and original_executed == cq['summary']['source_synthetic_task_contracts_executed'], 'Source population accounting mismatch')
    require(len(trace['rows']) == 28 and len({r['id'] for r in trace['rows']}) == 28, 'Trace row identities differ')
    require(dict(Counter(r['kind'] for r in trace['rows'])) == {'requirement': 12, 'scope': 8, 'competency_question': 8}, 'Trace population changed')
    require(trace['summary']['full_requirement_acceptance_claimed'] is False, 'Trace completeness cannot establish full acceptance')
    trace_states = dict(sorted(Counter(r['acceptance_state'] for r in trace['rows']).items()))
    require(trace_states == trace['summary']['acceptance_states'], 'Trace acceptance counts differ')
    group_counts = dict(Counter(g['cohort'] for g in sem['groups']))
    require(group_counts == sem['cohorts'], 'Independent review cohort mismatch')
    adjudicated = [g for g in sem['groups'] if g['adjudication'] is not None]
    # A new review requires a reviewed rating schema, not automatic label guessing.
    require(not adjudicated and not any(g['independent_ratings'] for g in sem['groups']), 'New independent judgments require explicit synthesis/rating review')
    require(refs['counts']['sources'] == len(corpus['sources']) and refs['counts']['interpretations'] == len(corpus['interpretations']), 'Source corpus denominator mismatch')
    require(refs['inputs_sha256']['references/corpus.json'] == inventory['references/corpus.json']['sha256'], 'Source corpus hash mismatch')
    constraints = []
    h_rows = {r['source_element']: r for r in h['obligations'] if r['source_element'].startswith('C-')}
    s_rows = {r['source_element']: r for r in s['obligations'] if r['source_element'].startswith('C-')}
    for c in model['constraints']:
        ident = c['id']; hr = h_rows[ident]; sr = s_rows[ident]
        open_route = hr['outcome'] != 'PASS' or sr['outcome'] != 'PASS'
        follow = policy['constraint_follow_up'].get(ident)
        require(not open_route or follow is not None, 'Unowned formal gap: ' + ident)
        constraints.append({'id': ident, 'title': c['title'], 'hermit': {'id': hr['id'], 'outcome': hr['outcome']},
                            'shacl': {'id': sr['id'], 'outcome': sr['outcome']}, 'open_route': open_route,
                            'follow_up': follow, 'independent_semantic_acceptance': 'NOT_ESTABLISHED'})
    reconciliations = {r['id']: r for r in policy['trace_reconciliation']}
    for r in trace['rows']:
        if r['id'] in reconciliations:
            require(r['acceptance_state'] == reconciliations[r['id']]['recorded_state'], 'Stale trace overlay')
    return {
        'schema_version': 1, 'status': 'SYNTHESIS_COMPLETE_SCIENTIFIC_ACCEPTANCE_NOT_ESTABLISHED', 'integrity_status': 'PASS',
        'report_date': policy['report_date'], 'model_version': model['version'], 'semantic_source_commit': policy['semantic_source_commit'],
        'evidence_checkpoint_commit': policy['evidence_checkpoint_commit'], 'source_inventory': inventory,
        'synthesis_inputs_sha256': {p: digest((ROOT / p).read_bytes()) for p in [POLICY, 'tools/build_quality_report.py', 'tests/test_quality.py']},
        'new_scientific_engine_executions': 0, 'overall_semantic_correctness_percent': None,
        'metrics': {
            'Q-01': {'catalog_concepts': len(model['concepts']), 'typed_core': sum(c['scope_layer'] == 'FORMAL_CORE' for c in model['concepts']), 'optional_boundaries': sum(c['scope_layer'] == 'OPTIONAL_PHENOMENON_BOUNDARY' for c in model['concepts']), 'imported_anchors_separate': len(model['imported_types']), 'associations_bridges': len(model['associations']), 'generalizations': len(model['generalizations']), 'constraints': len(model['constraints'])},
            'Q-02': {**fraction(hc.get('PASS', 0), 295), 'outcomes': hc},
            'Q-03': {**fraction(sum(c['status'] == 'PASS' for c in h['cases']), len(h['cases'])), 'recorded_source_commit': h['source_commit'], 'case_statuses': dict(Counter(c['status'] for c in h['cases']))},
            'Q-04': {**fraction(sc.get('PASS', 0), 359), 'outcomes': sc},
            'Q-05': fraction(answer_pass, len(answers)), 'Q-06': fraction(mutant_pass, len(mutants)),
            'Q-07': {**fraction(original_executed, len(contracts)), 'original_population_pending': [c['cq_id'] for c in contracts if c['source_population_execution'] != 'EXECUTED_SYNTHETIC_QUERY_CONTRACT'], 'independent_real_data_acceptance': 'NOT_ESTABLISHED'},
            'Q-08': {**fraction(sum(r['trace_status'] == 'COMPLETE' for r in trace['rows']), 28), 'original_acceptance_states': trace_states, 'full_requirement_acceptance': False, 'scope_rows_outside_674': 8},
            'Q-09': {**fraction(0, group_counts['core']), 'cohorts': group_counts, 'independent_adjudications_all_cohorts': 0},
            'Q-10': {**fraction(0, 0), 'status': 'UNDEFINED_NO_INDEPENDENT_ADJUDICATIONS_OR_ACCEPTANCE_SCHEMA'},
            'Q-11': {'counts': refs['counts'], 'independent_mapping_acceptance': 'NOT_ESTABLISHED'},
            'Q-12': {'status': 'NOT_ESTABLISHED', 'numerator': None, 'denominator': None, 'percent': None, 'issues': [7, 13]},
            'Q-13': {'status': 'NOT_ESTABLISHED', 'numerator': None, 'denominator': None, 'percent': None, 'issues': [12]},
            'Q-14': {'status': 'HISTORICAL_VERSION_BOUND_EVIDENCE_RETAINED_NOT_RERUN_BY_SYNTHESIS', 'native_checks': d['evaluation/native-stage-receipt.json']['checks'], 'historical_documentation_audit': d['evaluation/documentation-audit.json'], 'historical_release_profile': 'docs/first-release-profile.md at evidence checkpoint', 'manuscript_review': 'NOT_ESTABLISHED', 'issues': [14]}
        },
        'shacl_modules': modules, 'constraint_rows': constraints,
        'trace_rows': [{'id': r['id'], 'recorded_state': r['acceptance_state'], 'remaining_obligation_as_recorded': r['remaining_obligation'], 'post_trace_reconciliation': reconciliations.get(r['id'])} for r in trace['rows']],
        'source_limits': corpus['open_limits'], 'trace_reconciliation': policy['trace_reconciliation'],
        'framework_decisions': policy['framework_decisions'], 'judgment': policy['judgment'],
        'claim_ceiling': 'Bounded versioned verification and synthetic retrieval plus a source-qualified editorial corpus; no independent semantic acceptance, full normative conformance, held-out applicability or stable scientific validation.'
    }


def render(report, policy):
    metrics = report['metrics']
    lines = ['# Claim-based quality and evidence report', '',
             '**Report milestone complete; independent scientific acceptance is not established.** This post-prerelease synthesis is dated ' + report['report_date'] + ', for conceptual design ' + report['model_version'] + ' at `' + report['semantic_source_commit'] + '`. Evidence is pinned at checkpoint `' + report['evidence_checkpoint_commit'] + '`; individual receipts retain their original execution provenance. This report runs no HermiT, SHACL or CQ engine.', '',
             'The [policy and metric definitions](policy.json) are the interpretation contract; the [machine-readable report](report.json) preserves counts, source hashes, all 25 constraint rows, all 28 trace rows and limitations. Its integrity PASS checks accounting, not domain truth.', '',
             '## Measurement contract', '', policy['metric_timing'], '', policy['aggregation_policy'], '',
             '| ID / measure | Unit and numerator | Denominator | Permitted interpretation |', '| --- | --- | --- | --- |']
    for m in policy['metric_definitions']:
        lines.append('| ' + ' | '.join([m['id'] + ' / ' + m['name'], m['unit'] + ': ' + m['numerator'], m['denominator'], m['interpretation']]) + ' |')
    lines += ['', '## Evidence and bounded claims', '', '| Measure | Observed result | Claim restriction / next route |', '| --- | --- | --- |']
    observations = {
        'Q-01': ('; '.join(str(v) + ' ' + k.replace('_', ' ') for k, v in metrics['Q-01'].items()), 'Inventory only; neither a taxonomy score nor quality evidence.'),
        'Q-02': ('281/295 scoped PASS (95.25%); 14 NOT_RUN', 'Formal encoding coverage; #4 remains open.'),
        'Q-03': ('693/693 recorded matching cases', 'Finite original fixture suite; not 693 independent domain samples or 295 reviewed meanings.'),
        'Q-04': ('341/359 scoped PASS (94.99%); 1 PARTIAL; 17 NOT_RUN', 'C-08 compatibility and complete profile integration remain #5; no global conformance claim.'),
        'Q-05': ('32/32 exact synthetic answer cases', 'No OWL inference or independently specified held-out population; native/supplementary profile limits remain.'),
        'Q-06': ('8/8 successfully executed/detected query mutants', 'Errors are not mutation detection; only the declared mutants were measured.'),
        'Q-07': ('5/8 original population contracts executed; CQ06–CQ08 pending', 'Synthetic controls for all eight do not execute the three independent populations (#13).'),
        'Q-08': ('28/28 public traces; 12 requirements, 8 scope obligations, 8 CQs', 'Trace completeness is not 28 accepted requirements; original per-row statuses and later overlay remain separate.'),
        'Q-09': ('0/295 core groups independently adjudicated; separate 4 boundary + 20 original acceptance groups', '0% review completion, not 0% correctness. Eight later scope traces do not silently enlarge this original review cohort (#7).'),
        'Q-10': ('Undefined; zero independently adjudicated groups', 'No semantic acceptance rate, overall correctness or confidence interval is estimated.'),
        'Q-11': ('11 sources; 19 dated locators; 13 author-side interpretations, including 1 NOT_ASSESSED', 'Source register complete within #8 scope; four limits and uninspected clauses remain (#7/#14).'),
        'Q-12': ('Not established in these public receipts', 'Independent real/held-out case acceptance remains #7/#13; 11 source scenarios are not fabricated organizational cases.'),
        'Q-13': ('Not established', 'Relational/application reconciliation, immutable history and calculation validation remain #12.'),
        'Q-14': ('Version-bound native, mapping, engine, query, source and historical publication receipts retained', 'Release freeze was 21 commands/79 regressions at the release; later #6 reported 89 regressions. Neither is a new run by this synthesis; manuscript #14 remains open.')
    }
    # Ensure rendered headline numbers cannot silently drift from the checked snapshot.
    require(metrics['Q-02']['outcomes'] == {'PASS': 281, 'NOT_RUN': 14} and metrics['Q-03']['numerator'] == metrics['Q-03']['denominator'] == 693 and metrics['Q-04']['outcomes'] == {'PASS': 341, 'PARTIAL': 1, 'NOT_RUN': 17}, 'Review narrative for changed formal evidence')
    require(metrics['Q-05']['numerator'] == 32 and metrics['Q-06']['numerator'] == 8 and metrics['Q-07']['numerator'] == 5, 'Review narrative for changed CQ evidence')
    for m in policy['metric_definitions']:
        observed, limit = observations[m['id']]
        lines.append('| ' + m['id'] + ' | ' + observed + ' | ' + limit + ' |')
    lines += ['', '## Module populations and exclusions', '',
              'Each module uses its own focus/identity/inference policy. A matched negative test means the expected rejection occurred, not that invalid data conformed. Do not sum these fixture families into independent scientific samples or a quality score.', '',
              '| Receipt | Original source commit | Scenarios | Engine executions | Engine outcomes | Preflight outcomes / blocked scenarios |', '| --- | --- | ---: | ---: | --- | --- |']
    for r in report['shacl_modules']:
        lines.append('| ' + ' | '.join(['[' + r['receipt'] + '](../../' + r['receipt'] + ')', '`' + r['recorded_source_commit'] + '`', str(r['scenarios']), str(r['engine_executions']), str(r['engine_outcomes']), str(r['preflight_outcomes']) + ' / ' + ', '.join(r['blocked_scenarios'])]) + ' |')
    lines += ['', 'The conditional batch retains its pre-validation identity rejection and blocked C-08 task. C-14 structural reconciliation reuses 12 earlier admission cases and adds **zero** engine executions or formal PASS rows. Historical planning labels in the source/coverage files are not current execution outcomes.', '',
              '## All interpretation-constraint routes', '',
              'The two fixed engine denominators remain separate. A scoped pass in one engine never discharges the other engine\'s unexecuted row. All meanings still require independent review; this table reports encoded/exercised scope, not 25 independent semantic approvals.', '',
              '| Constraint | HermiT row | SHACL row | Remaining route / owner |', '| --- | --- | --- | --- |']
    for r in report['constraint_rows']:
        follow = r['follow_up']
        route = follow['route'] + ' (' + ', '.join('#' + str(n) for n in follow['issues']) + ')' if follow else 'Both engine rows have scoped PASS; full semantic adequacy remains #7.'
        lines.append('| ' + r['id'] + ' — ' + r['title'] + ' | ' + r['hermit']['id'] + ' ' + r['hermit']['outcome'] + ' | ' + r['shacl']['id'] + ' ' + r['shacl']['outcome'] + ' | ' + route + ' |')
    lines += ['', '## Requirements and post-trace reconciliation', '',
              'The original 28-row ledger remains unchanged at its actual provenance. Its acceptance-state distribution is `' + json.dumps(metrics['Q-08']['original_acceptance_states'], sort_keys=True) + '`. The JSON report retains every row and its recorded remaining obligation. The following explicit overlay accounts for later evidence and reroutes remaining tasks; it does not rewrite historical statuses or count an editorial result as a formal pass.', '',
              '| Source row | Recorded state | Current synthesis disposition | Evidence / remaining owner |', '| --- | --- | --- | --- |']
    for r in policy['trace_reconciliation']:
        lines.append('| ' + ' | '.join([r['id'], r['recorded_state'], r['current_disposition'], r['evidence'] + '. ' + r['reason'] + ' Follow-up: ' + ', '.join('#' + str(n) for n in r['issues'])]) + ' |')
    lines += ['', '## Quality-framework adoption decisions', '']
    for r in policy['framework_decisions']:
        src = '[' + r['source'] + '](' + r['source'] + ')' if r['source'].startswith('https://') else r['source']
        lines += ['- **' + r['candidate'] + ': ' + r['decision'] + '.** ' + r['basis'] + ' Source: ' + src + '.', '']
    lines += ['Verification, validation, evaluation, assessment and assurance are separated here by the evidence question and intended use. They are not asserted to be a universal linear lifecycle or a newly implemented external standard.', '',
              '## Judgment and remaining claim limits', '', report['judgment']['reason'], '',
              '- Development prerelease: published within its historical bounded profile.',
              '- This quality-report milestone: complete for claim/evidence synthesis.',
              '- Independent semantic acceptance, full normative acceptance, held-out applicability and operational preservation: not established.',
              '- Overall semantic-correctness percentage and number of critical semantic findings: **unestimated**, not zero.', '',
              'The four source-review limits remain:', '']
    for r in report['source_limits']:
        lines.append('- ' + r['id'] + ': ' + r['limitation'] + ' (#' + '/#'.join(map(str, r['owner_issues'])) + ').')
    lines += ['', 'Next apply this report to the latest author-approved manuscript and a location-specific claim/number ledger (#14). Formal/application work remains #4/#5/#12, independent review #7 and independently prepared case/CQ populations #13. Future extension tracking #16 does not become a validated capability. No manuscript was reviewed or modified by this synthesis.', '',
              '## Exact source binding and reproduction', '',
              'All entries below are read at the evidence checkpoint. Scientific receipts must also match the working bytes; the historical assurance plan, documentation audit and release profile are intentionally read as historical versions to avoid circular dependence on new guide pages. Each receipt keeps its original execution commit as well. The new policy and generator hashes are in report.json.', '',
              '| Source at checkpoint | SHA-256 |', '| --- | --- |']
    base = 'https://github.com/ArazSaieArasi3/riskium/blob/' + report['evidence_checkpoint_commit'] + '/'
    for p, r in report['source_inventory'].items():
        lines.append('| [' + p + '](' + base + p + ') | `' + r['sha256'] + '` |')
    lines += ['', '```sh', 'python3 tools/build_quality_report.py --check', '```', '',
              'Without `--check`, regenerate only after deliberately reviewing the source bindings and policy. This command verifies provenance, hashes, row-level denominators, module accounting, error/mutation handling, independent-review absence and named gap ownership. It recomputes the synthesis, not the scientific executions. A current CI or website deployment is separate publication evidence.']
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    policy = json.loads((ROOT / POLICY).read_text())
    d, inventory = load_inputs(policy)
    report = assemble(policy, d, inventory)
    outputs = {'evaluation/quality/report.json': json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + '\n',
               'evaluation/quality/README.md': render(report, policy)}
    for name, content in outputs.items():
        p = ROOT / name
        if args.check:
            require(p.exists() and p.read_text() == content, 'Stale quality synthesis: ' + name)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
    print(json.dumps({'integrity': report['integrity_status'], 'status': report['status'], 'metrics': len(policy['metric_definitions']), 'constraint_rows': len(report['constraint_rows']), 'trace_rows': len(report['trace_rows']), 'new_scientific_engine_executions': 0}))


if __name__ == '__main__':
    main()
