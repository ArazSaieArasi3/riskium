"""Generate both ordered cardinality ends of all reviewed typed relations."""
import hashlib
import json
from pathlib import Path

from rdflib import BNode, Graph, Literal, Namespace, RDF
from build_shacl import ROOT, RISK, SH

E = Namespace("https://github.com/ArazSaieArasi3/riskium/shapes/0.2.0#")
OUT = ROOT / "ontology/shacl/0.2.0"


def bounds(text):
    parts=text.split("..")
    return int(parts[0]), (int(parts[0]) if len(parts)==1 else None if parts[1]=="*" else int(parts[1]))


def endpoint_shape(model, relation, end):
    """A source end counts sources per target, so its path is inverse."""
    rid=relation["id"]; name=rid+"-"+end
    focus=relation["target" if end=="source" else "source"]
    lo,hi=bounds(relation[end+"_end_cardinality"])
    g=Graph();g.bind("ep",E);g.bind("risk",RISK);g.bind("sh",SH)
    n,p=E[name],E[name+"-count"]
    g.add((n,RDF.type,SH.NodeShape));g.add((n,SH.targetClass,RISK[focus]))
    g.add((n,SH.property,p));g.add((p,RDF.type,SH.PropertyShape))
    path=RISK[rid]
    if end=="source":
        path=BNode(name+"-inverse");g.add((path,SH.inversePath,RISK[rid]))
    g.add((p,SH.path,path));g.add((p,SH.minCount,Literal(lo)))
    if hi is not None:g.add((p,SH.maxCount,Literal(hi)))
    return g


def render():
    path=ROOT/"ontology/riskium-model.json";model=json.loads(path.read_text())
    source_digest=hashlib.sha256(path.read_bytes()).hexdigest()
    policy=json.loads((ROOT/"evaluation/native-review-decisions.json").read_text())
    if model["version"]!="0.3.1" or policy["source_model_sha256"]!=source_digest:
        raise ValueError("Reviewed source version/digest changed")
    rels=[r for r in model["associations"] if r["scope_layer"]=="FORMAL_CORE"]
    if len(rels)!=127:raise ValueError("Reviewed relation inventory changed")
    graph=Graph();graph.bind("ep",E);graph.bind("risk",RISK);graph.bind("sh",SH)
    entries=[]
    for r in sorted(rels,key=lambda r:r["id"]):
        for end in ("source","target"):
            part=endpoint_shape(model,r,end)
            for t in part:graph.add(t)
            lo,hi=bounds(r[end+"_end_cardinality"])
            entries.append(dict(source_element=r["id"]+":"+end,
                shape=str(E[r["id"]+"-"+end]),property_shape=str(E[r["id"]+"-"+end+"-count"]),
                focus_class=r["target" if end=="source" else "source"],
                path="inverse" if end=="source" else "direct",property=r["id"],minimum=lo,maximum=hi))
    return graph,dict(profile_version="0.2.0",source_sha256=source_digest,
        typed_relations=127,ordered_endpoint_shapes=254,endpoints=entries,
        semantics="Unqualified RDF value-node counts after asserted identity normalization; no imports or OWL inference",
        limits="Cardinality module only; class admission and unrelated conditional shapes are separate modules")


def main():
    graph,receipt=render();OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/"endpoints.ttl";graph.serialize(destination=path,format="turtle")
    receipt["shapes_sha256"]=hashlib.sha256(path.read_bytes()).hexdigest()
    (OUT/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(dict(relations=127,endpoints=254,triples=len(graph))))


if __name__=="__main__":main()
