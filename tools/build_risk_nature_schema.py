"""Build the additive schema-10 storage/guards without reading expected answers."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'implementation/relational/0.9.0/010_risk_nature.sql'
# Match Python str.strip/isspace's complete Unicode whitespace set, including
# NBSP and the C0 information separators. SQL and API share the same boundary.
WHITESPACE = 'char('+','.join(str(v) for v in range(0x110000) if chr(v).isspace())+')'
COMMON = dict(narrative='TEXT NOT NULL', source_record_id='TEXT NOT NULL REFERENCES source_record(record_id)',
              source_locator='TEXT NOT NULL', interpretation_origin='TEXT NOT NULL', recorded_at='TEXT NOT NULL')
SCHEMAS = {
    'nature_support': dict(version_id='TEXT PRIMARY KEY REFERENCES version_snapshot(version_id)', artifact_id='TEXT NOT NULL REFERENCES nature_membership(artifact_id)',
                           native_class='TEXT NOT NULL', **COMMON, code='TEXT', scheme_version_id='TEXT REFERENCES nature_support(version_id)'),
    'nature_context': dict(version_id='TEXT PRIMARY KEY REFERENCES version_snapshot(version_id)', artifact_id='TEXT NOT NULL REFERENCES information_artifact(artifact_id)', **COMMON),
    'nature_snapshot': dict(version_id='TEXT PRIMARY KEY REFERENCES version_snapshot(version_id)', artifact_id='TEXT NOT NULL REFERENCES nature_membership(artifact_id)',
                            case_id='TEXT NOT NULL REFERENCES risk_case(case_id)', term_version_id='TEXT NOT NULL REFERENCES nature_support(version_id)',
                            context_version_id='TEXT REFERENCES nature_context(version_id)', **COMMON),
    'nature_entry': dict(version_id='TEXT PRIMARY KEY REFERENCES version_snapshot(version_id)', entry_id='TEXT NOT NULL REFERENCES register_entry(entry_id)',
                         previous_version_id='TEXT REFERENCES version_snapshot(version_id)', **COMMON),
}


def build():
    sql = ['-- SQLite schema 10: immutable source-qualified risk-nature task.']
    sql.append("""CREATE TABLE nature_membership (
 artifact_id TEXT PRIMARY KEY REFERENCES information_artifact(artifact_id),
 native_class TEXT NOT NULL CHECK(native_class IN ('RKM-C005','RKM-C006','RKM-C018','RKM-X02')),
 scheme_id TEXT REFERENCES nature_membership(artifact_id), code TEXT,
 UNIQUE(scheme_id,code),
 CHECK((native_class='RKM-C006' AND scheme_id IS NOT NULL AND code IS NOT NULL AND length(trim(code,char(9)||char(10)||char(13)||' '))>0)
 OR (native_class<>'RKM-C006' AND scheme_id IS NULL AND code IS NULL))) STRICT;""")
    for table, fields in SCHEMAS.items():
        sql.append('CREATE TABLE '+table+' (\n '+',\n '.join(k+' '+v for k,v in fields.items())+') STRICT;')
    sql += ["""CREATE TABLE nature_objective (
 context_version_id TEXT NOT NULL REFERENCES nature_context(version_id),
 objective_version_id TEXT NOT NULL REFERENCES nature_support(version_id),
 objective_id TEXT NOT NULL REFERENCES nature_membership(artifact_id),
 PRIMARY KEY(context_version_id,objective_version_id), UNIQUE(context_version_id,objective_id)) STRICT;""",
    """CREATE TABLE nature_entry_link (
 entry_version_id TEXT NOT NULL REFERENCES nature_entry(version_id),
 nature_version_id TEXT NOT NULL REFERENCES nature_snapshot(version_id),
 PRIMARY KEY(entry_version_id,nature_version_id)) STRICT;""",
    """CREATE TABLE nature_correction (
 corrected_version_id TEXT PRIMARY KEY REFERENCES nature_snapshot(version_id),
 prior_version_id TEXT NOT NULL REFERENCES nature_snapshot(version_id),
 actor TEXT NOT NULL, reason TEXT NOT NULL,
 source_record_id TEXT NOT NULL REFERENCES source_record(record_id),
 source_locator TEXT NOT NULL, interpretation_origin TEXT NOT NULL, recorded_at TEXT NOT NULL) STRICT;"""]
    checks = []
    def invalid(table, code, condition, key='version_id', joins=''):
        checks.append(f"SELECT t.{key} AS version_id,'{code}' AS code FROM {table} t {joins} WHERE {condition}")
    # Every snapshot is an explicit typed projection of the sealed source payload.
    payloads = []
    for table, fields in SCHEMAS.items():
        members = {k:'t.'+k for k in fields}
        if table == 'nature_support':
            # Null term-only fields do not occur in non-term input records.
            options = [("t.native_class='RKM-C006'", members),
                       ("t.native_class<>'RKM-C006'", {k:v for k,v in members.items() if k not in ('code','scheme_version_id')})]
        elif table == 'nature_context':
            members['objective_version_ids'] = "json((SELECT json_group_array(objective_version_id) FROM (SELECT objective_version_id FROM nature_objective o WHERE o.context_version_id=t.version_id ORDER BY objective_version_id)))"
            options = [('1', members)]
        elif table == 'nature_entry':
            members['nature_version_ids'] = "json((SELECT json_group_array(nature_version_id) FROM (SELECT nature_version_id FROM nature_entry_link l WHERE l.entry_version_id=t.version_id ORDER BY nature_version_id)))"
            options = [('1', members)]
        else:
            options = [('1', members)]
        for where, values in options:
            expression='json_object('+','.join("'"+k+"',"+v for k,v in sorted(values.items()))+')'
            payloads.append(f'SELECT t.version_id,{expression} AS expected_payload FROM {table} t WHERE {where}')
        invalid(table,'PROVENANCE', ' OR '.join("length(trim(t."+k+",char(9)||char(10)||char(13)||' '))=0" for k in ('narrative','source_locator','interpretation_origin')))
        invalid(table,'TIME', "length(t.recorded_at)<>20 OR substr(t.recorded_at,1,4)<'0001' OR t.recorded_at NOT GLOB '????-??-??T??:??:??Z' OR strftime('%Y-%m-%dT%H:%M:%SZ',t.recorded_at) IS NOT t.recorded_at OR date(t.recorded_at,'+0 days') IS NOT substr(t.recorded_at,1,10)")
        owner='entry_id' if table=='nature_entry' else 'artifact_id'
        invalid(table,'OWNER', f't.{owner} IS NOT v.artifact_id OR t.source_record_id IS NOT v.source_record_id OR (v.is_issued=1 AND t.recorded_at IS NOT v.issued_at)', joins='JOIN version_snapshot v USING(version_id)')
    sql.append('CREATE VIEW v_nature_expected_payload AS\n'+'\nUNION ALL\n'.join(payloads)+';')
    checks.append("SELECT p.version_id,'PAYLOAD' FROM v_nature_expected_payload p JOIN version_snapshot v USING(version_id) WHERE json(v.payload_json) IS NOT p.expected_payload")
    invalid('nature_support','IDENTITY', "m.native_class IS NOT t.native_class OR t.native_class NOT IN ('RKM-C006','RKM-C018','RKM-X02')", joins='LEFT JOIN nature_membership m USING(artifact_id)')
    invalid('nature_support','TERM_VERSION', "(t.native_class='RKM-C006' AND (s.native_class IS NOT 'RKM-C018' OR v.is_issued IS NOT 1 OR s.artifact_id IS NOT m.scheme_id OR t.code IS NOT m.code)) OR (t.native_class<>'RKM-C006' AND (t.code IS NOT NULL OR t.scheme_version_id IS NOT NULL))",
            joins='LEFT JOIN nature_support s ON s.version_id=t.scheme_version_id LEFT JOIN version_snapshot v ON v.version_id=t.scheme_version_id JOIN nature_membership m ON m.artifact_id=t.artifact_id')
    invalid('nature_support','TIME','s.recorded_at>t.recorded_at', joins='JOIN nature_support s ON s.version_id=t.scheme_version_id')
    invalid('nature_context','CONTEXT_VERSION', "a.kind IS NOT 'RKM-C002'", joins='JOIN information_artifact a USING(artifact_id)')
    invalid('nature_objective','OBJECTIVE_VERSION', "s.native_class IS NOT 'RKM-X02' OR s.artifact_id IS NOT t.objective_id OR v.is_issued IS NOT 1", key='context_version_id',
            joins='LEFT JOIN nature_support s ON s.version_id=t.objective_version_id LEFT JOIN version_snapshot v ON v.version_id=t.objective_version_id')
    invalid('nature_objective','TIME','s.recorded_at>c.recorded_at',key='context_version_id', joins='JOIN nature_support s ON s.version_id=t.objective_version_id JOIN nature_context c ON c.version_id=t.context_version_id')
    invalid('nature_snapshot','IDENTITY', "m.native_class IS NOT 'RKM-C005' OR EXISTS(SELECT 1 FROM nature_snapshot q WHERE q.artifact_id=t.artifact_id AND q.case_id<>t.case_id)", joins='LEFT JOIN nature_membership m USING(artifact_id)')
    invalid('nature_snapshot','TERM_VERSION', "s.native_class IS NOT 'RKM-C006' OR v.is_issued IS NOT 1", joins='LEFT JOIN nature_support s ON s.version_id=t.term_version_id LEFT JOIN version_snapshot v ON v.version_id=t.term_version_id')
    invalid('nature_snapshot','CONTEXT_VERSION','t.context_version_id IS NOT NULL AND (c.version_id IS NULL OR v.is_issued IS NOT 1)', joins='LEFT JOIN nature_context c ON c.version_id=t.context_version_id LEFT JOIN version_snapshot v ON v.version_id=t.context_version_id')
    invalid('nature_snapshot','TIME','s.recorded_at>t.recorded_at OR c.recorded_at>t.recorded_at', joins='JOIN nature_support s ON s.version_id=t.term_version_id LEFT JOIN nature_context c ON c.version_id=t.context_version_id')
    invalid('nature_snapshot','RECORDING', 'v.is_issued=1 AND (NOT EXISTS(SELECT 1 FROM nature_entry_link l WHERE l.nature_version_id=t.version_id) OR EXISTS(SELECT 1 FROM nature_entry_link l JOIN version_snapshot e ON e.version_id=l.entry_version_id WHERE l.nature_version_id=t.version_id AND e.is_issued<>1))', joins='JOIN version_snapshot v USING(version_id)')
    invalid('nature_entry','RECORDING','t.previous_version_id IS NOT v.previous_version_id OR t.entry_id IS NOT v.entry_id OR NOT EXISTS(SELECT 1 FROM nature_entry_link l WHERE l.entry_version_id=t.version_id)', joins='JOIN version_snapshot v USING(version_id)')
    invalid('nature_entry_link','RECORDING','e.case_id<>n.case_id OR (v.is_issued=1 AND nv.is_issued<>1)',key='entry_version_id',joins='JOIN nature_entry q ON q.version_id=t.entry_version_id JOIN register_entry e ON e.entry_id=q.entry_id JOIN nature_snapshot n ON n.version_id=t.nature_version_id JOIN version_snapshot v ON v.version_id=t.entry_version_id JOIN version_snapshot nv ON nv.version_id=t.nature_version_id')
    invalid('nature_entry','TIME','p.issued_at>t.recorded_at',joins='JOIN version_snapshot p ON p.version_id=t.previous_version_id')
    invalid('nature_correction','CORRECTION', 'a.artifact_id<>p.artifact_id OR a.case_id<>p.case_id OR t.corrected_version_id=t.prior_version_id OR av.is_issued<>1 OR pv.is_issued<>1',key='corrected_version_id',joins='JOIN nature_snapshot a ON a.version_id=t.corrected_version_id JOIN nature_snapshot p ON p.version_id=t.prior_version_id JOIN version_snapshot av ON av.version_id=a.version_id JOIN version_snapshot pv ON pv.version_id=p.version_id')
    invalid('nature_correction','PROVENANCE',' OR '.join("length(trim(t."+k+",char(9)||char(10)||char(13)||' '))=0" for k in ('actor','reason','source_locator','interpretation_origin')),key='corrected_version_id')
    invalid('nature_correction','TIME', "length(t.recorded_at)<>20 OR t.recorded_at NOT GLOB '????-??-??T??:??:??Z' OR strftime('%Y-%m-%dT%H:%M:%SZ',t.recorded_at) IS NOT t.recorded_at OR date(t.recorded_at,'+0 days') IS NOT substr(t.recorded_at,1,10) OR t.recorded_at<a.recorded_at OR t.recorded_at<p.recorded_at",key='corrected_version_id',joins='JOIN nature_snapshot a ON a.version_id=t.corrected_version_id JOIN nature_snapshot p ON p.version_id=t.prior_version_id')
    sql.append('CREATE VIEW v_nature_invalid AS\n'+'\nUNION ALL\n'.join(checks)+';')
    tables = {'nature_membership':['artifact_id'], **{t:['version_id'] for t in SCHEMAS}, 'nature_objective':['context_version_id','objective_version_id'], 'nature_entry_link':['entry_version_id','nature_version_id'], 'nature_correction':['corrected_version_id']}
    for table, keys in tables.items():
        for op in ('UPDATE','DELETE'):
            sql.append(f"CREATE TRIGGER {table}_{op.lower()} BEFORE {op} ON {table} BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;")
        duplicate=' AND '.join(k+'=NEW.'+k for k in keys)
        code='CORRECTION' if table=='nature_correction' else 'IDENTITY'
        sql.append(f"CREATE TRIGGER {table}_duplicate BEFORE INSERT ON {table} WHEN EXISTS(SELECT 1 FROM {table} WHERE {duplicate}) BEGIN SELECT RAISE(ABORT,'NRA-{code}'); END;")
        owners = ([('context_version_id','nature_objective')] if table=='nature_objective' else
                  [('entry_version_id','nature_entry_link'),('nature_version_id','nature_entry_link')] if table=='nature_entry_link' else
                  [('version_id',table)] if table in SCHEMAS else [])
        for field,_ in owners:
            sql.append(f"CREATE TRIGGER {table}_{field}_frozen BEFORE INSERT ON {table} WHEN EXISTS(SELECT 1 FROM version_snapshot WHERE version_id=NEW.{field} AND is_issued=1) BEGIN SELECT RAISE(ABORT,'NRA-IMMUTABLE'); END;")
    sql.append("""CREATE TRIGGER nature_membership_validate BEFORE INSERT ON nature_membership BEGIN
 SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM information_artifact WHERE artifact_id=NEW.artifact_id AND kind='RKM-C014')
 OR EXISTS(SELECT 1 FROM version_snapshot WHERE artifact_id=NEW.artifact_id AND is_issued=1)
 OR EXISTS(SELECT 1 FROM artifact_typing WHERE artifact_id=NEW.artifact_id)
 OR EXISTS(SELECT 1 FROM knowledge_type WHERE artifact_id=NEW.artifact_id)
 OR EXISTS(SELECT 1 FROM evidence_reference_type WHERE artifact_id=NEW.artifact_id)
 OR (NEW.native_class='RKM-C006' AND (NOT EXISTS(SELECT 1 FROM nature_membership WHERE artifact_id=NEW.scheme_id AND native_class='RKM-C018') OR EXISTS(SELECT 1 FROM nature_membership WHERE scheme_id=NEW.scheme_id AND code=NEW.code)))
 THEN RAISE(ABORT,'NRA-IDENTITY') END;
 END;""")
    # Prevent later old-profile subtype additions from bypassing the new membership.
    for table in ('artifact_typing','knowledge_type','evidence_reference_type'):
        sql.append(f"CREATE TRIGGER nature_exclusive_{table} BEFORE INSERT ON {table} WHEN EXISTS(SELECT 1 FROM nature_membership WHERE artifact_id=NEW.artifact_id) BEGIN SELECT RAISE(ABORT,'NRA-IDENTITY'); END;")
    for table in SCHEMAS:
        # Payload/list checks run at seal after all child bindings have staged.
        clauses=[]
        for code in ('PROVENANCE','TIME','OWNER','IDENTITY','TERM_VERSION','CONTEXT_VERSION'):
            clauses.append(f"SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code='{code}') THEN RAISE(ABORT,'NRA-{code}') END;")
        sql.append(f"CREATE TRIGGER {table}_validate AFTER INSERT ON {table} BEGIN "+' '.join(clauses)+' END;')
    sql.append("""CREATE TRIGGER nature_objective_validate AFTER INSERT ON nature_objective BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.context_version_id AND code IN ('OBJECTIVE_VERSION','TIME')) THEN RAISE(ABORT,'NRA-OBJECTIVE_VERSION') END; END;
 CREATE TRIGGER nature_entry_link_validate AFTER INSERT ON nature_entry_link BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM nature_entry e JOIN register_entry r ON r.entry_id=e.entry_id JOIN nature_snapshot n ON n.version_id=NEW.nature_version_id WHERE e.version_id=NEW.entry_version_id AND r.case_id<>n.case_id) THEN RAISE(ABORT,'NRA-RECORDING') END; END;
 CREATE TRIGGER nature_correction_validate AFTER INSERT ON nature_correction BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.corrected_version_id AND code IN ('CORRECTION','PROVENANCE','TIME')) THEN RAISE(ABORT,'NRA-CORRECTION') END;
 SELECT CASE WHEN EXISTS(WITH RECURSIVE w(id) AS (SELECT NEW.prior_version_id UNION SELECT c.prior_version_id FROM nature_correction c JOIN w ON c.corrected_version_id=w.id) SELECT 1 FROM w WHERE id=NEW.corrected_version_id) THEN RAISE(ABORT,'NRA-CORRECTION') END; END;
 CREATE TRIGGER nature_validate_seal BEFORE UPDATE ON version_snapshot WHEN OLD.is_issued=0 AND NEW.is_issued=1 BEGIN
 SELECT CASE WHEN EXISTS(SELECT 1 FROM nature_membership m WHERE m.artifact_id=NEW.artifact_id) AND NOT EXISTS(SELECT 1 FROM v_nature_expected_payload p WHERE p.version_id=NEW.version_id) THEN RAISE(ABORT,'NRA-METADATA') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM v_nature_expected_payload p WHERE p.version_id=NEW.version_id) AND (NEW.payload_json IS NOT OLD.payload_json OR NEW.issued_at IS NOT json_extract(NEW.payload_json,'$.recorded_at') OR EXISTS(SELECT 1 FROM v_nature_invalid WHERE version_id=NEW.version_id AND code<>'RECORDING')) THEN RAISE(ABORT,'NRA-SEAL') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM nature_snapshot WHERE version_id=NEW.version_id) AND (NOT EXISTS(SELECT 1 FROM nature_entry_link WHERE nature_version_id=NEW.version_id) OR EXISTS(SELECT 1 FROM nature_entry_link l JOIN version_snapshot v ON v.version_id=l.entry_version_id WHERE l.nature_version_id=NEW.version_id AND v.is_issued<>1)) THEN RAISE(ABORT,'NRA-RECORDING') END;
 SELECT CASE WHEN EXISTS(SELECT 1 FROM nature_entry e WHERE e.version_id=NEW.version_id) AND (NOT EXISTS(SELECT 1 FROM nature_entry_link WHERE entry_version_id=NEW.version_id) OR EXISTS(SELECT 1 FROM nature_entry_link l JOIN nature_snapshot n ON n.version_id=l.nature_version_id JOIN nature_entry e ON e.version_id=l.entry_version_id JOIN register_entry r ON r.entry_id=e.entry_id WHERE l.entry_version_id=NEW.version_id AND r.case_id<>n.case_id)) THEN RAISE(ABORT,'NRA-RECORDING') END;
 END;""")
    sql += ['CREATE INDEX nature_by_case ON nature_snapshot(case_id,version_id);',
            'CREATE INDEX nature_by_artifact ON nature_snapshot(artifact_id,version_id);',
            'CREATE INDEX nature_children ON nature_correction(prior_version_id,corrected_version_id);',
            'CREATE INDEX nature_recorders ON nature_entry_link(nature_version_id,entry_version_id);']
    return ('\n\n'.join(sql)+'\n').replace("char(9)||char(10)||char(13)||' '", WHITESPACE)


if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    if args.check:
        if OUT.read_text()!=build():raise ValueError('Stale schema 10')
    else:OUT.write_text(build())
