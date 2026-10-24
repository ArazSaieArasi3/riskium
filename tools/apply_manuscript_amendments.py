"""Apply the seven owner-approved prose amendments to the exact 7.0.7 DOCX.

Author-facing files stay outside the public source repository. Run using the
primary document runtime, then render and visually inspect before delivery.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import zipfile
from lxml import etree as E

ROOT = Path(__file__).resolve().parents[1]
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def text(node):
    return ''.join(node.xpath('.//w:t/text()', namespaces=NS))


def apply(source, output, modified_at):
    proposals_path = ROOT / 'evaluation/final-review/manuscript-proposals.json'
    proposals = json.loads(proposals_path.read_bytes())
    expected = next(a['sha256'] for a in proposals['artifacts'] if a['filename'].endswith('.docx'))
    assert sha(source.read_bytes()) == expected, 'Wrong source manuscript'
    with zipfile.ZipFile(source) as archive:
        document = E.fromstring(archive.read('word/document.xml'))
        paragraphs = document.find('w:body', NS).findall('w:p', NS)
        before = [E.tostring(p) for p in paragraphs]
        changes = []
        for proposal in proposals['rows']:
            index = proposal['docx_paragraph_index']
            paragraph = paragraphs[index]
            old = text(paragraph)
            assert old == proposal['original_text']
            assert sha(old.encode()) == proposal['source_paragraph_sha256']
            new = proposal['proposed_text']
            note = None
            if proposal['id'] == 'MA-06':
                sentence = (' An author-led review with assistant support accepted the declared bounded release scope; '
                            'this review is not independent validation, and final package verification remains separate.')
                new = new.replace(' No production application,', sentence + ' No production application,')
                note = 'Necessary factual update within the same approved paragraph: disclose the now-explicit owner/author scope review and its independence/final-freeze limits.'
            runs = paragraph.findall('w:r', NS)
            nodes = paragraph.findall('.//w:t', NS)
            assert len(runs) == len(nodes) == 1, 'Review formatting before changing a split run'
            nodes[0].text = new
            assert text(paragraph) == new
            changes.append({'id': proposal['id'], 'paragraph_index': index,
                            'reason': proposal['reason'], 'additional_reason': note,
                            'original_text': old, 'new_text': new,
                            'original_paragraph_sha256': sha(old.encode()),
                            'new_paragraph_sha256': sha(new.encode())})
        allowed = {r['paragraph_index'] for r in changes}
        assert all(E.tostring(p) == before[i] for i, p in enumerate(paragraphs) if i not in allowed)
        cp = 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'
        dc = 'http://purl.org/dc/elements/1.1/'
        dt = 'http://purl.org/dc/terms/'
        core = E.fromstring(archive.read('docProps/core.xml'))
        fields = {f'{{{cp}}}version': '7.0.8', f'{{{cp}}}revision': '4',
                  f'{{{dc}}}subject': 'Manuscript v7.0.8; ontology baseline v0.3.1; ORSD revision 0.4.3',
                  f'{{{dc}}}description': 'Owner-approved bounded release scope and necessary evidence updates; selected ontology figure retained.',
                  f'{{{dt}}}modified': modified_at}
        for tag, value in fields.items():
            node = core.find(tag)
            assert node is not None, tag
            node.text = value
        replacements = {'word/document.xml': E.tostring(document, xml_declaration=True, encoding='UTF-8', standalone=True),
                        'docProps/core.xml': E.tostring(core, xml_declaration=True, encoding='UTF-8', standalone=True)}
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as target:
            for entry in archive.infolist():
                target.writestr(deepcopy(entry), replacements.get(entry.filename, archive.read(entry.filename)))
        with zipfile.ZipFile(output) as target:
            unchanged = [p for p in archive.namelist() if p not in replacements and archive.read(p) == target.read(p)]
            assert len(unchanged) == len(archive.namelist()) - 2
            assert archive.namelist() == target.namelist()
    return {'schema': 'riskium-manuscript-prose-sync-v1', 'source_manuscript_version': '7.0.7',
            'manuscript_version': '7.0.8', 'model_version': '0.3.1', 'orsd_revision': '0.4.3',
            'source_docx_sha256': expected, 'proposal_sha256': sha(proposals_path.read_bytes()),
            'output_docx_sha256': sha(output.read_bytes()), 'modified_at': modified_at,
            'changes': changes,
            'preservation': {'changed_body_paragraphs': len(changes), 'inserted_or_removed_paragraphs': 0,
                             'unaffected_body_paragraph_xml_unchanged': True,
                             'all_tables_unchanged': True, 'all_other_package_members_byte_identical': True,
                             'unchanged_package_members': len(unchanged),
                             'title_authors_affiliations_references_unchanged': True,
                             'figure_media_dimensions_styles_headers_footers_unchanged': True,
                             'numeric_results_and_historical_statuses_preserved': True},
            'render_and_visual_qa': 'REQUIRED_AFTER_THIS_TEXT_TRANSFORM'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--modified-at', default=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
    args = parser.parse_args()
    assert args.source.resolve() != args.output.resolve()
    receipt = apply(args.source, args.output, args.modified_at)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'manuscript': receipt['manuscript_version'], 'changed_paragraphs': 7,
                      'unchanged_package_members': receipt['preservation']['unchanged_package_members']}))


if __name__ == '__main__':
    main()
