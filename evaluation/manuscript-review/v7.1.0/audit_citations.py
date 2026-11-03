"""Recheck exact citation placement in the author-held Riskium 7.1.0 DOCX.

This checks numbering and declared bibliographic text, not external publication
metadata, interpretation adequacy, venue compliance or a newer paper version.
Usage: python audit_citations.py /path/to/Riskium_Manuscript_v7_1_0.docx > reference-audit.json
Requires python-docx. The DOCX digest is pinned in receipt.json.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

HERE = Path(__file__).resolve().parent
EXPECTED = {a['name']: a['sha256'] for a in json.loads((HERE/'receipt.json').read_text())['artifacts']}
AUTHOR_PAPERS = {15: 'CM4SLE', 16: 'CM4DI', 27: 'CM-PharmE conference',
                 28: 'CM-PharmE journal', 30: 'GenAI organizational model',
                 31: 'SME blockchain fundraising'}


def main(path):
    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert path.name in EXPECTED and digest == EXPECTED[path.name], 'Wrong manuscript binary'
    doc = Document(path)
    bib = {}
    for paragraph in doc.paragraphs:
        if paragraph.style and paragraph.style.name == 'References':
            match = re.match(r'^\[(\d+)\]\s*(.*)$', paragraph.text, re.S)
            assert match, paragraph.text
            n = int(match.group(1))
            assert n not in bib, n
            bib[n] = match.group(2)
    assert sorted(bib) == list(range(1, 35)), sorted(bib)
    first = {}; counts = {}; order = []
    for node in doc._element.body:
        body_text = ''.join(t.text or '' for t in node.iter(qn('w:t')))
        if body_text.strip() == 'References':
            break
        for match in re.finditer(r'\[(\d+)\]', body_text):
            n = int(match.group(1))
            assert n in bib, (n, body_text[:100])
            counts[n] = counts.get(n, 0) + 1
            if n not in first:
                first[n] = body_text[max(0, match.start()-90):min(len(body_text), match.end()+90)]
                order.append(n)
    assert order == list(range(1, 35)), order
    assert set(first) == set(bib)
    rows = []
    for n in sorted(bib):
        entry = bib[n]
        doi = re.search(r'\bdoi:\s*([^\s]+)', entry, re.I)
        url = re.search(r'https?://\S+', entry)
        rows.append(dict(number=n,author_requested=AUTHOR_PAPERS.get(n),
                         bibliography=entry,first_use_context=first[n],in_text_mentions=counts[n],
                         stated_doi=doi.group(1).rstrip('.') if doi else None,
                         stated_url=url.group(0).rstrip('.') if url else None,
                         external_metadata_status='NOT_REVERIFIED_BY_THIS_SCRIPT'))
    print(json.dumps(dict(schema='riskium-reference-placement-1',manuscript='7.1.0',
                          manuscript_sha256=digest,bibliography_items=len(bib),
                          cited_items=len(first),first_mention_sequence=order,
                          author_papers=AUTHOR_PAPERS,rows=rows,
                          limits=['Exact placement and transcription only; publication metadata needs source inspection.',
                                  'Journal publication state for reference 28 requires an actual publisher record.',
                                  'Six author papers are counted as citations, not independent validation.']),
                     indent=2,ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) != 2: raise SystemExit('Provide one DOCX path')
    main(sys.argv[1])
