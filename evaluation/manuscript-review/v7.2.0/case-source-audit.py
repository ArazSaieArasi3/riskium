#!/usr/bin/env python3
"""Recount the author-held case source database without exporting its contents."""
import argparse
import csv
import hashlib
import io
import json
import sqlite3
import zipfile
from collections import Counter
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, required=True)
    parser.add_argument('--archive', type=Path, required=True)
    args = parser.parse_args()
    expected = {
        'db': 'b1f08a5b9464f1c0c06acd112324707ae91d97d28883b006ca12ff6c2ee7b780',
        'archive': '0a7abf11cd143f1b02027eb77f4f5bfcee613021d9eebb63bb7c46fa81f8d220',
        'decisions': '5cdb2697e5d245620bbfd06ef74d0d32979a73827cffe0839dea3d5f20ea88e6',
    }
    assert digest(args.db.read_bytes()) == expected['db']
    assert digest(args.archive.read_bytes()) == expected['archive']
    with zipfile.ZipFile(args.archive) as archive:
        member = next(n for n in archive.namelist() if n.endswith('/Case_Adjudication_11.csv'))
        decision_bytes = archive.read(member)
    assert digest(decision_bytes) == expected['decisions']
    decisions = list(csv.DictReader(io.StringIO(decision_bytes.decode('utf-8-sig'))))
    assert len(decisions) == 11
    assert Counter(row['case_admission'] for row in decisions) == {'WITHHELD': 11}
    con = sqlite3.connect(f'file:{args.db}?mode=ro', uri=True)
    con.execute('pragma query_only=on')
    scalar = lambda q: con.execute(q).fetchone()[0]
    active = dict(con.execute("""select publication_type,count(*) from source_work
        where stage_scope='IN_SCOPE' group by publication_type"""))
    active_record_works = dict(con.execute("""select w.publication_type,count(distinct w.source_id)
        from source_work w join source_record r on w.source_id=r.source_id
        where r.role_status!='OUT_OF_SCOPE_THIS_STAGE' group by w.publication_type"""))
    counts = {table: scalar(f'select count(*) from {table}') for table in
              ('source_work', 'source_record', 'evidence_passage', 'catalog_item',
               'item_record_link', 'reported_value', 'scenario_component')}
    checks = {
        'sqlite_integrity': scalar('pragma integrity_check'),
        'foreign_key_violations': len(con.execute('pragma foreign_key_check').fetchall()),
        'source_records_without_evidence': scalar('select count(*) from source_record where evidence_id is null'),
        'record_evidence_source_mismatch': scalar('select count(*) from source_record r join evidence_passage e on r.evidence_id=e.evidence_id where r.source_id!=e.source_id'),
        'item_link_missing_target': scalar('select count(*) from item_record_link l left join catalog_item i on l.item_id=i.item_id left join source_record r on l.record_id=r.record_id where i.item_id is null or r.record_id is null'),
        'value_record_source_mismatch': scalar('select count(*) from reported_value v join source_record r on v.record_id=r.record_id where v.source_id!=r.source_id'),
        'value_evidence_source_mismatch': scalar('select count(*) from reported_value v join evidence_passage e on v.evidence_id=e.evidence_id where v.source_id!=e.source_id'),
        'scenario_evidence_source_mismatch': scalar('select count(*) from scenario_component s join source_record r on s.record_id=r.record_id join evidence_passage e on s.evidence_id=e.evidence_id where r.source_id!=e.source_id'),
    }
    correction = con.execute("select source_id,related_source_id,source_relationship from source_work where publication_type='Correction' and stage_scope='IN_SCOPE'").fetchall()
    result = {
        'input_sha256': {'db': expected['db'], 'archive': expected['archive'], 'decision_csv': expected['decisions']},
        'active_source_works': active, 'active_works_with_active_records': active_record_works,
        'all_rows': counts,
        'active_source_records': scalar("select count(*) from source_record where role_status!='OUT_OF_SCOPE_THIS_STAGE'"),
        'out_of_scope_record_count': scalar("select count(*) from source_record where role_status='OUT_OF_SCOPE_THIS_STAGE'"),
        'out_of_scope_record_work': [row[0] for row in con.execute("select distinct source_id from source_record where role_status='OUT_OF_SCOPE_THIS_STAGE'")],
        'correction_lineage': [{'correction_id': a, 'related_source_id': b, 'relationship': c} for a,b,c in correction],
        'decision_rows': len(decisions), 'withheld_decisions': sum(row['case_admission']=='WITHHELD' for row in decisions),
        'admitted_organizational_cases': dict(con.execute('select key,value from case_metadata')).get('accepted_risk_cases'),
        'checks': checks,
        'scope_note': 'Structural and preservation recount only; no independent source-truth, extraction accuracy, case identity or semantic validation.'
    }
    assert active == active_record_works == {'Correction': 1, 'Journal article': 30}
    assert counts == {'source_work':55,'source_record':1023,'evidence_passage':875,'catalog_item':883,'item_record_link':1011,'reported_value':1695,'scenario_component':84}
    assert result['active_source_records']==1011 and result['out_of_scope_record_count']==12
    assert result['admitted_organizational_cases']=='0'
    assert checks['sqlite_integrity']=='ok' and all(v==0 for k,v in checks.items() if k!='sqlite_integrity')
    assert len(correction)==1 and con.execute('select 1 from source_work where source_id=?',(correction[0][1],)).fetchone()
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
