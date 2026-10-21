/* Direct schema-1.0.2 parse/serialize check using the current OntoUML SDK. */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const os = require('node:os');
const sdkPath = path.resolve(process.argv[2] || 'tools/native-sdk/node_modules/ontouml-js-current');
os.networkInterfaces = () => ({}); // Only the generated-ID seed; explicit model IDs are retained.
const o = require(sdkPath);
const pkg = JSON.parse(fs.readFileSync(path.join(sdkPath, 'package.json')));
if (pkg.version !== '1.0.0') throw new Error('Expected the reviewed SDK version 1.0.0.');
const root = path.resolve(__dirname, '..');
const raw = fs.readFileSync(path.join(root, 'ontology/native/riskium.ontouml.json'));
const before = JSON.parse(raw);
const afterText = o.serializationUtils.serialize(o.serializationUtils.parse(raw.toString()), 2);
const after = JSON.parse(afterText);
const by = new Map(after.elements.map(e => [e.id, e]));
const errors = [];
if (before.elements.length !== after.elements.length || by.size !== after.elements.length) errors.push('Element allocation changed.');
const common = ['id', 'type', 'name', 'description'];
const specific = {Class: ['stereotype', 'isAbstract', 'restrictedTo', 'order', 'properties', 'literals'],
  BinaryRelation: ['stereotype', 'properties'], Property: ['propertyType', 'cardinality'],
  Generalization: ['specific', 'general'], GeneralizationSet: ['generalizations', 'isDisjoint', 'isComplete'],
  Package: ['contents'], Note: ['text']};
const normalizations = {};
for (const e of before.elements) {
  const r = by.get(e.id);
  if (!r) {errors.push('Missing element: ' + e.id); continue;}
  for (const key of common.concat(specific[e.type] || [])) {
    if (JSON.stringify(e[key]) !== JSON.stringify(r[key])) errors.push('Invariant changed: ' + e.id + ':' + key);
  }
  for (const key of Object.keys(e)) {
    if (JSON.stringify(e[key]) !== JSON.stringify(r[key])) normalizations[key] = (normalizations[key] || 0) + 1;
  }
  for (const [key, value] of Object.entries(e.customProperties || {})) {
    if (JSON.stringify(r.customProperties?.[key]) !== JSON.stringify(value)) errors.push('Custom source metadata changed: ' + e.id + ':' + key);
  }
}
const report = {engine: 'ontouml-js', version: pkg.version, node: process.version,
  source_native_sha256: crypto.createHash('sha256').update(raw).digest('hex'),
  status: errors.length ? 'failed' : 'passed', errors,
  checked_elements: before.elements.length, method: 'Direct official SDK parse, serialize and invariant comparison.',
  field_normalizations: normalizations,
  normalization_disposition: 'SDK normalizes date representation, empty metadata and nullable defaults. The normalized output is not adopted as the canonical export; known source fields and declared set policy must remain equal.',
  runtime_adjustment: 'networkInterfaces returns an empty object for generated-ID seeding; verification/serialization rules are unchanged.',
  limitations: ['Not a GUI/editor import test or complete semantic verification.', 'HermiT and SHACL remain unexecuted.']};
if (process.argv.includes('--write') && !errors.length) fs.writeFileSync(path.join(root, 'evaluation/native-roundtrip-checks.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
process.exitCode = errors.length ? 1 : 0;
