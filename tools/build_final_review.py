"""Reconcile a historical evidence checkpoint into a proposed final-review package.

This is evidence accounting: no scientific engine execution or owner judgment.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evaluation/final-review'
EVIDENCE = {
    'model': ['ontology/riskium-model.json'],
    'native': ['evaluation/native-stage-receipt.json', 'evaluation/native-exchange-checks.json', 'evaluation/native-roundtrip-checks.json'],
    'owl': ['evaluation/owl-mapping-receipt.json', 'ontology/derived/riskium.owl.ttl'],
    'h': ['evaluation/hermit/report.json'],
    'conditional': ['evaluation/shacl/coverage-status.json', 'evaluation/shacl/report.json', 'evaluation/shacl/endpoints/report.json'],
    'admission': ['evaluation/shacl/admission/report.json.gz'],
    'coherence': ['evaluation/shacl/coherence/report.json'],
    'qualification': ['evaluation/shacl/qualification/report.json.gz'],
    'compatibility': ['evaluation/shacl/compatibility/report.json.gz'],
    'comparison': ['evaluation/shacl/comparison/report.json.gz'],
    'sql': ['evaluation/relational/history/report.json.gz'],
    'source6': ['evaluation/sources/cq06/report.json.gz'],
    'source78': ['evaluation/sources/cq0708/report.json.gz'],
    'boundary': ['evaluation/c14-boundary-review.json'],
    'references': ['evaluation/references/report.json', 'references/corpus.json'],
    'trace': ['evaluation/traceability/ledger.json', 'requirements/requirements.json', 'requirements/scope-requirements.json', 'requirements/competency-questions.json'],
    'cq': ['evaluation/cq/report.json'],
    'quality': ['evaluation/quality/report.json'],
    'manuscript': ['evaluation/manuscript-review/ledger.json'],
    'owner': ['evaluation/owner-review/register.json'],
    'publication': ['docs/first-release-profile.md'] + [f'evaluation/releases/v0.3.1-rc.{n}-publication.json' for n in range(2, 8)],
    'documentation': ['evaluation/documentation-audit.json'],
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def build():
    policy_bytes = (OUT / 'policy.json').read_bytes()
    manuscript_bytes = (OUT / 'manuscript-proposals.json').read_bytes()
    policy, amendments = json.loads(policy_bytes), json.loads(manuscript_bytes)
    checkpoint = policy['evidence_checkpoint_commit']
    sources, registry = {}, {}
    for key, paths in EVIDENCE.items():
        registry[key] = []
        for path in paths:
            data = subprocess.check_output(['git', '-C', str(ROOT), 'show', checkpoint + ':' + path])
            # This review remains a dated snapshot when the owner's live register evolves.
            # Other mutable prose is also read from its named checkpoint, not HEAD.
            frozen_only = key in ('owner', 'documentation') or path.endswith('.md')
            if not frozen_only:
                require((ROOT / path).read_bytes() == data, 'Evidence changed after checkpoint: ' + path)
            sources[path] = data
            registry[key].append({'path': path, 'sha256': digest(data), 'checkpoint': checkpoint,
                                  'current_equality_required': not frozen_only})

    def source(key):
        path = EVIDENCE[key][0]
        data = sources[path]
        return json.loads(gzip.decompress(data) if path.endswith('.gz') else data)

    def ids(rows):
        result = [r['id'] for r in rows]
        require(len(result) == len(set(result)), 'Duplicate row IDs')
        return set(result)

    model, h, sh = source('model'), source('h'), source('conditional')
    trace, owner, ledger = source('trace'), source('owner'), source('manuscript')
    proposals = {r['id']: r for r in policy['constraints']}
    require(ids(model['constraints']) == ids(policy['constraints']) and len(proposals) == 25, 'Need all 25 clauses')
    require(set(policy['trace_proposals']) == ids(trace['rows']) and len(trace['rows']) == 28, 'Need all 28 trace rows')
    require(ids(owner['rows']) == ids(policy['owner_proposals']) and len(owner['rows']) == 11, 'Need all 11 owner prompts')
    require(owner['ratings_recorded'] == 0 and all(r['owner_rating'] is None for r in owner['rows']), 'Checkpoint owner snapshot unexpected')
    require(len(policy['claims']) == 12 and len(ids(policy['claims'])) == 12, 'Need all claim groups')
    require(len(ledger['rows']) == 65 and len(ids(ledger['rows'])) == 65, 'Need all manuscript claims')
    require(policy['final_release_ready'] is False and policy['critical_findings_count'] is None, 'No final acceptance inferred')
    require(policy['owner_judgments_generated'] == policy['new_scientific_engine_executions'] == 0, 'Preparation only')
    require(policy['overall_semantic_correctness_percent'] is None and policy['full_requirement_acceptance_claimed'] is False, 'No correctness or acceptance percentage')
    for group in ('constraints', 'claims', 'owner_proposals'):
        for row in policy[group]:
            require(all(k in EVIDENCE for k in row['evidence_keys']), 'Unknown evidence reference')
            require(row.get('owner_disposition') is None and row.get('owner_rating') is None and row.get('owner_response') is None, 'No proposal is an owner judgment')
    for row in policy['trace_proposals'].values():
        require(row['owner_disposition'] is None, 'No trace acceptance inferred')
        require(set(row['constraint_ids']) <= set(proposals), 'Unknown clause in trace')
    constraints = []
    routes = []
    for clause in model['constraints']:
        cid = clause['id']
        original = {name: [r for r in receipt['obligations'] if r.get('source_element') == cid]
                    for name, receipt in [('HermiT', h), ('SHACL', sh)]}
        require(all(len(v) == 1 for v in original.values()), 'Every clause needs exactly one row per ledger')
        constraints.append({'source_clause': clause, 'historical_obligations': original, **proposals[cid]})
        for engine, rows in original.items():
            for row in rows:
                if row['outcome'] == 'NOT_RUN':
                    routes.append({'engine': engine, 'original_obligation': row,
                                   'constraint_id': cid, 'proposal': proposals[cid],
                                   'disposition_kind': 'PROPOSED_CURRENT_ALTERNATIVE_OR_EXCLUSION_NOT_ENGINE_DISCHARGE'})
    require(Counter(r['engine'] for r in routes) == {'HermiT': 14, 'SHACL': 17}, 'Need all 31 historical unexecuted routes')
    require(Counter(r['outcome'] for r in h['obligations']) == {'PASS': 281, 'NOT_RUN': 14}, 'HermiT ledger changed')
    require(Counter(r['outcome'] for r in sh['obligations']) == {'PASS': 341, 'PARTIAL': 1, 'NOT_RUN': 17}, 'SHACL ledger changed')
    require(len(amendments['rows']) == amendments['proposal_count'] == 7, 'Need 7 exact manuscript proposals')
    require(amendments['source_file_modified'] is False and amendments['new_docx_or_pdf_created'] is False, 'No manuscript application claimed')
    artifact_hashes = {r['filename']: r['sha256'] for r in ledger['artifacts']}
    for artifact in amendments['artifacts']:
        require(artifact_hashes[artifact['filename']] == artifact['sha256'], 'Manuscript hash mismatch')
    for row in amendments['rows']:
        require(row['status'] == 'PROPOSED_NOT_APPLIED' and row['owner_disposition'] is None, 'Unapproved manuscript amendment')
        require(len(row['source_paragraph_sha256']) == 64 and row['proposed_text'], 'Exact amendment binding missing')
    # Retain original criterion, priority/source rule, original acceptance state and
    # remaining obligation. Current proposals are a separate overlay, never edits.
    original_definitions = {r['id']: r for path in EVIDENCE['trace'][1:] for r in json.loads(sources[path])}
    require(set(original_definitions) == ids(trace['rows']), 'Trace definitions missing')
    require(Counter(r.get('priority') for r in original_definitions.values()) == {None: 16, 'MUST': 11, 'SHOULD': 1}, 'Original priorities changed')
    traces = [{'original_definition': original_definitions[r['id']], 'original': {k: v for k, v in r.items() if k != 'formal_evidence'},
               'original_complete_row_sha256': digest(encoded(r)),
               'original_formal_evidence_count': len(r.get('formal_evidence', [])),
               'proposal': policy['trace_proposals'][r['id']]} for r in trace['rows']]
    populations = {k: source(k)['summary'] for k in ('compatibility', 'comparison', 'sql', 'source6', 'source78')}
    report = {
        'schema': 'riskium-final-review-report-v1', 'target': policy['target'],
        'evidence_checkpoint_commit': checkpoint, 'status': policy['status'],
        'input_sha256': {'evaluation/final-review/policy.json': digest(policy_bytes),
                         'evaluation/final-review/manuscript-proposals.json': digest(manuscript_bytes)},
        'evidence_registry': registry, 'claims': policy['claims'], 'constraints': constraints,
        'historical_not_run_routes': routes,
        'historical_c08_partial': [r for r in sh['obligations'] if r['outcome'] == 'PARTIAL'],
        'trace_rows': traces, 'manuscript_baseline_claims': ledger['rows'],
        'manuscript_amendments': amendments, 'owner_checkpoint_snapshot': owner,
        'owner_proposals': policy['owner_proposals'], 'method_specific_supplements': populations,
        'summary': {'clauses': 25, 'historical_not_run_routes': 31, 'hermit_not_run': 14,
                    'shacl_not_run': 17, 'trace_rows': 28, 'baseline_manuscript_claims': 65,
                    'proposed_manuscript_amendments': 7, 'owner_prompts': 11,
                    'owner_ratings_at_checkpoint': 0, 'new_owner_ratings': 0,
                    'new_scientific_engine_executions': 0, 'final_release_ready': False,
                    'critical_findings_count': None, 'semantic_correctness_percent': None},
        'critical_screen': policy['critical_screen'], 'blocked_until_review': policy['blocked_until_review'],
        'future_ownership': policy['future_ownership'],
        'limits': ['All dispositions are assistant proposals. Actual judgments remain in #7; the historical owner snapshot does not constrain later real ratings.',
                   'Counts are method-specific, overlapping populations. They are not summed into accuracy, coverage or scientific acceptance.',
                   'MUST priorities and original acceptance criteria are preserved. Any narrowed current executable scope needs explicit owner acceptance.',
                   'Historical NOT_RUN/PARTIAL outcomes and original 5/8 CQ population checkpoint remain unchanged; supplements do not rewrite them.',
                   'No unresolved critical in-scope identity, forbidden-inference, integrity or data-loss finding may be deferred simply to ship.'],
    }
    outputs = {'report.json': encoded(report)}

    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', '<br>')

    def table(headers, rows):
        return '| ' + ' | '.join(headers) + ' |\n|' + '|'.join([' --- '] * len(headers)) + '|\n' + ''.join('| ' + ' | '.join(cell(c) for c in row) + ' |\n' for row in rows)

    def evidence(keys):
        return ', '.join(f'[{key}](../../{EVIDENCE[key][0]})' for key in keys)

    def write(name, title, body):
        intro = (f'# {title}\n\nBaseline 0.3.1; manuscript 7.0.7; evidence checkpoint `{checkpoint}`. '
                 'Preparation #27; **proposals only, not owner acceptance or final release**. '
                 'Machine bindings and unchanged source outcomes: [report.json](report.json). '
                 'This is the historical preparation snapshot; see the [live owner decisions](../owner-review/README.md) and [current article](../manuscript-review/v7.0.8/README.md) for subsequent approved work.\n\n')
        outputs[name] = (intro + body + '\n').encode()

    write('README.md', 'Final v0.3.1 claim and review package',
          'The technical packets rc.1–rc.7 are consolidated. This closes review preparation, not semantic judgment. '
          'The finite next action is the owner deciding the 11 explicit prompts below, including the narrower operational claims; '
          'then apply accepted prose and perform one final stable freeze. No additional feature prerelease is scheduled.\n\n' +
          table(['Accounting completed', 'Rows', 'Meaning'], [
              ['[Clause proposals](constraints.md)',25,'All original clauses; retained claim and excluded scope'],
              ['[Historical unexecuted routes](routes.md)',31,'14 HermiT + 17 SHACL, no historical relabeling'],
              ['[Requirement/scope/CQ overlay](requirements.md)',28,'12 requirements + 8 scope obligations + 8 CQs; no full MUST acceptance'],
              ['[Owner decision prompts](owner-decisions.md)',11,'Proposed judgment/evidence/counterexample/risk; 0 actual ratings at checkpoint'],
              ['[Manuscript reconciliation](manuscript.md)','65 + 7','65 baseline claim dispositions retained; 7 exact text proposals not applied'],
              ['[Final freeze checklist](freeze-checklist.md)','Pending','Owner scope acceptance, critical resolutions, article QA and final publication profile']]) +
          '\n## Retained claim groups\n\n' + table(['ID / claim','Evidence','Permitted wording','Excluded wording'],
          [[r['id']+' / '+r['title'], evidence(r['evidence_keys']), r['permitted_wording'],r['excluded_wording']] for r in policy['claims']]) +
          '\n## Method-specific supplement populations\n\n' + table(['Receipt','Recorded population (not additive)'],
          [[evidence([k]),json.dumps(v,ensure_ascii=False)] for k,v in populations.items()]) +
          '\nOriginal HermiT: 693 matching finite cases; 281/295 obligations PASS, 14 NOT_RUN. Historical consolidated SHACL fixed ledger: 341/359 PASS, one PARTIAL, 17 NOT_RUN. '
          'These are recorded outcomes, not fresh runs here or semantic correctness percentages. Original CQ checkpoint: 40 executions and 5/8 bounded synthetic-population contracts; later source supplements remain separate. '
          'Historical private SQLite counts and pharmaceutical corpus numbers are preserved only as historical results, not current public reruns. '
          'Full scientific correctness and critical findings remain unestimated until attributable review.\n\n'
          'Rebuild/check: `python tools/build_final_review.py --write` / `--check`. The checker binds immutable scientific receipts and preserves the owner register as a historical snapshot, so subsequent real review does not erase preparation history.')
    write('constraints.md','All 25 clause dispositions',table(
        ['Clause','Original HermiT / SHACL','Proposed current route','Retained claim','Unclaimed / deferred','Evidence / owner prompts'],
        [[r['id']+' '+r['source_clause']['title'], ' / '.join(r['historical_obligations'][e][0]['outcome'] for e in ('HermiT','SHACL')),
          r['proposed_disposition'],r['retained_claim'],r['unclaimed_or_deferred'],evidence(r['evidence_keys'])+'; '+', '.join(r['owner_review_ids'])] for r in constraints]) +
        '\nAll original clause statements and complete original obligation rows are retained in report.json. Proposed alternative evidence never discharges the historical HermiT route.')
    write('routes.md','All 31 historical NOT_RUN routes',table(
        ['Engine / obligation','Clause','Original outcome and reason/scope','Proposed route','Retained claim / exclusion','Evidence'],
        [[r['engine']+' '+r['original_obligation']['id'],r['constraint_id'],
          'NOT_RUN: '+str(r['original_obligation'].get('reason',r['original_obligation'].get('scope','See original obligation'))),
          r['proposal']['proposed_disposition'],r['proposal']['retained_claim']+' EXCLUSION: '+r['proposal']['unclaimed_or_deferred'],
          evidence(r['proposal']['evidence_keys'])] for r in routes]) +
        '\nC-08 is separately **PARTIAL** in the fixed SHACL ledger (SHACL-0620). Profile 0.6.0 adds 37 actual SHACL executions and 4 preflight rejections for declared interpretation metadata only; no full tolerance policy, numeric conversion or globally accepted C-08 is inferred.')
    write('requirements.md','Original requirements and proposed first-final scope',
          'Original criteria, priorities and remaining obligations are not rewritten. Full original requirement acceptance is **not** claimed. '
          'RKRS-05, RKRS-08 and RKRS-11 retain their original MUST priority: the current operational exclusions require explicit owner scope decisions.\n\n' +
          table(['ID / original state','Original acceptance criterion','Clauses / proposed scope','Retained limit and owner decision'],
          [[r['original']['id']+' / '+r['original_definition'].get('priority','priority not declared')+' / '+r['original']['acceptance_state'],r['original']['acceptance_criterion'],
            ', '.join(r['proposal']['constraint_ids'])+' / '+r['proposal']['proposed_scope'],r['proposal']['limit']] for r in traces]))
    write('owner-decisions.md','Concrete owner decision table (11 pending judgments)',
          'Review each row as author/owner with assistant support. Enter ACCEPT_SCOPED, REVISE or REJECT plus rationale, evidence and any critical finding; '
          'acknowledge the specific exclusions. These suggested labels are not recorded owner ratings. The live register is '
          '[evaluation/owner-review/register.json](../owner-review/register.json); this package preserves its 0-rating checkpoint snapshot. '
          'A generic instruction to continue does not supply these judgments.\n\n' +
          table(['ID / topic','Assistant proposal','Evidence','Counterexample to examine','Residual risk','Exact wording/scope decision'],
          [[r['id']+' / '+r['topic'],r['assistant_proposal'],evidence(r['evidence_keys']),r['counterexample_to_examine'],r['residual_risk'],r['wording_or_scope_decision']] for r in policy['owner_proposals']]) +
          '\nFor OR-10 decide the seven [exact manuscript proposals](manuscript.md) and exclusion of full computation, workflow/time execution and generic admission readiness from this first final release. '
          'For OR-11 record the release decision only after the [freeze checklist](freeze-checklist.md) is complete. '
          'Any discovered critical defect in retained scope must be fixed/rechecked or the affected claim explicitly rejected; no critical defect is marked resolved here.')
    write('manuscript.md','Manuscript 7.0.7 reconciliation and exact proposed amendments',
          amendments['inspection']+' **The DOCX/PDF were not edited and no new article version was created.**\n\n' +
          table(['Artifact','SHA-256'],[[r['filename'],r['sha256']] for r in amendments['artifacts']]) +
          '\nAll 65 [baseline manuscript ledger](../manuscript-review/ledger.json) rows/dispositions are copied unchanged into report.json. '
          'Withdrawn historical COH/COP/query/pattern assertions remain withdrawn; graph connectivity is not semantic cohesion or correctness. '
          'Historical private-companion counts are not fresh public runs.\n\n' +
          table(['Proposal / exact locator','Reason','Original paragraph SHA-256','State'],
          [[r['id']+' / '+r['locator'],r['reason'],r['source_paragraph_sha256'],r['status']] for r in amendments['rows']]) +
          ''.join('\n## '+r['id']+' — '+r['locator']+'\n\nSource prefix: '+r['source_prefix']+'\n\nOriginal full paragraph:\n\n'+r['original_text']+'\n\nProposed full paragraph:\n\n'+r['proposed_text']+'\n' for r in amendments['rows']) +
          '\n'+amendments['preservation'])
    write('freeze-checklist.md','Finite first-final freeze and publication checklist',
          table(['Step','Current state','Exit evidence'],[
              ['1. Consolidated review preparation #27','COMPLETE_PREPARATION_ONLY','25 clauses, 31 NOT_RUN routes, 28 traces, 65 baseline manuscript claims, seven exact prose proposals and 11 owner prompts; deterministic source checks'],
              ['2. Actual owner judgments #7','PENDING','OR-01–OR-10 explicit ratings/rationale, original MUST scope exclusions and sourced/withheld case judgments; author involvement disclosed'],
              ['3. Critical in-scope findings','UNESTABLISHED','Attributable review finds/records issues; every critical identity, forbidden-inference, integrity or data-loss finding resolved and affected evidence rechecked'],
              ['4. Accepted manuscript wording','PROPOSED_NOT_APPLIED','Apply only accepted exact prose changes, equivalent Word/PDF rendering and visual QA; bind both artifact hashes and preservation diff'],
              ['5. Stable publication implementation','PENDING','Reviewed final v0.3.1 profile, correct final/latest metadata, immutable tag and five-or-declared assets/inventory/checksums; existing prerelease-only guard is not bypassed'],
              ['6. One exact clean final freeze','PENDING','OR-11 final decision, no unresolved critical in-scope finding, clean pinned candidate, appropriate affected fresh engine replays and provenance; scientific receipts not rewritten'],
              ['7. Publish and independently read back','PENDING','Exact final tag/commit, downloaded asset SHA-256 and archive inventory, metadata/latest check; prior rc tags/assets unchanged']]) +
          '\n## Critical versus future scope\n\n'+policy['critical_screen']+'\n\n' +
          table(['Future issue','Scope that may remain open only if unclaimed'],[[r['issue'],r['scope']] for r in policy['future_ownership']]) +
          '\nDo not defer a defect within the retained claim under one of these broad issues. '
          'Neither full original MUST acceptance nor independent validation is established by narrowing proposed release scope. '
          'No additional feature prerelease, blanket 100% score or closure of every research issue is required for the bounded final artifact. '
          'Final publication waits for the finite exit evidence above, not a count of RCs.')
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    require(args.write != args.check, 'Choose exactly one of --write / --check')
    outputs = build()
    for name, data in outputs.items():
        path = OUT / name
        if args.write:
            path.write_bytes(data)
        else:
            require(path.exists() and path.read_bytes() == data, 'Stale final-review artifact: ' + str(path.relative_to(ROOT)))
    print(json.dumps({'status':'SOURCE_BOUND_PREPARATION_MATCHED', 'outputs':len(outputs),
                      'clauses':25, 'historical_not_run_routes':31, 'traces':28,
                      'owner_prompts':11, 'new_owner_ratings':0, 'final_release_ready':False}))


if __name__ == '__main__':
    main()
