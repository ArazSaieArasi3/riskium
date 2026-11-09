"""Bounded candidate SQLite sidecar; never mutate the exact-schema v7 source."""
import hashlib
import importlib.util
import json
import sqlite3
import sys
from pathlib import Path
from urllib.parse import urlsplit

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
import relational_evidence as legacy
import run_relational_evidence as fixture_source

RISK = Namespace('https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#')
EU = Namespace('https://github.com/ArazSaieArasi3/riskium/candidates/issue93/evidence-use#')
BASE_TABLES = ('artifact', 'artifact_version', 'reference_snapshot', 'reference_context')
TABLES = ('metadata',) + BASE_TABLES + ('grounding_record', 'explicit_alias', 'evidence_use')
USE_FIELDS = ('id', 'reference_version', 'item_version', 'context_version', 'grounding_version', 'purpose', 'recorded_at', 'justification')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def contract():
    c = json.loads((HERE / 'contract.json').read_text())
    for path, sha in c['inputs_sha256'].items():
        if digest(ROOT / path) != sha:
            raise ValueError('R-EU-BINDING: ' + path)
    return c


def ddl():
    text = (HERE / 'schema.sql').read_text()
    for table in TABLES:
        for operation in ('UPDATE', 'DELETE'):
            text += f"\nCREATE TRIGGER {table}_{operation.lower()} BEFORE {operation} ON {table} BEGIN SELECT RAISE(ABORT,'R-EU-IMMUTABLE'); END;\n"
    return text


def connect(path=':memory:'):
    db = sqlite3.connect(path, isolation_level=None)
    db.execute('PRAGMA foreign_keys=ON')
    db.execute('PRAGMA recursive_triggers=ON')
    return db


def snapshot(db, tables=TABLES):
    return {t: sorted([list(r) for r in db.execute('SELECT * FROM '+t)], key=encode) for t in tables}


def imported_hash(db):
    return hashlib.sha256(encode(snapshot(db, BASE_TABLES)).encode()).hexdigest()


def schema(db):
    return list(db.execute("SELECT type,name,tbl_name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY type,name"))


def health(db):
    c = contract()
    if db.execute('PRAGMA foreign_keys').fetchone()[0] != 1 or db.execute('PRAGMA recursive_triggers').fetchone()[0] != 1:
        raise ValueError('R-EU-CONNECTION')
    expected = connect(); expected.executescript(ddl())
    try:
        if schema(db) != schema(expected):
            raise ValueError('R-EU-SCHEMA')
    finally:
        expected.close()
    metadata = dict(db.execute('SELECT key,value FROM metadata'))
    if set(metadata) != {'schema_hash', 'source_state_hash', 'imported_sha256', 'export_contract_hash'} or metadata['schema_hash'] != hashlib.sha256(ddl().encode()).hexdigest() or metadata['export_contract_hash'] != c['export_contract_sha256']:
        raise ValueError('R-EU-METADATA')
    if metadata['imported_sha256'] != imported_hash(db):
        raise ValueError('R-EU-SNAPSHOT')
    if db.execute('PRAGMA foreign_key_check').fetchall() or db.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
        raise ValueError('R-EU-INTEGRITY')
    if db.execute('SELECT 1 FROM v_use_invalid LIMIT 1').fetchone():
        raise ValueError('R-EU-COHERENCE')


