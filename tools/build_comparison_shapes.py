"""C-13/C-18 explicit selection and comparison policy, outside native OWL."""
import hashlib
import json
from rdflib import BNode, Graph, Literal, Namespace, OWL, RDF, URIRef
from rdflib.collection import Collection
from build_shacl import ROOT, RISK, SH
from build_coherence_shapes import prepare as prepare_base

C = Namespace("https://github.com/ArazSaieArasi3/riskium/shapes/0.7.0#")
SP = Namespace("https://github.com/ArazSaieArasi3/riskium/profiles/comparison/0.7.0#")
OUT = ROOT / "ontology/shacl/0.7.0"
POLICY = ROOT / "evaluation/shacl/comparison/profile-policy.json"
SIGNATURES = {"R-12":("RKM-C032","RKM-C033"),"R-13":("RKM-C032","RKM-C034"),
 "R-14":("RKM-C034","RKM-C036"),"R-15":("RKM-C034","RKM-C038"),
 "R-16":("RKM-C038","RKM-C036"),"R-45":("RKM-C032","RKM-C002"),
 "R-46":("RKM-C032","RKM-C035"),"R-48":("RKM-C034","RKM-C039"),
 "R-49":("RKM-C035","RKM-C036"),"RX-006":("RKM-C015","RKM-C014"),
 "RX-014":("RKM-C032","RKM-C015"),"RX-015":("RKM-C032","RKM-C015"),
 "RX-016":("RKM-C034","RKM-C015"),"RK2-018":("RKM-C035","RKM-C039"),
 "RK2-019":("RKM-C036","RKM-C039")}
SELECTORS = (SP.leftAssessment, SP.leftResult, SP.rightAssessment, SP.rightResult)
PAIRS = {"Method":("assessment","R-46"), "MethodVersion":("assessment","RX-015"),
 "Scale":("result","R-14"),"ScaleVersion":("result","RX-016"),"Dimension":("result","R-48"),
 "Basis":("assessment","R-12"),"BasisVersion":("assessment",SP.basisVersion),
 "Context":("assessment","R-45"),"ContextVersion":("assessment","RX-014"),
 "Temporal":("assessment",SP.temporalContext)}


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(raw, profile, request):
    if profile not in ("raw", "direct-comparison"): raise ValueError("Unsupported comparison profile")
    if len(request) != 5 or any(not isinstance(n, URIRef) for n in request):
        raise ValueError("Caller must supply five named request/assessment/result identities")
    if profile != "raw":
        if any(p in SELECTORS for _,p,_ in raw): raise ValueError("Input cannot supply caller focus selectors")
        for p in (OWL.sameAs, OWL.differentFrom):
            for a,b in raw.subject_objects(p):
                if any(str(n).startswith((str(C),str(SP))) for n in (a,b)):
                    raise ValueError("Identity cannot rewrite reserved comparison vocabulary")
    return prepare_base(raw, "raw" if profile == "raw" else "managed")


