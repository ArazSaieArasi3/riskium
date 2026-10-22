"""Check source digests and replay selected frozen C-11/C-12 graph pairs."""
import hashlib
import gzip
import json

from pyshacl import validate
from rdflib import RDF

from build_shacl import ROOT, SH
from run_admission_shacl import reconstruct_pair

PATH = ROOT / "evaluation/shacl/qualification/report.json.gz"
SELECTED = ("VOC-DUPLICATE-KEY", "VOC-OTHER-SCHEME", "VOC-SCHEME-MISMATCH",
            "EVIDENCE-CHALLENGE-WITH-SUPPORT-PAIR", "EVIDENCE-MISSING-ITEM-PAIR",
            "EVIDENCE-INTEGRATED")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    report = json.loads(gzip.decompress(PATH.read_bytes()).decode())
    input_match = all(digest((ROOT / path).read_bytes()) == sha for path, sha in report["inputs"].items())
    graph_match = all(digest(record["text"].encode()) == sha for sha, record in report["graphs"].items())
    case_lookup = {row["id"]: row for row in report["cases"]}
    replays = []
    for identifier in SELECTED:
        row = case_lookup[identifier]
        data, shapes = reconstruct_pair(report, row)
        conforms, result, _ = validate(data_graph=data, shacl_graph=shapes, inference="none",
                                        meta_shacl=True, do_owl_imports=False, advanced=False)
        root = next(result.subjects(RDF.type, SH.ValidationReport))
        found = sorted((str(result.value(n, SH.sourceShape)),
                        str(result.value(n, SH.sourceConstraintComponent)),
                        str(result.value(n, SH.focusNode))) for n in result.objects(root, SH.result))
        replays.append(dict(id=identifier, matched=(found == sorted(map(tuple, row["violations"])) and
                            bool(conforms) == (row["observed"] == "CONFORMS"))))
    output = dict(source_commit=report["source_commit"], report_sha256=digest(PATH.read_bytes()),
                  cases=len(report["cases"]), engine_executions=sum(x["engine_executed"] for x in report["cases"]),
                  all_input_digests_match=input_match, all_graph_snapshot_digests_match=graph_match,
                  snapshot_replays=replays, outcomes={o["id"]:o["outcome"] for o in report["obligations"]},
                  limitations=report["limitations"])
    path = PATH.with_name("verification.json"); path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(dict(input_match=input_match,graph_match=graph_match,
                          replays=sum(x["matched"] for x in replays),cases=len(report["cases"]))))
    if not input_match or not graph_match or not all(x["matched"] for x in replays):
        raise SystemExit(1)


if __name__ == "__main__":main()