def initialize(source, target):
    """Copy issued documentary snapshots only; import creates no use or role."""
    contract(); legacy.health(source)
    if target.execute("SELECT 1 FROM sqlite_master WHERE type='table' LIMIT 1").fetchone():
        raise ValueError('R-EU-REQUIRES-EMPTY-SIDECAR')
    before = fixture_source.state_hash(source)
    target.executescript(ddl())
    target.execute('BEGIN')
    try:
        target.executemany('INSERT INTO artifact VALUES(?,?)', source.execute('SELECT artifact_id,label FROM information_artifact ORDER BY artifact_id').fetchall())
        versions = source.execute('SELECT version_id,artifact_id,payload_json FROM version_snapshot WHERE is_issued=1 ORDER BY version_id').fetchall()
        target.executemany('INSERT INTO artifact_version VALUES(?,?,?)', [(v,a,hashlib.sha256(p.encode()).hexdigest()) for v,a,p in versions])
        target.executemany('INSERT INTO reference_snapshot VALUES(?,?,?,?)', source.execute('SELECT e.version_id,e.item_version_id,e.evidential_role,e.source_locator FROM evidence_snapshot e JOIN version_snapshot v USING(version_id) WHERE v.is_issued=1 ORDER BY e.version_id').fetchall())
        target.executemany('INSERT INTO reference_context VALUES(?,?)', source.execute('SELECT t.version_id,t.target_version_id FROM evidence_target t JOIN version_snapshot v ON v.version_id=t.version_id WHERE v.is_issued=1 ORDER BY t.version_id,t.target_version_id').fetchall())
        metadata = {'schema_hash':hashlib.sha256(ddl().encode()).hexdigest(), 'source_state_hash':before,
                    'imported_sha256':imported_hash(target), 'export_contract_hash':contract()['export_contract_sha256']}
        target.executemany('INSERT INTO metadata VALUES(?,?)', sorted(metadata.items()))
        health(target)
        if before != fixture_source.state_hash(source):
            raise ValueError('R-EU-SOURCE-MODIFIED')
        target.execute('COMMIT')
    except BaseException:
        target.execute('ROLLBACK')
        raise


def iri(value):
    if not isinstance(value,str) or any(ch.isspace() for ch in value) or not urlsplit(value).scheme or ':' not in value:
        raise ValueError('R-EU-IRI')
    return value


def add_grounding(db, record):
    health(db)
    if set(record) != {'version_id','artifact_id','body','locator'}:
        raise ValueError('R-EU-GROUNDING-INPUT')
    for k in ['version_id','artifact_id']: iri(record[k])
    if db.execute('SELECT 1 FROM artifact_version WHERE id=?',(record['version_id'],)).fetchone():
        raise ValueError('R-EU-GROUNDING-VERSION-COLLISION')
    db.execute('INSERT INTO grounding_record VALUES(?,?,?,?)',tuple(record[k] for k in ['version_id','artifact_id','body','locator']))


def record_use(db, record):
    health(db)
    if set(record) != set(USE_FIELDS):
        raise ValueError('R-EU-USE-INPUT')
    for key in USE_FIELDS[:5]: iri(record[key])
    legacy.canonical_utc(record['recorded_at'],'R-EU-TIME')
    db.execute('BEGIN')
    try:
        db.execute('INSERT INTO evidence_use VALUES(?,?,?,?,?,?,?,?)',tuple(record[k] for k in USE_FIELDS))
        health(db)
        db.execute('COMMIT')
    except BaseException:
        db.execute('ROLLBACK')
        raise


def add_alias(db,left,right):
    health(db); iri(left); iri(right)
    db.execute('INSERT INTO explicit_alias VALUES(?,?)',(left,right))


def restore_dump(db,text):
    """Restore a trusted sidecar dump with all tables before rows and audit before commit."""
    if db.execute("SELECT 1 FROM sqlite_master WHERE type='table' LIMIT 1").fetchone():
        raise ValueError('R-EU-REQUIRES-EMPTY-SIDECAR')
    statements=[s for s in legacy.b.statements(text) if s.strip().upper() not in ('BEGIN TRANSACTION;','COMMIT;')]
    tables=[s for s in statements if s.lstrip().upper().startswith('CREATE TABLE')]
    inserts=[s for s in statements if s.lstrip().upper().startswith('INSERT INTO')]
    rest=[s for s in statements if s not in tables and s not in inserts]
    db.execute('BEGIN');db.execute('PRAGMA defer_foreign_keys=ON')
    try:
        for statement in tables+inserts+rest:db.execute(statement)
        health(db);db.execute('COMMIT')
    except BaseException:
        db.execute('ROLLBACK');raise


