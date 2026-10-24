"""Inspect actual SQLite structure against explicit purpose/column/FD contracts.

Structural checks flag review needs. They do not discover domain dependencies,
prove a normal form, or substitute for user/workload acceptance.
"""
from collections import Counter
import json

from build_relational_assessment import NEW_TABLES

PURPOSES={
 'source_record':'Append-only exact raw source JSON; preserves unknown and received evidence before admission.',
 'identity_registry':'Global governed identifier/family registry; display labels never establish identity.',
 'risk_case':'Original selected RiskCase identity; no new actual cases are admitted by assessment fixtures.',
 'information_artifact':'Stable documentary identity and existing native kind; selected new subtype memberships live separately.',
 'register_entry':'Selected case/register membership with typed references.',
 'working_draft':'Editable application staging for original issue API; not an issued native version.',
 'draft_dependency':'Pending version dependency slots belonging to a working draft.',
 'version_snapshot':'Sealed payload, source and issue state for a distinct artifact version.',
 'version_dependency':'Immutable version-owned effective dependency pins in the original profile.',
 'schema_migration':'Executed migration numbers and exact SQL digests, matching user_version.',
 'artifact_typing':'Explicit selected concrete native type of an existing generic artifact, with vocabulary keys when applicable.',
 'scale_snapshot':'Version-owned declared scale dimension and explicit scale target.',
 'scale_level':'Governed vocabulary level membership in one immutable selected scale version.',
 'method_scope':'Version-qualified many-to-many permission for method, scale and dimension.',
 'assessment_snapshot':'Version-owned basis, context, method and distinct temporal qualifiers.',
 'result_snapshot':'One qualified result version owned by one assessment version; source, missingness and supplied lexical value stay explicit.'}

MEANINGS={
 'record_id':'Exact source-record identifier.', 'original_json':'Exact received JSON; null and unresolved fields are preserved.',
 'resource_id':'Globally unique governed identifier across supported resource families.', 'family':'Enforced local identity family; not inferred from a label.',
 'case_id':'Selected RiskCase identifier.', 'label':'Non-unique human display label; not an identity key.', 'source_record_id':'Exact source_record provenance key for this row.',
 'artifact_id':'Stable InformationArtifact identity.', 'kind':'Original bounded native kind discriminator.',
 'entry_id':'Register-entry identity or optional selected revision target.', 'entry_kind':'Fixed native entry type used by a composite FK.',
 'register_id':'Selected RiskRegister artifact.', 'register_kind':'Fixed native register type used by a composite FK.',
 'draft_id':'Editable staging identity, excluded from native issued-version export.',
 'previous_version_id':'Explicit predecessor version; original entry lineage remains same-entry and acyclic.',
 'payload_json':'Serialized issued/staged content; new bundle payloads preserve the exact declared metadata dictionary.',
 'slot':'Application dependency role Context, Method, Scale or Criteria.',
 'target_version_id':'Pinned target ArtifactVersion.', 'direct_artifact_id':'Optional explicitly asserted direct target; must agree with versionOf.',
 'version_id':'Distinct version identity.', 'owner_version_id':'Version owning an immutable dependency pin.',
 'issued_at':'Canonical issue timestamp; distinct from recorded, reference and validity time.', 'is_issued':'0 staging / 1 sealed; sealed content and owned metadata are immutable.',
 'version':'Applied schema migration number.', 'sha256':'Digest of exact applied SQL bytes.',
 'native_class':'Concrete selected native membership, with an exact model element and no label-derived typing.',
 'scheme_uri':'Governed vocabulary scheme IRI; required only for selected vocabulary members.',
 'scheme_edition':'Explicit scheme edition IRI; different editions retain distinct keys.',
 'local_code':'Nonempty scheme/edition-qualified code; not a bare global identity key.',
 'scale_version_id':'Pinned ArtifactVersion of the exact scale, with frozen declared dimension.', 'scale_id':'Optional/direct native AssessmentScale assertion, checked against its version.',
 'dimension_id':'Governed AssessmentDimension artifact; missing cannot become a default dimension.',
 'level_id':'Optional selected AssessmentScaleLevel artifact, bound to its scale version.',
 'method_version_id':'Pinned issued version of AssessmentMethodSpecification.', 'method_id':'Optional/direct method assertion; absence is not fabricated from a version.',
 'assessment_version_id':'Version owning assessment interpretation and result membership.', 'assessment_id':'Stable AssessmentInformation identity.',
 'basis_id':'Required native AssessmentBasis assertion.', 'basis_version_id':'Supplementary selected basis version; absence makes strict comparison not ready.',
 'context_id':'Optional/direct RiskContextSpecification assertion.', 'context_version_id':'Required pinned issued context version.',
 'temporal_context_id':'Opaque relevant time-interpretation identity for exact-join policy; not an interval computation.',
 'recorded_at':'When the assessment information was recorded; supplied canonical UTC value.',
 'reference_at':'Optional reference instant; SQL NULL means unknown.', 'valid_from':'Optional declared validity start; not inferred from recording or issue.',
 'valid_to':'Optional declared validity end; simple endpoint order is checked only when both endpoints are supplied.',
 'result_version_id':'Distinct issued/staged version of the result artifact.', 'result_id':'Stable DimensionAssessmentResult identity; labels/values do not merge it.',
 'score_kind':'REPORTED or UNKNOWN; computed claims are explicitly unsupported in this profile.',
 'reported_value':'Source lexical text, including literal zero and high-precision spelling; never used as verified arithmetic.',
 'source_locator':'Nonempty exact source location for this result assertion.', 'interpretation_origin':'Nonempty attribution of extraction/interpretation; existence is not source truth.'}

