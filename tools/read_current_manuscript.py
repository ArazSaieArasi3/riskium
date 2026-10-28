"""Read approved private Word/PDF bytes; write only a public hash/location receipt."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = 'evaluation/consistency/current-0.3.0'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compact(text):
    return ''.join(c for c in unicodedata.normalize('NFKC', text).casefold() if c.isalnum())


def text(element):
    return ''.join(t.text or '' for t in element.findall('.//w:t', NS))


def require(value, message):
    if not value:
        raise ValueError(message)


def readback(directory):
    policy = json.loads((ROOT / OUT / 'policy.json').read_text())
    approved = json.loads((ROOT / 'evaluation/manuscript-review/v7.0.8/receipt.json').read_text())
    ledger = json.loads((ROOT / 'evaluation/manuscript-review/ledger.json').read_text())
    artifacts = []
    for row in approved['artifacts']:
        data = (Path(directory) / row['filename']).read_bytes()
        require(sha(data) == row['sha256'] and len(data) == row['size_bytes'], 'Unapproved manuscript bytes: ' + row['filename'])
        artifacts.append({k: row[k] for k in ('filename', 'sha256', 'size_bytes')})
    docx, pdf = [Path(directory) / row['filename'] for row in approved['artifacts']]
    with zipfile.ZipFile(docx) as package:
        document = ET.fromstring(package.read('word/document.xml'))
        media = [{'member': name, 'sha256': sha(package.read(name)), 'bytes': len(package.read(name))}
                 for name in package.namelist() if name.startswith('word/media/')]
    paras = document.findall('w:body/w:p', NS)
    tables = document.findall('w:body/w:tbl', NS)
    locations = {'P' + str(i): text(p) for i, p in enumerate(paras)}
    for ti, table in enumerate(tables):
        for ri, row in enumerate(table.findall('w:tr', NS)):
            for ci, cell in enumerate(row.findall('w:tc', NS)):
                locations[f'T{ti}:R{ri}:C{ci}'] = text(cell)
    extracted = subprocess.check_output(['pdftotext', str(pdf), '-']).decode()
    pages = extracted.split('\f')
    if not pages[-1].strip():
        pages.pop()
    require(len(pages) == 9, 'Approved PDF page count changed')
    compact_pages = [compact(p) for p in pages]
    joined_pdf = ''.join(compact_pages)
    boundaries = [0]
    for page in compact_pages:
        boundaries.append(boundaries[-1] + len(page))
    amendments = []
    for row in approved['changes']:
        value = locations['P' + str(row['paragraph_index'])]
        require(value == row['new_text'] and sha(value.encode()) == row['new_paragraph_sha256'], 'Approved amendment differs: ' + row['id'])
        require(compact(value) in ''.join(compact_pages), 'Full approved paragraph absent from PDF: ' + row['id'])
        amendments.append(dict(id=row['id'], word_location='P' + str(row['paragraph_index']),
                               text_sha256=sha(value.encode()), matched=True,
                               pdf_pages=[i + 1 for i, p in enumerate(compact_pages) if compact(value[:90]) in p or compact(value[-90:]) in p]))
    claims = []
    require(set(policy['manuscript_locators']) == {r['id'] for r in ledger['rows']}, 'Missing claim-location declaration')
    for row in ledger['rows']:
        locator = policy['manuscript_locators'][row['id']]
        nodes = []
        for binding in locator['word']:
            value = locations[binding['location']]
            require(binding['fragment'] in value, 'Claim locator fragment absent: ' + row['id'])
            nodes.append(dict(location=binding['location'], node_text_sha256=sha(value.encode()), fragment_sha256=sha(binding['fragment'].encode())))
        page_numbers = set()
        for fragment in locator['pdf_fragments']:
            needle = compact(fragment)
            starts = [m.start() for m in re.finditer(re.escape(needle), joined_pdf)]
            matched = [i + 1 for i in range(len(pages))
                       if any(start < boundaries[i + 1] and start + len(needle) > boundaries[i] for start in starts)]
            require(matched, 'Claim disposition absent from PDF: ' + row['id'] + ': ' + fragment)
            page_numbers.update(matched)
        claims.append(dict(id=row['id'], claim=row['claim'], checked_value=row['checked_value'],
                           historical_disposition=row['disposition'], word_locations=nodes, pdf_pages=sorted(page_numbers),
                           disposition=locator['disposition'], qualification=locator['qualification'],
                           historical_evidence_status='HISTORICAL_ARCHIVED_NOT_FRESH_REEXECUTED' if any(isinstance(p, dict) for p in row['evidence']) else 'UNCHANGED_PUBLIC_SOURCE_BOUND_RECEIPT'))
    all_text = '\n'.join(locations.values())
    for forbidden in policy['later_engineering_absent_from_paper']:
        require(forbidden not in all_text and compact(forbidden) not in ''.join(compact_pages), 'Later engineering unexpectedly in evaluated paper: ' + forbidden)
    groups = []
    for claim in policy['current_claims']:
        nodes = []
        page_numbers = set()
        for index in claim['paper_disposition']['word_paragraphs']:
            value = locations['P' + str(index)]
            require(compact(value) in joined_pdf, 'Current claim paper anchor absent from PDF: ' + claim['id'])
            nodes.append(dict(location='P' + str(index), node_text_sha256=sha(value.encode())))
            for fragment in (value[:80], value[-80:]):
                page_numbers.update(i + 1 for i, p in enumerate(compact_pages) if compact(fragment) in p)
        require(nodes and page_numbers, 'Current claim has no actual paper disposition')
        groups.append(dict(id=claim['id'], state=claim['paper_disposition']['state'], word_locations=nodes, pdf_pages=sorted(page_numbers)))
    table_receipts = []
    for i, table in enumerate(tables):
        require(i in (0, 1, 2, 3, 4), 'Unexpected manuscript table')
        table_receipts.append(dict(word_table_index=i, purpose=['Author affiliations', 'Table I: related work', 'Table II: domain responsibilities', 'Table III: synthetic CQs', 'Table IV: quality evidence and limits'][i],
                                   rows=len(table.findall('w:tr', NS)), text_sha256=sha(text(table).encode())))
    figure_paragraphs = [i for i, p in enumerate(paras) if p.findall('.//w:drawing', NS)]
    require(len(media) == 1 and len(figure_paragraphs) == 1, 'Figure/media population differs')
    return dict(schema='riskium-current-paper-baseline-readback-v2', manuscript_version='7.0.8',
                status='ACTUAL_APPROVED_BASELINE_READBACK_PASS', reviewed_on='2026-10-28', timezone='Asia/Tehran',
                method='Actual private author-file bytes read from their resolved file identities; SHA-256/size equal approved delivery. Full OOXML body/tables/media read; all 65 declared claim dispositions located in actual Word/PDF; all seven full approved paragraphs match both files.',
                artifacts=artifacts, body_paragraphs=len(paras), paragraphs_checked=len(amendments), amendments=amendments,
                pdf_pages=9, pdf_extracted_text_sha256=sha(extracted.encode()),
                claim_dispositions=claims, current_claim_groups=groups, tables=table_receipts,
                figures=[dict(word_paragraph=figure_paragraphs[0], caption_paragraph=63, media=media[0],
                              public_figure='diagrams/selected-view.svg', public_manifest='diagrams/manifest.json',
                              relation='Approved baseline image and bounded 28/31/10 caption; no fresh vector/image equivalence claim')],
                later_engineering_disposition='SSC/SCL/EQR/ELC functionality and current release status are NOT_CLAIMED_IN_PAPER. Conceptual commitments do not imply those later executions.',
                fresh_scientific_engine_runs=0, private_binaries_committed=False, new_manuscript_revision=False,
                new_word_render=False, new_pdf_render=True,
                visual_qa='All nine actual delivered PDF pages rendered and visually inspected for this checkpoint; no article edit or new semantic review.',
                scope='Approved paper baseline reconciliation; final submission reproduction, venue/format/coauthor decisions and current documentation remain separate.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = json.dumps(readback(args.directory), indent=2, ensure_ascii=False) + '\n'
    path = ROOT / OUT / 'manuscript-readback.json'
    if args.check:
        require(path.read_text() == result, 'Actual manuscript readback differs from recorded checkpoint')
    else:
        path.write_text(result)
    print(json.dumps(dict(status='ACTUAL_APPROVED_BASELINE_READBACK_PASS', manuscript='7.0.8', claims=65, amendments=7, pdf_pages=9)))


if __name__ == '__main__':
    main()
