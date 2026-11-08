/* Direct SDK interoperability for the isolated candidate, not a GUI/semantic certification. */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
require('node:os').networkInterfaces = () => ({}); // Generated-ID seed only; source IDs remain explicit.
const [input, sdkDir, output] = process.argv.slice(2);
if (!input || !sdkDir || !output) throw new Error('Pass native input, SDK directory and report output.');
const sdkPath=path.resolve(sdkDir), sdk=require(sdkPath);
const pkg=JSON.parse(fs.readFileSync(path.join(sdkPath,'package.json')));
if (pkg.version!=='1.0.0') throw new Error('Expected pinned SDK 1.0.0.');
const raw=fs.readFileSync(input), before=JSON.parse(raw);
const after=JSON.parse(sdk.serializationUtils.serialize(sdk.serializationUtils.parse(raw.toString()),2));
const by=new Map(after.elements.map(e=>[e.id,e])), errors=[];
if(before.elements.length!==after.elements.length||by.size!==after.elements.length) errors.push('Element allocation changed');
const common=['id','type','name','description'];
const fields={Class:['stereotype','isAbstract','restrictedTo','order','properties','literals'],BinaryRelation:['stereotype','properties'],Property:['propertyType','cardinality'],Generalization:['specific','general'],GeneralizationSet:['generalizations','isDisjoint','isComplete'],Package:['contents'],Note:['text']};
for(const e of before.elements){
 const r=by.get(e.id);
 if(!r){errors.push('Missing '+e.id);continue;}
 for(const key of common.concat(fields[e.type]||[])) if(JSON.stringify(e[key])!==JSON.stringify(r[key]))errors.push(e.id+':'+key);
 for(const [key,val] of Object.entries(e.customProperties||{})) if(JSON.stringify(val)!==JSON.stringify(r.customProperties?.[key]))errors.push(e.id+':customProperties:'+key);
}
const report={engine:'ontouml-js',version:pkg.version,node:process.version,input_sha256:crypto.createHash('sha256').update(raw).digest('hex'),checked_elements:before.elements.length,status:errors.length?'FAIL':'PASS',errors,
 scope:'Direct parse/serialize and source-invariant preservation; not GUI import or independent conceptual acceptance.',runtime_adjustment:'networkInterfaces returns an empty object for generated-ID seeding; source IDs and SDK serializer rules are unchanged.'};
fs.writeFileSync(output,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({status:report.status,elements:report.checked_elements,errors:errors.length}));
process.exitCode=errors.length?1:0;