def information_graph(db, reference_version):
    """A version-qualified documentary view without actual-use role assertions."""
    health(db)
    row = db.execute('SELECT rv.artifact_id,iv.artifact_id,r.item_version FROM reference_snapshot r JOIN artifact_version rv ON rv.id=r.version_id JOIN artifact_version iv ON iv.id=r.item_version WHERE r.version_id=?',(reference_version,)).fetchone()
    if not row: raise ValueError('R-EU-REFERENCE')
    ref,item,item_version=row
    g=Graph();g.bind('risk',RISK);g.bind('eu',EU)
    for resource,kind in [(ref,'RKM-C065'),(ref,'RKM-C014'),(item,'RKM-C014')]:g.add((URIRef(resource),RDF.type,RISK[kind]))
    g.add((URIRef(ref),RISK['RX-021'],URIRef(item)))
    for version,artifact in [(reference_version,ref),(item_version,item)]:
        g.add((URIRef(version),RDF.type,RISK['RKM-C015']));g.add((URIRef(version),RISK['RX-006'],URIRef(artifact)))
    for ctx_version,ctx in db.execute('SELECT c.context_version,v.artifact_id FROM reference_context c JOIN artifact_version v ON v.id=c.context_version WHERE c.reference_version=?',(reference_version,)):
        g.add((URIRef(ctx),RDF.type,RISK['RKM-C014']));g.add((URIRef(ref),RISK['R-68'],URIRef(ctx)))
        g.add((URIRef(ctx_version),RDF.type,RISK['RKM-C015']));g.add((URIRef(ctx_version),RISK['RX-006'],URIRef(ctx)))
    return g


def rows(db):
    health(db)
    return [list(row) for row in db.execute((HERE/'query.sql').read_text())]


def use_graph(db, use_id):
    health(db)
    selected = [r for r in rows(db) if r[0] == use_id]
    if len(selected) != 1: raise ValueError('R-EU-USE')
    use,ref,ref_v,item,item_v,ctx,ctx_v,ground,ground_v,purpose=selected[0]
    graph=information_graph(db,ref_v)
    for resource,kind in [(use,'RKM-C075'),(item,'RKM-C066'),(ref,'RKM-C076'),(ground,'RKM-C014'),(ground_v,'RKM-C015')]:graph.add((URIRef(resource),RDF.type,RISK[kind]))
    for pred,obj in [('RE-001',item),('RE-002',ref),('RE-003',ground)]:graph.add((URIRef(use),RISK[pred],URIRef(obj)))
    graph.add((URIRef(ground_v),RISK['RX-006'],URIRef(ground)))
    for pred,obj in [('referenceVersion',ref_v),('itemVersion',item_v),('context',ctx),('contextVersion',ctx_v),('groundingVersion',ground_v)]:graph.add((URIRef(use),EU[pred],URIRef(obj)))
    # Match the pinned profile's plain RDF string enumeration. Its sh:datatype
    # xsd:string check also accepts plain strings; the engine distinguishes an
    # explicitly typed rdflib Literal in sh:in term equality.
    graph.add((URIRef(use),EU.purpose,Literal(purpose)))
    time,justification=db.execute('SELECT recorded_at,justification FROM evidence_use WHERE id=?',(use,)).fetchone()
    graph.add((URIRef(use),EU.recordedAt,Literal(time,datatype=XSD.dateTime)))
    graph.add((URIRef(use),EU.justification,Literal(justification)))
    body,locator=db.execute('SELECT body,locator FROM grounding_record WHERE version_id=?',(ground_v,)).fetchone()
    graph.add((URIRef(ground_v),EU.groundingText,Literal(body)))
    graph.add((URIRef(ground_v),EU.groundingLocator,Literal(locator)))
    for left,right in db.execute('SELECT left_id,right_id FROM explicit_alias'):graph.add((URIRef(left),URIRef('http://www.w3.org/2002/07/owl#sameAs'),URIRef(right)))
    return graph
