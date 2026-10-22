"""Run from protected base, consuming a proposed tree as data; never execute its wheels."""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from catalog import (
    PIN,
    ROOT,
    build_entry,
    canonical,
    fetch_artifact,
    read_json,
    retained_entry,
    validate_index,
    validate_transition,
    verify_host,
    wheel_diff,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proposal", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--host", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--artifacts", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    args.evidence.mkdir(parents=True, exist_ok=True)
    profile = verify_host(args.host, args.python)
    previous = read_json(ROOT / "catalog/v1/index.json")
    candidate_safety = {
        **previous,
        "sequence": previous["sequence"] + 1,
        "security": read_json(args.proposal / "catalog/security.json"),
    }
    validate_transition(previous, candidate_safety)
    # Input PR: check actual wheels and emit diffs. The PR does not grant publication authority.
    for path in sorted((args.proposal / "catalog/packages").rglob("*.json")):
        source = read_json(path)
        if retained_entry(source, previous) is not None:
            continue
        wheel = fetch_artifact(source, args.artifacts)
        entry = build_entry(source, args.artifacts, args.host, args.python, profile)
        older = [
            e
            for e in previous["entries"]
            if e["id"] == entry["id"] and e["sha256"] != entry["sha256"]
        ]
        older.sort(key=lambda e: tuple(int(n) for n in e["version"].split(".")))
        before = None
        if older:
            old = older[-1]
            before = fetch_artifact(
                {"wheel": {"url": old["url"], "sha256": old["sha256"]}}, args.artifacts
            )
        # Digest is the filename; a submitted package ID never becomes a local path.
        (args.evidence / (entry["sha256"] + ".json")).write_bytes(
            canonical(
                {
                    "identity": entry["id"],
                    "review_status": "requires_human_review",
                    "changes": wheel_diff(before, wheel),
                }
            )
        )
    proposed = validate_index(read_json(args.proposal / "catalog/v1/index.json"))
    validate_transition(previous, proposed)
    if canonical(previous) == canonical(proposed):
        print(json.dumps({"ok": True, "publication": False}))
        return 0
    # Generator/input commits must both already belong to protected main.
    for commit in (proposed["source_commit"], proposed["generator_commit"]):
        subprocess.run(
            [
                "git",
                "-C",
                str(args.proposal),
                "merge-base",
                "--is-ancestor",
                commit,
                args.base,
            ],
            check=True,
            capture_output=True,
        )
    # A separate disposable checkout runs exactly the approved generator version.
    with tempfile.TemporaryDirectory(prefix="catalog-generator-") as temporary:
        checkout = Path(temporary) / "generator"
        subprocess.run(
            ["git", "clone", "--shared", "--no-checkout", str(ROOT), str(checkout)],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(checkout),
                "checkout",
                "--detach",
                proposed["generator_commit"],
            ],
            check=True,
            capture_output=True,
        )
        generator_pin = read_json(checkout / "catalog/toolchain.json")
        if generator_pin != PIN:
            raise ValueError("qualify a changed Host pin before publication")
        old = Path(temporary) / "previous.json"
        old.write_bytes(canonical(previous))
        command = [
            str(args.python),
            str(checkout / "tools/build_catalog.py"),
            "--source-repo",
            str(args.proposal.resolve()),
            "--source-commit",
            proposed["source_commit"],
            "--approved-ref",
            args.base,
            "--sequence",
            str(proposed["sequence"]),
            "--previous",
            str(old),
            "--host",
            str(args.host.resolve()),
            "--python",
            str(args.python.resolve()),
            "--artifacts",
            str(args.artifacts.resolve()),
            "--output",
            str((args.proposal / "catalog/v1/index.json").resolve()),
            "--fetch",
            "--check",
        ]
        subprocess.run(command, check=True)
    print(json.dumps({"ok": True, "publication": True}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError):
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "catalog CI rejected input, review, pin or publication transition",
                }
            )
        )
        raise SystemExit(1)
