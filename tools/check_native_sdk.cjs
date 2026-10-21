/* Supplemental verification using ontouml-js 0.4.1, not a reader for schema 1.0.2. */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const sdkRoot = process.argv[2];
if (!sdkRoot) throw new Error('Pass the directory containing the installed ontouml-js package.');
// The dependency uses networkInterfaces only to seed generated IDs. All model IDs
// below are supplied explicitly. No verification rule is patched.
require('node:os').networkInterfaces = () => ({});
const sdkPath = path.resolve(sdkRoot);
const o = require(sdkPath);
const pkg = JSON.parse(fs.readFileSync(path.join(sdkPath, 'package.json')));
if (pkg.version !== '0.4.1') throw new Error('Expected the reviewed SDK version 0.4.1.');
const root = path.resolve(__dirname, '..');
const nativePath = path.join(root, 'ontology/native/riskium.ontouml.json');
const raw = fs.readFileSync(nativePath);
const doc = JSON.parse(raw);
const by = new Map(doc.elements.map(e => [e.id, e]));
const project = new o.Project({id: doc.id, name: 'Riskium'});
const model = project.createModel({id: doc.root, name: 'Riskium'});
const classes = new Map();
for (const e of doc.elements.filter(e => e.type === 'Class')) {
  const c = new o.Class({id: e.id, name: e.name, stereotype: e.stereotype,
    restrictedTo: e.restrictedTo, isAbstract: e.isAbstract, order: e.order});
  // Preserve unknown legacy-only extensionality instead of accepting the SDK's
  // implicit false default. Its missing-field finding is retained in the report.
  c.isExtensional = null;
  model.addContent(c);
  classes.set(e.id, c);
}
const gs = new Map();
for (const e of doc.elements.filter(e => e.type === 'Generalization')) {
  gs.set(e.id, model.createGeneralization(classes.get(e.general), classes.get(e.specific), null, {id: e.id}));
}
for (const e of doc.elements.filter(e => e.type === 'GeneralizationSet')) {
  model.createGeneralizationSet(e.generalizations.map(i => gs.get(i)), e.isDisjoint, e.isComplete, null, null, {id: e.id});
}
for (const e of doc.elements.filter(e => e.type === 'BinaryRelation')) {
  const ends = e.properties.map(i => by.get(i));
  const r = model.createBinaryRelation(classes.get(ends[0].propertyType), classes.get(ends[1].propertyType), e.name, e.stereotype, {id: e.id});
  [r.getSourceEnd(), r.getTargetEnd()].forEach((end, i) => {
    end.id = ends[i].id;
    end.cardinality = new o.Cardinality(ends[i].cardinality);
  });
}
const issues = o.OntoumlVerification.verify(project).map(i => ({code: i.code, severity: i.severity,
  source: i.data.source.id, title: i.title, description: i.description}));
const tally = {};
for (const i of issues) tally[i.code] = (tally[i.code] || 0) + 1;
const rulesFiles = ['class_verification.js', 'generalization_verification.js',
  'relation_verification.js', 'property_verification.js', 'generalization_set_verification.js'];
const ruleDigests = {};
for (const f of rulesFiles) ruleDigests[f] = crypto.createHash('sha256').update(fs.readFileSync(path.join(sdkPath, 'dist/libs/verification', f))).digest('hex');
const report = {engine: 'ontouml-js', version: pkg.version, node: process.version,
  source_native_sha256: crypto.createHash('sha256').update(raw).digest('hex'),
  input_method: 'Reconstructed SDK objects from schema-1.0.2 typed classes, relations, generalizations and sets; not direct schema-1.0.2 import.',
  runtime_adjustment: 'networkInterfaces returns an empty object for generated-ID initialization; all model IDs are explicit; verifier rules unchanged.',
  status: issues.length ? 'FINDINGS_RETAINED' : 'NO_FINDINGS_IN_IMPLEMENTED_RULES',
  class_count: classes.size, generalization_count: gs.size,
  findings_by_code: tally, findings: issues, verifier_file_sha256: ruleDigests,
  limitations: ['Relation, property and generalization-set verification functions in this SDK version contain no implemented rules.',
    'Legacy-only isExtensional was left unknown. Missing-field findings are compatibility findings, not silently resolved domain decisions.',
    'No GUI import, full semantic certification, HermiT or SHACL execution is established.']};
console.log(JSON.stringify(report, null, 2));
if (process.argv.includes('--write')) fs.writeFileSync(path.join(root, 'evaluation/native-sdk-checks.json'), JSON.stringify(report, null, 2) + '\n');
// Findings remain visible; invocation success is not reported as model conformance.
