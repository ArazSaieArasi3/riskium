"""Build the versioned, scoped explicit-data profile for four source constraints."""
import json
import hashlib
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, BNode
from rdflib.collection import Collection

ROOT = Path(__file__).resolve().parents[1]
RISK = Namespace("https://github.com/ArazSaieArasi3/riskium/ontologies/riskium/0.3.1#")
S = Namespace("https://github.com/ArazSaieArasi3/riskium/shapes/0.1.0#")
SH = Namespace("http://www.w3.org/ns/shacl#")
VERSION_RULES = (("Context", "RX-014", "RKM-C032", "RKM-C002", "R-45"),
                 ("Method", "RX-015", "RKM-C032", "RKM-C035", "R-46"),
                 ("Scale", "RX-016", "RKM-C034", "RKM-C036", "R-14"),
                 ("Criteria", "RX-013", "RKM-X04", "RKM-C072", None))
OUT = ROOT / "ontology/shacl/0.1.0"


def fresh():
    g = Graph()
    for prefix, ns in (("risk", RISK), ("s", S), ("sh", SH), ("owl", OWL)):
        g.bind(prefix, ns)
    return g


def node(g, name, cls=None, props=()):
    n = S[name]
    g.add((n, RDF.type, SH.NodeShape))
    if cls:
        g.add((n, SH.targetClass, RISK[cls]))
        g.add((n, SH["class"], RISK[cls]))
    for prop in props:
        g.add((n, SH.targetSubjectsOf, RISK[prop]))
    return n


def prop(g, owner, name, path, minimum=None, maximum=None, cls=None):
    p = S[name]
    g.add((owner, SH.property, p)); g.add((p, RDF.type, SH.PropertyShape))
    g.add((p, SH.path, RISK[path]))
    if minimum is not None:
        g.add((p, SH.minCount, Literal(minimum)))
    if maximum is not None:
        g.add((p, SH.maxCount, Literal(maximum)))
    if cls:
        g.add((p, SH["class"], RISK[cls]))
    return p


def sparql(g, owner, name, query, message):
    c = S[name]
    g.add((owner, SH.sparql, c)); g.add((c, RDF.type, SH.SPARQLConstraint))
    g.add((c, SH.message, Literal(message)))
    g.add((c, SH.select, Literal("PREFIX risk: <" + str(RISK) + ">\n"
                               "PREFIX owl: <" + str(OWL) + ">\n" + query)))


def managed():
    g = fresh()
    n = node(g, "C06Relator", "RKM-C052", ("R-56", "R-57"))
    prop(g, n, "C06Bearer", "R-56", 1, 1, "RKM-C053")
    prop(g, n, "C06Authority", "R-57", 1, 1, "RKM-C054")
    n = node(g, "C06Distinct", "RKM-C052")
    sparql(g, n, "C06DistinctQuery", """SELECT $this WHERE {
        $this risk:R-56 ?bearer ; risk:R-57 ?authority .
        FILTER (?bearer = ?authority || NOT EXISTS { ?bearer owl:differentFrom ?authority })
    }""", "Mediation requires resolved distinct actors with explicit difference evidence.")
    n = node(g, "C08Anchor", "RKM-C070", ("RX-025", "RK2-020"))
    prop(g, n, "C08Indicator", "RX-025", None, 1, "RKM-C069")
    prop(g, n, "C08Scale", "RK2-020", None, 1, "RKM-C036")
    choices = []
    for name, path in (("C08IndicatorAlternative", "RX-025"), ("C08ScaleAlternative", "RK2-020")):
        alt = node(g, name)
        prop(g, alt, name + "Link", path, 1)
        choices.append(alt)
    head = BNode("threshold-alternatives"); Collection(g, head, choices)
    g.add((n, SH["or"], head))
    for label, path, source, artifact, direct in VERSION_RULES:
        n = node(g, "C25" + label, props=(path,))
        g.add((n, SH["class"], RISK[source]))
        link = prop(g, n, "C25" + label + "Link", path, cls="RKM-C015")
        version = node(g, "C25" + label + "Version")
        prop(g, version, "C25" + label + "VersionOf", "RX-006", 1, 1, artifact)
        g.add((link, SH.node, version))
        if direct:
            agreement = node(g, "C25" + label + "Agreement", props=(path,))
            sparql(g, agreement, "C25" + label + "AgreementQuery", f"""SELECT $this WHERE {{
                $this risk:{path} ?version ; risk:{direct} ?direct .
                ?version risk:RX-006 ?artifact . FILTER (?artifact != ?direct)
            }}""", "Direct artifact reference and selected versionOf target must agree after identity normalization.")
    return g


def publication(g):
    n = node(g, "C09PublishedDescription")
    g.add((n, SH["class"], RISK["RKM-C024"]))
    # No targetClass: the caller supplies a declared publication targetNode set.
    p = S.C09Aboutness; g.add((n, SH.property, p)); g.add((p, SH.minCount, Literal(1)))
    path, head = BNode("aboutness-path"), BNode("aboutness-members")
    g.add((p, SH.path, path)); g.add((path, SH.alternativePath, head))
    Collection(g, head, [RISK["RK2-007"], RISK["RK2-008"], RISK["R-37"]])
    for name, rel, cls in (("Case", "RK2-007", "RKM-X01"),
                            ("Pattern", "RK2-008", "RKM-C001"),
                            ("Scenario", "R-37", "RKM-C003")):
        prop(g, n, "C09" + name, rel, cls=cls)
    return g


def profiles():
    return {"raw": fresh(), "managed": managed(), "published": publication(managed()),
            "task-ready": publication(managed())}


def main():
    model = json.loads((ROOT / "ontology/riskium-model.json").read_text())
    source_digest=hashlib.sha256((ROOT / "ontology/riskium-model.json").read_bytes()).hexdigest()
    reviewed=json.loads((ROOT / "evaluation/native-review-decisions.json").read_text())
    if reviewed["source_model_sha256"]!=source_digest or model["version"]!="0.3.1":
        raise ValueError("Reviewed source version/digest changed")
    relations = {r["id"]: r for r in model["associations"]}
    expected = {"R-56": ("RKM-C052", "RKM-C053"), "R-57": ("RKM-C052", "RKM-C054"),
                "RX-025": ("RKM-C070", "RKM-C069"), "RK2-020": ("RKM-C070", "RKM-C036"),
                "RK2-007": ("RKM-C024", "RKM-X01"), "RK2-008": ("RKM-C024", "RKM-C001"),
                "R-37": ("RKM-C024", "RKM-C003"), "RX-006": ("RKM-C015", "RKM-C014")}
    for _, rel, source, artifact, direct in VERSION_RULES:
        expected[rel] = (source, "RKM-C015")
        if direct: expected[direct] = (source, artifact)
    for identifier, endpoints in expected.items():
        r = relations[identifier]
        if (r["source"], r["target"]) != endpoints or r["scope_layer"] != "FORMAL_CORE":
            raise ValueError("Reviewed SHACL signature changed: " + identifier)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, g in profiles().items():
        g.serialize(destination=OUT / (name + ".ttl"), format="turtle")
    receipt = dict(profile_version="0.1.0", source_sha256=source_digest,
        constraints=["C-06", "C-08", "C-09", "C-25"],
        profiles_sha256={p.stem: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob("*.ttl"))},
        status="SCOPED_PROFILE_GENERATED_NOT_DOMAIN_VALIDATED")
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps({k: len(v) for k, v in profiles().items()}))


if __name__ == "__main__":
    main()
