"""Hash every tracked blob in an exact Git commit for a release inventory."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, stdout=subprocess.PIPE
    ).stdout


def inventory(ref):
    commit = git("rev-parse", "--verify", f"{ref}^{{commit}}").decode().strip()
    entries = []
    for record in git("ls-tree", "-r", "-z", commit).split(b"\0"):
        if not record:
            continue
        header, path = record.split(b"\t", 1)
        mode, kind, blob = header.split(b" ")
        if kind != b"blob":
            raise ValueError(f"Non-file entry in release tree: {path!r}")
        data = git("cat-file", "blob", blob.decode("ascii"))
        entries.append({
            "path": path.decode("utf-8"),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })
    return {
        "schema": "riskium-release-inventory-v1",
        "source_commit": commit,
        "scope": "all tracked files at source_commit; no untracked files or external Wiki Git history",
        "file_count": len(entries),
        "total_bytes": sum(item["bytes"] for item in entries),
        "files": entries,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="HEAD", help="Git commit or ref to inventory")
    parser.add_argument("--output", type=Path, help="Write JSON to this path (prefer outside the repository)")
    parser.add_argument("--verify", type=Path, help="Verify a previously generated manifest")
    args = parser.parse_args()
    if args.verify and args.output:
        parser.error("--output and --verify are mutually exclusive")
    if args.verify:
        expected = json.loads(args.verify.read_text(encoding="utf-8"))
        actual = inventory(expected["source_commit"])
        if actual != expected:
            raise SystemExit("Manifest differs from its pinned Git commit")
        print(json.dumps({"status": "verified", "source_commit": actual["source_commit"],
                          "file_count": actual["file_count"], "total_bytes": actual["total_bytes"]}))
        return
    result = inventory(args.ref)
    data = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(data, encoding="utf-8")
        print(json.dumps({"status": "written", "source_commit": result["source_commit"],
                          "file_count": result["file_count"], "total_bytes": result["total_bytes"],
                          "output": str(args.output)}))
    else:
        print(data, end="")


if __name__ == "__main__":
    main()