REVIEW={
 'artifact_typing':('artifact_id -> native_class, qualifiers, source','Conditional scheme/edition/code key applies only to vocabulary members; membership is separate from stable artifact identity.'),
 'scale_snapshot':('scale_version_id -> scale_id, dimension_id, source','The direct scale target repeats versionOf deliberately as an explicit assertion; equality is guarded. No automatic claim of BCNF.'),
 'scale_level':('level_id -> scale_version_id, source','A distinct level resource belongs to one governed version in this local profile; reissued levels use distinct identities.'),
 'method_scope':('(method_version_id, scale_id, dimension_id) -> source','Association table has a composite key and no arbitrary one-column surrogate; version ownership preserves prior permissions.'),
 'assessment_snapshot':('assessment_version_id -> selected role pins, qualifiers, source','Optional direct references preserve whether a native assertion was supplied; guarded version targets are deliberate constrained redundancy, not an unreviewed latest join.'),
 'result_snapshot':('result_version_id -> result_id, owning assessment version, dimension, selection, source/value qualifiers','Multiple values use distinct qualified rows, not comma-separated values or an unqualified single scalar; source/version dependencies are explicit.')}


def inspect(c, contracts=None):
    purposes=PURPOSES if contracts is None else contracts
    tables=[];findings=[]
    for name,sql in c.execute("SELECT name,sql FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall():
        columns=c.execute('PRAGMA table_info('+name+')').fetchall()
        keys=[r[1] for r in sorted(columns,key=lambda r:r[5]) if r[5]]
        indexes=[]
        for row in c.execute('PRAGMA index_list('+name+')').fetchall():
            indexes.append(dict(name=row[1],unique=bool(row[2]),origin=row[3],columns=[r[2] for r in c.execute('PRAGMA index_info('+row[1]+')')]))
        fks=[dict(id=r[0],sequence=r[1],target_table=r[2],column=r[3],target_column=r[4],on_delete=r[6]) for r in c.execute('PRAGMA foreign_key_list('+name+')')]
        purpose=purposes.get(name)
        if not purpose:findings.append(dict(table=name,code='UNEXPLAINED_TABLE'))
        if not keys:findings.append(dict(table=name,code='MISSING_PRIMARY_KEY'))
        if len(columns)==1 and (not purpose or not fks):findings.append(dict(table=name,code='UNEXPLAINED_ONE_COLUMN_TABLE'))
        dictionary=[]
        for col in columns:
            meaning=MEANINGS.get(col[1])
            if not meaning:findings.append(dict(table=name,column=col[1],code='UNDOCUMENTED_COLUMN'))
            dictionary.append(dict(name=col[1],datatype=col[2],not_null=bool(col[3]),default=col[4],primary_key_order=col[5],meaning=meaning))
        review=REVIEW.get(name,('Primary key -> stored row attributes within the original bounded profile','Original 0.1.0 dictionary/guards retained; full domain normalization is not inferred from schema inspection.'))
        tables.append(dict(name=name,purpose=purpose,primary_key=keys,columns=dictionary,foreign_keys=fks,indexes=indexes,
            strict=sql.rstrip().endswith('STRICT'),declared_functional_dependency=review[0],design_review=review[1]))
    return dict(schema='riskium-relational-design-audit-v1',method='Actual SQLite PRAGMAs plus authored purpose/FD/dictionary review; not automatic normalization proof.',
        summary=dict(tables=len(tables),columns=sum(len(t['columns']) for t in tables),foreign_key_columns=sum(len(t['foreign_keys']) for t in tables),
            named_indexes=sum(sum(i['origin']=='c' for i in t['indexes']) for t in tables),one_column_tables=sum(len(t['columns'])==1 for t in tables),findings=len(findings)),
        findings=findings,tables=tables,production_usability_validated=False,full_normal_form_proven=False)


def render(report):
    lines=['# Relational schema dictionary and design review', '',report['method'],'',
        'Table and column counts are inventory, not a quality score. A one-column subtype/key-membership table can be valid when its purpose, key, FK and consumers are explicit. Unexplained tables or undocumented columns are findings. Guarded redundant direct/version assertions are disclosed rather than falsely called a proved normal form.','',
        'Summary: '+json.dumps(report['summary'])+'.','']
    for table in report['tables']:
        lines += ['## '+table['name'],'',table['purpose'] or 'UNEXPLAINED','',
            'Declared FD: `'+table['declared_functional_dependency']+'`. '+table['design_review'],'',
            '| Column | Type | Required | Meaning |','| --- | --- | --- | --- |']
        for col in table['columns']:lines.append(f"| {col['name']} | {col['datatype']} | {col['not_null']} | {col['meaning']} |")
        lines += ['', 'Primary key: `'+', '.join(table['primary_key'])+'`. Foreign keys: `'+json.dumps(table['foreign_keys'])+'`.','',
            'Indexes: `'+json.dumps(table['indexes'])+'`.','']
    return '\n'.join(lines)+'\n'
