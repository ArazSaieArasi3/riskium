"""Losslessly archive full admission graph snapshots and emit a readable index."""
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evaluation/shacl/admission"


def sha(value):
    return hashlib.sha256(value).hexdigest()


def main():
    raw = (OUT / "report.json").read_bytes()
    report = json.loads(raw)
    if report["coverage"]["passed"] != 80 or any(c["status"] != "PASS" for c in report["cases"]):
        raise SystemExit("Cannot package an incomplete or failed admission receipt")
    for path, expected in report["inputs"].items():
        if sha((ROOT / path).read_bytes()) != expected:
            raise SystemExit("Receipt input changed: " + path)
    compressed = gzip.compress(raw, mtime=0)
    if gzip.decompress(compressed) != raw:
        raise SystemExit("Archive round-trip changed receipt bytes")
    (OUT / "report.json.gz").write_bytes(compressed)
    index = {k: v for k, v in report.items() if k not in ("graphs", "cases")}
    index["archive"] = dict(path="report.json.gz", encoding="gzip of UTF-8 JSON",
        compressed_sha256=sha(compressed), uncompressed_sha256=sha(raw),
        compressed_bytes=len(compressed), uncompressed_bytes=len(raw),
        packaging_code_sha256=sha(Path(__file__).read_bytes()),
        graph_snapshot_count=len(report["graphs"]), lossless_round_trip_verified=True)
    index["cases"] = [{k: c[k] for k in ("id", "source_elements", "family", "profile", "status", "observed", "engine_executed")}
                      for c in report["cases"]]
    (OUT / "report-index.json").write_text(json.dumps(index, indent=2) + "\n")
    md = (OUT / "report.md").read_text().replace("[JSON receipt](report.json)",
        "[lossless full JSON archive](report.json.gz) and [readable index](report-index.json)")
    md = md.replace(".venv-shacl/bin/python tools/summarize_shacl.py",
        ".venv-shacl/bin/python tools/package_admission_receipt.py\n.venv-shacl/bin/python tools/summarize_shacl.py")
    (OUT / "report.md").write_text(md)
    print(json.dumps(index["archive"]))


if __name__ == "__main__":
    main()
