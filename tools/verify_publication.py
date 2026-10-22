"""Verify served index bytes and selected artifacts after publication, without execution."""
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from urllib.request import build_opener

from catalog import (
    POLICY,
    BoundedRedirect,
    canonical,
    fetch_artifact,
    https_url,
    parse_json,
    validate_index,
)


def verify(index_url, expected_path, previous_path=None):
    expected_bytes = expected_path.read_bytes()
    expected = validate_index(parse_json(expected_bytes))
    previous = validate_index(parse_json(previous_path.read_bytes())) if previous_path else {"entries": []}
    with build_opener(BoundedRedirect()).open(https_url(index_url), timeout=30) as response:
        actual = response.read(4 * 1024 * 1024 + 1)
    validate_index(parse_json(actual))
    if actual != expected_bytes:
        raise ValueError("served index differs from the checked publication")
    previous_blocks = {(d["id"], d["version"], d["sha256"]) for d in previous.get("security", []) if d["status"] == "blocked"}
    old = {(e["id"], e["version"], e["sha256"], e["url"]) for e in previous["entries"]
           if not e["withdrawal"] and (e["id"], e["version"], e["sha256"]) not in previous_blocks}
    blocked = {(d["id"], d["version"], d["sha256"]) for d in expected["security"] if d["status"] == "blocked"}
    checked, skipped = [], []
    with tempfile.TemporaryDirectory(prefix="publication-availability-") as temporary:
        for entry in expected["entries"]:
            identity = {key: entry[key] for key in ("id", "version", "sha256")}
            key = (entry["id"], entry["version"], entry["sha256"], entry["url"])
            # Withdrawal/security publication must survive unavailable retired assets.
            if entry["withdrawal"] or (entry["id"], entry["version"], entry["sha256"]) in blocked or key in old:
                skipped.append({**identity, "reason": "withdrawn, blocked or unchanged published artifact"})
                continue
            wheel = fetch_artifact({"wheel": {"url": entry["url"], "sha256": entry["sha256"]}}, Path(temporary))
            if wheel.stat().st_size != entry["size"] or wheel.stat().st_size > POLICY["max_wheel_bytes"]:
                raise ValueError("served artifact size differs from checked publication")
            checked.append(identity)
    return {"ok": True, "sequence": expected["sequence"],
            "index_sha256": hashlib.sha256(actual).hexdigest(),
            "checked_artifacts": checked, "skipped_artifacts": skipped,
            "scope": "exact index and newly distributed/relocated artifacts; not human approval"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index-url", required=True)
    parser.add_argument("--expected", type=Path, required=True)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = verify(args.index_url, args.expected, args.previous)
    except (OSError, ValueError, KeyError) as exc:
        result = {"ok": False, "error": str(exc), "next_step": "Do not mark this publication live; inspect endpoint and immutable artifacts."}
    args.output.write_bytes(canonical(result))
    print(json.dumps({"ok": result["ok"]}))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