def render():
    model_path=ROOT/"ontology/riskium-model.json"; contract_path=ROOT/"evaluation/coverage-review.json"
    model=json.loads(model_path.read_text()); policy=json.loads(POLICY.read_text())
    native=json.loads((ROOT/"evaluation/native-review-decisions.json").read_text())
    if model["version"]!="0.3.1" or native["source_model_sha256"]!=digest(model_path): raise ValueError("Native source changed")
    if policy["source_sha256"]!=digest(model_path) or policy["contract_sha256"]!=digest(contract_path): raise ValueError("Policy source changed")
    relations={r["id"]:r for r in model["associations"]}
    for rid,pair in SIGNATURES.items():
        r=relations[rid]
        if (r["source"],r["target"])!=pair or r["scope_layer"]!="FORMAL_CORE": raise ValueError("Relation changed: "+rid)
    constraints={c["id"]:c for c in model["constraints"]}; rows=[]
    for row in json.loads(contract_path.read_text())["obligation_reviews"]:
        if row["source_element"] in ("C-13","C-18"):
            sha=hashlib.sha256(json.dumps(constraints[row["source_element"]],sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
            if sha!=row["source_element_sha256"]: raise ValueError("Constraint changed")
            rows.append({k:row[k] for k in ("obligation_id","engine","source_element","source_element_sha256")})
    if len(rows)!=4: raise ValueError("Expected two engine rows per constraint")
    g=Graph()
    for prefix,ns in (("cmp",C),("sp",SP),("risk",RISK),("sh",SH)):g.bind(prefix,ns)
    owners={"selection":[],"comparison":[]}
    def node(name,group,cls=None):
        n=C[name];owners[group].append(str(n));g.add((n,RDF.type,SH.NodeShape))
        if cls:g.add((n,SH["class"],RISK[cls]))
        g.add((n,SH.nodeKind,SH.IRI));return n
    def path_node(name,path):
        if len(path)==1:return path[0]
        head=BNode(name+"-path");Collection(g,head,path);return head
    def prop(owner,name,path,cls=None):
        p=C[name];g.add((owner,SH.property,p));g.add((p,RDF.type,SH.PropertyShape))
        g.add((p,SH.path,path_node(name,path)));g.add((p,SH.minCount,Literal(1)))
        g.add((p,SH.maxCount,Literal(1)));g.add((p,SH.nodeKind,SH.IRI))
        if cls:g.add((p,SH["class"],RISK[cls]))
    n=node("Selection","selection","RKM-C034")
    for name,path,cls in (("Scale",[RISK["R-14"]],"RKM-C036"),("Level",[RISK["R-15"]],"RKM-C038"),
        ("Dimension",[RISK["R-48"]],"RKM-C039"),("ScaleVersion",[RISK["RX-016"]],"RKM-C015"),
        ("LevelScale",[RISK["R-15"],RISK["R-16"]],"RKM-C036"),
        ("LevelVersion",[RISK["R-15"],SP.levelScaleVersion],"RKM-C015"),
        ("ScaleDimension",[RISK["R-14"],RISK["RK2-019"]],"RKM-C039"),
        ("ScaleVersionTarget",[RISK["RX-016"],RISK["RX-006"]],"RKM-C036"),
        ("LevelVersionTarget",[RISK["R-15"],SP.levelScaleVersion,RISK["RX-006"]],"RKM-C036")):
        prop(n,"Selection"+name,path,cls)
    n=node("Comparison","comparison")
    for side in ("Left","Right"):
        ap=SP[side.lower()+"Assessment"]
        prop(n,side+"Assessment",[ap],"RKM-C032")
        for name,field,cls in (("Method","R-46","RKM-C035"),("MethodVersion","RX-015","RKM-C015"),
            ("Basis","R-12","RKM-C033"),("BasisVersion",SP.basisVersion,"RKM-C015"),
            ("Context","R-45","RKM-C002"),("ContextVersion","RX-014","RKM-C015"),
            ("Temporal",SP.temporalContext,None),("Source",SP.source,None)):
            predicate=RISK[field] if isinstance(field,str) and not isinstance(field,URIRef) else field
            prop(n,side+name,[ap,predicate],cls)
        for name,field,cls in (("MethodVersionTarget",RISK["RX-015"],"RKM-C035"),
                ("BasisVersionTarget",SP.basisVersion,"RKM-C033"),("ContextVersionTarget",RISK["RX-014"],"RKM-C002")):
            prop(n,side+name,[ap,field,RISK["RX-006"]],cls)
    prefix="PREFIX risk: <"+str(RISK)+">\nPREFIX sp: <"+str(SP)+">\nPREFIX owl: <"+str(OWL)+">\n"
    def query(name,group,body):
        owner=node(name,group);q=C[name+"Query"];g.add((owner,SH.sparql,q));g.add((q,RDF.type,SH.SPARQLConstraint))
        g.add((q,SH.select,Literal(prefix+"SELECT DISTINCT $this WHERE {\n"+body+"\n}")))
        g.add((q,SH.message,Literal(name+": exact declarations and explicit identity evidence govern this task.")))
    def compare(name,group,body):
        body+="\nFILTER (?a != ?b)\n"
        query(name+"Mismatch",group,body+"FILTER EXISTS { ?a owl:differentFrom ?b }")
        query(name+"Unknown",group,body+"FILTER NOT EXISTS { ?a owl:differentFrom ?b }")
    for name,body in (
        ("LevelScale","$this risk:R-15/risk:R-16 ?a ; risk:R-14 ?b ."),
        ("LevelVersion","$this risk:R-15/sp:levelScaleVersion ?a ; risk:RX-016 ?b ."),
        ("SelectedDimension","$this risk:R-48 ?a ; risk:R-14/risk:RK2-019 ?b ."),
        ("ScaleVersionBinding","$this risk:RX-016/risk:RX-006 ?a ; risk:R-14 ?b ."),
        ("LevelVersionBinding","$this risk:R-15/sp:levelScaleVersion/risk:RX-006 ?a ; risk:R-14 ?b .")):
        compare(name,"selection",body)
    for side in ("Left","Right"):
        selector=side.lower();anchors=f"$this sp:{selector}Assessment ?assessment ; sp:{selector}Result ?result .\n"
        query(side+"MissingMembership","comparison",anchors+"FILTER NOT EXISTS { ?assessment risk:R-13 ?result }")
        query(side+"MissingScalePermission","comparison",anchors+"?assessment risk:R-46 ?method . ?result risk:R-14 ?scale . FILTER NOT EXISTS { ?method risk:R-49 ?scale }")
        query(side+"MissingDimensionPermission","comparison",anchors+"?assessment risk:R-46 ?method . ?result risk:R-48 ?dimension . FILTER NOT EXISTS { ?method risk:RK2-018 ?dimension }")
        for name,version,artifact in (("MethodBinding","risk:RX-015","risk:R-46"),
            ("BasisBinding","sp:basisVersion","risk:R-12"),("ContextBinding","risk:RX-014","risk:R-45")):
            compare(side+name,"comparison",anchors+f"?assessment {version}/risk:RX-006 ?a ; {artifact} ?b .")
    for name,(kind,field) in PAIRS.items():
        selector="Assessment" if kind=="assessment" else "Result"
        predicate="<"+str(field)+">" if isinstance(field,URIRef) else "risk:"+field
        body=f"$this sp:left{selector}/{predicate} ?a ; sp:right{selector}/{predicate} ?b ."
        compare("Pair"+name,"comparison",body)
    return g,dict(profile_version="0.7.0",source_sha256=digest(model_path),contract_sha256=digest(contract_path),
        policy_sha256=digest(POLICY),obligations=rows,relation_signatures=SIGNATURES,target_owners=owners,
        native_semantics_changed=False,scope="Selected level/version/dimension joins and strict direct-comparison eligibility; no numeric ranking/calculation/transformations")


def main():
    g,receipt=render();OUT.mkdir(parents=True,exist_ok=True);g.serialize(destination=OUT/"comparison.ttl",format="turtle")
    receipt["shapes_sha256"]=digest(OUT/"comparison.ttl");(OUT/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({"profile":"0.7.0","triples":len(g)}))


if __name__=="__main__":main()
