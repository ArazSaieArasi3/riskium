"""Verify the owner-approved release scope and independent artifact version bindings.

This is a synchronization check, not a fresh document render, scientific engine
run, independent semantic review or final publication authorization.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_bytes())


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def check(root=None):
    global ROOT
    if root is not None:
        ROOT = Path(root)
    matrix = read('releases/artifact-matrix.json')
    owner = read('evaluation/owner-review/register.json')
    accepted = read('evaluation/owner-review/accepted-scope.json')
    scope = read('requirements/release-scope-v0.3.1.json')
    article = read('evaluation/manuscript-review/v7.0.8/receipt.json')
    policy = read('evaluation/final-review/policy.json')
    model = read('ontology/riskium-model.json')
    prep = read('evaluation/final-review/report.json')
    require(matrix['accepted_model_version'] == accepted['model_version'] == scope['model_version'] == article['model_version'] == model['version'] == '0.3.1', 'Model compatibility mismatch')
    require(matrix['orsd_revision'] == scope['documentation_revision'] == article['orsd_revision'] == accepted['orsd_revision'] == '0.4.3', 'ORSD compatibility mismatch')
    require(matrix['manuscript_version'] == article['manuscript_version'] == accepted['manuscript_version'] == '7.0.8', 'Manuscript compatibility mismatch')
    require(matrix['target_release'] == accepted['release_target'] == scope['target_release'] == 'v0.3.1', 'Package version mismatch')
    require(owner['final_candidate_signoff'] is False, 'Do not invent another owner signoff')
    if matrix['final_release_published']:
        publication = read(matrix['publication_receipt'])
        require(publication['tag'] == matrix['latest_published_package'] == matrix['target_release'], 'Published version mismatch')
        require(publication['publication_state'] == 'PUBLISHED_AND_INDEPENDENTLY_DOWNLOADED_VERIFIED', 'Publication readback missing')
        require(publication['downloaded_bytes_match'] and publication['archive_inventory_verified'] and publication['tag_commit_verified'] and publication['latest_verified'], 'Final readback gates missing')
        require(publication['final_metadata'] == {'draft': False, 'prerelease': False}, 'Wrong final maturity metadata')
    else:
        require(matrix['latest_published_package'] == 'v0.3.1-rc.7', 'Unknown pre-final publication state')
    require('0.4.3' in (ROOT / 'requirements/ontology-requirements.md').read_text(), 'ORSD prose revision missing')
    require(owner['ratings_recorded'] == 11 and len(owner['rows']) == 11, 'Explicit owner decisions missing')
    require({r['id'] for r in owner['rows']} == {f'OR-{i:02}' for i in range(1, 12)}, 'Owner prompt identity mismatch')
    require(Counter(r['owner_rating'] for r in owner['rows']) == {'ACCEPT_SCOPED': 9, 'REVISE_BEFORE_FINAL': 1, 'HOLD_UNTIL_FINAL_FREEZE': 1}, 'Conditional/revision decisions must not become blanket acceptance')
    require(owner['rows'][9]['status'] == 'DECIDED_REVISION_IMPLEMENTED', 'Article revision not resolved')
    require(owner['rows'][10]['status'] == 'CONDITION_ACCEPTED_TECHNICAL_GATE_PENDING', 'Final freeze condition lost')
    require(owner['authorization'] == accepted['authority'] and owner['authorization']['response_verbatim_fa'], 'Owner response/source boundary missing')
    require(owner['independent_validation_claimed'] is False and accepted['independent_validation'] is False, 'Author review is not independent')
    require(owner['critical_findings_count'] is None and owner['critical_findings_reported_in_this_response'] == 0, 'Do not manufacture a zero-critical certificate')
    require(accepted['full_original_requirement_acceptance'] is False and accepted['historical_engine_outcomes_changed'] is False and accepted['overall_semantic_correctness_percent'] is None, 'Unsupported acceptance/correctness claim')
    require(accepted['final_technical_issue'] == matrix['final_technical_issue'] == owner['rows'][10]['technical_execution_issue'] == 28, 'Missing finite final-freeze successor')
    require(len(accepted['constraints']) == 25 and {r['id'] for r in accepted['constraints']} == {r['id'] for r in model['constraints']}, 'Clause disposition missing')
    for current, proposal in zip(accepted['constraints'], policy['constraints']):
        require({k: v for k, v in current.items() if k != 'owner_disposition'} == {k: v for k, v in proposal.items() if k != 'owner_disposition'}, 'Accepted clause changed beyond reviewed proposal')
        require(current['owner_disposition'] == 'ACCEPTED_WITH_DECLARED_EXCLUSIONS', 'Unaccepted clause scope')
    for current, proposal in zip(accepted['claims'], policy['claims']):
        require({k: v for k, v in current.items() if k != 'owner_disposition'} == {k: v for k, v in proposal.items() if k != 'owner_disposition'}, 'Claim beyond reviewed proposal')
    require(len(accepted['claims']) == 12, 'Claim group missing')
    definitions = {r['id']: r for path in scope['baseline_definition_sha256'] for r in read(path)}
    require(len(scope['rows']) == len(accepted['trace_dispositions']) == len(definitions) == 28, 'Trace scope missing')
    require(Counter(r.get('priority') for r in definitions.values()) == {None: 16, 'MUST': 11, 'SHOULD': 1}, 'Original MUST priority changed')
    require({r['id'] for r in scope['rows']} == set(definitions) == set(accepted['trace_dispositions']), 'Trace identity mismatch')
    for path, expected in scope['baseline_definition_sha256'].items():
        require(sha(path) == expected, 'Original requirements changed: ' + path)
    for row in scope['rows']:
        require(row['original_definition'] == definitions[row['id']], 'Original requirement/criterion altered')
        require(row['accepted_release_scope'] == accepted['trace_dispositions'][row['id']], 'ORSD and owner scope disagree')
        proposal = policy['trace_proposals'][row['id']]
        require({k: v for k, v in row['accepted_release_scope'].items() if k != 'owner_disposition'} == {k: v for k, v in proposal.items() if k != 'owner_disposition'}, 'Trace exceeds reviewed scope')
    require(article['status'] == 'APPLIED_AND_VERIFIED' and len(article['changes']) == 7, 'Seven necessary edits not verified')
    proposals = read('evaluation/final-review/manuscript-proposals.json')
    require(article['proposal_sha256'] == sha('evaluation/final-review/manuscript-proposals.json'), 'Manuscript proposal binding changed')
    for change, proposal in zip(article['changes'], proposals['rows']):
        require(change['id'] == proposal['id'] and change['paragraph_index'] == proposal['docx_paragraph_index'], 'Unexpected paragraph change')
        require(change['original_text'] == proposal['original_text'], 'Original paragraph binding changed')
        require(hashlib.sha256(change['new_text'].encode()).hexdigest() == change['new_paragraph_sha256'], 'Changed paragraph hash mismatch')
        if change['id'] != 'MA-06':
            require(change['new_text'] == proposal['proposed_text'], 'Unapproved prose beyond seven amendments')
        else:
            require(change['additional_reason'] and 'An author-led review with assistant support' in change['new_text'], 'Author review disclosure missing')
    qa = article['render_and_visual_qa']
    require(qa['pages'] == 9 and qa['all_seven_full_revised_paragraphs_present_in_pdf'] and qa['all_nine_page_images_visually_inspected'] and qa['delivered_pdf_all_nine_pages_pixel_identical_to_inspected_render'], 'Document QA/readback incomplete')
    for path, expected in article['bindings_sha256'].items():
        require(sha(path) == expected, 'Manuscript correspondence drift: ' + path)
    for component in matrix['artifacts']:
        require(component['compatible_model'] == model['version'], 'Component model mismatch')
        for file in component['files']:
            require(sha(file['path']) == file['sha256'], 'Artifact byte drift: ' + file['path'])
    by_id = {r['id']: r for r in matrix['artifacts']}
    require(len(by_id) == len(matrix['artifacts']) == 10, 'Missing/duplicate artifact component')
    require(by_id['MANUSCRIPT']['external_artifacts'] == article['artifacts'], 'Delivered document digest/version mismatch')
    require(by_id['RELATIONAL']['version'] == read('implementation/relational/0.1.0/mapping.json')['schema_version'], 'Relational version drift')
    # Preserve scientific bytes while allowing dated explanatory/owner documents to evolve.
    for key in ('model', 'native', 'owl', 'h', 'conditional', 'sql', 'source6', 'source78'):
        for file in prep['evidence_registry'][key]:
            require(sha(file['path']) == file['sha256'], 'Evaluated scientific input drift: ' + file['path'])
    return {'status': 'ARTIFACT_SCOPE_ALIGNMENT_PASS', 'components': 10, 'owner_decisions': 11,
            'scoped_acceptances': 9, 'implemented_article_revision': '7.0.8',
            'orsd_revision': '0.4.3', 'model_version': '0.3.1',
            'final_freeze_pending': not matrix['final_release_published'], 'new_scientific_engine_executions': 0}


if __name__ == '__main__':
    print(json.dumps(check()))
